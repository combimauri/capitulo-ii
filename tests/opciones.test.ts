/** Opciones (diseño técnico §9) y copia de seguridad de la partida (§10.2). */
import { beforeEach, describe, expect, it } from 'vitest';

/** localStorage de mentira: el guardado y las opciones solo existen en el navegador. */
function almacen() {
  const m = new Map<string, string>();
  return {
    getItem: (k: string) => m.get(k) ?? null,
    setItem: (k: string, v: string) => { m.set(k, String(v)); },
    removeItem: (k: string) => { m.delete(k); },
  };
}

beforeEach(() => {
  (globalThis as unknown as { window: unknown }).window = { localStorage: almacen() };
});

describe('opciones', () => {
  it('sin nada guardado, las de siempre; los valores no válidos se ignoran', async () => {
    window.localStorage.setItem('capitulo2.opciones.juego', JSON.stringify({ texto: 'turbo', ui: 125 }));
    const { opciones, fijarOpcion, alCambiarOpcion } = await import('../src/core/Opciones');
    expect(opciones.texto).toBe('normal');
    const cambios: string[] = [];
    const quitar = alCambiarOpcion((k) => cambios.push(k));
    fijarOpcion('cf', 'asistida');
    quitar();
    fijarOpcion('cf', 'normal');
    expect(cambios).toEqual(['cf']);
    expect(JSON.parse(window.localStorage.getItem('capitulo2.opciones.juego')!).cf).toBe('normal');
  });
});

describe('exportar e importar la partida', () => {
  it('lo exportado se vuelve a leer igual; lo que no es una partida, o es de otra versión, se rechaza', async () => {
    const { SaveSystem, SAVE_VERSION } = await import('../src/core/SaveSystem');
    expect(SaveSystem.exportar()).toBeNull();
    SaveSystem.guardar('auto', { ink: '{"x":1}', mundo: { escena: 'piso', x: 10, y: 20, dir: 'abajo' }, meta: { jornada: 4 } });
    const texto = SaveSystem.exportar()!;
    const leida = SaveSystem.leerExportada(texto);
    expect(typeof leida).toBe('object');
    expect(leida).toEqual(SaveSystem.cargar('auto'));
    expect(SaveSystem.leerExportada('{"hola":1}')).toBeTypeOf('string');
    expect(SaveSystem.leerExportada('no es json')).toBeTypeOf('string');
    const vieja = JSON.parse(texto); vieja.version = SAVE_VERSION + 1;
    expect(SaveSystem.leerExportada(JSON.stringify(vieja))).toMatch(/otra versión/);
    SaveSystem.borrar('auto');
    expect(SaveSystem.importar('auto', leida as never)).toBe(true);
    expect(SaveSystem.cargar('auto')?.meta.jornada).toBe(4);
  });
});
