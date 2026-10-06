/** Lectura de mapas de Tiled (.tmj) al formato que usa LocationScene (diseño técnico §5). */

export type Dir = 'abajo' | 'arriba' | 'izquierda' | 'derecha';

export interface Rect { x: number; y: number; w: number; h: number }
export interface Colision extends Rect { condicion?: string }
export interface Point { x: number; y: number }

export interface Hotspot extends Rect {
  name: string;
  nombre: string;
  mirar?: string;
  usar?: string;
  hablar?: string;
  aprox: Point;
  orientacion?: Dir;
  /** Expresión sobre variables de ink: "var", "!var", "var==valor", "var!=valor". */
  condicion?: string;
  /** Se activa al pisar la zona (salidas por los bordes, encuentros). */
  auto?: boolean;
  /** Usar un objeto del inventario aquí: item → knot ("lapiz_amory=j3_depto.agujero_lapiz;…"). */
  con?: Record<string, string>;
}

export interface Npc extends Point {
  name: string;
  sprite: string;
  dir: Dir;
  frame?: number;
  hotspot: Hotspot;
  /** Caja de colisión en los pies. */
  solido: boolean;
  /** Si el jugador se acerca a menos de esta distancia, el personaje se aleja (sueños). */
  huye?: number;
}

export interface Spawn extends Point { name: string; orientacion: Dir }

export interface LocationData {
  id: string;
  nombre: string;
  fondo: string;
  width: number;
  height: number;
  colisiones: Colision[];
  hotspots: Hotspot[];
  spawns: Spawn[];
  npcs: Npc[];
  /** Knot de ink que se ejecuta cada vez que se entra (el knot decide si hace algo). */
  alEntrar?: string;
  /** Desplazamiento de cámara (mapas más grandes que la pantalla). */
  sigueCamara: boolean;
  /** Tinte del protagonista (p. ej. de noche en el prólogo). */
  tinteProta?: number;
  /** Fondo alternativo cuando se cumple una condición (el mismo sitio, cambiado). */
  fondoAlt?: { clave: string; condicion: string };
  /** Luces de neón que parpadean. */
  parpadeo: boolean;
}

interface TiledProp { name: string; value: unknown }
interface TiledObject { name: string; x: number; y: number; width: number; height: number; properties?: TiledProp[] }
interface TiledLayer { name: string; type: string; objects?: TiledObject[] }
interface TiledMap { width: number; height: number; tilewidth: number; tileheight: number; properties?: TiledProp[]; layers: TiledLayer[] }

const props = (p?: TiledProp[]) => Object.fromEntries((p ?? []).map((x) => [x.name, String(x.value)]));

export function parseTiled(id: string, raw: string): LocationData {
  const map = JSON.parse(raw) as TiledMap;
  const layer = (name: string) => map.layers.find((l) => l.name === name)?.objects ?? [];
  const mp = props(map.properties);
  const hotspot = (o: TiledObject, p: Record<string, string>): Hotspot => {
    const [ax, ay] = (p.aprox ?? `${o.x + o.width / 2},${o.y + o.height + 8}`).split(',').map(Number);
    return {
      name: o.name, nombre: p.nombre_visible ?? o.name, x: o.x, y: o.y, w: o.width, h: o.height,
      mirar: p.mirar, usar: p.usar, hablar: p.hablar, aprox: { x: ax, y: ay },
      orientacion: p.orientacion as Dir | undefined, condicion: p.condicion, auto: p.auto === 'true',
      con: p.con ? Object.fromEntries(p.con.split(';').map((par) => par.split('=').map((x) => x.trim()))) : undefined,
    };
  };
  return {
    id,
    nombre: mp.nombre ?? id,
    fondo: mp.fondo ?? `loc-${id}`,
    width: map.width * map.tilewidth,
    height: map.height * map.tileheight,
    colisiones: layer('colisiones').map((o) => ({ x: o.x, y: o.y, w: o.width, h: o.height, condicion: props(o.properties).condicion })),
    hotspots: layer('hotspots').map((o) => hotspot(o, props(o.properties))),
    spawns: layer('spawns').map((o) => ({
      name: o.name, x: o.x, y: o.y, orientacion: (props(o.properties).orientacion ?? 'abajo') as Dir,
    })),
    npcs: layer('npcs').map((o) => {
      const p = props(o.properties);
      // El punto del NPC son sus pies; el hotspot cubre su cuerpo (20x40).
      const h = hotspot({ ...o, x: o.x - 10, y: o.y - 40, width: 20, height: 40 }, {
        ...p, aprox: p.aprox ?? `${o.x},${o.y + 14}`, orientacion: p.orientacion_jugador ?? 'arriba',
      });
      return {
        name: o.name, x: o.x, y: o.y, sprite: p.sprite ?? o.name, dir: (p.dir ?? 'abajo') as Dir,
        frame: p.frame !== undefined ? Number(p.frame) : undefined, hotspot: h, solido: p.solido !== 'false',
        huye: p.huye ? Number(p.huye) : undefined,
      };
    }),
    alEntrar: mp.al_entrar,
    tinteProta: mp.prota_tinte ? parseInt(mp.prota_tinte.replace('#', ''), 16) : undefined,
    fondoAlt: mp.fondo_alt ? { clave: mp.fondo_alt, condicion: mp.fondo_alt_si ?? '' } : undefined,
    parpadeo: mp.parpadeo === 'true',
    sigueCamara: map.width * map.tilewidth > 480 || map.height * map.tileheight > 288,   // 270 px = 17 tiles (272)
  };
}

/** Evalúa una condición simple de hotspot/NPC contra un lector de variables. */
export function cumple(condicion: string | undefined, leer: (v: string) => unknown): boolean {
  if (!condicion) return true;
  return condicion.split('&&').every((parte) => {
    const c = parte.trim();
    const m = /^(!)?\s*([\w.]+)\s*(==|!=)?\s*(.*)$/.exec(c);
    if (!m) return true;
    const [, no, nombre, op, valor] = m;
    const v = leer(nombre);
    if (!op) return no ? !v : !!v;
    const igual = String(v) === valor.replace(/^"|"$/g, '');
    return op === '==' ? igual : !igual;
  });
}

export function contains(r: Rect, p: Point): boolean {
  return p.x >= r.x && p.x < r.x + r.w && p.y >= r.y && p.y < r.y + r.h;
}

export function overlaps(a: Rect, b: Rect): boolean {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}
