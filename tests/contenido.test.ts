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
        for (const ruta of [h.mirar, h.usar, h.hablar, ...Object.values(h.con ?? {})].filter(Boolean) as string[]) {
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
    b.set('jornada', 1);
    b.goTo('piso.entrar');
    const t = recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j1_gimnasia: 'fallo' } : {}));
    expect(t).toContain('Más energía');
    expect(b.get('sospecha')).toBe(3);
  });

  it('hacerla bien provoca el elogio', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 1);
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

describe('jornada 2', () => {
  it('fallar los Dos Minutos de Odio y además la transición al Gran Hermano suma 10 de Sospecha', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 2);
    b.goTo('odio.sentarse');
    recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j2_odio: 'fallo', cf_j2_odio_transicion: 'fallo' } : {}));
    expect(b.get('sospecha')).toBe(10);
  });

  it('un Odio perfecto hace que O\'Brien te mire', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 2);
    b.goTo('odio.sentarse');
    const t = recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j2_odio: 'perfecto', cf_j2_odio_transicion: 'ok' } : {}));
    expect(t).toContain('me mira de reojo');
    expect(b.get('sospecha')).toBe(0);
  });

  it('solo quien mira a Amory en el clímax le ve limpiarse las gafas', () => {
    for (const amory of ['visto', 'no']) {
      const b = new NarrativeBridge(resultado.json!);
      b.set('jornada', 2);
      b.goTo('odio.sentarse');
      const t = recorrerConMinijuegos(b, (a) => (a === 'cf' ? { cf_j2_odio: 'aceptable', cf_j2_odio_amory: amory } : {}));
      expect(t.includes('limpiándose las gafas')).toBe(amory === 'visto');
    }
  });

  for (const [indice, reaccion, duda, sospecha, escena] of [
    [0, 'risa', 5, 25, null], [1, 'reprimenda', 0, 20, null], [2, 'denuncia', 0, 20, 'despacho_voss'],
  ] as const) {
    it(`la broma de Amory: ${reaccion}`, () => {
      const b = new NarrativeBridge(resultado.json!);
      const escenas: string[] = [];
      b.on('command', (t: { key: string; value: string }) => { if (t.key === 'escena') escenas.push(t.value); });
      b.set('jornada', 2);
      b.set('sospecha', 20);
      b.goTo('depto.mesa');
      for (let i = 0; i < 100; i++) {
        const paso = b.next();
        if (paso.type === 'accion') { if (paso.acciones.some((x) => x.key === 'minijuego')) b.set('frente_j2', 'hecho'); }
        else if (paso.type === 'choices') b.choose(paso.choices[indice].index);
        else if (paso.type === 'end') break;
      }
      expect(b.get('amory_reaccion')).toBe(reaccion);
      expect(b.get('duda')).toBe(duda);
      expect(b.get('sospecha')).toBe(sospecha);
      expect(b.list('inventario')).toContain('lapiz_amory');
      expect(escenas.includes('despacho_voss')).toBe(escena === 'despacho_voss');
      if (reaccion === 'denuncia') {
        b.goTo('voss_despacho.entrar');
        recorrer(b);
        expect(b.get('sospecha')).toBe(10);
      }
    });
  }
});

/** Juega un fragmento: elige `elecciones` en orden (0 si se acaban) y simula los minijuegos. */
function jugar(b: NarrativeBridge, ruta: string, opts: { elecciones?: number[]; minijuegos?: Record<string, unknown> } = {}) {
  const textos: string[] = [];
  const comandos: string[] = [];
  const quitar = b.on('command', (t: { key: string; value: string }) => comandos.push(`${t.key}:${t.value}`));
  const elecciones = [...(opts.elecciones ?? [])];
  b.goTo(ruta);
  for (let i = 0; i < 200; i++) {
    const paso = b.next();
    if (paso.type === 'accion') {
      for (const [k, v] of Object.entries(opts.minijuegos ?? {})) b.set(k, v);
      if (paso.line) textos.push(paso.line.text);
    } else if (paso.type === 'line') textos.push(paso.line.text);
    else if (paso.type === 'choices') b.choose(paso.choices[Math.min(elecciones.shift() ?? 0, paso.choices.length - 1)].index);
    else break;
  }
  quitar();
  return { texto: textos.join(' '), comandos };
}

describe('jornada 3', () => {
  const nueva = (vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 3);
    b.set('amory_borrado', true);
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };

  it('el sueño termina la jornada 2 y despierta en la 3, con Amory ya borrado', () => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 2);
    const { comandos } = jugar(b, 'sueno.final');
    expect(b.get('jornada')).toBe(3);
    expect(b.get('amory_borrado')).toBe(true);
    expect(comandos).toContain('escena:piso');
    expect(comandos.some((c) => c.startsWith('final'))).toBe(false);
  });

  it('al despacho de Voss solo se entra tras hablar con Pell y con Brooke (que sube la Sospecha)', () => {
    const b = nueva();
    expect(jugar(b, 'depto.despacho').comandos).not.toContain('escena:despacho_voss');
    jugar(b, 'j3_pell');
    expect(jugar(b, 'depto.despacho').comandos).not.toContain('escena:despacho_voss');
    jugar(b, 'j3_brooke');
    expect(b.get('sospecha')).toBe(3);
    expect(jugar(b, 'depto.despacho').comandos).toContain('escena:despacho_voss');
  });

  it('con Voss: si le denunciaste, la Duda sube; si insistes, la Sospecha sube 10', () => {
    const b = nueva({ amory_reaccion: 'denuncia' });
    const { texto } = jugar(b, 'voss_despacho.entrar', { elecciones: [1] });
    expect(texto).toContain('exceso de cansancio');
    expect(b.get('duda')).toBe(5);
    expect(b.get('sospecha')).toBe(10);
    const b2 = nueva({ amory_reaccion: 'risa' });
    expect(jugar(b2, 'voss_despacho.entrar', { elecciones: [0] }).texto).toContain('Está pálido');
    expect(b2.get('sospecha')).toBe(0);
  });

  it('al volver del despacho llega el doblepensar; aceptar baja Duda y Sospecha, recordar sube la Duda', () => {
    const a = nueva({ voss_j3_visto: true, duda: 10, sospecha: 10 });
    const ra = jugar(a, 'depto.entrar', { minijuegos: { dp_j3_amory: 'aceptar' } });
    expect(ra.texto).toContain('Siempre ha sido así');
    expect(ra.comandos).toContain('objeto:lapiz_amory');
    expect([a.get('duda'), a.get('sospecha')]).toEqual([5, 5]);
    const r = nueva({ voss_j3_visto: true, duda: 10 });
    expect(jugar(r, 'depto.entrar', { minijuegos: { dp_j3_amory: 'recordar' } }).texto).toContain('Felix Amory existía ayer');
    expect(r.get('duda')).toBe(25);
    expect(r.get('diario_amory')).toBe(true);
  });

  it('tirar el lápiz por el agujero de la memoria lo destruye; guardarlo no', () => {
    const conLapiz = (vars: Record<string, unknown>) => {
      const b = nueva();
      b.set('jornada', 2);
      jugar(b, 'j2_mesa', { elecciones: [1], minijuegos: { frente_j2: 'hecho' } });   // Amory presta el lápiz
      b.set('jornada', 3);
      for (const [k, v] of Object.entries(vars)) b.set(k, v);
      return b;
    };
    const antes = conLapiz({ duda: 12 });
    expect(jugar(antes, 'j3_lapiz_agujero').texto).toContain('Tengo que devolvérselo');
    const tirar = conLapiz({ dp_j3_amory: 'aceptar', duda: 12 });
    jugar(tirar, 'j3_lapiz_agujero', { elecciones: [0] });
    expect(tirar.get('lapiz_destruido')).toBe(true);
    expect(tirar.get('duda')).toBe(2);
    expect(tirar.list('inventario')).not.toContain('lapiz_amory');
    const guardar = conLapiz({ dp_j3_amory: 'recordar' });
    jugar(guardar, 'j3_lapiz_agujero', { elecciones: [1] });
    expect(guardar.list('inventario')).toContain('lapiz_amory');
    expect(jugar(guardar, 'objetos.lapiz_mirar').texto).toContain('Esto existió');
  });

  it('en el pasillo, la limpiadora desaparece cuando el guardia dobla la esquina', () => {
    const b = nueva({ dp_j3_amory: 'recordar' });
    expect(jugar(b, 'pasillo.nell_mirar').texto).toContain('Son los dibujos de Amory');
    expect(jugar(b, 'pasillo.salir').comandos).not.toContain('escena:piso_noche');
    const { comandos } = jugar(b, 'pasillo.encuentro');
    expect(b.get('nell_se_fue')).toBe(true);
    expect(b.get('guardia_pasillo')).toBe(true);
    expect(comandos).toEqual(expect.arrayContaining(['prota:izquierda', 'prota:derecha']));
    expect(jugar(b, 'pasillo.salir').comandos).toContain('escena:piso_noche');
  });

  for (const [dp, duda, reaccion, esperado] of [
    ['aceptar', 0, 'risa', 'Mañana ganaremos más kilómetros'],
    ['aceptar', 15, 'risa', '¿Por qué no recuerdo con quién comía los martes?'],
    ['recordar', 30, 'reprimenda', 'Felix Amory existía. Felix Amory existía.'],
    ['aceptar', 0, 'denuncia', 'Yo dije su nombre'],
  ] as const) {
    it(`cierre del Acto I: ${dp}, duda ${duda}, ${reaccion}`, () => {
      const b = nueva({ dp_j3_amory: dp, duda, amory_reaccion: reaccion });
      expect(jugar(b, 'piso_noche.entrar').texto).toContain(esperado);
    });
  }

  it('dormir cierra el Acto I y despierta en la Jornada 4', () => {
    const b = nueva();
    const { texto, comandos } = jugar(b, 'piso_noche.dormir');
    expect(texto).toContain('FIN DEL ACTO I');
    expect(comandos).toContain('escena:piso');
    expect(b.get('jornada')).toBe(4);
  });
});

describe('jornada 4', () => {
  const nueva = (vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 4);
    b.set('amory_borrado', true);
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };

  it('por la mañana, el cajón de la mesa guarda la foto de Ivy', () => {
    const b = nueva();
    jugar(b, 'piso.entrar');
    const { comandos } = jugar(b, 'piso.cajon_usar');
    expect(b.list('inventario')).toContain('foto_ivy');
    expect(comandos).toContain('objeto:foto_ivy');
  });

  it('Voss asigna el Registro; el cajón da el compás y, bajo el fieltro, la lámina y la nota', () => {
    const b = nueva({ amory_reaccion: 'denuncia' });
    expect(jugar(b, 'depto.entrar').texto).toContain('buen ojo');
    expect(b.get('registro_asignado')).toBe(true);
    jugar(b, 'j4_cajon');
    expect(b.list('inventario')).toContain('compas');
    jugar(b, 'j4_cajon');
    expect(b.list('inventario')).toEqual(expect.arrayContaining(['zonificacion', 'nota_amory']));
    expect(b.get('duda')).toBe(5);
  });

  it('mirar el mapa con la lámina sube la Duda y, con Duda alta, recuerda la nota', () => {
    const b = nueva({ duda: 25, registro_asignado: true });
    jugar(b, 'j4_cajon'); jugar(b, 'j4_cajon');
    const { texto } = jugar(b, 'j4_libro', { minijuegos: { registro_j4_lamina: 'si' } });
    expect(texto).toContain('Todas en zona prole');
    expect(texto).toContain('¿Por qué nunca en el centro?');
    expect(b.get('duda')).toBe(33);
    const sin = nueva({ registro_asignado: true });
    expect(jugar(sin, 'j4_libro', { minijuegos: { registro_j4_lamina: 'no' } }).texto).not.toContain('zona prole');
  });

  it('el día sigue: Registro → cantina → parte ilegible → ir a Limehouse o volver a casa', () => {
    const b = nueva();
    expect(jugar(b, 'depto.salir').comandos).not.toContain('escena:cantina');
    b.set('registro_j4_hecho', true);
    expect(jugar(b, 'depto.salir').comandos).toContain('escena:cantina');
    jugar(b, 'cantina.entrar');
    expect(jugar(b, 'cantina.salir').comandos).toContain('escena:departamento');
    const ir = jugar(b, 'depto.entrar', { elecciones: [0] });
    expect(ir.texto).toContain('ilegible');
    expect(ir.comandos).toContain('escena:limehouse');
    expect(b.get('visita_prole_j4')).toBe(true);
    const b2 = nueva({ registro_j4_hecho: true, cantina_j4_vista: true });
    expect(jugar(b2, 'depto.entrar', { elecciones: [1] }).comandos).toContain('escena:piso_noche');
    expect(b2.get('visita_prole_j4')).toBe(false);
  });

  it('en Limehouse, Dot completa el parte, Sammy ofrece metralla y aparece Crane', () => {
    const b = nueva();
    expect(jugar(b, 'limehouse.volver').comandos).not.toContain('escena:piso_noche');
    jugar(b, 'pub.entrar');
    const { texto } = jugar(b, 'limehouse.sammy', { elecciones: [1, 0] });
    expect(texto).toContain('Los Hennessy');
    expect(b.get('ilegible_completado')).toBe(true);
    expect(b.get('dot_confianza')).toBe(2);
    expect(b.list('inventario')).toContain('metralla_sammy');
    expect(b.get('crane_aparece')).toBe(true);
    jugar(b, 'piso.cajon_usar');   // sin cajon_disponible: la foto no está
    b.set('cajon_disponible', true);
    jugar(b, 'piso.cajon_usar');
    expect(jugar(b, 'limehouse.crane').texto).toContain('Le devolveré la cara de su hermana');
    expect(b.list('inventario')).toContain('tarjeta_crane');
    expect(jugar(b, 'objetos.foto_mirar').texto).toContain('Ya tengo su cara');
    expect(jugar(b, 'limehouse.volver').comandos).toContain('escena:piso_noche');
  });

  it('volver tarde de un barrio prole: Hilda lo apunta (Sospecha +3)', () => {
    const b = nueva({ visita_prole_j4: true, hilda_aprecio: 1 });
    expect(jugar(b, 'piso_noche.entrar').texto).toContain('Qué celo');
    expect(b.get('sospecha')).toBe(3);
    const c = nueva({ visita_prole_j4: true, hilda_aprecio: 2 });
    jugar(c, 'piso_noche.entrar');
    expect(c.get('sospecha')).toBe(0);
    const { comandos } = jugar(c, 'piso_noche.dormir');
    expect(c.get('jornada')).toBe(5);
    expect(comandos).toContain('escena:piso');
  });
});

describe('jornada 5', () => {
  const nueva = (vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 5);
    b.set('amory_borrado', true);
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };
  const conFoto = (vars: Record<string, unknown> = {}) => {
    const b = nueva({ cajon_disponible: true, ...vars });
    jugar(b, 'j4_cajon_piso');
    return b;
  };

  it('por la mañana: sin tarjeta, el anuncio del periódico; con la foto, decidir si llevarla', () => {
    const b = conFoto();
    expect(jugar(b, 'piso.entrar').texto).toContain('ESTUDIO CRANE');
    b.set('desayunado', true);
    expect(jugar(b, 'piso.puerta_usar', { elecciones: [0] }).comandos).toContain('escena:mercado');
    expect(b.get('foto_a_crane')).toBe(true);
    const sin = nueva({ desayunado: true });
    expect(jugar(sin, 'piso.puerta_usar').texto).toContain('CERRADA POR REFORMAS');
  });

  it('en el estudio, hablar de «Naranjas y limones» da información a Crane', () => {
    const b = conFoto({ foto_a_crane: true });
    jugar(b, 'estudio.entrar', { elecciones: [1, 0] });
    expect(b.get('crane_info')).toBe(1);
    expect(b.get('sospecha')).toBe(3);
    expect(b.list('inventario')).not.toContain('foto_ivy');
  });

  for (const [sammy, duda, sospecha, pos] of [['correr', 10, 8, 'calzada'], ['cubierto', 5, 0, 'puesto'], ['paralizado', 5, 0, 'puesto']] as const) {
    it(`el cohete del mercado: ${sammy}`, () => {
      const b = nueva();
      const { comandos } = jugar(b, 'mercado.cohete', { minijuegos: { sammy_j5: sammy } });
      expect([b.get('duda'), b.get('sospecha')]).toEqual([duda, sospecha]);
      expect(comandos).toEqual(expect.arrayContaining(['escena:mercado_ruinas', `pos:${pos}`]));
      expect(b.get('sammy_intento')).toBe(sammy === 'correr');
      const despues = jugar(b, 'ruinas.entrar').texto;
      expect(despues).toContain('Retiren eso');
      expect(b.get('diario_sammy')).toBe(true);
      expect(b.get('dot_confianza')).toBe(sammy === 'correr' ? 2 : 0);
    });
  }

  it('mentir a Voss sobre el retraso, si corriste hacia el impacto, cuesta 10 de Sospecha', () => {
    const b = nueva({ sammy_intento: true });
    expect(jugar(b, 'depto.entrar', { elecciones: [1] }).texto).toContain('Corría hacia el impacto');
    expect(b.get('sospecha')).toBe(10);
    const v = nueva();
    jugar(v, 'depto.entrar', { elecciones: [0, 1] });
    expect(v.get('sospecha')).toBe(3);
  });

  it('el patrón: la conclusión sube la Duda; dejar la lámina puesta cuesta 10 de Sospecha', () => {
    const b = nueva({ ilegible_completado: true });
    const { texto } = jugar(b, 'j4_libro', { elecciones: [0], minijuegos: { registro_j5_lamina_puesta: 'si' } });
    expect(texto).toContain('Once de once');
    expect(texto).toContain('Stepney fue la excepción');
    expect(b.list('inventario')).toEqual(expect.arrayContaining(['zonificacion', 'compas']));
    expect(b.get('patron_conclusion')).toBe('proles');
    expect(b.get('duda')).toBe(10);
    expect(b.get('sospecha')).toBe(10);
    expect(b.get('diario_cohetes')).toBe(true);
    const c = nueva();
    jugar(c, 'j5_libro', { elecciones: [2], minijuegos: { registro_j5_lamina_puesta: 'no' } });
    expect(c.get('diario_cohetes')).toBe(false);
  });

  it('el diario: aparece en el abrigo; abrirlo a la vista cuesta Sospecha; escribir en el hueco sube la Duda', () => {
    const b = nueva({ dp_j3_amory: 'aceptar' });
    expect(jugar(b, 'piso_noche.abrigo').texto).toContain('Se llamaba Felix');
    expect(b.list('inventario')).toContain('diario');
    expect(b.get('duda')).toBe(5);
    jugar(b, 'j5_diario_cono'); jugar(b, 'j5_diario_cono');
    expect(b.get('sospecha')).toBe(5);
    const { texto } = jugar(b, 'j5_hueco', { elecciones: [0], minijuegos: { diario_entradas: 1 } });
    expect(texto).toContain('1984. Creo.');
    expect(b.get('diario_iniciado')).toBe(true);
    expect(b.get('diario_escondite')).toBe('cartel');
    expect(b.get('duda')).toBe(10);
    expect(jugar(b, 'piso_noche.dormir').comandos).toContain('escena:piso');
    expect(b.get('jornada')).toBe(6);
  });

  it('cada entrada del diario está declarada en ink (desbloqueo y «escrita»)', () => {
    const b = new NarrativeBridge(resultado.json!);
    const entradas = JSON.parse(fs.readFileSync(path.join(RAIZ, 'content/diario/entradas.json'), 'utf8')).entradas as { id: string }[];
    for (const e of entradas) {
      expect(b.story.variablesState.GlobalVariableExistsWithName(e.id), e.id).toBe(true);
      expect(b.story.variablesState.GlobalVariableExistsWithName(`${e.id}_escrita`), `${e.id}_escrita`).toBe(true);
    }
  });
});

describe('jornada 6', () => {
  const nueva = (vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 6);
    b.set('amory_borrado', true);
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };
  const con = (b: NarrativeBridge, ...items: string[]) => {
    const inv = b.story.variablesState.$('inventario') as unknown as { AddItem: (i: string) => void };
    for (const i of items) inv.AddItem(i);
    b.story.variablesState.$('inventario', inv as never);
    return b;
  };

  it('Hilda en la escalera: «siete muertos son siete muertos» se apunta', () => {
    const b = nueva({ hilda_aprecio: 1 });
    expect(jugar(b, 'escalera.entrar', { elecciones: [0] }).texto).toContain('Inspección del Comité');
    expect([b.get('sospecha'), b.get('hilda_aprecio')]).toEqual([5, 0]);
  });

  it('el archivo: la caja buena, el parte que no es el mío y el doblepensar sobre lo que oí', () => {
    const b = nueva({ parte_j1_prisioneros: '12.000', parte_j1_km: '30', parte_j1_verbo: 'aplastado al enemigo', duda: 20 });
    const { texto } = jugar(b, 'archivo.estanterias', { elecciones: [0, 2], minijuegos: { dp_j6_parte: 'recordar' } });
    expect(texto).toContain('Esta no es');
    expect(texto).toContain('Escribí «aplastado al enemigo». Escribí 30 kilómetros');
    expect(b.get('prisioneros_j6')).toBe('1.200');
    expect(b.get('duda')).toBe(35);
    expect(b.get('diario_parte')).toBe(true);
    expect(b.get('parte_en_mesa')).toBe(true);
  });

  it('guardarse el parte alterado: si la telepantalla del techo mira, Voss aparece en la puerta', () => {
    const visto = nueva({ archivo_vigilado: true, parte_en_mesa: true });
    expect(jugar(visto, 'archivo.parte_coger').texto).toContain('¿Encuentra lo que busca, camarada?');
    expect(visto.get('sospecha')).toBe(15);
    expect(visto.list('inventario')).not.toContain('parte_alterado');
    const oculto = nueva({ archivo_vigilado: false, parte_en_mesa: true });
    jugar(oculto, 'archivo.parte_coger');
    expect(oculto.list('inventario')).toContain('parte_alterado');
    expect(oculto.get('prueba_parte')).toBe(true);
  });

  it('Crane devuelve la cara de Ivy y prueba hasta dónde se habla en su estudio', () => {
    const b = nueva({ foto_a_crane: true });
    jugar(b, 'estudio.entrar', { elecciones: [1, 1, 1] });
    expect(b.list('inventario')).toContain('foto_ivy_restaurada');
    expect(b.get('crane_info')).toBe(3);
    expect(b.get('sospecha')).toBe(13);
    expect(b.get('crane_trastienda')).toBe(true);
    jugar(b, 'j6_recorte_mirar'); jugar(b, 'j6_recorte_mirar');
    expect(b.get('duda')).toBe(10);
    expect(b.get('diario_chocolate')).toBe(true);
  });

  it('la inspección: el diario mal escondido se lo lleva el Comité y la Sospecha ya no baja de 40', () => {
    const b = con(nueva({ hilda_aprecio: 1, diario_iniciado: true }), 'diario');
    const { texto } = jugar(b, 'piso_noche.entrar', { minijuegos: { escondite_j6_diario: 'colchon' } });
    expect(texto).toContain('Nota el bulto');
    expect(b.get('diario_confiscado')).toBe(true);
    expect(b.get('sospecha')).toBe(25);
    expect(b.get('comite_leyo')).toBe(true);
    b.story.EvaluateFunction('baja_sospecha', [20]);
    expect(b.get('sospecha')).toBe(40);
  });

  it('la inspección: detrás del cartel de Ivy, pedir que no lo toque lo salva', () => {
    const b = con(nueva({ hilda_aprecio: 1, visita_prole_j4: true, foto_a_crane: true }), 'diario', 'parte_alterado');
    jugar(b, 'piso_noche.entrar', { elecciones: [0], minijuegos: { escondite_j6_diario: 'cartel', escondite_j6_parte: 'cajon' } });
    expect(b.get('diario_confiscado')).toBe(false);
    expect(b.get('hilda_aprecio')).toBe(2);
    expect(b.list('inventario')).not.toContain('parte_alterado');
    expect(b.get('sospecha')).toBe(15);   // el papel con sello (+10) y «te vieron en Limehouse» (+5)
    const h = con(nueva(), 'diario');
    jugar(h, 'piso_noche.entrar', { minijuegos: { escondite_j6_diario: 'hornillo' } });
    expect(h.get('diario_hollin')).toBe(true);
    expect(jugar(h, 'piso_noche.dormir').comandos).toContain('escena:piso');
  });

  it('las líneas que reescribe cada doblepensar existen en ink', () => {
    const ids = new Set(inkFiles(path.join(RAIZ, 'content/ink')).flatMap((f) => [...fs.readFileSync(f, 'utf8').matchAll(/# id:(\w+)/g)].map((m) => m[1])));
    for (const f of fs.readdirSync(path.join(RAIZ, 'content/doblepensar'))) {
      const c = JSON.parse(fs.readFileSync(path.join(RAIZ, 'content/doblepensar', f), 'utf8'));
      for (const id of Object.keys(c.reescribir ?? {})) expect(ids.has(id), `${f}: ${id}`).toBe(true);
    }
  });
});

describe('jornada 7 y los finales del Acto II', () => {
  const nueva = (vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', 7);
    b.set('amory_borrado', true);
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };
  /** Todas las líneas de un recorrido tienen id (los finales no cuelgan de ningún hotspot). */
  const conIds = (b: NarrativeBridge, ruta: string, elecciones: number[] = []) => {
    b.goTo(ruta);
    const lineas = [];
    for (let i = 0; i < 300; i++) {
      const paso = b.next();
      if (paso.type === 'line') lineas.push(paso.line);
      else if (paso.type === 'accion') { if (paso.line) lineas.push(paso.line); }
      else if (paso.type === 'choices') b.choose(paso.choices[Math.min(elecciones.shift() ?? 0, paso.choices.length - 1)].index);
      else break;
    }
    for (const l of lineas) expect(l.id, l.text).toBeTruthy();
    return lineas.map((l) => l.text).join(' ');
  };

  it('Nell: la canción, hasta cuatro preguntas (devuelve el diario si lo tenía el Comité) y aceptar', () => {
    const b = nueva({ diario_confiscado: true, comite_leyo: true, patron_conclusion: 'proles', sospecha: 55 });
    const { texto, comandos } = jugar(b, 'suministros.cintas', { elecciones: [1, 2, 2, 0, 0] });
    expect(comandos).toContain('prota:abajo');
    expect(texto).toContain('Los proles también limpian allí');
    expect(texto).toContain('a tres plantas de aquí');
    expect(texto).toContain('Basta de preguntas');
    expect(texto).toContain('Sobre todo con la gente amable');
    expect(b.list('inventario')).toEqual(expect.arrayContaining(['diario', 'llave_calderas']));
    expect(b.get('diario_confiscado')).toBe(false);
    expect(b.get('nell_respuesta')).toBe('aceptar');
    const { comandos: fin, texto: textoFin } = jugar(b, 'piso_noche.dormir');
    expect(textoFin).toContain('LA HERMANDAD');
    expect(fin).toContain('escena:piso');
    expect(b.get('jornada')).toBe(8);
  });

  it('negarse con poca Duda lleva al Final A', () => {
    const b = nueva({ duda: 10 });
    expect(jugar(b, 'j7_nell.peticion', { elecciones: [1] }).comandos).toContain('escena:piso_noche');
    expect(b.get('nell_respuesta')).toBe('negar');
    b.goTo('piso_noche.entrar');
    const texto = conIds(b, 'piso_noche.entrar');
    expect(texto).toContain('Amaba al Gran Hermano');
    expect(texto).toContain('Estasia. Siempre fue Estasia');
  });

  it('negarse con Duda alta deja la decisión para la noche', () => {
    const b = nueva({ duda: 40 });
    jugar(b, 'j7_nell.peticion', { elecciones: [1] });
    expect(b.get('nell_respuesta')).toBe('dudar');
    jugar(b, 'piso_noche.dormir', { elecciones: [0] });
    expect(b.get('nell_respuesta')).toBe('aceptar_tarde');
    const c = nueva({ duda: 40, nell_respuesta: 'dudar' });
    const { comandos } = jugar(c, 'piso_noche.dormir', { elecciones: [1] });
    expect(comandos).toContain('final:A');
  });

  it('denunciar a Nell lleva al Final B temprano', () => {
    const b = nueva();
    expect(jugar(b, 'j7_nell.peticion', { elecciones: [2] }).comandos).toContain('escena:despacho_voss');
    const texto = conIds(b, 'voss_despacho.entrar');
    expect(texto).toContain('Restauro fotografías antiguas');
    expect(texto).toContain('miembro de la organización conocida como la Hermandad');
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

describe('Acto III', () => {
  const nueva = (jornada: number, vars: Record<string, unknown> = {}) => {
    const b = new NarrativeBridge(resultado.json!);
    b.set('jornada', jornada);
    b.set('amory_borrado', true);
    b.set('nell_respuesta', 'aceptar');
    for (const [k, v] of Object.entries(vars)) b.set(k, v);
    return b;
  };
  const inv = (b: NarrativeBridge) => b.list('inventario');

  it('J8: el Registro trae la directiva (0305); Brooke da la pista en el ascensor; quien dudó una noche pasa antes por Nell', () => {
    const b = nueva(8);
    expect(jugar(b, 'depto.salir').texto).toContain('Primero el Registro');
    const { texto } = jugar(b, 'j8_libro', { minijuegos: { registro_j8_fallos: 0 } });
    expect(texto).toContain('Cero tres, cero cinco');
    expect(inv(b)).toContain('directiva');
    expect(jugar(b, 'depto.salir').comandos).toContain('escena:calderas');
    expect(b.get('pista_combinacion')).toBe(true);
    const c = nueva(8, { nell_respuesta: 'aceptar_tarde', registro_j8_hecho: true });
    expect(jugar(c, 'depto.salir').comandos).toContain('escena:suministros');
    expect(jugar(c, 'suministros.entrar').comandos).toContain('escena:calderas');
    expect(inv(c)).toContain('llave_calderas');
  });

  it('J8: el montacargas chirría si se baja deprisa (Sospecha +5) y la planta once arranca el reloj de cuatro minutos', () => {
    const b = nueva(8);
    const { comandos } = jugar(b, 'calderas.montacargas', { minijuegos: { montacargas_j8: 'chirrido' } });
    expect(b.get('sospecha')).toBe(5);
    expect(comandos).toContain('escena:planta11');
    expect(jugar(b, 'planta11.entrar').comandos).toContain('reloj:inicio=23:00:00,limite=240,agotar=planta11.agotado');
    jugar(b, 'planta11.agotado');
    expect(b.get('guardia_entrante')).toBe(true);
    expect(b.get('sospecha')).toBe(10);
  });

  it('J8: sin llave no se abre; la combinación falla con pista y, acertada, se entra al Archivo Restringido', () => {
    const b = nueva(8);
    expect(jugar(b, 'planta11.puerta').texto).toContain('Acero');
    jugar(b, 'planta11.panel', { minijuegos: { cerrojo_j8: 'ok' } });
    expect(b.get('llave_ar')).toBe(true);
    jugar(b, 'planta11.puerta', { minijuegos: { cerrojo_j8: 'fallo' } });
    expect(b.get('cerrojo_intentos')).toBe(1);
    const { texto, comandos } = jugar(b, 'planta11.puerta', { minijuegos: { cerrojo_j8: 'abierta' } });
    expect(texto).toContain('Lo he tenido en la mano esta misma mañana');
    expect(comandos).toEqual(expect.arrayContaining(['reloj:parar', 'escena:archivo_restringido']));
  });

  it('J8: la Planilla Azul sube la Duda 20; la hoja del mercado solo se puede llevar si se ha leído', () => {
    const b = nueva(8, { duda: 30, patron_conclusion: 'cobardes' });
    expect(jugar(b, 'archivo_r.salir').texto).toContain('sin mirar');
    expect(jugar(b, 'archivo_r.semana').texto).toContain('Nos bombardeamos');
    expect(b.get('duda')).toBe(50);
    const { comandos } = jugar(b, 'archivo_r.salir', { elecciones: [1], minijuegos: { copia_lineas: 3 } });
    expect(b.get('prueba_sacada')).toBe('copia');
    expect(inv(b)).toContain('copia_planilla');
    expect(comandos).toContain('escena:planta11');
    const c = nueva(8);
    jugar(c, 'archivo_r.semana');
    jugar(c, 'archivo_r.semana16');
    jugar(c, 'archivo_r.salir', { elecciones: [1] });
    expect(c.get('hoja_robada')).toBe(true);
    expect(inv(c)).toContain('hoja_planilla');
  });

  it('J8: la iniciación guarda cada respuesta; el parte alterado da confianza y cada «no» la quita', () => {
    const c = nueva(8, { prueba_sacada: 'hoja' });
    const { texto, comandos } = jugar(c, 'sotano.entrar', { elecciones: [0, 1, 0, 0, 1, 0] });
    expect(c.get('iniciacion_vida')).toBe('Sí');
    expect(c.get('iniciacion_matar')).toBe('No');
    expect(c.get('iniciacion_ivy')).toBe('No');
    expect(c.get('iniciacion_traicion')).toBe('No');
    expect(c.get('nell_confianza')).toBe(-2);
    expect(texto).toContain('Mientes. Todos traicionan');
    expect(texto).toContain('Folkestone');
    expect(c.get('libro_fragmentos')).toBe(1);
    expect(comandos).toContain('escena:piso_noche');
  });

  it('J9: Voss sospecha de la hoja robada y de la llave; la nota trae el Times falso; el panel solo con vaho o abrigo', () => {
    const b = nueva(9, { hoja_robada: true, llave_ar: true });
    const { texto, comandos } = jugar(b, 'depto.entrar', { minijuegos: { cf_j9_voss: 'fallo' } });
    expect(texto).toContain('Anoche alguien entró en la planta once');
    expect(b.get('sospecha')).toBe(30);
    expect(inv(b)).toEqual(expect.arrayContaining(['tubo', 'times_falso']));
    expect(comandos).toContain('escena:miniver');
    expect(jugar(b, 'lavabos.panel').texto).toContain('Así no');
    jugar(b, 'lavabos.grifos', { minijuegos: { cf_j9_lavabo: 'perfecto' } });
    expect(b.get('vaho')).toBe(true);
    jugar(b, 'lavabos.panel');
    expect(inv(b)).toContain('sobre_miniver');
    expect(inv(b)).not.toContain('times_falso');
    const fin = jugar(b, 'lavabos.puerta');
    expect(fin.texto).toContain('Movieron la fecha un día');
    expect(b.get('times_original_visto')).toBe(true);
    expect(inv(b)).toEqual(expect.arrayContaining(['times_original', 'libro']));
  });

  it('J9: decirle a Syme el nombre de Amory cuesta Sospecha y Duda', () => {
    const b = nueva(9);
    expect(jugar(b, 'j9_syme').texto).toContain('No conozco a ningún Amory');
    expect([b.get('sospecha'), b.get('duda')]).toEqual([3, 3]);
  });

  it('J10: el mitin cambia de enemigo; tocar la pancarta del Gran Hermano cuesta 10', () => {
    const b = nueva(10);
    const { texto, comandos } = jugar(b, 'cantina.entrar', { elecciones: [1], minijuegos: { cf_j10_mitin_bh: 1 } });
    expect(texto).toContain('Pájaros. Dibujé pájaros');
    expect(texto).toContain('Mi silla siempre ha sido mía');
    expect(b.get('pell_j10')).toBe('verdad');
    expect(b.get('sospecha')).toBe(15);
    expect(comandos).toContain('escena:departamento_noche');
  });

  it('J10: la misión de Nell: Brooke cubre una vez; la segunda, Voss lo ve (Sospecha +20) y la misión falla', () => {
    const b = nueva(10, { nota_nell_j10: true, rectificacion_1: 'completa' });
    jugar(b, 'j10_depto.mesa');
    expect(b.get('cargando_prueba')).toBe(true);
    expect(jugar(b, 'j10_depto.carrito').texto).toContain('Falta el parte');
    const { comandos } = jugar(b, 'j10_depto.visto');
    expect(comandos).toContain('seguir:');
    expect(b.get('sospecha')).toBe(0);
    const fallo = jugar(b, 'j10_depto.visto');
    expect(fallo.texto).toContain('El agujero está aquí');
    expect(b.get('mision_j10')).toBe('fallida');
    expect(b.get('sospecha')).toBe(20);
    expect(fallo.comandos).toContain('escena:escalera');
    const c = nueva(10, { nota_nell_j10: true });
    jugar(c, 'j10_depto.mesa');
    jugar(c, 'j10_depto.archivador');
    jugar(c, 'j10_depto.carrito');
    expect(c.get('prueba_rectificacion')).toBe(true);
    expect(c.get('libro_fragmentos')).toBe(3);
  });

  it('J10: de vuelta a casa detienen a Parsons; la hija dice que ahora dice dos nombres', () => {
    const b = nueva(10, { rectificacion_hecha: true });
    const { texto, comandos } = jugar(b, 'escalera.entrar');
    expect(texto).toContain('Ahora dice dos');
    expect(b.get('sospecha')).toBe(5);
    expect(comandos).toContain('escena:piso_noche');
  });

  it('J11: el expediente de Ivy; aceptar el doblepensar baja la Duda; cambiar el nombre de Len lo salva', () => {
    const b = nueva(11, { duda: 50, sospecha: 30 });
    const { texto } = jugar(b, 'j11_expediente', { minijuegos: { dp_j11_ivy: 'aceptar' } });
    expect(texto).toContain('Era él');
    expect(b.get('ivy_revelada')).toBe(true);
    expect(b.get('duda')).toBe(55);
    expect(b.get('sospecha')).toBe(25);
    const c = nueva(11, { expediente_visto: true });
    jugar(c, 'minimor.entrar', { minijuegos: { len_decision: 'cambio', len_sustituto: 'ASH, T.', len_chico: true } });
    expect(c.get('len_salvado')).toBe(true);
    expect(c.get('sospecha')).toBe(10);
    const d = nueva(11, { expediente_visto: true });
    expect(jugar(d, 'minimor.entrar', { minijuegos: { len_decision: 'rabia' } }).texto).toContain('Siempre tenemos copias');
    expect(d.get('sospecha')).toBe(30);
  });

  it('J11: con Crane bajo sospecha, Charrington le recuerda a él; arrancar el cartel cuesta 15 y el diario va al hornillo', () => {
    const b = nueva(11, { crane_info: 2 });
    jugar(b, 'j11_charrington_mirar');
    expect(b.get('crane_sospechado')).toBe(true);
    const c = nueva(11, { dp_j11_ivy: 'recordar', diario_escondite: 'cartel' });
    expect(jugar(c, 'piso_noche.cartel_usar').texto).toContain('Los símbolos del Partido no se destruyen');
    expect(c.get('cartel_arrancado')).toBe(true);
    expect(c.get('diario_escondite')).toBe('hornillo');
    expect(c.get('sospecha')).toBe(15);
  });

  it('J12: si salvó a Len, Dot lo sabe; el sobre de Crane; aceptar el trato lleva al Final B', () => {
    const b = nueva(12, { len_salvado: true, len_sustituto: 'ASH, T.', dot_confianza: 1, desayunado: true });
    expect(jugar(b, 'piso.puerta_usar', { minijuegos: { cf_j12_ejecucion: 'aceptable' } }).texto).toContain('en el lugar de Pike, ASH, T.');
    expect(b.get('dot_confianza')).toBe(3);
    const c = nueva(12, { iniciacion_vida: 'Sí', crane_info: 1, ivy_revelada: true });
    expect(jugar(c, 'depto.entrar').comandos).toContain('escena:estudio');
    expect(c.get('crane_revelado')).toBe(true);
    const { texto, comandos } = jugar(c, 'estudio.crane');
    expect(texto).toContain('«Sí.»');
    expect(texto).toContain('yo la fotografié cantándola');
    expect(texto).toContain('Lo que duele es callar');
    expect(texto).toContain('Lo decidieron hace cinco años');
    expect(comandos).toContain('final:B');
  });

  it('J12: fingir o negarse lleva a la persecución; en casa de Dot llega el mensaje de Nell y el reloj echa a andar', () => {
    const b = nueva(12);
    expect(jugar(b, 'estudio.crane', { elecciones: [1] }).comandos).toContain('escena:callejones');
    expect(b.get('crane_sigue')).toBe(true);
    const c = nueva(12, { crane_decision: 'fingir', dot_confianza: 3, dp_j11_ivy: 'recordar' });
    const { texto, comandos } = jugar(c, 'casa_dot.entrar');
    expect(texto).toContain('Bonita colección');
    expect(texto).toContain('Tú corriste hacia mi niño');
    expect(texto).toContain('El reloj anda');
    expect(c.get('reloj_en_marcha')).toBe(true);
    expect(c.get('mensaje_nell')).toBe(true);
    expect(inv(c)).toEqual(expect.arrayContaining(['dibujos_amory', 'metralla_brillante']));
    expect(comandos).toContain('final:demo');
  });

  it('J12: el atajo prole solo se abre a quien trató a los proles como personas', () => {
    expect(jugar(nueva(12, { dot_confianza: 1 }), 'callejones.atajo').comandos).not.toContain('pos:atajo');
    expect(jugar(nueva(12, { dot_confianza: 2 }), 'callejones.atajo').comandos).toContain('pos:atajo');
  });

  it('Sospecha 100: en el Acto I, vaporización (C0); después, el arresto donde esté (Final C)', () => {
    const b = nueva(2);
    expect(jugar(b, 'arresto').comandos).toContain('final:C0');
    const c = nueva(8, { escena_actual: 'planta11' });
    expect(jugar(c, 'arresto').texto).toContain('Un golpe de porra en la nuca');
    const d = nueva(9, { escena_actual: 'departamento' });
    expect(jugar(d, 'arresto').texto).toContain('Acompáñeles');
  });

  it('cada entrada nueva del diario está declarada en ink', () => {
    const entradas = JSON.parse(fs.readFileSync(path.join(RAIZ, 'content/diario/entradas.json'), 'utf8')).entradas as { id: string }[];
    const b = new NarrativeBridge(resultado.json!);
    for (const e of entradas) {
      expect(b.story.variablesState.GlobalVariableExistsWithName(e.id), e.id).toBe(true);
      expect(b.story.variablesState.GlobalVariableExistsWithName(`${e.id}_escrita`), `${e.id}_escrita`).toBe(true);
    }
  });

  it('los mapas de sigilo declaran sus vigilantes', () => {
    const porId = new Map(localizaciones.map((l) => [l.id, l]));
    const p11 = porId.get('planta11')!;
    expect(p11.sigilo?.alSerVisto).toBe('planta11.visto');
    expect(p11.conosRotativos?.periodo).toBe(6000);
    expect(p11.npcs.find((n) => n.name === 'guardia')?.vigia?.ruta.length).toBe(4);
    expect(porId.get('minimor_archivo')!.sigilo?.ocultos.length).toBe(5);
    expect(porId.get('miniver')!.sigilo?.social).toBe(true);
    expect(porId.get('departamento_noche')!.sigilo?.condicion).toBe('cargando_prueba');
    expect(porId.get('callejones')!.hotspots.filter((h) => h.ruido).length).toBe(5);
    expect(porId.get('callejones')!.hotspots.filter((h) => h.escondite).length).toBe(6);
  });
});
