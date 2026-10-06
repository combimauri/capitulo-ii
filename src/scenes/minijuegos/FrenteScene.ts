/**
 * Minijuego 2 — Mover el frente (diseño técnico §6.4).
 * Las banderitas rojas se arrastran hasta la nueva línea que dicta la directiva.
 * El corcho está acribillado de agujeros de alfiler: el frente siempre vuelve al mismo río.
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const MAPA = { x: 120, y: 78, escala: 2 };          // la imagen mide 360x200 y se dibuja al doble
const PX_POR_KM = 1.5;                               // píxeles de arte por kilómetro
const DIRECCION = { x: 0.62, y: -0.78 };             // hacia el noreste (hacia el enemigo)
// posiciones actuales de las banderas (coordenadas de la imagen del mapa)
const FRENTE = [{ x: 70, y: 166 }, { x: 120, y: 150 }, { x: 170, y: 150 }, { x: 220, y: 134 }, { x: 270, y: 126 }];
const TOLERANCIA = 12;

const aPantalla = (p: { x: number; y: number }) => ({ x: MAPA.x + p.x * MAPA.escala, y: MAPA.y + p.y * MAPA.escala });

export class FrenteScene extends Minijuego {
  private colocadas = 0;
  private linea!: Phaser.GameObjects.Graphics;
  private banderas: Phaser.GameObjects.Container[] = [];

  constructor() { super('Frente'); }

  create() {
    this.colocadas = 0;
    this.banderas = [];
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(width / 2, height / 2, width, height, 0x1a1411);
    this.add.image(MAPA.x, MAPA.y, 'mapa-frente').setOrigin(0).setScale(MAPA.escala);

    const km = Number(String(narrativa.get('parte_j1_km') ?? '12').replace(/\D/g, '')) || 12;
    const d = km * PX_POR_KM;
    this.add.text(24, 16, `minipax.carto 15.4.84 malabar · avance ${km}km confirmado · desplazar línea frente`, {
      fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4),
    });
    this.add.text(24, 40, 'Arrastra cada bandera roja hasta su nueva posición.', {
      fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3),
    });

    // escala
    const ex = MAPA.x + 20, ey = MAPA.y + 400 - 22;
    this.add.rectangle(ex, ey, 10 * PX_POR_KM * MAPA.escala, 4, COLOR.gris2).setOrigin(0, 0.5);
    this.add.text(ex, ey - 18, '10 km', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.gris2) });

    this.linea = this.add.graphics();
    const objetivos = FRENTE.map((p) => ({ x: p.x + DIRECCION.x * d, y: p.y + DIRECCION.y * d }));
    objetivos.forEach((o) => {
      const s = aPantalla(o);
      this.add.circle(s.x, s.y, 7).setStrokeStyle(2, COLOR.rojo4, 0.7);
      this.add.text(s.x + 9, s.y - 9, '?', { fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.rojo4) }).setAlpha(0.7);
    });

    FRENTE.forEach((p, i) => {
      const s = aPantalla(p);
      const b = this.crearBandera(s.x, s.y);
      b.setData('objetivo', aPantalla(objetivos[i]));
      this.banderas.push(b);
    });
    this.dibujarLinea();

    this.input.on('drag', (_p: Phaser.Input.Pointer, obj: Phaser.GameObjects.Container, x: number, y: number) => {
      obj.setPosition(x, y);
      this.dibujarLinea();
    });
    this.input.on('dragend', (_p: Phaser.Input.Pointer, obj: Phaser.GameObjects.Container) => {
      const o = obj.getData('objetivo') as { x: number; y: number };
      if (Phaser.Math.Distance.Between(obj.x, obj.y, o.x, o.y) <= TOLERANCIA) {
        obj.setPosition(o.x, o.y);
        obj.disableInteractive();
        obj.setData('colocada', true);
        audio.play('tecla');
        this.colocadas++;
        this.dibujarLinea();
        if (this.colocadas === FRENTE.length) this.completado(km);
      }
    });
  }

  private crearBandera(x: number, y: number) {
    const c = this.add.container(x, y);
    c.add(this.add.rectangle(0, -10, 2, 20, COLOR.gris2).setOrigin(0.5, 0.5));
    c.add(this.add.rectangle(1, -18, 12, 8, COLOR.rojo4).setOrigin(0, 0.5).setStrokeStyle(1, 0x4f1114));
    c.add(this.add.circle(0, 0, 3, COLOR.gris2));
    c.setSize(24, 30).setInteractive({ draggable: true, useHandCursor: true });
    return c;
  }

  private dibujarLinea() {
    const g = this.linea.clear().lineStyle(3, COLOR.rojo3, 0.85);
    g.beginPath();
    this.banderas.forEach((b, i) => (i ? g.lineTo(b.x, b.y) : g.moveTo(b.x, b.y)));
    g.strokePath();
  }

  private completado(km: number) {
    const { width } = this.scale;
    this.add.text(width / 2, 500, `Frente de Malabar actualizado: +${km} km`, {
      fontFamily: FUENTE.maquina, fontSize: '28px', color: hex(COLOR.papel4), backgroundColor: '#000000', padding: { x: 12, y: 4 },
    }).setOrigin(0.5);
    this.time.delayedCall(1500, () => this.terminar({ resultado: 'hecho' }));
  }
}
