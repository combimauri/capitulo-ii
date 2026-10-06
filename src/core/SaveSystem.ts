/** Guardado en localStorage con esquema versionado (diseño técnico §10). */
import type { Dir } from './Location';

export const SAVE_VERSION = 1;
const PREFIJO = 'capitulo2.partida.';

export interface SaveData {
  version: number;
  fecha: string;
  ink: string;
  mundo: { escena: string; x: number; y: number; dir: Dir; reloj?: typeof import('./juego').mision.reloj };
  meta: { jornada: number };
  /** Registro de diálogos (con lo que el doblepensar haya reescrito). */
  registro?: ReturnType<import('./Registro').Registro['serializar']>;
}

function storage(): Storage | null {
  try {
    const s = window.localStorage;
    const k = '__prueba__';
    s.setItem(k, '1');
    s.removeItem(k);
    return s;
  } catch {
    return null;
  }
}

export interface Capitulo { fecha: string; autor: string; texto: string; cierre: string }

export const SaveSystem = {
  disponible(): boolean {
    return storage() !== null;
  },

  guardar(ranura: string, data: Omit<SaveData, 'version' | 'fecha'>): boolean {
    const s = storage();
    if (!s) return false;
    try {
      s.setItem(PREFIJO + ranura, JSON.stringify({ ...data, version: SAVE_VERSION, fecha: new Date().toISOString() }));
      return true;
    } catch {
      return false;
    }
  },

  cargar(ranura: string): SaveData | null {
    const s = storage();
    if (!s) return null;
    try {
      const raw = s.getItem(PREFIJO + ranura);
      if (!raw) return null;
      const data = JSON.parse(raw) as SaveData;
      return data.version === SAVE_VERSION ? data : null;   // migraciones: pendientes
    } catch {
      return null;
    }
  },

  /** Finales alcanzados en cualquier partida (desbloquean líneas del menú). */
  finales(): string[] {
    try { return JSON.parse(storage()?.getItem(PREFIJO + 'finales') ?? '[]') as string[]; } catch { return []; }
  },

  registrarFinal(id: string) {
    const s = storage();
    if (!s) return;
    const lista = new Set(this.finales());
    lista.add(id);
    try { s.setItem(PREFIJO + 'finales', JSON.stringify([...lista])); } catch { /* nada */ }
  },

  /** Galería de Capítulos II escritos en distintas partidas (guion, desbloqueo del Final D). */
  capitulos(): Capitulo[] {
    try { return JSON.parse(storage()?.getItem(PREFIJO + 'capitulos') ?? '[]') as Capitulo[]; } catch { return []; }
  },

  guardarCapitulo(c: Omit<Capitulo, 'fecha'>) {
    const s = storage();
    if (!s) return;
    const lista = [...this.capitulos(), { ...c, fecha: new Date().toISOString() }].slice(-30);
    try { s.setItem(PREFIJO + 'capitulos', JSON.stringify(lista)); } catch { /* nada */ }
  },

  /** La frase de cierre del Capítulo II de la última partida que llegó al Final D (cita del menú). */
  cierreD(): string {
    try { return storage()?.getItem(PREFIJO + 'cierre_d') ?? ''; } catch { return ''; }
  },

  guardarCierreD(texto: string) {
    try { storage()?.setItem(PREFIJO + 'cierre_d', texto); } catch { /* nada */ }
  },

  borrar(ranura: string) {
    try { storage()?.removeItem(PREFIJO + ranura); } catch { /* nada */ }
  },
};
