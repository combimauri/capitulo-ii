/**
 * Pausa (Esc o el botón MENÚ en pantallas táctiles): detiene el escenario y la interfaz.
 * Continuar · Opciones · Salir al menú (se sigue desde el último punto guardado).
 */
import Phaser from 'phaser';
import { EV, mano, mision } from '../core/juego';
import { COLOR, FUENTE, hex } from '../ui/estilo';

/** Escenas que la pausa congela (las que estén activas). */
const CONGELA = ['Location', 'UI'];

export class PausaScene extends Phaser.Scene {
  private congeladas: string[] = [];
  private seleccion = 0;
  private botones: { fondo: Phaser.GameObjects.Rectangle; accion: () => void }[] = [];

  constructor() { super('Pausa'); }

  create() {
    const { width, height } = this.scale;
    this.congeladas = CONGELA.filter((k) => this.scene.isActive(k));
    this.congeladas.forEach((k) => this.scene.pause(k));
    this.game.events.emit(EV.guardar);

    this.add.rectangle(0, 0, width, height, 0x000000, 0.72).setOrigin(0).setInteractive();
    this.add.rectangle(width / 2, height / 2, 380, 300, COLOR.gris1, 0.96).setStrokeStyle(2, COLOR.gris3);
    this.add.rectangle(width / 2, height / 2 - 150, 380, 4, COLOR.rojo3);
    this.add.text(width / 2, height / 2 - 110, 'PAUSA', { fontFamily: FUENTE.maquina, fontSize: '40px', color: hex(COLOR.papel4) }).setOrigin(0.5);

    this.botones = [];
    const opciones: [string, () => void][] = [
      ['Continuar', () => this.continuar()],
      ['Opciones', () => this.opciones()],
      ['Salir al menú', () => this.salir()],
    ];
    opciones.forEach(([texto, accion], i) => {
      const y = height / 2 - 40 + i * 60;
      const fondo = this.add.rectangle(width / 2, y, 300, 44, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
      this.add.text(width / 2, y, texto, { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(0.5);
      fondo.on('pointerover', () => this.seleccionar(i));
      fondo.on('pointerup', accion);
      this.botones.push({ fondo, accion });
    });
    this.add.text(width / 2, height / 2 + 132, 'Al salir se sigue desde el último punto guardado.', {
      fontFamily: FUENTE.texto, fontSize: '14px', color: '#8f8a7a',
    }).setOrigin(0.5);
    this.seleccionar(0);

    const kb = this.input.keyboard!;
    kb.on('keydown-ESC', () => this.continuar());
    kb.on('keydown-UP', () => this.seleccionar((this.seleccion + 2) % 3));
    kb.on('keydown-DOWN', () => this.seleccionar((this.seleccion + 1) % 3));
    kb.on('keydown-ENTER', () => this.botones[this.seleccion].accion());
  }

  private seleccionar(i: number) {
    this.seleccion = i;
    this.botones.forEach((b, j) => b.fondo.setFillStyle(j === i ? COLOR.rojo3 : COLOR.gris2));
  }

  private continuar() {
    this.congeladas.forEach((k) => { if (this.scene.isPaused(k)) this.scene.resume(k); });
    this.scene.stop();
  }

  private opciones() {
    this.scene.pause();
    this.scene.launch('Opciones', { desde: 'pausa', alCerrar: () => this.scene.resume() });
    this.scene.bringToTop('Opciones');
  }

  private salir() {
    mano.item = null;
    mision.reloj = null;
    this.game.scene.getScenes(false).forEach((s) => {
      if (s.scene.key !== 'Pausa' && (s.scene.isActive() || s.scene.isPaused())) s.scene.stop();
    });
    this.scene.start('Menu');
  }
}
