/** J2.05 (opcional) — Pintar la pancarta "¡MUERTE A EURASIA!" sin salirse de las letras. */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const LEMA = '¡MUERTE A EURASIA!';
// fuente 3x5 (igual que la de los carteles del arte)
const FUENTE_3X5: Record<string, string> = {
  M: '101111111101101', U: '101101101101111', E: '111100110100111', R: '110101110101101', T: '111010010010010',
  A: '010101111101101', S: '011100010001110', I: '111010010010111', '¡': '010000010010010', '!': '010010010000010', ' ': '000000000000000',
};
const CELDA = 4;            // resolución de la pintura (px)
const PIXEL = 8;            // tamaño de cada "píxel" de la letra
const BROCHA = 11;

export class PancartaScene extends Minijuego {
  private letra = new Set<number>();
  private pintadas = new Set<number>();
  private fuera = new Set<number>();
  private pintura!: Phaser.GameObjects.Graphics;
  private origen = { x: 0, y: 0 };
  private progreso!: Phaser.GameObjects.Text;
  private acabado = false;
  private ultimo: { x: number; y: number } | null = null;

  constructor() { super('Pancarta'); }

  create() {
    this.letra.clear(); this.pintadas.clear(); this.fuera.clear(); this.acabado = false;
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(width / 2, height / 2, width, height, 0x2e221b);
    const anchoLema = LEMA.length * 4 * PIXEL;
    this.origen = { x: Math.round((width - anchoLema) / 2), y: 200 };
    this.add.rectangle(width / 2, 240, anchoLema + 60, 120, 0xd8d2bd).setStrokeStyle(3, 0x8f8a7a);
    this.add.text(width / 2, 60, 'Pinta las letras sin salirte', { fontFamily: FUENTE.texto, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    this.progreso = this.add.text(width / 2, 380, '', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel3) }).setOrigin(0.5);

    // contorno de las letras y celdas que cuentan como "dentro"
    const g = this.add.graphics().lineStyle(1, 0x8f8a7a, 1);
    [...LEMA].forEach((ch, i) => {
      const bits = FUENTE_3X5[ch] ?? FUENTE_3X5[' '];
      [...bits].forEach((b, k) => {
        if (b !== '1') return;
        const x = this.origen.x + i * 4 * PIXEL + (k % 3) * PIXEL, y = this.origen.y + Math.floor(k / 3) * PIXEL;
        g.fillStyle(0xc1b89e, 1).fillRect(x, y, PIXEL, PIXEL);
        g.strokeRect(x, y, PIXEL, PIXEL);
        for (let cy = y; cy < y + PIXEL; cy += CELDA) for (let cx = x; cx < x + PIXEL; cx += CELDA) this.letra.add(this.celda(cx, cy));
      });
    });
    this.pintura = this.add.graphics();

    // el trazo se interpola entre puntos para que un gesto rápido no deje huecos
    const pintar = (p: Phaser.Input.Pointer) => {
      if (!p.isDown || this.acabado) return;
      const desde = this.ultimo ?? { x: p.x, y: p.y };
      const pasos = Math.max(1, Math.ceil(Phaser.Math.Distance.Between(desde.x, desde.y, p.x, p.y) / CELDA));
      for (let i = 1; i <= pasos; i++) this.pintar(desde.x + ((p.x - desde.x) * i) / pasos, desde.y + ((p.y - desde.y) * i) / pasos);
      this.ultimo = { x: p.x, y: p.y };
    };
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { this.ultimo = null; pintar(p); });
    this.input.on('pointermove', pintar);
    this.input.on('pointerup', () => { this.ultimo = null; });

    const boton = this.add.rectangle(width / 2, 450, 220, 44, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(width / 2, 450, 'TERMINAR', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    boton.on('pointerup', () => this.acabar());
    this.actualizar();
  }

  private celda(x: number, y: number) {
    return Math.floor((y - this.origen.y + 40) / CELDA) * 10000 + Math.floor((x - this.origen.x + 20) / CELDA);
  }

  private pintar(x: number, y: number) {
    this.pintura.fillStyle(COLOR.rojo3, 1).fillCircle(x, y, BROCHA);
    for (let dy = -BROCHA; dy <= BROCHA; dy += CELDA) {
      for (let dx = -BROCHA; dx <= BROCHA; dx += CELDA) {
        if (dx * dx + dy * dy > BROCHA * BROCHA) continue;
        const c = this.celda(x + dx, y + dy);
        if (this.letra.has(c)) this.pintadas.add(c); else this.fuera.add(c);
      }
    }
    this.actualizar();
  }

  private actualizar() {
    const cobertura = this.pintadas.size / this.letra.size;
    this.progreso.setText(`Pintado: ${Math.round(cobertura * 100)} %`);
  }

  private acabar() {
    if (this.acabado) return;
    this.acabado = true;
    const cobertura = this.pintadas.size / this.letra.size;
    const derrame = this.fuera.size / Math.max(1, this.pintadas.size);
    const bien = cobertura >= 0.75 && derrame <= 0.6;
    this.time.delayedCall(300, () => this.terminar({ resultado: bien ? 'bien' : 'mal', datos: { cobertura: Math.round(cobertura * 100) } }));
  }
}
