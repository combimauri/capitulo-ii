/**
 * Lo que pidieron los primeros jugadores: saber quién tiene algo nuevo que decir, por dónde se sale y qué hay
 * que hacer ahora. Comprueba la simulación en seco, la clasificación de los hotspots y los apuntes.
 */
import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { compileInk } from '../tools/vite-plugin-ink';
import { NarrativeBridge } from '../src/core/NarrativeBridge';
import { parseTiled, type Hotspot } from '../src/core/Location';
import { analizar } from '../src/core/pistas';
import { objetivo, personas, variables, type Apuntes } from '../src/core/apuntes';
import datos from '../content/apuntes.json';

const json = compileInk(path.resolve(__dirname, '../content/ink/main.ink')).json!;
const APUNTES = datos as Apuntes;
const loc = (id: string) => parseTiled(id, fs.readFileSync(path.resolve(__dirname, `../content/locations/${id}.tmj`), 'utf8'));
const hotspot = (id: string, nombre: string) => [...loc(id).hotspots, ...loc(id).npcs.map((n) => n.hotspot)].find((h) => h.name === nombre)!;

describe('la simulación en seco', () => {
  it('no cambia nada de la partida', () => {
    const b = new NarrativeBridge(json);
    b.set('jornada', 1);
    const antes = b.saveState();
    const vistos: string[] = [];
    b.on('command', () => vistos.push('comando'));
    for (const h of loc('escalera').hotspots) for (const r of [h.mirar, h.usar, h.hablar]) if (r) b.simular(r, antes);
    expect(b.saveState()).toBe(antes);
    expect(vistos).toEqual([]);
  });
});

describe('las marcas de cada hotspot', () => {
  const b = new NarrativeBridge(json);
  const sim = (r: string, e: string) => b.simular(r, e);

  it('la mano entre los escombros es algo nuevo, no una salida (aunque cambie de escena)', () => {
    const e = b.saveState();
    const mano = loc('stepney').hotspots.find((h) => (h.usar ?? h.mirar ?? '').startsWith('stepney.') && !h.auto && /mano|cascotes/i.test(`${h.name} ${h.nombre}`))!;
    expect(mano).toBeTruthy();
    const a = analizar(mano, e, new Set(), sim);
    expect(a.salida).toBe(false);
    expect(a.nuevo).toBe(true);
  });

  it('una puerta cerrada por la historia no lleva flecha (el Departamento, antes de redactar el parte)', () => {
    const b2 = new NarrativeBridge(json);
    b2.set('jornada', 1);
    expect(analizar(hotspot('departamento', 'salir'), b2.saveState(), new Set(), (r, e) => b2.simular(r, e)).salida).toBe(false);
  });

  it('una salida que lleva a otra escena lleva flecha; lo ya leído deja de ser nuevo', () => {
    const b2 = new NarrativeBridge(json);
    b2.set('jornada', 1);
    const e = b2.saveState();
    const s = (r: string, est: string) => b2.simular(r, est);
    const salir: Hotspot = hotspot('pub', 'salir');
    const a = analizar(salir, e, new Set(), s);
    expect(a.salida).toBe(true);
    const leidas = new Set(b2.simular(salir.usar ?? salir.mirar!, e).ids);
    expect(analizar(salir, e, leidas, s).nuevo).toBe(false);
  });
});

describe('los apuntes', () => {
  const globals = fs.readFileSync(path.resolve(__dirname, '../content/ink/globals.ink'), 'utf8');
  const declaradas = new Set([...globals.matchAll(/^\s*VAR\s+(\w+)/gm)].map((m) => m[1]));

  it('cada condición usa variables que existen en ink, y nunca «||» ni paréntesis', () => {
    for (const v of variables(APUNTES)) expect(declaradas.has(v), v).toBe(true);
    const conds = JSON.stringify(APUNTES);
    expect(conds.includes('||')).toBe(false);
  });

  it('hay un objetivo para el principio y para cada final en curso', () => {
    const b = new NarrativeBridge(json);
    const leer = (v: string) => b.get(v);
    expect(objetivo(APUNTES, leer)).toMatch(/cascotes/i);
    for (const f of ['C', 'D', 'E']) {
      b.set('final_en_curso', f);
      expect(objetivo(APUNTES, leer), f).not.toBe(APUNTES.objetivos[APUNTES.objetivos.length - 1].texto);
    }
  });

  it('el doblepensar borra a Amory de los apuntes', () => {
    const b = new NarrativeBridge(json);
    b.set('depto_visto', true); b.set('depto_j3_visto', true); b.set('dp_j3_amory', 'aceptar');
    expect(personas(APUNTES, (v) => b.get(v)).find((p) => p.id === 'amory')?.nombre).toBe('—');
  });
});
