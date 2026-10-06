/**
 * Base de los minijuegos (diseño técnico §6.1): reciben parámetros desde una etiqueta de ink
 * y devuelven un resultado al puente narrativo. Nunca tocan el estado de ink directamente.
 */
import Phaser from 'phaser';

export type Datos = Record<string, string | number | boolean>;

export interface ResultadoMinijuego {
  resultado: string;
  datos?: Datos;
}

export interface EntradaMinijuego {
  params: Record<string, string>;
  alTerminar: (r: ResultadoMinijuego) => void;
}

export abstract class Minijuego extends Phaser.Scene {
  protected params: Record<string, string> = {};
  private alTerminar: ((r: ResultadoMinijuego) => void) | null = null;
  private terminado = false;

  /** Tiempo que la app ha pasado en segundo plano durante el minijuego (móvil): no cuenta como jugado. */
  private tiempoOculto = 0;

  init(d: EntradaMinijuego) {
    this.params = d.params ?? {};
    this.alTerminar = d.alTerminar;
    this.terminado = false;
    this.tiempoOculto = 0;
    let ocultoEn = 0;
    const oculto = () => { ocultoEn = performance.now(); };
    const visible = () => { if (ocultoEn) this.tiempoOculto += performance.now() - ocultoEn; ocultoEn = 0; };
    this.game.events.on(Phaser.Core.Events.HIDDEN, oculto);
    this.game.events.on(Phaser.Core.Events.VISIBLE, visible);
    this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => {
      this.game.events.off(Phaser.Core.Events.HIDDEN, oculto);
      this.game.events.off(Phaser.Core.Events.VISIBLE, visible);
    });
  }

  /** El reloj del minijuego: el de la escena, sin el rato en que la app estuvo en segundo plano. */
  protected ahora() {
    return this.time.now - this.tiempoOculto;
  }

  protected terminar(r: ResultadoMinijuego, fundido = 300) {
    if (this.terminado) return;
    this.terminado = true;
    const cb = this.alTerminar;
    this.cameras.main.fadeOut(fundido, 11, 12, 15);
    this.cameras.main.once('camerafadeoutcomplete', () => {
      this.scene.stop();
      cb?.(r);
    });
  }
}
