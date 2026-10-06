/**
 * Escena de exploración cenital (diseño técnico §5).
 * Movimiento directo (teclado) o tocando/clicando (A*), colisiones, puntos interactivos y depuración.
 */
import Phaser from 'phaser';
import { narrativa, LOCALIZACIONES, RESOLUCION, EV } from '../core/juego';
import { contains, overlaps, type Dir, type Hotspot, type LocationData, type Point, type Rect } from '../core/Location';
import { NavGrid } from '../systems/Pathfinding';
import { SaveSystem } from '../core/SaveSystem';
import type { Tag } from '../core/tags';

interface EntradaEscena { escena: string; spawn?: string; x?: number; y?: number; dir?: Dir }

const VELOCIDAD = 72;          // px de mundo por segundo
const PIES = { w: 10, h: 5 };  // caja de colisión en los pies
const RADIO_INTERACCION = 26;
const PULSACION_LARGA = 400;   // ms → mirar

export class LocationScene extends Phaser.Scene {
  private loc!: LocationData;
  private prota!: Phaser.GameObjects.Sprite;
  private sombra!: Phaser.GameObjects.Ellipse;
  private dir: Dir = 'abajo';
  private nav!: NavGrid;
  private ruta: Point[] = [];
  private alLlegar: (() => void) | null = null;
  private enfocado: Hotspot | null = null;
  private ocupado = false;
  /** La pulsación que cerró un diálogo no debe convertirse en una orden de caminar. */
  private ignorarPulsacion = false;
  private teclas!: Record<string, Phaser.Input.Keyboard.Key>;
  private capaDepuracion!: Phaser.GameObjects.Graphics;
  private depurando = false;
  private pulsacion: { t: number; hotspot: Hotspot | null; consumida: boolean; timer?: Phaser.Time.TimerEvent } | null = null;
  private limpiar: (() => void)[] = [];

  constructor() { super('Location'); }

  create(data: EntradaEscena) {
    this.loc = LOCALIZACIONES[data.escena];
    const cam = this.cameras.main;
    cam.setZoom(RESOLUCION.zoom);
    cam.centerOn(RESOLUCION.mundoAncho / 2, RESOLUCION.mundoAlto / 2);
    cam.fadeIn(400, 11, 12, 15);

    this.add.image(0, 0, this.loc.fondo).setOrigin(0).setDepth(-1000);

    const spawn = this.loc.spawns.find((s) => s.name === data.spawn) ?? this.loc.spawns[0];
    const x = data.x ?? spawn.x, y = data.y ?? spawn.y;
    this.dir = data.dir ?? spawn.orientacion;
    this.sombra = this.add.ellipse(x, y, 14, 5, 0x000000, 0.28);
    this.prota = this.add.sprite(x, y, 'prot', this.cuadroQuieto()).setOrigin(0.5, 1);

    this.nav = new NavGrid(this.loc.width, this.loc.height, 4, (px, py) => this.bloqueado({ x: px, y: py }));
    this.capaDepuracion = this.add.graphics().setDepth(10000);

    this.configurarEntrada();
    this.configurarNarrativa();
    this.events.once('shutdown', () => this.limpiar.forEach((f) => f()));
  }

  // ------------------------------------------------------------------ entrada
  private configurarEntrada() {
    const kb = this.input.keyboard!;
    this.teclas = kb.addKeys('W,A,S,D,UP,DOWN,LEFT,RIGHT,E,SPACE,Q,SHIFT') as Record<string, Phaser.Input.Keyboard.Key>;
    kb.on('keydown-E', () => this.actuarEnfocado('principal'));
    kb.on('keydown-SPACE', () => this.actuarEnfocado('principal'));
    kb.on('keydown-Q', () => this.actuarEnfocado('mirar'));
    this.input.mouse?.disableContextMenu();

    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      if (this.ocupado || this.ignorarPulsacion) return;
      const punto = { x: p.worldX, y: p.worldY };
      const h = this.hotspotEn(punto);
      if (p.rightButtonDown()) {
        if (h) this.irYActuar(h, 'mirar');
        return;
      }
      this.pulsacion = { t: this.time.now, hotspot: h, consumida: false };
      if (h) {
        this.pulsacion.timer = this.time.delayedCall(PULSACION_LARGA, () => {
          if (this.pulsacion && !this.pulsacion.consumida) {
            this.pulsacion.consumida = true;
            this.irYActuar(h, 'mirar');
          }
        });
      }
    });
    this.input.on('pointerup', (p: Phaser.Input.Pointer) => {
      if (this.ignorarPulsacion) { this.ignorarPulsacion = false; this.pulsacion = null; return; }
      const pul = this.pulsacion;
      this.pulsacion = null;
      if (!pul || pul.consumida || this.ocupado || p.rightButtonReleased()) return;
      pul.timer?.remove();
      if (pul.hotspot) this.irYActuar(pul.hotspot, 'principal');
      else this.caminarA({ x: p.worldX, y: p.worldY });
    });
  }

  private configurarNarrativa() {
    const ev = this.game.events;
    const inicio = () => { this.ocupado = true; this.ruta = []; this.parar(); };
    const fin = () => {
      this.ocupado = false;
      // Si el diálogo se cerró con un clic o toque, ese mismo gesto se ignora hasta soltarlo.
      this.ignorarPulsacion = this.input.activePointer.isDown;
      this.autoguardar();
    };
    const depurar = (activo: boolean) => { this.depurando = activo; };
    ev.on(EV.dialogoIniciar, inicio);
    ev.on(EV.dialogoFin, fin);
    ev.on(EV.depurar, depurar);
    const quitar = narrativa.on('command', (t: Tag) => this.comando(t));
    this.limpiar.push(() => {
      ev.off(EV.dialogoIniciar, inicio); ev.off(EV.dialogoFin, fin); ev.off(EV.depurar, depurar); quitar();
    });
  }

  private comando(t: Tag) {
    if (t.key === 'escena' && t.value !== this.loc.id) {
      if (LOCALIZACIONES[t.value]) this.registry.set('cambioEscena', t.value);
      else console.info(`[escena] "${t.value}" aún no existe`);
    } else if (t.key === 'pos') {
      const s = this.loc.spawns.find((sp) => sp.name === t.value);
      if (s) { this.colocar(s.x, s.y); this.dir = s.orientacion; this.parar(); }
    }
  }

  // ------------------------------------------------------------------ bucle
  update(_t: number, dtMs: number) {
    const dt = dtMs / 1000;
    if (!this.ocupado) {
      const v = this.direccionTeclado();
      if (v.x || v.y) {
        this.ruta = []; this.alLlegar = null;
        const vel = VELOCIDAD * (this.teclas.SHIFT.isDown ? 1.6 : 1);
        this.mover(v.x * vel * dt, v.y * vel * dt);
      } else if (this.ruta.length) {
        this.seguirRuta(dt);
      } else {
        this.parar();
      }
      this.actualizarFoco();
    }
    this.prota.setDepth(this.prota.y);
    this.sombra.setPosition(this.prota.x, this.prota.y - 1).setDepth(this.prota.y - 1);
    this.dibujarDepuracion();
  }

  private direccionTeclado(): Point {
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
    if (movido) this.prota.anims.play(`prot-${this.dir}-andar`, true);
    return movido;
  }

  private parar() {
    this.prota.anims.stop();
    this.prota.setFrame(this.cuadroQuieto());
  }

  private cuadroQuieto() {
    return ['abajo', 'izquierda', 'derecha', 'arriba'].indexOf(this.dir) * 5;
  }

  private colocar(x: number, y: number) { this.prota.setPosition(x, y); }

  private pies(p: Point): Rect {
    return { x: p.x - PIES.w / 2, y: p.y - PIES.h, w: PIES.w, h: PIES.h };
  }

  private bloqueado(p: Point): boolean {
    const r = this.pies(p);
    if (r.x < 0 || r.y < 0 || r.x + r.w > this.loc.width || r.y + r.h > this.loc.height) return true;
    return this.loc.colisiones.some((c) => overlaps(r, c));
  }

  // ------------------------------------------------------------------ interacción
  private hotspotEn(p: Point): Hotspot | null {
    return this.loc.hotspots.find((h) => contains(h, p)) ?? null;
  }

  private actualizarFoco() {
    const pos = { x: this.prota.x, y: this.prota.y };
    let mejor: Hotspot | null = null, dmin = RADIO_INTERACCION;
    for (const h of this.loc.hotspots) {
      const d = Math.hypot(h.aprox.x - pos.x, h.aprox.y - pos.y);
      if (d < dmin) { dmin = d; mejor = h; }
    }
    if (mejor !== this.enfocado) {
      this.enfocado = mejor;
      const z = RESOLUCION.zoom;
      this.game.events.emit(EV.foco, mejor && {
        nombre: mejor.nombre,
        x: (mejor.x + mejor.w / 2) * z,
        y: mejor.y * z,
        mirar: !!mejor.mirar,
        usar: !!(mejor.usar || mejor.hablar),
      });
    }
  }

  private actuarEnfocado(modo: 'principal' | 'mirar') {
    if (this.ocupado || !this.enfocado) return;
    this.actuar(this.enfocado, modo);
  }

  private irYActuar(h: Hotspot, modo: 'principal' | 'mirar') {
    this.caminarA(h.aprox, () => this.actuar(h, modo));
  }

  private actuar(h: Hotspot, modo: 'principal' | 'mirar') {
    const ruta = modo === 'mirar' ? h.mirar : (h.usar ?? h.hablar ?? h.mirar);
    if (!ruta) return;
    if (h.orientacion) { this.dir = h.orientacion; this.parar(); }
    if (!narrativa.hasPath(ruta)) { console.warn(`[ink] no existe "${ruta}"`); return; }
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

  // ------------------------------------------------------------------ guardado
  private autoguardar() {
    const cambio = this.registry.get('cambioEscena') as string | undefined;
    if (cambio) {
      this.registry.remove('cambioEscena');
      this.scene.restart({ escena: cambio });
      return;
    }
    SaveSystem.guardar('auto', {
      ink: narrativa.saveState(),
      mundo: { escena: this.loc.id, x: Math.round(this.prota.x), y: Math.round(this.prota.y), dir: this.dir },
      meta: { jornada: Number(narrativa.get('jornada')) || 1 },
    });
  }

  // ------------------------------------------------------------------ depuración
  private dibujarDepuracion() {
    const g = this.capaDepuracion;
    g.clear();
    if (!this.depurando) return;
    g.lineStyle(1, 0xff4444, 0.9);
    this.loc.colisiones.forEach((c) => g.strokeRect(c.x, c.y, c.w, c.h));
    g.lineStyle(1, 0xffd34d, 0.9);
    this.loc.hotspots.forEach((h) => {
      g.strokeRect(h.x, h.y, h.w, h.h);
      g.fillStyle(0xffd34d, 1).fillRect(h.aprox.x - 1, h.aprox.y - 1, 3, 3);
    });
    g.lineStyle(1, 0x7fc496, 1);
    const pts = [{ x: this.prota.x, y: this.prota.y }, ...this.ruta];
    for (let i = 1; i < pts.length; i++) g.lineBetween(pts[i - 1].x, pts[i - 1].y, pts[i].x, pts[i].y);
    const p = this.pies({ x: this.prota.x, y: this.prota.y });
    g.lineStyle(1, 0x48b0ff, 1).strokeRect(p.x, p.y, p.w, p.h);
  }
}
