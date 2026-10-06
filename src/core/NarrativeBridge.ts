/**
 * Puente entre ink (estado narrativo) y el motor (diseño técnico §2).
 * No depende de Phaser para poder probarse en Node.
 */
import { Story } from 'inkjs';
import { parseLine, parseTag, type ParsedLine, type Tag } from './tags';

export interface Line extends ParsedLine {
  id: string | null;
  tags: Tag[];
}

export interface ChoiceOption {
  index: number;
  text: string;
  tags: Tag[];
}

export type Step =
  | { type: 'line'; line: Line }
  | { type: 'choices'; choices: ChoiceOption[] }
  | { type: 'end' };

type Listener = (...args: any[]) => void;

/** Etiquetas que son comandos para el motor (no metadatos de la línea). */
const COMANDOS = new Set(['escena', 'pos', 'jornada', 'cf', 'dp', 'minijuego', 'sigilo', 'documento',
  'comparar', 'sfx', 'musica', 'ambiente', 'fx', 'esperar', 'bloquear_input', 'final']);

export class NarrativeBridge {
  readonly story: Story;
  private listeners = new Map<string, Set<Listener>>();

  constructor(json: string) {
    this.story = new Story(json);
    this.story.onError = (msg) => console.error('[ink]', msg);
  }

  // ---------------------------------------------------------------- eventos
  on(event: string, fn: Listener): () => void {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(fn);
    return () => this.listeners.get(event)?.delete(fn);
  }

  private emit(event: string, ...args: unknown[]) {
    this.listeners.get(event)?.forEach((fn) => fn(...args));
  }

  // ---------------------------------------------------------------- flujo
  /** Salta a un knot o stitch ("piso.cartel_mirar"). */
  goTo(path: string) {
    this.story.ChoosePathString(path);
  }

  hasPath(path: string): boolean {
    try {
      const [knot, stitch] = path.split('.');
      const k = this.story.KnotContainerWithName(knot);
      if (!k) return false;
      return stitch ? k.namedContent.has(stitch) : true;
    } catch {
      return false;
    }
  }

  /** Avanza un paso: una línea, un conjunto de opciones o el final del fragmento. */
  next(): Step {
    while (this.story.canContinue) {
      const text = this.story.Continue() ?? '';
      const tags = (this.story.currentTags ?? []).map(parseTag);
      for (const t of tags) if (COMANDOS.has(t.key)) this.emit('command', t);
      if (!text.trim()) continue;          // línea vacía: solo traía comandos
      const id = tags.find((t) => t.key === 'id')?.value ?? null;
      return { type: 'line', line: { ...parseLine(text), id, tags } };
    }
    if (this.story.currentChoices.length) {
      return {
        type: 'choices',
        choices: this.story.currentChoices.map((c) => ({
          index: c.index, text: c.text, tags: (c.tags ?? []).map(parseTag),
        })),
      };
    }
    return { type: 'end' };
  }

  choose(index: number) {
    this.story.ChooseChoiceIndex(index);
  }

  // ---------------------------------------------------------------- variables
  get<T = unknown>(name: string): T {
    return this.story.variablesState.$(name) as T;
  }

  set(name: string, value: unknown) {
    this.story.variablesState.$(name, value as never);
  }

  observe(name: string, fn: (value: unknown) => void) {
    this.story.ObserveVariable(name, (_n: string, v: unknown) => fn(v));
  }

  call(fn: string, ...args: unknown[]) {
    return this.story.EvaluateFunction(fn, args as never[]);
  }

  // ---------------------------------------------------------------- guardado
  saveState(): string {
    return this.story.state.ToJson();
  }

  loadState(json: string) {
    this.story.state.LoadJson(json);
  }

  reset() {
    this.story.ResetState();
  }
}
