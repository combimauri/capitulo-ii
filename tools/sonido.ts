/**
 * Herramientas para medir la música (diseño técnico §12): renderiza una pista sin conexión en Node
 * (node-web-audio-api), mide su sonoridad (LUFS, BS.1770 con puerta), sus picos y su brillo, y analiza
 * la partitura (tonalidad, tempo, registro, disonancia, densidad) para comprobar que sostiene su emoción.
 *   npx tsx tools/sonido.ts [carpeta] [segundos]   → escribe un WAV por pista y un informe (ver el final)
 */
import { OfflineAudioContext } from 'node-web-audio-api';
import { PISTAS, renderizarPista, type Pista } from '../src/systems/Musica';
import { midi } from '../src/systems/partituras';

export const SR = 48000;

type Offline = new (canales: number, largo: number, sr: number) => globalThis.OfflineAudioContext;

/** Renderiza una pista en estéreo a 48 kHz (la frecuencia de los filtros de BS.1770). */
export async function renderizar(id: string, segundos: number): Promise<Float32Array[]> {
  const buf = await renderizarPista(id, segundos, SR, OfflineAudioContext as unknown as Offline);
  return [buf.getChannelData(0).slice(), buf.getChannelData(1).slice()];
}

// ------------------------------------------------------------------ medidas de la señal

function biquad(x: Float32Array, b: number[], a: number[]): Float32Array {
  const y = new Float32Array(x.length);
  let x1 = 0, x2 = 0, y1 = 0, y2 = 0;
  for (let i = 0; i < x.length; i++) {
    const v = b[0] * x[i] + b[1] * x1 + b[2] * x2 - a[1] * y1 - a[2] * y2;
    x2 = x1; x1 = x[i]; y2 = y1; y1 = v; y[i] = v;
  }
  return y;
}

/** Ponderación K de BS.1770 (coeficientes publicados para 48 kHz). */
const kPonderar = (x: Float32Array) => biquad(
  biquad(x, [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]),
  [1, -2, 1], [1, -1.99004745483398, 0.99007225036621],
);

/** Sonoridad integrada en LUFS (bloques de 400 ms con solape del 75 %, puertas absoluta y relativa). */
export function lufs(canales: Float32Array[], desde = 0): number {
  const k = canales.map((c) => kPonderar(c.subarray(Math.floor(desde * SR))));
  const bloque = Math.floor(0.4 * SR), paso = Math.floor(0.1 * SR);
  const energias: number[] = [];
  for (let i = 0; i + bloque <= k[0].length; i += paso) {
    let e = 0;
    for (const c of k) { let s = 0; for (let j = i; j < i + bloque; j++) s += c[j] * c[j]; e += s / bloque; }
    energias.push(e);
  }
  const l = (e: number) => -0.691 + 10 * Math.log10(e);
  const abs = energias.filter((e) => l(e) > -70);
  if (!abs.length) return -Infinity;
  const media = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;
  const rel = abs.filter((e) => l(e) > l(media(abs)) - 10);
  return l(media(rel));
}

/**
 * Lo que queda en el altavoz de un móvil: sin graves por debajo de unos 300 Hz (dos pasos altos de segundo orden).
 * Sirve para comprobar que una pista hecha de drones graves no desaparece en un teléfono.
 */
export function movil(canales: Float32Array[]): Float32Array[] {
  // Butterworth paso alto a 300 Hz (48 kHz), dos veces: 24 dB por octava
  const w = (2 * Math.PI * 300) / SR, q = Math.SQRT1_2, al = Math.sin(w) / (2 * q), cw = Math.cos(w), a0 = 1 + al;
  const b = [(1 + cw) / 2 / a0, -(1 + cw) / a0, (1 + cw) / 2 / a0], a = [1, (-2 * cw) / a0, (1 - al) / a0];
  return canales.map((c) => biquad(biquad(c, b, a), b, a));
}

/** El pico (en dBFS) de las dos pistas. */
export function pico(canales: Float32Array[]): number {
  let m = 0;
  for (const c of canales) for (const v of c) m = Math.max(m, Math.abs(v));
  return 20 * Math.log10(m || 1e-9);
}

/** Proporción de bloques de 400 ms en silencio (por debajo de -60 dBFS RMS): huecos dentro del bucle. */
export function silencio(canales: Float32Array[], desde = 0): number {
  const c = canales[0], bloque = Math.floor(0.4 * SR);
  let vacios = 0, total = 0;
  for (let i = Math.floor(desde * SR); i + bloque <= c.length; i += bloque) {
    let s = 0;
    for (let j = i; j < i + bloque; j++) s += c[j] * c[j] + canales[1][j] * canales[1][j];
    total++;
    if (10 * Math.log10(s / (2 * bloque) + 1e-12) < -60) vacios++;
  }
  return total ? vacios / total : 1;
}

/** Diferencia de sonoridad entre la izquierda y la derecha (dB): la mezcla no debe cargarse a un lado. */
export function desequilibrio(canales: Float32Array[]): number {
  const e = canales.map((c) => c.reduce((a, v) => a + v * v, 0));
  return Math.abs(10 * Math.log10((e[0] + 1e-12) / (e[1] + 1e-12)));
}

// ------------------------------------------------------------------ análisis de la partitura

/** Perfiles tonales de Krumhansl-Kessler (mayor y menor). */
const MAYOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88];
const MENOR = [6.33, 2.68, 3.52, 5.38, 2.6, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17];
const NOMBRES = ['do', 'do#', 're', 'mib', 'mi', 'fa', 'fa#', 'sol', 'lab', 'la', 'sib', 'si'];
const PERCUSION = new Set(['redoble', 'bombo', 'tecla', 'timbre', 'carro', 'latido', 'tictac', 'roce']);

function correlacion(a: number[], b: number[]) {
  const ma = a.reduce((x, y) => x + y) / 12, mb = b.reduce((x, y) => x + y) / 12;
  let num = 0, da = 0, db = 0;
  for (let i = 0; i < 12; i++) { num += (a[i] - ma) * (b[i] - mb); da += (a[i] - ma) ** 2; db += (b[i] - mb) ** 2; }
  return num / Math.sqrt(da * db || 1);
}

export interface Rasgos {
  /** Tonalidad más probable, su modo y cuánto se parece la partitura a ella (0..1). */
  tonalidad: string;
  modo: 'mayor' | 'menor';
  claridad: number;
  bpm: number;
  /** Nota MIDI media (ponderada por duración) de lo que tiene altura. */
  registro: number;
  /** Proporción del tiempo con intervalos ásperos sonando a la vez (segundas menores, tritonos, séptimas mayores). */
  disonancia: number;
  /** Ataques por segundo (todas las voces). */
  densidad: number;
  /** Proporción de ataques de percusión. */
  percusion: number;
  /** Cuántas veces se repite el patrón más común de ataques por compás (ostinato: 0..1). */
  ostinato: number;
}

export function rasgos(p: Pista): Rasgos {
  const tonales = p.notas.filter((n) => !PERCUSION.has(n.voz));
  const perfil = new Array(12).fill(0);
  for (const n of tonales) perfil[midi(n.n) % 12] += n.d * (n.v ?? 1);
  let mejor = { tonalidad: 'do', modo: 'mayor' as 'mayor' | 'menor', claridad: -1 };
  for (let i = 0; i < 12; i++) {
    for (const [modo, ref] of [['mayor', MAYOR], ['menor', MENOR]] as const) {
      const rot = ref.map((_, k) => ref[(k - i + 12) % 12]);
      const c = correlacion(perfil, rot);
      if (c > mejor.claridad) mejor = { tonalidad: NOMBRES[i], modo, claridad: c };
    }
  }
  const dur = tonales.reduce((a, n) => a + n.d, 0) || 1;
  const registro = tonales.reduce((a, n) => a + midi(n.n) * n.d, 0) / dur;
  // disonancia: se muestrea la partitura cada medio pulso y se miran las clases de altura que suenan juntas
  let asperos = 0, muestras = 0;
  for (let b = 0; b < p.pulsos; b += 0.5) {
    const suenan = [...new Set(tonales.filter((n) => n.b <= b && b < n.b + n.d).map((n) => midi(n.n) % 12))];
    if (suenan.length < 2) continue;
    muestras++;
    if (suenan.some((x, i) => suenan.slice(i + 1).some((y) => [1, 6, 11].includes(Math.abs(x - y))))) asperos++;
  }
  const segundos = (p.pulsos * 60) / p.bpm;
  // ostinato: patrón de ataques (cuantizado a semicorcheas) de cada compás de 4 pulsos
  const patrones = new Map<string, number>();
  for (let c = 0; c < Math.floor(p.pulsos / 4); c++) {
    const ataques = p.notas.filter((n) => n.b >= c * 4 && n.b < c * 4 + 4).map((n) => `${Math.round((n.b - c * 4) * 4)}${n.voz}`);
    const clave = [...new Set(ataques)].sort().join(',');
    patrones.set(clave, (patrones.get(clave) ?? 0) + 1);
  }
  const compases = Math.max(1, Math.floor(p.pulsos / 4));
  return {
    ...mejor,
    bpm: p.bpm,
    registro,
    disonancia: muestras ? asperos / muestras : 0,
    densidad: p.notas.length / segundos,
    percusion: p.notas.length ? p.notas.filter((n) => PERCUSION.has(n.voz)).length / p.notas.length : 0,
    ostinato: Math.max(0, ...patrones.values()) / compases,
  };
}

// ------------------------------------------------------------------ objetivos de sonoridad

/** Lo que suena de fondo mientras se lee y lo que debe golpear: dos niveles (LUFS, antes del volumen general). */
const FONDO = new Set(['rutina', 'duda', 'tension', 'nostalgia', 'calidez', 'frustracion', 'vacio', 'alegria']);
export const objetivo = (p: Pista): number | null => (p.diegetica ? null : FONDO.has(p.emocion) ? -32 : -29.5);

// ------------------------------------------------------------------ WAV

export function wav(canales: Float32Array[]): Buffer {
  const n = canales[0].length, buf = Buffer.alloc(44 + n * 4);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + n * 4, 4); buf.write('WAVE', 8);
  buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34);
  buf.write('data', 36); buf.writeUInt32LE(n * 4, 40);
  for (let i = 0; i < n; i++) for (let c = 0; c < 2; c++) {
    buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, canales[c][i])) * 32767), 44 + i * 4 + c * 2);
  }
  return buf;
}

/** Sonoridad de cada voz de una pista por separado (para equilibrar la mezcla). */
export async function porVoces(id: string, segundos: number): Promise<Record<string, number>> {
  const p = PISTAS[id], todas = p.notas;
  const r: Record<string, number> = {};
  try {
    for (const voz of [...new Set(todas.map((n) => n.voz))]) {
      p.notas = todas.filter((n) => n.voz === voz);
      r[voz] = lufs(await renderizar(id, segundos), 1);
    }
  } finally {
    p.notas = todas;
  }
  return r;
}

// ------------------------------------------------------------------ informe por consola
if (process.argv[1]?.endsWith('sonido.ts') && process.argv[2] === '--calibrar') {
  // propone el volumen de cada pista para que llegue a su objetivo
  for (const id of Object.keys(PISTAS)) {
    const o = objetivo(PISTAS[id]);
    if (o === null) continue;
    const l = lufs(await renderizar(id, Math.min(75, (PISTAS[id].pulsos * 60) / PISTAS[id].bpm + 3)), 2);
    console.log(`${id} ${PISTAS[id].volumen} ${(PISTAS[id].volumen * 10 ** ((o - l) / 20)).toFixed(2)} ${l.toFixed(1)}`);
  }
} else if (process.argv[1]?.endsWith('sonido.ts') && process.argv[2] === '--voces') {
  for (const id of process.argv[3].split(',')) {
    const r = await porVoces(id, Number(process.argv[4]) || 30);
    console.log(id.padEnd(16), Object.entries(r).map(([v, l]) => `${v} ${l.toFixed(1)}`).join(' · '));
  }
} else if (process.argv[1]?.endsWith('sonido.ts')) {
  const fs = await import('node:fs');
  const carpeta = process.argv[2] ?? 'dist-sonido';
  const segundos = Number(process.argv[3]) || 40;
  const solo = process.argv[4]?.split(',');
  fs.mkdirSync(carpeta, { recursive: true });
  console.log('pista                  emoción      LUFS   pico  silencio  tonalidad      claridad bpm  reg  disonancia dens  ostinato');
  for (const id of Object.keys(PISTAS)) {
    if (solo && !solo.includes(id)) continue;
    const c = await renderizar(id, segundos);
    fs.writeFileSync(`${carpeta}/${id}.wav`, wav(c));
    const r = rasgos(PISTAS[id]);
    console.log(`${id.padEnd(22)} ${PISTAS[id].emocion.padEnd(11)} ${lufs(c, 2).toFixed(1).padStart(6)} ${pico(c).toFixed(1).padStart(5)} ${(silencio(c, 2) * 100).toFixed(0).padStart(6)} %  `
      + `${`${r.tonalidad} ${r.modo}`.padEnd(13)} ${r.claridad.toFixed(2)}   ${String(r.bpm).padEnd(4)} ${r.registro.toFixed(0).padStart(3)}  ${r.disonancia.toFixed(2).padStart(6)}    ${r.densidad.toFixed(1).padStart(4)}  ${r.ostinato.toFixed(2)}`);
  }
}
