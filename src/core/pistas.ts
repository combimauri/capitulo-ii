/**
 * Qué marca lleva cada hotspot (pistas visuales, src/ui/marcas.ts). Sin Phaser: se prueba en Node.
 */
import type { Hotspot } from './Location';
import type { Simulacion } from './NarrativeBridge';

/** Cómo se llaman las salidas en los mapas (tools/generar_mapas.py): salir, puerta, portal, escalera, ir_…, entrar_… */
const SALIDA = /salir|salida|puerta|portal|bajar|subir|volver|irse|escalera|ascensor|(^|\.)ir_|entrar_/;

/** Lo que se sabe de un hotspot: si lleva a otra escena y si tiene líneas sin leer. */
export interface Analisis { salida: boolean; nuevo: boolean; vistazo: boolean }

/** Clasifica un hotspot jugando en seco sus acciones. Puro (sin Phaser): se prueba en Node. */
export function analizar(h: Hotspot, estado: string, leidas: Set<string>,
  simular: (ruta: string, estado: string) => Simulacion): Analisis {
  const principal = h.hablar ?? h.usar ?? h.mirar;
  const r: Analisis = { salida: false, nuevo: false, vistazo: false };
  if (principal) {
    const s = simular(principal, estado);
    // una salida lleva a otra escena y además se llama como una salida: los cambios de escena de la historia
    // (la mano de Ivy entre los escombros, el cohete del mercado, el final del sueño) no son puertas
    r.salida = !!s.escena && SALIDA.test(`${h.name} ${principal}`);
    r.nuevo = s.ids.some((id) => !leidas.has(id));
  }
  if (!r.nuevo && h.mirar && h.mirar !== principal) r.vistazo = simular(h.mirar, estado).ids.some((id) => !leidas.has(id));
  return r;
}
