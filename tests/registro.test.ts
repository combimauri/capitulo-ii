/** Registro de diálogos y doblepensar (diseño técnico §7.1). */
import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { BORRADO, coincide, Registro } from '../src/core/Registro';

const ALIAS = ['Felix Amory', 'Amory'];
const LINEAS = ['j1_05_amory_*', 'j2_04_amory_*'];

function conHistoria() {
  const r = new Registro();
  r.anotar('j1_05_amory_01', 'AMORY', '¿Te ha hablado Voss? ¿A ti?');
  r.anotar('j1_05_amory_mirar', 'PENSAMIENTO', 'Felix Amory. Dibuja mapas con la lengua entre los dientes.');
  r.anotar('j1_06_pens_01', 'PENSAMIENTO', 'Amory habla demasiado rápido.');
  r.anotar('j1_05_voss_01', 'VOSS', 'Camarada Reyes. Un momento.');
  r.anotar('j2_04_amory_04', 'AMORY', 'Toma, usa el mío.');
  return r;
}

describe('registro', () => {
  it('los patrones admiten comodines', () => {
    expect(coincide('j2_04_amory_03', LINEAS)).toBe(true);
    expect(coincide('j2_04_voss_03', LINEAS)).toBe(false);
  });

  it('no duplica una línea que se vuelve a leer y no anota líneas sin id', () => {
    const r = conHistoria();
    r.anotar('j1_05_voss_01', 'VOSS', 'Camarada Reyes. Un momento.');
    r.anotar(null, 'VOSS', 'Sin id');
    expect(r.entradas).toHaveLength(5);
  });

  it('aceptar borra el nombre del hablante y del texto, y deja el resto intacto', () => {
    const r = conHistoria();
    const afectadas = r.doblepensar(LINEAS, ALIAS, 'aceptar');
    expect(afectadas.map((e) => e.id)).toEqual(['j1_05_amory_01', 'j1_05_amory_mirar', 'j1_06_pens_01', 'j2_04_amory_04']);
    expect(r.entradas[0].hablante).toBe(BORRADO);
    expect(r.entradas[1].texto).toBe(`${BORRADO}. Dibuja mapas con la lengua entre los dientes.`);
    expect(r.entradas[2].texto).toBe(`${BORRADO} habla demasiado rápido.`);
    expect(r.entradas[3]).toMatchObject({ hablante: 'VOSS', estado: 'normal' });
    expect(r.entradas[0].original?.hablante).toBe('AMORY');
  });

  it('recordar conserva el nombre, tachado', () => {
    const r = conHistoria();
    r.doblepensar(LINEAS, ALIAS, 'recordar');
    expect(r.entradas[0]).toMatchObject({ hablante: 'AMORY', estado: 'tachada' });
    expect(r.aliasDe(r.entradas[0])).toEqual(ALIAS);
    expect(r.nombra(r.entradas[0], ALIAS)).toBe(true);
    expect(r.nombra(r.entradas[1], ALIAS)).toBe(false);
  });

  it('lo que se anota después del doblepensar también se reescribe', () => {
    const r = conHistoria();
    r.doblepensar(LINEAS, ALIAS, 'aceptar');
    r.anotar('j3_02_prot_01', 'PROTAGONISTA', 'Disculpe, camarada. ¿Sabe dónde se ha sentado hoy Amory?');
    expect(r.entradas.at(-1)?.texto).toBe(`Disculpe, camarada. ¿Sabe dónde se ha sentado hoy ${BORRADO}?`);
  });

  it('reescribir: aceptar cambia lo que se dijo; recordar lo conserva, tachado', () => {
    const a = new Registro();
    a.anotar('j1_07_tp_02', 'TELEPANTALLA', 'Nuestras fuerzas han aplastado al enemigo.');
    a.reescribir({ j1_07_tp_02: 'Nuestras fuerzas han resistido con firmeza.' }, 'aceptar');
    expect(a.entradas[0]).toMatchObject({ texto: 'Nuestras fuerzas han resistido con firmeza.', estado: 'reescrita' });
    const r = new Registro();
    r.anotar('j1_07_tp_02', 'TELEPANTALLA', 'Nuestras fuerzas han aplastado al enemigo.');
    r.reescribir({ j1_07_tp_02: 'Otra cosa.' }, 'recordar');
    expect(r.entradas[0]).toMatchObject({ texto: 'Nuestras fuerzas han aplastado al enemigo.', estado: 'tachada' });
  });

  it('se guarda y se restaura con las decisiones', () => {
    const r = conHistoria();
    r.doblepensar(LINEAS, ALIAS, 'aceptar');
    const copia = new Registro();
    copia.cargar(JSON.parse(JSON.stringify(r.serializar())));
    expect(copia.entradas).toEqual(r.entradas);
    copia.anotar('j3_x', 'AMORY', 'Hola');
    expect(copia.entradas.at(-1)?.hablante).toBe(BORRADO);
  });

  it('cada # dp:id=… de ink tiene su configuración, con alias y patrones', () => {
    const raiz = path.resolve(__dirname, '..');
    const ink = fs.readdirSync(path.join(raiz, 'content/ink/acto1')).map((f) => fs.readFileSync(path.join(raiz, 'content/ink/acto1', f), 'utf8')).join('\n');
    const ids = [...ink.matchAll(/# dp:id=([\w-]+)/g)].map((m) => m[1]);
    expect(ids.length).toBeGreaterThan(0);
    for (const id of ids) {
      const c = JSON.parse(fs.readFileSync(path.join(raiz, 'content/doblepensar', `${id}.json`), 'utf8'));
      expect((c.alias?.length ?? 0) + Object.keys(c.reescribir ?? {}).length, id).toBeGreaterThan(0);
      expect(c.lineas.length).toBeGreaterThan(0);
      expect(c.aceptar && c.recordar && c.telepantalla).toBeTruthy();
    }
  });
});
