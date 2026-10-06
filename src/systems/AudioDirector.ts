/**
 * Efectos de sonido sintetizados en tiempo real con Web Audio (diseño técnico §12).
 * No necesitan archivos: el silbido del cohete, por ejemplo, se adapta a cualquier duración.
 */

type Sfx = 'silbido' | 'impacto' | 'pitido' | 'silbato' | 'sello' | 'tubo' | 'tecla' | 'plumilla'
  | 'acierto' | 'fallo' | 'grieta' | 'fanfarria' | 'tos';

class Audio {
  private ctx: AudioContext | null = null;
  private master: GainNode | null = null;
  volumen = 0.6;

  /** Debe llamarse dentro de un gesto del usuario (toque o tecla) para desbloquear el audio en móvil. */
  desbloquear() {
    if (!this.ctx) {
      try {
        this.ctx = new AudioContext();
        this.master = this.ctx.createGain();
        this.master.gain.value = this.volumen;
        this.master.connect(this.ctx.destination);
      } catch {
        return;
      }
    }
    if (this.ctx.state === 'suspended') void this.ctx.resume();
  }

  play(id: string, dur?: number) {
    const ctx = this.ctx, out = this.master;
    if (!ctx || !out) return;
    const t = ctx.currentTime;
    switch (id as Sfx) {
      case 'silbido': return this.silbido(ctx, out, t, dur ?? 2.6);
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
      case 'fanfarria':
        [523, 659, 784, 1046].forEach((f, i) => this.tono(ctx, out, t + i * 0.16, f, 0.22, 0.1, 'square'));
        return;
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
