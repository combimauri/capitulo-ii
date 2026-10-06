/** Instancias compartidas por todas las escenas. */
import historia from '../../content/ink/main.ink';
import { NarrativeBridge } from './NarrativeBridge';
import { parseTiled, type LocationData } from './Location';
import pisoRaw from '../../content/locations/piso.tmj?raw';

export const narrativa = new NarrativeBridge(historia);

export const LOCALIZACIONES: Record<string, LocationData> = {
  piso: parseTiled('piso', pisoRaw),
};

export const RESOLUCION = { ancho: 960, alto: 540, mundoAncho: 480, mundoAlto: 270, zoom: 2 };

/** Eventos entre escenas (se emiten por game.events). */
export const EV = {
  dialogoIniciar: 'dialogo:iniciar',    // (ruta?: string)  sin ruta = continuar el flujo principal
  dialogoFin: 'dialogo:fin',
  foco: 'hotspot:foco',                 // (info | null)
  depurar: 'depurar',                   // (activo: boolean)
} as const;
