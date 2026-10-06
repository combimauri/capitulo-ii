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

  init(d: EntradaMinijuego) {
    this.params = d.params ?? {};
    this.alTerminar = d.alTerminar;
    this.terminado = false;
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
