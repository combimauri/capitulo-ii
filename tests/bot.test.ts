/**
 * Bot de recorrido (diseño técnico §11.2): partidas enteras con elecciones y minijuegos al azar.
 *   npx vitest run tests/bot.test.ts                      comprobaciones (unas 200 partidas)
 *   BOT_PARTIDAS=500 npx vitest run tests/bot.test.ts     además, informe de equilibrio con 500 partidas por perfil
 *   (BOT_INFORME=/tmp/informe.md lo guarda también en Markdown)
 */
import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { compileInk } from '../tools/vite-plugin-ink';
import { NarrativeBridge } from '../src/core/NarrativeBridge';
import { parseTiled } from '../src/core/Location';
import { azar, jugarPartida, PERFILES, type Partida } from '../tools/bot';

const RAIZ = path.resolve(__dirname, '..');
const json = compileInk(path.join(RAIZ, 'content/ink/main.ink')).json!;
const DIR = path.join(RAIZ, 'content/locations');
const locs = Object.fromEntries(fs.readdirSync(DIR).filter((f) => f.endsWith('.tmj')).map((f) => {
  const id = f.replace('.tmj', '');
  return [id, parseTiled(id, fs.readFileSync(path.join(DIR, f), 'utf8'))];
}));

const N = Number(process.env.BOT_PARTIDAS) || 0;
/** Partidas por perfil: pocas por defecto (el superviviente, más, para llegar a los finales D y E). */
const POR_PERFIL: Record<string, number> = N
  ? Object.fromEntries(Object.keys(PERFILES).map((p) => [p, N]))
  : { azar: 25, fiel: 25, curioso: 25, torpe: 25, temerario: 15, superviviente: 40 };

const FINALES = ['A', 'B', 'C', 'C0', 'D', 'E'];

const atasco = (p: Partida) => (p.atasco ? `${p.atasco.escena} J${p.atasco.jornada}: ${p.atasco.motivo} (${p.atasco.knot})` : '');
/** Todo lo que ha ido mal en una partida (errores de ink, del motor, atascos, partidas que no terminan). */
const problemas = (p: Partida) => [
  ...p.errores, ...p.avisos,
  ...(p.atasco ? [atasco(p)] : []), ...(['limite', 'error'].includes(p.resultado) ? [`${p.resultado} en ${p.ultimaEscena}`] : []),
];

function jugar(porPerfil: Record<string, number>, semilla = 1) {
  const b = new NarrativeBridge(json);
  const partidas: Partida[] = [];
  for (const [nombre, n] of Object.entries(porPerfil)) {
    for (let i = 0; i < n; i++) partidas.push(jugarPartida(b, locs, azar(semilla + i * 7919), PERFILES[nombre]));
  }
  return partidas;
}

const partidas = jugar(POR_PERFIL);

describe('bot de recorrido', () => {
  it('no hay errores de ink en tiempo de ejecución', () => {
    expect([...new Set(partidas.flatMap((p) => p.errores))]).toEqual([]);
  });

  it('la Duda y la Sospecha nunca salen de 0..100', () => {
    expect(partidas.flatMap((p) => p.fueraDeRango)).toEqual([]);
  });

  it('ninguna partida se atasca: todas llegan a un final', () => {
    expect([...new Set(partidas.flatMap(problemas))]).toEqual([]);
  });

  it('se alcanzan todos los finales, también C0 y el arrepentimiento de la J13', () => {
    const vistos = new Set(partidas.map((p) => p.resultado));
    for (const f of FINALES) expect(vistos.has(f), `nadie llega al final ${f}`).toBe(true);
    expect(partidas.some((p) => p.lineas.has('j13_00a_pens_01')), 'nadie se arrepiente en la J13').toBe(true);
  });

  it('siempre suena música al explorar: ningún sitio, en ninguna jornada, se queda en silencio', () => {
    const mudos = new Set<string>();
    for (const p of partidas) for (const [donde, pistas] of p.musica) if (pistas.has(null)) mudos.add(donde);
    expect([...mudos].sort()).toEqual([]);
  });

  it('cada sitio de cada jornada tiene la música de su momento', () => {
    const oidas = new Map<string, Set<string | null>>();
    for (const p of partidas) for (const [donde, pistas] of p.musica) for (const x of pistas) {
      if (!oidas.has(donde)) oidas.set(donde, new Set());
      oidas.get(donde)!.add(x);
    }
    const oye = (donde: string, pista: string) => oidas.get(donde)?.has(pista);
    // la rutina del creyente, la grieta desde que Amory no está, el miedo al final
    expect(oye('departamento@J1', 'rutina')).toBe(true);
    expect(oye('departamento@J3', 'grieta')).toBe(true);
    expect(oye('avenida@J11', 'minimor')).toBe(true);
    expect(oye('escalera@J1', 'himno_pared')).toBe(true);
    expect(oye('piso@J4', 'soledad')).toBe(true);
    // el mercado antes del cohete, la huida, el refugio, la cripta
    expect(oye('mercado@J5', 'prole')).toBe(true);
    expect(oye('mercado_ruinas@J5', 'ruinas')).toBe(true);
    expect(oye('estudio@J5', 'crane')).toBe(true);
    expect(oye('estudio@J12', 'crane_oscuro')).toBe(true);
    expect(oye('tunel1@J13', 'tuneles')).toBe(true);
    expect(oye('celda@J13', 'celda') || [...oidas.keys()].some((k) => k.startsWith('celda@') && oidas.get(k)!.has('celda'))).toBe(true);
  });

  it('los momentos clave cambian la música: el prólogo, Sammy, la firma de Voss, Goldstein', () => {
    const pedidas = new Set(partidas.flatMap((p) => p.cues.map((c) => `${c.escena}:${c.pista}`)));
    for (const x of ['stepney:terror', 'stepney_ivy:ruinas', 'stepney_ivy:odio', 'stepney_ivy:himno', 'mercado:silencio',
      'minimor_archivo:rabia', 'cripta:cripta', 'casa_dot:refugio']) expect(pedidas.has(x), x).toBe(true);
  });

  it.runIf(N > 0)('informe de equilibrio', () => informe(partidas), 3_600_000);
});

// ------------------------------------------------------------------ informe

/** Umbrales de Duda y Sospecha en ink: qué línea sale en cada rama (para saber cuál se tomó). */
const UMBRALES: { que: string; si: string; no: string }[] = [
  { que: 'J4 piso: duda < 20', si: 'j4_01_pens_d0', no: 'j4_01_pens_d1' },
  { que: 'J4 registro: duda < 20', si: 'j4_03_seis_d0', no: 'j4_03_seis_d1' },
  { que: 'J4 Limehouse: duda < 20', si: 'j4_06_pens_d0', no: 'j4_06_pens_d1' },
  { que: 'J4 Crane: duda < 20', si: 'j4_07b_pens_d0', no: 'j4_07b_pens_d1' },
  { que: 'J6 piso: duda >= 20', si: 'j6_01_pens_d1', no: 'j6_01_pens_d0' },
  { que: 'J7 piso: duda >= 50', si: 'j7_01_pens_d2', no: 'j7_01_pens_d0|j7_01_pens_d1' },
  { que: 'J7 negarse a Nell: duda >= 30 (insiste)', si: 'j7_04d_pens_00', no: 'j7_04n_pens_00' },
  { que: 'J7 aceptar a Nell: sospecha >= 50', si: 'j7_04a_pens_02', no: 'j7_04a_pens_03' },
  { que: 'J8 piso: duda >= 50', si: 'j8_01_pens_d2', no: 'j8_01_pens_d1' },
  { que: 'J9 gimnasia: duda >= 60 (difícil)', si: 'j9_01_tp_02', no: 'j9_01_tp_02b' },
  { que: 'J10 rectificación: duda >= 60', si: 'j10_04_voss_03', no: 'j10_04_voss_03b' },
  { que: 'J13 entrada: duda < 92 (arrepentimiento)', si: 'j13_00a_pens_01', no: 'j13_00_cartel' },
  { que: 'J13 tablones: duda >= 50', si: 'j13_02_mapa_d2', no: 'j13_02_mapa_03' },
];

const pct = (a: number, b: number) => (b ? `${Math.round((100 * a) / b)}%` : '—');
function percentil(xs: number[], q: number) {
  if (!xs.length) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  return s[Math.min(s.length - 1, Math.floor(q * s.length))];
}

function informe(ps: Partida[]) {
  const perfiles = Object.keys(PERFILES);
  const de = (perfil: string) => ps.filter((p) => p.perfil === perfil);
  const salida: string[] = [];
  const tabla = (titulo: string, filas: Record<string, unknown>[]) => {
    salida.push(`\n## ${titulo}`);
    console.log(`\n## ${titulo}`);
    console.table(filas);
    const cols = Object.keys(filas[0] ?? {});
    salida.push(`| ${cols.join(' | ')} |`, `|${cols.map(() => '---').join('|')}|`, ...filas.map((f) => `| ${cols.map((c) => f[c]).join(' | ')} |`));
  };

  // finales
  tabla('Finales por perfil', perfiles.map((perfil) => {
    const xs = de(perfil);
    const fila: Record<string, unknown> = { perfil, partidas: xs.length };
    for (const r of [...FINALES, 'atascado', 'limite', 'error']) fila[r] = pct(xs.filter((p) => p.resultado === r).length, xs.length);
    return fila;
  }));

  // Duda y Sospecha al empezar cada jornada, y arrestos
  for (const perfil of perfiles) {
    const xs = de(perfil);
    const filas = [];
    for (let j = 1; j <= 13; j++) {
      const en = xs.filter((p) => p.jornadas[j]);
      if (!en.length) continue;
      const d = en.map((p) => p.jornadas[j].duda), s = en.map((p) => p.jornadas[j].sospecha);
      filas.push({
        jornada: j, partidas: en.length,
        'duda p10/p50/p90': `${percentil(d, 0.1)} / ${percentil(d, 0.5)} / ${percentil(d, 0.9)}`,
        'sospecha p10/p50/p90': `${percentil(s, 0.1)} / ${percentil(s, 0.5)} / ${percentil(s, 0.9)}`,
        'arresto en la jornada': pct(en.filter((p) => p.arresto === j).length, en.length),
      });
    }
    tabla(`Al empezar cada jornada · ${perfil}`, filas);
  }

  // umbrales: de las partidas que pasan por ese punto, cuántas toman la rama «sí»
  tabla('Umbrales de ink: % que toma la rama «sí» (partidas que pasan por ahí)', UMBRALES.map((u) => {
    const si = new RegExp(`^(${u.si})$`), no = new RegExp(`^(${u.no})$`);
    const fila: Record<string, unknown> = { umbral: u.que };
    for (const perfil of perfiles) {
      const xs = de(perfil);
      const s = xs.filter((p) => [...p.lineas].some((l) => si.test(l))).length;
      const n = xs.filter((p) => [...p.lineas].some((l) => no.test(l))).length;
      fila[perfil] = s + n ? `${pct(s, s + n)} (${s + n})` : '—';
    }
    return fila;
  }));

  // de dónde viene la Sospecha
  const origen = new Map<string, { s: number; d: number; n: number }>();
  for (const p of ps) for (const [k, v] of Object.entries(p.origen)) {
    const o = origen.get(k) ?? { s: 0, d: 0, n: 0 };
    o.s += v.sospecha; o.d += v.duda; o.n++;
    origen.set(k, o);
  }
  tabla('De dónde viene la Sospecha (media por partida, todos los perfiles)', [...origen.entries()]
    .sort((a, b) => b[1].s - a[1].s).slice(0, 20)
    .map(([k, o]) => ({ knot: k, 'sospecha/partida': (o.s / ps.length).toFixed(1), 'partidas con cambios': pct(o.n, ps.length), 'duda/partida': (o.d / ps.length).toFixed(1) })));

  tabla('De dónde viene la Duda (media por partida, todos los perfiles)', [...origen.entries()]
    .sort((a, b) => b[1].d - a[1].d).slice(0, 25)
    .map(([k, o]) => ({ knot: k, 'duda/partida': (o.d / ps.length).toFixed(1), 'partidas con cambios': pct(o.n, ps.length), 'duda/partida con cambios': (o.d / o.n).toFixed(1) })));

  // BOT_INFORME=ruta.md: el mismo informe en Markdown
  if (process.env.BOT_INFORME) fs.writeFileSync(process.env.BOT_INFORME, `# Informe del bot de recorrido (${N} partidas por perfil)\n${salida.join('\n')}\n`);
}
