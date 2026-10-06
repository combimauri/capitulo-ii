/**
 * Capa de interfaz siempre activa (diseño técnico §7): diálogo, pensamientos, telepantalla,
 * carteles, elecciones, foco de objetos, ojo de la Sospecha y depuración.
 */
import Phaser from 'phaser';
import { narrativa, EV } from '../core/juego';
import type { ChoiceOption, Line } from '../core/NarrativeBridge';
import { COLOR, FUENTE, hex } from '../ui/estilo';

const VELOCIDAD_TEXTO = 55;          // caracteres por segundo
const CAJA = { x: 40, y: 386, w: 880, h: 132 };

const NOMBRES: Record<string, string> = { PROTAGONISTA: '' };

export class UIScene extends Phaser.Scene {
  private activo = false;
  private bloqueoHasta = 0;
  private escribiendo: Phaser.Time.TimerEvent | null = null;
  private textoCompleto = '';
  private destino: Phaser.GameObjects.Text | null = null;

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
  private opciones!: Phaser.GameObjects.Container;
  private opcionesLista: { fondo: Phaser.GameObjects.Rectangle; choice: ChoiceOption }[] = [];
  private opcionSel = 0;
  private foco!: Phaser.GameObjects.Container;
  private focoTexto!: Phaser.GameObjects.Text;
  private ojo!: Phaser.GameObjects.Graphics;
  private depuracion!: Phaser.GameObjects.Text;
  private depurando = false;

  constructor() { super('UI'); }

  create() {
    this.crearCaja();
    this.crearPensamiento();
    this.crearCartel();
    this.opciones = this.add.container(0, 0).setVisible(false);
    this.crearFoco();
    this.ojo = this.add.graphics();
    this.dibujarOjo(Number(narrativa.get('sospecha')) || 0);
    narrativa.observe('sospecha', (v) => this.dibujarOjo(Number(v)));
    this.depuracion = this.add.text(8, 8, '', {
      fontFamily: FUENTE.maquina, fontSize: '18px', color: '#ffd34d', backgroundColor: '#000000aa', padding: { x: 6, y: 4 },
    }).setVisible(false).setDepth(100);

    const ev = this.game.events;
    const iniciar = (ruta?: string) => this.iniciar(ruta);
    const foco = (info: FocoInfo | null) => this.mostrarFoco(info);
    ev.on(EV.dialogoIniciar, iniciar);
    ev.on(EV.foco, foco);
    this.events.once('shutdown', () => { ev.off(EV.dialogoIniciar, iniciar); ev.off(EV.foco, foco); });

    const kb = this.input.keyboard!;
    ['SPACE', 'ENTER', 'E'].forEach((k) => kb.on(`keydown-${k}`, () => this.confirmar()));
    kb.on('keydown-UP', () => this.moverSeleccion(-1));
    kb.on('keydown-DOWN', () => this.moverSeleccion(1));
    kb.on('keydown-W', () => this.moverSeleccion(-1));
    kb.on('keydown-S', () => this.moverSeleccion(1));
    kb.on('keydown', (e: KeyboardEvent) => {
      const n = Number(e.key);
      if (n >= 1 && n <= this.opcionesLista.length) this.elegir(n - 1);
    });
    kb.on('keydown-F1', () => this.alternarDepuracion());
    this.input.on('pointerdown', () => { if (this.activo && !this.opciones.visible) this.confirmar(); });

    if (this.registry.get('introPendiente')) {
      this.registry.set('introPendiente', false);
      this.game.events.emit(EV.dialogoIniciar);   // avisa también a LocationScene (bloquea el movimiento)
    }
  }

  update() {
    if (this.depurando) {
      this.depuracion.setText([
        'DEPURACIÓN (F1)',
        `duda ${narrativa.get('duda')} · sospecha ${narrativa.get('sospecha')} · jornada ${narrativa.get('jornada')}`,
        `desayunado ${narrativa.get('desayunado')} · tele_volumen ${narrativa.get('tele_volumen')}`,
        `inventario ${String(narrativa.get('inventario') ?? '')}`,
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
      [this.cajaFondo, this.cajaFranja, this.texto, this.nombreFondo, this.nombre, this.indicador]).setVisible(false);
  }

  private crearPensamiento() {
    const banda = this.add.rectangle(480, 0, 960, 10, 0x000000, 0.55).setOrigin(0.5, 0);
    this.pensamientoTexto = this.add.text(480, 24, '', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 6,
      wordWrap: { width: 820, useAdvancedWrap: true }, stroke: '#000000', strokeThickness: 3,
    }).setOrigin(0.5, 0);
    this.pensamiento = this.add.container(0, 0, [banda, this.pensamientoTexto]).setVisible(false);
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
    this.focoTexto = this.add.text(0, -12, '', {
      fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.papel4),
    }).setOrigin(0.5);
    this.foco = this.add.container(0, 0, [fondo, this.focoTexto]).setVisible(false);
    this.foco.setData('fondo', fondo);
  }

  // ------------------------------------------------------------------ flujo de diálogo
  private iniciar(ruta?: string) {
    if (ruta) narrativa.goTo(ruta);
    this.activo = true;
    this.bloqueoHasta = this.time.now + 180;
    this.foco.setVisible(false);
    this.avanzar();
  }

  private avanzar() {
    const paso = narrativa.next();
    if (paso.type === 'line') this.mostrarLinea(paso.line);
    else if (paso.type === 'choices') this.mostrarOpciones(paso.choices);
    else this.terminar();
  }

  private terminar() {
    this.activo = false;
    this.ocultarTodo();
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
    if (!this.activo || this.time.now < this.bloqueoHasta) return;
    if (this.opciones.visible) return this.elegir(this.opcionSel);
    if (this.escribiendo) return this.completarTexto();
    this.avanzar();
  }

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
    const quien = tele ? 'TELEPANTALLA' : (l.speaker ? (NOMBRES[l.speaker] ?? l.speaker) : '');
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
    const alto = 46, sep = 10, ancho = 620;
    const y0 = 270 - (choices.length * (alto + sep)) / 2;
    choices.forEach((c, i) => {
      const y = y0 + i * (alto + sep);
      const fondo = this.add.rectangle(480, y, ancho, alto, COLOR.gris2, 0.95).setStrokeStyle(2, COLOR.gris3)
        .setInteractive({ useHandCursor: true });
      const t = this.add.text(480, y, `${i + 1}. ${c.text}`, {
        fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4),
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

  // ------------------------------------------------------------------ foco y HUD
  private mostrarFoco(info: FocoInfo | null) {
    if (!info || this.activo) { this.foco.setVisible(false); return; }
    const acciones = [info.usar ? 'E usar' : '', info.mirar ? 'Q mirar' : ''].filter(Boolean).join(' · ');
    this.focoTexto.setText(`${info.nombre}${acciones ? '   ' + acciones : ''}`);
    const fondo = this.foco.getData('fondo') as Phaser.GameObjects.Rectangle;
    fondo.setSize(this.focoTexto.width + 20, 24);
    const x = Phaser.Math.Clamp(info.x, fondo.width / 2 + 4, 960 - fondo.width / 2 - 4);
    this.foco.setPosition(x, Math.max(30, info.y - 4)).setVisible(true);
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

interface FocoInfo { nombre: string; x: number; y: number; mirar: boolean; usar: boolean }
