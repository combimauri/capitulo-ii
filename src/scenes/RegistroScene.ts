/**
 * Registro de diálogos (diseño técnico §7.1) y doblepensar.
 *   Consulta:     tecla L o botón REG. → historial desplazable.
 *   Doblepensar:  # dp:id=DP-J3-AMORY  → configuración en content/doblepensar/DP-J3-AMORY.json.
 *                 El registro se desplaza solo hasta las líneas afectadas, los nombres se deshacen
 *                 y el jugador decide: aceptar (el nombre desaparece) o recordar (queda tachado).
 */
import Phaser from 'phaser';
import { Minijuego } from './minijuegos/Minijuego';
import { narrativa, registro } from '../core/juego';
import { BORRADO, type Alias, type EntradaRegistro } from '../core/Registro';
import { audio } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';

interface DpConfig {
  lineas: string[];
  alias: Alias;
  telepantalla: string;
  aceptar: string;
  recordar: string;
}
const CONFIGS = import.meta.glob('../../content/doblepensar/*.json', { eager: true, import: 'default' }) as Record<string, DpConfig>;
const configDe = (id?: string) => Object.entries(CONFIGS).find(([ruta]) => id && ruta.endsWith(`/${id}.json`))?.[1];

const LISTA = { x: 70, y: 74, w: 820, h: 360 };
const COL_TEXTO = 236;
const RUIDO = '▓▒░#%&@$*';

interface Fila { entrada: EntradaRegistro; y: number; hablante: Phaser.GameObjects.Text; texto: Phaser.GameObjects.Text; tachon: Phaser.GameObjects.Rectangle }

/** Tacha las apariciones de un nombre con el carácter combinado U+0336. */
const tachar = (texto: string, alias: Alias) =>
  texto.replace(new RegExp(`\\b(${alias.join('|')})\\b`, 'g'), (m) => [...m].map((c) => c + '̶').join(''));

export class RegistroScene extends Minijuego {
  private contenido!: Phaser.GameObjects.Container;
  private filas: Fila[] = [];
  private alto = 0;
  private desplazamiento = 0;
  private dp: DpConfig | null = null;
  private ruido: Phaser.GameObjects.Graphics | null = null;
  /** El listado se ve a través de su propia cámara (recorta sin máscaras y se desplaza con scrollY). */
  private camLista!: Phaser.Cameras.Scene2D.Camera;
  /** Y otra por encima para lo que se superpone al listado (opciones, telepantalla, estática). */
  private camSobre!: Phaser.Cameras.Scene2D.Camera;

  constructor() { super('Registro'); }

  create() {
    this.filas = []; this.desplazamiento = 0; this.ruido = null;
    this.dp = this.params.id ? configDe(this.params.id) ?? null : null;
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(200, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, COLOR.negro, 0.94).setOrigin(0).setInteractive();
    this.add.rectangle(LISTA.x - 14, LISTA.y - 14, LISTA.w + 28, LISTA.h + 28, COLOR.gris1).setOrigin(0).setStrokeStyle(2, COLOR.gris3);
    this.add.text(width / 2, 30, 'REGISTRO', { fontFamily: FUENTE.maquina, fontSize: '32px', color: hex(COLOR.papel4) }).setOrigin(0.5);

    this.contenido = this.add.container(0, 0);
    this.camLista = this.cameras.add(LISTA.x, LISTA.y, LISTA.w, LISTA.h).setScroll(LISTA.x, LISTA.y);
    this.cameras.main.ignore(this.contenido);
    this.children.list.forEach((o) => { if (o !== this.contenido) this.camLista.ignore(o); });
    this.camSobre = this.cameras.add(0, 0, width, height);
    this.camSobre.ignore(this.children.list.slice());
    this.maquetar();
    this.irA(this.maxDesplazamiento());

    if (this.dp) {
      void this.doblepensar(this.dp);
    } else {
      this.controlesConsulta();
    }
  }

  // ------------------------------------------------------------------ lista
  private maquetar() {
    this.contenido.removeAll(true);
    this.filas = [];
    let y = LISTA.y + 6;
    const nombre = String(narrativa.get('nombre') || '').toUpperCase();
    if (!registro.entradas.length) {
      this.contenido.add(this.add.text(LISTA.x + LISTA.w / 2, LISTA.y + LISTA.h / 2, 'Aún no hay nada escrito.', {
        fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.gris3),
      }).setOrigin(0.5));
    }
    for (const e of registro.entradas) {
      const tipo = e.hablante === 'PENSAMIENTO' ? 'pens' : e.hablante === 'TELEPANTALLA' ? 'tele' : 'dialogo';
      const etiqueta = this.etiqueta(e, nombre);
      const color = tipo === 'tele' ? COLOR.tele5 : tipo === 'pens' ? COLOR.papel3 : COLOR.papel4;
      const hablante = this.add.text(LISTA.x + 10, y, etiqueta, {
        fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(color),
      });
      const textoVisible = e.estado === 'tachada' && this.dp === null ? this.textoTachado(e) : e.texto;
      const texto = this.add.text(LISTA.x + COL_TEXTO, y, this.formato(e, textoVisible), {
        fontFamily: FUENTE.texto, fontSize: '18px', color: hex(tipo === 'pens' ? 0xa8a290 : color), lineSpacing: 4,
        wordWrap: { width: LISTA.w - COL_TEXTO - 16, useAdvancedWrap: true },
      });
      const alias = registro.aliasDe(e);
      const tachon = this.add.rectangle(hablante.x - 2, y + 11, hablante.width + 4, 2, COLOR.rojo4).setOrigin(0, 0.5)
        .setVisible(!!alias && registro.nombra(e, alias));
      this.contenido.add([hablante, texto, tachon]);
      this.filas.push({ entrada: e, y: y - LISTA.y, hablante, texto, tachon });
      y += Math.max(texto.height, 22) + 12;
    }
    this.alto = y - LISTA.y;
  }

  private etiqueta(e: EntradaRegistro, nombre = String(narrativa.get('nombre') || '').toUpperCase()) {
    return e.hablante === 'PROTAGONISTA' ? nombre : e.hablante === 'PENSAMIENTO' ? '' : e.hablante;
  }

  /** Los pensamientos van entre paréntesis. */
  private formato(e: EntradaRegistro, texto: string) {
    return e.hablante === 'PENSAMIENTO' ? `(${texto})` : texto;
  }

  private textoTachado(e: EntradaRegistro) {
    const alias = registro.aliasDe(e);
    return alias ? tachar(e.texto, alias) : e.texto;
  }

  /** Lo que no es el listado (avisos, opciones, estática) se dibuja por encima, con su cámara. */
  private fuera<T extends Phaser.GameObjects.GameObject>(o: T): T {
    this.cameras.main.ignore(o);
    this.camLista.ignore(o);
    return o;
  }

  private maxDesplazamiento() { return Math.max(0, this.alto - LISTA.h + 6); }

  private irA(d: number) {
    this.desplazamiento = Phaser.Math.Clamp(d, 0, this.maxDesplazamiento());
    this.camLista.scrollY = LISTA.y + this.desplazamiento;
  }

  private controlesConsulta() {
    const { width } = this.scale;
    const cerrar = this.fuera(this.add.text(width - 70, 30, 'CERRAR ✕', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel3) })
      .setOrigin(1, 0.5).setInteractive({ useHandCursor: true }));
    cerrar.on('pointerup', () => this.cerrar());
    this.fuera(this.add.text(width / 2, 486, this.sys.game.device.os.desktop ? 'Rueda o flechas para desplazar · L o Esc para cerrar' : 'Desliza para desplazar', {
      fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.gris3),
    }).setOrigin(0.5));
    this.input.on('wheel', (_p: unknown, _o: unknown, _dx: number, dy: number) => this.irA(this.desplazamiento + dy * 0.6));
    let arrastre: { y: number; d: number } | null = null;
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { arrastre = { y: p.y, d: this.desplazamiento }; });
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => { if (arrastre && p.isDown) this.irA(arrastre.d - (p.y - arrastre.y)); });
    this.input.on('pointerup', () => { arrastre = null; });
    const kb = this.input.keyboard!;
    kb.on('keydown-UP', () => this.irA(this.desplazamiento - 40));
    kb.on('keydown-W', () => this.irA(this.desplazamiento - 40));
    kb.on('keydown-DOWN', () => this.irA(this.desplazamiento + 40));
    kb.on('keydown-S', () => this.irA(this.desplazamiento + 40));
    kb.on('keydown-PAGE_UP', () => this.irA(this.desplazamiento - LISTA.h));
    kb.on('keydown-PAGE_DOWN', () => this.irA(this.desplazamiento + LISTA.h));
    this.time.delayedCall(250, () => {
      kb.on('keydown-L', () => this.cerrar());
      kb.on('keydown-ESC', () => this.cerrar());
    });
  }

  private cerrar() { this.salir('cerrado', 150); }

  private salir(resultado: string, fundido: number) {
    this.tweens.add({ targets: [this.camLista, this.camSobre], alpha: 0, duration: fundido });
    this.terminar({ resultado }, fundido);
  }

  // ------------------------------------------------------------------ doblepensar
  private async doblepensar(c: DpConfig) {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    this.estatica(true);
    const afectadas = this.filas.filter((f) => registro.afectadas(c.lineas, c.alias).includes(f.entrada));
    await espera(700);

    // el registro se desplaza solo hasta la primera línea afectada
    if (afectadas.length) {
      const destino = Phaser.Math.Clamp(afectadas[0].y - 40, 0, this.maxDesplazamiento());
      await new Promise<void>((ok) => this.tweens.addCounter({
        from: this.desplazamiento, to: destino, duration: 1600, ease: 'Sine.easeInOut',
        onUpdate: (t) => this.irA(t.getValue() ?? destino), onComplete: () => ok(),
      }));
    }
    await espera(500);

    // las letras tiemblan, se deshacen y se recomponen como "—"
    const visibles = afectadas.filter((f) => f.y - this.desplazamiento < LISTA.h + 40);
    await this.deshacer(visibles, c.alias);
    this.estatica(false);
    await espera(700);

    // la telepantalla, en voz baja
    const { width } = this.scale;
    const tele = this.fuera(this.add.text(width / 2, 462, '', {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.tele5), align: 'center', wordWrap: { width: 820 },
    }).setOrigin(0.5));
    for (let i = 1; i <= c.telepantalla.length; i++) {
      tele.setText(c.telepantalla.slice(0, i));
      await espera(32);
    }
    await espera(900);

    const decision = await this.elegir(c);
    tele.destroy();
    registro.doblepensar(c.lineas, c.alias, decision);
    if (decision === 'recordar') {
      audio.play('plumilla');
      for (const f of afectadas) {
        f.hablante.setText(this.etiqueta(f.entrada));
        f.texto.setText(this.formato(f.entrada, this.textoTachado(f.entrada)));
        f.tachon.setVisible(registro.nombra(f.entrada, c.alias)).setSize(f.hablante.width + 4, 2).setScale(0, 1);
        this.tweens.add({ targets: f.tachon, scaleX: 1, duration: 260 });
        await espera(90);
      }
    } else {
      audio.play('tubo');
    }
    await espera(1500);
    this.salir(decision, 600);
  }

  /** Estática y bordes oscuros mientras dura el doblepensar. */
  private estatica(activa: boolean) {
    if (!activa) { this.ruido?.destroy(); this.ruido = null; return; }
    const { width, height } = this.scale;
    this.ruido = this.fuera(this.add.graphics().setDepth(10));
    const g = this.ruido;
    const dibujar = () => {
      if (!this.ruido) return;
      g.clear();
      for (let i = 0; i < 260; i++) {
        const borde = Math.random();
        const x = Math.random() * width;
        const y = Math.random() * height;
        const lejos = Math.min(x, width - x, y, height - y);
        if (lejos > 70 + borde * 60) continue;
        g.fillStyle(Math.random() < 0.5 ? 0xffffff : 0x000000, 0.12 + Math.random() * 0.25).fillRect(x, y, 2 + Math.random() * 6, 2);
      }
      this.time.delayedCall(70, dibujar);
    };
    dibujar();
  }

  private async deshacer(filas: Fila[], alias: Alias) {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    const re = new RegExp(`\\b(${alias.join('|')})\\b`, 'gi');
    const esNombre = (t: string) => new RegExp(`\\b(${alias.join('|')})\\b`, 'i').test(t);
    const ruido = (s: string) => [...s].map((ch) => (ch === ' ' ? ' ' : RUIDO[Math.floor(Math.random() * RUIDO.length)])).join('');
    for (let paso = 0; paso < 18; paso++) {
      for (const f of filas) {
        const nombre = this.etiqueta(f.entrada);
        f.hablante.setText(paso % 3 === 2 || !esNombre(nombre) ? nombre : ruido(nombre)).setX(LISTA.x + 10 + Phaser.Math.Between(-2, 2));
        f.hablante.setAlpha(0.5 + Math.random() * 0.5);
        f.texto.setText(this.formato(f.entrada, f.entrada.texto.replace(re, (m) => ruido(m))));
      }
      if (paso % 2 === 0) audio.play(paso % 4 === 0 ? 'grieta' : 'tecla');
      await espera(70);
    }
    for (const f of filas) {
      f.hablante.setText(esNombre(f.entrada.hablante) ? BORRADO : this.etiqueta(f.entrada)).setX(LISTA.x + 10).setAlpha(1);
      f.texto.setText(this.formato(f.entrada, f.entrada.texto.replace(re, BORRADO)));
    }
  }

  private elegir(c: DpConfig): Promise<'aceptar' | 'recordar'> {
    return new Promise((ok) => {
      const { width } = this.scale;
      const capa = this.fuera(this.add.container(0, 0).setDepth(20));
      capa.add(this.add.rectangle(LISTA.x - 14, 190, LISTA.w + 28, 140, 0x000000, 0.82).setOrigin(0));
      const opciones: ['aceptar' | 'recordar', string][] = [['aceptar', c.aceptar], ['recordar', c.recordar]];
      let elegido = false;
      const fin = (d: 'aceptar' | 'recordar') => {
        if (elegido) return;
        elegido = true;
        capa.destroy();
        ok(d);
      };
      opciones.forEach(([d, texto], i) => {
        const y = 232 + i * 54;
        const fondo = this.add.rectangle(width / 2, y, 640, 42, COLOR.gris2, 0.97).setStrokeStyle(2, COLOR.rojo3)
          .setInteractive({ useHandCursor: true });
        const t = this.add.text(width / 2, y, `${i + 1}. ${texto}`, { fontFamily: FUENTE.texto, fontSize: '21px', color: hex(COLOR.papel4) }).setOrigin(0.5);
        fondo.on('pointerover', () => fondo.setFillStyle(COLOR.rojo3));
        fondo.on('pointerout', () => fondo.setFillStyle(COLOR.gris2));
        fondo.on('pointerup', () => fin(d));
        capa.add([fondo, t]);
      });
      capa.setAlpha(0);
      this.tweens.add({ targets: capa, alpha: 1, duration: 400 });
      this.input.keyboard?.on('keydown', (e: KeyboardEvent) => {
        if (e.key === '1') fin('aceptar');
        if (e.key === '2') fin('recordar');
      });
    });
  }
}
