/** Middleware de Vercel: lista blanca de países. */
import { describe, expect, it } from 'vitest';
import middleware from '../middleware';

const pedir = (pais?: string, ruta = '/') =>
  middleware(new Request(`https://capitulo-ii.vercel.app${ruta}`, { headers: pais ? { 'x-vercel-ip-country': pais } : {} }));

describe('middleware: lista blanca de países', () => {
  it('deja pasar a Argentina, Bolivia, Brasil, Chile y España', () => {
    for (const pais of ['AR', 'BO', 'BR', 'CL', 'ES']) {
      const r = pedir(pais);
      expect(r.status, pais).toBe(200);
      expect(r.headers.get('x-middleware-next'), pais).toBe('1');
    }
  });

  it('a los demás países, y sin país conocido, les responde 403 en cualquier ruta (también los recursos)', async () => {
    for (const [pais, ruta] of [['US', '/'], ['MX', '/sw.js'], ['FR', '/assets/index.js'], [undefined, '/']] as const) {
      const r = pedir(pais, ruta);
      expect(r.status, `${pais} ${ruta}`).toBe(403);
      expect(r.headers.get('x-middleware-next')).toBeNull();
      expect(r.headers.get('cache-control')).toBe('no-store');
    }
    expect(await pedir('US').text()).toContain('no está disponible');
  });
});
