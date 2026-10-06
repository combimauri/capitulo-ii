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
    else if (paso.type === 'accion') { if (paso.line) lineas.push(paso.line); }
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
      for (const h of [...loc.hotspots, ...loc.npcs.map((n) => n.hotspot)]) {
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
      for (const h of [...loc.hotspots.filter((x) => !x.auto), ...loc.npcs.map((n) => n.hotspot)]) {
        if (h.mirar || h.usar || h.hablar) expect(dentro(h.aprox), `${h.name} aprox`).toBe(false);
      }
      for (const s of loc.spawns) expect(dentro(s), `spawn ${s.name}`).toBe(false);
    });
  }
});

/** Recorre simulando los minijuegos: `resultados` decide qué variables escribe cada acción. */
function recorrerConMinijuegos(b: NarrativeBridge, resultados: (accion: string) => Record<string, unknown>) {
  const textos: string[] = [];
  for (let i = 0; i < 200; i++) {
    const paso = b.next();
    if (paso.type === 'accion') {
      for (const a of paso.acciones) for (const [k, v] of Object.entries(resultados(a.key === 'minijuego' ? a.value.split(',')[0] : a.key))) b.set(k, v);
      if (paso.line) textos.push(paso.line.text);
    } else if (paso.type === 'line') textos.push(paso.line.text);
    else if (paso.type === 'choices') b.choose(0);
    else break;
  }
  return textos.join(' ');
}

describe('los resultados de los minijuegos cambian la historia', () => {
  it('fallar la gimnasia provoca la reprimenda y sube la Sospecha', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.goTo('piso.entrar');
    const t = recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j1_gimnasia: 'fallo' } : {}));
    expect(t).toContain('Más energía');
    expect(b.get('sospecha')).toBe(3);
  });

  it('hacerla bien provoca el elogio', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.goTo('piso.entrar');
    expect(recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j1_gimnasia: 'perfecto' } : {}))).toContain('Mirad todos');
  });

  it('fallar el júbilo del noticiero sube la Sospecha', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.goTo('piso_noche.entrar');
    recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j1_noticia: 'fallo' } : {}));
    expect(b.get('sospecha')).toBe(3);
  });

  it('cada palabra tibia del parte sube la Sospecha', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.goTo('depto.mesa');
    recorrerConMinijuegos(b, (a) => (a === 'parte' ? { parte_j1_tibias: 2, parte_j1_verbo: 'resistido' } : {}));
    expect(b.get('sospecha')).toBe(4);
    expect(b.get('parte_j1_enviado')).toBe(true);
  });
});

describe('estado', () => {
  it('desayunar desbloquea la puerta y el estado se guarda y restaura', () => {
    const b = new NarrativeBridge(resultado.json!);
    const escenas: string[] = [];
    recorrer(b);
    b.goTo('piso.puerta_usar');
    expect(recorrer(b).map((l) => l.text).join(' ')).toMatch(/desayuno/i);
    b.goTo('piso.hornillo_usar');
    recorrer(b);
    const guardado = b.saveState();
    const c = new NarrativeBridge(resultado.json!);
    c.on('command', (t: { key: string; value: string }) => { if (t.key === 'escena') escenas.push(t.value); });
    c.loadState(guardado);
    expect(c.get('desayunado')).toBe(true);
    c.goTo('piso.puerta_usar');
    recorrer(c);
    expect(escenas).toEqual(['escalera']);
  });

  it('cada escena pedida desde ink existe como mapa', () => {
    const ids = new Set(localizaciones.map((l) => l.id));
    const texto = inkFiles(path.join(RAIZ, 'content/ink')).map((f) => fs.readFileSync(f, 'utf8')).join('\n');
    for (const m of texto.matchAll(/#\s*escena:([\w]+)/g)) expect(ids.has(m[1]), m[1]).toBe(true);
  });

  it('cada # escena:x # pos:y apunta a un punto de aparición que existe en ese mapa', () => {
    const porId = new Map(localizaciones.map((l) => [l.id, l]));
    const texto = inkFiles(path.join(RAIZ, 'content/ink')).map((f) => fs.readFileSync(f, 'utf8')).join('\n');
    for (const m of texto.matchAll(/#\s*escena:(\w+)\s*#\s*pos:(\w+)/g)) {
      expect(porId.get(m[1])?.spawns.some((s) => s.name === m[2]), `${m[1]} → ${m[2]}`).toBe(true);
    }
  });

  it('el parte de la jornada 1 llega al noticiero de la noche', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('parte_j1_verbo', 'aplastado al enemigo');
    b.set('parte_j1_km', '30');
    b.goTo('piso_noche.entrar');
    const textos = recorrer(b).map((l) => l.text).join(' ');
    expect(textos).toContain('aplastado al enemigo');
    expect(textos).toContain('ganando 30 kilómetros');
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
