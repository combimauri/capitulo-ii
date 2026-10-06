/**
 * Crimen facial automático (guion J13: CF-J13-GOLDSTEIN · CF[Odio, automático]). El jugador NO controla nada:
 * la cara se crispa sola durante dos segundos, la pista acierta las marcas por su cuenta y suena, deformado,
 * un eco de los Dos Minutos de Odio. Luego la cara se relaja. Cinco años de entrenamiento.
 *   # minijuego:cf_auto,expr=odio
 */
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const DURACION = 2000;
const GOLPES = 5;
const PISTA = { y: 460, xGolpe: 200 };

export class CFAutomaticoScene extends Minijuego {
  constructor() { super('CFAutomatico'); }

  create() {
    const { width, height } = this.scale;
    const g = narrativa.get('genero') === 'f' ? 'm' : 'h';
    const expr = this.params.expr ?? 'odio';
    this.cameras.main.fadeIn(200, 11, 12, 15);
    this.add.rectangle(width / 2, height / 2, width, height, COLOR.tele0);
    for (let y = 0; y < height; y += 3) this.add.rectangle(width / 2, y, width, 1, 0x000000, 0.25);
    this.add.text(width / 2, 30, `CRIMEN FACIAL · ${expr.toUpperCase()} · AUTOMÁTICO`, {
      fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.rojo4),
    }).setOrigin(0.5);
    this.add.rectangle(width / 2, 214, 300, 300, COLOR.tele1).setStrokeStyle(3, COLOR.tele4);
    const retrato = this.add.image(width / 2, 214, `retrato-prot_${g}_neutral`).setScale(3);
    this.add.rectangle(width / 2, PISTA.y, width - 80, 54, 0x000000, 0.45).setStrokeStyle(1, COLOR.tele1);
    const aro = this.add.circle(PISTA.xGolpe, PISTA.y, 26).setStrokeStyle(3, COLOR.papel4);
    const ayuda = this.add.text(width / 2, 400, 'No puedes evitarlo.', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3), stroke: '#000', strokeThickness: 4,
    }).setOrigin(0.5).setAlpha(0);

    this.time.delayedCall(250, () => {
      audio.play('eco_odio');
      retrato.setTexture(`retrato-prot_${g}_${expr}`);
      this.tweens.add({ targets: ayuda, alpha: 1, duration: 300 });
      // la cara tiembla: los músculos van solos
      this.tweens.add({ targets: retrato, x: { from: width / 2 - 3, to: width / 2 + 3 }, duration: 60, yoyo: true, repeat: Math.floor(DURACION / 120) });
      this.cameras.main.shake(DURACION, 0.002);
    });
    // las marcas llegan y se aciertan solas, una tras otra
    for (let k = 0; k < GOLPES; k++) {
      const marca = this.add.circle(width + 40, PISTA.y, 20, 0xc8382f).setStrokeStyle(2, 0x000000);
      const llega = 250 + (k + 1) * (DURACION / (GOLPES + 1));
      this.tweens.add({
        targets: marca, x: PISTA.xGolpe, duration: 900, delay: llega - 900, onComplete: () => {
          audio.play('acierto');
          aro.setStrokeStyle(5, 0xc8382f);
          this.time.delayedCall(90, () => aro.setStrokeStyle(3, COLOR.papel4));
          this.tweens.add({ targets: marca, scale: 1.6, alpha: 0, duration: 160, onComplete: () => marca.destroy() });
        },
      });
    }
    // y se relaja
    this.time.delayedCall(250 + DURACION, () => {
      retrato.setTexture(`retrato-prot_${g}_neutral`);
      this.tweens.add({ targets: ayuda, alpha: 0, duration: 400 });
    });
    this.time.delayedCall(250 + DURACION + 1100, () => this.terminar({ resultado: 'automatico' }, 500));
  }
}
