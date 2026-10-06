/**
 * Plugin de Vite que compila archivos .ink (con sus INCLUDE) a JSON de ink.
 * `import historia from '../content/ink/main.ink'` devuelve el JSON como string.
 */
import fs from 'node:fs';
import path from 'node:path';
import type { Plugin } from 'vite';
import { Compiler, CompilerOptions } from 'inkjs/compiler/Compiler';
import { PosixFileHandler } from 'inkjs/compiler/FileHandler/PosixFileHandler';

const ERROR = 2;

export interface InkResult {
  json: string | null;
  errors: string[];
  warnings: string[];
  files: string[];
}

export function compileInk(file: string): InkResult {
  const root = path.dirname(file) + path.sep;
  const base = new PosixFileHandler(root);
  const files = new Set<string>([file]);
  const handler = {
    ResolveInkFilename: (f: string) => base.ResolveInkFilename(f),
    LoadInkFileContents: (f: string) => {
      files.add(path.resolve(root, f));
      return base.LoadInkFileContents(f);
    },
  };
  const errors: string[] = [];
  const warnings: string[] = [];
  const options = new CompilerOptions(path.basename(file), [], false,
    (msg: string, type: number) => (type === ERROR ? errors : warnings).push(msg), handler);
  let json: string | null = null;
  try {
    json = new Compiler(fs.readFileSync(file, 'utf8'), options).Compile().ToJson() ?? null;
  } catch {
    // los errores ya están en `errors`
  }
  return { json, errors, warnings, files: [...files] };
}

export default function inkPlugin(): Plugin {
  return {
    name: 'capitulo-ii:ink',
    enforce: 'pre',
    load(id) {
      if (!id.endsWith('.ink')) return null;
      const r = compileInk(id);
      r.files.forEach((f) => this.addWatchFile(f));
      r.warnings.forEach((w) => this.warn(w));
      if (!r.json || r.errors.length) this.error(`ink:\n${r.errors.join('\n')}`);
      return `export default ${JSON.stringify(r.json)};`;
    },
  };
}
