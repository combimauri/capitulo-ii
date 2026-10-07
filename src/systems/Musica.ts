/**
 * Música sintetizada en tiempo real (diseño técnico §12). Las partituras están en partituras.ts; aquí, el
 * motor: un planificador que programa las notas por delante del reloj de audio (el bucle no tiene costuras),
 * las voces de los instrumentos, el paneo de cada voz y una sala (reverberación) por pista.
 * También sabe renderizar una pista sin conexión (OfflineAudioContext), para las pruebas del sonido.
 */
import { PISTAS, frecuencia, type Nota, type Pista, type Voz } from './partituras';

export { PISTAS, type Pista, type Nota, type Voz } from './partituras';

const ANTICIPO = 0.5;      // segundos que se programan por delante
const FUNDIDO = 1.4;

/** Dónde suena cada voz en el estéreo (-1 izquierda, 1 derecha): una pequeña orquesta delante del jugador. */
const PANEO: Partial<Record<Voz, number>> = {
  acorde: -0.2, piano: 0.12, piano_limpio: 0.1, cuerdas: -0.15, tremolo: 0.3, pizzicato: 0.25, lamento: 0.2,
  caja: 0.08, campana: -0.15, coro: -0.1, organo: 0, metal: -0.2, trompeta: 0.15, tictac: 0.35, roce: -0.4,
  pulso: -0.15, redoble: 0.2, timbal: -0.1,
};

/** Las voces que se tocan «a mano»: un poco de imprecisión en el tiempo y en la fuerza las hace humanas. */
const HUMANAS = new Set<Voz>(['piano', 'piano_limpio', 'bajo', 'acorde', 'pizzicato', 'lamento', 'tarareo', 'caja']);

type Ctx = BaseAudioContext;

const cacheOndas = new WeakMap<Ctx, Record<string, PeriodicWave>>();
/** Un timbre fijo a partir de sus armónicos (una sola oscilación por nota, barata en el móvil). */
function onda(ctx: Ctx, clave: string, armonicos: number[]): PeriodicWave {
  const c = cacheOndas.get(ctx) ?? {};
  cacheOndas.set(ctx, c);
  if (!c[clave]) {
    const real = new Float32Array(armonicos.length + 1), imag = new Float32Array(armonicos.length + 1);
    armonicos.forEach((a, i) => { imag[i + 1] = a; });
    c[clave] = ctx.createPeriodicWave(real, imag);
  }
  return c[clave];
}

const cacheSalas = new WeakMap<Ctx, Record<string, AudioBuffer>>();
/**
 * La respuesta de una sala, inventada: ruido estéreo que se apaga en `cola` segundos y pierde los agudos
 * antes que los graves (como el aire y las paredes). Breve = una habitación; larga = una cripta.
 */
function sala(ctx: Ctx, cola: number): AudioBuffer {
  const clave = cola.toFixed(2);
  const c = cacheSalas.get(ctx) ?? {};
  cacheSalas.set(ctx, c);
  if (c[clave]) return c[clave];
  const sr = ctx.sampleRate, n = Math.ceil(sr * cola), retardo = Math.floor(sr * 0.018);
  const buf = ctx.createBuffer(2, n + retardo, sr);
  for (let canal = 0; canal < 2; canal++) {
    const d = buf.getChannelData(canal);
    let lp = 0;
    for (let i = 0; i < n; i++) {
      const t = i / sr;
      const amp = Math.exp((-6.9 * t) / cola);
      // un filtro de un polo que se cierra con el tiempo: la cola se oscurece
      const k = 0.15 + 0.8 * Math.min(1, t / cola);
      lp = lp * k + (Math.random() * 2 - 1) * (1 - k);
      d[i + retardo] = lp * amp * (1.4 + k);
    }
  }
  c[clave] = buf;
  return buf;
}

/** Una pista sonando: su bus (para fundirla sin cortar las notas ya programadas) y su planificador. */
class Reproduccion {
  readonly bus: GainNode;
  private filtro: BiquadFilterNode;
  private salidas: Partial<Record<Voz, AudioNode>> = {};
  private timer = 0;
  private inicio: number;
  private siguiente = 0;          // índice de la próxima nota dentro del bucle
  private vuelta = 0;
  private murmullo: AudioBufferSourceNode | null = null;
  private proximoVaso = 0;
  private nodosFinales: AudioNode[] = [];

  constructor(private ctx: Ctx, out: AudioNode, readonly id: string, private p: Pista, offline = false) {
    this.bus = ctx.createGain();
    if (offline) this.bus.gain.value = p.volumen;
    else {
      this.bus.gain.setValueAtTime(0.0001, ctx.currentTime);
      this.bus.gain.exponentialRampToValueAtTime(p.volumen, ctx.currentTime + (p.entrada ?? FUNDIDO));
    }
    this.filtro = ctx.createBiquadFilter();
    this.filtro.type = 'lowpass';
    this.filtro.frequency.value = p.corte ?? 12000;
    let ultimo: AudioNode = this.bus.connect(this.filtro);
    if (p.altavoz) {
      // el altavoz: satura y recorta graves y agudos
      const sat = ctx.createWaveShaper();
      const curva = new Float32Array(1024);
      for (let i = 0; i < curva.length; i++) { const x = (i / (curva.length - 1)) * 2 - 1; curva[i] = Math.tanh(x * 3.2); }
      sat.curve = curva;
      const banda = ctx.createBiquadFilter();
      banda.type = 'bandpass'; banda.frequency.value = 1300; banda.Q.value = 0.9;
      ultimo = ultimo.connect(sat).connect(banda);
    }
    ultimo.connect(out);
    this.nodosFinales.push(ultimo);
    if (p.sala) {
      // la sala: una parte de la señal va a la reverberación y vuelve mezclada
      const envio = ctx.createGain(), conv = ctx.createConvolver();
      envio.gain.value = p.sala;
      conv.normalize = true;
      conv.buffer = sala(ctx, p.cola ?? 2.2);
      ultimo.connect(envio).connect(conv).connect(out);
      this.nodosFinales.push(conv);
    }
    this.p.notas.sort((a, b) => a.b - b.b);
    this.inicio = ctx.currentTime + (offline ? 0.05 : 0.15);
    if (p.murmullo) this.empezarMurmullo(p.murmullo);
    if (!offline) {
      this.timer = window.setInterval(() => this.programar(this.ctx.currentTime + ANTICIPO), 100);
      this.programar(ctx.currentTime + ANTICIPO);
    }
  }

  private get pulso() { return 60 / this.p.bpm; }

  /** Programa las notas que caen antes de `limite` (en el renderizado sin conexión, toda la pista de una vez). */
  programar(limite: number) {
    if (!this.p.notas.length) return;
    const largo = this.p.pulsos * this.pulso;
    for (let guarda = 0; guarda < 100000; guarda++) {
      if (this.siguiente >= this.p.notas.length) { this.siguiente = 0; this.vuelta++; }
      const nota = this.p.notas[this.siguiente];
      const t = this.inicio + this.vuelta * largo + nota.b * this.pulso;
      if (t > limite) break;
      if (t >= this.ctx.currentTime - 0.05) this.tocar(nota, t);
      this.siguiente++;
    }
    if (this.p.murmullo) {
      while (this.proximoVaso < limite) {
        this.proximoVaso = Math.max(this.proximoVaso, this.ctx.currentTime) + 2 + Math.random() * 5;
        this.vaso(this.proximoVaso);
      }
    }
  }

  /** La salida de cada voz: su sitio en el estéreo. */
  private salida(voz: Voz): AudioNode {
    const s = this.salidas[voz];
    if (s) return s;
    // un altavoz es una sola fuente: todo sale del mismo sitio
    const pan = this.p.altavoz ? 0 : this.p.paneo?.[voz] ?? PANEO[voz] ?? 0;
    let nodo: AudioNode = this.bus;
    if (pan && typeof this.ctx.createStereoPanner === 'function') {
      const p = this.ctx.createStereoPanner();
      p.pan.value = pan;
      p.connect(this.bus);
      nodo = p;
    }
    this.salidas[voz] = nodo;
    return nodo;
  }

  private tocar(nota: Nota, t: number) {
    const des = this.p.desafino ?? 0;
    const humana = HUMANAS.has(nota.voz) && !this.p.rigida;
    if (humana) t += Math.random() * 0.012;
    const f = frecuencia(nota.n) * (1 + (Math.random() - 0.5) * des), d = nota.d * this.pulso;
    const v = (nota.v ?? 1) * (humana ? 0.9 + Math.random() * 0.2 : 1);
    const out = this.salida(nota.voz);
    switch (nota.voz) {
      case 'tarareo': return this.tararear(out, f, t, d, v);
      case 'bajo': return this.piano(out, f, t, d + 0.25, 0.09 * v, 0.02);
      case 'acorde': return this.piano(out, f, t, d, 0.035 * v, 0.02);
      case 'piano_limpio': return this.piano(out, f, t, d + 0.6, 0.085 * v, 0.004);
      case 'trompeta': return this.metal(out, f, t, d * 0.92, 0.085 * v, 2600);
      case 'metal': return this.metal(out, f, t, d * 0.7, 0.03 * v, 1500);
      case 'tuba': return this.metal(out, f, t, d * 0.8, 0.09 * v, 500);
      case 'redoble': return this.golpeRuido(out, t, 0.09, 1800, 0.12 * v, 'highpass');
      case 'bombo': return this.bombo(out, t, v);
      case 'caja': return this.caja(out, f, t, v);
      case 'cuerdas': return this.cuerdas(out, f, t, d, 0.03 * v);
      case 'tremolo': return this.cuerdas(out, f, t, d, 0.026 * v, 7.5);
      case 'pizzicato': return this.piano(out, f, t, 0.35, 0.06 * v, 0.004);
      case 'tecla': return this.golpeRuido(out, t + Math.random() * 0.02, 0.035, 2600, (0.3 + Math.random() * 0.15) * v, 'bandpass');
      case 'timbre': return this.caja(out, 3150, t, v);
      case 'carro': return this.golpeRuido(out, t, 0.35, 1400, 0.18 * v, 'bandpass', true);
      case 'organo': return this.organo(out, f, t, d, 0.05 * v);
      case 'campana': return this.campana(out, f, t, 0.05 * v);
      case 'latido': return this.latido(out, t, v);
      case 'lamento': return this.lamento(out, f, t, d, 0.07 * v);
      case 'coro': return this.coro(out, f, t, d, 0.03 * v);
      case 'timbal': return this.timbal(out, f, t, v);
      case 'pulso': return this.pulsoSint(out, f, t, d, 0.1 * v);
      case 'dron': return this.dron(out, f, t, d, 0.05 * v);
      case 'tictac': return this.golpeRuido(out, t, 0.03, nota.n.endsWith('5') ? 3400 : 2300, 0.5 * v, 'bandpass');
      case 'roce': return this.roce(out, f, t, d, 0.05 * v);
      default: return this.piano(out, f, t, d + 0.3, 0.1 * v, 0.016);
    }
  }

  /** Metales: diente de sierra con un filtro que se abre en el ataque, como una boquilla. */
  private metal(out: AudioNode, f: number, t: number, dur: number, vol: number, brillo: number) {
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
    osc.connect(fl); osc2.connect(o2).connect(fl); fl.connect(g).connect(out);
    for (const o of [osc, osc2]) { o.start(t); o.stop(t + dur + 0.08); }
  }

  private golpeRuido(out: AudioNode, t: number, dur: number, f: number, vol: number, tipo: BiquadFilterType, barrido = false) {
    const ctx = this.ctx;
    const src = ctx.createBufferSource(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
    src.buffer = ruidoBlanco(ctx);
    fl.type = tipo; fl.frequency.setValueAtTime(f, t);
    if (barrido) fl.frequency.exponentialRampToValueAtTime(f * 3, t + dur);
    g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(fl).connect(g).connect(out);
    src.start(t, Math.random() * 1.5, dur + 0.02);
  }

  private bombo(out: AudioNode, t: number, v: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(120, t); osc.frequency.exponentialRampToValueAtTime(48, t + 0.18);
    g.gain.setValueAtTime(0.22 * v, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.3);
    osc.connect(g).connect(out);
    osc.start(t); osc.stop(t + 0.32);
    this.golpeRuido(out, t, 0.04, 1200, 0.08 * v, 'lowpass');   // la maza contra el parche
  }

  /** Caja de música: púa metálica, mucho armónico inarmónico y una cola larga. */
  private caja(out: AudioNode, f: number, t: number, v: number) {
    const ctx = this.ctx;
    for (const [mult, peso, cola] of [[1, 1, 1.4], [2.76, 0.25, 0.5], [5.4, 0.08, 0.25]] as const) {
      const osc = ctx.createOscillator(), g = ctx.createGain();
      osc.type = 'sine'; osc.frequency.value = f * mult;
      g.gain.setValueAtTime(0.06 * peso * v, t); g.gain.exponentialRampToValueAtTime(0.0001, t + cola);
      osc.connect(g).connect(out);
      osc.start(t); osc.stop(t + cola + 0.05);
    }
  }

  /**
   * Cuerdas: tres sierras desafinadas entre sí, ataque y caída lentos, sin agudos.
   * Con `tremolo` (Hz), el arco tiembla: el miedo de las películas de antes.
   */
  private cuerdas(out: AudioNode, f: number, t: number, dur: number, vol: number, tremolo = 0) {
    const ctx = this.ctx;
    const fl = ctx.createBiquadFilter(), g = ctx.createGain();
    fl.type = 'lowpass'; fl.frequency.value = Math.min(tremolo ? 4200 : 3200, f * (tremolo ? 6 : 4));
    // legato: el ataque y la caída son rectas que se cruzan con la nota siguiente (sin hueco entre acordes)
    const ataque = Math.min(0.35, dur * 0.4), fin = t + dur + 0.35;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol, t + ataque);
    g.gain.setValueAtTime(vol, Math.max(t + ataque, t + dur - 0.05));
    g.gain.linearRampToValueAtTime(0, fin);
    const fuentes: AudioScheduledSourceNode[] = [];
    if (tremolo) {
      const am = ctx.createGain(), lfo = ctx.createOscillator(), prof = ctx.createGain();
      am.gain.value = 0.55; lfo.frequency.value = tremolo * (0.95 + Math.random() * 0.1); prof.gain.value = 0.45;
      lfo.connect(prof).connect(am.gain);
      fl.connect(am).connect(g);
      fuentes.push(lfo);
    } else fl.connect(g);
    g.connect(out);
    for (const det of [-0.004, 0, 0.005]) {
      const osc = ctx.createOscillator();
      osc.type = 'sawtooth'; osc.frequency.value = f * (1 + det);
      osc.connect(fl); fuentes.push(osc);
    }
    for (const o of fuentes) { o.start(t); o.stop(fin + 0.05); }
  }

  /** Piano de pared viejo: dos cuerdas que no coinciden, un armónico y un ataque seco. */
  private piano(out: AudioNode, f: number, t: number, dur: number, vol: number, desafino: number) {
    const ctx = this.ctx;
    const g = ctx.createGain();
    // las notas graves suenan más tiempo que las agudas
    const caida = Math.min(dur, 0.6 + 2400 / Math.max(80, f));
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.006);
    g.gain.exponentialRampToValueAtTime(vol * 0.35, t + 0.22);
    g.gain.exponentialRampToValueAtTime(0.0001, t + caida);
    g.connect(out);
    const d = 1 + (Math.random() - 0.5) * desafino;
    for (const [mult, tipo, peso] of [[1, 'triangle', 1], [1.011 - (0.016 - Math.min(desafino, 0.016)) * 0.5, 'triangle', 0.7], [2.006, 'sine', 0.22]] as const) {
      const osc = ctx.createOscillator();
      const go = ctx.createGain();
      osc.type = tipo;
      osc.frequency.value = f * d * mult;
      go.gain.value = peso;
      osc.connect(go).connect(g);
      osc.start(t);
      osc.stop(t + caida + 0.05);
    }
  }

  /** Una voz que tararea con la boca cerrada: senoidal con vibrato, ataque blando y algo de nariz. */
  private tararear(out: AudioNode, f: number, t: number, dur: number, v: number) {
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
    const fin = t + dur * 0.96, vol = 0.11 * v;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.07);
    g.gain.setValueAtTime(vol * 0.85, Math.max(t + 0.08, fin - 0.12));
    g.gain.exponentialRampToValueAtTime(0.0001, fin);
    osc.connect(g); armonico.connect(ga).connect(g);
    g.connect(out);
    for (const o of [osc, armonico, vib]) { o.start(t); o.stop(fin + 0.05); }
  }

  /** Órgano de iglesia (la cripta): registros de 16', 8', 4' y 2 2/3', con el aire que entra en el tubo. */
  private organo(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    // legato, como quien no levanta los dedos: la nota siguiente entra mientras esta se apaga
    const g = ctx.createGain(), fin = t + dur;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol, t + 0.08);
    g.gain.setValueAtTime(vol, Math.max(t + 0.08, fin));
    g.gain.linearRampToValueAtTime(0, fin + 0.3);
    g.connect(out);
    const osc = ctx.createOscillator(), sub = ctx.createOscillator(), gs = ctx.createGain();
    osc.setPeriodicWave(onda(ctx, 'organo', [1, 0.55, 0.32, 0.4, 0.12, 0.18, 0.05, 0.1]));
    osc.frequency.value = f;
    sub.type = 'sine'; sub.frequency.value = f / 2; gs.gain.value = 0.45;
    osc.connect(g); sub.connect(gs).connect(g);
    for (const o of [osc, sub]) { o.start(t); o.stop(fin + 0.4); }
  }

  /**
   * Campana de iglesia (San Clemente): parciales inarmónicos (el «hum» una octava por debajo, la tercera
   * menor que le da su color triste) que se apagan cada uno a su ritmo.
   */
  private campana(out: AudioNode, f: number, t: number, vol: number) {
    const ctx = this.ctx;
    const parciales: [number, number, number][] = [[0.5, 0.5, 5], [1, 1, 3.5], [1.19, 0.45, 2.4], [1.5, 0.3, 1.8], [2, 0.32, 1.5], [2.74, 0.16, 0.8], [3.76, 0.08, 0.5]];
    for (const [mult, peso, cola] of parciales) {
      const osc = ctx.createOscillator(), g = ctx.createGain();
      osc.type = 'sine'; osc.frequency.value = f * mult;
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(vol * peso, t + 0.004);
      g.gain.exponentialRampToValueAtTime(0.0001, t + cola);
      osc.connect(g).connect(out);
      osc.start(t); osc.stop(t + cola + 0.05);
    }
  }

  /** El corazón: dos golpes sordos, el segundo más flojo. */
  private latido(out: AudioNode, t: number, v: number) {
    const ctx = this.ctx;
    for (const [d, peso] of [[0, 1], [0.24, 0.6]] as const) {
      const osc = ctx.createOscillator(), g = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(70, t + d); osc.frequency.exponentialRampToValueAtTime(38, t + d + 0.14);
      g.gain.setValueAtTime(0.0001, t + d);
      g.gain.exponentialRampToValueAtTime(0.32 * peso * v, t + d + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t + d + 0.2);
      osc.connect(g).connect(out);
      osc.start(t + d); osc.stop(t + d + 0.22);
      // el golpe en el pecho: lo que se oye del latido en un altavoz pequeño
      this.golpeRuido(out, t + d, 0.07, 650, 0.22 * peso * v, 'lowpass');
    }
  }

  /**
   * Un clarinete solo, en registro grave (la tristeza): armónicos impares, la nota que entra un poco baja
   * y se afina, y un vibrato que llega tarde, como en quien sopla con cuidado.
   */
  private lamento(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), vib = ctx.createOscillator(), vibG = ctx.createGain();
    const fl = ctx.createBiquadFilter(), g = ctx.createGain();
    osc.setPeriodicWave(onda(ctx, 'clarinete', [1, 0.04, 0.42, 0.03, 0.22, 0.02, 0.12, 0.01, 0.06]));
    osc.frequency.setValueAtTime(f * 0.985, t);
    osc.frequency.exponentialRampToValueAtTime(f, t + 0.07);
    vib.frequency.value = 4.8;
    vibG.gain.setValueAtTime(0, t);
    vibG.gain.linearRampToValueAtTime(0, t + Math.min(0.35, dur * 0.4));
    vibG.gain.linearRampToValueAtTime(f * 0.006, t + Math.min(0.9, dur * 0.8));
    vib.connect(vibG).connect(osc.frequency);
    fl.type = 'lowpass'; fl.frequency.value = Math.min(3000, f * 5); fl.Q.value = 0.5;
    const fin = t + dur * 0.97;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.08);
    g.gain.exponentialRampToValueAtTime(vol * 0.8, Math.max(t + 0.09, fin - 0.15));
    g.gain.exponentialRampToValueAtTime(0.0001, fin + 0.12);
    osc.connect(fl).connect(g).connect(out);
    for (const o of [osc, vib]) { o.start(t); o.stop(fin + 0.15); }
  }

  /** Un coro que no dice nada («aaa»): tres voces desafinadas y dos formantes de vocal abierta. */
  private coro(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const fin = t + dur;
    const g = ctx.createGain();
    const ataque = Math.min(0.5, dur * 0.4);
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol, t + ataque);
    g.gain.setValueAtTime(vol, Math.max(t + ataque, fin - 0.05));
    g.gain.linearRampToValueAtTime(0, fin + 0.4);
    g.connect(out);
    const formantes = [[700, 1, 6], [1150, 0.6, 8], [2600, 0.18, 10]] as const;
    const mezcla = ctx.createGain();
    for (const [ff, peso, q] of formantes) {
      const bp = ctx.createBiquadFilter(), gp = ctx.createGain();
      bp.type = 'bandpass'; bp.frequency.value = ff; bp.Q.value = q; gp.gain.value = peso * 3;
      mezcla.connect(bp).connect(gp).connect(g);
    }
    const vib = ctx.createOscillator(), vibG = ctx.createGain();
    vib.frequency.value = 5.1; vibG.gain.value = f * 0.005;
    vib.connect(vibG);
    const fuentes: AudioScheduledSourceNode[] = [vib];
    for (const det of [-0.006, 0.0, 0.007]) {
      const osc = ctx.createOscillator();
      osc.type = 'sawtooth'; osc.frequency.value = f * (1 + det);
      vibG.connect(osc.frequency);
      osc.connect(mezcla); fuentes.push(osc);
    }
    for (const o of fuentes) { o.start(t); o.stop(fin + 0.45); }
  }

  /** Timbal: un golpe con altura que se hunde un poco, y el parche que sigue vibrando. */
  private timbal(out: AudioNode, f: number, t: number, v: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), osc2 = ctx.createOscillator(), g = ctx.createGain(), g2 = ctx.createGain();
    osc.type = 'sine'; osc2.type = 'sine';
    osc.frequency.setValueAtTime(f * 1.04, t); osc.frequency.exponentialRampToValueAtTime(f, t + 0.08);
    osc2.frequency.value = f * 1.5;
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.3 * v, t + 0.006); g.gain.exponentialRampToValueAtTime(0.0001, t + 1.6);
    g2.gain.setValueAtTime(0.1 * v, t); g2.gain.exponentialRampToValueAtTime(0.0001, t + 0.5);
    osc.connect(g).connect(out); osc2.connect(g2).connect(out);
    const fuentes = [osc, osc2];
    // los modos altos del parche (1,98 y 2,44 veces la nota): dan la altura y se oyen en cualquier altavoz
    for (const [mult, peso, cola] of [[1.98, 0.09, 0.9], [2.44, 0.06, 0.6], [2.9, 0.035, 0.4]] as const) {
      const o = ctx.createOscillator(), go = ctx.createGain();
      o.type = 'sine'; o.frequency.value = f * mult;
      go.gain.setValueAtTime(peso * v, t); go.gain.exponentialRampToValueAtTime(0.0001, t + cola);
      o.connect(go).connect(out); fuentes.push(o);
    }
    for (const o of fuentes) { o.start(t); o.stop(t + 1.65); }
    this.golpeRuido(out, t, 0.08, 900, 0.14 * v, 'lowpass');
  }

  /** Pulso sintético apagado (la tensión de las misiones): onda cuadrada, filtro que se cierra enseguida. */
  private pulsoSint(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const osc = ctx.createOscillator(), fl = ctx.createBiquadFilter(), g = ctx.createGain();
    osc.type = 'square'; osc.frequency.value = f;
    fl.type = 'lowpass'; fl.Q.value = 4;
    // el ataque, brillante (se oye en cualquier altavoz); luego el filtro se cierra sobre la nota
    fl.frequency.setValueAtTime(Math.min(4000, Math.max(1400, f * 8)), t);
    fl.frequency.exponentialRampToValueAtTime(Math.max(120, f * 1.2), t + Math.min(0.25, dur));
    const fin = t + Math.min(dur, 0.4);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, fin);
    osc.connect(fl).connect(g).connect(out);
    osc.start(t); osc.stop(fin + 0.02);
  }

  /** Dron: un acorde grave que respira (el filtro se abre y se cierra muy despacio). */
  private dron(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const fin = t + dur;
    const fl = ctx.createBiquadFilter(), g = ctx.createGain(), lfo = ctx.createOscillator(), lfoG = ctx.createGain();
    // el filtro deja pasar los armónicos medios: en el altavoz de un móvil, sin graves, el oído reconstruye la nota
    fl.type = 'lowpass'; fl.frequency.value = Math.min(1800, f * 6 + 260); fl.Q.value = 1.5;
    lfo.frequency.value = 0.08 + Math.random() * 0.06; lfoG.gain.value = Math.min(900, f * 2 + 120);
    lfo.connect(lfoG).connect(fl.frequency);
    const ataque = Math.min(2.5, dur * 0.3);
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol, t + ataque);
    g.gain.setValueAtTime(vol, Math.max(t + ataque, fin - 0.2));
    g.gain.linearRampToValueAtTime(0, fin + 1);
    fl.connect(g).connect(out);
    const fuentes: AudioScheduledSourceNode[] = [lfo];
    // dos sierras casi iguales (el batido lento) y una octava por debajo, suave: el suelo que tiembla
    for (const [mult, tipo, peso] of [[1, 'sawtooth', 1], [1.003, 'sawtooth', 1], [0.5, 'sine', 0.35]] as const) {
      const osc = ctx.createOscillator(), go = ctx.createGain();
      osc.type = tipo; osc.frequency.value = f * mult; go.gain.value = peso;
      osc.connect(go).connect(fl); fuentes.push(osc);
    }
    for (const o of fuentes) { o.start(t); o.stop(fin + 1.05); }
  }

  /** Un roce metálico que sube despacio: algo que se arrastra en otra sala. */
  private roce(out: AudioNode, f: number, t: number, dur: number, vol: number) {
    const ctx = this.ctx;
    const src = ctx.createBufferSource(), bp = ctx.createBiquadFilter(), g = ctx.createGain();
    src.buffer = ruidoBlanco(ctx); src.loop = true;
    bp.type = 'bandpass'; bp.Q.value = 28;
    bp.frequency.setValueAtTime(f, t); bp.frequency.exponentialRampToValueAtTime(f * 1.45, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    // un filtro tan estrecho deja pasar muy poca energía del ruido: hay que subirlo mucho
    g.gain.exponentialRampToValueAtTime(vol * 40, t + dur * 0.7);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(bp).connect(g).connect(out);
    src.start(t); src.stop(t + dur + 0.05);
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
    const t = this.ctx.currentTime, dur = rapido ? 0.08 : (this.p.salida ?? FUNDIDO);
    this.bus.gain.cancelScheduledValues(t);
    this.bus.gain.setValueAtTime(Math.max(0.0001, this.bus.gain.value), t);
    this.bus.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    const m = this.murmullo, finales = this.nodosFinales, cola = (this.p.sala ? this.p.cola ?? 2.2 : 0);
    window.setTimeout(() => {
      try { m?.stop(); } catch { /* ya parado */ }
      for (const n of finales) n.disconnect();
    }, (dur + 0.6 + cola) * 1000 + ANTICIPO * 1000);
  }
}

const cacheRuido = new WeakMap<Ctx, AudioBuffer>();
/** Dos segundos de ruido blanco compartidos por todos los golpes (no se crea un búfer por nota). */
function ruidoBlanco(ctx: Ctx): AudioBuffer {
  let b = cacheRuido.get(ctx);
  if (!b) {
    b = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate);
    const d = b.getChannelData(0);
    for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
    cacheRuido.set(ctx, b);
  }
  return b;
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

  /** La que debería sonar, aunque el audio aún no se haya desbloqueado (para las pruebas). */
  get pedida() { return this.deseada; }
}

/**
 * Renderiza `segundos` de una pista sin conexión, en estéreo (para medirla: sonoridad, picos, espectro).
 * `Offline` permite pasar otra implementación de OfflineAudioContext (en Node, la de node-web-audio-api).
 */
export function renderizarPista(id: string, segundos: number, sampleRate = 44100,
  Offline: new (canales: number, largo: number, sr: number) => OfflineAudioContext = OfflineAudioContext): Promise<AudioBuffer> {
  const p = PISTAS[id];
  if (!p) throw new Error(`no existe la pista ${id}`);
  const ctx = new Offline(2, Math.ceil(segundos * sampleRate), sampleRate);
  const r = new Reproduccion(ctx, ctx.destination, id, p, true);
  r.programar(segundos);
  return ctx.startRendering();
}
