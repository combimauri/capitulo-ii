// Compila content/ink/main.ink y muestra errores y avisos (uso: node tools/compilar-ink.mjs)
import fs from 'node:fs';
import path from 'node:path';
import { Compiler, CompilerOptions } from 'inkjs/compiler/Compiler';
import { PosixFileHandler } from 'inkjs/compiler/FileHandler/PosixFileHandler';

const main = path.resolve('content/ink/main.ink');
const mensajes = [];
const opciones = new CompilerOptions('main.ink', [], false, (m, t) => mensajes.push([t, m]), new PosixFileHandler(path.dirname(main) + '/'));
try {
  new Compiler(fs.readFileSync(main, 'utf8'), opciones).Compile();
} catch { /* los errores ya están en mensajes */ }
for (const [t, m] of mensajes) console.log(t === 2 ? 'ERROR' : 'aviso', m);
console.log(mensajes.some(([t]) => t === 2) ? 'FALLO' : 'OK');
