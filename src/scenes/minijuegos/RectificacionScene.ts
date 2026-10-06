/**
 * Minijuego 4 — La Gran Rectificación (guion J10.04). Contrarreloj de madrugada.
 *   fase=1: arrancar las banderitas negras de Eurasia en Malabar, clavar las amarillas de Estasia en otros
 *           frentes y corregir partes antiguos tocando cada «euroasiático».
 *   fase=2: el Libro de Registro de impactos: tachar «euroasiáticos» en cada cabecera y escribir «estasiáticos».
 *   # minijuego:rectificacion,fase=1,duda=alta,resultado=rectificacion_1   → "completa" | "incompleta"
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const MAPA = { x: 120, y: 92, escala: 2 };
/** Banderas negras de Eurasia sobre Malabar (coordenadas de la imagen mapa-frente). */
const NEGRAS = [{ x: 70, y: 166 }, { x: 95, y: 158 }, { x: 120, y: 150 }, { x: 170, y: 150 }, { x: 220, y: 134 }, { x: 245, y: 130 }, { x: 270, y: 126 }];
/** Casillas de los frentes del este en mapa-estasia (dos por frente). */
export const CASILLAS_ESTASIA = [{ x: 78, y: 74 }, { x: 128, y: 92 }, { x: 214, y: 52 }, { x: 238, y: 88 }, { x: 150, y: 162 }, { x: 262, y: 170 }];

const PARTES = [
  'PARTE N.º 7 · 2.4.84 · MALABAR. Las fuerzas euroasiáticas han sido rechazadas en el sector norte. Dos mil prisioneros euroasiáticos. La aviación euroasiática no ha comparecido.',
  'PARTE N.º 11 · 22.4.84 · MYSORE. El enemigo euroasiático mantiene sus posiciones. Resistido con firmeza. Bajas euroasiáticas estimadas: novecientas.',
];
const CAMBIO: Record<string, string> = {
  'euroasiáticas': 'estasiáticas', 'euroasiáticos': 'estasiáticos', 'euroasiática': 'estasiática', 'euroasiático': 'estasiático',
};
const PAGINAS = [
  ['19.4.84 · WATNEY ST. · J-8 · 08:12 · 7', '19.4.84 · WAPPING · I-9 · 00:40 · 3', '19.4.84 · ROTHERHITHE · J-10 · 02:55 · 5'],
  ['11.4.84 · LIMEHOUSE · J-7 · 02:20 · 4', '12.4.84 · STEPNEY · K-6 · 23:05 · 2', '14.4.84 · SHADWELL · J-8 · 03:15 · 6'],
  ['03.5.84 · BERMONDSEY · H-10 · 01:30', '03.5.84 · POPLAR · K-7 · 03:50', '04.5.84 · WAPPING · I-9 · 02:10'],
  ['05.5.84 · SOUTHWARK (BOROUGH) · F-10 · 22:45', '07.5.84 · DEPTFORD · K-11 · 04:10'],
];
const PENSAMIENTOS = {
  1: { media: ['Doce kilómetros en Malabar. Contra Eurasia.', 'Agujeros vacíos. El corcho parece un colador.', 'Siempre fue Estasia. Lo dice el papel.'],
    alta: ['Ivy murió por Eurasia. Ahora Ivy murió por Estasia.', 'Agujeros vacíos. Un frente entero, en una noche.', 'Sé que miento. Lo sé. Lo hago igual.'] },
  2: { media: ['Los cohetes de la semana pasada eran euroasiáticos. Ahora son estasiáticos.', 'Siguen saliendo de Folkestone.'],
    alta: ['Bermondsey, estasiático. Poplar, estasiático.', 'Watney Street, estasiático. Sammy murió por Estasia.', 'Ya está corregido.'] },
} as const;

export class RectificacionScene extends Minijuego {
  private restante = 0;
  private hecho = false;
  private capa!: Phaser.GameObjects.Container;
  private reloj!: Phaser.GameObjects.Text;
  private consigna!: Phaser.GameObjects.Text;
  private pensamiento!: Phaser.GameObjects.Text;
  private pendientes = 0;
  private pasos: (() => void)[] = [];

  constructor() { super('Rectificacion'); }

  create() {
    const { width, height } = this.scale;
    const fase = this.params.fase === '2' ? 2 : 1;
    this.restante = fase === 1 ? 150 : 75;
    this.hecho = false;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x1a1411).setOrigin(0);
    this.capa = this.add.container(0, 0);
    this.reloj = this.add.text(width - 20, 12, '', { fontFamily: FUENTE.maquina, fontSize: '32px', color: hex(COLOR.papel4) }).setOrigin(1, 0).setDepth(10);
    this.consigna = this.add.text(24, 14, '', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setDepth(10);
    this.pensamiento = this.add.text(width / 2, height - 30, '', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), stroke: '#000', strokeThickness: 4, align: 'center',
    }).setOrigin(0.5).setDepth(10);
    const lista = PENSAMIENTOS[fase][this.params.duda === 'alta' ? 'alta' : 'media'];
    let k = 0;
    const pensar = () => {
      if (this.hecho) return;
      this.pensamiento.setText(lista[k++ % lista.length]).setAlpha(1);
      this.tweens.add({ targets: this.pensamiento, alpha: 0, delay: 3200, duration: 600 });
    };
    this.time.addEvent({ delay: 5200, loop: true, callback: pensar, startAt: 3600 });
    this.pasos = fase === 1 ? [() => this.banderas(), () => this.estasia(), () => this.parte(0), () => this.parte(1)] : PAGINAS.map((_, i) => () => this.pagina(i));
    this.siguiente();
  }

  private siguiente() {
    this.capa.removeAll(true);
    const paso = this.pasos.shift();
    if (!paso) return this.acabar('completa');
    paso();
  }

  private hecha() {
    this.pendientes--;
    if (this.pendientes <= 0) this.time.delayedCall(450, () => { if (!this.hecho) this.siguiente(); });
  }

  // ------------------------------------------------------------------ fase 1
  private banderas() {
    this.consigna.setText('Malabar. Arranca las banderas negras de Eurasia.');
    this.capa.add(this.add.image(MAPA.x, MAPA.y, 'mapa-frente').setOrigin(0).setScale(MAPA.escala));
    // el corcho, acribillado
    const g = this.add.graphics().fillStyle(0x000000, 0.55);
    for (let i = 0; i < 60; i++) g.fillCircle(MAPA.x + Phaser.Math.Between(20, 700), MAPA.y + Phaser.Math.Between(20, 380), 1.5);
    this.capa.add(g);
    this.pendientes = NEGRAS.length;
    NEGRAS.forEach((p) => {
      const x = MAPA.x + p.x * MAPA.escala, y = MAPA.y + p.y * MAPA.escala;
      const b = this.bandera(x, y, 0x16181c);
      b.setSize(30, 40).setInteractive({ useHandCursor: true });
      b.once('pointerup', () => {
        audio.play('tecla');
        this.tweens.add({ targets: b, y: y - 60, alpha: 0, angle: 40, duration: 300, onComplete: () => b.destroy() });
        this.capa.add(this.add.circle(x, y + 10, 2, 0x000000));
        this.hecha();
      });
    });
  }

  private estasia() {
    this.consigna.setText('Manchuria, Mongolia, Indonesia. Clava las banderas amarillas de Estasia.');
    const tiene = this.textures.exists('mapa-estasia');
    this.capa.add(tiene ? this.add.image(MAPA.x, MAPA.y, 'mapa-estasia').setOrigin(0).setScale(MAPA.escala)
      : this.add.rectangle(MAPA.x, MAPA.y, 720, 400, 0x6a5a3a).setOrigin(0));
    this.pendientes = CASILLAS_ESTASIA.length;
    CASILLAS_ESTASIA.forEach((p) => {
      const x = MAPA.x + p.x * MAPA.escala, y = MAPA.y + p.y * MAPA.escala;
      const hueco = this.add.circle(x, y, 9).setStrokeStyle(2, 0xe0bf68, 0.9).setInteractive({ useHandCursor: true });
      this.capa.add(hueco);
      hueco.once('pointerup', () => {
        hueco.destroy();
        audio.play('sello');
        this.capa.add(this.bandera(x, y, 0xe0bf68));
        this.hecha();
      });
    });
  }

  private bandera(x: number, y: number, color: number) {
    const c = this.add.container(x, y);
    c.add(this.add.rectangle(0, -10, 2, 24, 0x8a8a8a));
    c.add(this.add.rectangle(1, -20, 16, 11, color).setOrigin(0, 0.5).setStrokeStyle(1, 0x000000));
    this.capa.add(c);
    return c;
  }

  /** Un parte antiguo: cada «euroasiático» se toca y se convierte en «estasiático». */
  private parte(i: number) {
    const { width } = this.scale;
    this.consigna.setText(`Partes antiguos (${i + 1}/${PARTES.length}). Corrige cada «euroasiático».`);
    this.capa.add(this.add.rectangle(width / 2, 270, 760, 330, 0xeeead9).setStrokeStyle(1, 0x8f8a7a));
    const est = { fontFamily: FUENTE.maquina, fontSize: '28px', color: '#22252a' };
    let x = 130, y = 140;
    this.pendientes = 0;
    for (const palabra of PARTES[i].split(' ')) {
      const limpia = palabra.replace(/[.,:]/g, '');
      const t = this.add.text(x, y, palabra, est);
      if (x + t.width > 830) { x = 130; y += 40; t.setPosition(x, y); }
      this.capa.add(t);
      if (CAMBIO[limpia]) {
        this.pendientes++;
        t.setColor(hex(COLOR.rojo3)).setInteractive({ useHandCursor: true });
        this.capa.add(this.add.rectangle(t.x, t.y + t.height - 2, t.width, 2, COLOR.rojo3).setOrigin(0));
        t.once('pointerup', () => {
          audio.play('tecla');
          t.setText(palabra.replace(limpia, CAMBIO[limpia])).setColor('#1d2a44');
          this.hecha();
        });
      }
      x += t.width + 12;
    }
  }

  // ------------------------------------------------------------------ fase 2
  private pagina(i: number) {
    const { width } = this.scale;
    this.consigna.setText(`Libro de Registro de impactos · página ${i + 1}/${PAGINAS.length}`);
    this.capa.add(this.add.rectangle(width / 2, 280, 640, 380, 0xe2d9bf).setStrokeStyle(2, 0x6a5c44));
    const cabecera = this.add.text(width / 2, 130, 'IMPACTOS EUROASIÁTICOS', { fontFamily: FUENTE.maquina, fontSize: '36px', color: '#2a2218' })
      .setOrigin(0.5).setInteractive({ useHandCursor: true });
    this.capa.add(cabecera);
    PAGINAS[i].forEach((l, k) => this.capa.add(this.add.text(220, 210 + k * 44, l, { fontFamily: FUENTE.maquina, fontSize: '26px', color: '#2a2218' })));
    this.pendientes = 1;
    cabecera.once('pointerup', () => {
      audio.play('plumilla');
      const raya = this.add.rectangle(cabecera.x - cabecera.width / 2, cabecera.y, cabecera.width, 3, 0x22252a).setOrigin(0, 0.5).setScale(0, 1);
      this.capa.add(raya);
      this.tweens.add({ targets: raya, scaleX: 1, duration: 260 });
      this.capa.add(this.add.text(width / 2, cabecera.y + 30, 'estasiáticos', { fontFamily: FUENTE.texto, fontSize: '26px', color: '#1d2a44' }).setOrigin(0.5).setAngle(-3));
      this.hecha();
    });
  }

  update(_t: number, dt: number) {
    if (this.hecho) return;
    this.restante -= dt / 1000;
    const m = Math.floor(Math.max(0, this.restante) / 60), s = Math.floor(Math.max(0, this.restante) % 60);
    this.reloj.setText(`${m}:${String(s).padStart(2, '0')}`).setColor(hex(this.restante < 20 ? COLOR.rojo4 : COLOR.papel4));
    if (this.restante <= 0) this.acabar('incompleta');
  }

  private acabar(resultado: string) {
    if (this.hecho) return;
    this.hecho = true;
    this.consigna.setText(resultado === 'completa' ? 'Corregido.' : 'Se acaba el tiempo.');
    this.time.delayedCall(900, () => this.terminar({ resultado }));
  }
}
