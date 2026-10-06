/**
 * La lista de prisioneros (guion D-J11-LEN): la funcionaria se gira para atender el teléfono.
 * Diez segundos con la lista en las manos y una máquina de escribir al lado.
 *   Tachar «PIKE, L.» y escribir a máquina un nombre de la lista de reserva → "cambio" (datos: sustituto, chico)
 *   No tocar nada (o dejar pasar el tiempo) → "nada" · Tachar sin sustituir → "tachado" · Romperla → "rabia"
 *   # minijuego:lista,resultado=len_decision,vars=len
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const PRESOS = [
  { nombre: 'CHEN, W.', nota: '(captur. frente Manchuria)', foto: 0 },
  { nombre: 'KOVAL, D.', nota: '(captur. frente Manchuria)', foto: 1 },
  { nombre: 'PIKE, L.', nota: '(captur. frente Manchuria)', foto: 2 },
  { nombre: 'HOGAN, T.', nota: '(captur. frente Indonesia)', foto: 3 },
];
const RESERVA = [
  { nombre: 'MARSH, J.', foto: 4 }, { nombre: 'DOYLE, P.', foto: 5 }, { nombre: 'QUILL, R.', foto: 6 },
  { nombre: 'ASH, T.', foto: 7, chico: true }, { nombre: 'FENN, B.', foto: 8 },
];

export class ListaScene extends Minijuego {
  private restante = 10;
  private corriendo = false;
  private tachado = false;
  private hecho = false;
  private reloj!: Phaser.GameObjects.Text;
  private ayuda!: Phaser.GameObjects.Text;
  private renglonPike!: Phaser.GameObjects.Text;
  private reserva: Phaser.GameObjects.Rectangle[] = [];

  constructor() { super('Lista'); }

  create() {
    const { width, height } = this.scale;
    this.restante = Number(this.params.segundos) || 10;
    this.corriendo = false; this.tachado = false; this.hecho = false; this.reserva = [];
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0xf4f4f0).setOrigin(0);    // el Minimor: todo blanco
    this.add.rectangle(30, 40, 520, 420, 0xffffff).setOrigin(0).setStrokeStyle(1, 0xb0b0b0);
    this.add.text(46, 54, 'PRISIONEROS ESTASIÁTICOS · EJECUCIÓN PÚBLICA', { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#22252a' });
    this.add.text(46, 76, 'PARQUE DE LA VICTORIA', { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#22252a' });
    PRESOS.forEach((p, i) => {
      const y = 120 + i * 82;
      if (this.textures.exists('fichas-presos')) this.add.image(70, y + 26, 'fichas-presos', p.foto).setScale(2);
      const t = this.add.text(110, y + 6, `${i + 1}. ${p.nombre}`, { fontFamily: FUENTE.maquina, fontSize: '28px', color: '#22252a' });
      this.add.text(110, y + 38, p.nota, { fontFamily: FUENTE.maquina, fontSize: '18px', color: '#5a5a5a' });
      if (p.nombre.startsWith('PIKE')) {
        this.renglonPike = t;
        t.setInteractive({ useHandCursor: true }).on('pointerup', () => this.tachar());
      }
    });
    // la lista de reserva
    this.add.rectangle(580, 40, 350, 420, 0xffffff).setOrigin(0).setStrokeStyle(1, 0xb0b0b0);
    this.add.text(596, 54, 'LISTA DE RESERVA', { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#22252a' });
    RESERVA.forEach((r, i) => {
      const y = 92 + i * 72;
      const fondo = this.add.rectangle(590, y, 330, 66, 0xffffff).setOrigin(0).setStrokeStyle(1, 0xd0d0d0);
      if (this.textures.exists('fichas-presos')) this.add.image(624, y + 33, 'fichas-presos', r.foto).setScale(2);
      this.add.text(664, y + 20, r.nombre, { fontFamily: FUENTE.maquina, fontSize: '26px', color: '#22252a' });
      fondo.on('pointerup', () => this.sustituir(r));
      this.reserva.push(fondo);
    });
    this.reloj = this.add.text(width - 20, 6, '', { fontFamily: FUENTE.maquina, fontSize: '30px', color: '#22252a' }).setOrigin(1, 0);
    this.ayuda = this.add.text(30, height - 66, 'La funcionaria se gira para atender el teléfono.', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: '#22252a', wordWrap: { width: 560 },
    });
    this.boton(width - 290, height - 40, 'NO TOCAR NADA', () => this.acabar(this.tachado ? 'tachado' : 'nada'));
    this.boton(width - 100, height - 40, 'ROMPERLA', () => this.romper());
    this.time.delayedCall(1600, () => {
      this.corriendo = true;
      this.ayuda.setText('Tacha a Pike, L. Otro ocupará su lugar.');
    });
  }

  private boton(x: number, y: number, texto: string, alPulsar: () => void) {
    const f = this.add.rectangle(x, y, 176, 40, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(x, y, texto, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    f.on('pointerup', alPulsar);
  }

  private tachar() {
    if (!this.corriendo || this.tachado || this.hecho) return;
    this.tachado = true;
    const t = this.renglonPike;
    const raya = this.add.rectangle(t.x - 2, t.y + t.height / 2, t.width + 4, 3, 0x22252a).setOrigin(0, 0.5).setScale(0, 1);
    this.tweens.add({ targets: raya, scaleX: 1, duration: 250 });
    audio.play('plumilla');
    this.ayuda.setText('Ahora, un nombre de la reserva. A máquina.');
    this.reserva.forEach((r) => r.setInteractive({ useHandCursor: true }).setStrokeStyle(2, COLOR.rojo3));
  }

  private sustituir(r: { nombre: string; chico?: boolean }) {
    if (!this.tachado || this.hecho) return;
    this.hecho = true;
    const t = this.renglonPike;
    const nuevo = this.add.text(t.x + t.width + 18, t.y, '', { fontFamily: FUENTE.maquina, fontSize: '28px', color: '#1d2a44' });
    let i = 0;
    this.time.addEvent({
      delay: 90, repeat: r.nombre.length - 1, callback: () => {
        i++; nuevo.setText(r.nombre.slice(0, i)); audio.play('tecla');
        if (i >= r.nombre.length) this.time.delayedCall(700, () => this.terminar({ resultado: 'cambio', datos: { sustituto: r.nombre, chico: !!r.chico } }));
      },
    });
  }

  private romper() {
    if (this.hecho) return;
    this.hecho = true;
    audio.play('papel');
    this.cameras.main.shake(250, 0.01);
    const g = this.add.graphics().lineStyle(6, 0x22252a, 1);
    g.lineBetween(290, 40, 260, 250).lineBetween(260, 250, 300, 460);
    this.time.delayedCall(700, () => this.terminar({ resultado: 'rabia' }));
  }

  private acabar(resultado: string) {
    if (this.hecho) return;
    this.hecho = true;
    this.time.delayedCall(300, () => this.terminar({ resultado }));
  }

  update(_t: number, dt: number) {
    if (!this.corriendo || this.hecho) return;
    this.restante -= dt / 1000;
    this.reloj.setText(`${Math.max(0, Math.ceil(this.restante))}`).setColor(this.restante < 4 ? hex(COLOR.rojo4) : '#22252a');
    if (this.restante <= 0) {
      this.ayuda.setText('La funcionaria cuelga el teléfono.');
      this.acabar(this.tachado ? 'tachado' : 'nada');
    }
  }
}
