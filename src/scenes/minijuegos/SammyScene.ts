/**
 * D-J5-SAMMY — Secuencia contrarreloj (guion J5.04, diseño técnico §6.6).
 * Elegir en 4 segundos: correr hacia Sammy o ponerse a cubierto (si no se elige, parálisis).
 * Si corre: tres obstáculos razonables, uno tras otro. La secuencia está hecha para fallar
 * siempre, pero el jugador tiene que sentir que casi lo consigue.
 * Resultado: "correr" | "cubierto" | "paralizado".
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { texturaProta } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const ELEGIR_MS = 4000;
const PISTA = { x0: 140, x1: 820, y: 470 };

export class SammyScene extends Minijuego {
  private capa!: Phaser.GameObjects.Container;
  private prota!: Phaser.GameObjects.Sprite;
  private resuelto = false;

  constructor() { super('Sammy'); }

  preload() {
    this.load.image('sammy-fondo', 'assets/minijuegos/sammy-fondo.png');
    this.load.image('sammy-nino', 'assets/minijuegos/sammy-nino.png');
  }

  create() {
    const { width, height } = this.scale;
    this.resuelto = false;
    this.cameras.main.fadeIn(150, 255, 255, 255);
    // el mercado congelado, desaturado y oscuro: el tiempo se ralentiza
    // la calle del mercado en el instante del silbido: gente pegada al suelo, Dot alzando la cabeza
    const fondo = this.add.image(width / 2, height / 2, 'sammy-fondo').setScale(2).setTint(0x8a8a8a);
    this.tweens.add({ targets: fondo, scale: fondo.scale * 1.06, duration: 9000 });
    this.add.rectangle(0, 0, width, height, 0x000000, 0.45).setOrigin(0);
    this.capa = this.add.container(0, 0).setDepth(10);

    // pista: el protagonista, Sammy agachado de espaldas en mitad de la calzada
    this.add.image(PISTA.x1, PISTA.y + 6, 'sammy-nino').setOrigin(0.5, 1).setScale(2);
    this.add.text(PISTA.x1, PISTA.y + 12, 'SAMMY', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.ocre4) }).setOrigin(0.5, 0);
    this.prota = this.add.sprite(PISTA.x0, PISTA.y + 6, texturaProta(), 10).setOrigin(0.5, 1).setScale(2);   // de perfil, a la derecha

    audio.play('silbido', 9);
    this.elegir();
  }

  private texto(y: number, s: string, size = 30, color = COLOR.papel4) {
    return this.add.text(this.scale.width / 2, y, s, {
      fontFamily: FUENTE.maquina, fontSize: `${size}px`, color: hex(color), align: 'center', wordWrap: { width: 820 },
    }).setOrigin(0.5);
  }

  private boton(x: number, y: number, w: number, s: string, alPulsar: () => void) {
    const fondo = this.add.rectangle(x, y, w, 64, COLOR.rojo3, 0.95).setStrokeStyle(3, 0x000000).setInteractive({ useHandCursor: true });
    const t = this.add.text(x, y, s, { fontFamily: FUENTE.maquina, fontSize: '28px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    fondo.on('pointerdown', alPulsar);
    this.capa.add([fondo, t]);
    return fondo;
  }

  private limpiar() {
    this.capa.removeAll(true);
    this.input.keyboard?.removeAllListeners();
  }

  /** Dos opciones grandes y una barra que se vacía. */
  private elegir() {
    this.capa.add(this.texto(110, 'Sammy.', 44));
    const barra = this.add.rectangle(this.scale.width / 2 - 300, 170, 600, 8, COLOR.papel4).setOrigin(0, 0.5);
    this.capa.add(barra);
    this.tweens.add({ targets: barra, scaleX: 0, duration: ELEGIR_MS });
    const decidir = (d: 'correr' | 'cubierto' | 'paralizado') => {
      if (this.resuelto) return;
      this.resuelto = true;
      this.limpiar();
      if (d === 'correr') this.carrera(); else this.cubrirse(d);
    };
    this.boton(290, 280, 340, 'CORRER HACIA SAMMY', () => decidir('correr'));
    this.boton(670, 280, 340, 'PONERSE A CUBIERTO', () => decidir('cubierto'));
    this.input.keyboard?.on('keydown', (e: KeyboardEvent) => {
      if (e.key === '1' || e.code === 'ArrowLeft') decidir('correr');
      if (e.key === '2' || e.code === 'ArrowRight') decidir('cubierto');
    });
    this.time.delayedCall(ELEGIR_MS, () => decidir('paralizado'));
  }

  private cubrirse(d: 'cubierto' | 'paralizado') {
    this.capa.add(this.texto(200, d === 'cubierto'
      ? 'Te tiras detrás de un puesto de patatas.\nEntre las cajas ves a Sammy, todavía agachado.\nDot se levanta y echa a correr hacia él.'
      : 'No te mueves.\nSammy sigue agachado, de espaldas.', 26));
    this.time.delayedCall(2600, () => this.impacto(d));
  }

  /** Avanza hacia Sammy (0..1); nunca llega a 1. */
  private mover(hasta: number) {
    this.prota.play({ key: `${this.prota.texture.key}-derecha-andar`, frameRate: 14 }, true);
    this.tweens.add({
      targets: this.prota, x: PISTA.x0 + (PISTA.x1 - PISTA.x0) * hasta, duration: 500, ease: 'Sine.easeOut',
      onComplete: () => this.prota.stop().setFrame(10),
    });
  }

  /** Los obstáculos: cada uno razonable; el conjunto, imposible. */
  private async carrera() {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    this.mover(0.15);

    // 1. Un tenderete se derrumba: rodearlo por la izquierda
    await this.obstaculo('Un tenderete se derrumba delante.', [['← RODEAR', 'ArrowLeft']], 1600);
    this.mover(0.4);

    // 2. Una mujer cae con un niño en brazos: ayudarla o saltar (las dos cuestan tiempo)
    const r = await this.obstaculo('Una mujer cae con un niño en brazos.', [['AYUDARLA', 'Digit1'], ['SALTAR', 'Digit2']], 2200);
    this.mover(r === 'SALTAR' ? 0.62 : 0.56);
    if (r === 'AYUDARLA') await espera(500);

    // 3. Un patrullero le agarra del brazo: soltarse a fuerza de tirones
    await this.forcejeo();
    this.mover(0.93);
    this.capa.add(this.texto(200, 'Estiras el brazo.\nTus dedos rozan su camisa.', 30));
    await espera(1300);
    this.impacto('correr');
  }

  private obstaculo(titulo: string, opciones: [string, string][], ms: number): Promise<string> {
    return new Promise((ok) => {
      this.limpiar();
      this.capa.add(this.texto(150, titulo, 32));
      let hecho = false;
      const fin = (o: string) => { if (hecho) return; hecho = true; audio.play(o === 'tarde' ? 'fallo' : 'tecla'); ok(o); };
      opciones.forEach(([s, tecla], i) => {
        this.boton(this.scale.width / 2 + (i - (opciones.length - 1) / 2) * 340, 280, 300, s, () => fin(s));
        this.input.keyboard?.on(`keydown-${tecla === 'ArrowLeft' ? 'LEFT' : tecla === 'Digit1' ? 'ONE' : 'TWO'}`, () => fin(s));
      });
      this.time.delayedCall(ms, () => fin('tarde'));
    });
  }

  private forcejeo(): Promise<void> {
    return new Promise((ok) => {
      this.limpiar();
      this.capa.add(this.texto(130, '¡Identifíquese, camarada! ¡Al suelo!', 34, COLOR.rojo4));
      this.capa.add(this.texto(180, 'Un patrullero te agarra del brazo.', 24));
      const necesarios = 10;
      let tirones = 0;
      const barra = this.add.rectangle(this.scale.width / 2 - 200, 360, 0, 14, COLOR.papel4).setOrigin(0, 0.5);
      this.capa.add([this.add.rectangle(this.scale.width / 2, 360, 404, 18).setStrokeStyle(2, COLOR.papel3), barra]);
      const tirar = () => {
        tirones++;
        audio.play('tecla');
        barra.width = 400 * Math.min(1, tirones / necesarios);
        this.cameras.main.shake(60, 0.004);
        if (tirones >= necesarios) { this.limpiar(); ok(); }
      };
      this.boton(this.scale.width / 2, 270, 360, '¡SOLTARSE!', tirar);
      this.input.keyboard?.on('keydown-SPACE', tirar);
      this.input.keyboard?.on('keydown-ENTER', tirar);
    });
  }

  private impacto(resultado: 'correr' | 'cubierto' | 'paralizado') {
    this.limpiar();
    audio.play('impacto');
    audio.play('pitido', 4);
    this.cameras.main.flash(1200, 255, 255, 255);
    this.add.rectangle(0, 0, this.scale.width, this.scale.height, 0xffffff).setOrigin(0).setDepth(20);
    this.time.delayedCall(1600, () => this.terminar({ resultado }, 900));
  }
}
