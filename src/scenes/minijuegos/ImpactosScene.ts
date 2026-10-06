/**
 * Minijuego 3 — Registro de Impactos (guion J4.03, diseño técnico §6.4).
 * Cada parte de Defensa Civil se clava con una chincheta en su casilla del mapa de Londres
 * y se anota en el Libro. Herramientas (si están en el inventario): la lámina de zonificación
 * y el compás. Nadie comenta el patrón: el jugador lo ve solo.
 *   # minijuego:impactos,registro=j4,vars=registro_j4   → content/impactos/j4.json
 * Datos devueltos: lamina (si/no: miró el mapa con la lámina puesta), compas (si/no), fallos.
 * Modo guiado (guiado=si, J5.07): tras clavar las chinchetas, el juego obliga a superponer la lámina y a
 * trazar un círculo de 2 km desde cada ministerio. Después pasa Brooke: «Quite eso del mapa».
 * Devuelve además lamina_puesta (si/no): si la lámina seguía puesta al cerrar el libro.
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

interface Parte { distrito: string; celda: string; hora: string; bajas: number }
interface Registro { fecha: string; partes: Parte[]; anteriores?: string[] }
const REGISTROS = import.meta.glob('../../../content/impactos/*.json', { eager: true, import: 'default' }) as Record<string, Registro>;
const registroDe = (id: string) => Object.entries(REGISTROS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];

const COLS = 'ABCDEFGHIJKL';
const MAPA = { x: 44, y: 72, escala: 2, celda: { w: 24, h: 16 }, n: 12 };
const ANCHO = MAPA.celda.w * MAPA.escala, ALTO = MAPA.celda.h * MAPA.escala;
const KM_POR_CELDA = 2;
const PANEL = { x: 646, w: 290 };
/** Los cuatro ministerios (rombos blancos de la lámina), en casillas: los mismos que art/ui/londres.py. */
const MINISTERIOS = [[4.5, 5.6], [3.5, 4.4], [5.4, 4.0], [5.9, 5.3]];
const RADIO_GUIA = { km: 2, tolerancia: 0.5, centro: 14 };

/** "J-8" → columna 9, fila 7 (desde 0). */
export function celda(c: string) {
  const [l, n] = c.split('-');
  return { col: COLS.indexOf(l), fila: Number(n) - 1 };
}

export class ImpactosScene extends Minijuego {
  private reg!: Registro;
  private actual = 0;
  private fallos = 0;
  private lamina: Phaser.GameObjects.Image | null = null;
  private laminaVista = false;
  private compasUsado = false;
  private modo: 'chincheta' | 'compas' = 'chincheta';
  private circulos: Phaser.GameObjects.Container[] = [];
  private trazo: { x: number; y: number; g: Phaser.GameObjects.Graphics; t: Phaser.GameObjects.Text } | null = null;
  private tarjeta!: Phaser.GameObjects.Text;
  private libro!: Phaser.GameObjects.Container;
  private aviso!: Phaser.GameObjects.Text;
  private botonCompas: Phaser.GameObjects.Rectangle | null = null;
  private cerrar!: Phaser.GameObjects.Container;
  private guiado = false;
  private paso: 'chinchetas' | 'lamina' | 'compas' | 'brooke' = 'chinchetas';
  private ministerios: { x: number; y: number; hecho: boolean }[] = [];

  constructor() { super('Impactos'); }

  create() {
    this.reg = registroDe(this.params.registro ?? '')!;
    this.actual = 0; this.fallos = 0; this.laminaVista = false; this.compasUsado = false;
    this.modo = 'chincheta'; this.circulos = []; this.trazo = null; this.lamina = null; this.botonCompas = null;
    this.guiado = this.params.guiado === 'si';
    this.paso = 'chinchetas';
    this.ministerios = MINISTERIOS.map(([c, f]) => ({ x: MAPA.x + c * ANCHO, y: MAPA.y + f * ALTO, hecho: false }));
    const { width, height } = this.scale;
    const inventario = narrativa.list('inventario');
    this.cameras.main.fadeIn(300, 11, 12, 15);

    // la mesa del Registro
    this.add.rectangle(width / 2, height / 2, width, height, 0x2e221b);
    for (let y = 0; y < height; y += 18) this.add.rectangle(width / 2, y, width, 1, 0x1a1411);
    this.add.text(24, 18, `REGISTRO DE IMPACTOS · DEFENSA CIVIL · ${this.reg.fecha}`, {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4),
    });

    // mapa bajo el cristal, con su cuadrícula rotulada
    const mw = ANCHO * MAPA.n, mh = ALTO * MAPA.n;
    this.add.rectangle(MAPA.x - 18, MAPA.y - 18, mw + 26, mh + 26, 0x1a1411).setOrigin(0);
    const mapa = this.add.image(MAPA.x, MAPA.y, 'londres').setOrigin(0).setScale(MAPA.escala).setInteractive();
    for (let i = 0; i < MAPA.n; i++) {
      this.add.text(MAPA.x + i * ANCHO + ANCHO / 2, MAPA.y - 10, COLS[i], { fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.papel3) }).setOrigin(0.5);
      this.add.text(MAPA.x - 9, MAPA.y + i * ALTO + ALTO / 2, String(i + 1), { fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.papel3) }).setOrigin(0.5);
    }
    this.add.rectangle(MAPA.x + 10, MAPA.y + mh - 12, ANCHO, 4, COLOR.gris2).setOrigin(0, 0.5);
    this.add.text(MAPA.x + 10, MAPA.y + mh - 30, `${KM_POR_CELDA} km`, { fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.gris2) });

    // chinchetas de días anteriores
    for (const id of this.reg.anteriores ?? []) {
      for (const p of registroDe(id)?.partes ?? []) this.chincheta(p.celda, false);
    }
    // el parte ilegible de la víspera, si alguien fue a completarlo
    if (this.params.ilegible && narrativa.get('ilegible_completado') === true) this.chincheta(this.params.ilegible, false);

    // el parte del tubo
    this.add.rectangle(PANEL.x, MAPA.y - 18, PANEL.w, 128, COLOR.papel4).setOrigin(0).setStrokeStyle(1, 0x8f8a7a);
    this.add.text(PANEL.x + 12, MAPA.y - 10, 'DEF. CIVIL · IMPACTO', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.rojo3) });
    this.tarjeta = this.add.text(PANEL.x + 12, MAPA.y + 12, '', { fontFamily: FUENTE.maquina, fontSize: '21px', color: hex(COLOR.gris2), lineSpacing: 0 });

    // el Libro de Registro (las páginas anteriores, arrancadas)
    const ly = MAPA.y + 124;
    this.add.rectangle(PANEL.x, ly, PANEL.w, mh - 124 + 8, COLOR.papel3).setOrigin(0).setStrokeStyle(1, 0x8f8a7a);
    for (let y = ly + 4; y < ly + mh - 124; y += 7) this.add.rectangle(PANEL.x - 3, y, 6, 3, COLOR.papel3);   // restos de papel en el lomo
    this.add.text(PANEL.x + 12, ly + 8, `LIBRO DE REGISTRO · ${this.reg.fecha}`, { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.gris2) });
    this.libro = this.add.container(PANEL.x + 12, ly + 34);

    // herramientas
    this.aviso = this.add.text(MAPA.x, height - 34, 'Toca la casilla del parte para clavar la chincheta.', {
      fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3),
    }).setOrigin(0, 0.5);
    let bx = PANEL.x;
    if (inventario.includes('zonificacion')) {
      this.lamina = this.add.image(MAPA.x, MAPA.y, 'londres-zonas').setOrigin(0).setScale(MAPA.escala).setVisible(false).setDepth(2);
      this.boton(bx + 70, height - 34, 'LÁMINA', () => this.alternarLamina());
      bx += 148;
    }
    if (inventario.includes('compas')) {
      this.botonCompas = this.boton(bx + 70, height - 34, 'COMPÁS', () => this.alternarCompas());
    }
    this.cerrar = this.add.container(0, 0).setVisible(false).setDepth(10);
    const fc = this.add.rectangle(PANEL.x + PANEL.w / 2, MAPA.y + mh - 22, PANEL.w - 30, 36, COLOR.gris2).setStrokeStyle(2, COLOR.rojo3)
      .setInteractive({ useHandCursor: true });
    this.cerrar.add([fc, this.add.text(fc.x, fc.y, 'CERRAR EL LIBRO', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5)]);
    fc.on('pointerup', () => this.acabar());

    mapa.on('pointerdown', (p: Phaser.Input.Pointer) => this.pulsarMapa(p));
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => this.moverCompas(p));
    this.input.on('pointerup', () => this.soltarCompas());

    audio.play('tubo');
    this.mostrarParte();
  }

  private boton(x: number, y: number, texto: string, alPulsar: () => void) {
    const fondo = this.add.rectangle(x, y, 132, 36, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(x, y, texto, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    fondo.on('pointerup', alPulsar);
    return fondo;
  }

  private mostrarParte() {
    const p = this.reg.partes[this.actual];
    if (!p) {
      this.tarjeta.setText('Sin más partes.');
      if (this.guiado) return this.guia();
      this.aviso.setText(this.lamina || this.botonCompas ? 'El libro está al día. Puedes seguir mirando el mapa.' : 'El libro está al día.');
      this.cerrar.setVisible(true);
      return;
    }
    this.tarjeta.setText([`DISTRITO: ${p.distrito}`, `CUADR.: ${p.celda}`, `HORA: ${p.hora}`, `BAJAS: ${p.bajas}`].join('\n'));
  }

  private celdaEn(p: Phaser.Input.Pointer) {
    const col = Math.floor((p.x - MAPA.x) / ANCHO), fila = Math.floor((p.y - MAPA.y) / ALTO);
    return col >= 0 && col < MAPA.n && fila >= 0 && fila < MAPA.n ? `${COLS[col]}-${fila + 1}` : null;
  }

  private pulsarMapa(p: Phaser.Input.Pointer) {
    if (this.modo === 'compas') return this.empezarCompas(p);
    const parte = this.reg.partes[this.actual];
    const c = this.celdaEn(p);
    if (!parte || !c) return;
    if (c !== parte.celda) {
      // la chincheta rebota con un «clac» seco (tutorial: sin penalización)
      this.fallos++;
      audio.play('tecla');
      const rebote = this.add.circle(p.x, p.y, 5, 0x111111).setDepth(5);
      this.tweens.add({ targets: rebote, x: p.x + Phaser.Math.Between(-30, 30), y: p.y - 30, alpha: 0, duration: 420, ease: 'Quad.easeOut', onComplete: () => rebote.destroy() });
      return;
    }
    this.chincheta(c, true);
    audio.play('sello');
    this.anotar(parte);
    this.actual++;
    this.time.delayedCall(350, () => { if (this.actual < this.reg.partes.length) audio.play('tubo'); this.mostrarParte(); });
  }

  private chincheta(c: string, nueva: boolean) {
    const { col, fila } = celda(c);
    const x = MAPA.x + col * ANCHO + ANCHO / 2 + Phaser.Math.Between(-6, 6);
    const y = MAPA.y + fila * ALTO + ALTO / 2 + Phaser.Math.Between(-4, 4);
    const pin = this.add.container(x, y).setDepth(4);
    pin.add([this.add.circle(1, 2, 5, 0x000000, 0.35), this.add.circle(0, 0, 5, nueva ? 0x15161a : 0x3a3d44), this.add.circle(-1.5, -1.5, 1.5, 0x8a8f99)]);
    if (nueva) { pin.setScale(1.8).setAlpha(0); this.tweens.add({ targets: pin, scale: 1, alpha: 1, duration: 160, ease: 'Quad.easeIn' }); }
  }

  private anotar(p: Parte) {
    const n = this.libro.length;
    const t = this.add.text(0, n * 26, '', { fontFamily: FUENTE.maquina, fontSize: '19px', color: hex(COLOR.gris2) });
    this.libro.add(t);
    const linea = `${n + 1} · ${p.distrito.slice(0, 12)} · ${p.celda} · ${p.hora} · ${p.bajas}`;
    let i = 0;
    this.time.addEvent({ delay: 18, repeat: linea.length - 1, callback: () => t.setText(linea.slice(0, ++i)) });
  }

  // ------------------------------------------------------------------ herramientas
  private alternarLamina() {
    if (!this.lamina) return;
    const ver = !this.lamina.visible;
    this.lamina.setVisible(ver);
    audio.play('plumilla');
    // «mirarla» cuenta cuando ya hay chinchetas suficientes para ver dónde caen
    if (ver && this.actual >= Math.ceil(this.reg.partes.length / 2)) this.laminaVista = true;
    if (this.paso === 'lamina' && ver) { this.paso = 'compas'; this.guia(); }
  }

  /** La secuencia guiada del J5: el juego no deja mirar hacia otro lado. */
  private guia(): void {
    if (this.paso === 'chinchetas') {
      this.paso = 'lamina';
      if (this.lamina?.visible) { this.paso = 'compas'; return this.guia(); }
      this.aviso.setText('¿Por qué nunca en el centro? Superpón la lámina de zonificación.');
    } else if (this.paso === 'compas') {
      if (this.modo !== 'compas') this.alternarCompas();
      this.aviso.setText('Traza un círculo de 2 km desde cada ministerio (los rombos blancos).');
    } else if (this.paso === 'brooke') {
      if (this.modo === 'compas') this.alternarCompas();
      this.aviso.setText('BROOKE, al pasar, muy bajo: «Quite eso del mapa antes de las seis. Voss hace la ronda a las seis.»')
        .setColor(hex(COLOR.ocre4)).setWordWrapWidth(470);
      this.cerrar.setVisible(true);
    }
  }

  /** ¿El círculo sale de un ministerio con un radio de unos 2 km? */
  private comprobarMinisterio(x: number, y: number, r: number) {
    if (this.paso !== 'compas') return;
    const km = (r / ANCHO) * KM_POR_CELDA;
    const m = this.ministerios.find((p) => !p.hecho && Phaser.Math.Distance.Between(p.x, p.y, x, y) <= RADIO_GUIA.centro);
    if (!m || Math.abs(km - RADIO_GUIA.km) > RADIO_GUIA.tolerancia) return;
    m.hecho = true;
    audio.play('acierto');
    this.add.text(m.x + 7, m.y - 18, '✓', { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.rojo3) }).setDepth(8);
    const faltan = this.ministerios.filter((p) => !p.hecho).length;
    if (faltan) this.aviso.setText(`Ninguna chincheta dentro. Faltan ${faltan} ministerio${faltan > 1 ? 's' : ''}.`);
    else this.time.delayedCall(900, () => { this.paso = 'brooke'; this.guia(); });
  }

  private alternarCompas() {
    this.modo = this.modo === 'compas' ? 'chincheta' : 'compas';
    this.botonCompas?.setFillStyle(this.modo === 'compas' ? COLOR.rojo3 : COLOR.gris2);
    this.aviso.setText(this.modo === 'compas' ? 'Compás: arrastra desde un punto del mapa para trazar un círculo.' : 'Toca la casilla del parte para clavar la chincheta.');
  }

  private empezarCompas(p: Phaser.Input.Pointer) {
    const g = this.add.graphics().setDepth(6);
    const t = this.add.text(p.x, p.y, '', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.rojo3), backgroundColor: '#eeead9' }).setDepth(7);
    this.trazo = { x: p.x, y: p.y, g, t };
  }

  private moverCompas(p: Phaser.Input.Pointer) {
    if (!this.trazo || !p.isDown) return;
    const r = Phaser.Math.Distance.Between(this.trazo.x, this.trazo.y, p.x, p.y);
    this.trazo.g.clear().lineStyle(2, COLOR.rojo3, 0.9).strokeCircle(this.trazo.x, this.trazo.y, r)
      .fillStyle(COLOR.rojo3).fillCircle(this.trazo.x, this.trazo.y, 2).lineBetween(this.trazo.x, this.trazo.y, p.x, p.y);
    this.trazo.t.setPosition(p.x + 8, p.y - 18).setText(`${((r / ANCHO) * KM_POR_CELDA).toFixed(1)} km`);
  }

  private soltarCompas() {
    if (!this.trazo) return;
    const p = this.input.activePointer;
    this.comprobarMinisterio(this.trazo.x, this.trazo.y, Phaser.Math.Distance.Between(this.trazo.x, this.trazo.y, p.x, p.y));
    const c = this.add.container(0, 0, [this.trazo.g, this.trazo.t]);
    this.trazo = null;
    this.circulos.push(c);
    this.compasUsado = true;
    while (this.circulos.length > (this.guiado ? 4 : 3)) this.circulos.shift()?.destroy();
  }

  private acabar() {
    if (this.lamina?.visible) this.laminaVista = true;
    const puesta = this.lamina?.visible;
    this.terminar({
      resultado: 'hecho',
      datos: {
        lamina: this.laminaVista ? 'si' : 'no', compas: this.compasUsado ? 'si' : 'no', fallos: this.fallos,
        lamina_puesta: puesta ? 'si' : 'no',
      },
    });
  }
}
