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

  preload() {
    this.load.image('llaves-fondo', 'assets/minijuegos/llaves-fondo.png');
    this.load.image('llaves-etiqueta', 'assets/minijuegos/llaves-etiqueta.png');
    this.load.spritesheet('llaves-llave', 'assets/minijuegos/llaves-llave.png', { frameWidth: 16, frameHeight: 28 });
  }

  create() {
    const { width, height } = this.scale;
    this.fallos = 0; this.hecho = false;
    this.cameras.main.fadeIn(250, 11, 12, 15);
    // la garita: el tablero de llaves con su rótulo pintado («GARITA · PLANTA 11»), la telepantalla y el mostrador
    this.add.image(0, 0, 'llaves-fondo').setOrigin(0).setScale(2);
    this.reloj = this.add.text(width / 2, 20, '', { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4) }).setOrigin(0.5, 0);
    this.add.text(width / 2, height - 30, 'Archivo Restringido. Una sola llave.', {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3),
    }).setOrigin(0.5);
    ETIQUETAS.forEach((etiqueta, i) => {
      const x = 240 + (i % 4) * 160, y = 170 + Math.floor(i / 4) * 110;
      // la etiqueta de cartulina (ya inclinada en el arte), su texto y la llave colgada del gancho
      this.add.image(x + 46, y + 10, 'llaves-etiqueta').setScale(2);
      const tarjeta = this.add.rectangle(x + 46, y + 10, 92, 26, 0, 0).setAngle(-6);   // marco del acierto
      this.add.text(x + 48, y + 10, etiqueta, { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#22252a' }).setOrigin(0.5).setAngle(-6);
      this.add.image(x, y - 22, 'llaves-llave', (i + Math.floor(i / 4)) % 4).setOrigin(0.5, 0).setScale(2);
      const zona = this.add.rectangle(x + 27, y + 8, 132, 80, 0, 0).setInteractive({ useHandCursor: true });   // llave y etiqueta
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
