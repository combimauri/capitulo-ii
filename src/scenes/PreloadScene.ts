import Phaser from 'phaser';
import { LOCALIZACIONES, ITEMS } from '../core/juego';
import { COLOR, FUENTE, hex } from '../ui/estilo';

export const DIRS = ['abajo', 'izquierda', 'derecha', 'arriba'] as const;
const EXPRESIONES_RETRATO = ['neutral', 'entusiasmo', 'odio', 'jubilo', 'desprecio', 'duelo'];

export class PreloadScene extends Phaser.Scene {
  constructor() { super('Preload'); }

  preload() {
    const { width, height } = this.scale;
    const barra = this.add.rectangle(width / 2 - 150, height / 2, 0, 6, COLOR.tele4).setOrigin(0, 0.5);
    this.add.rectangle(width / 2, height / 2, 304, 10).setStrokeStyle(1, COLOR.tele1);
    this.add.text(width / 2, height / 2 - 28, 'CARGANDO REGISTROS DEL PARTIDO…', {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.tele5),
    }).setOrigin(0.5);
    this.load.on('progress', (p: number) => barra.setSize(300 * p, 6));

    // escenarios: un PNG por localización (o el indicado en la propiedad "fondo" del mapa)
    const fondos = new Set(Object.values(LOCALIZACIONES).map((l) => l.fondo));
    for (const clave of fondos) this.load.image(clave, `assets/locations/${clave.replace(/^loc-/, '')}.png`);

    // protagonista (H y M) y personajes de los mapas
    for (const g of ['h', 'm']) this.load.spritesheet(`prot_${g}`, `assets/sprites/protagonista_${g}.png`, { frameWidth: 20, frameHeight: 40 });
    const npcs = new Set(Object.values(LOCALIZACIONES).flatMap((l) => l.npcs.map((n) => n.sprite)));
    for (const n of npcs) this.load.spritesheet(`npc-${n}`, `assets/sprites/npc/${n}.png`, { frameWidth: 20, frameHeight: 40 });

    // retratos del crimen facial (y su versión agrietada)
    for (const g of ['h', 'm']) {
      for (const e of EXPRESIONES_RETRATO) {
        this.load.image(`retrato-prot_${g}_${e}`, `assets/retratos/prot_${g}_${e}.png`);
        this.load.image(`retrato-prot_${g}_${e}_grieta`, `assets/retratos/prot_${g}_${e}_grieta.png`);
      }
    }
    for (const f of ['neutral', 'grita', 'grita2', 'gafas']) this.load.image(`retrato-amory_${f}`, `assets/retratos/amory_${f}.png`);

    // minijuegos e iconos
    this.load.image('cascotes-fondo', 'assets/minijuegos/cascotes-fondo.png');
    this.load.image('mapa-frente', 'assets/minijuegos/mapa-frente.png');
    for (const p of ['goldstein', 'oveja', 'soldado', 'diccionario', 'gran_hermano']) this.load.image(`cf-${p}`, `assets/minijuegos/cf-${p}.png`);
    for (const i of [1, 2, 3]) this.load.image(`cascote-${i}`, `assets/minijuegos/cascote-${i}.png`);
    for (const item of Object.values(ITEMS)) this.load.image(item.icono, `assets/iconos/${item.icono}.png`);
    this.load.on('loaderror', (f: Phaser.Loader.File) => console.warn('[carga] falta', f.src));
  }

  create() {
    for (const g of ['prot_h', 'prot_m']) {
      DIRS.forEach((dir, fila) => {
        this.anims.create({
          key: `${g}-${dir}-andar`,
          frames: this.anims.generateFrameNumbers(g, { start: fila * 5 + 1, end: fila * 5 + 4 }),
          frameRate: 8,
          repeat: -1,
        });
      });
    }
    this.scene.start('Menu');
  }
}
