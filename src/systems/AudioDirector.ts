/**
 * Efectos de sonido sintetizados en tiempo real con Web Audio (diseño técnico §12).
 * No necesitan archivos: el silbido del cohete, por ejemplo, se adapta a cualquier duración.
 */

import { Musica } from './Musica';
import { Ambiente } from './Ambiente';

type Sfx = 'silbido' | 'impacto' | 'pitido' | 'silbato' | 'sello' | 'tubo' | 'tecla' | 'plumilla'
  | 'acierto' | 'fallo' | 'grieta' | 'fanfarria' | 'tos' | 'naranjas' | 'chirrido'
  | 'chapoteo' | 'zumbido' | 'tic' | 'papel' | 'alto' | 'golpes' | 'trampilla' | 'dinamo' | 'goteo' | 'descarga' | 'choque' | 'eco_odio'
  | 'puerta' | 'portazo' | 'furgoneta' | 'botas' | 'campanilla' | 'estatica' | 'sirena' | 'multitud' | 'clac' | 'silbido_lejos'
  | 'cerrojo' | 'aplauso' | 'obturador';

/** Los cuatro volúmenes de las opciones (diseño técnico §9). Se guardan aparte de la partida. */
export type Canal = 'general' | 'musica' | 'efectos' | 'ambiente';
const CLAVE_VOLUMEN = 'capitulo2.opciones.volumen';
// general 0.8 deja los efectos como estaban antes de separar canales (0.8² × 0.95 ≈ 0.6)
const VOLUMEN_INICIAL: Record<Canal, number> = { general: 0.8, musica: 1, efectos: 1, ambiente: 0.85 };

function leerVolumenes(): Record<Canal, number> {
  try {
    const g = JSON.parse(window.localStorage.getItem(CLAVE_VOLUMEN) ?? '{}') as Partial<Record<Canal, number>>;
    return { ...VOLUMEN_INICIAL, ...Object.fromEntries(Object.entries(g).filter(([, v]) => typeof v === 'number')) };
  } catch {
    return { ...VOLUMEN_INICIAL };
  }
}

class Audio {
  private ctx: AudioContext | null = null;
  private master: GainNode | null = null;
  private canales: Partial<Record<Exclude<Canal, 'general'>, GainNode>> = {};
  /** La música (pistas sintetizadas en bucle): la pone cada mapa con su propiedad «musica». */
  readonly musica = new Musica(() => (this.ctx && this.canales.musica ? { ctx: this.ctx, out: this.canales.musica } : null));
  /** Los ambientes en capas (telepantalla, oficina, túnel…): los pone cada mapa con su propiedad «ambiente». */
  readonly ambiente = new Ambiente(() => (this.ctx && this.canales.ambiente ? { ctx: this.ctx, out: this.canales.ambiente } : null));
  readonly volumenes: Record<Canal, number> = leerVolumenes();
  /** Silbidos largos en curso (la Habitación 101 los corta de golpe). */
  private largos: OscillatorNode[] = [];

  /** Debe llamarse dentro de un gesto del usuario (toque o tecla) para desbloquear el audio en móvil. */
  desbloquear() {
    if (!this.ctx) {
      try {
        this.ctx = new AudioContext();
        this.master = this.ctx.createGain();
        this.master.connect(this.ctx.destination);
        for (const c of ['musica', 'efectos', 'ambiente'] as const) {
          const g = this.ctx.createGain();
          g.connect(this.master);
          this.canales[c] = g;
        }
        this.aplicarVolumenes();
      } catch {
        return;
      }
    }
    if (this.ctx.state === 'suspended') void this.ctx.resume();
    this.musica.reanudar();
    this.ambiente.reanudar();
  }

  /** Cambia un volumen (0..1) y lo recuerda para la próxima vez. */
  ajustarVolumen(canal: Canal, v: number) {
    this.volumenes[canal] = Math.max(0, Math.min(1, v));
    try { window.localStorage.setItem(CLAVE_VOLUMEN, JSON.stringify(this.volumenes)); } catch { /* sin almacenamiento */ }
    this.aplicarVolumenes();
  }

  private aplicarVolumenes() {
    const ctx = this.ctx;
    if (!ctx || !this.master) return;
    // curva cuadrática: el oído percibe mejor los cambios en la parte baja del deslizador
    const curva = (v: number) => v * v;
    this.master.gain.setTargetAtTime(curva(this.volumenes.general) * 0.95, ctx.currentTime, 0.05);
    for (const c of ['musica', 'efectos', 'ambiente'] as const) this.canales[c]?.gain.setTargetAtTime(curva(this.volumenes[c]), ctx.currentTime, 0.05);
  }

  /** La telepantalla habla: todo lo demás baja un momento (ducking). */
  agachar(dur = 2.5) {
    this.musica.agachar(0.35, dur);
    this.ambiente.agachar(0.5, dur);
  }

  play(id: string, dur?: number) {
    const ctx = this.ctx, out = this.canales.efectos;
    if (!ctx || !out) return;
    const t = ctx.currentTime;
    switch (id as Sfx) {
      case 'silbido':
        this.musica.poner(null, true);       // el silbido corta la música en seco
        return this.silbido(ctx, out, t, dur ?? 2.6);
      case 'impacto': return this.impacto(ctx, out, t);
      case 'pitido': return this.tono(ctx, out, t, 5800, dur ?? 3.5, 0.05, 'sine', true);
      case 'silbato':
        this.tono(ctx, out, t, 2600, 0.35, 0.12, 'square');
        return this.tono(ctx, out, t + 0.45, 2600, 0.9, 0.12, 'square');
      case 'sello': return this.golpe(ctx, out, t, 90, 0.18, 0.6);
      case 'tubo': return this.ruido(ctx, out, t, 0.7, 1800, 0.25, true);
      case 'tecla': return this.golpe(ctx, out, t, 1400, 0.03, 0.12);
      case 'plumilla': return this.ruido(ctx, out, t, 0.12, 5000, 0.05);
      case 'acierto': return this.tono(ctx, out, t, 880, 0.09, 0.08, 'triangle');
      case 'fallo': return this.tono(ctx, out, t, 140, 0.25, 0.15, 'sawtooth');
      case 'grieta': return this.ruido(ctx, out, t, 0.18, 3000, 0.3);
      case 'tos':
        this.ruido(ctx, out, t, 0.12, 700, 0.2);
        return this.ruido(ctx, out, t + 0.22, 0.1, 600, 0.15);
      case 'naranjas':
        this.musica.agachar(0.15, 7);
        return this.naranjas(ctx, out, t);
      case 'chirrido':
        this.tono(ctx, out, t, 1900, 1.4, 0.08, 'sawtooth');
        return this.tono(ctx, out, t, 2350, 1.4, 0.06, 'square');
      case 'dinamo':
        this.tono(ctx, out, t, 180, 0.18, 0.06, 'sawtooth');
        return this.tono(ctx, out, t + 0.05, 240, 0.15, 0.05, 'sawtooth');
      case 'goteo': return this.golpe(ctx, out, t, 1800, 0.06, 0.08);
      case 'eco_odio':                     // los Dos Minutos de Odio, lejos y deformados, en la cabeza
        [0, 0.38, 0.76, 1.14].forEach((d, i) => {
          const v = 0.09 / (i + 1);
          this.tono(ctx, out, t + d, 1900 - i * 260, 0.5, v, 'sawtooth');
          this.ruido(ctx, out, t + d, 0.45, 1400 - i * 250, v * 2.2);
        });
        return;
      case 'choque':                       // el hombro contra el ladrillo mojado, a oscuras
        this.golpe(ctx, out, t, 85, 0.2, 0.7);
        return this.ruido(ctx, out, t, 0.18, 700, 0.18);
      case 'descarga':
        this.tono(ctx, out, t, 1200, dur ?? 0.8, 0.12, 'square');
        return this.ruido(ctx, out, t, dur ?? 0.8, 6000, 0.2);
      case 'chapoteo': return this.ruido(ctx, out, t, 0.35, 900, 0.35, true);
      case 'zumbido': return this.tono(ctx, out, t, 58, 0.7, 0.18, 'sawtooth', true);
      case 'tic': return this.golpe(ctx, out, t, 2400, 0.02, 0.18);
      case 'papel': return this.ruido(ctx, out, t, 0.25, 6000, 0.12, true);
      case 'alto':
        this.tono(ctx, out, t, 3000, 0.5, 0.14, 'square');
        return this.ruido(ctx, out, t, 0.5, 2500, 0.08);
      case 'golpes':
        [0, 0.32, 0.64].forEach((d) => this.golpe(ctx, out, t + d, 70, 0.25, 0.9));
        return;
      case 'trampilla':
        this.golpe(ctx, out, t, 55, 0.4, 0.8);
        return this.ruido(ctx, out, t, 0.3, 500, 0.3);
      case 'fanfarria':
        [523, 659, 784, 1046].forEach((f, i) => this.tono(ctx, out, t + i * 0.16, f, 0.22, 0.1, 'square'));
        return;
      case 'puerta':                       // puerta metálica: golpe grave, resonancia y el pestillo
        this.golpe(ctx, out, t, 60, 0.6, 0.7);
        this.tono(ctx, out, t, 220, 0.9, 0.04, 'triangle');
        this.tono(ctx, out, t, 331, 0.7, 0.025, 'triangle');
        return this.golpe(ctx, out, t + 0.32, 900, 0.05, 0.25);
      case 'portazo':                      // puerta de madera de un piso, cerrada con rabia
        this.golpe(ctx, out, t, 75, 0.35, 0.95);
        this.ruido(ctx, out, t, 0.25, 1200, 0.45);
        return this.golpe(ctx, out, t + 0.12, 1300, 0.04, 0.15);
      case 'furgoneta':                    // motor al ralentí que llega, se para y se queda vibrando
        this.motor(ctx, out, t, dur ?? 3.2);
        return;
      case 'botas':                        // pasos de botas en la escalera: muchos, al paso
        for (let i = 0; i < 10; i++) {
          const d = i * 0.36 + (i % 2) * 0.03;
          this.golpe(ctx, out, t + d, 95 + (i % 3) * 8, 0.12, 0.35 + i * 0.03);
          this.ruido(ctx, out, t + d, 0.06, 2200, 0.08 + i * 0.006);
        }
        return;
      case 'campanilla':                   // la campanilla de la puerta de una tienda (el estudio de Crane)
        [0, 0.09, 0.2].forEach((d, i) => {
          this.tono(ctx, out, t + d, 2093, 0.8 - i * 0.2, 0.05, 'sine');
          this.tono(ctx, out, t + d, 2794, 0.5 - i * 0.1, 0.025, 'sine');
        });
        return;
      case 'estatica':                     // la telepantalla se rompe en nieve
        this.ruido(ctx, out, t, dur ?? 1.2, 7000, 0.22);
        return this.tono(ctx, out, t, 15600, dur ?? 1.2, 0.01, 'sine');
      case 'sirena':                       // la sirena de la Semana del Odio: sube, se sostiene, baja
        return this.sirena(ctx, out, t, dur ?? 6);
      case 'multitud':                     // la plaza que ruge
        this.ruido(ctx, out, t, dur ?? 3, 900, 0.5, false);
        this.ruido(ctx, out, t + 0.1, (dur ?? 3) * 0.9, 2400, 0.18, false);
        return;
      case 'aplauso':                      // un niño que aplaude, solo
        for (let i = 0; i < 9; i++) this.ruido(ctx, out, t + i * 0.27 + Math.random() * 0.03, 0.05, 4500, 0.22);
        return;
      case 'clac': return this.golpe(ctx, out, t, 1600, 0.04, 0.25);
      case 'obturador':                    // la cámara de Crane: el espejo que sube y la cortinilla
        this.ruido(ctx, out, t, 0.03, 5000, 0.25);
        this.golpe(ctx, out, t + 0.05, 700, 0.05, 0.3);
        return this.ruido(ctx, out, t + 0.09, 0.05, 3000, 0.18);
      case 'cerrojo':
        this.golpe(ctx, out, t, 420, 0.08, 0.4);
        return this.golpe(ctx, out, t + 0.14, 300, 0.12, 0.5);
      case 'silbido_lejos':                // un cohete que no termina de caer (créditos del Final E)
        return this.silbidoLejano(ctx, out, t, dur ?? 30);
    }
  }

  private motor(ctx: AudioContext, out: AudioNode, t: number, dur: number) {
    const osc = ctx.createOscillator();
    const lfo = ctx.createOscillator();
    const lfoG = ctx.createGain();
    const filtro = ctx.createBiquadFilter();
    const g = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(70, t);
    osc.frequency.linearRampToValueAtTime(42, t + dur * 0.6);
    lfo.frequency.value = 11; lfoG.gain.value = 6;
    lfo.connect(lfoG).connect(osc.frequency);
    filtro.type = 'lowpass'; filtro.frequency.value = 380;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.35, t + 0.8);
    g.gain.setValueAtTime(0.35, t + dur * 0.7);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(filtro).connect(g).connect(out);
    for (const o of [osc, lfo]) { o.start(t); o.stop(t + dur + 0.05); }
  }

  private sirena(ctx: AudioContext, out: AudioNode, t: number, dur: number) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(180, t);
    osc.frequency.exponentialRampToValueAtTime(620, t + dur * 0.35);
    osc.frequency.setValueAtTime(620, t + dur * 0.65);
    osc.frequency.exponentialRampToValueAtTime(160, t + dur);
    const filtro = ctx.createBiquadFilter();
    filtro.type = 'lowpass'; filtro.frequency.value = 1600;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.12, t + dur * 0.3);
    g.gain.setValueAtTime(0.12, t + dur * 0.7);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(filtro).connect(g).connect(out);
    osc.start(t); osc.stop(t + dur + 0.05);
  }

  /** Muy lejos, muy agudo, bajando tan despacio que nunca llega. */
  private silbidoLejano(ctx: AudioContext, out: AudioNode, t: number, dur: number) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(2300, t);
    osc.frequency.exponentialRampToValueAtTime(1500, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.03, t + dur * 0.5);
    g.gain.setValueAtTime(0.03, t + dur * 0.9);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(out);
    osc.start(t); osc.stop(t + dur + 0.05);
    this.largos.push(osc);
    osc.onended = () => { this.largos = this.largos.filter((o) => o !== osc); };
  }

  /**
   * "Oranges and Lemons" (tonada tradicional, dominio público), las dos primeras frases en 3/4:
   * «Naranjas y limones, dicen las campanas de San Clemente…». En un piano viejo y desafinado.
   */
  private naranjas(ctx: AudioContext, out: AudioNode, t: number) {
    const beat = 60 / 126;
    const frase = 'G5:0:1 E5:1:1 G5:2:1 E5:3:1 C5:4:1 D5:5:.5 E5:5.5:.5 F5:6:1 D5:7:1 G5:8:1 E5:9:1 C5:10:2';
    // la segunda frase («You owe me five farthings…») arranca con dos corcheas
    const segunda = frase.replace('G5:0:1', 'G5:0:.5 G5:0.5:.5').replace(/:(\d+(?:\.\d+)?):/g, (_, b) => `:${Number(b) + 12}:`);
    const melodia = `${frase} ${segunda}`;
    for (const nota of melodia.split(' ')) {
      const [n, b, d] = nota.split(':');
      this.piano(ctx, out, t + Number(b) * beat, this.frecuencia(n), Number(d) * beat + 0.35, 0.11);
    }
    // mano izquierda: una nota grave en la primera parte de cada compás (do, do, sol, do)
    ['C3', 'C3', 'G2', 'C3', 'C3', 'C3', 'G2', 'C3'].forEach((n, i) =>
      this.piano(ctx, out, t + i * 3 * beat, this.frecuencia(n), 3 * beat, 0.07));
  }

  private frecuencia(nota: string) {
    const semitono = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 }[nota[0] as 'C'];
    const midi = 12 * (Number(nota.slice(-1)) + 1) + semitono + (nota.includes('#') ? 1 : 0);
    return 440 * 2 ** ((midi - 69) / 12);
  }

  /** Nota de piano viejo: dos cuerdas que no coinciden, un armónico y un ataque seco. */
  private piano(ctx: AudioContext, out: AudioNode, t: number, f: number, dur: number, vol: number) {
    const desafino = 1 + (Math.random() - 0.5) * 0.012;
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol, t + 0.006);
    g.gain.exponentialRampToValueAtTime(vol * 0.35, t + 0.25);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    g.connect(out);
    for (const [mult, tipo, peso] of [[1, 'triangle', 1], [1.009, 'triangle', 0.7], [2.004, 'sine', 0.25]] as const) {
      const osc = ctx.createOscillator();
      const go = ctx.createGain();
      osc.type = tipo;
      osc.frequency.value = f * desafino * mult;
      go.gain.value = peso;
      osc.connect(go).connect(g);
      osc.start(t);
      osc.stop(t + dur + 0.05);
    }
  }

  private silbido(ctx: AudioContext, out: AudioNode, t: number, dur: number) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(2200, t);
    osc.frequency.exponentialRampToValueAtTime(520, t + dur);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(0.25, t + dur * 0.8);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(out);
    osc.start(t);
    osc.stop(t + dur + 0.05);
    this.largos.push(osc);
    osc.onended = () => { this.largos = this.largos.filter((o) => o !== osc); };
  }

  /** Silencio absoluto: corta los silbidos que estén sonando. */
  cortar() {
    this.musica.poner(null, true);
    this.pararLargos();
  }

  /** Para los sonidos largos (silbidos) sin tocar la música. */
  pararLargos() {
    for (const o of this.largos) { try { o.stop(); } catch { /* ya parado */ } }
    this.largos = [];
  }

  private impacto(ctx: AudioContext, out: AudioNode, t: number) {
    this.ruido(ctx, out, t, 1.8, 400, 1.0);
    this.golpe(ctx, out, t, 45, 1.2, 1.0);
  }

  private tono(ctx: AudioContext, out: AudioNode, t: number, f: number, dur: number, vol: number,
    type: OscillatorType, lento = false) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = type;
    osc.frequency.value = f;
    g.gain.setValueAtTime(lento ? 0.0001 : vol, t);
    if (lento) g.gain.exponentialRampToValueAtTime(vol, t + 0.2);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(out);
    osc.start(t);
    osc.stop(t + dur + 0.05);
  }

  private golpe(ctx: AudioContext, out: AudioNode, t: number, f: number, dur: number, vol: number) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(f * 2, t);
    osc.frequency.exponentialRampToValueAtTime(f, t + dur * 0.5);
    g.gain.setValueAtTime(vol, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    osc.connect(g).connect(out);
    osc.start(t);
    osc.stop(t + dur + 0.05);
  }

  private ruido(ctx: AudioContext, out: AudioNode, t: number, dur: number, corte: number, vol: number, barrido = false) {
    const buf = ctx.createBuffer(1, Math.ceil(ctx.sampleRate * dur), ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const filtro = ctx.createBiquadFilter();
    filtro.type = 'lowpass';
    filtro.frequency.setValueAtTime(corte, t);
    if (barrido) filtro.frequency.exponentialRampToValueAtTime(corte / 6, t + dur);
    const g = ctx.createGain();
    g.gain.setValueAtTime(vol, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    src.connect(filtro).connect(g).connect(out);
    src.start(t);
  }
}

export const audio = new Audio();
