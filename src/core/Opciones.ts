/**
 * Opciones de juego y accesibilidad (diseño técnico §9). Se guardan aparte de la partida
 * (no se borran al empezar otra). Los volúmenes los guarda el director de audio.
 */
export type VelocidadTexto = 'lenta' | 'normal' | 'rapida' | 'instantanea';

export interface OpcionesJuego {
  texto: VelocidadTexto;
  /** Crimen facial: ventanas normales, amplias (y más lento) o la cara se compone sola (modo historia). */
  cf: 'normal' | 'asistida' | 'automatica';
  /** Sigilo: al ser visto, la Sospecha sube la mitad. */
  sigilo: 'normal' | 'reducida';
  /** Reducir destellos y temblores: el dial, los impactos, el glitch, la Habitación 101, los neones. */
  destellos: boolean;
  /** Tamaño de la interfaz de diálogo (fuente y cajas). */
  ui: 100 | 125;
  /** Mano dominante (móvil): los botones de acción van de su lado. */
  mano: 'derecha' | 'izquierda';
}

const CLAVE = 'capitulo2.opciones.juego';
const INICIAL: OpcionesJuego = { texto: 'normal', cf: 'normal', sigilo: 'normal', destellos: false, ui: 100, mano: 'derecha' };

/** Valores válidos de cada opción, en el orden en que se ofrecen. */
export const VALORES: { [K in keyof OpcionesJuego]: readonly OpcionesJuego[K][] } = {
  texto: ['lenta', 'normal', 'rapida', 'instantanea'],
  cf: ['normal', 'asistida', 'automatica'],
  sigilo: ['normal', 'reducida'],
  destellos: [false, true],
  ui: [100, 125],
  mano: ['derecha', 'izquierda'],
};

/** Caracteres por segundo de la máquina de escribir de los diálogos. */
export const CPS: Record<VelocidadTexto, number> = { lenta: 28, normal: 55, rapida: 120, instantanea: Infinity };

function leer(): OpcionesJuego {
  const o = { ...INICIAL };
  try {
    const g = JSON.parse(window.localStorage.getItem(CLAVE) ?? '{}') as Partial<OpcionesJuego>;
    for (const k of Object.keys(INICIAL) as (keyof OpcionesJuego)[]) {
      if ((VALORES[k] as readonly unknown[]).includes(g[k])) (o as Record<string, unknown>)[k] = g[k];
    }
  } catch { /* sin almacenamiento: las de siempre */ }
  return o;
}

export const opciones: OpcionesJuego = typeof window === 'undefined' ? { ...INICIAL } : leer();

const oyentes = new Set<(k: keyof OpcionesJuego) => void>();

export function fijarOpcion<K extends keyof OpcionesJuego>(k: K, v: OpcionesJuego[K]) {
  opciones[k] = v;
  try { window.localStorage.setItem(CLAVE, JSON.stringify(opciones)); } catch { /* sin almacenamiento */ }
  oyentes.forEach((f) => f(k));
}

/** Avisa cuando cambia una opción (p. ej. desde el menú de pausa). Devuelve cómo dejar de escuchar. */
export function alCambiarOpcion(f: (k: keyof OpcionesJuego) => void): () => void {
  oyentes.add(f);
  return () => oyentes.delete(f);
}
