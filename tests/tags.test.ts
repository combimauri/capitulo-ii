import { describe, expect, it } from 'vitest';
import { parseLine, parseTag } from '../src/core/tags';

describe('parseTag', () => {
  it('clave y valor', () => expect(parseTag('id:j1_01')).toEqual({ key: 'id', value: 'j1_01', params: {} }));
  it('parámetros', () =>
    expect(parseTag('cf:id=CF-J2-ODIO,expr=odio,dif=media').params).toEqual({ id: 'CF-J2-ODIO', expr: 'odio', dif: 'media' }));
  it('etiqueta sin valor', () => expect(parseTag(' cartel ')).toEqual({ key: 'cartel', value: '', params: {} }));
});

describe('parseLine', () => {
  it('diálogo', () => expect(parseLine('AMORY: ¿Te has fijado?')).toEqual({ kind: 'dialogo', speaker: 'AMORY', text: '¿Te has fijado?' }));
  it('pensamiento', () => expect(parseLine('PENSAMIENTO: Ivy.').kind).toBe('pensamiento'));
  it('telepantalla', () => expect(parseLine('TELEPANTALLA: ¡Atención!').kind).toBe('telepantalla'));
  it('nombres con espacios', () => expect(parseLine('HIJA PARSONS: Usted habla dormido.').speaker).toBe('HIJA PARSONS'));
  it('narración', () => expect(parseLine('Llueve.').kind).toBe('narracion'));
  it('no confunde dos puntos dentro de la frase', () =>
    expect(parseLine('Pensé esto: nada.').kind).toBe('narracion'));
});
