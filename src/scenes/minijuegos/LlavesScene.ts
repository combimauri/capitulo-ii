/**
 * El panel de llaves de la garita (guion J8.04): doce llaves con su etiqueta. Coger otra cuesta diez segundos.
 * El reloj de la misión sigue corriendo mientras se busca.
 *   # minijuego:llaves,vars=llaves_j8   → llaves_j8_fallos; resultado "ok" | "tiempo"
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { mision, hora } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const CORRECTA = 'A.R. – 1';
const ETIQUETAS = ['GAR. 2', 'A.R. – 7', 'ESC. S', 'R.A. – 1', 'CALD.', 'LAV. 11', CORRECTA, 'A.R. – 11', 'COR. 3', 'ARCH. 4', 'A. – 1', 'MONT.'];
const PENALIZACION = 10;

export class LlavesScene extends Minijuego {
  private fallos = 0;
  private reloj!: Phaser.GameObjects.Text;
  private hecho = false;

  constructor() { super('Llaves'); }

  create() {
    const { width, height } = this.scale;
    this.fallos = 0; this.hecho = false;
    this.cameras.main.fadeIn(250, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0d0f12).setOrigin(0);
    this.add.rectangle(width / 2, 280, 700, 400, 0x5a3e24).setStrokeStyle(4, 0x2e2014);
    this.add.text(width / 2, 104, 'GARITA · PLANTA 11', { fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.papel3) }).setOrigin(0.5);
    this.reloj = this.add.text(width / 2, 20, '', { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4) }).setOrigin(0.5, 0);
    this.add.text(width / 2, height - 30, 'Archivo Restringido. Una sola llave.', {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3),
    }).setOrigin(0.5);
    ETIQUETAS.forEach((etiqueta, i) => {
      const x = 240 + (i % 4) * 160, y = 170 + Math.floor(i / 4) * 110;
      this.add.circle(x, y - 26, 5, 0x9a9a9a);
      const llave = this.add.graphics();
      llave.fillStyle(0xb8a06a).fillCircle(x, y - 8, 11).fillStyle(0x5a3e24).fillCircle(x, y - 8, 4);
      llave.fillStyle(0xb8a06a).fillRect(x - 2, y, 5, 30).fillRect(x + 3, y + 20, 6, 4).fillRect(x + 3, y + 26, 4, 4);
      const tarjeta = this.add.rectangle(x + 40, y + 10, 76, 26, 0xeeead9).setStrokeStyle(1, 0x6a5c44).setAngle(-6);
      this.add.text(x + 40, y + 10, etiqueta, { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#22252a' }).setOrigin(0.5).setAngle(-6);
      const zona = this.add.rectangle(x + 16, y + 8, 110, 80, 0, 0).setInteractive({ useHandCursor: true });
      zona.on('pointerup', () => this.coger(etiqueta, tarjeta));
    });
  }

  private coger(etiqueta: string, tarjeta: Phaser.GameObjects.Rectangle) {
    if (this.hecho) return;
    if (etiqueta === CORRECTA) {
      this.hecho = true;
      audio.play('acierto');
      tarjeta.setStrokeStyle(3, COLOR.tele5);
      this.time.delayedCall(500, () => this.terminar({ resultado: 'ok', datos: { fallos: this.fallos } }));
      return;
    }
    this.fallos++;
    if (mision.reloj) mision.reloj.transcurrido += PENALIZACION;
    audio.play('fallo');
    this.cameras.main.shake(150, 0.004);
    const t = this.add.text(tarjeta.x, tarjeta.y - 40, `No entra. −${PENALIZACION} s`, {
      fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.rojo4), backgroundColor: '#000000aa',
    }).setOrigin(0.5);
    this.tweens.add({ targets: t, alpha: 0, y: t.y - 20, delay: 700, duration: 400, onComplete: () => t.destroy() });
  }

  update(_t: number, dt: number) {
    const r = mision.reloj;
    if (!r) return this.reloj.setText('');
    if (!this.hecho) r.transcurrido += dt / 1000;
    this.reloj.setText(hora(r.inicio + r.transcurrido)).setColor(hex(r.limite - r.transcurrido < 30 ? COLOR.rojo4 : COLOR.papel4));
    if (!this.hecho && r.transcurrido >= r.limite) { this.hecho = true; this.terminar({ resultado: 'tiempo', datos: { fallos: this.fallos } }); }
  }
}
