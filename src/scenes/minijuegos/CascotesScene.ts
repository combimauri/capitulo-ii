/** P.01 — Apartar los cascotes hasta encontrar la mano de Ivy. */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

export class CascotesScene extends Minijuego {
  constructor() { super('Cascotes'); }

  create() {
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(400, 11, 12, 15);
    this.add.image(width / 2, height / 2, 'cascotes-fondo').setScale(2);
    this.add.text(width / 2, 34, 'Aparta los cascotes', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4), stroke: '#000', strokeThickness: 4,
    }).setOrigin(0.5);

    const piezas = [
      { x: 470, y: 300, r: -0.2 }, { x: 545, y: 285, r: 0.4 }, { x: 410, y: 270, r: 0.1 },
      { x: 500, y: 240, r: -0.5 }, { x: 590, y: 330, r: 0.2 }, { x: 440, y: 335, r: 0.6 },
    ];
    let quedan = piezas.length;
    piezas.forEach((p, i) => {
      const img = this.add.image(p.x, p.y, `cascote-${(i % 3) + 1}`).setScale(2).setRotation(p.r)
        .setInteractive({ useHandCursor: true, pixelPerfect: false });
      img.on('pointerdown', () => {
        img.disableInteractive();
        audio.play('grieta');
        const dx = p.x < width / 2 ? -1 : 1;
        this.tweens.add({
          targets: img, x: p.x + dx * Phaser.Math.Between(260, 380), y: p.y + Phaser.Math.Between(-80, 120),
          angle: dx * 160, alpha: 0, duration: 420, ease: 'Cubic.easeOut',
          onComplete: () => {
            img.destroy();
            if (--quedan === 0) this.time.delayedCall(900, () => this.terminar({ resultado: 'hecho' }, 600));
          },
        });
      });
    });
  }
}
