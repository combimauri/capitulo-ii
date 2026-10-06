/**
 * Ambientes en capas, sintetizados (diseño técnico §12: «zumbido de telepantalla, calle, pub, túnel…»).
 * Cada mapa declara las suyas (propiedad «ambiente», separadas por comas) y aquí se funden al cambiar de sitio.
 * Una capa es un fondo continuo (ruido filtrado, zumbidos) más sucesos sueltos al azar (una tecla, un tubo
 * neumático, una gota, un perro lejos), para que no suene a bucle.
 */

type Fondo = { tipo: 'ruido'; color: 'blanco' | 'marron'; filtro: BiquadFilterType; f: number; q?: number; vol: number; ondula?: number }
  | { tipo: 'zumbido'; f: number; armonicos: number[]; vol: number };

interface Suceso {
  /** Segundos entre sucesos (mínimo, máximo). */
  cada: [number, number];
  /** Cuántos golpes seguidos (ráfagas de teclas). */
  rafaga?: [number, number];
  sonido: (ctx: AudioContext, out: AudioNode, t: number) => void;
}

interface Capa { fondos: Fondo[]; sucesos: Suceso[] }

// ---------------------------------------------------------------- sonidos sueltos
function clic(f: number, vol: number, dur = 0.03) {
  return (ctx: AudioContext, out: AudioNode, t: number) => {
    const osc = ctx.createOscillator(), g = ctx.createGain();
    osc.type = 'square'; osc.frequency.value = f * (0.9 + Math.random() * 0.2);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(out); osc.start(t); osc.stop(t + dur + 0.02);
  };
}

function soplo(corte: number, vol: number, dur: number, barrido = true) {
  return (ctx: AudioContext, out: AudioNode, t: number) => {
    const src = ctx.createBufferSource();
    src.buffer = ruido(ctx, dur, 'blanco');
    const fl = ctx.createBiquadFilter(), g = ctx.createGain();
    fl.type = 'bandpass'; fl.frequency.setValueAtTime(corte, t);
    if (barrido) fl.frequency.exponentialRampToValueAtTime(corte / 4, t + dur);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + dur * 0.2);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(fl).connect(g).connect(out); src.start(t);
  };
}

function gota(ctx: AudioContext, out: AudioNode, t: number) {
  const osc = ctx.createOscillator(), g = ctx.createGain();
  const f = 900 + Math.random() * 900;
  osc.type = 'sine'; osc.frequency.setValueAtTime(f, t); osc.frequency.exponentialRampToValueAtTime(f * 1.8, t + 0.05);
  g.gain.setValueAtTime(0.06, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
  osc.connect(g).connect(out); osc.start(t); osc.stop(t + 0.15);
}

function timbre(ctx: AudioContext, out: AudioNode, t: number) {
  const osc = ctx.createOscillator(), g = ctx.createGain();
  osc.type = 'sine'; osc.frequency.value = 3150;
  g.gain.setValueAtTime(0.025, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.9);
  osc.connect(g).connect(out); osc.start(t); osc.stop(t + 1);
}

function ladrido(ctx: AudioContext, out: AudioNode, t: number) {
  for (const d of [0, 0.32]) {
    const osc = ctx.createOscillator(), g = ctx.createGain(), fl = ctx.createBiquadFilter();
    osc.type = 'sawtooth'; osc.frequency.setValueAtTime(420, t + d); osc.frequency.exponentialRampToValueAtTime(260, t + d + 0.14);
    fl.type = 'bandpass'; fl.frequency.value = 900; fl.Q.value = 2;
    g.gain.setValueAtTime(0.0001, t + d); g.gain.exponentialRampToValueAtTime(0.02, t + d + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + d + 0.16);
    osc.connect(fl).connect(g).connect(out); osc.start(t + d); osc.stop(t + d + 0.2);
  }
}

/** Algo que podría ser un grito lejano. O una tubería. (El Minimor.) */
function lamento(ctx: AudioContext, out: AudioNode, t: number) {
  const osc = ctx.createOscillator(), g = ctx.createGain(), fl = ctx.createBiquadFilter();
  const f = 380 + Math.random() * 160;
  osc.type = 'sawtooth'; osc.frequency.setValueAtTime(f, t); osc.frequency.linearRampToValueAtTime(f * 1.25, t + 0.5);
  osc.frequency.linearRampToValueAtTime(f * 0.8, t + 1.4);
  fl.type = 'bandpass'; fl.frequency.value = 700; fl.Q.value = 6;
  g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.012, t + 0.3); g.gain.exponentialRampToValueAtTime(0.0001, t + 1.5);
  osc.connect(fl).connect(g).connect(out); osc.start(t); osc.stop(t + 1.6);
}

function tuberia(ctx: AudioContext, out: AudioNode, t: number) {
  for (const [d, f] of [[0, 140], [0.18, 132], [0.5, 150]] as const) {
    const osc = ctx.createOscillator(), g = ctx.createGain();
    osc.type = 'triangle'; osc.frequency.value = f;
    g.gain.setValueAtTime(0.03, t + d); g.gain.exponentialRampToValueAtTime(0.0001, t + d + 0.4);
    osc.connect(g).connect(out); osc.start(t + d); osc.stop(t + d + 0.45);
  }
}

function chasquidoVela(ctx: AudioContext, out: AudioNode, t: number) { clic(2600, 0.008, 0.012)(ctx, out, t); }

function cubiertos(ctx: AudioContext, out: AudioNode, t: number) {
  const osc = ctx.createOscillator(), g = ctx.createGain();
  osc.type = 'sine'; osc.frequency.value = 2400 + Math.random() * 1500;
  g.gain.setValueAtTime(0.018, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);
  osc.connect(g).connect(out); osc.start(t); osc.stop(t + 0.2);
}

const cache = new WeakMap<AudioContext, Record<string, AudioBuffer>>();
function ruido(ctx: AudioContext, dur: number, color: 'blanco' | 'marron'): AudioBuffer {
  const clave = `${color}${dur}`;
  const c = cache.get(ctx) ?? {};
  cache.set(ctx, c);
  if (c[clave]) return c[clave];
  const buf = ctx.createBuffer(1, Math.ceil(ctx.sampleRate * dur), ctx.sampleRate);
  const d = buf.getChannelData(0);
  let ultimo = 0;
  for (let i = 0; i < d.length; i++) {
    const w = Math.random() * 2 - 1;
    if (color === 'marron') { ultimo = (ultimo + 0.02 * w) / 1.02; d[i] = ultimo * 3.5; } else d[i] = w;
  }
  // fundido en las costuras para que el bucle no haga clic
  const n = Math.min(2000, d.length / 4);
  for (let i = 0; i < n; i++) { const k = i / n; d[i] *= k; d[d.length - 1 - i] *= k; }
  c[clave] = buf;
  return buf;
}

// ---------------------------------------------------------------- las capas
export const CAPAS: Record<string, Capa> = {
  /** La telepantalla: 50 Hz y sus armónicos, y de vez en cuando un chasquido de estática. */
  tele: {
    fondos: [{ tipo: 'zumbido', f: 50, armonicos: [1, 0.5, 0.25, 0.12], vol: 0.014 }],
    sucesos: [{ cada: [9, 22], sonido: soplo(6000, 0.02, 0.25, false) }],
  },
  /** El Minipax trabajando: máquinas de escribir, algún timbre de carro y el tubo neumático. */
  oficina: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'bandpass', f: 380, q: 0.7, vol: 0.08 }],
    sucesos: [
      { cada: [0.4, 2.2], rafaga: [3, 12], sonido: clic(1700, 0.02) },
      { cada: [8, 18], sonido: timbre },
      { cada: [14, 30], sonido: soplo(1800, 0.05, 0.9) },
    ],
  },
  cantina: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'bandpass', f: 480, q: 0.8, vol: 0.09, ondula: 0.3 }],
    sucesos: [{ cada: [0.8, 3.5], sonido: cubiertos }],
  },
  /** La calle: viento y la ciudad lejos. */
  calle: {
    fondos: [
      { tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 500, vol: 0.06, ondula: 0.5 },
      { tipo: 'ruido', color: 'blanco', filtro: 'bandpass', f: 900, q: 0.5, vol: 0.008, ondula: 0.6 },
    ],
    sucesos: [{ cada: [25, 50], sonido: ladrido }],
  },
  ruinas: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 420, vol: 0.07, ondula: 0.7 }],
    sucesos: [{ cada: [3, 9], sonido: (ctx, out, t) => clic(400, 0.01, 0.05)(ctx, out, t) }],
  },
  mercado: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'bandpass', f: 520, q: 0.7, vol: 0.12, ondula: 0.35 }],
    sucesos: [{ cada: [1.5, 5], sonido: cubiertos }],
  },
  noche: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 380, vol: 0.05, ondula: 0.8 }],
    sucesos: [{ cada: [18, 40], sonido: ladrido }, { cada: [6, 14], sonido: gota }],
  },
  /** El agua de los túneles, que corre hacia donde va el protagonista, y las gotas. */
  tunel: {
    fondos: [
      { tipo: 'ruido', color: 'blanco', filtro: 'bandpass', f: 1400, q: 0.6, vol: 0.025, ondula: 0.5 },
      { tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 160, vol: 0.08 },
    ],
    sucesos: [{ cada: [0.6, 3], sonido: gota }],
  },
  /** El Minimor: un zumbido constante y, muy de vez en cuando, algo que podría ser un grito. O una tubería. */
  minimor: {
    fondos: [{ tipo: 'zumbido', f: 60, armonicos: [1, 0.6, 0.3], vol: 0.018 }],
    sucesos: [{ cada: [25, 55], sonido: lamento }, { cada: [20, 45], sonido: tuberia }],
  },
  /** La cripta: el silencio de un lugar cerrado y antiguo. Apenas el aire y las velas. */
  cripta: {
    fondos: [{ tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 220, vol: 0.025 }],
    sucesos: [{ cada: [0.3, 2.5], sonido: chasquidoVela }, { cada: [6, 16], rafaga: [4, 14], sonido: clic(1300, 0.01) }],
  },
  calderas: {
    fondos: [
      { tipo: 'ruido', color: 'marron', filtro: 'lowpass', f: 260, vol: 0.09, ondula: 0.2 },
      { tipo: 'ruido', color: 'blanco', filtro: 'highpass', f: 5000, vol: 0.01 },
    ],
    sucesos: [{ cada: [7, 15], sonido: tuberia }],
  },
  /** Neones que zumban en el pasillo. */
  neon: {
    fondos: [{ tipo: 'zumbido', f: 100, armonicos: [1, 0.4, 0.4, 0.2, 0.2], vol: 0.009 }],
    sucesos: [],
  },
  goteo: {
    fondos: [],
    sucesos: [{ cada: [1.2, 4], sonido: gota }],
  },
  /** Las Mansiones Victoria: tuberías, una puerta lejos, la telepantalla de otro piso a través de la pared. */
  edificio: {
    fondos: [{ tipo: 'zumbido', f: 50, armonicos: [1, 0.3], vol: 0.008 }],
    sucesos: [{ cada: [15, 35], sonido: tuberia }],
  },
};

// ---------------------------------------------------------------- reproducción
class CapaSonando {
  private bus: GainNode;
  private fuentes: (AudioScheduledSourceNode)[] = [];
  private timers: number[] = [];

  constructor(private ctx: AudioContext, out: AudioNode, readonly id: string, capa: Capa) {
    this.bus = ctx.createGain();
    this.bus.gain.setValueAtTime(0.0001, ctx.currentTime);
    this.bus.gain.exponentialRampToValueAtTime(1, ctx.currentTime + 1.5);
    this.bus.connect(out);
    for (const f of capa.fondos) this.fondo(f);
    for (const s of capa.sucesos) this.programar(s);
  }

  private fondo(f: Fondo) {
    const ctx = this.ctx;
    const g = ctx.createGain();
    g.gain.value = f.vol;
    g.connect(this.bus);
    if (f.tipo === 'zumbido') {
      f.armonicos.forEach((peso, i) => {
        const osc = ctx.createOscillator();
        const go = ctx.createGain();
        osc.type = 'sine'; osc.frequency.value = f.f * (i + 1); go.gain.value = peso;
        osc.connect(go).connect(g); osc.start(); this.fuentes.push(osc);
      });
      return;
    }
    const src = ctx.createBufferSource();
    src.buffer = ruido(ctx, 6, f.color); src.loop = true;
    const fl = ctx.createBiquadFilter();
    fl.type = f.filtro; fl.frequency.value = f.f; if (f.q) fl.Q.value = f.q;
    src.connect(fl).connect(g);
    src.start(ctx.currentTime, Math.random() * 5);
    this.fuentes.push(src);
    if (f.ondula) {
      // el volumen respira despacio: ráfagas de viento, la gente que habla más o menos alto
      const lfo = ctx.createOscillator(), lg = ctx.createGain();
      lfo.frequency.value = 0.07 + Math.random() * 0.1; lg.gain.value = f.vol * f.ondula;
      lfo.connect(lg).connect(g.gain); lfo.start(); this.fuentes.push(lfo);
    }
  }

  private programar(s: Suceso) {
    const espera = (s.cada[0] + Math.random() * (s.cada[1] - s.cada[0])) * 1000;
    const id = window.setTimeout(() => {
      const t = this.ctx.currentTime + 0.05;
      const n = s.rafaga ? s.rafaga[0] + Math.floor(Math.random() * (s.rafaga[1] - s.rafaga[0] + 1)) : 1;
      for (let i = 0; i < n; i++) s.sonido(this.ctx, this.bus, t + i * (0.09 + Math.random() * 0.08));
      this.programar(s);
    }, espera);
    this.timers.push(id);
  }

  agachar(cuanto: number, dur: number) {
    const t = this.ctx.currentTime;
    this.bus.gain.cancelScheduledValues(t);
    this.bus.gain.setValueAtTime(Math.max(0.0001, this.bus.gain.value), t);
    this.bus.gain.exponentialRampToValueAtTime(cuanto, t + 0.2);
    this.bus.gain.setValueAtTime(cuanto, t + dur);
    this.bus.gain.exponentialRampToValueAtTime(1, t + dur + 1);
  }

  parar() {
    this.timers.forEach((id) => window.clearTimeout(id));
    const t = this.ctx.currentTime;
    this.bus.gain.cancelScheduledValues(t);
    this.bus.gain.setValueAtTime(Math.max(0.0001, this.bus.gain.value), t);
    this.bus.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
    const fuentes = this.fuentes;
    window.setTimeout(() => { for (const f of fuentes) { try { f.stop(); } catch { /* ya parada */ } } this.bus.disconnect(); }, 1400);
  }
}

export class Ambiente {
  private sonando = new Map<string, CapaSonando>();
  private deseadas: string[] = [];

  constructor(private contexto: () => { ctx: AudioContext; out: AudioNode } | null) {}

  /** Pone estas capas: las que ya suenan siguen sin cortes, las que sobran se funden. */
  poner(ids: string[]) {
    this.deseadas = ids.filter((id) => CAPAS[id]);
    const c = this.contexto();
    for (const [id, capa] of this.sonando) {
      if (!this.deseadas.includes(id)) { capa.parar(); this.sonando.delete(id); }
    }
    if (!c) return;
    for (const id of this.deseadas) {
      if (!this.sonando.has(id)) this.sonando.set(id, new CapaSonando(c.ctx, c.out, id, CAPAS[id]));
    }
  }

  reanudar() { this.poner(this.deseadas); }

  agachar(cuanto: number, dur: number) { for (const c of this.sonando.values()) c.agachar(cuanto, dur); }

  get capas() { return [...this.sonando.keys()]; }
}
