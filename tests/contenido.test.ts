/** Linter de contenido + humo narrativo (diseño técnico §11.2). */
import fs from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { compileInk } from '../tools/vite-plugin-ink';
import { NarrativeBridge } from '../src/core/NarrativeBridge';
import { parseTiled } from '../src/core/Location';

const RAIZ = path.resolve(__dirname, '..');
const MAIN = path.join(RAIZ, 'content/ink/main.ink');
const resultado = compileInk(MAIN);

function inkFiles(dir: string): string[] {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? inkFiles(path.join(dir, e.name)) : e.name.endsWith('.ink') ? [path.join(dir, e.name)] : []);
}

const localizaciones = fs.readdirSync(path.join(RAIZ, 'content/locations'))
  .filter((f) => f.endsWith('.tmj'))
  .map((f) => parseTiled(f.replace('.tmj', ''), fs.readFileSync(path.join(RAIZ, 'content/locations', f), 'utf8')));

/** Recorre un fragmento eligiendo siempre la opción `eleccion` y devuelve las líneas. */
function recorrer(b: NarrativeBridge, eleccion = 0) {
  const lineas = [];
  for (let i = 0; i < 200; i++) {
    const paso = b.next();
    if (paso.type === 'line') lineas.push(paso.line);
    else if (paso.type === 'choices') b.choose(paso.choices[Math.min(eleccion, paso.choices.length - 1)].index);
    else break;
  }
  return lineas;
}

describe('ink', () => {
  it('compila sin errores', () => {
    expect(resultado.errors).toEqual([]);
    expect(resultado.json).toBeTruthy();
  });

  it('no usa la notación {x|y} del guion (choca con las secuencias de ink)', () => {
    for (const f of inkFiles(path.join(RAIZ, 'content/ink'))) {
      const texto = fs.readFileSync(f, 'utf8').split('\n').filter((l) => !l.trim().startsWith('//')).join('\n');
      expect(texto, path.relative(RAIZ, f)).not.toMatch(/\{[^{}:|]+\|[^{}]+\}/);
    }
  });

  it('el flujo principal arranca y todas sus líneas tienen id', () => {
    const b = new NarrativeBridge(resultado.json!);
    const lineas = recorrer(b);
    expect(lineas.length).toBeGreaterThan(0);
    for (const l of lineas) expect(l.id, l.text).toBeTruthy();
  });
});

describe('localizaciones', () => {
  for (const loc of localizaciones) {
    it(`${loc.id}: cada acción de cada hotspot existe en ink y sus líneas tienen id único`, () => {
      const vistos = new Map<string, string>();
      for (const h of loc.hotspots) {
        for (const ruta of [h.mirar, h.usar, h.hablar].filter(Boolean) as string[]) {
          for (const eleccion of [0, 1, 2]) {
            const b = new NarrativeBridge(resultado.json!);
            expect(b.hasPath(ruta), `${h.name} → ${ruta}`).toBe(true);
            b.goTo(ruta);
            for (const l of recorrer(b, eleccion)) {
              expect(l.id, `${ruta}: "${l.text}"`).toBeTruthy();
              const previo = vistos.get(l.id!);
              expect(previo === undefined || previo === l.text, `id repetido ${l.id}`).toBe(true);
              vistos.set(l.id!, l.text);
            }
          }
        }
      }
    });

    it(`${loc.id}: los puntos de aproximación y spawns no caen dentro de colisiones`, () => {
      const dentro = (p: { x: number; y: number }) =>
        loc.colisiones.some((c) => p.x - 5 < c.x + c.w && p.x + 5 > c.x && p.y - 5 < c.y + c.h && p.y > c.y);
      for (const h of loc.hotspots) expect(dentro(h.aprox), `${h.name} aprox`).toBe(false);
      for (const s of loc.spawns) expect(dentro(s), `spawn ${s.name}`).toBe(false);
    });
  }
});

describe('estado', () => {
  it('desayunar desbloquea la puerta y el estado se guarda y restaura', () => {
    const b = new NarrativeBridge(resultado.json!);
    recorrer(b);
    b.goTo('piso.puerta_usar');
    expect(recorrer(b).map((l) => l.text).join(' ')).toMatch(/desayuno/i);
    b.goTo('piso.hornillo_usar');
    recorrer(b);
    const guardado = b.saveState();
    const c = new NarrativeBridge(resultado.json!);
    c.loadState(guardado);
    expect(c.get('desayunado')).toBe(true);
    c.goTo('piso.puerta_usar');
    expect(recorrer(c).some((l) => l.kind === 'cartel')).toBe(true);
  });

  it('la Sospecha no pasa de 0 a 100', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.call('sube_sospecha', 250);
    expect(b.get('sospecha')).toBe(100);
    b.call('baja_sospecha', 999);
    expect(b.get('sospecha')).toBe(0);
  });

  it('fijar_genero cambia la concordancia', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.call('fijar_genero', 'f');
    expect([b.get('o'), b.get('el'), b.get('un')]).toEqual(['a', 'la', 'una']);
  });
});
