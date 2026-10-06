/** Texto de los datos (documentos, libro, crimen facial): {variables} de ink y líneas condicionales. */
import { narrativa } from './juego';
import { cumple } from './Location';

/** Una línea de texto, o una línea que solo aparece si se cumple su condición ("var", "var==v", "var>=3"…). */
export type Linea = string | { texto: string; si?: string };

/** Sustituye {variable} por su valor en ink. */
export const interpolar = (s: string) => s.replace(/\{(\w+)\}/g, (_, v) => String(narrativa.get(v) ?? ''));

export const se_cumple = (condicion?: string) => cumple(condicion, (v) => narrativa.get(v));

/** Las líneas que tocan según el estado, ya interpoladas. */
export const lineas = (ls: Linea[] = []) =>
  ls.filter((l) => typeof l === 'string' || se_cumple(l.si)).map((l) => interpolar(typeof l === 'string' ? l : l.texto));
