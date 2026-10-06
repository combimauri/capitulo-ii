/**
 * Registro de diálogos (diseño técnico §7.1): el historial de lo que el jugador ha leído.
 * Es un elemento jugable: el doblepensar lo reescribe. No depende de Phaser.
 */

export type EstadoEntrada = 'normal' | 'reescrita' | 'tachada';

export interface EntradaRegistro {
  id: string;
  /** Hablante tal como lo escribe ink (AMORY, PENSAMIENTO, PROTAGONISTA…). */
  hablante: string;
  texto: string;
  estado: EstadoEntrada;
  original?: { hablante: string; texto: string };
}

/** Patrón con comodines: "j2_04_amory_*" → /^j2_04_amory_.*$/ */
export function coincide(id: string, patrones: string[]): boolean {
  return patrones.some((p) => new RegExp(`^${p.replace(/[.+?^${}()[\]\\]/g, '\\$&').replace(/\*/g, '.*')}$`).test(id));
}

export const BORRADO = '—';

/** Una persona y sus formas de nombrarla, de la más larga a la más corta ("Felix Amory", "Amory"). */
export type Alias = string[];

const escapar = (t: string) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const regexAlias = (alias: Alias, flags = 'i') =>
  new RegExp(`\\b(${[...alias].sort((a, b) => b.length - a.length).map(escapar).join('|')})\\b`, flags);

export class Registro {
  entradas: EntradaRegistro[] = [];
  /** Personas sobre las que ya se ha hecho doblepensar: aceptadas (se borran) o recordadas (se tachan). */
  private decisiones: { alias: Alias; decision: 'aceptar' | 'recordar' }[] = [];

  anotar(id: string | null, hablante: string | null, texto: string) {
    if (!id) return;
    if (this.entradas.some((e) => e.id === id)) return;   // líneas repetidas (diálogos que se releen)
    const e: EntradaRegistro = { id, hablante: hablante ?? '', texto, estado: 'normal' };
    for (const d of this.decisiones) this.aplicar(e, d.alias, d.decision);
    this.entradas.push(e);
  }

  /** Entradas que tocaría un doblepensar: las de los patrones y cualquiera que nombre a la persona. */
  afectadas(patrones: string[], alias: Alias): EntradaRegistro[] {
    const re = regexAlias(alias);
    return this.entradas.filter((e) => coincide(e.id, patrones) || re.test(e.hablante) || re.test(e.texto));
  }

  /**
   * Aceptar: el nombre desaparece ("—") del hablante y del texto.
   * Recordar: se conserva, pero tachado.
   */
  doblepensar(patrones: string[], alias: Alias, decision: 'aceptar' | 'recordar'): EntradaRegistro[] {
    const afectadas = this.afectadas(patrones, alias);
    for (const e of afectadas) this.aplicar(e, alias, decision);
    this.decisiones.push({ alias, decision });
    return afectadas;
  }

  private aplicar(e: EntradaRegistro, alias: Alias, decision: 'aceptar' | 'recordar') {
    const re = regexAlias(alias);
    if (!re.test(e.hablante) && !re.test(e.texto)) return;
    e.original ??= { hablante: e.hablante, texto: e.texto };
    if (decision === 'recordar') { e.estado = 'tachada'; return; }
    if (re.test(e.hablante)) e.hablante = BORRADO;
    e.texto = e.texto.replace(regexAlias(alias, 'g'), BORRADO);
    e.estado = 'reescrita';
  }

  /** Si la entrada quedó tachada por recordar a alguien, sus alias (para tachar el nombre en el texto). */
  aliasDe(e: EntradaRegistro): Alias | null {
    if (e.estado !== 'tachada') return null;
    return this.decisiones.find((d) => d.decision === 'recordar' && regexAlias(d.alias).test(`${e.hablante} ${e.texto}`))?.alias ?? null;
  }

  /** ¿El hablante de esta entrada es la persona? */
  nombra(e: EntradaRegistro, alias: Alias) { return regexAlias(alias).test(e.hablante); }

  serializar() {
    return { entradas: this.entradas, decisiones: this.decisiones };
  }

  cargar(datos?: { entradas?: EntradaRegistro[]; decisiones?: { alias: Alias; decision: 'aceptar' | 'recordar' }[] } | null) {
    this.entradas = datos?.entradas ?? [];
    this.decisiones = datos?.decisiones ?? [];
  }

  vaciar() { this.cargar(null); }
}
