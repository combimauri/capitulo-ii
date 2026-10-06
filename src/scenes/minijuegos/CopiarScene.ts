/**
 * Copiar la Planilla Azul a mano (guion D-J8-PLANILLA): treinta segundos; cada línea tarda cinco
 * (cuatro con el lápiz de Amory, que ya conoce el camino). El jugador elige qué copiar.
 *   # minijuego:copiar,doc=planilla_s18,lapiz=si,vars=copia   → copia_lineas, copia_firma; resultado = líneas copiadas
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { lineas } from '../../core/texto';
import type { Documento } from './DocumentoScene';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const DOCS = import.meta.glob('../../../content/documentos/*.json', { eager: true, import: 'default' }) as Record<string, Documento>;
const docDe = (id: string) => Object.entries(DOCS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];
const TIEMPO = 30;

interface Fila { texto: string; t: Phaser.GameObjects.Text; barra: Phaser.GameObjects.Rectangle; hecha: boolean }

export class CopiarScene extends Minijuego {
  private filas: Fila[] = [];
  private actual: Fila | null = null;
  private progreso = 0;
  private porLinea = 5;
  private restante = TIEMPO;
  private copiadas: string[] = [];
  private cuaderno!: Phaser.GameObjects.Text;
  private reloj!: Phaser.GameObjects.Text;
  private hecho = false;

  constructor() { super('Copiar'); }

  create() {
    const { width, height } = this.scale;
    this.filas = []; this.actual = null; this.progreso = 0; this.restante = TIEMPO; this.copiadas = []; this.hecho = false;
    this.porLinea = this.params.lapiz === 'si' ? 4 : 5;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0b0c0f).setOrigin(0);
    const d = docDe(this.params.doc ?? 'planilla_s18');
    // la planilla, a la izquierda (azul pálido)
    this.add.rectangle(20, 60, 600, 440, 0xc9d6e3).setOrigin(0).setStrokeStyle(1, 0x6a7a8a);
    const copiables = [...lineas(d?.lineas).slice(1), ...lineas(d?.pie)];
    copiables.forEach((texto, i) => {
      const y = 80 + i * 34;
      const t = this.add.text(32, y, texto, { fontFamily: FUENTE.maquina, fontSize: '17px', color: '#1d2a44' });
      const barra = this.add.rectangle(32, y + 22, 0, 3, COLOR.rojo3).setOrigin(0);
      const zona = this.add.rectangle(26, y - 3, 588, 30, 0x1d2a44, 0).setOrigin(0).setInteractive({ useHandCursor: true });
      const fila: Fila = { texto, t, barra, hecha: false };
      zona.on('pointerover', () => { if (!fila.hecha) zona.setFillStyle(0x1d2a44, 0.08); });
      zona.on('pointerout', () => zona.setFillStyle(0x1d2a44, 0));
      zona.on('pointerup', () => this.empezar(fila));
      this.filas.push(fila);
    });
    // el cuaderno, a la derecha
    this.add.rectangle(636, 60, 304, 440, 0xe8e2cc).setOrigin(0).setStrokeStyle(1, 0x8f8a7a);
    for (let y = 92; y < 496; y += 24) this.add.rectangle(646, y, 284, 1, 0x9ab0c8).setOrigin(0);
    this.add.rectangle(670, 60, 1, 440, 0xc8a0a0).setOrigin(0);
    this.cuaderno = this.add.text(676, 72, '', {
      fontFamily: FUENTE.texto, fontSize: '14px', color: '#4a4a52', lineSpacing: 7, wordWrap: { width: 256 },
    });
    this.add.text(20, 18, this.params.lapiz === 'si' ? 'Copia a lápiz las líneas que quieras llevarte. (El lápiz de Amory.)' : 'Copia las líneas que quieras llevarte.', {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3),
    });
    this.reloj = this.add.text(width - 20, 14, '', { fontFamily: FUENTE.maquina, fontSize: '32px', color: hex(COLOR.papel4) }).setOrigin(1, 0);
    const f = this.add.rectangle(width - 120, height - 22, 200, 34, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(width - 120, height - 22, 'BASTA', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    f.on('pointerup', () => this.acabar());
  }

  private empezar(f: Fila) {
    if (this.hecho || f.hecha || f === this.actual) return;
    if (this.actual) this.actual.barra.setSize(0, 3);   // se pierde lo que llevaba
    this.actual = f;
    this.progreso = 0;
    audio.play('plumilla');
  }

  update(_t: number, dt: number) {
    if (this.hecho) return;
    const s = dt / 1000;
    this.restante -= s;
    this.reloj.setText(`${Math.max(0, Math.ceil(this.restante))} s`).setColor(hex(this.restante < 8 ? COLOR.rojo4 : COLOR.papel4));
    const f = this.actual;
    if (f) {
      this.progreso += s / this.porLinea;
      f.barra.setSize(f.t.width * Math.min(1, this.progreso), 3);
      // el lápiz va dejando la línea en el cuaderno
      const parcial = f.texto.slice(0, Math.floor(f.texto.length * Math.min(1, this.progreso)));
      this.cuaderno.setText([...this.copiadas, parcial].map((l) => l.replace(/\s+/g, ' ')).join('\n'));
      if (Math.random() < 0.08) audio.play('plumilla');
      if (this.progreso >= 1) {
        f.hecha = true;
        f.t.setAlpha(0.45);
        this.copiadas.push(f.texto);
        this.actual = null;
        audio.play('acierto');
      }
    }
    if (this.restante <= 0) this.acabar();
  }

  private acabar() {
    if (this.hecho) return;
    this.hecho = true;
    const firma = this.copiadas.some((l) => l.startsWith('Autoriza'));
    this.time.delayedCall(400, () => this.terminar({ resultado: String(this.copiadas.length), datos: { lineas: this.copiadas.length, firma } }));
  }
}
