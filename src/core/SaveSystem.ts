/** Guardado en localStorage con esquema versionado (diseño técnico §10). */
import type { Dir } from './Location';

export const SAVE_VERSION = 1;
const PREFIJO = 'capitulo2.partida.';

export interface SaveData {
  version: number;
  fecha: string;
  ink: string;
  mundo: { escena: string; x: number; y: number; dir: Dir };
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

  borrar(ranura: string) {
    try { storage()?.removeItem(PREFIJO + ranura); } catch { /* nada */ }
  },
};
