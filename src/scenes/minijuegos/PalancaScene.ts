/**
 * El montacargas viejo (guion J8.03): la palanca de latón se baja despacio, sin soltarla.
 * Si baja demasiado deprisa, la reja chirría (y alguien puede oírlo). Si se suelta, la palanca vuelve hacia arriba.
 *   # minijuego:palanca,resultado=montacargas_j8   → "limpio" | "chirrido"
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const RIEL = { x: 480, arriba: 140, abajo: 420 };
const LIMITE = 300;          // px/s: por encima, chirría
const MUELLE = 50;           // px/s que sube sola si se suelta
const PLANTAS = 11;
const HUECO = { x: 120, y: 76, w: 720, h: 396 };   // la abertura de la reja, en píxeles del juego
const PLANTA_ARTE = 120;                            // alto de una planta en palanca-hueco.png

export class PalancaScene extends Minijuego {
  private mango!: Phaser.GameObjects.Container;
  private hueco!: Phaser.GameObjects.TileSprite;
  private y = RIEL.arriba;
  private agarrada = false;
  private pulsadaDesde = 0;
  private chirridos = 0;
  private enfriar = 0;
  private planta!: Phaser.GameObjects.Text;
  private aviso!: Phaser.GameObjects.Text;
  private hecho = false;
  private teclas!: Phaser.Input.Keyboard.Key[];

  constructor() { super('Palanca'); }

  preload() {
    for (const k of ['palanca-fondo', 'palanca-reja', 'palanca-hueco', 'palanca-mango']) this.load.image(k, `assets/minijuegos/${k}.png`);
  }

  create() {
    const { width, height } = this.scale;
    this.y = RIEL.arriba; this.agarrada = false; this.chirridos = 0; this.enfriar = 0; this.hecho = false; this.pulsadaDesde = 0;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    // el hueco del montacargas (se desplaza al subir), la reja de tijera y la cabina con la placa de latón
    // graduada de S a 11 (arte a la mitad de resolución, mostrado a 2x)
    this.hueco = this.add.tileSprite(HUECO.x, HUECO.y, HUECO.w / 2, HUECO.h / 2, 'palanca-hueco').setOrigin(0).setScale(2);
    this.add.image(HUECO.x, HUECO.y, 'palanca-reja').setOrigin(0).setScale(2);
    this.add.image(0, 0, 'palanca-fondo').setOrigin(0).setScale(2);
    const mango = this.add.image(0, 0, 'palanca-mango').setScale(2);
    this.mango = this.add.container(RIEL.x, this.y, [mango]).setSize(110, 50).setInteractive({ useHandCursor: true, draggable: true });
    this.planta = this.add.text(width / 2, 40, '', { fontFamily: FUENTE.maquina, fontSize: '34px', color: hex(COLOR.ocre4) }).setOrigin(0.5);
    this.add.text(width / 2, height - 36, 'Baja la palanca despacio, sin soltarla. (Arrastra, o mantén S / ↓)', {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3),
    }).setOrigin(0.5);
    this.aviso = this.add.text(width / 2, 90, '', { fontFamily: FUENTE.maquina, fontSize: '40px', color: hex(COLOR.rojo4) }).setOrigin(0.5);

    let ultimo = { y: 0, t: 0 };
    this.mango.on('dragstart', (p: Phaser.Input.Pointer) => { this.agarrada = true; ultimo = { y: p.y, t: this.time.now }; });
    this.mango.on('drag', (p: Phaser.Input.Pointer, _x: number, dy: number) => {
      const nuevo = Phaser.Math.Clamp(dy, RIEL.arriba, RIEL.abajo);
      const dt = Math.max(16, this.time.now - ultimo.t);
      const vel = ((nuevo - this.y) / dt) * 1000;
      ultimo = { y: p.y, t: this.time.now };
      this.mover(nuevo, vel);
    });
    this.mango.on('dragend', () => { this.agarrada = false; });
    const kb = this.input.keyboard!;
    this.teclas = [kb.addKey('S'), kb.addKey('DOWN')];
  }

  private mover(nuevo: number, vel: number) {
    if (vel > LIMITE) this.chirriar();
    this.y = nuevo;
    this.mango.y = nuevo;
    // la cabina sube: la pared del hueco baja por detrás de la reja
    this.hueco.tilePositionY = -Math.round(((nuevo - RIEL.arriba) / (RIEL.abajo - RIEL.arriba)) * PLANTAS * PLANTA_ARTE);
  }

  private chirriar() {
    if (this.time.now < this.enfriar) return;
    this.enfriar = this.time.now + 1200;
    this.chirridos++;
    audio.play('chirrido');
    this.cameras.main.shake(300, 0.006);
    this.aviso.setText('¡CHIRRÍA!').setAlpha(1);
    this.tweens.add({ targets: this.aviso, alpha: 0, delay: 600, duration: 400 });
  }

  update(_t: number, dt: number) {
    if (this.hecho) return;
    const tecla = this.teclas.some((k) => k.isDown);
    if (tecla) {
      if (!this.pulsadaDesde) this.pulsadaDesde = this.time.now;
      // cuanto más rato se mantiene, más deprisa baja: hay que soltar y volver a coger
      const vel = 90 + (this.time.now - this.pulsadaDesde) * 0.32;
      this.mover(Math.min(RIEL.abajo, this.y + (vel * dt) / 1000), vel);
    } else {
      this.pulsadaDesde = 0;
      if (!this.agarrada && this.y < RIEL.abajo) this.mover(Math.max(RIEL.arriba, this.y - (MUELLE * dt) / 1000), -MUELLE);
    }
    const planta = Math.round(((this.y - RIEL.arriba) / (RIEL.abajo - RIEL.arriba)) * PLANTAS);
    this.planta.setText(planta === 0 ? 'SÓTANO' : `PLANTA ${planta}`);
    if (this.y >= RIEL.abajo - 1) {
      this.hecho = true;
      audio.play('sello');
      this.time.delayedCall(700, () => this.terminar({ resultado: this.chirridos ? 'chirrido' : 'limpio', datos: { chirridos: this.chirridos } }));
    }
  }
}
