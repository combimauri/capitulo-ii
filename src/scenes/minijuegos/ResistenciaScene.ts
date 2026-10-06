/**
 * Aguantar veinticuatro horas (guion FD.04): un reloj de pared que avanza a saltos y las preguntas de O'Brien
 * sobre la segunda copia del libro. Se responde con silencio (no tocar nada) o con una mentira. Cada respuesta
 * sube el dial; la voluntad baja con cada descarga y se recupera un poco en los silencios.
 *   # minijuego:resistencia,resultado=resistencia_d   → "aguanto" | "delatado"
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const PREGUNTAS = ['¿Dónde está?', '¿Quién la tiene?', '¿La mujer del mercado?', '¿En Limehouse?', '¿En una cocina?',
  '¿Quién sabe leer allí?', '¿Dónde está la copia?', '¿La mujer del mercado?', '¿Quién la tiene?', '¿Dónde está?',
  '¿En las cosas de un niño?', '¿Dónde?'];
const MENTIRAS = ['«La quemé.»', '«La tiré al río.»', '«La tiene Goldstein.»'];
const SILENCIO = 6000;

export class ResistenciaScene extends Minijuego {
  private horas = 0;
  private voluntad = 1;
  private pregunta = 0;
  private limite = 0;
  private esperando = false;
  private hecho = false;
  private textoPregunta!: Phaser.GameObjects.Text;
  private reloj!: Phaser.GameObjects.Text;
  private esfera!: Phaser.GameObjects.Image;
  private barra!: Phaser.GameObjects.Rectangle;
  private espera!: Phaser.GameObjects.Rectangle;
  private botones: Phaser.GameObjects.GameObject[] = [];

  constructor() { super('Resistencia'); }

  preload() {
    for (const k of ['resistencia-fondo', 'resistencia-consola', 'resistencia-obrien']) this.load.image(k, `assets/minijuegos/${k}.png`);
    this.load.spritesheet('resistencia-reloj', 'assets/minijuegos/resistencia-reloj.png', { frameWidth: 72, frameHeight: 72 });
  }

  create() {
    const { width, height } = this.scale;
    this.horas = 0; this.voluntad = 1; this.pregunta = 0; this.hecho = false; this.botones = [];
    this.cameras.main.fadeIn(400, 11, 12, 15);
    // la sala blanca: azulejo, fluorescentes, O'Brien detrás de su consola
    this.add.image(0, 0, 'resistencia-fondo').setOrigin(0).setScale(2);
    this.add.image(150, 210, 'resistencia-obrien').setScale(2);
    this.add.image(16, 272, 'resistencia-consola').setOrigin(0).setScale(2);
    // el reloj de pared (la aguja de las horas salta con cada respuesta) y las horas en cifras debajo
    this.esfera = this.add.image(800, 120, 'resistencia-reloj', 0).setScale(2);
    this.reloj = this.add.text(800, 212, '', { fontFamily: FUENTE.maquina, fontSize: '30px', color: '#22252a' }).setOrigin(0.5);
    this.add.text(800, 244, 'Aguanta veinticuatro horas.', { fontFamily: FUENTE.texto, fontSize: '17px', color: '#5a5c60' }).setOrigin(0.5);
    // la voluntad
    this.add.text(300, 300, 'VOLUNTAD', { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#3a3c40' });
    this.add.rectangle(300, 330, 360, 16, 0xc8c8c4).setOrigin(0, 0.5);
    this.barra = this.add.rectangle(300, 330, 360, 16, 0x3a3c40).setOrigin(0, 0.5);
    this.textoPregunta = this.add.text(300, 170, '', { fontFamily: FUENTE.maquina, fontSize: '40px', color: '#22252a', wordWrap: { width: 380 } }).setOrigin(0, 0.5);
    this.add.rectangle(width / 2 - 300, height - 30, 600, 6, 0xc8c8c4).setOrigin(0, 0.5);
    this.espera = this.add.rectangle(width / 2 - 300, height - 30, 600, 6, 0x3a3c40).setOrigin(0, 0.5);
    this.add.text(width / 2, height - 22, '(callar: no tocar nada)', { fontFamily: FUENTE.texto, fontSize: '15px', color: '#6a6c70' }).setOrigin(0.5, 0);
    this.siguiente();
  }

  private siguiente() {
    this.botones.forEach((b) => b.destroy());
    this.botones = [];
    this.marcarHora(this.horas);
    if (this.horas >= 24) return this.acabar('aguanto');
    this.textoPregunta.setText(`O'BRIEN: ${PREGUNTAS[this.pregunta % PREGUNTAS.length]}`);
    this.pregunta++;
    MENTIRAS.forEach((m, i) => {
      const x = 200 + i * 280;
      const f = this.add.rectangle(x, 420, 250, 46, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      const t = this.add.text(x, 420, m, { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      f.on('pointerup', () => this.responder(true));
      this.botones.push(f, t);
    });
    this.limite = this.time.now + SILENCIO;
    this.esperando = true;
  }

  private responder(mentira: boolean) {
    if (!this.esperando || this.hecho) return;
    this.esperando = false;
    // la mentira compra más tiempo, pero duele más; el silencio duele menos y deja respirar
    this.voluntad -= mentira ? 0.19 : 0.12;
    this.horas += mentira ? 3 : 2;
    const k = mentira ? 0.75 : 0.5;
    audio.play('descarga', 0.6 + k);
    this.cameras.main.shake(500 + k * 600, 0.006 + k * 0.012);
    const velo = this.add.rectangle(0, 0, 960, 540, 0xffffff, 0).setOrigin(0).setDepth(20);
    this.tweens.add({
      targets: velo, alpha: 0.8, duration: 110, yoyo: true, repeat: 3, onComplete: () => {
        velo.destroy();
        if (!mentira) this.voluntad = Math.min(1, this.voluntad + 0.05);
        this.barra.setScale(Math.max(0, this.voluntad), 1);
        if (this.voluntad <= 0) return this.acabar('delatado');
        this.time.delayedCall(500, () => this.siguiente());
      },
    });
  }

  private acabar(r: string) {
    if (this.hecho) return;
    this.hecho = true;
    this.botones.forEach((b) => b.destroy());
    this.textoPregunta.setText(r === 'aguanto' ? '' : '«Dot.»');
    this.marcarHora(r === 'aguanto' ? 24 : this.horas);
    this.time.delayedCall(1800, () => this.terminar({ resultado: r }, 800));
  }

  private marcarHora(h: number) {
    this.reloj.setText(`${String(h).padStart(2, '0')}:00`);
    this.esfera.setFrame(h % 12);
  }

  update() {
    if (!this.esperando || this.hecho) return;
    const queda = Math.max(0, this.limite - this.time.now);
    this.espera.setScale(queda / SILENCIO, 1);
    if (queda === 0) this.responder(false);
  }
}
