/**
 * «Reducir destellos y vibración» (diseño técnico §9): los temblores de cámara se quedan en un
 * leve movimiento y los destellos claros desaparecen, en todas las escenas a la vez.
 * Los efectos hechos a mano (el dial, la resistencia, los recuerdos, los neones) preguntan a `suave()`.
 */
import Phaser from 'phaser';
import { opciones } from '../core/Opciones';

export const suave = () => opciones.destellos;

/** Intensidad de un parpadeo a mano: con la opción activa, mucho más tenue. */
export const destello = (alpha: number) => (opciones.destellos ? Math.min(alpha, 0.25) : alpha);

type Cam = Phaser.Cameras.Scene2D.Camera;
const proto = Phaser.Cameras.Scene2D.Camera.prototype as Cam;
const shake = proto.shake;
const flash = proto.flash;

proto.shake = function (this: Cam, duracion?: number, intensidad?: number | Phaser.Math.Vector2, ...resto: unknown[]) {
  if (opciones.destellos && typeof intensidad === 'number') intensidad *= 0.15;
  return (shake as (...a: unknown[]) => Cam).call(this, duracion, intensidad, ...resto);
};

proto.flash = function (this: Cam, duracion = 250, r = 255, g = 255, b = 255, ...resto: unknown[]) {
  // los fundidos breves a negro (volver al punto de control) se quedan; los destellos claros, no
  if (opciones.destellos && r + g + b > 200) {
    const [, alTerminar, contexto] = resto as [boolean?, ((...a: unknown[]) => void)?, unknown?];
    if (alTerminar) this.scene.time.delayedCall(duracion, () => alTerminar.call(contexto ?? this, this, 1));
    return this;
  }
  return (flash as (...a: unknown[]) => Cam).call(this, duracion, r, g, b, ...resto);
};
