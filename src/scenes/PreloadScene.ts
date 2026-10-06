import Phaser from 'phaser';
import { COLOR, FUENTE, hex } from '../ui/estilo';

export const DIRS = ['abajo', 'izquierda', 'derecha', 'arriba'] as const;

export class PreloadScene extends Phaser.Scene {
  constructor() { super('Preload'); }

  preload() {
    const { width, height } = this.scale;
    const barra = this.add.rectangle(width / 2 - 150, height / 2, 0, 6, COLOR.tele4).setOrigin(0, 0.5);
    this.add.rectangle(width / 2, height / 2, 304, 10).setStrokeStyle(1, COLOR.tele1);
    this.add.text(width / 2, height / 2 - 28, 'CARGANDO REGISTROS DEL PARTIDO…', {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.tele5),
    }).setOrigin(0.5);
    this.load.on('progress', (p: number) => barra.setSize(300 * p, 6));

    this.load.image('loc-piso', 'assets/locations/piso.png');
    this.load.spritesheet('prot', 'assets/sprites/protagonista_h.png', { frameWidth: 20, frameHeight: 40 });
  }

  create() {
    DIRS.forEach((dir, fila) => {
      this.anims.create({
        key: `prot-${dir}-andar`,
        frames: this.anims.generateFrameNumbers('prot', { start: fila * 5 + 1, end: fila * 5 + 4 }),
        frameRate: 7,
        repeat: -1,
      });
    });
    this.scene.start('Menu');
  }
}
