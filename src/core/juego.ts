/** Instancias compartidas por todas las escenas. */
import historia from '../../content/ink/main.ink';
import { NarrativeBridge } from './NarrativeBridge';
import { parseTiled, type LocationData } from './Location';
import items from '../../content/items.json';
import { Registro } from './Registro';

export const narrativa = new NarrativeBridge(historia);

/** Historial de lo leído; el doblepensar lo reescribe (diseño técnico §7.1). */
export const registro = new Registro();

const mapas = import.meta.glob('../../content/locations/*.tmj', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;

export const LOCALIZACIONES: Record<string, LocationData> = Object.fromEntries(
  Object.entries(mapas).map(([ruta, raw]) => {
    const id = ruta.split('/').pop()!.replace('.tmj', '');
    return [id, parseTiled(id, raw)];
  }),
);

/** mirar: knot de ink para mirarlo desde el inventario (si el texto depende de la historia). */
export interface Item { nombre: string; icono: string; descripcion: string; mirar?: string }
export const ITEMS = items as Record<string, Item>;

/** Objeto del inventario que el jugador lleva en la mano para usarlo con algo del escenario. */
export const mano = { item: null as string | null };

/** Vector del joystick táctil (lo escribe LocationScene, lo dibuja UIScene). */
export const tactil = { activo: false, x: 0, y: 0, origen: { x: 0, y: 0 } };

/**
 * Estado de las misiones de sigilo, compartido entre LocationScene (lo actualiza) y UIScene (lo dibuja).
 * reloj: ventana de tiempo de una misión; el reloj solo corre mientras se explora (no durante los diálogos).
 */
export const mision = {
  reloj: null as null | { inicio: number; transcurrido: number; limite: number; agotar: string; agotado: boolean },
  /** Medidor de detección (0..1) mientras algún cono ve al protagonista. */
  alerta: 0,
  /** Sigilo social: el mapa lo permite y la carpeta está abierta. */
  social: false,
  carpeta: false,
  oculto: false,
};

/** "23:00:00" → segundos del día; y al revés. */
export const segundos = (h: string) => h.split(':').map(Number).reduce((a, n) => a * 60 + (n || 0), 0);
export const hora = (s: number) => [Math.floor(s / 3600) % 24, Math.floor(s / 60) % 60, Math.floor(s) % 60].map((n) => String(n).padStart(2, '0')).join(':');

export const RESOLUCION = { ancho: 960, alto: 540, mundoAncho: 480, mundoAlto: 270, zoom: 2 };

/** Eventos entre escenas (se emiten por game.events). */
export const EV = {
  dialogoIniciar: 'dialogo:iniciar',    // (ruta?: string)  sin ruta = continuar el flujo principal
  dialogoFin: 'dialogo:fin',
  foco: 'hotspot:foco',                 // (info | null)
  depurar: 'depurar',                   // (activo: boolean)
  accion: 'accion',                     // ('principal' | 'mirar')  botones táctiles
  joystick: 'joystick',                 // ()  redibujar el joystick
  pausa: 'pausa',                       // (activa: boolean)  paneles que detienen el movimiento
  mano: 'mano',                         // ()  cambió el objeto en la mano
  carpeta: 'carpeta',                   // ()  abrir o cerrar la carpeta (sigilo social)
} as const;
