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
  /** Sigilo: la acción principal esconde al protagonista aquí (sábanas, portales, el carrito…). */
  escondite?: boolean;
  /** Sigilo: pisar la zona hace ruido (charcos, cubos) y atrae a los guardias cercanos. */
  ruido?: boolean;
  /** Sigilo: al pisar la zona, el punto de control pasa a ser este punto de aparición. */
  checkpoint?: string;
}

/** Quien vigila: un guardia que sigue una ruta o una telepantalla (sigilo, diseño técnico §6.5). */
export interface Vigia {
  /** Puntos de la ruta (el primero es donde empieza). Uno solo: no se mueve. */
  ruta: Point[];
  /** Alcance del cono en px y semiángulo en grados. */
  alcance: number;
  angulo: number;
  velocidad: number;
  /** Pausa en cada punto de la ruta (ms). */
  pausa: number;
  /** Direcciones a las que mira cuando está parado (se alternan en cada pausa). */
  gira?: Dir[];
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
  /** Sigilo: el personaje vigila (ruta y cono de visión). */
  vigia?: Vigia;
  /** Persigue al protagonista mientras ve su luz (Crane en los túneles): velocidad y variable de ink con la distancia. */
  /** siempre: condición con la que persigue aunque no vea la linterna (Crane, cuando te ha oído chocar). */
  persigue?: { velocidad: number; variable: string; siempre?: string };
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
  /** Fondos alternativos cuando se cumple su condición (el mismo sitio, cambiado); gana el primero. */
  fondosAlt: { clave: string; condicion: string }[];
  /** Luces de neón que parpadean. */
  parpadeo: boolean;
  /** Lo que ve la telepantalla (polígono); se dibuja cuando el jugador lleva el diario en la mano. */
  cono?: Point[];
  /** Telepantalla que gira: dos conos que se alternan cada pocos segundos; la variable dice si mira el primero. */
  conosRotativos?: { conos: Point[][]; variable: string; periodo: number };
  /**
   * Sigilo (diseño técnico §6.5): los conos ven al protagonista. Si le ven, se ejecuta alSerVisto
   * y vuelve al último punto de control.
   */
  sigilo?: {
    alSerVisto: string;
    checkpoint?: string;
    /** Solo vigilan mientras se cumple esta condición (p. ej. mientras se lleva algo encima). */
    condicion?: string;
    /** Telepantallas fijas que vigilan (polígonos; el primer punto es la pantalla). */
    fijos: Point[][];
    /** Telepantallas empotradas y ocultas (Minimor): solo se notan por el zumbido al acercarse. */
    ocultos: Point[][];
    /** «Sigilo social» (Miniver): con la carpeta abierta y en movimiento, nadie repara en ti. */
    social: boolean;
  };
  /** Oscuridad total: solo se ve lo que alumbra la linterna de dinamo (túneles). */
  oscuro: boolean;
  /** Knot que se lanza cada vez que el protagonista choca con algo a oscuras, con la linterna apagada. */
  alChocar?: string;
  /** La música del lugar (src/systems/Musica.ts), con condición opcional. */
  musica?: { id: string; condicion?: string };
  /** Un medidor en pantalla que lee una variable de ink de 0 a 100 (el hambre de la celda). */
  medidor?: { variable: string; etiqueta: string; condicion?: string };
}

interface TiledProp { name: string; value: unknown }
interface TiledObject { name: string; x: number; y: number; width: number; height: number; properties?: TiledProp[] }
interface TiledLayer { name: string; type: string; objects?: TiledObject[] }
interface TiledMap { width: number; height: number; tilewidth: number; tileheight: number; properties?: TiledProp[]; layers: TiledLayer[] }

const props = (p?: TiledProp[]) => Object.fromEntries((p ?? []).map((x) => [x.name, String(x.value)]));
const puntos = (s: string): Point[] => s.split(';').map((p) => { const [x, y] = p.split(',').map(Number); return { x, y }; });
const poligonos = (s?: string): Point[][] => (s ? s.split('|').map(puntos) : []);

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
      escondite: p.escondite === 'true', ruido: p.ruido === 'true', checkpoint: p.checkpoint,
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
        vigia: p.vista ? {
          ruta: p.ruta ? puntos(p.ruta) : [{ x: o.x, y: o.y }],
          alcance: Number(p.vista.split(',')[0]) || 90,
          angulo: Number(p.vista.split(',')[1]) || 35,
          velocidad: Number(p.velocidad) || 34,
          pausa: Number(p.pausa) || 1200,
          gira: p.gira ? p.gira.split(',') as Dir[] : undefined,
        } : undefined,
        persigue: p.persigue ? { velocidad: Number(p.persigue) || 30, variable: p.distancia_var ?? '', siempre: p.persigue_si } : undefined,
      };
    }),
    alEntrar: mp.al_entrar,
    tinteProta: mp.prota_tinte ? parseInt(mp.prota_tinte.replace('#', ''), 16) : undefined,
    // fondo_alt + fondo_alt_si (uno) o fondos_alt="loc-a:cond|loc-b:cond" (varios; gana el primero que se cumple)
    fondosAlt: [
      ...(mp.fondos_alt ? mp.fondos_alt.split('|').map((x) => { const i = x.indexOf(':'); return { clave: x.slice(0, i), condicion: x.slice(i + 1) }; }) : []),
      ...(mp.fondo_alt ? [{ clave: mp.fondo_alt, condicion: mp.fondo_alt_si ?? '' }] : []),
    ],
    parpadeo: mp.parpadeo === 'true',
    conosRotativos: mp.conos ? { conos: poligonos(mp.conos), variable: mp.cono_var ?? '', periodo: Number(mp.cono_periodo) || 5000 } : undefined,
    cono: mp.cono ? puntos(mp.cono) : undefined,
    sigilo: mp.sigilo ? {
      alSerVisto: mp.sigilo, checkpoint: mp.checkpoint, condicion: mp.sigilo_si, fijos: poligonos(mp.vigila), ocultos: poligonos(mp.ocultos), social: mp.social === 'true',
    } : undefined,
    oscuro: mp.oscuro === 'true',
    alChocar: mp.al_chocar,
    musica: mp.musica ? { id: mp.musica, condicion: mp.musica_si } : undefined,
    // medidor="hambre,Hambre" (+ medidor_si="cond")
    medidor: mp.medidor ? { variable: mp.medidor.split(',')[0], etiqueta: mp.medidor.split(',')[1] ?? mp.medidor, condicion: mp.medidor_si } : undefined,
    sigueCamara: map.width * map.tilewidth > 480 || map.height * map.tileheight > 288,   // 270 px = 17 tiles (272)
  };
}

/** Evalúa una condición simple de hotspot/NPC contra un lector de variables: "var", "!var", "var==v", "var>=3"… */
export function cumple(condicion: string | undefined, leer: (v: string) => unknown): boolean {
  if (!condicion) return true;
  return condicion.split('&&').every((parte) => {
    const c = parte.trim();
    const m = /^(!)?\s*([\w.]+)\s*(==|!=|>=|<=|>|<)?\s*(.*)$/.exec(c);
    if (!m) return true;
    const [, no, nombre, op, valor] = m;
    const v = leer(nombre);
    if (!op) return no ? !v : !!v;
    const limpio = valor.replace(/^"|"$/g, '');
    if (op === '==') return String(v) === limpio;
    if (op === '!=') return String(v) !== limpio;
    const a = Number(v), b = Number(limpio);
    return op === '>=' ? a >= b : op === '<=' ? a <= b : op === '>' ? a > b : a < b;
  });
}

/** Punto dentro de un polígono (regla par-impar). */
export function dentroPoligono(p: Point, poligono: Point[]): boolean {
  let dentro = false;
  for (let i = 0, j = poligono.length - 1; i < poligono.length; j = i++) {
    const a = poligono[i], b = poligono[j];
    if ((a.y > p.y) !== (b.y > p.y) && p.x < ((b.x - a.x) * (p.y - a.y)) / (b.y - a.y) + a.x) dentro = !dentro;
  }
  return dentro;
}

export function contains(r: Rect, p: Point): boolean {
  return p.x >= r.x && p.x < r.x + r.w && p.y >= r.y && p.y < r.y + r.h;
}

export function overlaps(a: Rect, b: Rect): boolean {
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}
