/**
 * Escena de exploración cenital (diseño técnico §5).
 * Movimiento directo (teclado o joystick táctil) o tocando/clicando (A*), colisiones,
 * puntos interactivos, personajes, transiciones pedidas desde ink y depuración.
 */
import Phaser from 'phaser';
import { narrativa, registro, mano, mision, segundos, LOCALIZACIONES, RESOLUCION, EV, tactil } from '../core/juego';
import { contains, cumple, overlaps, type Dir, type Hotspot, type LocationData, type Npc, type Point, type Rect } from '../core/Location';
import { NavGrid } from '../systems/Pathfinding';
import { Sigilo } from '../systems/Sigilo';
import { audio } from '../systems/AudioDirector';
import { SaveSystem } from '../core/SaveSystem';
import type { Tag } from '../core/tags';

export interface EntradaEscena {
  escena: string; spawn?: string; x?: number; y?: number; dir?: Dir; cargado?: boolean; reloj?: typeof mision.reloj;
}

/** Velocidad con la carpeta abierta (sigilo social): se camina leyendo. */
const VELOCIDAD_LEYENDO = 0.6;

const VELOCIDAD = 72;            // px de mundo por segundo
const PIES = { w: 10, h: 5 };    // caja de colisión en los pies
const PIES_NPC = { w: 12, h: 6 };
const RADIO_INTERACCION = 26;
const PULSACION_LARGA = 400;     // ms → mirar
const ARRASTRE_JOYSTICK = 14;    // px de pantalla para activar el joystick
const RADIO_JOYSTICK = 44;
const ZONA_MUERTA = 0.18;        // fracción del radio en la que el dedo aún no mueve al personaje
const DIRS: Dir[] = ['abajo', 'izquierda', 'derecha', 'arriba'];

interface Pulsacion {
  id: number; x: number; y: number; hotspot: Hotspot | null; consumida: boolean; joystick: boolean;
  timer?: Phaser.Time.TimerEvent;
}

export class LocationScene extends Phaser.Scene {
  private loc!: LocationData;
  private prota!: Phaser.GameObjects.Sprite;
  private fondo!: Phaser.GameObjects.Image;
  private cono!: Phaser.GameObjects.Graphics;
  private sombra!: Phaser.GameObjects.Ellipse;
  private texturaProta = 'prot_h';
  private dir: Dir = 'abajo';
  private nav!: NavGrid;
  private ruta: Point[] = [];
  private alLlegar: (() => void) | null = null;
  private enfocado: Hotspot | null = null;
  private ocupado = false;
  /** La pulsación que cerró un diálogo no debe convertirse en una orden de caminar. */
  private ignorarPulsacion = false;
  /** Momento en que terminó el último diálogo (la tecla que lo cerró no debe activar nada). */
  private finDialogo = 0;
  private teclas!: Record<string, Phaser.Input.Keyboard.Key>;
  private capaDepuracion!: Phaser.GameObjects.Graphics;
  private depurando = false;
  private pulsacion: Pulsacion | null = null;
  private npcs = new Map<string, { npc: Npc; sprite: Phaser.GameObjects.Sprite; visible: boolean }>();
  private hotspotsVisibles: Hotspot[] = [];
  private zonasPisadas = new Set<string>();
  private cambioPendiente: { escena?: string; spawn?: string } = {};
  private finalPendiente = false;
  private colisionesActivas: Rect[] = [];
  private limpiar: (() => void)[] = [];
  private sigilo: Sigilo | null = null;
  /** Punto de aparición al que se vuelve si te ven (sigilo). */
  private checkpoint = '';
  private volverAlControl = false;
  private moviendose = false;
  private arrestando = false;

  constructor() { super('Location'); }

  create(data: EntradaEscena) {
    this.loc = LOCALIZACIONES[data.escena];
    if (!this.loc) throw new Error(`Localización desconocida: ${data.escena}`);
    this.ocupado = false;
    this.ruta = []; this.alLlegar = null; this.enfocado = null; this.pulsacion = null;
    this.npcs.clear(); this.zonasPisadas.clear(); this.cambioPendiente = {}; this.limpiar = [];

    this.fondo = this.add.image(0, 0, this.loc.fondo).setOrigin(0).setDepth(-1000);
    if (this.loc.parpadeo) this.neones();
    this.cono = this.add.graphics().setDepth(8000);
    const verCono = () => this.dibujarCono();
    this.game.events.on(EV.mano, verCono);
    this.events.once('shutdown', () => this.game.events.off(EV.mano, verCono));
    this.dibujarCono();
    if (this.loc.conosRotativos && !this.loc.sigilo) this.vigilancia(this.loc.conosRotativos);
    if (narrativa.story.variablesState.GlobalVariableExistsWithName('escena_actual')) narrativa.set('escena_actual', this.loc.id);

    const spawn = this.loc.spawns.find((s) => s.name === data.spawn) ?? this.loc.spawns[0];
    const x = data.x ?? spawn.x, y = data.y ?? spawn.y;
    this.dir = data.dir ?? spawn.orientacion;
    this.texturaProta = narrativa.get('genero') === 'f' ? 'prot_m' : 'prot_h';
    this.sombra = this.add.ellipse(x, y, 14, 5, 0x000000, 0.28);
    this.prota = this.add.sprite(x, y, this.texturaProta, this.cuadroQuieto()).setOrigin(0.5, 1);
    if (this.loc.tinteProta !== undefined) this.prota.setTint(this.loc.tinteProta);
    this.finalPendiente = false;

    for (const npc of this.loc.npcs) {
      const sprite = this.add.sprite(npc.x, npc.y, `npc-${npc.sprite}`, npc.frame ?? 0).setOrigin(0.5, 1).setDepth(npc.y);
      if (npc.dir === 'izquierda') sprite.setFlipX(true);
      if (this.loc.tinteProta !== undefined) sprite.setTint(this.loc.tinteProta);   // la misma luz para todos
      this.npcs.set(npc.name, { npc, sprite, visible: true });
    }
    this.sigilo = null; this.volverAlControl = false; this.arrestando = false;
    mision.oculto = false;
    if (this.loc.sigilo) {
      this.checkpoint = this.loc.sigilo.checkpoint ?? spawn.name;
      this.sigilo = new Sigilo(this, this.loc, this.npcs, {
        prota: () => ({ x: this.prota.x, y: this.prota.y }),
        bloquea: (p) => this.colisionesActivas.some((c) => contains(c, p)),
        moviendose: () => this.moviendose,
        visto: () => this.visto(),
      });
      this.events.once('shutdown', () => { this.sigilo?.destroy(); this.sigilo = null; });
    }
    if (data.cargado && data.reloj !== undefined) mision.reloj = data.reloj;
    this.actualizarVisibilidad();

    const cam = this.cameras.main;
    cam.setZoom(RESOLUCION.zoom);
    if (this.loc.sigueCamara) {
      cam.setBounds(0, 0, this.loc.width, this.loc.height);
      cam.startFollow(this.prota, true, 0.12, 0.12, 0, 20);
    } else {
      cam.centerOn(RESOLUCION.mundoAncho / 2, RESOLUCION.mundoAlto / 2);
    }
    cam.fadeIn(400, 11, 12, 15);

    this.capaDepuracion = this.add.graphics().setDepth(10000);
    this.configurarEntrada();
    this.configurarNarrativa();
    this.events.once('shutdown', () => this.limpiar.forEach((f) => f()));

    if (!data.cargado && this.loc.alEntrar && narrativa.hasPath(this.loc.alEntrar)) {
      this.time.delayedCall(450, () => this.game.events.emit(EV.dialogoIniciar, this.loc.alEntrar));
    } else if (!data.cargado) {
      this.time.delayedCall(0, () => this.autoguardar());
    }
  }

  // ------------------------------------------------------------------ entrada
  private configurarEntrada() {
    const kb = this.input.keyboard!;
    this.teclas = kb.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,E,SPACE,Q,SHIFT') as Record<string, Phaser.Input.Keyboard.Key>;
    const principal = () => this.actuarEnfocado('principal');
    const mirar = () => this.actuarEnfocado('mirar');
    kb.on('keydown-E', principal);
    kb.on('keydown-SPACE', principal);
    kb.on('keydown-Q', mirar);
    this.input.mouse?.disableContextMenu();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.ocupado || this.ignorarPulsacion || this.registry.get('uiCapturo') === p.downTime) return;
      if (tactil.activo) return;   // un segundo dedo mientras el primero lleva el joystick
      const punto = { x: p.worldX, y: p.worldY };
      const h = this.hotspotEn(punto);
      if (p.rightButtonDown()) {
        if (h) this.irYActuar(h, 'mirar');
        return;
      }
      this.pulsacion = { id: p.id, x: p.x, y: p.y, hotspot: h, consumida: false, joystick: false };
      if (h) {
        this.pulsacion.timer = this.time.delayedCall(PULSACION_LARGA, () => {
          if (this.pulsacion && !this.pulsacion.consumida && !this.pulsacion.joystick) {
            this.pulsacion.consumida = true;
            this.irYActuar(h, 'mirar');
          }
        });
      }
    });

    this.input.on('pointermove', (p: Phaser.Input.Pointer) => {
      const pul = this.pulsacion;
      if (!pul || pul.id !== p.id || pul.consumida || this.ocupado || !p.isDown) return;
      const dx = p.x - pul.x, dy = p.y - pul.y;
      if (!pul.joystick && Math.hypot(dx, dy) > ARRASTRE_JOYSTICK && p.wasTouch) {
        pul.joystick = true;
        pul.timer?.remove();
        this.ruta = []; this.alLlegar = null;
        tactil.activo = true;
        tactil.origen = { x: pul.x, y: pul.y };
      }
      if (pul.joystick) {
        let d = Math.hypot(dx, dy) || 1;
        if (d > RADIO_JOYSTICK) {
          // el centro sigue al dedo: cambiar de dirección no obliga a volver hasta el origen
          pul.x = p.x - (dx / d) * RADIO_JOYSTICK;
          pul.y = p.y - (dy / d) * RADIO_JOYSTICK;
          tactil.origen = { x: pul.x, y: pul.y };
          d = RADIO_JOYSTICK;
        }
        const k = Math.max(0, (d / RADIO_JOYSTICK - ZONA_MUERTA) / (1 - ZONA_MUERTA));
        tactil.x = ((p.x - pul.x) / d) * k;
        tactil.y = ((p.y - pul.y) / d) * k;
        this.game.events.emit(EV.joystick);
      }
    });

    const soltar = (p: Phaser.Input.Pointer) => {
      if (this.ignorarPulsacion) { this.ignorarPulsacion = false; this.pulsacion = null; return; }
      const pul = this.pulsacion;
      if (pul && pul.id !== p.id) return;   // se levantó otro dedo
      this.pulsacion = null;
      if (pul?.joystick) {
        this.soltarJoystick();
        return;
      }
      if (!pul || pul.consumida || this.ocupado || p.rightButtonReleased()) return;
      pul.timer?.remove();
      if (mision.carpeta) this.caminarA({ x: p.worldX, y: p.worldY });
      else if (pul.hotspot) this.irYActuar(pul.hotspot, 'principal');
      else this.caminarA({ x: p.worldX, y: p.worldY });
    };
    this.input.on('pointerup', soltar);
    // el dedo sale de la pantalla, la app pasa a segundo plano o se cambia de escena: nunca seguir andando solo
    this.input.on('pointerupoutside', (p: Phaser.Input.Pointer) => { if (this.pulsacion?.id === p.id) { this.pulsacion = null; this.soltarJoystick(); } });
    this.game.events.on(Phaser.Core.Events.BLUR, this.soltarJoystick, this);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.game.events.off(Phaser.Core.Events.BLUR, this.soltarJoystick, this);
      this.soltarJoystick();
    });
  }

  /** Con el diario en la mano se ve hasta dónde llega la telepantalla. */
  private dibujarCono() {
    this.cono.clear();
    if (!this.loc.cono || mano.item !== 'diario') return;
    const puntos = this.loc.cono.map((p) => new Phaser.Math.Vector2(p.x, p.y));
    this.cono.fillStyle(0x7fc496, 0.13).fillPoints(puntos, true)
      .lineStyle(1, 0x7fc496, 0.6).strokePoints(puntos, true);
  }

  /** Una telepantalla de techo que gira: alterna sus conos cada 5 segundos y lo anota en ink. */
  private vigilancia(v: { conos: Point[][]; variable: string }) {
    const g = this.add.graphics().setDepth(8000);
    let i = 0;
    const girar = () => {
      const puntos = v.conos[i].map((p) => new Phaser.Math.Vector2(p.x, p.y));
      g.clear().fillStyle(0x7fc496, 0.14).fillPoints(puntos, true).lineStyle(1, 0x7fc496, 0.7).strokePoints(puntos, true);
      if (v.variable) narrativa.set(v.variable, i === 0);
      i = (i + 1) % v.conos.length;
    };
    girar();
    this.time.addEvent({ delay: 5000, loop: true, callback: girar });
  }

  /** Tubos de neón que fallan: la sala se oscurece a destellos irregulares. */
  private neones() {
    const velo = this.add.rectangle(0, 0, this.loc.width, this.loc.height, 0x000000, 0).setOrigin(0).setDepth(9000);
    const fallo = () => {
      if (!this.scene.isActive()) return;
      const veces = Phaser.Math.Between(1, 3);
      for (let i = 0; i < veces; i++) {
        this.time.delayedCall(i * 110, () => velo.setAlpha(0.35));
        this.time.delayedCall(i * 110 + 55, () => velo.setAlpha(0));
      }
      this.time.delayedCall(Phaser.Math.Between(900, 3200), fallo);
    };
    this.time.delayedCall(600, fallo);
  }

  private soltarJoystick() {
    if (!tactil.activo) return;
    tactil.activo = false; tactil.x = 0; tactil.y = 0;
    this.pulsacion = null;
    this.game.events.emit(EV.joystick);
  }

  private configurarNarrativa() {
    const ev = this.game.events;
    const inicio = () => { this.ocupado = true; this.ruta = []; this.parar(); };
    const fin = () => {
      this.ocupado = false;
      // Si el diálogo se cerró con un clic o toque, ese mismo gesto se ignora hasta soltarlo.
      this.ignorarPulsacion = this.input.activePointer.isDown;
      this.finDialogo = this.time.now;
      this.actualizarVisibilidad();
      this.enfocado = null;
      if (this.volverAlControl && !this.cambioPendiente.escena) {
        const s = this.loc.spawns.find((sp) => sp.name === this.checkpoint);
        if (s) { this.colocar(s.x, s.y); this.dir = s.orientacion; this.parar(); }
        this.sigilo?.reiniciar();
        this.cameras.main.flash(250, 11, 12, 15);
      }
      this.volverAlControl = false;
      // Sospecha 100: el arresto (Final C, o C0 en el Acto I)
      if (!this.arrestando && !this.finalPendiente && Number(narrativa.get('sospecha')) >= 100 && narrativa.hasPath('arresto')) {
        this.arrestando = true;
        this.cambioPendiente = {};
        this.time.delayedCall(300, () => this.game.events.emit(EV.dialogoIniciar, 'arresto'));
        return;
      }
      this.autoguardar();
    };
    const depurar = (activo: boolean) => { this.depurando = activo; };
    // paneles (registro) que detienen el mundo sin ser un diálogo
    const pausa = (activa: boolean) => { if (activa) inicio(); else { this.ocupado = false; this.finDialogo = this.time.now; } };
    const accion = (modo: 'principal' | 'mirar') => this.actuarEnfocado(modo);
    const carpeta = () => {
      if (!mision.social || this.ocupado) return;
      mision.carpeta = !mision.carpeta;
      audio.play('papel');
      if (mision.carpeta) { this.game.events.emit(EV.foco, null); this.enfocado = null; }
    };
    ev.on(EV.carpeta, carpeta);
    ev.on(EV.dialogoIniciar, inicio);
    ev.on(EV.dialogoFin, fin);
    ev.on(EV.depurar, depurar);
    ev.on(EV.accion, accion);
    ev.on(EV.pausa, pausa);
    const quitar = narrativa.on('command', (t: Tag) => this.comando(t));
    this.limpiar.push(() => {
      ev.off(EV.dialogoIniciar, inicio); ev.off(EV.dialogoFin, fin); ev.off(EV.depurar, depurar); ev.off(EV.accion, accion); ev.off(EV.pausa, pausa);
      ev.off(EV.carpeta, carpeta);
      quitar();
    });
  }

  private comando(t: Tag) {
    if (t.key === 'escena') {
      if (t.value === this.loc.id) return;
      if (LOCALIZACIONES[t.value]) this.cambioPendiente.escena = t.value;
      else console.info(`[escena] "${t.value}" aún no existe`);
    } else if (t.key === 'pos') {
      if (this.cambioPendiente.escena) { this.cambioPendiente.spawn = t.value; return; }
      const s = this.loc.spawns.find((sp) => sp.name === t.value);
      if (s) { this.colocar(s.x, s.y); this.dir = s.orientacion; this.parar(); }
    } else if (t.key === 'refrescar') {
      this.actualizarVisibilidad();
    } else if (t.key === 'final') {
      this.finalPendiente = true;
      if (t.value && t.value !== 'demo') SaveSystem.registrarFinal(t.value);
    } else if (t.key === 'prota') {
      // prota:izquierda → el protagonista se gira (sin moverse)
      this.dir = t.value as Dir;
      this.parar();
    } else if (t.key === 'seguir') {
      // seguir: al que han visto no se le devuelve al punto de control (alguien le ha cubierto)
      this.volverAlControl = false;
    } else if (t.key === 'reloj') {
      // reloj:inicio=23:00:00,limite=240,agotar=knot · reloj:mas=90 · reloj:menos=10 · reloj:parar
      const p = t.params;
      if (t.value === 'parar') mision.reloj = null;
      else if (p.inicio) mision.reloj = { inicio: segundos(p.inicio), transcurrido: 0, limite: Number(p.limite) || 240, agotar: p.agotar ?? '', agotado: false };
      else if (mision.reloj && p.mas) { mision.reloj.limite = mision.reloj.transcurrido + Number(p.mas); mision.reloj.agotado = false; }
      else if (mision.reloj && p.menos) mision.reloj.transcurrido += Number(p.menos);
    } else if (t.key === 'npc') {
      // npc:nombre=dir  → orienta a un personaje (p. ej. hacia el jugador)
      for (const [nombre, dir] of Object.entries(t.params)) {
        const n = this.npcs.get(nombre);
        if (n) n.sprite.setFlipX(dir === 'izquierda');
      }
    }
  }

  // ------------------------------------------------------------------ bucle
  update(_t: number, dtMs: number) {
    const dt = dtMs / 1000;
    this.moviendose = false;
    if (!this.ocupado) {
      const v = this.direccionEntrada();
      if ((v.x || v.y) && mision.oculto) this.salirEscondite();
      if (v.x || v.y) {
        this.ruta = []; this.alLlegar = null;
        const corre = !mision.carpeta && (this.teclas.SHIFT.isDown || (tactil.activo && Math.hypot(v.x, v.y) > 0.95));
        const vel = VELOCIDAD * (corre ? 1.6 : mision.carpeta ? VELOCIDAD_LEYENDO : 1);
        this.prota.anims.timeScale = corre ? 1.6 : 1;   // al correr, las piernas van al mismo ritmo
        this.moviendose = this.mover(v.x * vel * dt, v.y * vel * dt);
      } else if (this.ruta.length) {
        this.prota.anims.timeScale = mision.carpeta ? VELOCIDAD_LEYENDO : 1;
        this.seguirRuta(dt * (mision.carpeta ? VELOCIDAD_LEYENDO : 1));
        this.moviendose = true;
      } else if (!mision.oculto) {
        this.parar();
      }
      if (!mision.carpeta) this.actualizarFoco();
      this.comprobarZonas();
      this.avanzarReloj(dt);
    }
    this.sigilo?.update(dtMs, !this.ocupado);
    this.alejarPersonajes(dt);
    this.prota.setDepth(this.prota.y);
    this.sombra.setPosition(this.prota.x, this.prota.y - 1).setDepth(this.prota.y - 1);
    this.dibujarDepuracion();
  }

  /** Le han visto: la historia decide (¡Alto!, Sospecha) y después se vuelve al último punto de control. */
  private visto() {
    if (this.ocupado) return;
    this.salirEscondite();
    this.volverAlControl = true;
    audio.play('alto');
    const ruta = this.loc.sigilo?.alSerVisto;
    if (ruta && narrativa.hasPath(ruta)) this.game.events.emit(EV.dialogoIniciar, ruta);
  }

  private esconderse(h: Hotspot) {
    if (mision.oculto) return this.salirEscondite();
    mision.oculto = true;
    this.colocar(h.aprox.x, h.aprox.y);
    if (h.orientacion) this.dir = h.orientacion;
    this.parar();
    this.prota.setAlpha(0.35);
    this.sombra.setAlpha(0.1);
    audio.play('papel');
  }

  private salirEscondite() {
    if (!mision.oculto) return;
    mision.oculto = false;
    this.prota.setAlpha(1);
    this.sombra.setAlpha(1);
  }

  /** La ventana de tiempo de una misión: corre solo mientras se explora. */
  private avanzarReloj(dt: number) {
    const r = mision.reloj;
    if (!r || r.agotado) return;
    const antes = Math.floor(r.transcurrido);
    r.transcurrido += dt;
    if (Math.floor(r.transcurrido) !== antes && r.limite - r.transcurrido < 15) audio.play('tic');
    if (r.transcurrido >= r.limite) {
      r.agotado = true;
      if (r.agotar && narrativa.hasPath(r.agotar)) this.game.events.emit(EV.dialogoIniciar, r.agotar);
    }
  }

  /** Personajes con "huye": retroceden hacia la derecha mientras el jugador se acerca. */
  private alejarPersonajes(dt: number) {
    for (const n of this.npcs.values()) {
      const huye = n.npc.huye;
      if (!huye || !n.visible) continue;
      const dx = n.sprite.x - this.prota.x;
      if (dx > 0 && dx < huye && n.sprite.x < this.loc.width - 24) {
        const paso = VELOCIDAD * 1.05 * dt;
        n.sprite.x += paso;
        n.npc.x = n.sprite.x;
        n.npc.hotspot.x += paso;
        n.npc.hotspot.aprox.x += paso;
      }
    }
  }

  private direccionEntrada(): Point {
    if (tactil.activo) return { x: tactil.x, y: tactil.y };
    const k = this.teclas;
    let x = 0, y = 0;
    if (k.A.isDown || k.LEFT.isDown) x -= 1;
    if (k.D.isDown || k.RIGHT.isDown) x += 1;
    if (k.W.isDown || k.UP.isDown) y -= 1;
    if (k.S.isDown || k.DOWN.isDown) y += 1;
    if (x && y) { x *= Math.SQRT1_2; y *= Math.SQRT1_2; }
    return { x, y };
  }

  private seguirRuta(dt: number) {
    const objetivo = this.ruta[0];
    const dx = objetivo.x - this.prota.x, dy = objetivo.y - this.prota.y;
    const dist = Math.hypot(dx, dy);
    const paso = VELOCIDAD * dt;
    if (dist <= paso) {
      this.colocar(objetivo.x, objetivo.y);
      this.ruta.shift();
      if (!this.ruta.length) {
        this.parar();
        const f = this.alLlegar; this.alLlegar = null; f?.();
      }
      return;
    }
    const movido = this.mover((dx / dist) * paso, (dy / dist) * paso);
    if (!movido) { this.ruta = []; this.alLlegar = null; }
  }

  /** Mueve con colisión por ejes. Devuelve false si no pudo avanzar nada. */
  private mover(dx: number, dy: number): boolean {
    let movido = false;
    if (dx && !this.bloqueado({ x: this.prota.x + dx, y: this.prota.y })) { this.prota.x += dx; movido = true; }
    if (dy && !this.bloqueado({ x: this.prota.x, y: this.prota.y + dy })) { this.prota.y += dy; movido = true; }
    if (Math.abs(dx) > Math.abs(dy)) this.dir = dx < 0 ? 'izquierda' : 'derecha';
    else if (dy) this.dir = dy < 0 ? 'arriba' : 'abajo';
    if (movido) this.prota.anims.play(`${this.texturaProta}-${this.dir}-andar`, true);
    return movido;
  }

  private parar() {
    this.prota.anims.stop();
    this.prota.setFrame(this.cuadroQuieto());
  }

  private cuadroQuieto() { return DIRS.indexOf(this.dir) * 5; }

  private colocar(x: number, y: number) { this.prota.setPosition(x, y); }

  private pies(p: Point): Rect {
    return { x: p.x - PIES.w / 2, y: p.y - PIES.h, w: PIES.w, h: PIES.h };
  }

  private bloqueado(p: Point): boolean {
    const r = this.pies(p);
    if (r.x < 0 || r.y < 0 || r.x + r.w > this.loc.width || r.y + r.h > this.loc.height) return true;
    if (this.colisionesActivas.some((c) => overlaps(r, c))) return true;
    for (const { npc, visible } of this.npcs.values()) {
      if (visible && npc.solido && overlaps(r, { x: npc.x - PIES_NPC.w / 2, y: npc.y - PIES_NPC.h, ...PIES_NPC })) return true;
    }
    return false;
  }

  private reconstruirNav() {
    this.nav = new NavGrid(this.loc.width, this.loc.height, 4, (px, py) => this.bloqueado({ x: px, y: py }));
  }

  // ------------------------------------------------------------------ visibilidad según la historia
  private actualizarVisibilidad() {
    const leer = (v: string) => narrativa.get(v);
    const alt = this.loc.fondosAlt.find((f) => cumple(f.condicion, leer));
    this.fondo.setTexture(alt ? alt.clave : this.loc.fondo);
    this.colisionesActivas = this.loc.colisiones.filter((c) => cumple(c.condicion, leer));
    const conAccion = (h: Hotspot) => !!(h.mirar || h.usar || h.hablar || h.escondite);
    this.hotspotsVisibles = this.loc.hotspots.filter((h) => conAccion(h) && cumple(h.condicion, leer));
    for (const n of this.npcs.values()) {
      n.visible = cumple(n.npc.hotspot.condicion, leer);
      n.sprite.setVisible(n.visible);
      if (n.visible && conAccion(n.npc.hotspot)) this.hotspotsVisibles.push(n.npc.hotspot);
    }
    this.reconstruirNav();
  }

  // ------------------------------------------------------------------ interacción
  private hotspotEn(p: Point): Hotspot | null {
    // los NPC (añadidos al final) tienen prioridad sobre los objetos de fondo
    return [...this.hotspotsVisibles].reverse().find((h) => !h.auto && contains(h, p)) ?? null;
  }

  private actualizarFoco() {
    const pos = { x: this.prota.x, y: this.prota.y };
    let mejor: Hotspot | null = null, dmin = RADIO_INTERACCION;
    for (const h of this.hotspotsVisibles) {
      if (h.auto) continue;
      const d = Math.hypot(h.aprox.x - pos.x, h.aprox.y - pos.y);
      if (d < dmin) { dmin = d; mejor = h; }
    }
    if (mejor !== this.enfocado) {
      this.enfocado = mejor;
      const cam = this.cameras.main;
      const z = RESOLUCION.zoom;
      this.game.events.emit(EV.foco, mejor && {
        nombre: mejor.nombre,
        x: (mejor.x + mejor.w / 2 - cam.worldView.x) * z,
        y: (mejor.y - cam.worldView.y) * z,
        mirar: !!mejor.mirar,
        usar: !!(mejor.usar || mejor.hablar),
        hablar: !!mejor.hablar,
      });
    }
  }

  /** Zonas automáticas: se disparan una vez al entrar en ellas. */
  private comprobarZonas() {
    const p = { x: this.prota.x, y: this.prota.y - 2 };
    const leer = (v: string) => narrativa.get(v);
    for (const h of this.loc.hotspots) {
      if (!(h.ruido || h.checkpoint) || !cumple(h.condicion, leer)) continue;
      const clave = `@${h.name}`;
      const dentro = contains(h, p);
      if (dentro && !this.zonasPisadas.has(clave)) {
        this.zonasPisadas.add(clave);
        if (h.checkpoint) this.checkpoint = h.checkpoint;
        if (h.ruido) this.sigilo?.ruido({ x: h.x + h.w / 2, y: h.y + h.h / 2 });
      }
      if (!dentro) this.zonasPisadas.delete(clave);
    }
    for (const h of this.hotspotsVisibles) {
      if (!h.auto) continue;
      const dentro = contains(h, p);
      if (dentro && !this.zonasPisadas.has(h.name)) {
        this.zonasPisadas.add(h.name);
        this.actuar(h, 'principal');
        return;
      }
      if (!dentro) this.zonasPisadas.delete(h.name);
    }
  }

  private actuarEnfocado(modo: 'principal' | 'mirar') {
    if (mision.oculto && modo === 'principal') { this.salirEscondite(); return; }
    if (this.ocupado || mision.carpeta || !this.enfocado || this.time.now - this.finDialogo < 250) return;
    this.actuar(this.enfocado, modo);
  }

  private irYActuar(h: Hotspot, modo: 'principal' | 'mirar') {
    this.caminarA(h.aprox, () => this.actuar(h, modo));
  }

  private actuar(h: Hotspot, modo: 'principal' | 'mirar') {
    if (h.escondite && modo === 'principal' && !mano.item) { this.esconderse(h); return; }
    let ruta = modo === 'mirar' ? h.mirar : (h.hablar ?? h.usar ?? h.mirar);
    // con un objeto en la mano, la acción principal es usarlo aquí
    if (mano.item && modo === 'principal') {
      ruta = h.con?.[mano.item] ?? 'objetos.no_sirve';
      mano.item = null;
      this.game.events.emit(EV.mano);
    }
    if (!ruta) return;
    if (h.orientacion && !h.auto) { this.dir = h.orientacion; this.parar(); }
    if (!narrativa.hasPath(ruta)) { console.warn(`[ink] no existe "${ruta}"`); return; }
    // el NPC se gira hacia el jugador al hablarle
    const npc = [...this.npcs.values()].find((n) => n.npc.hotspot === h);
    if (npc && modo !== 'mirar') npc.sprite.setFlipX(this.prota.x < npc.npc.x && npc.npc.dir !== 'abajo');
    this.game.events.emit(EV.foco, null);
    this.enfocado = null;
    this.game.events.emit(EV.dialogoIniciar, ruta);
  }

  private caminarA(destino: Point, alLlegar?: () => void) {
    const ruta = this.nav.findPath({ x: this.prota.x, y: this.prota.y }, destino);
    if (!ruta) return;
    this.ruta = ruta;
    this.alLlegar = alLlegar ?? null;
    if (!ruta.length) { const f = this.alLlegar; this.alLlegar = null; f?.(); }
  }

  // ------------------------------------------------------------------ guardado y transiciones
  private autoguardar() {
    if (this.finalPendiente) {
      this.ocupado = true;
      SaveSystem.borrar('auto');
      this.cameras.main.fadeOut(900, 11, 12, 15);
      this.cameras.main.once('camerafadeoutcomplete', () => { this.scene.stop('UI'); this.scene.start('Menu'); });
      return;
    }
    const { escena, spawn } = this.cambioPendiente;
    if (escena) {
      this.cambioPendiente = {};
      this.ocupado = true;
      this.cameras.main.fadeOut(350, 11, 12, 15);
      this.cameras.main.once('camerafadeoutcomplete', () => this.scene.restart({ escena, spawn }));
      return;
    }
    SaveSystem.guardar('auto', {
      ink: narrativa.saveState(),
      registro: registro.serializar(),
      mundo: { escena: this.loc.id, x: Math.round(this.prota.x), y: Math.round(this.prota.y), dir: this.dir, reloj: mision.reloj ?? undefined },
      meta: { jornada: Number(narrativa.get('jornada')) || 1 },
    });
  }

  // ------------------------------------------------------------------ depuración
  private dibujarDepuracion() {
    const g = this.capaDepuracion;
    g.clear();
    if (!this.depurando) return;
    g.lineStyle(1, 0xff4444, 0.9);
    this.colisionesActivas.forEach((c) => g.strokeRect(c.x, c.y, c.w, c.h));
    for (const h of this.hotspotsVisibles) {
      g.lineStyle(1, h.auto ? 0x48b0ff : 0xffd34d, 0.9).strokeRect(h.x, h.y, h.w, h.h);
      g.fillStyle(0xffd34d, 1).fillRect(h.aprox.x - 1, h.aprox.y - 1, 3, 3);
    }
    g.lineStyle(1, 0x7fc496, 1);
    const pts = [{ x: this.prota.x, y: this.prota.y }, ...this.ruta];
    for (let i = 1; i < pts.length; i++) g.lineBetween(pts[i - 1].x, pts[i - 1].y, pts[i].x, pts[i].y);
    const p = this.pies({ x: this.prota.x, y: this.prota.y });
    g.lineStyle(1, 0x48b0ff, 1).strokeRect(p.x, p.y, p.w, p.h);
  }
}
