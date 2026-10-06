/**
 * El mapa de los pájaros (guion J13.02): tres capas sobre el mapa de Londres — los dibujos de Amory,
 * la lámina de zonificación y los círculos del compás. Primero, deducir dónde está San Clemente
 * («los cohetes no caen donde no quieren que caigan»); después, elegir la ruta entre bifurcaciones
 * evitando los derrumbes (pájaros de alas cerradas).
 *   # minijuego:tuneles,vars=mapa   → mapa_deducido (si/no), mapa_derrumbes
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';
import red from '../../../content/tuneles.json';

interface Nodo { id: string; nombre: string; x: number; y: number }
interface Tramo { a: string; b: string; derrumbe: boolean }
interface Red { nodos: Nodo[]; tramos: Tramo[]; inicio: string; fin: string }

const RED = red as Red;
const MAPA = { x: 40, y: 92, escala: 2 };
const CELDA = 24;
/** Los cuatro ministerios, en casillas (art/ui/londres.py): la Verdad, el Amor, la Paz, la Abundancia. */
const MINISTERIOS = [[4.5, 5.6], [3.5, 4.4], [5.4, 4.0], [5.9, 5.3]];
const INTENTOS = 3;
const PACIENCIA = 120000;

const aPantalla = (x: number, y: number) => ({ x: MAPA.x + x * MAPA.escala, y: MAPA.y + y * MAPA.escala });

export class TunelesScene extends Minijuego {
  private capas: Record<string, Phaser.GameObjects.GameObject> = {};
  private fase: 'deducir' | 'ruta' | 'hecho' = 'deducir';
  private fallos = 0;
  private derrumbes = 0;
  private actual = '';
  private deducido = true;
  private aviso!: Phaser.GameObjects.Text;
  private ruta!: Phaser.GameObjects.Graphics;
  private marcas!: Phaser.GameObjects.Graphics;
  private inicio = 0;

  constructor() { super('Tuneles'); }

  create() {
    const { width, height } = this.scale;
    this.capas = {}; this.fase = 'deducir'; this.fallos = 0; this.derrumbes = 0; this.deducido = true;
    this.actual = RED.inicio;
    this.inicio = this.time.now;
    this.cameras.main.fadeIn(400, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0d0b09).setOrigin(0);
    this.add.text(24, 18, 'EL MAPA DE LOS PÁJAROS', { fontFamily: FUENTE.maquina, fontSize: '28px', color: hex(COLOR.ocre4) });
    this.add.image(MAPA.x, MAPA.y, 'londres').setOrigin(0).setScale(MAPA.escala);

    const inv = narrativa.list('inventario');
    // las capas: la lámina y los círculos solo si se conservan la lámina y el compás
    const lamina = this.add.image(MAPA.x, MAPA.y, 'londres-zonas').setOrigin(0).setScale(MAPA.escala).setAlpha(0.75).setVisible(false);
    const compas = this.add.graphics().setVisible(false);
    for (const [c, f] of MINISTERIOS) {
      const p = aPantalla(c * CELDA, f * 16);
      compas.lineStyle(2, COLOR.rojo3, 0.9).strokeCircle(p.x, p.y, CELDA * MAPA.escala).fillStyle(COLOR.rojo3).fillCircle(p.x, p.y, 2);
    }
    const amory = this.add.image(MAPA.x, MAPA.y, 'londres-tuneles').setOrigin(0).setScale(MAPA.escala);
    this.capas = { amory, lamina, compas };
    this.marcas = this.add.graphics();
    this.ruta = this.add.graphics();

    const PANEL = 640;
    this.add.text(PANEL, 92, 'CAPAS', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel3) });
    const boton = (y: number, texto: string, capa: string, disponible: boolean) => {
      const f = this.add.rectangle(PANEL + 140, y, 280, 38, disponible ? COLOR.gris2 : COLOR.gris1).setStrokeStyle(2, COLOR.gris3);
      const t = this.add.text(PANEL + 140, y, disponible ? texto : `${texto} (no la tengo)`, {
        fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(disponible ? COLOR.papel4 : COLOR.gris3),
      }).setOrigin(0.5);
      if (!disponible) return;
      const pintar = () => f.setFillStyle((this.capas[capa] as unknown as Phaser.GameObjects.Components.Visible).visible ? COLOR.rojo3 : COLOR.gris2);
      f.setInteractive({ useHandCursor: true }).on('pointerup', () => {
        const c = this.capas[capa] as unknown as Phaser.GameObjects.Components.Visible;
        c.setVisible(!c.visible);
        audio.play('papel');
        pintar();
      });
      pintar();
      t.setDepth(1);
    };
    boton(140, 'DIBUJOS DE AMORY', 'amory', inv.includes('dibujos_amory'));
    boton(186, 'LÁMINA DE ZONAS', 'lamina', inv.includes('zonificacion'));
    boton(232, 'CÍRCULOS (COMPÁS)', 'compas', inv.includes('compas'));
    this.aviso = this.add.text(PANEL, 270, '', {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel4), wordWrap: { width: 290 }, lineSpacing: 4,
    });
    this.decir('«Los cohetes no caen donde no quieren que caigan.»\n«Excluir radio 2 km de edificios ministeriales.»\n\n¿Dónde está San Clemente? Toca el sitio en el mapa.');
    this.input.on('pointerup', (p: Phaser.Input.Pointer) => this.tocar(p));
  }

  private decir(texto: string) { this.aviso.setText(texto); }

  private nodo(id: string) { return RED.nodos.find((n) => n.id === id)!; }

  private tocar(p: Phaser.Input.Pointer) {
    const x = (p.x - MAPA.x) / MAPA.escala, y = (p.y - MAPA.y) / MAPA.escala;
    if (x < 0 || y < 0 || x > 288 || y > 192) return;
    if (this.fase === 'deducir') return this.deducir(x, y);
    if (this.fase === 'ruta') return this.elegir(x, y);
  }

  private deducir(x: number, y: number) {
    const sc = this.nodo(RED.fin);
    if (Math.hypot(sc.x - x, sc.y - y) <= 10) return this.encontrada();
    this.fallos++;
    audio.play('fallo');
    const p = aPantalla(x, y);
    this.marcas.lineStyle(2, COLOR.rojo4).lineBetween(p.x - 6, p.y - 6, p.x + 6, p.y + 6).lineBetween(p.x + 6, p.y - 6, p.x - 6, p.y + 6);
    if (this.fallos >= INTENTOS) {
      this.deducido = false;
      this.decir('El círculo del Miniver… Dentro, un pájaro dorado. El único.');
      this.time.delayedCall(1800, () => this.encontrada());
    } else {
      this.decir(['Aquí sí caen. Lo registré yo.', 'No. Más cerca de ellos. Donde nunca cae nada.'][this.fallos - 1] ?? 'No.');
    }
  }

  private encontrada() {
    if (this.fase !== 'deducir') return;
    this.fase = 'ruta';
    audio.play('acierto');
    const sc = aPantalla(this.nodo(RED.fin).x, this.nodo(RED.fin).y);
    const brillo = this.add.circle(sc.x, sc.y, 12).setStrokeStyle(3, COLOR.ocre4);
    this.tweens.add({ targets: brillo, scale: 1.6, alpha: 0.3, duration: 700, yoyo: true, repeat: -1 });
    this.decir('San Clemente. El único sitio de Londres donde nunca cae un cohete.\n\nAhora, el camino: toca la siguiente estación. Evita los pájaros con las alas cerradas.');
    this.dibujarNodos();
  }

  private dibujarNodos() {
    for (const n of RED.nodos) {
      const p = aPantalla(n.x, n.y);
      this.add.circle(p.x, p.y, n.id === this.actual ? 7 : 5, n.id === this.actual ? COLOR.ocre4 : 0x2a2218).setStrokeStyle(2, COLOR.ocre4);
    }
  }

  private elegir(x: number, y: number) {
    const destino = RED.nodos.find((n) => Math.hypot(n.x - x, n.y - y) <= 9);
    if (!destino || destino.id === this.actual) return;
    const tramo = RED.tramos.find((t) => (t.a === this.actual && t.b === destino.id) || (t.b === this.actual && t.a === destino.id));
    if (!tramo) { this.decir('Por ahí no hay túnel. Desde aquí, solo las estaciones unidas.'); return; }
    const a = aPantalla(this.nodo(this.actual).x, this.nodo(this.actual).y), b = aPantalla(destino.x, destino.y);
    if (tramo.derrumbe) {
      this.derrumbes++;
      audio.play('golpes');
      this.cameras.main.shake(200, 0.004);
      this.ruta.lineStyle(3, COLOR.rojo4, 0.9).lineBetween(a.x, a.y, (a.x + b.x) / 2, (a.y + b.y) / 2);
      this.decir(`Un pájaro con las alas cerradas. Derrumbe. Hay que volver a ${this.nodo(this.actual).nombre}.`);
      return;
    }
    audio.play('tecla');
    this.ruta.lineStyle(4, COLOR.ocre4, 0.95).lineBetween(a.x, a.y, b.x, b.y);
    this.actual = destino.id;
    this.add.circle(b.x, b.y, 7, COLOR.ocre4).setStrokeStyle(2, 0x2a2218);
    if (destino.id === RED.fin) {
      this.fase = 'hecho';
      this.decir('Bajo las campanas.');
      this.time.delayedCall(1400, () => this.terminar({ resultado: 'ruta', datos: { deducido: this.deducido ? 'si' : 'no', derrumbes: this.derrumbes } }, 600));
    } else {
      this.decir(`${destino.nombre}. ¿Y ahora?`);
    }
  }

  update() {
    if (this.fase === 'deducir' && this.time.now - this.inicio > PACIENCIA) { this.fallos = INTENTOS - 1; this.deducir(-100, -100); }
  }
}
