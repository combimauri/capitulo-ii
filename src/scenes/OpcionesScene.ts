/**
 * Opciones (diseño técnico §9), desde el menú principal o desde la pausa:
 *   SONIDO   los cuatro volúmenes (mientras está abierto desde el menú, suena algo para oírlos).
 *   JUEGO    velocidad del texto, crimen facial, sigilo, destellos, tamaño de la interfaz y mano dominante.
 *   PARTIDA  exportar la partida a un archivo e importarla (diseño técnico §10.2).
 */
import Phaser from 'phaser';
import { audio, type Canal } from '../systems/AudioDirector';
import { opciones, fijarOpcion, VALORES, type OpcionesJuego } from '../core/Opciones';
import { SaveSystem } from '../core/SaveSystem';
import { LOCALIZACIONES, narrativa, EV } from '../core/juego';
import { COLOR, FUENTE, hex } from '../ui/estilo';

type Pestana = 'sonido' | 'juego' | 'partida';

export interface EntradaOpciones { desde: 'menu' | 'pausa'; alCerrar?: () => void }

const ETIQUETAS: { [K in keyof OpcionesJuego]: { nombre: string; valores: string[]; ayuda: string[] } } = {
  texto: {
    nombre: 'Velocidad del texto', valores: ['Lenta', 'Normal', 'Rápida', 'Instantánea'],
    ayuda: ['El texto aparece despacio.', 'El texto aparece a ritmo de lectura.', 'El texto aparece deprisa.', 'Cada línea aparece entera de golpe.'],
  },
  cf: {
    nombre: 'Crimen facial', valores: ['Normal', 'Asistida', 'Automática'],
    ayuda: ['Hay que acertar cada expresión a tiempo.', 'Ritmo más lento y márgenes más amplios para acertar.',
      'Modo historia: la cara se compone sola. Las pancartas y las miradas siguen en tus manos.'],
  },
  sigilo: {
    nombre: 'Penalización de sigilo', valores: ['Normal', 'Reducida'],
    ayuda: ['Si te ven en una misión, la Sospecha sube lo que marca el guion.', 'Si te ven en una misión, la Sospecha sube la mitad.'],
  },
  destellos: {
    nombre: 'Reducir destellos', valores: ['No', 'Sí'],
    ayuda: ['Destellos, parpadeos y temblores de pantalla completos.', 'Sin destellos claros ni parpadeos rápidos; los temblores, apenas un roce.'],
  },
  ui: {
    nombre: 'Tamaño del texto', valores: ['100 %', '125 %'],
    ayuda: ['Diálogos, pensamientos y opciones a su tamaño normal.', 'Diálogos, pensamientos y opciones más grandes, en cajas más altas.'],
  },
  mano: {
    nombre: 'Mano dominante', valores: ['Derecha', 'Izquierda'],
    ayuda: ['En pantallas táctiles, los botones de acción van a la derecha.', 'En pantallas táctiles, los botones de acción van a la izquierda.'],
  },
};

/** El nombre del protagonista dentro del estado de ink guardado (las cadenas van con «^» delante). */
function nombreGuardado(ink: string): string {
  try { return String((JSON.parse(ink) as { variablesState?: Record<string, unknown> }).variablesState?.nombre ?? '').replace(/^\^/, ''); } catch { return ''; }
}

export class OpcionesScene extends Phaser.Scene {
  private desde: EntradaOpciones['desde'] = 'menu';
  private alCerrar: (() => void) | undefined;
  private pestana: Pestana = 'sonido';
  private contenido!: Phaser.GameObjects.Container;
  private pestanas: { id: Pestana; fondo: Phaser.GameObjects.Rectangle }[] = [];
  private ayuda!: Phaser.GameObjects.Text;

  constructor() { super('Opciones'); }

  init(d: EntradaOpciones) {
    this.desde = d?.desde ?? 'menu';
    this.alCerrar = d?.alCerrar;
  }

  create() {
    const { width, height } = this.scale;
    this.add.rectangle(0, 0, width, height, 0x0b0c0f, 1).setOrigin(0).setInteractive();
    this.add.text(width / 2, 46, 'OPCIONES', { fontFamily: FUENTE.maquina, fontSize: '36px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    // desde el menú sigue sonando su música; el ambiente de la calle, para oír su volumen
    if (this.desde === 'menu') audio.ambiente.poner(['calle']);

    this.pestanas = [];
    const PESTANAS: [Pestana, string][] = [['sonido', 'SONIDO'], ['juego', 'JUEGO'], ['partida', 'PARTIDA']];
    PESTANAS.forEach(([id, texto], i) => {
      const x = width / 2 + (i - 1) * 170;
      const fondo = this.add.rectangle(x, 104, 160, 38, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
      this.add.text(x, 104, texto, { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      fondo.on('pointerup', () => this.mostrar(id));
      this.pestanas.push({ id, fondo });
    });
    this.contenido = this.add.container(0, 0);
    this.ayuda = this.add.text(width / 2, 438, '', {
      fontFamily: FUENTE.texto, fontSize: '17px', color: '#8f8a7a', align: 'center', wordWrap: { width: 760 },
    }).setOrigin(0.5);

    const cerrar = this.add.rectangle(width / 2, height - 40, 180, 40, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(width / 2, height - 40, 'cerrar', { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3) }).setOrigin(0.5);
    cerrar.on('pointerup', () => this.cerrar());
    this.input.keyboard?.on('keydown-ESC', () => this.cerrar());
    this.mostrar(this.pestana);
  }

  private cerrar() {
    if (this.desde === 'menu') audio.ambiente.poner([]);
    const f = this.alCerrar;
    this.scene.stop();
    f?.();
  }

  private mostrar(p: Pestana) {
    this.pestana = p;
    this.pestanas.forEach((t) => t.fondo.setFillStyle(t.id === p ? COLOR.rojo3 : COLOR.gris2));
    this.contenido.removeAll(true);
    this.input.removeAllListeners('pointermove');
    this.input.removeAllListeners('pointerup');
    this.ayuda.setText('');
    if (p === 'sonido') this.sonido();
    else if (p === 'juego') this.juego();
    else this.partida();
  }

  // ------------------------------------------------------------------ sonido
  private sonido() {
    const { width } = this.scale;
    const CANALES: [Canal, string][] = [['general', 'General'], ['musica', 'Música'], ['efectos', 'Efectos'], ['ambiente', 'Ambiente']];
    const ANCHO = 320, X0 = width / 2 - 60;
    CANALES.forEach(([canal, nombre], i) => {
      const y = 180 + i * 64;
      const etiqueta = this.add.text(X0 - 40, y, nombre, { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(1, 0.5);
      const pista = this.add.rectangle(X0, y, ANCHO, 8, COLOR.gris2).setOrigin(0, 0.5);
      const lleno = this.add.rectangle(X0, y, ANCHO * audio.volumenes[canal], 8, COLOR.rojo3).setOrigin(0, 0.5);
      const asa = this.add.rectangle(X0 + ANCHO * audio.volumenes[canal], y, 16, 30, COLOR.papel4).setStrokeStyle(2, COLOR.gris1);
      const valor = this.add.text(X0 + ANCHO + 24, y, '', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(0, 0.5);
      // zona de toque generosa: toda la fila (44 px de alto como mínimo)
      const zona = this.add.rectangle(X0 - 10, y, ANCHO + 20, 48, 0, 0).setOrigin(0, 0.5).setInteractive({ useHandCursor: true });
      this.contenido.add([etiqueta, pista, lleno, asa, valor, zona]);
      const pintar = () => {
        const v = audio.volumenes[canal];
        lleno.setSize(ANCHO * v, 8); asa.setX(X0 + ANCHO * v); valor.setText(`${Math.round(v * 100)} %`);
      };
      const fijar = (px: number) => { audio.ajustarVolumen(canal, Math.round(((px - X0) / ANCHO) * 20) / 20); pintar(); };
      let arrastrando = false;
      zona.on('pointerdown', (p: Phaser.Input.Pointer) => { audio.desbloquear(); arrastrando = true; fijar(p.x); });
      this.input.on('pointermove', (p: Phaser.Input.Pointer) => { if (arrastrando && p.isDown) fijar(p.x); });
      this.input.on('pointerup', () => {
        if (arrastrando && (canal === 'efectos' || canal === 'general')) audio.play('sello');
        arrastrando = false;
      });
      pintar();
    });
  }

  // ------------------------------------------------------------------ juego y accesibilidad
  private juego() {
    const { width } = this.scale;
    const claves = Object.keys(ETIQUETAS) as (keyof OpcionesJuego)[];
    const X0 = width / 2 - 150, ANCHO = 520;
    claves.forEach((k, i) => {
      const y = 160 + i * 46;
      const e = ETIQUETAS[k];
      this.contenido.add(this.add.text(X0 - 20, y, e.nombre, { fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3) }).setOrigin(1, 0.5));
      const valores = VALORES[k] as readonly OpcionesJuego[typeof k][];
      const w = ANCHO / valores.length;
      const botones: Phaser.GameObjects.Rectangle[] = [];
      const pintar = () => botones.forEach((b, j) => b.setFillStyle(valores[j] === opciones[k] ? COLOR.rojo3 : COLOR.gris2));
      valores.forEach((v, j) => {
        const x = X0 + w * j + w / 2;
        const b = this.add.rectangle(x, y, w - 6, 38, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
        const t = this.add.text(x, y, e.valores[j], { fontFamily: FUENTE.texto, fontSize: '17px', color: hex(COLOR.papel4) }).setOrigin(0.5);
        b.on('pointerover', () => this.ayuda.setText(`${e.nombre}: ${e.ayuda[j]}`));
        b.on('pointerup', () => {
          fijarOpcion(k, v as never);
          pintar();
          this.ayuda.setText(`${e.nombre}: ${e.ayuda[j]}`);
          audio.play('tecla');
        });
        botones.push(b);
        this.contenido.add([b, t]);
      });
      pintar();
    });
  }

  // ------------------------------------------------------------------ partida
  private partida() {
    const { width } = this.scale;
    const hay = !!SaveSystem.cargar('auto');
    const boton = (y: number, texto: string, activo: boolean, accion: () => void) => {
      const f = this.add.rectangle(width / 2, y, 340, 44, COLOR.gris2).setStrokeStyle(1, COLOR.gris3);
      const t = this.add.text(width / 2, y, texto, { fontFamily: FUENTE.texto, fontSize: '21px', color: hex(activo ? COLOR.papel4 : COLOR.gris3) }).setOrigin(0.5);
      if (activo) {
        f.setInteractive({ useHandCursor: true });
        f.on('pointerover', () => f.setFillStyle(COLOR.rojo3));
        f.on('pointerout', () => f.setFillStyle(COLOR.gris2));
        f.on('pointerup', accion);
      }
      this.contenido.add([f, t]);
    };
    this.contenido.add(this.add.text(width / 2, 176, [
      'Guarda una copia de la partida en un archivo,',
      'o carga una para seguir en otro dispositivo.',
    ].join('\n'), { fontFamily: FUENTE.texto, fontSize: '19px', color: hex(COLOR.papel3), align: 'center', lineSpacing: 6 }).setOrigin(0.5));
    boton(262, 'Exportar partida', hay, () => this.exportar());
    // importar en mitad de una partida la abandonaría: solo desde el menú
    if (this.desde === 'menu') boton(320, 'Importar partida', true, () => this.importar());
    if (!hay) this.ayuda.setText('Todavía no hay ninguna partida guardada.');
  }

  private exportar() {
    if (this.desde === 'pausa') this.game.events.emit(EV.guardar);
    const texto = SaveSystem.exportar();
    if (!texto) return;
    const d = SaveSystem.cargar('auto')!;
    const nombre = this.desde === 'pausa' ? String(narrativa.get('nombre') ?? '') : nombreGuardado(d.ink);
    const fecha = new Date().toISOString().slice(0, 10);
    const archivo = `capitulo2-${nombre ? nombre.toLowerCase().normalize('NFD').replace(/[^a-z]/g, '') + '-' : ''}jornada${d.meta?.jornada ?? 1}-${fecha}.json`;
    const url = URL.createObjectURL(new Blob([texto], { type: 'application/json' }));
    const a = document.createElement('a');
    a.href = url; a.download = archivo;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    this.ayuda.setText(`Partida exportada: ${archivo}`);
  }

  private importar() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'application/json,.json';
    input.onchange = () => {
      const f = input.files?.[0];
      if (!f) return;
      void f.text().then((texto) => {
        const d = SaveSystem.leerExportada(texto);
        if (typeof d === 'string') { this.ayuda.setText(d); return; }
        if (!LOCALIZACIONES[d.mundo.escena]) { this.ayuda.setText('La partida es de otra versión del juego.'); return; }
        this.confirmar(SaveSystem.cargar('auto') ? 'Esto sustituye la partida guardada. ¿Seguir?' : '¿Cargar esta partida?', () => {
          if (SaveSystem.importar('auto', d)) { this.ayuda.setText(`Partida importada (jornada ${d.meta?.jornada ?? '?'}). Pulsa «Continuar» en el menú.`); this.mostrar('partida'); }
          else this.ayuda.setText('Este navegador no permite guardar la partida.');
        });
      });
    };
    input.click();
  }

  private confirmar(pregunta: string, si: () => void) {
    const { width, height } = this.scale;
    const capa = this.add.container(0, 0).setDepth(10);
    capa.add(this.add.rectangle(0, 0, width, height, 0x000000, 0.75).setOrigin(0).setInteractive());
    capa.add(this.add.rectangle(width / 2, height / 2, 520, 180, COLOR.gris1).setStrokeStyle(2, COLOR.rojo3));
    capa.add(this.add.text(width / 2, height / 2 - 40, pregunta, { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), align: 'center', wordWrap: { width: 460 } }).setOrigin(0.5));
    ([['Sí', -100, () => { capa.destroy(); si(); }], ['No', 100, () => capa.destroy()]] as const).forEach(([t, dx, f]) => {
      const b = this.add.rectangle(width / 2 + dx, height / 2 + 40, 150, 40, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
      b.on('pointerup', f);
      capa.add([b, this.add.text(width / 2 + dx, height / 2 + 40, t, { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4) }).setOrigin(0.5)]);
    });
  }
}
