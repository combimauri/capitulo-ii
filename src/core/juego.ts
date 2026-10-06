/** Instancias compartidas por todas las escenas. */
import historia from '../../content/ink/main.ink';
import { NarrativeBridge } from './NarrativeBridge';
import { parseTiled, type LocationData } from './Location';
import items from '../../content/items.json';

export const narrativa = new NarrativeBridge(historia);

const mapas = import.meta.glob('../../content/locations/*.tmj', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;

export const LOCALIZACIONES: Record<string, LocationData> = Object.fromEntries(
  Object.entries(mapas).map(([ruta, raw]) => {
    const id = ruta.split('/').pop()!.replace('.tmj', '');
    return [id, parseTiled(id, raw)];
  }),
);

export interface Item { nombre: string; icono: string; descripcion: string }
export const ITEMS = items as Record<string, Item>;

/** Vector del joystick táctil (lo escribe LocationScene, lo dibuja UIScene). */
export const tactil = { activo: false, x: 0, y: 0, origen: { x: 0, y: 0 } };

export const RESOLUCION = { ancho: 960, alto: 540, mundoAncho: 480, mundoAlto: 270, zoom: 2 };

/** Eventos entre escenas (se emiten por game.events). */
export const EV = {
  dialogoIniciar: 'dialogo:iniciar',    // (ruta?: string)  sin ruta = continuar el flujo principal
  dialogoFin: 'dialogo:fin',
  foco: 'hotspot:foco',                 // (info | null)
  depurar: 'depurar',                   // (activo: boolean)
  accion: 'accion',                     // ('principal' | 'mirar')  botones táctiles
  joystick: 'joystick',                 // ()  redibujar el joystick
} as const;
