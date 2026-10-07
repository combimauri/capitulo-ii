/**
 * Las partituras de la música (diseño técnico §12). Cada pista es una partitura corta en bucle: notas con su
 * pulso, su duración, su voz y su fuerza. El motor que las toca está en Musica.ts.
 * Todas las melodías son originales salvo «Naranjas y limones» (tradicional, dominio público).
 * Cada pista declara la emoción que busca; las pruebas comprueban que la partitura la sostiene
 * (tonalidad, tempo, registro, disonancia) y que suena a un volumen parecido al resto.
 */

export type Voz = 'piano' | 'piano_limpio' | 'tarareo' | 'bajo' | 'acorde'
  | 'trompeta' | 'metal' | 'tuba' | 'redoble' | 'bombo' | 'timbal'      // la banda del Partido
  | 'caja' | 'cuerdas' | 'tremolo' | 'pizzicato' | 'lamento' | 'coro'   // caja de música, orquesta
  | 'organo' | 'campana'                                                // la cripta de San Clemente
  | 'tecla' | 'timbre' | 'carro'                                        // la máquina de escribir como ritmo
  | 'latido' | 'pulso' | 'dron' | 'tictac' | 'roce';                    // la tensión y el miedo

/** Lo que el jugador debe sentir con cada pista. */
export type Emocion = 'misterio' | 'rutina' | 'duda' | 'tension' | 'miedo' | 'terror' | 'tristeza' | 'rabia'
  | 'frustracion' | 'alegria' | 'calidez' | 'esperanza' | 'fanatismo' | 'vacio' | 'nostalgia';

/** `v`: la fuerza de la nota (1 = normal). */
export interface Nota { b: number; d: number; n: string; voz: Voz; v?: number }

export interface Pista {
  bpm: number;
  /** Longitud del bucle en pulsos (incluye el silencio final, si lo hay). */
  pulsos: number;
  notas: Nota[];
  volumen: number;
  emocion: Emocion;
  /** Corte del filtro de la pista: menos agudos = más lejos. */
  corte?: number;
  /** Murmullo de gente y algún vaso: el pub. */
  murmullo?: number;
  /** Altavoz viejo: saturado y sin graves ni agudos (la calle, la telepantalla). */
  altavoz?: boolean;
  /** Desafinación de cada nota (0 = perfectamente afinado). */
  desafino?: number;
  /** Cuánta sala (reverberación, 0..1) y cuánto dura su cola en segundos. */
  sala?: number;
  cola?: number;
  /** Paneo propio de alguna voz (si no, el de Musica.ts). */
  paneo?: Partial<Record<Voz, number>>;
  /** Segundos de fundido al entrar y al salir (1,4 por defecto). */
  entrada?: number;
  salida?: number;
  /** Sin imprecisión humana (una máquina, un altavoz). */
  rigida?: boolean;
  /** Música que suena dentro de la escena (un piano, un altavoz): para las pruebas, no es «banda sonora». */
  diegetica?: boolean;
}

/**
 * "A4:2 G4:1 | F4:2 A4:1:.6" → notas seguidas desde el pulso `desde` ("-" es silencio; el tercer número,
 * si lo hay, es la fuerza). `fuerza` multiplica la de todas. Un acorde se escribe con «+»: "C4+E4+G4:2".
 */
export function melodia(texto: string, voz: Voz, desde = 0, fuerza = 1): Nota[] {
  const notas: Nota[] = [];
  let b = desde;
  for (const tok of texto.replace(/\|/g, ' ').split(/\s+/).filter(Boolean)) {
    const [n, d, v] = tok.split(':');
    if (n !== '-') for (const x of n.split('+')) notas.push({ b, d: Number(d), n: x, voz, v: (v ? Number(v) : 1) * fuerza });
    b += Number(d);
  }
  return notas;
}

/** Acompañamiento: [raíz, notas del acorde] por compás → bajo en el primer pulso y acorde en los demás. */
function acompanamiento(compases: [string, string[]][], porCompas: number, estilo: 'vals' | 'paseo'): Nota[] {
  const notas: Nota[] = [];
  compases.forEach(([raiz, acorde], i) => {
    const b0 = i * porCompas;
    if (estilo === 'vals') {
      notas.push({ b: b0, d: 1, n: raiz, voz: 'bajo' });
      for (const n of acorde) { notas.push({ b: b0 + 1, d: 0.8, n, voz: 'acorde' }, { b: b0 + 2, d: 0.8, n, voz: 'acorde' }); }
    } else {
      // stride de taberna: raíz, acorde, quinta, acorde
      const quinta = transponer(raiz, 7);
      notas.push({ b: b0, d: 1, n: raiz, voz: 'bajo' }, { b: b0 + 2, d: 1, n: quinta, voz: 'bajo' });
      for (const n of acorde) { notas.push({ b: b0 + 1, d: 0.6, n, voz: 'acorde' }, { b: b0 + 3, d: 0.6, n, voz: 'acorde' }); }
    }
  });
  return notas;
}

const NOMBRES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

export function midi(n: string): number {
  const m = /^([A-G])(#|b)?(\d)$/.exec(n);
  if (!m) return 60;
  const base = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[m[1] as 'C'] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
  return 12 * (Number(m[3]) + 1) + base;
}

export function transponer(n: string, semitonos: number): string {
  const x = midi(n) + semitonos;
  return `${NOMBRES[((x % 12) + 12) % 12]}${Math.floor(x / 12) - 1}`;
}

export const frecuencia = (n: string) => 440 * 2 ** ((midi(n) - 69) / 12);

// ---------------------------------------------------------------- la canción de Dot (fa mayor, 3/4)
// Dieciséis compases y dos de respiro: alguien la tararea mientras hace otra cosa.
const DOT = [
  'A4:2 G4:1 | F4:2 A4:1 | C5:2 D5:1 | C5:3 | Bb4:2 A4:1 | G4:2 Bb4:1 | A4:1 G4:1 F4:1 | G4:3',
  'A4:2 G4:1 | F4:2 A4:1 | C5:2 F5:1 | E5:2 D5:1 | C5:2 A4:1 | Bb4:2 G4:1 | A4:1 G4:1 E4:1 | F4:3 | -:6',
].join(' | ');

// ---------------------------------------------------------------- La Campana (do mayor, 4/4, piano de taberna)
const CAMPANA = [
  'E5:1 E5:.5 D5:.5 C5:1 G4:1 | A4:1 C5:1 E5:2 | D5:1 D5:.5 C5:.5 B4:1 G4:1 | D5:2 C5:1 B4:1',
  'E5:1 E5:.5 D5:.5 C5:1 G4:1 | A4:1 C5:1 F5:2 | E5:1 D5:1 G4:1 B4:1 | C5:3 -:1',
  'G5:1 G5:.5 F5:.5 E5:1 C5:1 | F5:1 E5:1 D5:2 | F5:1 F5:.5 E5:.5 D5:1 B4:1 | E5:1 D5:1 C5:2',
  'A4:1 B4:1 C5:1 D5:1 | E5:1 F5:1 E5:2 | D5:1 E5:1 F5:1 D5:1 | C5:3 -:1',
].join(' | ');
const C: [string, string[]] = ['C3', ['E4', 'G4', 'C5']];
const F: [string, string[]] = ['F2', ['A3', 'C4', 'F4']];
const G7: [string, string[]] = ['G2', ['B3', 'D4', 'F4']];
const Dm: [string, string[]] = ['D3', ['D4', 'F4', 'A4']];

const VF: [string, string[]] = ['F2', ['A3', 'C4']];
const VBb: [string, string[]] = ['Bb2', ['Bb3', 'D4']];
const VC7: [string, string[]] = ['C3', ['Bb3', 'E4']];

/** Sube o baja de octava todas las notas de una melodía escrita. */
export const octava = (texto: string, n: number) => texto.replace(/([A-G][#b]?)(\d)/g, (_, nota, o) => `${nota}${Number(o) + n}`);

/** Un acorde sostenido por compás (cuerdas, colchón). */
function colchon(acordes: string[][], porCompas: number, voz: Voz = 'cuerdas'): Nota[] {
  return acordes.flatMap((notas, i) => notas.map((n) => ({ b: i * porCompas, d: porCompas, n, voz })));
}

/** Marcha: bombo en 1 y 3, caja en 2 y 4, y un redoble al final de cada frase de cuatro compases. */
function marcha(compases: number): Nota[] {
  const notas: Nota[] = [];
  for (let c = 0; c < compases; c++) {
    const b0 = c * 4;
    notas.push({ b: b0, d: 1, n: 'C2', voz: 'bombo' }, { b: b0 + 2, d: 1, n: 'C2', voz: 'bombo' });
    notas.push({ b: b0 + 1, d: 1, n: 'C4', voz: 'redoble' }, { b: b0 + 3, d: 1, n: 'C4', voz: 'redoble' });
    if (c % 4 === 3) for (const x of [3.25, 3.5, 3.75]) notas.push({ b: b0 + x, d: 0.25, n: 'C4', voz: 'redoble' });
  }
  return notas;
}

// ---------------------------------------------------------------- el himno del Partido (do mayor, 4/4, marcha). Original.
const HIMNO = [
  'G4:1.5 G4:.5 C5:1 E5:1 | G5:2 E5:1 C5:1 | D5:1.5 D5:.5 E5:1 F5:1 | E5:3 -:1',
  'G5:1.5 F5:.5 E5:1 D5:1 | C5:1 D5:1 E5:1 C5:1 | B4:1 A4:1 G4:1 B4:1 | D5:3 -:1',
  'G4:1.5 G4:.5 C5:1 E5:1 | G5:2 A5:1 G5:1 | F5:1 E5:1 D5:1 F5:1 | E5:3 -:1',
  'C6:1.5 B5:.5 A5:1 G5:1 | F5:1 E5:1 D5:1 E5:1 | D5:1.5 C5:.5 B4:1 D5:1 | C5:3 -:1',
].join(' | ');
const HC: [string, string[]] = ['C3', ['E4', 'G4']];
const HF: [string, string[]] = ['F2', ['A3', 'C4']];
const HG7: [string, string[]] = ['G2', ['B3', 'F4']];
const ACORDES_HIMNO = [HC, HC, HG7, HC, HC, HC, HG7, HG7, HC, HC, HG7, HC, HF, HC, HG7, HC];

function banda(): Nota[] {
  const notas: Nota[] = [...melodia(HIMNO, 'trompeta'), ...marcha(16)];
  ACORDES_HIMNO.forEach(([raiz, acorde], i) => {
    const b0 = i * 4;
    notas.push({ b: b0, d: 1, n: transponer(raiz, -12), voz: 'tuba' }, { b: b0 + 2, d: 1, n: transponer(raiz, -5), voz: 'tuba' });
    for (const n of acorde) notas.push({ b: b0 + 1, d: 0.6, n, voz: 'metal' }, { b: b0 + 3, d: 0.6, n, voz: 'metal' });
  });
  return notas;
}

// ---------------------------------------------------------------- Crane (fa mayor, lento): la música se vuelve cálida cuando habla. Original.
const CRANE = [
  'C5:2 A4:1 Bb4:1 | C5:3 F5:1 | E5:2 D5:1 C5:1 | D5:4',
  'Bb4:2 G4:1 A4:1 | Bb4:3 E5:1 | D5:2 C5:1 Bb4:1 | A4:4',
  'C5:2 A4:1 Bb4:1 | C5:3 A5:1 | G5:2 F5:1 E5:1 | F5:2 D5:2',
  'C5:2 Bb4:1 A4:1 | G4:2 C5:2 | A4:1 G4:1 F4:1 E4:1 | F4:4',
].join(' | ');
const ACORDES_CRANE = [
  ['F3', 'A3', 'C4'], ['F3', 'A3', 'C4'], ['C3', 'G3', 'E4'], ['Bb2', 'F3', 'D4'],
  ['G2', 'D3', 'Bb3'], ['C3', 'G3', 'E4'], ['C3', 'Bb3', 'E4'], ['F3', 'A3', 'C4'],
  ['F3', 'A3', 'C4'], ['F3', 'A3', 'C4'], ['C3', 'G3', 'E4'], ['D3', 'A3', 'F4'],
  ['F3', 'A3', 'C4'], ['C3', 'G3', 'E4'], ['C3', 'Bb3', 'E4'], ['F3', 'A3', 'C4'],
];

// ---------------------------------------------------------------- «Naranjas y limones» (tradicional, dominio público)
const NARANJAS = [
  'G5:1 E5:1 G5:1 E5:1 C5:1 D5:.5 E5:.5 F5:1 D5:1 G5:1 E5:1 C5:2',
  'G5:.5 G5:.5 E5:1 G5:1 E5:1 C5:1 D5:.5 E5:.5 F5:1 D5:1 G5:1 E5:1 C5:2',
].join(' ');
const IZQUIERDA_NARANJAS = melodia('C3:3 C3:3 G2:3 C3:3 C3:3 C3:3 G2:3 C3:3', 'bajo');

// ---------------------------------------------------------------- la máquina de escribir convertida en ritmo (Final E)
function maquina(): Nota[] {
  const patrones = ['x x - x x x - x', 'x x x - x - x x', 'x - x x x x - x', 'x x - x - x x -'];
  const notas: Nota[] = [];
  for (let c = 0; c < 8; c++) {
    patrones[c % 4].split(' ').forEach((p, i) => { if (p === 'x') notas.push({ b: c * 4 + i * 0.5, d: 0.5, n: 'C5', voz: 'tecla' }); });
    if (c % 4 === 3) {
      notas.push({ b: c * 4 + 3.5, d: 0.5, n: 'C7', voz: 'timbre' });
      notas.push({ b: c * 4 + 3.75, d: 0.25, n: 'C4', voz: 'carro' });
    }
  }
  return notas;
}

// ================================================================ la banda sonora completa (M7)
// Utilidades para escribir partituras más largas.

/** Las mismas notas con otra voz o fuerza. */
const con = (notas: Nota[], cambios: Partial<Nota>): Nota[] => notas.map((n) => ({ ...n, ...cambios }));
/** Multiplica las duraciones de una melodía escrita (a la mitad de velocidad: 2). */
const alargar = (texto: string, k: number) => texto.split(/\s+/).filter(Boolean)
  .map((t) => (t === '|' ? t : t.replace(/^([^:]+):([\d.]+)/, (_, n, d) => `${n}:${Number(d) * k}`))).join(' ');
/** Golpes sueltos (percusión, campanadas, pizzicatos) en los pulsos dados. */
const golpes = (pulsos: number[], n: string, voz: Voz, fuerza = 1, d = 0.5): Nota[] => pulsos.map((b) => ({ b, d, n, voz, v: fuerza }));
/** El tictac de un reloj: tic y tac alternos cada `cada` pulsos, de `desde` a `hasta`. */
function reloj(desde: number, hasta: number, cada = 1, fuerza = 0.5): Nota[] {
  const notas: Nota[] = [];
  for (let b = desde, i = 0; b < hasta - 1e-9; b += cada, i++) notas.push({ b, d: 0.1, n: i % 2 ? 'C4' : 'C5', voz: 'tictac', v: fuerza });
  return notas;
}
/**
 * Un dibujo que recorre los acordes: cada acorde dura `porAcorde` pulsos y el dibujo se repite dentro, a pasos de
 * `paso` pulsos. Un número es una nota del acorde (0 = la primera), «.» es silencio y «!» acentúa.
 */
function dibujo(acordes: string[][], porAcorde: number, patron: string, paso: number, voz: Voz, fuerza = 1, dur = paso): Nota[] {
  const pasos = patron.split(/\s+/).filter(Boolean);
  const notas: Nota[] = [];
  acordes.forEach((acorde, i) => {
    for (let k = 0; k * paso < porAcorde - 1e-9; k++) {
      const tok = pasos[k % pasos.length];
      if (tok === '.') continue;
      const b = i * porAcorde + k * paso;
      notas.push({ b, d: Math.min(dur, acordes.length * porAcorde - b), n: acorde[parseInt(tok, 10) % acorde.length], voz, v: fuerza * (tok.endsWith('!') ? 1.3 : 1) });
    }
  });
  return notas;
}
/** Vals al piano, suave: el bajo en la primera parte y el acorde, flojo, en la segunda y la tercera. */
function valsSuave(compases: [string, string[]][], fuerza = 1): Nota[] {
  return compases.flatMap(([bajo, acorde], i) => [
    { b: i * 3, d: 3, n: bajo, voz: 'piano_limpio' as Voz, v: 0.75 * fuerza },
    ...acorde.flatMap((n) => [1, 2].map((k) => ({ b: i * 3 + k, d: 1, n, voz: 'piano_limpio' as Voz, v: 0.32 * fuerza }))),
  ]);
}

// ---------------------------------------------------------------- Naranjas y limones en menor: el leitmotiv de Ivy
// La misma tonada con los grados de la escala menor (la menor): mi do mi | do la si-do | re si mi | do la.
const IVY_1 = 'E5:1 C5:1 E5:1 | C5:1 A4:1 B4:.5 C5:.5 | D5:1 B4:1 E5:1 | C5:1 A4:2';
const IVY_2 = 'E5:.5 E5:.5 C5:1 E5:1 | C5:1 A4:1 B4:.5 C5:.5 | D5:1 B4:1 E5:1 | C5:1 A4:2';

/** El menú: un reloj que se para, la caja de música de Ivy muy despacio y un clarinete que pregunta. */
function misterio(): Nota[] {
  const pad = colchon([
    ['A2', 'E3', 'C4'], ['A2', 'E3', 'C4'], ['F2', 'C3', 'A3'], ['F2', 'C3', 'A3'],
    ['D2', 'A2', 'F3'], ['D2', 'A2', 'F3'], ['E2', 'B2', 'G#3'], ['E2', 'D3', 'G#3'],
    ['A2', 'E3', 'C4'], ['A2', 'E3', 'C4'], ['Bb1', 'F2', 'D3'], ['Bb1', 'F2', 'D3'],
    ['D2', 'A2', 'F3'], ['F2', 'C3', 'A3'], ['E2', 'B2', 'G#3'], ['E2', 'D3', 'G#3'],
  ], 4);
  return [
    { b: 0, d: 64, n: 'A1', voz: 'dron', v: 0.8 },
    ...con(pad, { v: 0.6 }),
    ...melodia(alargar(octava(IVY_1, 1), 2), 'caja', 6, 1.4),
    ...melodia('-:2 E4:1 F4:1 | E4:3 C4:1 | D4:2 F4:1.5 E4:.5 | D4:4 | -:1 A3:1 D4:1 E4:1 | F4:2 E4:1 C4:1 | G#3:2 B3:2 | E4:3', 'lamento', 32),
    // el reloj de Ivy: anda, y de pronto se para
    ...reloj(0, 16, 1, 0.8), ...reloj(32, 43, 1, 0.8),
    ...golpes([0, 32], 'A3', 'campana', 1.1, 4), ...golpes([48], 'E3', 'campana', 0.8, 4),
    { b: 26, d: 6, n: 'F5', voz: 'roce', v: 0.5 }, { b: 57, d: 5, n: 'C#6', voz: 'roce', v: 0.4 },
    { b: 40, d: 8, n: 'A5', voz: 'tremolo', v: 0.3 },
  ];
}

/** Transpone una melodía escrita `semitonos` arriba o abajo. */
const transponerTexto = (texto: string, semitonos: number) => texto.replace(/[A-G][#b]?\d/g, (n) => transponer(n, semitonos));

/** El piso, a solas: arpegios de piano que no terminan de resolver y, en una caja de música, la tonada de Ivy. */
function soledad(): Nota[] {
  const acordes = [['E2', 'B2', 'G3', 'F#4'], ['C2', 'G2', 'E3', 'B3'], ['A1', 'E2', 'C3', 'G3'], ['B1', 'F#2', 'D#3', 'A3'],
    ['E2', 'B2', 'G3', 'F#4'], ['C2', 'G2', 'E3', 'B3'], ['A1', 'E2', 'C3', 'G3'], ['B1', 'F#2', 'E3', 'A3']];
  return [
    ...dibujo(acordes, 6, '0 1 2 3 2 1', 0.5, 'piano_limpio', 0.6, 1.2),
    ...con(colchon([['G4', 'B4'], ['G4', 'B4'], ['E4', 'G4'], ['F#4', 'A4'], ['G4', 'B4'], ['G4', 'B4'], ['E4', 'G4'], ['F#4', 'A4']], 6), { v: 0.3 }),
    ...melodia(transponerTexto(IVY_1, -5), 'caja', 24, 1),
  ];
}

// ---------------------------------------------------------------- el Minipax
const RUTINA = [['D3', 'A3', 'D4'], ['Bb2', 'F3', 'Bb3'], ['G2', 'D3', 'G3'], ['A2', 'E3', 'A3'],
  ['D3', 'A3', 'D4'], ['F2', 'C3', 'F3'], ['G2', 'D3', 'G3'], ['A2', 'E3', 'A3']];

/** El trabajo de cada día: un ostinato que no se equivoca nunca y el himno, en menor, al fondo. */
function rutina(): Nota[] {
  return [
    ...dibujo(RUTINA, 8, '0! 1 2 1 0 1 2 1', 0.5, 'pizzicato', 0.8),
    ...con(colchon([['D4', 'F4', 'A4'], ['D4', 'F4', 'Bb4'], ['D4', 'G4', 'Bb4'], ['C#4', 'E4', 'A4'],
      ['D4', 'F4', 'A4'], ['C4', 'F4', 'A4'], ['D4', 'G4', 'Bb4'], ['C#4', 'E4', 'A4']], 8), { v: 0.5 }),
    ...melodia('A4:1.5 A4:.5 D5:1 F5:1 | A5:2 F5:1 D5:1 | E5:1.5 E5:.5 F5:1 G5:1 | F5:3 -:1', 'metal', 32, 1.4),
    ...melodia('G4:1.5 G4:.5 Bb4:1 D5:1 | C5:2 Bb4:1 G4:1 | A4:1.5 A4:.5 C#5:1 E5:1 | D5:3 -:1', 'metal', 48, 1.3),
    ...RUTINA.map((a, i) => ({ b: i * 8, d: 2, n: transponer(a[0], -12), voz: 'timbal' as Voz, v: 0.45 })),
  ];
}

/** Desde que Amory no está: el mismo ostinato con huecos, armonías que no cierran y un clarinete que duda. */
function grieta(): Nota[] {
  const acordes = [['D3', 'A3', 'D4'], ['Bb2', 'F3', 'Bb3'], ['G2', 'D3', 'G3'], ['A2', 'E3', 'A3'],
    ['D3', 'A3', 'D4'], ['D3', 'G#3', 'B3'], ['Bb2', 'F3', 'Bb3'], ['A2', 'E3', 'A3']];
  return [
    ...dibujo(acordes, 8, '0! 1 2 . 0 1 . 1', 0.5, 'pizzicato', 0.75),
    ...con(colchon([['E4', 'F4', 'A4'], ['D4', 'E4', 'A4'], ['Bb3', 'D4', 'E4'], ['C#4', 'G4', 'Bb4'],
      ['F4', 'A4', 'E5'], ['E4', 'G#4', 'B4'], ['D4', 'F4', 'A4'], ['C#4', 'E4', 'G4']], 8), { v: 0.5 }),
    ...melodia('-:4 A4:1.5 B4:.5 C#5:2 | D5:3 E5:1 C5:2 Bb4:2 | -:2 G4:1 A4:1 Bb4:2 B4:2 | C#5:3 Bb4:1 A4:4 | '
      + '-:4 F4:1.5 G4:.5 A4:2 | G#4:3 F#4:1 E4:2 D4:2 | -:2 D4:1 E4:1 F4:2 F#4:2 | E4:4 -:4', 'lamento', 0, 0.9),
    ...reloj(0, 64, 2, 0.3),
  ];
}

/** El frenesí de la Gran Rectificación: máquinas de escribir, un reloj y un ostinato que sube y vuelve a empezar. */
function frenesi(): Nota[] {
  const notas: Nota[] = [];
  ['A2', 'Bb2', 'B2', 'C3'].forEach((raiz, s) => {
    const b0 = s * 16;
    for (let c = 0; c < 4; c++) {
      [0, 7, 12, 7, 3, 7, 12, 10].forEach((i, k) => notas.push({ b: b0 + c * 4 + k * 0.5, d: 0.5, n: transponer(raiz, i), voz: 'pizzicato', v: k === 0 ? 1.2 : 0.85 }));
      'x x x . x x . x x x x . x . x x'.split(' ').forEach((x, k) => { if (x === 'x') notas.push({ b: b0 + c * 4 + k * 0.25, d: 0.25, n: 'C5', voz: 'tecla', v: 1 }); });
    }
    notas.push({ b: b0 + 7.5, d: 0.5, n: 'C7', voz: 'timbre', v: 0.8 }, { b: b0 + 15.5, d: 0.5, n: 'C7', voz: 'timbre', v: 0.8 });
    notas.push({ b: b0 + 7.75, d: 0.25, n: 'C4', voz: 'carro', v: 0.7 }, { b: b0 + 15.75, d: 0.25, n: 'C4', voz: 'carro', v: 0.7 });
    notas.push({ b: b0, d: 16, n: transponer(raiz, 15), voz: 'tremolo', v: 0.45 }, { b: b0, d: 16, n: transponer(raiz, 19), voz: 'tremolo', v: 0.45 });
    notas.push({ b: b0, d: 2, n: raiz, voz: 'timbal', v: 0.5 });
  });
  return [...notas, ...reloj(0, 64, 1, 0.45)];
}

/** El despacho de Voss: un reloj de pared, frío; notas sueltas muy agudas y una segunda menor que no se va. */
function voss(): Nota[] {
  return [
    { b: 0, d: 48, n: 'B1', voz: 'dron', v: 0.5 },
    ...reloj(0, 48, 1, 1),
    { b: 0, d: 16, n: 'F#5', voz: 'cuerdas', v: 0.35 }, { b: 0, d: 16, n: 'B5', voz: 'cuerdas', v: 0.3 },
    { b: 16, d: 16, n: 'G5', voz: 'cuerdas', v: 0.35 }, { b: 24, d: 8, n: 'C6', voz: 'cuerdas', v: 0.25 },
    { b: 32, d: 16, n: 'F#5', voz: 'cuerdas', v: 0.35 }, { b: 32, d: 16, n: 'A#5', voz: 'cuerdas', v: 0.3 },
    ...melodia('B5:4 F#5:4 -:8 C6:2 B5:6 -:8 A#4:4 B4:12', 'piano_limpio', 0, 1),
    ...golpes([0, 24], 'B1', 'timbal', 0.4, 2),
  ];
}

// ---------------------------------------------------------------- las misiones de la Hermandad
/** El sigilo: un pulso grave en 3+3+2, el corazón que se acelera y racimos de cuerdas que tiemblan. */
function sigilo(): Nota[] {
  const notas: Nota[] = [];
  const raices = ['E2', 'E2', 'E2', 'E2', 'C2', 'C2', 'B1', 'B1', 'E2', 'E2', 'E2', 'E2', 'F2', 'F2', 'B1', 'B1'];
  raices.forEach((r, c) => {
    [[0, 0, 1.3], [0, 0, 1], [12, 0, 1], [0, 0, 1.2], [0, 0, 1], [12, 0, 1], [0, 0, 1.2], [1, 0, 1]].forEach(([i, , v], k) =>
      notas.push({ b: c * 4 + k * 0.5, d: 0.5, n: transponer(r, i), voz: 'pulso', v }));
  });
  return [
    ...notas,
    ...golpes([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30], 'C2', 'latido', 0.5),
    ...golpes(Array.from({ length: 32 }, (_, i) => 32 + i), 'C2', 'latido', 0.55),
    { b: 16, d: 16, n: 'B4', voz: 'tremolo', v: 0.85 }, { b: 16, d: 16, n: 'C5', voz: 'tremolo', v: 0.85 },
    { b: 48, d: 16, n: 'E5', voz: 'tremolo', v: 0.8 }, { b: 48, d: 16, n: 'F5', voz: 'tremolo', v: 0.8 },
    ...con(colchon([['E3', 'B3'], ['E3', 'B3'], ['C3', 'G3'], ['B2', 'F#3'], ['E3', 'B3'], ['E3', 'B3'], ['F3', 'C4'], ['B2', 'F#3']], 8), { v: 0.45 }),
    ...golpes([15.5, 31.5, 47.5, 63.5], 'B4', 'pizzicato', 1),
    ...golpes([0, 32], 'E2', 'timbal', 0.4, 2), ...golpes([16], 'C2', 'timbal', 0.35, 2), ...golpes([48], 'F2', 'timbal', 0.35, 2),
    ...golpes([24, 56], 'B1', 'timbal', 0.4, 2),
  ];
}

/** El Miniver a plena luz: hacerse el normal. Un bajo que camina de puntillas y un clarinete en staccato. */
function infiltrado(): Nota[] {
  const compases = ['Gm', 'Gm', 'Eb', 'Eb', 'Cm', 'Cm', 'D7', 'D7'];
  const ACORDES: Record<string, string[]> = { Gm: ['G2', 'Bb2', 'D3', 'Bb2'], Eb: ['Eb2', 'G2', 'Bb2', 'G2'], Cm: ['C3', 'Eb3', 'G3', 'Eb3'], D7: ['D3', 'F#3', 'A3', 'C3'] };
  const ARRIBA: Record<string, string[]> = { Gm: ['Bb3', 'D4'], Eb: ['Bb3', 'Eb4'], Cm: ['Eb4', 'G4'], D7: ['F#3', 'C4'] };
  const notas: Nota[] = [];
  for (let vuelta = 0; vuelta < 2; vuelta++) {
    compases.forEach((c, i) => {
      const b0 = vuelta * 32 + i * 4;
      ACORDES[c].forEach((n, k) => notas.push({ b: b0 + k, d: 0.6, n, voz: 'pizzicato', v: k === 0 ? 1.1 : 0.85 }));
      for (const k of [1.5, 3.5]) for (const n of ARRIBA[c]) notas.push({ b: b0 + k, d: 0.4, n, voz: 'pizzicato', v: 0.45 });
    });
  }
  const tema = 'G4:.5 -:.5 Bb4:.5 -:.5 A4:.5 G4:.5 -:1 | D5:1.5 C5:.5 Bb4:1 -:1 | Eb5:.5 -:.5 D5:.5 -:.5 C5:.5 Bb4:.5 -:1 | G4:3 -:1 | '
    + 'C5:.5 -:.5 Eb5:.5 -:.5 D5:.5 C5:.5 -:1 | Bb4:1.5 A4:.5 G4:1 -:1 | A4:.5 -:.5 C5:.5 -:.5 F#4:1 A4:1 | D5:3 -:1';
  return [
    ...notas,
    ...melodia(tema, 'lamento', 0, 1.1),
    ...melodia(octava(tema, 1), 'piano_limpio', 32, 0.4),
    ...reloj(0, 64, 2, 0.35),
    ...golpes(Array.from({ length: 32 }, (_, i) => i * 2 + 1), 'C4', 'redoble', 0.6),
  ];
}

/** Los túneles: la oscuridad, un corazón despacio, bombas lejos y, entre las gotas, la tonada de Ivy que guía. */
function tuneles(): Nota[] {
  return [
    { b: 0, d: 64, n: 'E1', voz: 'dron', v: 0.5 }, { b: 0, d: 64, n: 'B1', voz: 'dron', v: 0.35 },
    ...con(colchon([['E3', 'B3', 'G4'], ['C3', 'G3', 'E4'], ['A2', 'E3', 'C4'], ['B2', 'F#3', 'D#4']], 16), { v: 0.55 }),
    ...melodia('-:4 B5:2 G5:2 B5:2 G5:2 E5:6 -:14 F#5:1 G5:1 A5:2 F#5:4 B5:2 G5:2 E5:8 -:12', 'piano_limpio', 0, 0.95),
    ...golpes([7, 23.5, 41, 55], 'E1', 'timbal', 0.65, 2),
    ...golpes(Array.from({ length: 32 }, (_, i) => i * 2), 'C2', 'latido', 0.3),
    { b: 28, d: 6, n: 'G#5', voz: 'roce', v: 0.35 },
  ];
}

/** El Minimor (de visita): un racimo grave que no se resuelve, un corazón que aguanta y algo que roza en otra sala. */
function minimor(): Nota[] {
  return [
    { b: 0, d: 48, n: 'C2', voz: 'dron', v: 0.8 },
    { b: 0, d: 24, n: 'C3', voz: 'cuerdas', v: 0.45 }, { b: 0, d: 24, n: 'Db3', voz: 'cuerdas', v: 0.4 },
    { b: 24, d: 24, n: 'C3', voz: 'cuerdas', v: 0.45 }, { b: 24, d: 24, n: 'G3', voz: 'cuerdas', v: 0.35 }, { b: 24, d: 24, n: 'Ab3', voz: 'cuerdas', v: 0.4 },
    ...con(colchon([['Eb3', 'E3'], ['Eb3', 'D3', 'Ab3']], 24, 'coro'), { v: 0.75 }),
    ...golpes([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 39.2, 41, 42.1, 44, 45.3, 46.5], 'C2', 'latido', 0.5),
    { b: 12, d: 6, n: 'E6', voz: 'roce', v: 0.35 }, { b: 36, d: 5, n: 'B5', voz: 'roce', v: 0.3 },
    ...melodia('C2:8 -:4 Db2:4 -:8 C2:8 -:4 B1:4 -:8', 'piano_limpio', 0, 1),
    { b: 20, d: 8, n: 'G5', voz: 'tremolo', v: 0.3 }, { b: 20, d: 8, n: 'Ab5', voz: 'tremolo', v: 0.3 },
  ];
}

/** El terror: la sala blanca de O'Brien, el arresto. Racimos, un corazón desbocado, golpes y metal que chirría. */
function terror(): Nota[] {
  return [
    { b: 0, d: 48, n: 'C2', voz: 'dron', v: 0.9 }, { b: 0, d: 48, n: 'C#2', voz: 'dron', v: 0.6 }, { b: 24, d: 24, n: 'F#2', voz: 'dron', v: 0.6 },
    // un coro sin palabras, en racimo, a media voz: el gemido de otra celda
    ...con(colchon([['C3', 'C#3', 'G3'], ['C3', 'F#3', 'G3']], 24, 'coro'), { v: 0.8 }),
    ...golpes([0, 1.1, 2, 5.5, 6.4, 9, 12, 12.8, 13.5, 18, 19, 22.5, 26, 27, 30, 33.2, 34, 38, 41, 42, 45], 'C2', 'latido', 0.75),
    { b: 6, d: 5, n: 'A6', voz: 'roce', v: 0.45 }, { b: 20, d: 7, n: 'D5', voz: 'roce', v: 0.45 }, { b: 36, d: 4, n: 'E7', voz: 'roce', v: 0.35 },
    { b: 10, d: 8, n: 'Bb5', voz: 'tremolo', v: 0.4 }, { b: 10, d: 8, n: 'B5', voz: 'tremolo', v: 0.4 },
    { b: 30, d: 10, n: 'E6', voz: 'tremolo', v: 0.3 }, { b: 30, d: 10, n: 'F6', voz: 'tremolo', v: 0.3 },
    ...melodia('C1+C#1+D1+G#1:4', 'piano', 16, 1.2), ...melodia('D#1+E1+A#1:4', 'piano', 40, 1),
    ...golpes([16], 'C2', 'timbal', 1, 2), ...golpes([40], 'D#2', 'timbal', 0.9, 2),
  ];
}

/** La celda: hambre, la luz que no se apaga. Un clarinete que baja y baja; el tiempo ya no pasa. */
function celda(): Nota[] {
  return [
    ...con(colchon([['D2', 'A2', 'F3'], ['D2', 'G2', 'Bb2'], ['D2', 'F2', 'Bb2'], ['D2', 'C#3', 'E3']], 12), { v: 0.55 }),
    ...melodia('-:4 F4:3 E4:1 | D4:4 -:4 | -:4 G4:2 F4:2 | E4:6 -:2 | -:4 F4:2 E4:2 | D4:3 C#4:1 D4:4', 'lamento', 0, 0.8),
    ...golpes([0, 24], 'D2', 'piano_limpio', 0.6, 4), ...golpes([36], 'A1', 'piano_limpio', 0.55, 4),
  ];
}

// ---------------------------------------------------------------- la tristeza, la rabia, la huida
const VIVY: Record<string, [string, string[]]> = {
  Am: ['A2', ['C4', 'E4']], F: ['F2', ['A3', 'C4']], E7: ['E2', ['G#3', 'D4']], Dm7: ['D2', ['F3', 'C4']], Dm: ['D2', ['F3', 'A3']], E: ['E2', ['G#3', 'B3']],
};
const IVY_ACORDES = ['Am', 'F', 'E7', 'Am', 'Am', 'Dm7', 'E7', 'Am', 'Am', 'F', 'E7', 'Am', 'F', 'Dm', 'E', 'E7'];

/** El duelo por Ivy: «Naranjas y limones» en menor, al clarinete, con un vals de piano que apenas se atreve. */
function ivy(): Nota[] {
  return [
    ...valsSuave(IVY_ACORDES.map((c) => VIVY[c]), 0.85),
    ...con(colchon(IVY_ACORDES.map((c) => [transponer(VIVY[c][0], 12), ...VIVY[c][1]]), 3), { v: 0.4 }),
    ...melodia(`${IVY_1} | ${IVY_2}`, 'lamento', 0),
    ...melodia(octava(IVY_1, -1), 'piano_limpio', 24, 0.95),
    ...melodia('C5:3 D5:3 B4:3 C5:3', 'cuerdas', 24, 0.6),
    ...melodia('C5:2 B4:1 | A4:3 | G#4:2 A4:1 | B4:3', 'lamento', 36, 0.9),
  ];
}

/** Las ruinas (el mercado después del cohete, Shadwell): quintas vacías, un coro sin palabras, suspiros. */
function ruinas(): Nota[] {
  return [
    { b: 0, d: 48, n: 'D2', voz: 'dron', v: 0.4 },
    ...con(colchon([['D3', 'A3'], ['C3', 'G3'], ['Bb2', 'F3'], ['A2', 'E3']], 12), { v: 0.6 }),
    ...con(colchon([['F4'], ['E4'], ['D4'], ['C#4']], 12, 'coro'), { v: 0.55 }),
    ...melodia('-:2 A4:2 G4:1 F4:1 | E4:3 -:3 | -:2 G4:2 F4:1 E4:1 | D4:3 -:3 | -:2 D5:2 C5:1 Bb4:1 | A4:4 -:2 | -:2 E4:2 F4:1 E4:1 | C#4:4 -:2', 'lamento', 0, 0.9),
  ];
}

/** La rabia: Voss firmó la orden. Timbales, cuerdas a golpe de arco, metales que muerden y una trompeta que grita. */
function rabia(): Nota[] {
  const acordes = [['D3', 'F3', 'A3', 'D4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['G2', 'Bb2', 'D3', 'G3'], ['A2', 'C#3', 'G3', 'A3'],
    ['D3', 'F3', 'A3', 'D4'], ['Bb2', 'D3', 'F3', 'Bb3'], ['Eb3', 'G3', 'Bb3', 'Eb4'], ['A2', 'C#3', 'E3', 'A3']];
  const stabs = [['D4', 'F4', 'A4'], ['D4', 'F4', 'Bb4'], ['D4', 'G4', 'Bb4'], ['C#4', 'G4', 'Bb4'], ['D4', 'F4', 'A4'], ['D4', 'F4', 'Bb4'], ['Eb4', 'G4', 'Bb4'], ['C#4', 'E4', 'A4']];
  const notas: Nota[] = [];
  acordes.forEach((a, i) => {
    const raiz = transponer(a[0], -12);
    for (let c = 0; c < 2; c++) {
      [[0, 0.85], [1, 0.5], [1.5, 0.6], [2.5, 0.5], [3.5, 0.65]].forEach(([b, v]) => notas.push({ b: i * 8 + c * 4 + b, d: 0.5, n: raiz, voz: 'timbal', v }));
    }
    for (const b of [0, 1.5, 4, 5.5]) for (const n of stabs[i]) notas.push({ b: i * 8 + b, d: 0.6, n, voz: 'metal', v: 1.25 });
  });
  const redoble = (desde: number) => [0, 0.25, 0.5, 0.75, 1, 1.25].map((x, k) => ({ b: desde + x, d: 0.25, n: 'C4', voz: 'redoble' as Voz, v: 0.6 + k * 0.12 }));
  return [
    ...notas,
    ...dibujo(acordes, 8, '0! 0 3 0 2 0 1 0', 0.5, 'cuerdas', 1.1, 0.4),
    ...melodia('D3:1.5 D3:.5 F3:1 A3:1 | D4:4 | Bb2:1.5 Bb2:.5 D3:1 F3:1 | Bb3:4 | G2:1.5 G2:.5 Bb2:1 D3:1 | G3:4 | A2:1.5 A2:.5 C#3:1 E3:1 | A3:2 Bb3:2', 'tuba', 0, 0.75),
    ...melodia('D5:1.5 E5:.5 F5:1 A5:1 | G5:1.5 F5:.5 E5:2 | F5:1.5 D5:.5 Bb4:1 D5:1 | C5:2 Bb4:1 A4:1 | '
      + 'Bb4:1.5 Eb5:.5 G5:2 | F5:1 Eb5:1 D5:1 C5:1 | C#5:2 E5:1 G5:1 | A5:3 -:1', 'trompeta', 32),
    ...redoble(30.5), ...redoble(62.5),
  ];
}

/** La huida por los callejones de Limehouse: un pulso que corre, tambores y metales que suben. */
function persecucion(): Nota[] {
  const raices = ['C2', 'Ab1', 'Bb1', 'G1', 'C2', 'Db2', 'Eb2', 'G1'];
  const acordes = [['C4', 'Eb4', 'G4'], ['C4', 'Eb4', 'Ab4'], ['D4', 'F4', 'Bb4'], ['B3', 'D4', 'G4'],
    ['C4', 'Eb4', 'G4'], ['Db4', 'F4', 'Ab4'], ['Eb4', 'G4', 'Bb4'], ['B3', 'D4', 'F4']];
  const notas: Nota[] = [];
  raices.forEach((r, i) => {
    for (let c = 0; c < 2; c++) {
      const b0 = i * 8 + c * 4;
      '0! 1 0 0 1 0 0! 1'.split(' ').forEach((t, k) => notas.push({ b: b0 + k * 0.5, d: 0.5, n: t.startsWith('1') ? transponer(r, 12) : r, voz: 'pulso', v: t.endsWith('!') ? 1.3 : 1 }));
      for (const b of [0, 1.5, 2]) notas.push({ b: b0 + b, d: 0.5, n: 'C2', voz: 'bombo', v: 0.9 });
      for (const [b, v] of [[1, 1], [3, 1], [1.75, 0.45], [3.5, 0.45]]) notas.push({ b: b0 + b, d: 0.25, n: 'C4', voz: 'redoble', v });
    }
    notas.push({ b: i * 8, d: 2, n: r, voz: 'timbal', v: 0.5 });
    for (const n of acordes[i]) notas.push({ b: i * 8, d: 8, n, voz: 'tremolo', v: 0.75 });
    if (i < 4) for (const n of acordes[i]) notas.push({ b: i * 8, d: 1, n, voz: 'metal', v: 1.2 });
  });
  return [...notas, ...melodia('C4:2 D4:2 | Eb4:2 F4:2 | Db4:2 Eb4:2 | F4:2 Ab4:2 | G4:2 Bb4:2 | Eb5:4 | D5:2 B4:2 | G4:4', 'metal', 32, 1.3)];
}

// ---------------------------------------------------------------- Dot, Crane, la Hermandad, Goldstein
const VDOT: Record<string, string[]> = {
  Dm: ['D3', 'A3', 'F4'], F: ['F2', 'C4', 'A3'], Bb: ['Bb2', 'F3', 'D4'], Gm: ['G2', 'D3', 'Bb3'], C: ['C3', 'G3', 'E4'], A7: ['A2', 'C#4', 'G3'],
};
const DOT_MENOR = ['Dm', 'F', 'Bb', 'F', 'Gm', 'Gm', 'Dm', 'C', 'Dm', 'F', 'F', 'C', 'F', 'Gm', 'A7', 'Dm', 'Dm', 'A7'];

/** La casa de Dot (la huida): su canción, despacio y al piano, con armonía en menor. Sammy ya no está. */
function refugio(): Nota[] {
  return [
    ...melodia(DOT, 'piano_limpio', 0, 0.95),
    ...con(colchon(DOT_MENOR.map((c) => VDOT[c].slice(1)), 3), { v: 0.4 }),
    ...DOT_MENOR.map((c, i) => ({ b: i * 3, d: 3, n: VDOT[c][0], voz: 'pizzicato' as Voz, v: 0.7 })),
  ];
}

/** «En menor», para el tema de Crane: la, mi y re bajan medio tono. El mismo hombre, sin la sonrisa. */
const menor = (texto: string) => texto.replace(/([ADE])(\d)/g, '$1b$2');

/** El juramento (el sótano de La Campana) y Nell en el almacén: un coro grave, una campana lejos, la tonada de Ivy. */
function hermandad(): Nota[] {
  const coro = [['A3', 'C4', 'E4'], ['A3', 'C4', 'F4'], ['G3', 'C4', 'E4'], ['G#3', 'B3', 'E4'], ['A3', 'C4', 'E4'], ['A3', 'D4', 'F4'], ['A3', 'C4', 'F4'], ['G#3', 'B3', 'E4']];
  return [
    ...con(colchon(coro, 8, 'coro'), { v: 0.7 }),
    ...con(colchon([['A2'], ['F2'], ['C3'], ['E2'], ['A2'], ['D2'], ['F2'], ['E2']], 8), { v: 0.6 }),
    ...golpes([0], 'A3', 'campana', 1, 4), ...golpes([32], 'E3', 'campana', 0.9, 4),
    ...melodia('E5:1 C5:1 E5:1 C5:1 | A4:2 B4:1 C5:1 | D5:2 B4:2 | E5:1 C5:1 A4:2', 'lamento', 16, 0.85),
    ...melodia('C5:2 B4:2 | A4:4 | G#4:2 A4:1 B4:1 | E4:4', 'cuerdas', 48, 0.6),
    ...golpes(Array.from({ length: 16 }, (_, i) => i * 4), 'A1', 'timbal', 0.35, 2),
  ];
}

/** La cripta de San Clemente: «Naranjas y limones» como un coral de órgano, y las campanas que la cantan. */
function cripta(): Nota[] {
  const tema = 'G4:2 E4:2 G4:2 E4:2 | C4:2 D4:1 E4:1 F4:2 D4:2 | G4:2 E4:2 C4:4';
  const coral: [number, number, string[]][] = [
    [0, 2, ['C2', 'E3', 'C4']], [2, 2, ['A1', 'E3', 'C4']], [4, 2, ['E2', 'B3', 'E4']], [6, 2, ['C2', 'G3', 'C4']],
    [8, 2, ['F1', 'A2', 'F3']], [10, 1, ['D2', 'A2', 'F3']], [11, 1, ['E2', 'G3', 'C4']], [12, 2, ['F2', 'A3', 'C4']],
    [14, 2, ['G1', 'G3', 'B3']], [16, 2, ['E2', 'C4', 'E4']], [18, 2, ['A1', 'A3', 'C4']], [20, 2, ['G1', 'D3', 'F3']], [22, 2, ['C2', 'E3', 'G3']],
  ];
  const armonia = (desde: number, fuerza: number) => coral.flatMap(([b, d, ns]) => ns.map((n) => ({ b: desde + b, d, n, voz: 'organo' as Voz, v: fuerza })));
  const coda: [number, string[]][] = [[48, ['A1', 'E3', 'C4']], [52, ['F1', 'A3', 'C4']], [56, ['C2', 'G3', 'E4']], [60, ['G1', 'D3', 'B3']]];
  return [
    ...melodia(tema, 'organo', 0, 1.1), ...armonia(0, 0.8),
    ...melodia(tema, 'coro', 24, 1.1), ...melodia(octava(tema, 1), 'campana', 24, 1.3), ...armonia(24, 0.6),
    ...coda.flatMap(([b, ns]) => ns.map((n) => ({ b, d: b === 60 ? 3 : 4, n, voz: 'organo' as Voz, v: 0.6 }))),
    ...golpes([0], 'C3', 'campana', 0.6, 4), ...golpes([48, 52, 56, 60], 'C4', 'campana', 0.35, 3),
  ];
}

// ---------------------------------------------------------------- el Partido
/** La Canción del Odio (original): marcha en mi menor, bombo en cada pulso, al unísono, sin piedad. */
const ODIO = 'E4:1 E4:1 G4:1 E4:1 | B4:1.5 A4:.5 G4:1 F#4:1 | E4:1 E4:1 G4:1 B4:1 | E5:3 -:1 | '
  + 'D5:1 D5:1 C5:1 B4:1 | A4:1.5 G4:.5 F#4:1 E4:1 | F#4:1 G4:1 A4:1 F#4:1 | E4:3 -:1';
function odio(): Nota[] {
  const compases: [string, string[]][] = [['E2', ['E4', 'G4']], ['B1', ['D#4', 'A4']], ['E2', ['E4', 'G4']], ['E2', ['E4', 'B4']],
    ['G2', ['D4', 'G4']], ['A2', ['C4', 'E4']], ['B1', ['D#4', 'F#4']], ['E2', ['E4', 'G4']]];
  const notas: Nota[] = [];
  for (let vuelta = 0; vuelta < 2; vuelta++) {
    compases.forEach(([raiz, acorde], i) => {
      const b0 = vuelta * 32 + i * 4;
      notas.push({ b: b0, d: 1, n: raiz, voz: 'tuba', v: 0.8 }, { b: b0 + 2, d: 1, n: transponer(raiz, 7), voz: 'tuba', v: 0.7 });
      for (const n of acorde) notas.push({ b: b0 + 1, d: 0.6, n, voz: 'metal', v: 1 }, { b: b0 + 3, d: 0.6, n, voz: 'metal', v: 1 });
      for (let k = 0; k < 4; k++) notas.push({ b: b0 + k, d: 0.5, n: 'C2', voz: 'bombo', v: k === 0 ? 1.2 : 0.9 });
      notas.push({ b: b0 + 1, d: 0.25, n: 'C4', voz: 'redoble', v: 0.9 }, { b: b0 + 3, d: 0.25, n: 'C4', voz: 'redoble', v: 0.9 });
    });
  }
  return [
    ...notas,
    ...melodia(ODIO, 'trompeta', 0, 1.3), ...melodia(ODIO, 'trompeta', 32, 1.35), ...melodia(octava(ODIO, -1), 'tuba', 32, 0.55),
    ...golpes([0, 16, 32, 48], 'E2', 'timbal', 0.7, 2),
    ...[3.25, 3.5, 3.75].flatMap((x) => [28, 60].map((b) => ({ b: b + x, d: 0.25, n: 'C4', voz: 'redoble' as Voz, v: 1 }))),
  ];
}

/** El Café del Castaño: un vals alegre que sale de la telepantalla. Nadie lo escucha. */
const CAFE = 'G4:2 Bb4:1 | Eb5:2 D5:1 | C5:1 Bb4:1 Ab4:1 | G4:3 | F4:2 G4:1 | Ab4:2 C5:1 | Bb4:1 Ab4:1 G4:1 | F4:3 | '
  + 'G4:2 Bb4:1 | Eb5:2 F5:1 | G5:1 F5:1 Eb5:1 | C5:3 | Bb4:1 G4:1 Eb4:1 | F4:2 Ab4:1 | G4:1 F4:1 D4:1 | Eb4:3';
const VEb: [string, string[]] = ['Eb2', ['G3', 'Bb3']];
const VAb: [string, string[]] = ['Ab2', ['Ab3', 'C4']];
const VBb7: [string, string[]] = ['Bb2', ['Ab3', 'D4']];
const VCm: [string, string[]] = ['C3', ['G3', 'C4']];
const VFm: [string, string[]] = ['F2', ['Ab3', 'C4']];

export const PISTAS: Record<string, Pista> = {
  /** El himno del Partido, perfectamente afinado (créditos de los finales A y B). */
  himno: { bpm: 104, pulsos: 64, volumen: 0.43, emocion: 'fanatismo', sala: 0.25, cola: 2.5, notas: banda() },
  /** Desde los altavoces de la calle: metálico, saturado, un poco desafinado. */
  himno_altavoz: { bpm: 104, pulsos: 64, volumen: 0.19, emocion: 'fanatismo', diegetica: true, rigida: true, sala: 0.35, cola: 3, altavoz: true, desafino: 0.012, notas: banda() },
  /** La telepantalla del piso, de noche: el himno en volumen nocturno. */
  himno_tele: { bpm: 104, pulsos: 64, volumen: 0.1, emocion: 'rutina', diegetica: true, rigida: true, altavoz: true, corte: 1800, desafino: 0.008, notas: banda() },
  crane: {
    bpm: 72, pulsos: 64, volumen: 0.5, emocion: 'calidez', sala: 0.2, cola: 1.4,
    notas: [...melodia(CRANE, 'piano'), ...colchon(ACORDES_CRANE, 4)],
  },
  /** El sueño: «Naranjas y limones» en una caja de música. */
  caja_musica: { bpm: 112, pulsos: 28, volumen: 1.08, emocion: 'nostalgia', sala: 0.45, cola: 3.5, notas: melodia(octava(NARANJAS, 1), 'caja') },
  /** El epílogo del Final D: piano solo, muy lento. */
  naranjas_lento: { bpm: 56, pulsos: 30, volumen: 1.03, emocion: 'esperanza', sala: 0.35, cola: 3, notas: [...melodia(NARANJAS, 'piano'), ...IZQUIERDA_NARANJAS] },
  /** Créditos del Final D: ahora con orquesta. */
  naranjas_orquesta: {
    bpm: 84, pulsos: 26, volumen: 0.63, emocion: 'esperanza', sala: 0.4, cola: 3,
    notas: [
      ...melodia(octava(NARANJAS, -1), 'cuerdas'),
      ...colchon([['C3', 'G3', 'E4'], ['C3', 'G3', 'E4'], ['G2', 'D3', 'B3'], ['C3', 'G3', 'E4'],
        ['C3', 'G3', 'E4'], ['C3', 'G3', 'E4'], ['G2', 'D3', 'B3'], ['C3', 'G3', 'E4']], 3),
      ...melodia('C2:3 C2:3 G1:3 C2:3 C2:3 C2:3 G1:3 C2:3', 'pizzicato'),
    ],
  },
  /** Los años en la cripta: la máquina de escribir convertida en ritmo. */
  maquina: { bpm: 100, pulsos: 32, volumen: 1, emocion: 'tension', diegetica: true, notas: maquina() },
  prole: {
    bpm: 96, pulsos: 54, volumen: 0.26, corte: 2400, emocion: 'alegria', diegetica: true, sala: 0.15, cola: 1,
    notas: melodia(DOT, 'tarareo'),
  },
  prole_piano: {
    bpm: 92, pulsos: 54, volumen: 0.73, emocion: 'calidez', sala: 0.2, cola: 1.5,
    notas: [
      ...melodia(DOT, 'piano'),
      ...acompanamiento([VF, VF, VF, VF, VBb, VC7, VC7, VC7, VF, VF, VF, VBb, VF, VC7, VC7, VF], 3, 'vals'),
    ],
  },
  taberna: {
    bpm: 132, pulsos: 64, volumen: 0.63, murmullo: 0.06, emocion: 'alegria', diegetica: true, sala: 0.12, cola: 0.9,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
  taberna_calle: {
    bpm: 132, pulsos: 64, volumen: 0.3, corte: 1100, emocion: 'alegria', diegetica: true,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
  taberna_lejos: {
    bpm: 132, pulsos: 64, volumen: 0.32, corte: 420, murmullo: 0.04, emocion: 'alegria', diegetica: true,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
  // ---------------------------------------------------------------- la banda sonora completa (M7)
  /** El menú: el misterio. El reloj de Ivy, su tonada en una caja de música lejana. */
  misterio: { bpm: 60, pulsos: 64, volumen: 0.62, emocion: 'misterio', sala: 0.5, cola: 4, entrada: 3, notas: misterio() },
  /** El Minipax en el Acto I: la rutina de un creyente. */
  rutina: { bpm: 96, pulsos: 64, volumen: 0.66, emocion: 'rutina', rigida: true, sala: 0.2, cola: 1.2, notas: rutina() },
  /** El Minipax desde que Amory no está. */
  grieta: { bpm: 84, pulsos: 64, volumen: 0.56, emocion: 'duda', sala: 0.3, cola: 2, notas: grieta() },
  /** La noche de la Gran Rectificación. */
  frenesi: { bpm: 144, pulsos: 64, paneo: { tremolo: -0.3, tecla: -0.25 }, volumen: 0.64, emocion: 'frustracion', sala: 0.15, cola: 1, notas: frenesi() },
  /** El despacho de Voss. */
  voss: { bpm: 60, pulsos: 48, volumen: 0.9, emocion: 'tension', sala: 0.35, cola: 2.5, notas: voss() },
  /** Las misiones de la Hermandad en el Minipax (sigilo). */
  sigilo: { bpm: 104, pulsos: 64, volumen: 0.62, emocion: 'tension', sala: 0.25, cola: 1.6, notas: sigilo() },
  /** La misión del Miniver: hacerse el normal. */
  infiltrado: { bpm: 108, pulsos: 64, paneo: { lamento: -0.25, piano_limpio: -0.15 }, volumen: 0.77, emocion: 'tension', sala: 0.25, cola: 1.5, notas: infiltrado() },
  /** Los túneles del metro, hacia San Clemente. */
  tuneles: { bpm: 66, pulsos: 64, volumen: 0.61, emocion: 'tension', sala: 0.6, cola: 4.5, notas: tuneles() },
  /** El Ministerio del Amor (de visita, en la Jornada 11). */
  minimor: { bpm: 56, pulsos: 48, volumen: 0.69, emocion: 'miedo', sala: 0.5, cola: 4, notas: minimor() },
  /** La sala blanca de O'Brien, los arrestos. */
  terror: { bpm: 52, pulsos: 48, volumen: 0.48, emocion: 'terror', sala: 0.55, cola: 4.5, entrada: 0.6, notas: terror() },
  /** La celda del Minimor. */
  celda: { bpm: 46, pulsos: 48, volumen: 0.87, emocion: 'miedo', sala: 0.45, cola: 3.5, notas: celda() },
  /** El duelo por Ivy (el prólogo, la calle Stepney). */
  ivy: { bpm: 58, pulsos: 48, volumen: 0.73, emocion: 'tristeza', sala: 0.45, cola: 3.2, notas: ivy() },
  /** Las ruinas: el mercado después del cohete, la estación de Shadwell. */
  ruinas: { bpm: 54, pulsos: 48, volumen: 0.71, emocion: 'tristeza', sala: 0.5, cola: 3.5, notas: ruinas() },
  /** La rabia: la firma de Voss. */
  rabia: { bpm: 132, pulsos: 64, volumen: 0.38, emocion: 'rabia', sala: 0.2, cola: 1.3, entrada: 0.4, notas: rabia() },
  /** La huida por los callejones. */
  persecucion: { bpm: 152, pulsos: 64, volumen: 0.68, emocion: 'miedo', sala: 0.2, cola: 1.2, entrada: 0.3, notas: persecucion() },
  /** La casa de Dot, cuando le esconde. */
  refugio: { bpm: 66, pulsos: 54, volumen: 1.09, emocion: 'nostalgia', sala: 0.35, cola: 2.4, notas: refugio() },
  /** Crane se quita la máscara. */
  crane_oscuro: {
    bpm: 60, pulsos: 64, volumen: 0.95, emocion: 'miedo', desafino: 0.012, sala: 0.35, cola: 2.5,
    notas: [
      ...melodia(menor(CRANE), 'piano', 0, 1.4),
      ...con(colchon(ACORDES_CRANE.map((a) => a.map(menor)), 4, 'tremolo'), { v: 0.55 }),
      { b: 0, d: 64, n: 'F1', voz: 'dron', v: 0.5 },
      ...golpes(Array.from({ length: 16 }, (_, i) => i * 4), 'C2', 'latido', 0.35),
    ],
  },
  /** El juramento de la Hermandad. */
  hermandad: { bpm: 60, pulsos: 64, volumen: 0.8, emocion: 'misterio', sala: 0.45, cola: 3.5, notas: hermandad() },
  /** La cripta de San Clemente: Goldstein, el Capítulo II. */
  cripta: { bpm: 56, pulsos: 64, volumen: 0.51, emocion: 'esperanza', sala: 0.6, cola: 5, notas: cripta() },
  /** La Semana del Odio. */
  odio: { bpm: 120, pulsos: 64, volumen: 0.35, emocion: 'fanatismo', rigida: true, sala: 0.3, cola: 2.2, notas: odio() },
  /** Lo mismo, por los altavoces de la calle y del Gran Salón. */
  odio_altavoz: { bpm: 120, pulsos: 64, volumen: 0.17, emocion: 'fanatismo', diegetica: true, rigida: true, altavoz: true, desafino: 0.01, sala: 0.4, cola: 3, notas: odio() },
  /** El Café del Castaño. */
  cafe: {
    bpm: 92, pulsos: 48, volumen: 0.26, emocion: 'vacio', diegetica: true, rigida: true, altavoz: true, desafino: 0.012, corte: 2600,
    notas: [
      ...melodia(CAFE, 'piano'), ...melodia(CAFE, 'cuerdas', 0, 0.5),
      ...acompanamiento([VEb, VEb, VAb, VEb, VBb7, VAb, VBb7, VBb7, VEb, VEb, VCm, VAb, VEb, VFm, VBb7, VEb], 3, 'vals'),
    ],
  },
  /** El piso, a solas con la foto de Ivy. */
  soledad: { bpm: 64, pulsos: 48, volumen: 1.01, emocion: 'nostalgia', sala: 0.4, cola: 2.8, notas: soledad() },
  /** El himno de la telepantalla del vecino, a través de la pared (la escalera). */
  himno_pared: { bpm: 104, pulsos: 64, volumen: 0.13, emocion: 'rutina', diegetica: true, rigida: true, altavoz: true, corte: 650, desafino: 0.008, notas: banda() },
};
