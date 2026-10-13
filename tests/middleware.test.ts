/** Middleware de Vercel: lista blanca de países. */
import { describe, expect, it } from 'vitest';
import middleware from '../middleware';

const pedir = (pais?: string, ruta = '/', dominio = 'capitulo-ii.vercel.app') =>
  middleware(new Request(`https://${dominio}${ruta}`, { headers: pais ? { 'x-vercel-ip-country': pais } : {} }));

describe('middleware: lista blanca de países', () => {
  it('deja pasar a Latinoamérica (salvo México, Colombia y Puerto Rico) y a Europa', () => {
    for (const pais of ['AR', 'BO', 'BR', 'CL', 'UY', 'PE', 'GT', 'HN', 'ES', 'FR', 'DE', 'GB', 'CH', 'NO', 'UA', 'pt']) {
      const r = pedir(pais);
      expect(r.status, pais).toBe(200);
      expect(r.headers.get('x-middleware-next'), pais).toBe('1');
    }
  });

  it('a los demás países, y sin país conocido, les responde 403 en cualquier ruta (también los recursos)', async () => {
    for (const [pais, ruta] of [['US', '/'], ['MX', '/sw.js'], ['CO', '/assets/index.js'], ['PR', '/'], ['JP', '/'], [undefined, '/']] as const) {
      const r = pedir(pais, ruta);
      expect(r.status, `${pais} ${ruta}`).toBe(403);
      expect(r.headers.get('x-middleware-next')).toBeNull();
      expect(r.headers.get('cache-control')).toBe('no-store');
    }
    expect(await pedir('US').text()).toContain('no está disponible');
  });

  it('vale igual en el dominio propio', () => {
    expect(pedir('BO', '/', 'capitulo-ii.combinatoria.club').status).toBe(200);
    expect(pedir('US', '/assets/index.js', 'capitulo-ii.combinatoria.club').status).toBe(403);
  });
});
