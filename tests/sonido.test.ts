/**
 * El sonido (diseño técnico §12): cada pista se renderiza sin conexión (node-web-audio-api) y se mide.
 * Comprueba que nada satura, que todas suenan a un volumen parecido según su papel (fondo o momento fuerte),
 * que la mezcla no se carga a un lado, que no hay huecos muertos dentro de un bucle, que cada partitura
 * sostiene la emoción que declara y que el móvil puede tocarla.
 */
import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { PISTAS, type Pista } from '../src/systems/Musica';
import { midi, type Emocion } from '../src/systems/partituras';
import { desequilibrio, lufs, movil, objetivo, pico, rasgos, renderizar, silencio } from '../tools/sonido';
import { parseTiled } from '../src/core/Location';

/** Un bucle entero (y un poco más), sin pasar de 75 s. */
const segundos = (p: Pista) => Math.min(75, (p.pulsos * 60) / p.bpm + 3);
const medidas: Record<string, { lufs: number; pico: number; silencio: number; lados: number; movil: number }> = {};

describe('la música, renderizada', () => {
  it('se renderizan todas las pistas', async () => {
    for (const id of Object.keys(PISTAS)) {
      const c = await renderizar(id, segundos(PISTAS[id]));
      medidas[id] = { lufs: lufs(c, 2), pico: pico(c), silencio: silencio(c, 2), lados: desequilibrio(c), movil: lufs(movil(c), 2) };
    }
  }, 600_000);

  it('nada satura: los picos quedan por debajo de -3 dBFS', () => {
    for (const [id, m] of Object.entries(medidas)) expect(m.pico, id).toBeLessThan(-3);
  });

  it('cada pista suena a su nivel: ±1,5 LU de su objetivo (fondo -32, momento fuerte -29,5)', () => {
    for (const [id, m] of Object.entries(medidas)) {
      const o = objetivo(PISTAS[id]);
      if (o === null) {
        // lo que suena dentro de la escena (un piano al otro lado de la pared, un altavoz) puede ir más bajo
        expect(m.lufs, id).toBeGreaterThan(-40);
        expect(m.lufs, id).toBeLessThan(-27);
      } else {
        expect(Math.abs(m.lufs - o), `${id}: ${m.lufs.toFixed(1)} LUFS (objetivo ${o})`).toBeLessThanOrEqual(1.5);
      }
    }
  });

  it('la mezcla no se carga a un lado (menos de 2,5 dB entre izquierda y derecha)', () => {
    for (const [id, m] of Object.entries(medidas)) expect(m.lados, id).toBeLessThan(2.5);
  });

  it('en el altavoz de un móvil (sin graves) ninguna pista desaparece: pierde menos de 7,5 dB', () => {
    for (const [id, m] of Object.entries(medidas)) {
      if (PISTAS[id].diegetica) continue;
      expect(m.lufs - m.movil, `${id}: ${m.lufs.toFixed(1)} → ${m.movil.toFixed(1)} LUFS en un móvil`).toBeLessThan(7.5);
    }
  });

  it('la banda sonora no tiene huecos muertos dentro del bucle', () => {
    for (const [id, m] of Object.entries(medidas)) {
      if (PISTAS[id].diegetica) continue;
      expect(m.silencio, `${id}: ${(m.silencio * 100).toFixed(0)} % en silencio`).toBeLessThan(0.25);
    }
  });
});

// ------------------------------------------------------------------ la emoción, en la partitura

const voces = (p: Pista) => new Set(p.notas.map((n) => n.voz));
const hay = (p: Pista, ...vs: string[]) => vs.some((v) => voces(p).has(v as never));

/** Lo que la teoría pide a cada emoción (tonalidad, tempo, registro, aspereza, pulso). */
const REGLAS: Record<Emocion, (p: Pista) => string | null> = {
  tristeza: (p) => { const r = rasgos(p); return r.modo === 'menor' && p.bpm <= 72 && r.densidad <= 4 ? null : 'menor, lenta y con pocas notas'; },
  nostalgia: (p) => { const r = rasgos(p); return r.disonancia <= 0.45 && r.densidad <= 4 ? null : 'consonante y despacio'; },
  miedo: (p) => { const r = rasgos(p); return (r.modo === 'menor' || r.claridad < 0.75) && (r.registro <= 58 || r.disonancia >= 0.3) ? null : 'menor, grave o áspera'; },
  terror: (p) => { const r = rasgos(p); return r.disonancia >= 0.6 && r.claridad < 0.6 && r.registro <= 50 ? null : 'sin tonalidad, áspera y grave'; },
  rabia: (p) => { const r = rasgos(p); return r.modo === 'menor' && p.bpm >= 120 && r.densidad >= 8 && hay(p, 'timbal', 'bombo') ? null : 'menor, rápida, densa y con timbales'; },
  tension: (p) => { const r = rasgos(p); return (r.modo === 'menor' || r.claridad < 0.8) && (hay(p, 'latido', 'tictac', 'pulso', 'tecla') || r.ostinato >= 0.4) ? null : 'menor y con un pulso que no para'; },
  duda: (p) => (rasgos(p).claridad < 0.75 ? null : 'tonalidad ambigua'),
  rutina: (p) => { const r = rasgos(p); return r.claridad >= 0.8 && r.disonancia <= 0.25 && p.bpm >= 84 && p.bpm <= 112 ? null : 'clara, sin aspereza y a paso de oficina'; },
  misterio: (p) => (rasgos(p).modo === 'menor' && p.bpm <= 72 && (p.sala ?? 0) >= 0.4 ? null : 'menor, lenta y con mucha sala'),
  esperanza: (p) => { const r = rasgos(p); return r.modo === 'mayor' && p.bpm <= 90 && r.disonancia <= 0.15 ? null : 'mayor, serena y consonante'; },
  calidez: (p) => { const r = rasgos(p); return r.modo === 'mayor' && r.disonancia <= 0.35 ? null : 'mayor y amable'; },
  alegria: (p) => (rasgos(p).modo === 'mayor' && p.bpm >= 90 ? null : 'mayor y con paso vivo'),
  fanatismo: (p) => (p.bpm >= 100 && p.bpm <= 130 && hay(p, 'bombo', 'redoble') ? null : 'marcha con bombo'),
  frustracion: (p) => { const r = rasgos(p); return p.bpm >= 130 && r.densidad >= 10 && r.ostinato >= 0.4 ? null : 'rápida, atestada y que no avanza'; },
  vacio: (p) => (rasgos(p).modo === 'mayor' && p.altavoz ? null : 'una alegría que sale de un altavoz'),
};

describe('la emoción de cada pista', () => {
  for (const [id, p] of Object.entries(PISTAS)) {
    it(`${id} sostiene la ${p.emocion}`, () => {
      expect(REGLAS[p.emocion](p), `${id}: debería ser ${REGLAS[p.emocion](p)} (${JSON.stringify(rasgos(p))})`).toBeNull();
    });
  }

  it('la banda sonora cubre las emociones del juego: tristeza, rabia, alegría, miedo, frustración, duda…', () => {
    const usadas = new Set(Object.values(PISTAS).map((p) => p.emocion));
    for (const e of ['tristeza', 'rabia', 'alegria', 'miedo', 'terror', 'frustracion', 'duda', 'tension', 'esperanza', 'misterio'] as Emocion[]) {
      expect(usadas.has(e), e).toBe(true);
    }
  });

  it('el leitmotiv de Ivy («Naranjas y limones» en menor) vuelve en el menú, el duelo, la Hermandad, los túneles y el piso', () => {
    // mi do mi do la: bajar una tercera mayor, subirla, bajarla y bajar una tercera menor
    const motivo = [-4, 4, -4, -3];
    const tiene = (p: Pista) => {
      const porVoz = new Map<string, number[]>();
      for (const n of [...p.notas].sort((a, b) => a.b - b.b)) {
        if (!porVoz.has(n.voz)) porVoz.set(n.voz, []);
        porVoz.get(n.voz)!.push(midi(n.n));
      }
      return [...porVoz.values()].some((alturas) => alturas.some((_, i) => motivo.every((d, k) => alturas[i + k + 1] - alturas[i + k] === d)));
    };
    for (const id of ['misterio', 'ivy', 'hermandad', 'tuneles', 'soledad']) expect(tiene(PISTAS[id]), id).toBe(true);
  });

  it('el tema de Crane se oscurece: la misma melodía, en menor', () => {
    const melodia = (id: string) => PISTAS[id].notas.filter((n) => n.voz === 'piano').map((n) => midi(n.n));
    const clara = melodia('crane'), oscura = melodia('crane_oscuro');
    expect(oscura.length).toBe(clara.length);
    // el mismo dibujo: cada nota igual o medio tono más baja
    oscura.forEach((n, i) => expect([0, -1]).toContain(n - clara[i]));
    expect(rasgos(PISTAS.crane).modo).toBe('mayor');
    expect(rasgos(PISTAS.crane_oscuro).modo).toBe('menor');
  });
});

// ------------------------------------------------------------------ el móvil

/** Osciladores y fuentes que crea cada nota de cada voz (Musica.ts). */
const COSTE: Record<string, number> = {
  piano: 3, piano_limpio: 3, bajo: 3, acorde: 3, pizzicato: 3, tarareo: 3, trompeta: 2, metal: 2, tuba: 2, redoble: 1, bombo: 1,
  timbal: 3, caja: 3, timbre: 3, cuerdas: 3, tremolo: 4, lamento: 2, coro: 4, organo: 2, campana: 7, tecla: 1, carro: 1,
  latido: 2, pulso: 1, dron: 4, tictac: 1, roce: 1,
};

describe('el móvil', () => {
  it('ninguna pista pide más de 90 fuentes de sonido a la vez', () => {
    for (const [id, p] of Object.entries(PISTAS)) {
      const pulso = 60 / p.bpm;
      // cada nota suena su duración más la caída (medio segundo largo; las campanas y cajas, más)
      const tramos = p.notas.map((n) => {
        const cola = ['campana', 'caja', 'timbal'].includes(n.voz) ? 3 : n.voz === 'dron' ? 1.1 : 0.6;
        return { desde: n.b * pulso, hasta: (n.b + n.d) * pulso + cola, coste: COSTE[n.voz] ?? 3 };
      });
      let maximo = 0;
      for (const t of tramos) {
        const a = tramos.filter((x) => x.desde <= t.desde && t.desde < x.hasta).reduce((s, x) => s + x.coste, 0);
        maximo = Math.max(maximo, a);
      }
      expect(maximo, id).toBeLessThanOrEqual(90);
    }
  });
});

// ------------------------------------------------------------------ los mapas

describe('los mapas', () => {
  const DIR = path.resolve(__dirname, '../content/locations');
  const locs = fs.readdirSync(DIR).filter((f) => f.endsWith('.tmj'))
    .map((f) => parseTiled(f.replace('.tmj', ''), fs.readFileSync(path.join(DIR, f), 'utf8')));

  it('todos los mapas tienen música, y la última de su lista no tiene condición (nunca se quedan sin nada)', () => {
    for (const loc of locs) {
      expect(loc.musica.length, loc.id).toBeGreaterThan(0);
      const ultima = loc.musica[loc.musica.length - 1];
      // el mercado, después del cohete, se queda en silencio a propósito (el pitido en los oídos)
      if (loc.id !== 'mercado') expect(ultima.condicion ?? '', `${loc.id}: ${ultima.id}`).toBe('');
    }
  });
});
