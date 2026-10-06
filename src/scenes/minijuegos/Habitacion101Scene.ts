/**
 * Habitación 101 (guion FC.04 / FD.05): los cascotes llenan la pantalla desde abajo, el silbido del cohete
 * sube sin parar y el polvo tapa la boca (hay que toser para respirar). Sobre los escombros flotan las
 * opciones, todas traiciones. Si no se elige, los cascotes tapan la cara y la de Ivy se elige sola.
 *   # minijuego:h101,resultado=traicion_101   (opciones según el estado; sin=dot quita una)
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';
import { narrativa } from '../../core/juego';

const DURACION = 24000;
const TEXTOS: Record<string, string> = {
  nell: '«¡Háganselo a Nell! ¡A Nell! ¡Ella me buscó!»',
  dot: '«¡Dot! ¡La del mercado! ¡Ella escondió…!»',
  brooke: '«¡Brooke! ¡En el Minipax! ¡Es hermana de…!»',
  len: '«¡Len Pike! ¡Está vivo! ¡Yo le cambié el nombre!»',
  ivy: '«¡Ivy era una traidora! ¡Merecía morir! ¡El cohete fue justicia!»',
};

interface Opcion { id: string; c: Phaser.GameObjects.Container; vx: number; vy: number }

export class Habitacion101Scene extends Minijuego {
  private inicio = 0;
  private aire = 1;
  private hecho = false;
  private opciones: Opcion[] = [];
  private cascotes!: Phaser.GameObjects.Graphics;
  private nivel = 0;
  private velo!: Phaser.GameObjects.Rectangle;
  private medidor!: Phaser.GameObjects.Rectangle;

  constructor() { super('Habitacion101'); }

  create() {
    const { width, height } = this.scale;
    this.inicio = -1; this.aire = 1; this.hecho = false; this.opciones = []; this.nivel = 0;
    this.cameras.main.fadeIn(600, 0, 0, 0);
    if (this.textures.exists('vineta-habitacion101')) this.add.image(0, 0, 'vineta-habitacion101').setOrigin(0).setScale(2);
    else this.add.rectangle(0, 0, width, height, 0x3a3a38).setOrigin(0);
    this.cascotes = this.add.graphics().setDepth(5);
    this.velo = this.add.rectangle(0, 0, width, height, 0x000000, 0).setOrigin(0).setDepth(8);
    // el aire: hay que toser
    this.add.rectangle(30, 30, 200, 14, 0x000000, 0.6).setOrigin(0).setDepth(9);
    this.medidor = this.add.rectangle(32, 32, 196, 10, COLOR.papel3).setOrigin(0).setDepth(9);
    this.add.text(30, 50, 'ESPACIO · TOSER', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.papel4) }).setDepth(9);
    const toser = this.add.rectangle(width - 110, height - 44, 180, 46, COLOR.gris2, 0.9).setStrokeStyle(2, COLOR.gris3).setDepth(9).setInteractive({ useHandCursor: true });
    this.add.text(width - 110, height - 44, 'TOSER', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5).setDepth(9);
    toser.on('pointerdown', () => this.toser());
    this.input.keyboard?.on('keydown-SPACE', () => this.toser());

    // todas son traiciones: solo las que el protagonista puede pronunciar (y no la ya hecha)
    const v = (n: string) => narrativa.get(n);
    const posibles = this.params.opciones ? this.params.opciones.split('/')
      : ['nell', ...(Number(v('dot_confianza')) >= 1 ? ['dot'] : []), ...(v('brooke_revelada') ? ['brooke'] : []), ...(v('len_salvado') ? ['len'] : []), 'ivy'];
    const ids = posibles.filter((i) => TEXTOS[i] && i !== this.params.sin);
    ids.forEach((id, i) => {
      const t = this.add.text(0, 0, TEXTOS[id], { fontFamily: FUENTE.texto, fontSize: '20px', color: '#ffffff', stroke: '#000', strokeThickness: 4, wordWrap: { width: 250 }, align: 'center' }).setOrigin(0.5);
      const f = this.add.rectangle(0, 0, t.width + 24, t.height + 14, 0x1d1f22, 0.75).setStrokeStyle(2, COLOR.rojo3);
      const c = this.add.container(240 + (i % 2) * 480 + (i % 4 >= 2 ? 120 : 0), 120 + Math.floor(i / 2) * 105, [f, t]).setDepth(7).setSize(t.width + 24, t.height + 14)
        .setInteractive({ useHandCursor: true });
      c.on('pointerup', () => this.traicionar(id));
      this.opciones.push({ id, c, vx: Phaser.Math.FloatBetween(-18, 18), vy: Phaser.Math.FloatBetween(-10, 10) });
    });
    audio.play('silbido', DURACION / 1000);
  }

  private toser() {
    if (this.hecho) return;
    this.aire = Math.min(1, this.aire + 0.2);
    audio.play('tos');
    this.cameras.main.shake(80, 0.003);
  }

  private traicionar(id: string) {
    if (this.hecho) return;
    this.hecho = true;
    this.opciones.forEach((o) => { if (o.id !== id) o.c.setVisible(false); });
    const elegida = this.opciones.find((o) => o.id === id)?.c;
    if (elegida) this.tweens.add({ targets: elegida, x: 480, y: 220, scale: 1.3, duration: 400 });
    // silencio absoluto
    audio.cortar();
    this.time.delayedCall(1800, () => this.terminar({ resultado: id }, 1200));
  }

  /** Las traiciones chocan entre sí en lugar de taparse: todas tienen que poder leerse. */
  private separar() {
    for (let i = 0; i < this.opciones.length; i++) {
      for (let j = i + 1; j < this.opciones.length; j++) {
        const a = this.opciones[i], b = this.opciones[j];
        const dx = b.c.x - a.c.x, dy = b.c.y - a.c.y;
        const sx = (a.c.width + b.c.width) / 2 + 6 - Math.abs(dx);
        const sy = (a.c.height + b.c.height) / 2 + 6 - Math.abs(dy);
        if (sx <= 0 || sy <= 0) continue;
        if (sx < sy) {
          const m = (sx / 2) * Math.sign(dx || 1);
          a.c.x -= m; b.c.x += m;
          [a.vx, b.vx] = [b.vx, a.vx];
        } else {
          const m = (sy / 2) * Math.sign(dy || 1);
          a.c.y -= m; b.c.y += m;
          [a.vy, b.vy] = [b.vy, a.vy];
        }
      }
    }
  }

  update(_t: number, dt: number) {
    if (this.hecho) return;
    if (this.inicio < 0) this.inicio = this.time.now;
    const t = Math.min(1, (this.time.now - this.inicio) / DURACION);
    const s = dt / 1000;
    this.aire = Math.max(0, this.aire - s * 0.14);
    this.medidor.setSize(196 * this.aire, 10).setFillStyle(this.aire < 0.3 ? COLOR.rojo4 : COLOR.papel3);
    // los escombros suben; sin aire, la vista se estrecha
    const altura = 540 * (0.08 + t * 0.92);
    if (altura > this.nivel + 6) {
      this.nivel = altura;
      for (let k = 0; k < 14; k++) {
        const x = Phaser.Math.Between(0, 960), y = 540 - Phaser.Math.Between(0, Math.round(altura));
        const tono = Phaser.Math.RND.pick([0x6a5a48, 0x8a7a64, 0x4a4038, 0x9a6a52, 0x5a5048]);
        this.cascotes.fillStyle(tono, 1).fillRect(x, y, Phaser.Math.Between(6, 26), Phaser.Math.Between(4, 14));
      }
      this.cascotes.fillStyle(0x4a4038, 1).fillRect(0, 540 - altura * 0.7, 960, altura * 0.7);
    }
    this.velo.setAlpha(Math.max(t * 0.5, (1 - this.aire) * 0.7));
    for (const o of this.opciones) {
      o.c.x = Phaser.Math.Clamp(o.c.x + o.vx * s, 140, 820);
      o.c.y = Phaser.Math.Clamp(o.c.y + o.vy * s, 90, Math.max(100, 540 - altura - 30));
      if (o.c.x <= 140 || o.c.x >= 820) o.vx *= -1;
      if (o.c.y <= 90) o.vy = Math.abs(o.vy);
    }
    this.separar();
    // no se puede no traicionar: justo antes del impacto, Ivy se elige sola
    if (t >= 1) {
      this.velo.setAlpha(1);
      this.traicionar('ivy');
    }
  }
}
