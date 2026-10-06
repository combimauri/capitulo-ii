/**
 * La declaración voluntaria (guion FC.04): se firma manteniendo pulsado sobre la línea, exactamente como la Ficha
 * de Afiliación del prólogo. El mismo sonido de plumilla. Después, el sello: APTO.
 *   # minijuego:declaracion,enemigo=Estasia
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const TIEMPO_FIRMA = 2200;
const LINEA = { x: 330, y: 400, w: 300 };

export class DeclaracionScene extends Minijuego {
  private firma!: Phaser.GameObjects.Graphics;
  private firmando: number | null = null;
  private firmado = false;

  constructor() { super('Declaracion'); }

  create() {
    const { width, height } = this.scale;
    this.firmando = null; this.firmado = false;
    const nombre = String(narrativa.get('nombre')), apellido = String(narrativa.get('apellido'));
    this.cameras.main.fadeIn(500, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0xf2f2ee).setOrigin(0);
    this.add.rectangle(width / 2, 260, 700, 440, 0xeeead9).setStrokeStyle(1, 0x8f8a7a);
    this.add.text(width / 2, 70, 'DECLARACIÓN VOLUNTARIA', { fontFamily: FUENTE.maquina, fontSize: '32px', color: '#22252a' }).setOrigin(0.5);
    const texto = [
      `Yo, ${nombre} ${apellido}, declaro que mi hermana, IVY ${apellido.toUpperCase()},`,
      `era una agente al servicio de ${this.params.enemigo ?? (Number(narrativa.get('jornada')) >= 10 ? 'Estasia' : 'Eurasia')}, y que el impacto`,
      'que puso fin a su vida en la calle Stepney fue un acto de justicia.',
      'Declaro que el Partido me protegió.',
      'Declaro que amo al Gran Hermano.',
    ];
    this.add.text(150, 120, texto.join('\n'), { fontFamily: FUENTE.maquina, fontSize: '24px', color: '#22252a', lineSpacing: 10 });
    this.add.rectangle(LINEA.x, LINEA.y, LINEA.w, 2, 0x22252a).setOrigin(0, 0.5);
    this.add.text(LINEA.x, LINEA.y + 8, 'Firma', { fontFamily: FUENTE.maquina, fontSize: '18px', color: '#5a5a5a' });
    this.firma = this.add.graphics();
    const ayuda = this.add.text(width / 2, height - 40, 'Mantén pulsado sobre la línea para firmar.', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.gris3),
    }).setOrigin(0.5);
    const zona = this.add.rectangle(LINEA.x - 10, LINEA.y - 40, LINEA.w + 20, 60, 0, 0).setOrigin(0).setInteractive({ useHandCursor: true });
    zona.on('pointerdown', () => this.empezar());
    this.input.on('pointerup', () => this.soltar());
    this.input.keyboard?.on('keydown-SPACE', () => this.empezar());
    this.input.keyboard?.on('keyup-SPACE', () => this.soltar());
    this.tweens.add({ targets: ayuda, alpha: 0.4, duration: 700, yoyo: true, repeat: -1 });
  }

  private empezar() { if (!this.firmado && this.firmando === null) this.firmando = this.time.now; }

  private soltar() { if (!this.firmado && this.firmando !== null) { this.firmando = null; this.firma.clear(); } }

  update() {
    if (this.firmando === null || this.firmado) return;
    const t = Math.min(1, (this.time.now - this.firmando) / TIEMPO_FIRMA);
    // el trazo de la firma, una onda que avanza
    const g = this.firma.clear().lineStyle(2, 0x1d2a44, 1);
    g.beginPath();
    for (let i = 0; i <= 60 * t; i++) {
      const x = LINEA.x + 10 + (i / 60) * (LINEA.w - 20);
      const y = LINEA.y - 14 + Math.sin(i * 0.7) * 8 + Math.sin(i * 0.23) * 5;
      if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
    g.strokePath();
    if (Math.random() < 0.3) audio.play('plumilla');
    if (t >= 1) this.sellar();
  }

  private sellar() {
    this.firmado = true;
    this.time.delayedCall(500, () => {
      audio.play('sello');
      const s = this.add.text(700, 320, 'APTO', { fontFamily: FUENTE.maquina, fontSize: '64px', color: hex(COLOR.rojo4), padding: { x: 10, y: 0 } })
        .setOrigin(0.5).setAngle(-12).setScale(2).setAlpha(0);
      this.add.rectangle(700, 320, 170, 70).setStrokeStyle(4, COLOR.rojo4, 0.8).setAngle(-12);
      this.tweens.add({ targets: s, scale: 1, alpha: 0.85, duration: 180 });
      this.cameras.main.shake(120, 0.004);
      this.time.delayedCall(1800, () => this.terminar({ resultado: 'firmada' }, 800));
    });
  }
}
