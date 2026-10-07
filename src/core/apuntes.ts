/**
 * Apuntes (pedidos en las primeras pruebas con jugadores): lo que el protagonista tiene que hacer ahora,
 * la gente que conoce y lo que ha averiguado. Todo sale de content/apuntes.json y se desbloquea con
 * variables de ink, así que nunca adelanta nada. Sin Phaser: se prueba en Node.
 */
import { cumple } from './Location';

/** Lo que se sabe más tarde de alguien: sustituye al texto (y al nombre, si trae uno: el doblepensar lo borra). */
export interface Variante { si: string; texto: string; nombre?: string }
export interface Persona { id: string; nombre: string; si?: string; texto: string; variantes?: Variante[] }
export interface Pista { id: string; titulo: string; si?: string; texto: string }
export interface Apuntes { objetivos: { si?: string; texto: string }[]; personas: Persona[]; pistas: Pista[] }

type Leer = (v: string) => unknown;

/** Lo que hay que hacer ahora: el primer objetivo cuya condición se cumple. */
export function objetivo(a: Apuntes, leer: Leer): string {
  return a.objetivos.find((o) => cumple(o.si, leer))?.texto ?? '';
}

/** La gente que se conoce, con lo último que se sabe de cada uno (gana la última variante que se cumple). */
export function personas(a: Apuntes, leer: Leer): { id: string; nombre: string; texto: string }[] {
  return a.personas.filter((p) => cumple(p.si, leer)).map((p) => {
    const v = [...(p.variantes ?? [])].reverse().find((x) => cumple(x.si, leer));
    return { id: p.id, nombre: v?.nombre ?? p.nombre, texto: v?.texto ?? p.texto };
  });
}

/** Lo que se ha averiguado, en orden. */
export function pistas(a: Apuntes, leer: Leer): Pista[] {
  return a.pistas.filter((p) => cumple(p.si, leer));
}

/** Las variables que usan todas las condiciones (para comprobar que existen en ink). */
export function variables(a: Apuntes): string[] {
  const conds = [...a.objetivos.map((o) => o.si), ...a.personas.flatMap((p) => [p.si, ...(p.variantes ?? []).map((v) => v.si)]), ...a.pistas.map((p) => p.si)];
  return [...new Set(conds.filter(Boolean).flatMap((c) => c!.split('&&').map((x) => /^\s*!?\s*([\w.]+)/.exec(x)?.[1]).filter(Boolean) as string[]))];
}
