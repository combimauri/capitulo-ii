/**
 * Capa de interfaz siempre activa (diseño técnico §7): diálogo, pensamientos, telepantalla,
 * carteles, elecciones, acciones bloqueantes (minijuegos, pausas, efectos), foco de objetos,
 * controles táctiles, inventario, ojo de la Sospecha y depuración.
 */
import Phaser from 'phaser';
import { narrativa, EV, ITEMS, tactil } from '../core/juego';
import type { ChoiceOption, Line } from '../core/NarrativeBridge';
import type { Tag } from '../core/tags';
import type { ResultadoMinijuego } from './minijuegos/Minijuego';
import { audio } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';

const VELOCIDAD_TEXTO = 55;          // caracteres por segundo
const CAJA = { x: 40, y: 386, w: 880, h: 132 };

/** Minijuegos por etiqueta: cf → Facecrime; minijuego:<tipo> → escena. */
const MINIJUEGOS: Record<string, string> = { cf: 'Facecrime', cascotes: 'Cascotes', ficha: 'Ficha', parte: 'Parte' };

interface FocoInfo { nombre: string; x: number; y: number; mirar: boolean; usar: boolean; hablar: boolean }

export class UIScene extends Phaser.Scene {
  private activo = false;
  private enAccion = false;
  private bloqueoHasta = 0;
  private escribiendo: Phaser.Time.TimerEvent | null = null;
  private textoCompleto = '';
  private destino: Phaser.GameObjects.Text | null = null;
  private esTactil = false;

  private caja!: Phaser.GameObjects.Container;
  private cajaFondo!: Phaser.GameObjects.Rectangle;
  private cajaFranja!: Phaser.GameObjects.Rectangle;
  private nombre!: Phaser.GameObjects.Text;
  private nombreFondo!: Phaser.GameObjects.Rectangle;
  private texto!: Phaser.GameObjects.Text;
  private indicador!: Phaser.GameObjects.Text;
  private pensamiento!: Phaser.GameObjects.Container;
  private pensamientoTexto!: Phaser.GameObjects.Text;
  private cartel!: Phaser.GameObjects.Container;
  private cartelTexto!: Phaser.GameObjects.Text;
  private velo!: Phaser.GameObjects.Rectangle;
  private opciones!: Phaser.GameObjects.Container;
  private opcionesLista: { fondo: Phaser.GameObjects.Rectangle; choice: ChoiceOption }[] = [];
  private opcionSel = 0;
  private foco!: Phaser.GameObjects.Container;
  private focoTexto!: Phaser.GameObjects.Text;
  private botones!: Phaser.GameObjects.Container;
  private joystick!: Phaser.GameObjects.Graphics;
  private inventario!: Phaser.GameObjects.Container;
  private ojo!: Phaser.GameObjects.Graphics;
  private depuracion!: Phaser.GameObjects.Text;
  private depurando = false;
  private inventarioAbiertoEn = 0;

  constructor() { super('UI'); }

  create() {
    this.activo = false; this.enAccion = false;
    this.esTactil = this.sys.game.device.input.touch;
    this.velo = this.add.rectangle(0, 0, 960, 540, 0x000000, 1).setOrigin(0).setAlpha(0).setDepth(40);
    this.crearCaja();
    this.crearPensamiento();
    this.crearCartel();
    this.opciones = this.add.container(0, 0).setVisible(false).setDepth(30);
    this.crearFoco();
    this.crearBotonesTactiles();
    this.joystick = this.add.graphics().setDepth(25);
    this.inventario = this.add.container(0, 0).setVisible(false).setDepth(60);
    this.ojo = this.add.graphics().setDepth(20);
    this.dibujarOjo(Number(narrativa.get('sospecha')) || 0);
    narrativa.observe('sospecha', (v) => this.dibujarOjo(Number(v)));
    this.depuracion = this.add.text(8, 8, '', {
      fontFamily: FUENTE.maquina, fontSize: '18px', color: '#ffd34d', backgroundColor: '#000000aa', padding: { x: 6, y: 4 },
    }).setVisible(false).setDepth(100);

    const ev = this.game.events;
    const iniciar = (ruta?: string) => this.iniciar(ruta);
    const foco = (info: FocoInfo | null) => this.mostrarFoco(info);
    const joy = () => this.dibujarJoystick();
    ev.on(EV.dialogoIniciar, iniciar);
    ev.on(EV.foco, foco);
    ev.on(EV.joystick, joy);
    const quitar = narrativa.on('command', () => undefined);
    this.events.once('shutdown', () => { ev.off(EV.dialogoIniciar, iniciar); ev.off(EV.foco, foco); ev.off(EV.joystick, joy); quitar(); });

    const kb = this.input.keyboard!;
    ['SPACE', 'ENTER', 'E'].forEach((k) => kb.on(`keydown-${k}`, () => this.confirmar()));
    kb.on('keydown-UP', () => this.moverSeleccion(-1));
    kb.on('keydown-DOWN', () => this.moverSeleccion(1));
    kb.on('keydown-W', () => this.moverSeleccion(-1));
    kb.on('keydown-S', () => this.moverSeleccion(1));
    kb.on('keydown-I', () => this.alternarInventario());
    kb.on('keydown-ESC', () => { if (this.inventario.visible) this.alternarInventario(); });
    kb.on('keydown', (e: KeyboardEvent) => {
      audio.desbloquear();
      const n = Number(e.key);
      if (n >= 1 && n <= this.opcionesLista.length) this.elegir(n - 1);
    });
    kb.on('keydown-F1', () => this.alternarDepuracion());
    this.input.on('pointerdown', () => {
      audio.desbloquear();
      if (this.activo && !this.enAccion && !this.opciones.visible) this.confirmar();
    });

    if (this.registry.get('introPendiente')) {
      this.registry.set('introPendiente', false);
      this.game.events.emit(EV.dialogoIniciar);   // avisa también a LocationScene (bloquea el movimiento)
    }
  }

  update() {
    this.botones.setVisible(this.esTactil && !this.activo && !this.inventario.visible);
    if (this.depurando) {
      this.depuracion.setText([
        'DEPURACIÓN (F1)',
        `duda ${narrativa.get('duda')} · sospecha ${narrativa.get('sospecha')} · jornada ${narrativa.get('jornada')}`,
        `${narrativa.get('nombre')} ${narrativa.get('apellido')} (${narrativa.get('genero')}) · ${narrativa.get('num')}`,
        `inventario: ${narrativa.list('inventario').join(', ')}`,
      ].join('\n'));
    }
  }

  // ------------------------------------------------------------------ construcción
  private crearCaja() {
    this.cajaFondo = this.add.rectangle(0, 0, CAJA.w, CAJA.h, COLOR.papel3).setOrigin(0).setStrokeStyle(2, COLOR.gris2);
    this.cajaFranja = this.add.rectangle(0, 0, 8, CAJA.h, COLOR.rojo3).setOrigin(0);
    this.texto = this.add.text(28, 22, '', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.gris2), lineSpacing: 6,
      wordWrap: { width: CAJA.w - 56, useAdvancedWrap: true },
    });
    this.nombreFondo = this.add.rectangle(20, -14, 10, 28, COLOR.gris2).setOrigin(0);
    this.nombre = this.add.text(32, -10, '', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) });
    this.indicador = this.add.text(CAJA.w - 26, CAJA.h - 26, '▼', { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.rojo3) });
    this.tweens.add({ targets: this.indicador, alpha: 0.2, duration: 450, yoyo: true, repeat: -1 });
    this.caja = this.add.container(CAJA.x, CAJA.y,
      [this.cajaFondo, this.cajaFranja, this.texto, this.nombreFondo, this.nombre, this.indicador]).setVisible(false).setDepth(30);
  }

  private crearPensamiento() {
    const banda = this.add.rectangle(480, 0, 960, 10, 0x000000, 0.55).setOrigin(0.5, 0);
    this.pensamientoTexto = this.add.text(480, 24, '', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 6,
      wordWrap: { width: 820, useAdvancedWrap: true }, stroke: '#000000', strokeThickness: 3,
    }).setOrigin(0.5, 0);
    this.pensamiento = this.add.container(0, 0, [banda, this.pensamientoTexto]).setVisible(false).setDepth(30);
    this.pensamiento.setData('banda', banda);
  }

  private crearCartel() {
    const fondo = this.add.rectangle(0, 0, 960, 540, COLOR.negro, 0.94).setOrigin(0);
    this.cartelTexto = this.add.text(480, 270, '', {
      fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 8,
      wordWrap: { width: 760, useAdvancedWrap: true },
    }).setOrigin(0.5);
    this.cartel = this.add.container(0, 0, [fondo, this.cartelTexto]).setVisible(false).setDepth(50);
  }

  private crearFoco() {
    const fondo = this.add.rectangle(0, 0, 10, 24, COLOR.gris1, 0.85).setOrigin(0.5, 1).setStrokeStyle(1, COLOR.gris3);
    this.focoTexto = this.add.text(0, -12, '', { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    this.foco = this.add.container(0, 0, [fondo, this.focoTexto]).setVisible(false).setDepth(15);
    this.foco.setData('fondo', fondo);
  }

  /** Botones táctiles: solo en dispositivos con pantalla táctil (diseño técnico §8). */
  private crearBotonesTactiles() {
    this.botones = this.add.container(0, 0).setDepth(20).setVisible(false);
    const boton = (x: number, y: number, r: number, etiqueta: string, alPulsar: () => void) => {
      const c = this.add.circle(x, y, r, COLOR.gris1, 0.55).setStrokeStyle(2, COLOR.papel3, 0.7).setInteractive();
      const t = this.add.text(x, y, etiqueta, { fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      c.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); alPulsar(); });
      this.botones.add([c, t]);
    };
    boton(880, 450, 44, 'USAR', () => this.game.events.emit(EV.accion, 'principal'));
    boton(790, 488, 34, 'MIRAR', () => this.game.events.emit(EV.accion, 'mirar'));
    boton(900, 92, 30, 'OBJ.', () => this.alternarInventario());
  }

  // ------------------------------------------------------------------ flujo de diálogo
  private iniciar(ruta?: string) {
    if (ruta) narrativa.goTo(ruta);
    this.activo = true;
    this.bloqueoHasta = this.time.now + 180;
    this.foco.setVisible(false);
    if (this.inventario.visible) this.alternarInventario();
    this.avanzar();
  }

  private avanzar() {
    const paso = narrativa.next();
    if (paso.type === 'line') this.mostrarLinea(paso.line);
    else if (paso.type === 'accion') void this.ejecutarAcciones(paso.acciones, paso.line);
    else if (paso.type === 'choices') this.mostrarOpciones(paso.choices);
    else this.terminar();
  }

  private terminar() {
    this.activo = false;
    this.ocultarTodo();
    if (this.velo.alpha > 0) this.tweens.add({ targets: this.velo, alpha: 0, duration: 700 });
    this.game.events.emit(EV.dialogoFin);
  }

  private ocultarTodo() {
    this.caja.setVisible(false);
    this.pensamiento.setVisible(false);
    this.cartel.setVisible(false);
    this.opciones.setVisible(false).removeAll(true);
    this.opcionesLista = [];
  }

  private confirmar() {
    if (!this.activo || this.enAccion || this.time.now < this.bloqueoHasta) return;
    if (this.opciones.visible) return this.elegir(this.opcionSel);
    if (this.escribiendo) return this.completarTexto();
    this.avanzar();
  }

  // ------------------------------------------------------------------ acciones bloqueantes
  private async ejecutarAcciones(acciones: Tag[], linea: Line | null) {
    this.enAccion = true;
    for (const a of acciones) {
      if (a.key === 'sfx') {
        audio.play(a.value);
      } else if (a.key === 'esperar') {
        this.ocultarTodo();
        await this.esperar(Number(a.value) * 1000 || 1000);
      } else if (a.key === 'fx') {
        await this.efecto(a.value);
      } else {
        const tipo = a.key === 'minijuego' ? a.value.split(',')[0].trim() : a.key;
        const escena = MINIJUEGOS[tipo];
        if (!escena) { console.warn(`[minijuego] desconocido: ${tipo}`); continue; }
        this.ocultarTodo();
        const r = await this.lanzarMinijuego(escena, a.params);
        this.aplicarResultado(tipo, a.params, r);
      }
    }
    this.enAccion = false;
    this.bloqueoHasta = this.time.now + 150;
    if (linea) this.mostrarLinea(linea); else this.avanzar();
  }

  private esperar(ms: number) {
    return new Promise<void>((ok) => this.time.delayedCall(ms, ok));
  }

  private lanzarMinijuego(escena: string, params: Record<string, string>) {
    return new Promise<ResultadoMinijuego>((ok) => this.scene.launch(escena, { params, alTerminar: ok }));
  }

  private aplicarResultado(tipo: string, params: Record<string, string>, r: ResultadoMinijuego) {
    if (tipo === 'cf') {
      const id = (params.id ?? '').toLowerCase().replace(/^cf-/, '').replace(/-/g, '_');
      narrativa.set(`cf_${id}`, r.resultado);
    } else if (tipo === 'ficha' && r.datos) {
      for (const k of ['nombre', 'apellido', 'num']) narrativa.set(k, String(r.datos[k]));
      narrativa.call('fijar_genero', String(r.datos.genero));
    } else if (params.vars && r.datos) {
      for (const [k, v] of Object.entries(r.datos)) narrativa.set(`${params.vars}_${k}`, v);
    }
  }

  /** Efectos de pantalla: negro, blanco, fundido, temblor, destello. */
  private efecto(fx: string): Promise<void> {
    const loc = this.scene.get('Location');
    return new Promise((ok) => {
      switch (fx) {
        case 'negro':
          this.velo.setFillStyle(0x000000);
          this.tweens.add({ targets: this.velo, alpha: 1, duration: 500, onComplete: () => ok() });
          break;
        case 'aclarar':
          this.tweens.add({ targets: this.velo, alpha: 0, duration: 700, onComplete: () => ok() });
          break;
        case 'blanco':
          this.velo.setFillStyle(0xffffff);
          this.tweens.add({ targets: this.velo, alpha: 1, duration: 1400, onComplete: () => ok() });
          break;
        case 'destello':
          this.velo.setFillStyle(0xffffff).setAlpha(1);
          this.tweens.add({ targets: this.velo, alpha: 0, duration: 900, onComplete: () => ok() });
          break;
        case 'temblor':
          loc?.cameras.main.shake(700, 0.012);
          this.time.delayedCall(700, () => ok());
          break;
        default:
          ok();
      }
    });
  }

  // ------------------------------------------------------------------ líneas
  private mostrarLinea(l: Line) {
    this.ocultarTodo();
    if (l.kind === 'pensamiento') {
      this.pensamiento.setVisible(true);
      this.escribir(this.pensamientoTexto, l.text);
      const banda = this.pensamiento.getData('banda') as Phaser.GameObjects.Rectangle;
      banda.setSize(960, this.alturaFinal(this.pensamientoTexto, l.text) + 44);
      return;
    }
    if (l.kind === 'cartel') {
      this.cartel.setVisible(true).setAlpha(0);
      this.tweens.add({ targets: this.cartel, alpha: 1, duration: 300 });
      this.cartelTexto.setText(l.text);
      return;
    }
    const tele = l.kind === 'telepantalla';
    this.cajaFondo.setFillStyle(tele ? COLOR.tele1 : COLOR.papel3).setStrokeStyle(2, tele ? COLOR.tele4 : COLOR.gris2);
    this.cajaFranja.setFillStyle(tele ? COLOR.tele4 : COLOR.rojo3);
    this.texto.setStyle({ fontFamily: tele ? FUENTE.maquina : FUENTE.texto, fontSize: tele ? '28px' : '22px',
      color: hex(tele ? COLOR.tele5 : COLOR.gris2) });
    const quien = tele ? 'TELEPANTALLA' : l.speaker === 'PROTAGONISTA' ? String(narrativa.get('nombre')).toUpperCase() : (l.speaker ?? '');
    this.nombre.setText(quien).setColor(hex(tele ? COLOR.tele5 : COLOR.papel4));
    this.nombreFondo.setVisible(!!quien).setSize(this.nombre.width + 24, 28).setFillStyle(tele ? COLOR.tele0 : COLOR.gris2);
    this.caja.setVisible(true);
    this.escribir(this.texto, l.text);
  }

  private alturaFinal(t: Phaser.GameObjects.Text, s: string) {
    const prev = t.text; t.setText(s); const h = t.height; t.setText(prev); return h;
  }

  private escribir(destino: Phaser.GameObjects.Text, texto: string) {
    this.escribiendo?.remove();
    this.destino = destino;
    this.textoCompleto = texto;
    this.indicador.setVisible(false);
    let n = 0;
    destino.setText('');
    this.escribiendo = this.time.addEvent({
      delay: 1000 / VELOCIDAD_TEXTO,
      repeat: texto.length - 1,
      callback: () => {
        n++;
        destino.setText(texto.slice(0, n));
        if (n >= texto.length) this.completarTexto();
      },
    });
  }

  private completarTexto() {
    this.escribiendo?.remove();
    this.escribiendo = null;
    this.destino?.setText(this.textoCompleto);
    this.indicador.setVisible(true);
  }

  // ------------------------------------------------------------------ elecciones
  private mostrarOpciones(choices: ChoiceOption[]) {
    this.caja.setVisible(false);
    this.opciones.removeAll(true);
    this.opcionesLista = [];
    const alto = 46, sep = 10, ancho = 700;
    const y0 = 290 - (choices.length * (alto + sep)) / 2;
    choices.forEach((c, i) => {
      const y = y0 + i * (alto + sep);
      const fondo = this.add.rectangle(480, y, ancho, alto, COLOR.gris2, 0.95).setStrokeStyle(2, COLOR.gris3)
        .setInteractive({ useHandCursor: true });
      const t = this.add.text(480, y, `${i + 1}. ${c.text}`, {
        fontFamily: FUENTE.texto, fontSize: '21px', color: hex(COLOR.papel4),
      }).setOrigin(0.5);
      fondo.on('pointerover', () => this.seleccionar(i));
      fondo.on('pointerup', () => this.elegir(i));
      this.opciones.add([fondo, t]);
      this.opcionesLista.push({ fondo, choice: c });
    });
    this.opciones.setVisible(true);
    this.seleccionar(0);
    this.bloqueoHasta = this.time.now + 200;
  }

  private seleccionar(i: number) {
    this.opcionSel = i;
    this.opcionesLista.forEach((o, j) => o.fondo.setFillStyle(j === i ? COLOR.rojo3 : COLOR.gris2, 0.95));
  }

  private moverSeleccion(d: number) {
    if (!this.opciones.visible || !this.opcionesLista.length) return;
    this.seleccionar((this.opcionSel + d + this.opcionesLista.length) % this.opcionesLista.length);
  }

  private elegir(i: number) {
    if (!this.opciones.visible || this.time.now < this.bloqueoHasta) return;
    const o = this.opcionesLista[i];
    if (!o) return;
    narrativa.choose(o.choice.index);
    this.opciones.setVisible(false).removeAll(true);
    this.opcionesLista = [];
    this.avanzar();
  }

  // ------------------------------------------------------------------ foco, joystick, inventario
  private mostrarFoco(info: FocoInfo | null) {
    if (!info || this.activo) { this.foco.setVisible(false); return; }
    const acciones = this.esTactil ? '' : [info.usar ? (info.hablar ? 'E hablar' : 'E usar') : '', info.mirar ? 'Q mirar' : ''].filter(Boolean).join(' · ');
    this.focoTexto.setText(`${info.nombre}${acciones ? '   ' + acciones : ''}`);
    const fondo = this.foco.getData('fondo') as Phaser.GameObjects.Rectangle;
    fondo.setSize(this.focoTexto.width + 20, 24);
    const x = Phaser.Math.Clamp(info.x, fondo.width / 2 + 4, 960 - fondo.width / 2 - 4);
    this.foco.setPosition(x, Phaser.Math.Clamp(info.y - 4, 30, 520)).setVisible(true);
  }

  private dibujarJoystick() {
    const g = this.joystick.clear();
    if (!tactil.activo) return;
    const { x: ox, y: oy } = tactil.origen;   // ya en coordenadas internas (960x540)
    g.fillStyle(COLOR.gris1, 0.35).fillCircle(ox, oy, 48).lineStyle(2, COLOR.papel3, 0.5).strokeCircle(ox, oy, 48);
    g.fillStyle(COLOR.papel3, 0.6).fillCircle(ox + tactil.x * 40, oy + tactil.y * 40, 18);
  }

  private alternarInventario() {
    const abrir = !this.inventario.visible && !this.activo;
    this.inventario.removeAll(true).setVisible(abrir);
    if (!abrir) return;
    const items = narrativa.list('inventario');
    const c = this.inventario;
    this.inventarioAbiertoEn = this.time.now;
    // el mismo toque que abre el panel no debe cerrarlo al soltarse
    c.add(this.add.rectangle(0, 0, 960, 540, 0x000000, 0.6).setOrigin(0).setInteractive()
      .on('pointerup', () => { if (this.time.now - this.inventarioAbiertoEn > 300) this.alternarInventario(); }));
    c.add(this.add.rectangle(480, 270, 640, 300, 0x2e221b).setStrokeStyle(3, 0x1a1411));
    c.add(this.add.text(480, 142, 'OBJETOS', { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4) }).setOrigin(0.5));
    const desc = this.add.text(480, 370, items.length ? 'Toca un objeto para mirarlo.' : 'No llevas nada.', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3), align: 'center', wordWrap: { width: 580 },
    }).setOrigin(0.5);
    c.add(desc);
    items.forEach((id, i) => {
      const item = ITEMS[id];
      const x = 480 - (items.length - 1) * 60 + i * 120, y = 250;
      const casilla = this.add.rectangle(x, y, 92, 92, 0x1a1411).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      c.add(casilla);
      if (item && this.textures.exists(item.icono)) c.add(this.add.image(x, y, item.icono).setScale(4));
      casilla.on('pointerup', () => desc.setText(item ? `${item.nombre}\n${item.descripcion}` : id));
    });
  }

  /** El ojo se abre a medida que sube la Sospecha (biblia visual §8). */
  private dibujarOjo(sospecha: number) {
    const g = this.ojo, cx = 920, cy = 30, w = 22;
    const apertura = Phaser.Math.Clamp(sospecha / 100, 0, 1);
    g.clear();
    g.fillStyle(COLOR.gris1, 0.8).fillCircle(cx, cy, 20);
    if (apertura < 0.05) {
      g.lineStyle(2, COLOR.papel3).lineBetween(cx - w / 2, cy, cx + w / 2, cy);
      return;
    }
    const h = 2 + apertura * 12;
    g.fillStyle(COLOR.papel4).fillEllipse(cx, cy, w, h);
    g.fillStyle(apertura > 0.75 ? COLOR.rojo4 : COLOR.tele4).fillCircle(cx, cy, Math.min(5, h / 2));
    g.fillStyle(COLOR.negro).fillCircle(cx, cy, Math.min(2, h / 3));
    if (apertura > 0.75) {
      g.lineStyle(1, COLOR.rojo4).lineBetween(cx - 10, cy - 1, cx - 6, cy).lineBetween(cx + 6, cy + 1, cx + 10, cy);
    }
  }

  private alternarDepuracion() {
    this.depurando = !this.depurando;
    this.depuracion.setVisible(this.depurando);
    this.game.events.emit(EV.depurar, this.depurando);
  }
}
