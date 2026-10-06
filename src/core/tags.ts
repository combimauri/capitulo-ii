/**
 * Etiquetas de ink (diseño técnico §4.5).
 *   "id:j1_01_tp_01"                → { key: 'id', value: 'j1_01_tp_01', params: {} }
 *   "cf:id=CF-J2-ODIO,expr=odio"    → { key: 'cf', value: 'id=…', params: { id: 'CF-J2-ODIO', expr: 'odio' } }
 *   "cartel"                        → { key: 'cartel', value: '', params: {} }
 */
export interface Tag {
  key: string;
  value: string;
  params: Record<string, string>;
}

export function parseTag(raw: string): Tag {
  const text = raw.trim();
  const i = text.indexOf(':');
  const key = (i === -1 ? text : text.slice(0, i)).trim();
  const value = i === -1 ? '' : text.slice(i + 1).trim();
  const params: Record<string, string> = {};
  if (value.includes('=')) {
    for (const part of value.split(',')) {
      const [k, ...rest] = part.split('=');
      if (k) params[k.trim()] = rest.join('=').trim();
    }
  }
  return { key, value, params };
}

export type LineKind = 'dialogo' | 'pensamiento' | 'telepantalla' | 'cartel' | 'narracion';

export interface ParsedLine {
  kind: LineKind;
  speaker: string | null;
  text: string;
}

const ESPECIALES: Record<string, LineKind> = {
  PENSAMIENTO: 'pensamiento',
  TELEPANTALLA: 'telepantalla',
  CARTEL: 'cartel',
};

/** "AMORY: Hola." → { kind: 'dialogo', speaker: 'AMORY', text: 'Hola.' } */
export function parseLine(raw: string): ParsedLine {
  const text = raw.trim();
  const m = /^([A-ZÁÉÍÓÚÜÑ][A-ZÁÉÍÓÚÜÑ0-9 .'()-]*?)\s*:\s+(.*)$/u.exec(text);
  if (!m) return { kind: 'narracion', speaker: null, text };
  const speaker = m[1].trim();
  const kind = ESPECIALES[speaker.split(' ')[0]] ?? 'dialogo';
  return { kind, speaker: kind === 'dialogo' ? speaker : null, text: m[2].trim() };
}
