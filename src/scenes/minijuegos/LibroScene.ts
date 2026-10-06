/**
 * Lectura del libro de Goldstein (guion J8.09, J9.07, J10.05, J11.08): papel mecanografiado,
 * página a página. Las frases que coinciden con algo que el protagonista ya vio quedan subrayadas;
 * al tocar un subrayado vuelve el recuerdo.
 *   # minijuego:libro,fragmento=1   → content/libro/fragmentos.json
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { interpolar, se_cumple } from '../../core/texto';
import { COLOR, FUENTE, hex } from '../../ui/estilo';
import fragmentos from '../../../content/libro/fragmentos.json';

interface Subrayado { frase: string; si?: string; recuerdo: string }
interface Parrafo { texto: string; subrayado?: Subrayado[] }
interface Fragmento { cabecera?: string[]; capitulo: string; parrafos: Parrafo[] }

const FRAGMENTOS = fragmentos as Record<string, Fragmento>;
const HOJA = { x: 130, y: 20, w: 700, h: 470 };
const MARGEN = 40;
const LETRA = 23;
const INTERLINEA = 30;

interface Palabra { texto: string; subrayado: Subrayado | null }

export class LibroScene extends Minijuego {
  private paginas: (Palabra[][] | 'titulo')[] = [];
  private pagina = 0;
  private capa!: Phaser.GameObjects.Container;
  private recuerdo: Phaser.GameObjects.Container | null = null;
  private anchoLetra = 11;
  private fragmento!: Fragmento;
  private tocoSubrayado = false;

  constructor() { super('Libro'); }

  preload() {
    this.load.image('libro-fondo', 'assets/minijuegos/libro-fondo.png');
    for (const v of [0, 1, 2]) this.load.image(`libro-hoja-${v}`, `assets/minijuegos/libro-hoja-${v}.png`);
  }

  create() {
    this.fragmento = FRAGMENTOS[this.params.fragmento ?? '1'];
    this.pagina = 0; this.recuerdo = null;
    this.cameras.main.fadeIn(500, 11, 12, 15);
    // la mesa del sótano, la vela, las tapas viejas y el fajo cosido con hilo: libro-fondo
    this.add.image(0, 0, 'libro-fondo').setOrigin(0).setScale(2);
    const medida = this.add.text(0, 0, 'MMMMMMMMMM', { fontFamily: FUENTE.maquina, fontSize: `${LETRA}px` });
    this.anchoLetra = medida.width / 10;
    medida.destroy();
    this.paginar();
    this.capa = this.add.container(0, 0);
    this.dibujar();
    this.input.on('pointerup', () => {
      if (this.tocoSubrayado) { this.tocoSubrayado = false; return; }
      this.avanzar();
    });
    this.input.keyboard?.on('keydown', (e: KeyboardEvent) => { if (['Space', 'Enter', 'ArrowRight', 'KeyE'].includes(e.code)) this.avanzar(); });
  }

  /** Reparte los párrafos en páginas, palabra a palabra (la letra de máquina es de ancho fijo). */
  private paginar() {
    const columnas = Math.floor((HOJA.w - MARGEN * 2) / this.anchoLetra);
    const lineasPorPagina = Math.floor((HOJA.h - 120) / INTERLINEA);
    this.paginas = ['titulo'];
    let actual: Palabra[][] = [];
    for (const p of this.fragmento.parrafos) {
      const texto = interpolar(p.texto);
      const subs = (p.subrayado ?? []).filter((s) => se_cumple(s.si) && texto.includes(s.frase));
      // qué letras pertenecen a un subrayado
      const marca: (Subrayado | null)[] = [...texto].map(() => null);
      for (const s of subs) { const i = texto.indexOf(s.frase); for (let k = i; k < i + s.frase.length; k++) marca[k] = s; }
      const palabras: Palabra[] = [];
      let i = 0;
      for (const w of texto.split(' ')) { palabras.push({ texto: w, subrayado: marca[i] ?? null }); i += w.length + 1; }
      // líneas
      const lineas: Palabra[][] = [[]];
      let largo = 0;
      for (const w of palabras) {
        if (largo + w.texto.length > columnas && lineas[lineas.length - 1].length) { lineas.push([]); largo = 0; }
        lineas[lineas.length - 1].push(w);
        largo += w.texto.length + 1;
      }
      if (actual.length + lineas.length > lineasPorPagina && actual.length) { this.paginas.push(actual); actual = []; }
      actual.push(...lineas, []);
    }
    if (actual.length) this.paginas.push(actual);
  }

  private dibujar() {
    this.capa.removeAll(true);
    this.recuerdo?.destroy(); this.recuerdo = null;
    const c = this.capa;
    // la hoja de encima (manchas, una quemadura o una esquina rota, y el hilo que cose el fajo): una de tres variantes
    c.add(this.add.image(HOJA.x, HOJA.y, `libro-hoja-${this.pagina % 3}`).setOrigin(0).setScale(2));
    c.add(this.add.text(HOJA.x + HOJA.w - 20, HOJA.y + HOJA.h - 14, `— ${this.pagina + 1} —`, {
      fontFamily: FUENTE.maquina, fontSize: '18px', color: '#6a5c44',
    }).setOrigin(1, 1));
    const est = { fontFamily: FUENTE.maquina, fontSize: `${LETRA}px`, color: '#2a2218' };
    const pag = this.paginas[this.pagina];
    if (pag === 'titulo') {
      let y = HOJA.y + 120;
      for (const l of this.fragmento.cabecera ?? []) {
        c.add(this.add.text(HOJA.x + HOJA.w / 2, y, l, { ...est, fontSize: '26px' }).setOrigin(0.5));
        y += 40;
      }
      c.add(this.add.text(HOJA.x + HOJA.w / 2, y + 50, this.fragmento.capitulo, { ...est, fontSize: '28px' }).setOrigin(0.5));
      audio.play('papel');
      return;
    }
    let y = HOJA.y + 60;
    for (const linea of pag) {
      let x = HOJA.x + MARGEN;
      for (const w of linea) {
        c.add(this.add.text(x, y, w.texto, est));
        const ancho = w.texto.length * this.anchoLetra;
        if (w.subrayado) {
          const s = w.subrayado;
          const raya = this.add.rectangle(x, y + LETRA + 1, ancho + this.anchoLetra, 2, COLOR.rojo3).setOrigin(0);
          const zona = this.add.rectangle(x, y, ancho + this.anchoLetra, LETRA + 4, 0, 0).setOrigin(0).setInteractive({ useHandCursor: true });
          zona.on('pointerup', () => { this.tocoSubrayado = true; this.mostrarRecuerdo(s); });
          c.add([raya, zona]);
        }
        x += ancho + this.anchoLetra;
      }
      y += INTERLINEA;
    }
    audio.play('papel');
  }

  private mostrarRecuerdo(s: Subrayado) {
    this.recuerdo?.destroy();
    const { width } = this.scale;
    const t = this.add.text(width / 2, 0, interpolar(s.recuerdo), {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), align: 'center', wordWrap: { width: 640 },
    }).setOrigin(0.5, 0);
    const fondo = this.add.rectangle(width / 2, -10, 680, t.height + 24, 0x3a2a1c, 0.95).setOrigin(0.5, 0).setStrokeStyle(2, 0xc4ab7e);
    this.recuerdo = this.add.container(0, 470, [fondo, t]).setAlpha(0);
    this.tweens.add({ targets: this.recuerdo, alpha: 1, duration: 250 });
    audio.play('grieta');
  }

  private avanzar() {
    if (this.recuerdo) { this.recuerdo.destroy(); this.recuerdo = null; return; }
    if (this.pagina < this.paginas.length - 1) { this.pagina++; this.dibujar(); return; }
    this.terminar({ resultado: 'leido' }, 600);
  }
}
