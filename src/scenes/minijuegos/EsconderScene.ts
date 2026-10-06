/**
 * Esconder el diario (guion J6.05): ~6 segundos para arrastrar lo comprometedor a un escondite
 * antes de que Hilda abra la puerta. Unos escondites son seguros y otros no (eso lo decide ink).
 *   # minijuego:esconder,vars=escondite_j6
 * Datos: <objeto> = cartel | colchon | cajon | hornillo | ninguno, por cada objeto que se lleve encima.
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa, ITEMS } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const TIEMPO = 6500;
/** Escondites, en coordenadas del mapa del piso (el fondo se dibuja a 2x). */
const ESCONDITES: Record<string, { nombre: string; x: number; y: number; w: number; h: number }> = {
  cartel: { nombre: 'Detrás del cartel de Ivy', x: 192, y: 24, w: 40, h: 50 },
  colchon: { nombre: 'Bajo el colchón', x: 50, y: 70, w: 52, h: 96 },
  cajon: { nombre: 'En el cajón', x: 392, y: 144, w: 30, h: 22 },
  hornillo: { nombre: 'Dentro del hornillo', x: 350, y: 116, w: 36, h: 30 },
};
/** Lo que puede comprometer (id de inventario → clave del resultado). */
const OBJETOS: [string, string][] = [['diario', 'diario'], ['parte_alterado', 'parte'], ['foto_ivy_restaurada', 'foto']];

export class EsconderScene extends Minijuego {
  private dondes: Record<string, string> = {};
  private acabado = false;

  constructor() { super('Esconder'); }

  create() {
    const { width, height } = this.scale;
    this.dondes = {}; this.acabado = false;
    this.cameras.main.fadeIn(200, 11, 12, 15);
    this.add.image(0, 0, 'loc-piso_noche').setOrigin(0).setScale(2);
    this.add.rectangle(0, 0, width, height, 0x000000, 0.35).setOrigin(0);
    this.add.text(width / 2, 22, 'Hilda está en la puerta. Esconde lo que no debe ver.', {
      fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.papel4), backgroundColor: '#000000aa', padding: { x: 10, y: 4 },
    }).setOrigin(0.5, 0);

    const zonas = Object.entries(ESCONDITES).map(([id, e]) => {
      const r = this.add.rectangle(e.x * 2, e.y * 2, e.w * 2, e.h * 2, COLOR.ocre4, 0.12).setOrigin(0).setStrokeStyle(2, COLOR.ocre4, 0.8);
      const t = this.add.text(e.x * 2 + e.w, e.y * 2 + e.h * 2 + 4, e.nombre, {
        fontFamily: FUENTE.texto, fontSize: '15px', color: hex(COLOR.ocre4), backgroundColor: '#000000aa', padding: { x: 4, y: 1 },
      }).setOrigin(0.5, 0);
      return { id, r, t };
    });

    // los objetos, abajo, listos para arrastrar
    const inventario = narrativa.list('inventario');
    const presentes = OBJETOS.filter(([item]) => inventario.includes(item));
    presentes.forEach(([item, clave], i) => {
      this.dondes[clave] = 'ninguno';
      const x = width / 2 + (i - (presentes.length - 1) / 2) * 120, y = height - 70;
      const fondo = this.add.rectangle(0, 0, 76, 76, 0x1a1411, 0.95).setStrokeStyle(2, COLOR.papel3);
      const icono = this.add.image(0, 0, ITEMS[item]?.icono ?? '').setScale(3.5);
      const c = this.add.container(x, y, [fondo, icono]).setSize(76, 76).setInteractive({ draggable: true, useHandCursor: true });
      c.setData('origen', { x, y });
      c.on('drag', (_p: Phaser.Input.Pointer, dx: number, dy: number) => c.setPosition(dx, dy));
      c.on('dragend', () => {
        const z = zonas.find(({ r }) => Phaser.Geom.Rectangle.Contains(r.getBounds(), c.x, c.y));
        if (z && !this.acabado) {
          this.dondes[clave] = z.id;
          audio.play('plumilla');
          c.disableInteractive();
          this.tweens.add({ targets: c, scale: 0.4, alpha: 0, duration: 200 });
          if (Object.values(this.dondes).every((d) => d !== 'ninguno')) this.time.delayedCall(400, () => this.acabar());
        } else {
          const o = c.getData('origen');
          this.tweens.add({ targets: c, x: o.x, y: o.y, duration: 150 });
        }
      });
    });

    // la cuenta atrás: tres golpes secos, y otra vez
    const barra = this.add.rectangle(width / 2 - 300, 70, 600, 8, COLOR.rojo4).setOrigin(0, 0.5);
    this.tweens.add({ targets: barra, scaleX: 0, duration: TIEMPO });
    for (let t = 0; t < TIEMPO; t += 2200) {
      for (let k = 0; k < 3; k++) this.time.delayedCall(t + k * 220, () => { audio.play('sello'); this.cameras.main.shake(60, 0.002); });
    }
    this.time.delayedCall(TIEMPO, () => this.acabar());
    if (!presentes.length) this.time.delayedCall(300, () => this.acabar());
  }

  private acabar() {
    if (this.acabado) return;
    this.acabado = true;
    this.terminar({ resultado: 'hecho', datos: { ...this.dondes } }, 300);
  }
}
