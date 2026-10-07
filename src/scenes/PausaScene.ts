/**
 * Pausa (Esc o el botón MENÚ en pantallas táctiles): detiene el escenario y la interfaz.
 * Continuar · Opciones · Salir al menú (se sigue desde el último punto guardado).
 */
import Phaser from 'phaser';
import { EV, mano, mision } from '../core/juego';
import { COLOR, FUENTE, hex } from '../ui/estilo';
import { alternarPantallaCompleta, hayPantallaCompleta } from '../ui/pantalla';

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

    this.botones = [];
    const opciones: [string, () => void][] = [
      ['Continuar', () => this.continuar()],
      ['Opciones', () => this.opciones()],
      // en móvil, entrar y salir de la pantalla completa sin dejar la partida
      ...(hayPantallaCompleta(this) ? [[this.textoPantalla(), () => alternarPantallaCompleta(this)] as [string, () => void]] : []),
      ['Salir al menú', () => this.salir()],
    ];
    const alto = 170 + opciones.length * 56;
    this.add.rectangle(0, 0, width, height, 0x000000, 0.72).setOrigin(0).setInteractive();
    this.add.rectangle(width / 2, height / 2, 380, alto, COLOR.gris1, 0.96).setStrokeStyle(2, COLOR.gris3);
    this.add.rectangle(width / 2, height / 2 - alto / 2, 380, 4, COLOR.rojo3);
    this.add.text(width / 2, height / 2 - alto / 2 + 44, 'PAUSA', { fontFamily: FUENTE.maquina, fontSize: '40px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    opciones.forEach(([texto, accion], i) => {
      const y = height / 2 - alto / 2 + 112 + i * 56;
      const fondo = this.add.rectangle(width / 2, y, 300, 44, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
      const t = this.add.text(width / 2, y, texto, { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(0.5);
      fondo.on('pointerover', () => this.seleccionar(i));
      fondo.on('pointerup', accion);
      this.botones.push({ fondo, accion });
      if (texto === this.textoPantalla()) {
        const rotular = () => t.setText(this.textoPantalla());
        this.scale.on(Phaser.Scale.Events.ENTER_FULLSCREEN, rotular);
        this.scale.on(Phaser.Scale.Events.LEAVE_FULLSCREEN, rotular);
        this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
          this.scale.off(Phaser.Scale.Events.ENTER_FULLSCREEN, rotular);
          this.scale.off(Phaser.Scale.Events.LEAVE_FULLSCREEN, rotular);
        });
      }
    });
    this.add.text(width / 2, height / 2 + alto / 2 - 24, 'Al salir se sigue desde el último punto guardado.', {
      fontFamily: FUENTE.texto, fontSize: '14px', color: '#8f8a7a',
    }).setOrigin(0.5);
    this.seleccionar(0);

    const kb = this.input.keyboard!;
    kb.on('keydown-ESC', () => this.continuar());
    const n = this.botones.length;
    kb.on('keydown-UP', () => this.seleccionar((this.seleccion + n - 1) % n));
    kb.on('keydown-DOWN', () => this.seleccionar((this.seleccion + 1) % n));
    kb.on('keydown-ENTER', () => this.botones[this.seleccion].accion());
  }

  private textoPantalla() {
    return this.scale.isFullscreen ? 'Salir de pantalla completa' : 'Pantalla completa';
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
