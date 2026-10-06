/**
 * Actualizaciones de la app instalada (PWA): una versión nueva no recarga la página en mitad
 * de una partida; el menú principal ofrece actualizar.
 */
import { registerSW } from 'virtual:pwa-register';

export const pwa = {
  /** Hay una versión nueva esperando: llamarla la instala y recarga. */
  actualizar: null as null | (() => void),
  /** El menú se entera cuando llega una versión nueva mientras está abierto. */
  alHaberVersion: null as null | (() => void),
};

export function registrarPwa() {
  const actualizarSW = registerSW({
    immediate: true,
    onNeedRefresh() {
      pwa.actualizar = () => void actualizarSW(true);
      pwa.alHaberVersion?.();
    },
  });
}
