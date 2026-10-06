/**
 * «¿Qué hora marca?» (guion FC.03c): O'Brien sostiene el reloj de Ivy delante de los ojos del protagonista.
 * Las agujas marcan las 21:40. La mano de O'Brien está en el dial. Cada ronda, tres respuestas: la verdad,
 * la mentira que cree que quiere oír, o el silencio. Ninguna es la correcta. En la quinta ronda no hay
 * opciones: las agujas tiemblan y se desplazan solas hasta las 23:15.
 *   # minijuego:dial,ronda=2,resultado=dial_respuesta   → "nueve" | "once" | "silencio" (datos: nivel)
 * Las líneas de O'Brien están en ink, entre ronda y ronda.
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const NIVELES = [40, 60, 80, 95];
const SILENCIO = 7000;
const RELOJ = { x: 480, y: 220, r: 66 };
const DIAL = { x: 812, y: 250, r: 86 };

export class DialScene extends Minijuego {
  private hora = 21 * 60 + 40;
  private agujas!: Phaser.GameObjects.Graphics;
  private aguja!: Phaser.GameObjects.Graphics;
  private nivel = 0;
  private elegido = false;
  private limite = 0;
  private barra!: Phaser.GameObjects.Rectangle;

  constructor() { super('Dial'); }

  create() {
    const { width, height } = this.scale;
    const ronda = Number(this.params.ronda) || 1;
    this.hora = 21 * 60 + 40; this.elegido = false;
    this.nivel = Number(this.params.desde) || 0;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0xf2f2ee).setOrigin(0);
    // O'Brien, a la izquierda
    const clave = ronda === 5 ? 'retrato-obrien_sonrisa' : 'retrato-obrien_neutral';
    if (this.textures.exists(clave)) this.add.image(150, 230, clave).setScale(2.4);
    this.add.text(150, 360, "O'BRIEN", { fontFamily: FUENTE.maquina, fontSize: '22px', color: '#3a3c40' }).setOrigin(0.5);
    // el reloj de Ivy
    if (this.textures.exists('reloj-ivy-grande')) this.add.image(RELOJ.x, RELOJ.y, 'reloj-ivy-grande');
    else this.add.circle(RELOJ.x, RELOJ.y, RELOJ.r, 0xeeead9).setStrokeStyle(4, 0x6a5c44);
    this.agujas = this.add.graphics();
    this.pintarAgujas(0);
    // el dial del 1 al 100
    this.aguja = this.add.graphics();
    const g = this.add.graphics();
    g.lineStyle(8, 0xc8c8c4).beginPath().arc(DIAL.x, DIAL.y, DIAL.r, Math.PI, 0).strokePath();
    for (let v = 0; v <= 100; v += 10) {
      const a = Math.PI + (v / 100) * Math.PI;
      g.lineStyle(2, v >= 80 ? COLOR.rojo4 : 0x3a3c40).lineBetween(DIAL.x + Math.cos(a) * (DIAL.r - 14), DIAL.y + Math.sin(a) * (DIAL.r - 14), DIAL.x + Math.cos(a) * DIAL.r, DIAL.y + Math.sin(a) * DIAL.r);
      this.add.text(DIAL.x + Math.cos(a) * (DIAL.r + 16), DIAL.y + Math.sin(a) * (DIAL.r + 16), String(v), { fontFamily: FUENTE.maquina, fontSize: '16px', color: '#3a3c40' }).setOrigin(0.5);
    }
    this.pintarDial();

    if (ronda >= 5) { void this.rendirse(); return; }
    this.add.text(width / 2, 352, '¿Qué hora marca este reloj?', { fontFamily: FUENTE.maquina, fontSize: '30px', color: '#22252a' }).setOrigin(0.5);
    const boton = (x: number, texto: string, r: string) => {
      const f = this.add.rectangle(x, 420, 300, 48, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      this.add.text(x, 420, texto, { fontFamily: FUENTE.texto, fontSize: '21px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      f.on('pointerup', () => this.responder(r, ronda));
    };
    boton(width / 2 - 170, '«Las nueve y cuarenta.»', 'nueve');
    boton(width / 2 + 170, '«Las once y cuarto.»', 'once');
    this.add.rectangle(width / 2 - 300, 470, 600, 6, 0xc8c8c4).setOrigin(0, 0.5);
    this.barra = this.add.rectangle(width / 2 - 300, 470, 600, 6, 0x3a3c40).setOrigin(0, 0.5);
    this.add.text(width / 2, 490, '(o no decir nada)', { fontFamily: FUENTE.texto, fontSize: '16px', color: '#6a6c70' }).setOrigin(0.5, 0);
    this.limite = this.time.now + SILENCIO;
    const kb = this.input.keyboard!;
    kb.on('keydown-ONE', () => this.responder('nueve', ronda));
    kb.on('keydown-TWO', () => this.responder('once', ronda));
  }

  private pintarAgujas(temblor: number) {
    const h = (this.hora / 60) % 12, m = this.hora % 60;
    const g = this.agujas.clear();
    const aguja = (ang: number, largo: number, grosor: number) => {
      const a = ang - Math.PI / 2 + (Math.random() - 0.5) * temblor;
      g.lineStyle(grosor, 0x1d1f22).lineBetween(RELOJ.x, RELOJ.y, RELOJ.x + Math.cos(a) * largo, RELOJ.y + Math.sin(a) * largo);
    };
    aguja((h / 12) * Math.PI * 2, RELOJ.r * 0.5, 5);
    aguja((m / 60) * Math.PI * 2, RELOJ.r * 0.78, 3);
    g.fillStyle(0x1d1f22).fillCircle(RELOJ.x, RELOJ.y, 4);
  }

  private pintarDial() {
    const a = Math.PI + (this.nivel / 100) * Math.PI;
    this.aguja.clear().lineStyle(4, COLOR.rojo4).lineBetween(DIAL.x, DIAL.y, DIAL.x + Math.cos(a) * (DIAL.r - 8), DIAL.y + Math.sin(a) * (DIAL.r - 8))
      .fillStyle(0x3a3c40).fillCircle(DIAL.x, DIAL.y, 7);
  }

  private responder(r: string, ronda: number) {
    if (this.elegido) return;
    this.elegido = true;
    const base = NIVELES[Math.min(ronda, 4) - 1];
    const nivel = r === 'silencio' ? Math.max(20, base - 20) : r === 'once' ? Math.min(100, base + 10) : base;
    this.tweens.addCounter({
      from: this.nivel, to: nivel, duration: 700, onUpdate: (tw) => { this.nivel = tw.getValue() ?? nivel; this.pintarDial(); },
      onComplete: () => this.descarga(nivel, () => this.terminar({ resultado: r, datos: { nivel } }, 300)),
    });
  }

  /** La descarga: blanco que vibra, en proporción al dial. */
  private descarga(nivel: number, despues: () => void) {
    const k = nivel / 100;
    audio.play('descarga', 0.4 + k * 1.4);
    this.cameras.main.shake(400 + k * 1200, 0.004 + k * 0.02);
    const velo = this.add.rectangle(0, 0, 960, 540, 0xffffff, 0).setOrigin(0).setDepth(20);
    this.tweens.add({ targets: velo, alpha: 0.65 + k * 0.3, duration: 120, yoyo: true, repeat: Math.round(2 + k * 4), onComplete: () => { velo.destroy(); despues(); } });
  }

  /** Quinta vez: sin opciones. Las agujas tiemblan con la estática del doblepensar y van solas hasta las 23:15. */
  private async rendirse() {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    await espera(1500);
    audio.play('pitido', 3.2);
    const destino = 23 * 60 + 15;
    for (let i = 0; i <= 60; i++) {
      this.hora = Math.round(21 * 60 + 40 + ((destino - (21 * 60 + 40)) * i) / 60);
      this.pintarAgujas(0.4 * (1 - i / 60));
      if (i % 6 === 0) this.cameras.main.shake(80, 0.003);
      await espera(50);
    }
    this.pintarAgujas(0);
    await espera(1800);
    this.terminar({ resultado: 'once', datos: { nivel: this.nivel } }, 600);
  }

  update() {
    if (this.elegido || !this.barra || !this.limite) return;
    const queda = Math.max(0, this.limite - this.time.now);
    this.barra.setScale(queda / SILENCIO, 1);
    if (queda === 0) this.responder('silencio', Number(this.params.ronda) || 1);
  }
}
