/**
 * Música sintetizada en tiempo real (diseño técnico §12). Cada pista es una partitura corta en bucle:
 * notas con su tiempo en pulsos, su duración y su voz. Un planificador las va programando por delante
 * del reloj de audio, así que no hay archivos que descargar y el bucle no tiene costuras.
 *
 *   prole          La canción de Dot: leitmotiv de la vida prole. Vals tarareado, melodía original.
 *   taberna        Piano de La Campana, desafinado, con bajo de paseo y el murmullo del pub. Original.
 *   taberna_calle  La Campana oída desde la calle de Limehouse.
 *   taberna_lejos  Lo mismo oído a través del suelo (el sótano).
 *   prole_piano    La canción de Dot al piano, con acompañamiento de vals.
 */

type Voz = 'piano' | 'tarareo' | 'bajo' | 'acorde'
  | 'trompeta' | 'metal' | 'tuba' | 'redoble' | 'bombo'      // la banda del Partido
  | 'caja' | 'cuerdas' | 'pizzicato'                          // caja de música, orquesta
  | 'tecla' | 'timbre' | 'carro';                             // la máquina de escribir como ritmo

export interface Nota { b: number; d: number; n: string; voz: Voz }

export interface Pista {
  bpm: number;
  /** Longitud del bucle en pulsos (incluye el silencio final, si lo hay). */
  pulsos: number;
  notas: Nota[];
  volumen: number;
  /** Corte del filtro de la pista: menos agudos = más lejos. */
  corte?: number;
  /** Murmullo de gente y algún vaso: el pub. */
  murmullo?: number;
  /** Altavoz viejo: saturado y sin graves ni agudos (la calle, la telepantalla). */
  altavoz?: boolean;
  /** Desafinación de cada nota (0 = perfectamente afinado). */
  desafino?: number;
}

/** "A4:2 G4:1 | F4:2 A4:1" → notas seguidas desde el pulso `desde` ("-" es silencio). */
function melodia(texto: string, voz: Voz, desde = 0): Nota[] {
  const notas: Nota[] = [];
  let b = desde;
  for (const tok of texto.replace(/\|/g, ' ').split(/\s+/).filter(Boolean)) {
    const [n, d] = tok.split(':');
    if (n !== '-') notas.push({ b, d: Number(d), n, voz });
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

function midi(n: string): number {
  const m = /^([A-G])(#|b)?(\d)$/.exec(n);
  if (!m) return 60;
  const base = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[m[1] as 'C'] + (m[2] === '#' ? 1 : m[2] === 'b' ? -1 : 0);
  return 12 * (Number(m[3]) + 1) + base;
}

function transponer(n: string, semitonos: number): string {
  const x = midi(n) + semitonos;
  return `${NOMBRES[((x % 12) + 12) % 12]}${Math.floor(x / 12) - 1}`;
}

const frecuencia = (n: string) => 440 * 2 ** ((midi(n) - 69) / 12);

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
const octava = (texto: string, n: number) => texto.replace(/([A-G][#b]?)(\d)/g, (_, nota, o) => `${nota}${Number(o) + n}`);

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

export const PISTAS: Record<string, Pista> = {
  /** El himno del Partido, perfectamente afinado (créditos de los finales A y B). */
  himno: { bpm: 104, pulsos: 64, volumen: 0.45, notas: banda() },
  /** Desde los altavoces de la calle: metálico, saturado, un poco desafinado. */
  himno_altavoz: { bpm: 104, pulsos: 64, volumen: 0.26, altavoz: true, desafino: 0.012, notas: banda() },
  /** La telepantalla del piso, de noche: el himno en volumen nocturno. */
  himno_tele: { bpm: 104, pulsos: 64, volumen: 0.14, altavoz: true, corte: 1800, desafino: 0.008, notas: banda() },
  crane: {
    bpm: 72, pulsos: 64, volumen: 0.52,
    notas: [...melodia(CRANE, 'piano'), ...colchon(ACORDES_CRANE, 4)],
  },
  /** El sueño: «Naranjas y limones» en una caja de música. */
  caja_musica: { bpm: 112, pulsos: 28, volumen: 0.9, notas: melodia(octava(NARANJAS, 1), 'caja') },
  /** El epílogo del Final D: piano solo, muy lento. */
  naranjas_lento: { bpm: 56, pulsos: 30, volumen: 0.9, notas: [...melodia(NARANJAS, 'piano'), ...IZQUIERDA_NARANJAS] },
  /** Créditos del Final D: ahora con orquesta. */
  naranjas_orquesta: {
    bpm: 84, pulsos: 26, volumen: 0.6,
    notas: [
      ...melodia(octava(NARANJAS, -1), 'cuerdas'),
      ...colchon([['C3', 'G3', 'E4'], ['C3', 'G3', 'E4'], ['G2', 'D3', 'B3'], ['C3', 'G3', 'E4'],
        ['C3', 'G3', 'E4'], ['C3', 'G3', 'E4'], ['G2', 'D3', 'B3'], ['C3', 'G3', 'E4']], 3),
      ...melodia('C2:3 C2:3 G1:3 C2:3 C2:3 C2:3 G1:3 C2:3', 'pizzicato'),
    ],
  },
  /** Los años en la cripta: la máquina de escribir convertida en ritmo. */
  maquina: { bpm: 100, pulsos: 32, volumen: 1, notas: maquina() },
  prole: {
    bpm: 96, pulsos: 54, volumen: 0.26, corte: 2400,
    notas: melodia(DOT, 'tarareo'),
  },
  prole_piano: {
    bpm: 92, pulsos: 54, volumen: 0.6,
    notas: [
      ...melodia(DOT, 'piano'),
      ...acompanamiento([VF, VF, VF, VF, VBb, VC7, VC7, VC7, VF, VF, VF, VBb, VF, VC7, VC7, VF], 3, 'vals'),
    ],
  },
  taberna: {
    bpm: 132, pulsos: 64, volumen: 0.63, murmullo: 0.06,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
  taberna_calle: {
    bpm: 132, pulsos: 64, volumen: 0.3, corte: 1100,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
  taberna_lejos: {
    bpm: 132, pulsos: 64, volumen: 0.32, corte: 420, murmullo: 0.04,
    notas: [
      ...melodia(CAMPANA, 'piano'),
      ...acompanamiento([C, F, G7, G7, C, F, G7, C, C, Dm, G7, C, F, C, G7, C], 4, 'paseo'),
    ],
  },
};

const ANTICIPO = 0.5;      // segundos que se programan por delante
const FUNDIDO = 1.4;

/** Una pista sonando: su bus (para fundirla sin cortar las notas ya programadas) y su planificador. */
class Reproduccion {
  readonly bus: GainNode;
  private filtro: BiquadFilterNode;
  private timer: number;
  private inicio: number;
  private siguiente = 0;          // índice de la próxima nota dentro del bucle
  private vuelta = 0;
  private murmullo: AudioBufferSourceNode | null = null;
  private proximoVaso = 0;

  constructor(private ctx: AudioContext, out: AudioNode, readonly id: string, private p: Pista) {
    this.bus = ctx.createGain();
    this.bus.gain.setValueAtTime(0.0001, ctx.currentTime);
    this.bus.gain.exponentialRampToValueAtTime(p.volumen, ctx.currentTime + FUNDIDO);
    this.filtro = ctx.createBiquadFilter();
    this.filtro.type = 'lowpass';
    this.filtro.frequency.value = p.corte ?? 9000;
    if (p.altavoz) {
      // el altavoz: satura y recorta graves y agudos
      const sat = ctx.createWaveShaper();
      const curva = new Float32Array(1024);
      for (let i = 0; i < curva.length; i++) { const x = (i / (curva.length - 1)) * 2 - 1; curva[i] = Math.tanh(x * 3.2); }
      sat.curve = curva;
      const banda = ctx.createBiquadFilter();
      banda.type = 'bandpass'; banda.frequency.value = 1300; banda.Q.value = 0.9;
      this.bus.connect(this.filtro).connect(sat).connect(banda).connect(out);
    } else {
      this.bus.connect(this.filtro).connect(out);
    }
    this.p.notas.sort((a, b) => a.b - b.b);
    this.inicio = ctx.currentTime + 0.15;
    if (p.murmullo) this.empezarMurmullo(p.murmullo);
    this.timer = window.setInterval(() => this.programar(), 100);
    this.programar();
  }

  private get pulso() { return 60 / this.p.bpm; }

  private programar() {
    const limite = this.ctx.currentTime + ANTICIPO;
    const largo = this.p.pulsos * this.pulso;
    for (let guarda = 0; guarda < 500; guarda++) {
      if (this.siguiente >= this.p.notas.length) { this.siguiente = 0; this.vuelta++; }
      const nota = this.p.notas[this.siguiente];
      const t = this.inicio + this.vuelta * largo + nota.b * this.pulso;
      if (t > limite) break;
      if (t >= this.ctx.currentTime - 0.05) this.tocar(nota, t);
      this.siguiente++;
    }
    if (this.p.murmullo && this.ctx.currentTime > this.proximoVaso) {
      this.proximoVaso = this.ctx.currentTime + 2 + Math.random() * 5;
      this.vaso(this.ctx.currentTime + Math.random() * 0.4);
    }
  }

  private tocar(nota: Nota, t: number) {
    const des = this.p.desafino ?? 0;
    const f = frecuencia(nota.n) * (1 + (Math.random() - 0.5) * des), d = nota.d * this.pulso;
    switch (nota.voz) {
      case 'tarareo': return this.tararear(f, t, d);
      case 'bajo': return this.piano(f, t, d + 0.25, 0.09, 0.02);
      case 'acorde': return this.piano(f, t, d, 0.035, 0.02);
      case 'trompeta': return this.metal(f, t, d * 0.92, 0.085, 2600);
      case 'metal': return this.metal(f, t, d * 0.7, 0.03, 1500);
      case 'tuba': return this.metal(f, t, d * 0.8, 0.09, 500);
      case 'redoble': return this.golpeRuido(t, 0.09, 1800, 0.12, 'highpass');
      case 'bombo': return this.bombo(t);
      case 'caja': return this.caja(f, t);
      case 'cuerdas': return this.cuerdas(f, t, d, 0.03);
      case 'pizzicato': return this.piano(f, t, 0.35, 0.06, 0.004);
      case 'tecla': return this.golpeRuido(t + Math.random() * 0.02, 0.035, 2600, 0.3 + Math.random() * 0.15, 'bandpass');
      case 'timbre': return this.caja(3150, t);
      case 'carro': return this.golpeRuido(t, 0.35, 1400, 0.18, 'bandpass', true);
      default: return this.piano(f, t, d + 0.3, 0.1, 0.016);
    }
  }

  /** Metales: diente de sierra con un filtro que se abre en el ataque, como una boquilla. */
  private metal(f: number, t: number, dur: number, vol: number, brillo: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), osc2 = ctx.createOscillator();
    const fl = ctx.createBiquadFilter(), g = ctx.createGain();
    osc.type = 'sawtooth'; osc2.type = 'square';
    osc.frequency.value = f; osc2.frequency.value = f * 1.003;
    fl.type = 'lowpass'; fl.Q.value = 2;
    fl.frequency.setValueAtTime(brillo * 0.25, t);
    fl.frequency.exponentialRampToValueAtTime(brillo, t + 0.05);
    fl.frequency.exponentialRampToValueAtTime(brillo * 0.6, t + Math.max(0.1, dur));
    const o2 = ctx.createGain(); o2.gain.value = 0.35;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.03);
    g.gain.setValueAtTime(vol * 0.8, t + Math.max(0.05, dur - 0.06));
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur + 0.04);
    osc.connect(fl); osc2.connect(o2).connect(fl); fl.connect(g).connect(this.bus);
    for (const o of [osc, osc2]) { o.start(t); o.stop(t + dur + 0.08); }
  }

  private golpeRuido(t: number, dur: number, f: number, vol: number, tipo: BiquadFilterType, barrido = false) {
    const ctx = this.ctx;
    const n = Math.ceil(ctx.sampleRate * dur);
    const buf = ctx.createBuffer(1, n, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    const src = ctx.createBufferSource(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
    src.buffer = buf;
    fl.type = tipo; fl.frequency.setValueAtTime(f, t);
    if (barrido) fl.frequency.exponentialRampToValueAtTime(f * 3, t + dur);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(fl).connect(g).connect(this.bus);
    src.start(t);
  }

  private bombo(t: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(120, t); osc.frequency.exponentialRampToValueAtTime(48, t + 0.18);
    g.gain.setValueAtTime(0.22, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.3);
    osc.connect(g).connect(this.bus);
    osc.start(t); osc.stop(t + 0.32);
  }

  /** Caja de música: púa metálica, mucho armónico inarmónico y una cola larga. */
  private caja(f: number, t: number) {
    const ctx = this.ctx;
    for (const [mult, peso, cola] of [[1, 1, 1.4], [2.76, 0.25, 0.5], [5.4, 0.08, 0.25]] as const) {
      const osc = ctx.createOscillator(), g = ctx.createGain();
      osc.type = 'sine'; osc.frequency.value = f * mult;
      g.gain.setValueAtTime(0.06 * peso, t); g.gain.exponentialRampToValueAtTime(0.0001, t + cola);
      osc.connect(g).connect(this.bus);
      osc.start(t); osc.stop(t + cola + 0.05);
    }
  }

  /** Cuerdas: tres sierras desafinadas entre sí, ataque y caída lentos, sin agudos. */
  private cuerdas(f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const fl = ctx.createBiquadFilter(), g = ctx.createGain();
    fl.type = 'lowpass'; fl.frequency.value = Math.min(3200, f * 4);
    const fin = t + dur + 0.25;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + Math.min(0.35, dur * 0.4));
    g.gain.setValueAtTime(vol, Math.max(t + 0.36, fin - 0.4));
    g.gain.exponentialRampToValueAtTime(0.0001, fin);
    fl.connect(g).connect(this.bus);
    for (const det of [-0.004, 0, 0.005]) {
      const osc = ctx.createOscillator();
      osc.type = 'sawtooth'; osc.frequency.value = f * (1 + det);
      osc.connect(fl); osc.start(t); osc.stop(fin + 0.05);
    }
  }

  /** Piano de pared viejo: dos cuerdas que no coinciden, un armónico y un ataque seco. */
  private piano(f: number, t: number, dur: number, vol: number, desafino: number) {
    const ctx = this.ctx;
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.006);
    g.gain.exponentialRampToValueAtTime(vol * 0.35, t + 0.22);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    g.connect(this.bus);
    const d = 1 + (Math.random() - 0.5) * desafino;
    for (const [mult, tipo, peso] of [[1, 'triangle', 1], [1.011, 'triangle', 0.7], [2.006, 'sine', 0.22]] as const) {
      const osc = ctx.createOscillator();
      const go = ctx.createGain();
      osc.type = tipo;
      osc.frequency.value = f * d * mult;
      go.gain.value = peso;
      osc.connect(go).connect(g);
      osc.start(t);
      osc.stop(t + dur + 0.05);
    }
  }

  /** Una voz que tararea con la boca cerrada: senoidal con vibrato, ataque blando y algo de nariz. */
  private tararear(f: number, t: number, dur: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    const armonico = ctx.createOscillator();
    const vib = ctx.createOscillator();
    const vibG = ctx.createGain();
    const g = ctx.createGain();
    const ga = ctx.createGain();
    osc.type = 'sine'; armonico.type = 'triangle';
    osc.frequency.value = f; armonico.frequency.value = f;
    vib.frequency.value = 5.2; vibG.gain.value = f * 0.007;
    vib.connect(vibG); vibG.connect(osc.frequency); vibG.connect(armonico.frequency);
    ga.gain.value = 0.35;
    const fin = t + dur * 0.96;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.11, t + 0.07);
    g.gain.setValueAtTime(0.11 * 0.85, Math.max(t + 0.08, fin - 0.12));
    g.gain.exponentialRampToValueAtTime(0.0001, fin);
    osc.connect(g); armonico.connect(ga).connect(g);
    g.connect(this.bus);
    for (const o of [osc, armonico, vib]) { o.start(t); o.stop(fin + 0.05); }
  }

  private empezarMurmullo(vol: number) {
    const ctx = this.ctx;
    const dur = 4;
    const buf = ctx.createBuffer(1, ctx.sampleRate * dur, ctx.sampleRate);
    const data = buf.getChannelData(0);
    // ruido marrón: voces graves que no se entienden
    let ultimo = 0;
    for (let i = 0; i < data.length; i++) { ultimo = (ultimo + 0.02 * (Math.random() * 2 - 1)) / 1.02; data[i] = ultimo * 3.5; }
    const src = ctx.createBufferSource();
    src.buffer = buf; src.loop = true;
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass'; bp.frequency.value = 520; bp.Q.value = 0.8;
    const g = ctx.createGain();
    g.gain.value = vol / this.p.volumen;
    src.connect(bp).connect(g).connect(this.bus);
    src.start();
    this.murmullo = src;
  }

  private vaso(t: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = 2600 + Math.random() * 900;
    g.gain.setValueAtTime(0.03, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.25);
    osc.connect(g).connect(this.bus);
    osc.start(t); osc.stop(t + 0.3);
  }

  /** Baja un momento (un silbido, la telepantalla) y vuelve. */
  agachar(cuanto: number, dur: number) {
    const t = this.ctx.currentTime, v = this.p.volumen;
    this.bus.gain.cancelScheduledValues(t);
    this.bus.gain.setValueAtTime(Math.max(0.0001, this.bus.gain.value), t);
    this.bus.gain.exponentialRampToValueAtTime(Math.max(0.0001, v * cuanto), t + 0.2);
    this.bus.gain.setValueAtTime(Math.max(0.0001, v * cuanto), t + dur);
    this.bus.gain.exponentialRampToValueAtTime(v, t + dur + 1);
  }

  parar(rapido = false) {
    window.clearInterval(this.timer);
    const t = this.ctx.currentTime, dur = rapido ? 0.08 : FUNDIDO;
    this.bus.gain.cancelScheduledValues(t);
    this.bus.gain.setValueAtTime(Math.max(0.0001, this.bus.gain.value), t);
    this.bus.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    const m = this.murmullo;
    window.setTimeout(() => { try { m?.stop(); } catch { /* ya parado */ } this.filtro.disconnect(); }, (dur + 0.6) * 1000 + ANTICIPO * 1000);
  }
}

export class Musica {
  private actual: Reproduccion | null = null;
  /** Lo que debería sonar (aunque el audio aún no esté desbloqueado). */
  private deseada: string | null = null;

  constructor(private contexto: () => { ctx: AudioContext; out: AudioNode } | null) {}

  poner(id: string | null, rapido = false) {
    const pista = id && PISTAS[id] ? id : null;
    this.deseada = pista;
    if (this.actual?.id === pista) return;
    this.actual?.parar(rapido);
    this.actual = null;
    const c = this.contexto();
    if (!pista || !c) return;
    this.actual = new Reproduccion(c.ctx, c.out, pista, PISTAS[pista]);
  }

  /** Al desbloquear el audio (primer toque), empieza lo que ya debía sonar. */
  reanudar() { if (this.deseada && !this.actual) this.poner(this.deseada); }

  agachar(cuanto: number, dur: number) { this.actual?.agachar(cuanto, dur); }

  get sonando() { return this.actual?.id ?? null; }
}
