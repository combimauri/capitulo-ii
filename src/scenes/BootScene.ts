import Phaser from 'phaser';

/** Espera a que las fuentes pixel estén listas antes de dibujar texto. */
export class BootScene extends Phaser.Scene {
  constructor() { super('Boot'); }

  async create() {
    try {
      await Promise.all([
        document.fonts.load('20px "Pixelify Sans"'),
        document.fonts.load('20px "VT323"'),
      ]);
    } catch { /* si falla, se usa la fuente de respaldo */ }
    this.scene.start('Preload');
  }
}
