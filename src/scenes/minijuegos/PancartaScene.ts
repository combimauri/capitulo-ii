/** J2.05 (opcional) — Pintar la pancarta "¡MUERTE A EURASIA!" sin salirse de las letras. */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

/** En dos líneas, con letras grandes: con el dedo, en un móvil, también se puede pintar sin salirse. */
const LINEAS = ['¡MUERTE A', 'EURASIA!'];
// fuente 3x5 (igual que la de los carteles del arte)
const FUENTE_3X5: Record<string, string> = {
  M: '101111111101101', U: '101101101101111', E: '111100110100111', R: '110101110101101', T: '111010010010010',
  A: '010101111101101', S: '011100010001110', I: '111010010010111', '¡': '010000010010010', '!': '010010010000010', ' ': '000000000000000',
};
const CELDA = 4;            // resolución de la pintura (px)
const PIXEL = 20;           // tamaño de cada "píxel" de la letra (las mismas casillas que art/minijuegos/pancarta.py)
const ARRIBA = 108, ENTRE = 28;
const BROCHA = 16;          // radio de la pincelada (la mancha es de 16x16 en el arte)

export class PancartaScene extends Minijuego {
  private letra = new Set<number>();
  /** Un margen de 8 px alrededor de las letras: rozar el contorno con el dedo no cuenta como derrame. */
  private margen = new Set<number>();
  private pintadas = new Set<number>();
  private fuera = new Set<number>();
  private pintura!: Phaser.GameObjects.RenderTexture;   // a la resolución del arte (480x270), mostrada a 2x
  private progreso!: Phaser.GameObjects.Text;
  private acabado = false;
  private ultimo: { x: number; y: number } | null = null;

  constructor() { super('Pancarta'); }

  preload() {
    this.load.image('pancarta-fondo', 'assets/minijuegos/pancarta-fondo.png');
    this.load.image('pancarta-brocha', 'assets/minijuegos/pancarta-brocha.png');
    this.load.spritesheet('pancarta-mancha', 'assets/minijuegos/pancarta-mancha.png', { frameWidth: 16, frameHeight: 16 });
  }

  create() {
    this.letra.clear(); this.margen.clear(); this.pintadas.clear(); this.fuera.clear(); this.acabado = false;
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    // el suelo del Centro con la tela extendida y las letras ya trazadas a lápiz (en las mismas celdas que puntúan)
    this.add.image(0, 0, 'pancarta-fondo').setOrigin(0).setScale(2);
    this.add.text(width / 2, 26, 'Pinta las letras sin salirte', { fontFamily: FUENTE.texto, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    this.progreso = this.add.text(width / 2, 392, '', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel3) }).setOrigin(0.5);

    // celdas que cuentan como "dentro" (el contorno de las letras está dibujado en pancarta-fondo)
    LINEAS.forEach((linea, n) => {
      const ox = (width - (linea.length * 4 * PIXEL - PIXEL)) / 2, oy = ARRIBA + n * (5 * PIXEL + ENTRE);
      [...linea].forEach((ch, i) => {
        const bits = FUENTE_3X5[ch] ?? FUENTE_3X5[' '];
        [...bits].forEach((b, k) => {
          if (b !== '1') return;
          const x = ox + i * 4 * PIXEL + (k % 3) * PIXEL, y = oy + Math.floor(k / 3) * PIXEL;
          for (let cy = y; cy < y + PIXEL; cy += CELDA) for (let cx = x; cx < x + PIXEL; cx += CELDA) this.letra.add(this.celda(cx, cy));
        });
      });
    });
    for (const c of this.letra) {
      for (let dy = -2; dy <= 2; dy++) for (let dx = -2; dx <= 2; dx++) if (!this.letra.has(c + dy * 10000 + dx)) this.margen.add(c + dy * 10000 + dx);
    }
    this.pintura = this.add.renderTexture(0, 0, width / 2, height / 2).setOrigin(0).setScale(2);
    // la brocha sigue al puntero (la punta, abajo a la izquierda, es donde pinta)
    const brocha = this.add.image(-100, -100, 'pancarta-brocha').setOrigin(1 / 20, 19 / 20).setScale(2).setDepth(5);
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => brocha.setPosition(p.x, p.y));

    // el trazo se interpola entre puntos para que un gesto rápido no deje huecos
    const pintar = (p: Phaser.Input.Pointer) => {
      if (!p.isDown || this.acabado) return;
      const desde = this.ultimo ?? { x: p.x, y: p.y };
      const pasos = Math.max(1, Math.ceil(Phaser.Math.Distance.Between(desde.x, desde.y, p.x, p.y) / CELDA));
      for (let i = 1; i <= pasos; i++) this.pintar(desde.x + ((p.x - desde.x) * i) / pasos, desde.y + ((p.y - desde.y) * i) / pasos);
      this.pintura.render();
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
    return Math.floor(y / CELDA) * 10000 + Math.floor(x / CELDA);
  }

  private pintar(x: number, y: number) {
    // una pincelada de 16x16 px de arte (= radio BROCHA en el juego), alineada a la rejilla del arte
    this.pintura.stamp('pancarta-mancha', Phaser.Math.Between(0, 2), Math.round(x / 2) - 8, Math.round(y / 2) - 8, { originX: 0, originY: 0 });
    for (let dy = -BROCHA; dy <= BROCHA; dy += CELDA) {
      for (let dx = -BROCHA; dx <= BROCHA; dx += CELDA) {
        if (dx * dx + dy * dy > BROCHA * BROCHA) continue;
        const c = this.celda(x + dx, y + dy);
        if (this.letra.has(c)) this.pintadas.add(c); else if (!this.margen.has(c)) this.fuera.add(c);
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
