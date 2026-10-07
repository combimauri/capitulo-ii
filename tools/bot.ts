/**
 * Bot de recorrido (diseño técnico §11.2): juega la partida entera sin Phaser, con elecciones y resultados
 * de minijuegos al azar, imitando a LocationScene y UIScene (escenas, zonas, objetos, sigilo, reloj, arresto).
 * Sirve para equilibrar la Duda y la Sospecha (hito M7) y para encontrar callejones sin salida.
 *   const p = jugarPartida(json, localizaciones, azar(1), PERFILES.azar);
 */
import { NarrativeBridge, type ChoiceOption } from '../src/core/NarrativeBridge';
import { cumple, musicaDe, type Hotspot, type LocationData } from '../src/core/Location';
import type { Tag } from '../src/core/tags';
import items from '../content/items.json';
import diario from '../content/diario/entradas.json';
import apuntes from '../content/apuntes.json';
import { objetivo, type Apuntes } from '../src/core/apuntes';

// ------------------------------------------------------------------ azar

/** Generador con semilla (mulberry32): la misma semilla, la misma partida. */
export function azar(semilla: number): () => number {
  let s = semilla >>> 0;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

type Rng = () => number;
const elegir = <T>(rng: Rng, xs: readonly T[]): T => xs[Math.floor(rng() * xs.length)];
const entre = (rng: Rng, a: number, b: number) => a + Math.floor(rng() * (b - a + 1));

/** Índice al azar según pesos. */
function ponderado(rng: Rng, pesos: number[]): number {
  const total = pesos.reduce((a, b) => a + b, 0);
  let r = rng() * total;
  for (let i = 0; i < pesos.length; i++) { r -= pesos[i]; if (r < 0) return i; }
  return pesos.length - 1;
}

// ------------------------------------------------------------------ perfiles

/**
 * Cómo juega el bot. Las probabilidades son por partida (minijuegos) o por acción (sigilo, choques).
 *   azar     elige todo con la misma probabilidad
 *   fiel     obedece: primeras opciones, acepta el doblepensar, buena cara
 *   curioso  explora y recuerda: opciones nuevas, rechaza el doblepensar, cara regular
 *   torpe    falla los minijuegos y le ven en el sigilo
 */
export interface Perfil {
  nombre: string;
  /** Probabilidad de elegir la primera opción (la obediente, casi siempre); si no, al azar. */
  primera: number;
  /** Crimen facial: perfecto, aceptable, fallo. */
  cf: [number, number, number];
  /** Probabilidad de «recordar» en el doblepensar. */
  recordar: number;
  /** Probabilidad de acertar en los minijuegos de habilidad (pancarta, palanca, llaves, rectificación…). */
  maña: number;
  /** Probabilidad de que le vean en cada acción de un mapa con sigilo (sin esconderse). */
  visto: number;
  /** Probabilidad de chocar a oscuras en cada acción (túneles). */
  choque: number;
  /** Peso de repetir una acción ya hecha en la jornada (1 = da igual; 0.1 = casi siempre algo nuevo). */
  repetir: number;
  /** Peso de las acciones de «mirar» frente a las principales. */
  mirar: number;
  /** Pesos extra sobre el texto de las opciones (p. ej. preferir las preguntas). */
  preferir?: [RegExp, number][];
  /**
   * Prever: antes de elegir, prueba cada opción hasta la siguiente elección y mira cuánto sube la Sospecha.
   * Cada 10 puntos de Sospecha dividen el peso de la opción por e^prever (negativo: los busca). 0 = no mira.
   */
  prever?: number;
  /** Acciones que este jugador casi nunca hace (clave «escena/hotspot…»), opcionalmente solo si se cumple `si`. */
  evitar?: { accion: RegExp; si?: string }[];
}

export const PERFILES: Record<string, Perfil> = {
  azar: { nombre: 'azar', primera: 0, cf: [1, 1, 1], recordar: 0.5, maña: 0.5, visto: 0.15, choque: 0.15, repetir: 0.5, mirar: 1 },
  fiel: { nombre: 'fiel', primera: 0.75, cf: [0.55, 0.4, 0.05], recordar: 0.1, maña: 0.85, visto: 0.05, choque: 0.05, repetir: 0.3, mirar: 0.5 },
  curioso: {
    nombre: 'curioso', primera: 0, cf: [0.3, 0.45, 0.25], recordar: 0.85, maña: 0.6, visto: 0.1, choque: 0.1, repetir: 0.15, mirar: 1,
    preferir: [[/¿/, 2], [/[Rr]ecord|[Pp]reguntar|[Ll]eer|[Mm]irar/, 1.5]],
  },
  /**
   * superviviente: quiere llegar a la Jornada 13 (finales D y E). Acepta a Nell, no se vende a Crane,
   * recuerda (la Duda abre la puerta de los túneles), cuida la cara y prevé qué opciones suben la Sospecha.
   */
  superviviente: {
    nombre: 'superviviente', primera: 0, cf: [0.6, 0.35, 0.05], recordar: 0.9, maña: 0.85, visto: 0.04, choque: 0.08, repetir: 0.25, mirar: 0.6, prever: 2,
    preferir: [
      [/¿Cómo entro en el Archivo|Volver mañana al cuarto|Escuchar lo que ha venido|Usted mató a mi hermana|Deme un día|Huir a casa de Dot|Acudir a la calle Cable/, 20],
      [/Apartar el carrito|No volver\.|No sé quién es usted|¿Qué quiere saber|Entregar a Goldstein/, 0.02],
    ],
  },
  /** temerario: busca la Sospecha (falla la cara, se deja ver, elige lo que más sube). Para el Final C0. */
  temerario: { nombre: 'temerario', primera: 0, cf: [0, 0.1, 0.9], recordar: 0.9, maña: 0.1, visto: 0.6, choque: 0.5, repetir: 0.6, mirar: 0.5, prever: -3 },
  torpe: { nombre: 'torpe', primera: 0, cf: [0.1, 0.3, 0.6], recordar: 0.5, maña: 0.2, visto: 0.35, choque: 0.4, repetir: 0.5, mirar: 1 },
};

// ------------------------------------------------------------------ resultado

export interface Instantanea { duda: number; sospecha: number }

export interface Partida {
  perfil: string;
  /** Final alcanzado (A, B, C, C0, D, E…), «atascado», «limite» o «error». */
  resultado: string;
  /** Si se atascó: dónde y por qué. */
  atasco?: { escena: string; jornada: number; knot: string; motivo: string };
  /** Duda y Sospecha al empezar cada jornada. */
  jornadas: Record<number, Instantanea>;
  maxDuda: number;
  maxSospecha: number;
  /** Jornada del (primer) arresto por Sospecha 100. */
  arresto?: number;
  /** Veces que se lanzó el arresto (más de una: se repite). */
  arrestos: number;
  /** Errores de ink en tiempo de ejecución y excepciones (motor o historia). */
  errores: string[];
  /** Avisos: escenas que no existen, knots que no existen, diálogos sin fin… */
  avisos: string[];
  /** Duda o Sospecha fuera de 0..100, con dónde. */
  fueraDeRango: string[];
  /** Ids de línea vistos (para saber qué rama de cada umbral se tomó). */
  lineas: Set<string>;
  /** De dónde vienen la Duda y la Sospecha: cambios sumados por knot.stitch de ink. */
  origen: Record<string, Instantanea>;
  /** Decisiones (# decision:) y la opción elegida. */
  decisiones: Record<string, string>;
  acciones: number;
  ultimaEscena: string;
  /** La música que sonaba al explorar cada sitio, por «escena@Jjornada» (null: silencio). */
  musica: Map<string, Set<string | null>>;
  /** Las pistas pedidas con # musica: desde ink (y dónde), en orden. */
  cues: { pista: string; escena: string; jornada: number; knot: string }[];
  /** El objetivo de los apuntes que se veía al explorar cada sitio, por «escena@Jjornada». */
  objetivos: Map<string, Set<string>>;
}

/** Límites de la partida. */
export interface Limites {
  /** Acciones de exploración como máximo. */
  acciones: number;
  /** Acciones seguidas sin ver una línea nueva: atascado. */
  sinNovedad: number;
  /** Pasos de un solo diálogo antes de darlo por bucle. */
  pasosDialogo: number;
  /** Depuración: recibe cada acción, línea y elección. */
  traza?: (s: string) => void;
}

const LIMITES: Limites = { acciones: 5000, sinNovedad: 400, pasosDialogo: 4000 };

// ------------------------------------------------------------------ minijuegos

const ITEMS = items as Record<string, { mirar?: string }>;
const ENTRADAS = (diario as { entradas: { id: string; frases: { texto: string; si?: string }[] }[] }).entradas;
const RESERVA = [{ nombre: 'MARSH, J.' }, { nombre: 'DOYLE, P.' }, { nombre: 'QUILL, R.' }, { nombre: 'ASH, T.', chico: true }, { nombre: 'FENN, B.' }];
const ESCONDITES = ['cartel', 'colchon', 'cajon', 'hornillo'];

interface Resultado { resultado: string; datos?: Record<string, string | number | boolean> }

/**
 * Lo que devolvería cada minijuego (src/scenes/minijuegos/*), al azar según el perfil.
 * Devuelve null si el minijuego no devuelve nada que la historia lea.
 */
function jugarMinijuego(tipo: string, params: Record<string, string>, b: NarrativeBridge, rng: Rng, p: Perfil): Resultado | null {
  const exito = () => rng() < p.maña;
  const v = (n: string) => b.get(n);
  switch (tipo) {
    case 'cf': {
      const resultado = ['perfecto', 'aceptable', 'fallo'][ponderado(rng, p.cf)];
      const malo = resultado === 'fallo' ? 0.7 : resultado === 'aceptable' ? 0.3 : 0.05;
      return {
        resultado,
        datos: {
          transicion: rng() < malo ? 'fallo' : 'ok', amory: rng() < 0.4 ? 'visto' : 'no',
          bh: rng() < malo / 2 ? entre(rng, 1, 2) : 0, pancartas: entre(rng, 0, 8),
        },
      };
    }
    case 'dp': return { resultado: rng() < p.recordar ? 'recordar' : 'aceptar' };
    case 'ficha': {
      const apellido = elegir(rng, ['Reyes', 'Hale', 'Moss', 'Lark']);
      return { resultado: 'firmada', datos: { nombre: elegir(rng, ['Ada', 'Tom', 'Eli', 'Ruth']), apellido, genero: rng() < 0.5 ? 'm' : 'f', num: `${entre(rng, 1000, 9999)} 0${apellido[0]}` } };
    }
    case 'diario': {
      const leer = (n: string) => b.get(n);
      const disponibles = ENTRADAS.filter((e) => leer(e.id) === true && leer(`${e.id}_escrita`) !== true);
      if (!disponibles.length || rng() < 0.1) return { resultado: '' };
      const e = elegir(rng, disponibles);
      const frases = e.frases.filter((f) => cumple(f.si, leer));
      if (!frases.length) return { resultado: '' };
      return { resultado: elegir(rng, frases).texto, datos: { entrada: e.id } };
    }
    case 'parte': {
      const verbo = elegir(rng, ['avanzado', 'aplastado al enemigo', 'resistido']);
      return {
        resultado: 'enviado',
        datos: { verbo, km: elegir(rng, ['4', '12', '30']), prisioneros: elegir(rng, ['800', '3.000', '12.000']), bajas: elegir(rng, ['2.000', '9.000', '40.000']), tibias: verbo === 'aplastado al enemigo' ? 0 : 1 },
      };
    }
    case 'impactos': {
      const lamina = rng() < 0.5 ? 'si' : 'no';
      return { resultado: 'hecho', datos: { lamina, compas: rng() < 0.5 ? 'si' : 'no', fallos: entre(rng, 0, 3), lamina_puesta: lamina === 'si' && rng() < 0.5 ? 'si' : 'no' } };
    }
    case 'pancarta': return { resultado: exito() ? 'bien' : 'mal', datos: { cobertura: entre(rng, 40, 100) } };
    case 'frente': return { resultado: 'hecho' };
    case 'sammy': return { resultado: exito() ? elegir(rng, ['correr', 'cubierto']) : elegir(rng, ['paralizado', 'cubierto']) };
    case 'esconder': {
      const inv = b.list('inventario');
      const datos: Record<string, string> = {};
      for (const [item, clave] of [['diario', 'diario'], ['parte_alterado', 'parte'], ['foto_ivy_restaurada', 'foto']]) {
        if (inv.includes(item)) datos[clave] = elegir(rng, ESCONDITES);
      }
      return { resultado: 'hecho', datos };
    }
    case 'palanca': { const chirridos = exito() ? 0 : entre(rng, 1, 3); return { resultado: chirridos ? 'chirrido' : 'limpio', datos: { chirridos } }; }
    case 'llaves': return { resultado: exito() || rng() < 0.5 ? 'ok' : 'tiempo', datos: { fallos: entre(rng, 0, 4) } };
    case 'combinacion': return { resultado: exito() ? 'abierta' : elegir(rng, ['fallo', 'tiempo', 'abierta']) };
    case 'copiar': { const lineas = entre(rng, exito() ? 3 : 0, 6); return { resultado: String(lineas), datos: { lineas, firma: lineas > 0 && rng() < 0.5 } }; }
    case 'lista': {
      const r = elegir(rng, ['cambio', 'nada', 'tachado', 'rabia']);
      if (r !== 'cambio') return { resultado: r };
      const s = elegir(rng, RESERVA);
      return { resultado: r, datos: { sustituto: s.nombre, chico: !!s.chico } };
    }
    case 'rectificacion': return { resultado: exito() ? 'completa' : 'incompleta' };
    case 'tuneles': return { resultado: 'ruta', datos: { deducido: exito() ? 'si' : 'no', derrumbes: entre(rng, 0, 3) } };
    case 'dial': return { resultado: elegir(rng, ['nueve', 'once', 'silencio']), datos: { nivel: entre(rng, 20, 100) } };
    case 'h101': {
      const posibles = params.opciones ? params.opciones.split('/')
        : ['nell', ...(Number(v('dot_confianza')) >= 1 ? ['dot'] : []), ...(v('brooke_revelada') ? ['brooke'] : []), ...(v('len_salvado') ? ['len'] : []), 'ivy'];
      const ids = posibles.filter((i) => i !== params.sin);
      return { resultado: elegir(rng, ids) };
    }
    case 'resistencia': return { resultado: exito() ? 'aguanto' : 'delatado' };
    case 'capitulo': {
      // el Capítulo II calcula esto él mismo (CapituloScene)
      b.set('metralla_cierre', !!v('sammy_intento') || b.list('inventario').includes('metralla_brillante'));
      const corregida = rng() < 0.5 ? 'si' : 'no';
      return {
        resultado: 'escrito',
        datos: { ivy_corregida: corregida, apertura: 'apertura', mov1: 'uno', mov2: 'dos', mov3: 'tres', mov4: 'cuatro', cierre: 'cierre', texto: 'texto', voces: entre(rng, 0, 4) },
      };
    }
    case 'cascotes': return { resultado: 'hecho' };
    case 'declaracion': return { resultado: 'firmada' };
    case 'epilogo': case 'creditos': return { resultado: 'fin' };
    case 'cf_auto': return { resultado: 'automatico' };
    default: return null;   // documento, comparar, libro…: solo se leen
  }
}

/** Minijuegos que conoce UIScene (los demás se saltan con un aviso). */
const MINIJUEGOS = new Set(['cf', 'dp', 'cascotes', 'ficha', 'parte', 'frente', 'pancarta', 'impactos', 'sammy', 'diario', 'comparar', 'esconder',
  'documento', 'libro', 'copiar', 'palanca', 'llaves', 'combinacion', 'rectificacion', 'lista', 'tuneles', 'capitulo', 'dial', 'h101',
  'declaracion', 'resistencia', 'epilogo', 'creditos', 'cf_auto']);

/** El juego se ha quedado colgado (p. ej. una excepción en mitad de una acción): la partida no puede seguir. */
class Colgado extends Error {}

// ------------------------------------------------------------------ acciones de exploración

/** Lo que puede hacer el jugador al explorar. clave: «escena/hotspot» + modo (:p principal, :m mirar, @ zona, # escondite, +objeto). */
interface Accion {
  clave: string;
  peso: number;
  tipo: 'ruta' | 'esconderse' | 'esperar' | 'inventario';
  ruta?: string;
}

// ------------------------------------------------------------------ la partida

/**
 * Juega una partida completa desde «Nueva partida».
 * `b` puede reutilizarse entre partidas (se reinicia aquí); crear la Story una sola vez ahorra mucho tiempo.
 */
export function jugarPartida(json: string | NarrativeBridge, locs: Record<string, LocationData>, rng: Rng, perfil: Perfil, limites: Partial<Limites> = {}): Partida {
  const lim = { ...LIMITES, ...limites };
  const b = typeof json === 'string' ? new NarrativeBridge(json) : json;
  const vars = b.story.variablesState;
  const existe = (n: string) => vars.GlobalVariableExistsWithName(n);
  const leer = (n: string) => b.get(n);
  const num = (n: string) => Number(b.get(n)) || 0;

  const p: Partida = {
    perfil: perfil.nombre, resultado: 'limite', jornadas: {}, maxDuda: 0, maxSospecha: 0, arrestos: 0,
    errores: [], avisos: [], fueraDeRango: [], lineas: new Set(), origen: {}, decisiones: {}, acciones: 0, ultimaEscena: '',
    musica: new Map(), cues: [], objetivos: new Map(),
  };

  // estado del motor (LocationScene + mision)
  let loc!: LocationData;
  let pendiente: { escena?: string; spawn?: string } = {};
  /** # musica: de ink: manda sobre la del mapa hasta cambiar de escena (LocationScene.musicaForzada). */
  let musicaForzada: string | null | undefined;
  let finalPendiente = false;
  let terminado = false;
  let arrestando = false;
  let oculto = false;
  let reloj: null | { transcurrido: number; limite: number; agotar: string; agotado: boolean; escena: string } = null;
  let ultimoKnot = '';
  let jornada = -1;
  let retroceso = '';
  let hechas = new Map<string, number>();
  let sinNovedad = 0;
  const usadas = new Map<string, number>();   // textos de opciones ya elegidos (para no girar en bucles)

  const traza = lim.traza ?? (() => {});
  const avisar = (s: string) => { if (!p.avisos.includes(s)) p.avisos.push(s); };
  const fallar = (s: string) => { if (!p.errores.includes(s)) p.errores.push(s); };

  b.reset();
  /** Dónde iba ink (knot.stitch) cuando pasó algo: más preciso que la ruta con la que empezó el diálogo. */
  let punto = '';
  const rutaInk = () => {
    const st = b.story.state;
    const ruta = st.currentPathString ?? st.previousPathString ?? '';
    return ruta.split('.').filter((x) => !/^\d+$/.test(x) && !x.startsWith('c-') && !x.startsWith('g-')).slice(0, 2).join('.');
  };
  const donde = () => {
    const aqui = rutaInk() || punto;
    return aqui && !aqui.startsWith(ultimoKnot) ? `${ultimoKnot} → ${aqui}` : ultimoKnot;
  };
  b.story.onError = (msg: string, tipo: number) => { traza(`  !! ${msg}`); return tipo === 1 ? avisar(`[ink aviso] ${msg}`) : fallar(`[ink] ${msg} (${donde()})`); };
  /** Escribir en ink como el motor: si la variable no existe, inkjs lanza (y en el juego el diálogo se queda colgado). */
  const escribir = (n: string, valor: unknown) => {
    try { b.set(n, valor); } catch (e) { fallar(`[motor] ${(e as Error).message} (${donde()})`); }
  };
  /** Lo que escribe UIScene.fijar: solo variables que ink declara, con su tipo. */
  const escribirResultado = (n: string, valor: unknown) => {
    if (!existe(n)) return;
    const actual = b.get(n);
    if (typeof actual === 'number') b.set(n, Number(valor) || 0);
    else if (typeof actual === 'boolean') b.set(n, valor === true || valor === 'si' || valor === 'true');
    else b.set(n, String(valor));
  };

  // ---------------------------------------------------------------- vigilancia de variables
  let antes: Instantanea = { duda: 0, sospecha: 0 };
  const vigilar = (contexto: string) => {
    const d = num('duda'), s = num('sospecha'), j = num('jornada');
    if (d !== antes.duda || s !== antes.sospecha) {
      const k = `J${j} ${punto || ultimoKnot}`;
      const o = (p.origen[k] ??= { duda: 0, sospecha: 0 });
      o.duda += d - antes.duda; o.sospecha += s - antes.sospecha;
      antes = { duda: d, sospecha: s };
    }
    if (d > p.maxDuda) p.maxDuda = d;
    if (s > p.maxSospecha) p.maxSospecha = s;
    if (d < 0 || d > 100) p.fueraDeRango.push(`duda=${d} en ${contexto} (J${j})`);
    if (s < 0 || s > 100) p.fueraDeRango.push(`sospecha=${s} en ${contexto} (J${j})`);
    if (j !== jornada) {
      // la jornada solo avanza: si retrocede, la historia ha caído en una rama que no es suya
      if (j < jornada && !retroceso) retroceso = `la jornada retrocede de ${jornada} a ${j} en ${donde()} (escena ${loc.id})`;
      jornada = j;
      if (!(j in p.jornadas)) p.jornadas[j] = { duda: d, sospecha: s };
      hechas = new Map();   // jornada nueva: todo vuelve a ser nuevo
    }
  };

  // ---------------------------------------------------------------- comandos (LocationScene.comando)
  let simulando = false;
  const quitar = b.on('command', (t: Tag) => {
    if (simulando) return;
    if (t.key === 'escena') {
      if (t.value === loc.id) return;
      if (locs[t.value]) pendiente.escena = t.value;
      else avisar(`escena inexistente "${t.value}" (${ultimoKnot})`);
    } else if (t.key === 'pos') {
      if (pendiente.escena) pendiente.spawn = t.value;
    } else if (t.key === 'musica') {
      musicaForzada = t.value && t.value !== 'silencio' ? t.value : null;
      p.cues.push({ pista: t.value, escena: loc.id, jornada: num('jornada'), knot: ultimoKnot });
    } else if (t.key === 'final') {
      finalPendiente = true;
      if (t.value && t.value !== 'demo') p.resultado = t.value;
    } else if (t.key === 'reloj') {
      const q = t.params;
      if (t.value === 'parar') reloj = null;
      else if (q.inicio) reloj = { transcurrido: 0, limite: Number(q.limite) || 240, agotar: q.agotar ?? '', agotado: false, escena: loc.id };
      else if (reloj && q.mas) { reloj.limite = reloj.transcurrido + Number(q.mas); reloj.agotado = false; }
      else if (reloj && q.menos) reloj.transcurrido += Number(q.menos);
    }
  });

  // ---------------------------------------------------------------- diálogo (UIScene.iniciar/avanzar)
  /** Cuánto sube la Sospecha cada opción, jugándola en seco hasta la siguiente elección (sin minijuegos ni comandos). */
  const preverSospecha = (choices: ChoiceOption[]): number[] => {
    const estado = b.story.state.ToJson();
    const onError = b.story.onError;
    b.story.onError = () => {};
    simulando = true;
    try {
      return choices.map((c) => {
        b.story.state.LoadJson(estado);
        const s0 = num('sospecha');
        try {
          b.choose(c.index);
          for (let i = 0; i < 300; i++) { const t = b.next().type; if (t === 'choices' || t === 'end') break; }
        } catch { /* la rama falla: que decida el azar */ }
        return num('sospecha') - s0;
      });
    } finally {
      b.story.state.LoadJson(estado);
      b.story.onError = onError;
      simulando = false;
    }
  };

  const elegirOpcion = (choices: ChoiceOption[]): ChoiceOption => {
    if (choices.length === 1) return choices[0];
    if (rng() < perfil.primera) return choices[0];
    const subidas = perfil.prever ? preverSospecha(choices) : null;
    const pesos = choices.map((c, i) => {
      let w = 1 / (1 + (usadas.get(c.text) ?? 0)) ** 2;
      for (const [re, k] of perfil.preferir ?? []) if (re.test(c.text)) w *= k;
      if (subidas) w *= Math.exp((-perfil.prever! * subidas[i]) / 10);
      return w;
    });
    return choices[ponderado(rng, pesos)];
  };

  const acciones = (lista: Tag[]) => {
    for (const a of lista) {
      if (!['cf', 'dp', 'minijuego', 'documento', 'comparar'].includes(a.key)) continue;   // sfx, fx, esperar, recuerdo, viñeta…
      const tipo = a.key === 'minijuego' ? a.value.split(',')[0].trim() : a.key;
      if (!MINIJUEGOS.has(tipo)) { avisar(`minijuego desconocido "${tipo}" (${ultimoKnot})`); continue; }
      const params = Object.keys(a.params).length || a.key === 'minijuego' ? a.params : { id: a.value };
      const r = jugarMinijuego(tipo, params, b, rng, perfil);
      if (!r) continue;
      try {
        aplicarResultado(tipo, params, r);
      } catch (e) {
        // UIScene.ejecutarAcciones es asíncrona: la excepción deja enAccion = true y el diálogo no avanza nunca
        const motivo = `excepción en UIScene.aplicarResultado (${tipo}): ${(e as Error).message}`;
        fallar(`[motor] ${motivo} (${donde()})`);
        throw new Colgado(motivo);
      }
    }
  };

  /** UIScene.aplicarResultado, tal cual. */
  const aplicarResultado = (tipo: string, params: Record<string, string>, r: Resultado) => {
    if (tipo === 'cf') {
      const id = (params.id ?? '').toLowerCase().replace(/^cf-/, '').replace(/-/g, '_');
      escribirResultado(`cf_${id}`, r.resultado);
      for (const [k, v] of Object.entries(r.datos ?? {})) if (existe(`cf_${id}_${k}`)) escribirResultado(`cf_${id}_${k}`, String(v));
    } else if (tipo === 'dp') {
      escribirResultado((params.id ?? '').toLowerCase().replace(/-/g, '_'), r.resultado);
    } else if (tipo === 'ficha' && r.datos) {
      for (const k of ['nombre', 'apellido', 'num']) escribirResultado(k, String(r.datos[k]));
      b.call('fijar_genero', String(r.datos.genero));
    } else if (tipo === 'diario') {
      if (r.resultado && r.datos?.entrada) {
        escribirResultado(`${r.datos.entrada}_escrita`, true);
        if (existe(`${r.datos.entrada}_frase`)) escribirResultado(`${r.datos.entrada}_frase`, r.resultado);
        escribirResultado('diario_ultima', r.resultado);
        escribirResultado('diario_texto', `${leer('diario_texto') || ''}¶${r.resultado}`);
        escribirResultado('diario_entradas', num('diario_entradas') + 1);
      }
    } else {
      if (params.resultado) escribirResultado(params.resultado, r.resultado);
      if (params.vars && r.datos) for (const [k, v] of Object.entries(r.datos)) escribirResultado(`${params.vars}_${k}`, v);
    }
  };

  let profundidad = 0;
  const dialogo = (ruta?: string) => {
    if (terminado) return;
    if (++profundidad > 50) { fallar(`diálogos encadenados sin fin (${ruta})`); terminado = true; p.resultado = 'error'; return; }
    try {
      if (ruta) { b.goTo(ruta); ultimoKnot = ruta; punto = ''; }
      traza(`▶ ${ruta ?? '(flujo principal)'} [${loc.id} J${num('jornada')} D${num('duda')} S${num('sospecha')}]`);
      for (let i = 0; ; i++) {
        if (i > lim.pasosDialogo) { avisar(`diálogo sin fin en ${ultimoKnot}`); break; }
        const paso = b.next();
        punto = rutaInk() || punto;
        vigilar(ultimoKnot);
        if (paso.type === 'line' || paso.type === 'accion') {
          const id = paso.line?.id;
          if (id && !p.lineas.has(id)) { p.lineas.add(id); sinNovedad = 0; }
          traza(`  ${paso.line?.speaker ?? paso.line?.kind ?? ''}: ${paso.line?.text ?? ''}${paso.type === 'accion' ? ` {${paso.acciones.map((t) => `${t.key}:${t.value}`).join(' ')}}` : ''}`);
          if (paso.type === 'accion') { acciones(paso.acciones); vigilar(ultimoKnot); }
        } else if (paso.type === 'choices') {
          const c = elegirOpcion(paso.choices);
          traza(`  ? ${paso.choices.map((o) => o.text).join(' | ')} → ${c.text}`);
          usadas.set(c.text, (usadas.get(c.text) ?? 0) + 1);
          const d = c.tags.find((t) => t.key === 'decision');
          if (d) p.decisiones[d.value] = c.text;
          else for (const o of paso.choices) { const x = o.tags.find((t) => t.key === 'decision'); if (x) p.decisiones[x.value] = c.text; }
          b.choose(c.index);
        } else break;
      }
    } catch (e) {
      if (e instanceof Colgado) throw e;
      fallar(`[excepción] ${(e as Error).message} (${donde()})`);
      terminado = true; p.resultado = 'error';
      return;
    }
    fin();
    profundidad--;
  };

  /** LocationScene: al terminar un diálogo. */
  const fin = () => {
    // un solo arresto: dentro de un final ya no se arresta a nadie (LocationScene)
    const yaDetenido = String(leer('final_en_curso') ?? '') !== '';
    if (!arrestando && !finalPendiente && !yaDetenido && num('sospecha') >= 100 && b.hasPath('arresto')) {
      arrestando = true;
      pendiente = {};
      p.arrestos++;
      if (p.arresto === undefined) p.arresto = num('jornada');
      dialogo('arresto');
      return;
    }
    autoguardar();
  };

  const autoguardar = () => {
    if (finalPendiente) { terminado = true; return; }
    if (pendiente.escena) entrar(pendiente.escena);
  };

  /** LocationScene.create (sin cargar partida). */
  const entrar = (escena: string, cargado = false) => {
    pendiente = {};
    loc = locs[escena];
    p.ultimaEscena = escena;
    musicaForzada = undefined;
    arrestando = false; oculto = false;
    if (existe('escena_actual')) escribir('escena_actual', loc.id);
    if (!cargado && loc.alEntrar && b.hasPath(loc.alEntrar)) dialogo(loc.alEntrar);
  };

  // ---------------------------------------------------------------- exploración
  const visibles = (): Hotspot[] => {
    const conAccion = (h: Hotspot) => !!(h.mirar || h.usar || h.hablar || h.escondite);
    const hs = loc.hotspots.filter((h) => conAccion(h) && cumple(h.condicion, leer));
    for (const n of loc.npcs) if (cumple(n.hotspot.condicion, leer) && conAccion(n.hotspot)) hs.push(n.hotspot);
    return hs;
  };

  const posibles = (): Accion[] => {
    const lista: Accion[] = [];
    const inv = b.list('inventario');
    // un silbido: quedan segundos (no los minutos de una misión) y lo único sensato es esconderse y esperar
    const apuro = !!reloj && !reloj.agotado && reloj.limite - reloj.transcurrido <= 15;
    const add = (a: Omit<Accion, 'peso'>, peso: number) => {
      if (a.ruta && !b.hasPath(a.ruta)) { avisar(`knot inexistente "${a.ruta}" en ${loc.id}`); return; }
      // con el reloj en marcha, esconderse y esperar no se gastan: se repiten cuantas veces haga falta
      const urgente = apuro && (a.tipo === 'esperar' || a.tipo === 'esconderse');
      if (perfil.evitar?.some((e) => e.accion.test(a.clave) && cumple(e.si, leer))) peso *= 0.01;
      lista.push({ ...a, peso: peso * (urgente ? 1 : perfil.repetir ** (hechas.get(a.clave) ?? 0)) });
    };
    for (const h of visibles()) {
      const id = `${loc.id}/${h.name}`;
      const principal = h.hablar ?? h.usar ?? h.mirar;
      if (h.auto) { if (principal) add({ clave: `${id}@`, tipo: 'ruta', ruta: principal }, 1); continue; }
      // con el reloj corriendo, quien sabe dónde esconderse corre hacia ahí
      if (h.escondite) add({ clave: `${id}#`, tipo: 'esconderse' }, oculto ? 0.2 : apuro ? 30 * perfil.maña : 0.6);
      else if (principal) add({ clave: `${id}:p`, tipo: 'ruta', ruta: principal }, principal === h.mirar ? perfil.mirar : 1);
      if (h.mirar && h.mirar !== principal) add({ clave: `${id}:m`, tipo: 'ruta', ruta: h.mirar }, perfil.mirar * 0.5);
      for (const [item, ruta] of Object.entries(h.con ?? {})) if (inv.includes(item)) add({ clave: `${id}+${item}`, tipo: 'ruta', ruta }, 1);
    }
    for (const item of inv) {
      const ruta = ITEMS[item]?.mirar;
      if (ruta) add({ clave: `inv/${item}`, tipo: 'inventario', ruta }, perfil.mirar * 0.2);
    }
    // quedarse quieto (escondido, esperar a que pase; o dejar correr el reloj)
    add({ clave: `${loc.id}/esperar`, tipo: 'esperar' }, apuro && oculto ? 100 * perfil.maña : reloj ? 0.5 : 0.05);
    return lista;
  };

  /** Lo que pasa mientras se camina hacia el punto: el reloj, los conos, los choques a oscuras. Devuelve si interrumpe. */
  const caminar = (segundos: number, quieto: boolean): boolean => {
    for (const n of loc.npcs) if (n.persigue?.variable && existe(n.persigue.variable)) escribir(n.persigue.variable, entre(rng, 20, 400) * (perfil.maña < 0.5 ? 0.6 : 1));
    if (loc.conosRotativos?.variable && existe(loc.conosRotativos.variable)) escribir(loc.conosRotativos.variable, rng() < 0.5);
    if (reloj && !reloj.agotado) {
      reloj.transcurrido += segundos;
      if (reloj.transcurrido >= reloj.limite) {
        reloj.agotado = true;
        // un reloj de misión que se agota lejos de su misión: nadie lo paró al salir
        // (salvo que sea la escena de su propio «agotar»: la misión del Minimor empieza en la recepción y sigue en el archivo)
        if (reloj.escena !== loc.id && !reloj.agotar.startsWith(`${loc.id}.`)) avisar(`[motor] el reloj de ${reloj.escena} (${reloj.agotar}) se agota en ${loc.id}`);
        if (reloj.agotar && b.hasPath(reloj.agotar)) { dialogo(reloj.agotar); return true; }
      }
    }
    if (!quieto && !oculto && loc.sigilo && cumple(loc.sigilo.condicion, leer) && rng() < perfil.visto) {
      if (b.hasPath(loc.sigilo.alSerVisto)) { dialogo(loc.sigilo.alSerVisto); return true; }
    }
    if (!quieto && loc.oscuro && loc.alChocar && rng() < perfil.choque) {
      if (existe('choques')) escribir('choques', num('choques') + 1);
      if (b.hasPath(loc.alChocar)) { dialogo(loc.alChocar); return true; }
    }
    return false;
  };

  const marcarEscondido = (v: boolean) => { oculto = v; if (existe('escondido')) escribir('escondido', v); };

  // ---------------------------------------------------------------- la partida
  try {
    entrar('stepney', true);   // MenuScene: nueva partida (cargado: no se ejecuta al_entrar)
    dialogo();                 // el flujo principal (prólogo)
    while (!terminado) {
      if (p.acciones >= lim.acciones) { p.resultado = 'limite'; break; }
      if (retroceso) {
        p.resultado = 'atascado';
        p.atasco = { escena: loc.id, jornada: num('jornada'), knot: ultimoKnot, motivo: retroceso };
        break;
      }
      if (sinNovedad >= lim.sinNovedad) {
        p.resultado = 'atascado';
        p.atasco = { escena: loc.id, jornada: num('jornada'), knot: ultimoKnot, motivo: `${lim.sinNovedad} acciones sin nada nuevo` };
        break;
      }
      const lista = posibles();
      if (!lista.length) {
        p.resultado = 'atascado';
        p.atasco = { escena: loc.id, jornada: num('jornada'), knot: ultimoKnot, motivo: 'no hay nada que hacer' };
        break;
      }
      // lo que suena mientras se explora (LocationScene.actualizarVisibilidad)
      const clave = `${loc.id}@J${num('jornada')}`;
      if (!p.musica.has(clave)) p.musica.set(clave, new Set());
      p.musica.get(clave)!.add(musicaForzada !== undefined ? musicaForzada : musicaDe(loc, leer));
      if (!p.objetivos.has(clave)) p.objetivos.set(clave, new Set());
      p.objetivos.get(clave)!.add(objetivo(apuntes as Apuntes, leer));
      const a = lista[ponderado(rng, lista.map((x) => x.peso))];
      hechas.set(a.clave, (hechas.get(a.clave) ?? 0) + 1);
      p.acciones++; sinNovedad++;
      traza(`· ${a.tipo} ${a.clave}`);
      if (a.tipo === 'esperar') { caminar(entre(rng, 10, 30), true); continue; }
      if (a.tipo === 'esconderse') {
        if (oculto) { marcarEscondido(false); continue; }
        if (caminar(entre(rng, 1, perfil.maña < 0.5 ? 6 : 3), false)) continue;
        marcarEscondido(true);
        continue;
      }
      // mirar el inventario no mueve ni gasta tiempo de reloj; moverse saca del escondite
      if (a.tipo === 'inventario') { dialogo(a.ruta); continue; }
      if (oculto) marcarEscondido(false);
      if (caminar(entre(rng, 2, 12), false)) continue;
      dialogo(a.ruta);
    }
  } catch (e) {
    if (!(e instanceof Colgado)) throw e;
    p.resultado = 'atascado';
    p.atasco = { escena: loc.id, jornada: num('jornada'), knot: donde(), motivo: e.message };
  } finally {
    quitar();
  }
  return p;
}
