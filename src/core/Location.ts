/** Lectura de mapas de Tiled (.tmj) al formato que usa LocationScene (diseño técnico §5). */

export type Dir = 'abajo' | 'arriba' | 'izquierda' | 'derecha';

export interface Rect { x: number; y: number; w: number; h: number }
export interface Point { x: number; y: number }

export interface Hotspot extends Rect {
  name: string;
  nombre: string;
  mirar?: string;
  usar?: string;
  hablar?: string;
  aprox: Point;
  orientacion?: Dir;
}

export interface Spawn extends Point { name: string; orientacion: Dir }

export interface LocationData {
  id: string;
  nombre: string;
  fondo: string;
  width: number;
  height: number;
  colisiones: Rect[];
  hotspots: Hotspot[];
  spawns: Spawn[];
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
  return {
    id,
    nombre: mp.nombre ?? id,
    fondo: mp.fondo ?? `loc-${id}`,
    width: map.width * map.tilewidth,
    height: map.height * map.tileheight,
    colisiones: layer('colisiones').map((o) => ({ x: o.x, y: o.y, w: o.width, h: o.height })),
    hotspots: layer('hotspots').map((o) => {
      const p = props(o.properties);
      const [ax, ay] = (p.aprox ?? `${o.x + o.width / 2},${o.y + o.height + 8}`).split(',').map(Number);
      return {
        name: o.name, nombre: p.nombre_visible ?? o.name, x: o.x, y: o.y, w: o.width, h: o.height,
        mirar: p.mirar, usar: p.usar, hablar: p.hablar, aprox: { x: ax, y: ay },
        orientacion: p.orientacion as Dir | undefined,
      };
    }),
    spawns: layer('spawns').map((o) => ({
      name: o.name, x: o.x, y: o.y, orientacion: (props(o.properties).orientacion ?? 'abajo') as Dir,
    })),
  };
}

export function contains(r: Rect, p: Point): boolean {
  return p.x >= r.x && p.x < r.x + r.w && p.y >= r.y && p.y < r.y + r.h;
}

export function overlaps(a: Rect, b: Rect): boolean {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}
