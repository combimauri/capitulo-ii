/**
 * Minijuego de documentos (diseño técnico §6.3): un parte de guerra con huecos.
 * El contenido viene de content/documentos/<documento>.json.
 */
import Phaser from 'phaser';
import { Minijuego, type Datos } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

interface LineaDoc { antes: string; hueco?: string; despues?: string; opciones?: string[]; tibias?: string[] }
interface Documento { directiva: string[]; titulo: string; lineas: LineaDoc[]; pensamiento_tibio?: string }

const DOCS = import.meta.glob('../../../content/documentos/*.json', { eager: true, import: 'default' }) as Record<string, Documento>;
const documento = (id: string) => Object.entries(DOCS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];

const PAPEL = { x: 150, y: 170, w: 660, h: 320 };
const ESTILO = { fontFamily: FUENTE.maquina, fontSize: '25px', color: hex(COLOR.gris2) };

export class ParteScene extends Minijuego {
  private doc!: Documento;
  private elegidas: Record<string, string> = {};
  private capa!: Phaser.GameObjects.Container;
  private chips: Phaser.GameObjects.Container | null = null;
  private enviar!: Phaser.GameObjects.Container;
  private pensamiento!: Phaser.GameObjects.Text;

  constructor() { super('Parte'); }

  preload() {
    this.load.image('parte-fondo', 'assets/minijuegos/parte-fondo.png');
    this.load.image('parte-directiva', 'assets/minijuegos/parte-directiva.png');
  }

  create() {
    this.doc = documento(this.params.documento ?? '')!;
    this.elegidas = {};
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(300, 11, 12, 15);

    // escritorio metálico del Minipax, con el parte impreso encima (membrete, filete rojo y pie): parte-fondo
    this.add.image(0, 0, 'parte-fondo').setOrigin(0).setScale(2);

    // directiva del tubo neumático
    const tubo = this.add.container(40, 24);
    tubo.add(this.add.image(0, 0, 'parte-directiva').setOrigin(0).setScale(2));
    tubo.add(this.add.text(12, 10, 'DIRECTIVA · TUBO 14', { fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.rojo3) }));
    tubo.add(this.add.text(12, 34, this.doc.directiva.join('\n'), { fontFamily: FUENTE.maquina, fontSize: '19px', color: hex(COLOR.gris2), lineSpacing: 1 }));
    tubo.setAngle(-2).setAlpha(0);
    this.tweens.add({ targets: tubo, alpha: 1, y: 30, duration: 400 });
    audio.play('tubo');

    // papel del parte (dibujado en parte-fondo)
    this.add.text(PAPEL.x + PAPEL.w / 2, PAPEL.y + 22, this.doc.titulo, {
      fontFamily: FUENTE.maquina, fontSize: '28px', color: hex(COLOR.gris2),
    }).setOrigin(0.5, 0);
    this.capa = this.add.container(0, 0);

    this.pensamiento = this.add.text(width / 2, height - 22, '', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), stroke: '#000', strokeThickness: 4,
    }).setOrigin(0.5);

    this.enviar = this.add.container(width - 150, 115);
    const fondo = this.add.rectangle(0, 0, 230, 46, COLOR.gris2).setStrokeStyle(2, COLOR.gris3);
    this.enviar.add([fondo, this.add.text(0, 0, 'ENVIAR POR EL TUBO', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5)]);
    fondo.setInteractive({ useHandCursor: true }).on('pointerup', () => this.intentarEnviar());
    this.time.delayedCall(400, () => this.input.keyboard?.on('keydown-ENTER', () => this.intentarEnviar()));

    this.maquetar();
  }

  private huecos() { return this.doc.lineas.filter((l) => l.hueco); }
  private completo() { return this.huecos().every((l) => this.elegidas[l.hueco!]); }

  /** Coloca palabras y huecos en el papel con ajuste de línea. */
  private maquetar() {
    this.capa.removeAll(true);
    const izq = PAPEL.x + 34, der = PAPEL.x + PAPEL.w - 34;
    let x = izq, y = PAPEL.y + 78;
    const salto = 34, espacio = 9;
    const colocar = (w: number) => { if (x + w > der && x > izq) { x = izq; y += salto; } const px = x; x += w + espacio; return px; };

    for (const linea of this.doc.lineas) {
      for (const palabra of linea.antes.split(' ')) {
        const t = this.add.text(0, y, palabra, ESTILO);
        t.setX(colocar(t.width)).setY(y);
        this.capa.add(t);
      }
      if (linea.hueco) {
        const ancho = Math.max(...linea.opciones!.map((o) => this.add.text(0, 0, o, ESTILO).setVisible(false).width)) + 20;
        const gx = colocar(ancho), gy = y;
        const valor = this.elegidas[linea.hueco];
        const caja = this.add.rectangle(gx, gy - 2, ancho, 30, valor ? COLOR.papel4 : 0xb5af9c).setOrigin(0)
          .setStrokeStyle(1, valor ? COLOR.gris3 : COLOR.rojo3).setInteractive({ useHandCursor: true });
        const t = this.add.text(gx + ancho / 2, gy + 13, valor ?? '______', { ...ESTILO, color: hex(valor ? COLOR.gris2 : COLOR.rojo3) }).setOrigin(0.5);
        caja.on('pointerup', () => this.abrirOpciones(linea, gx, gy, ancho));
        this.capa.add([caja, t]);
      }
      for (const palabra of (linea.despues ?? '').split(' ').filter(Boolean)) {
        const t = this.add.text(0, y, palabra, ESTILO);
        t.setX(palabra === '.' || palabra === ',' ? x - espacio - 2 : colocar(t.width)).setY(y);
        if (palabra === '.' || palabra === ',') x += t.width;
        this.capa.add(t);
      }
      x = izq; y += salto + 8;   // cada línea del documento empieza en una línea nueva
    }
    this.enviar.setAlpha(this.completo() ? 1 : 0.4);
  }

  private abrirOpciones(linea: LineaDoc, gx: number, gy: number, ancho: number) {
    this.chips?.destroy();
    const c = this.add.container(0, 0).setDepth(10);
    const opciones = linea.opciones!;
    const w = 210, h = 38;
    const total = opciones.length * (w + 8) - 8;
    let x0 = Phaser.Math.Clamp(gx + ancho / 2 - total / 2, 20, this.scale.width - total - 20);
    const y0 = gy + 40 + h / 2 > PAPEL.y + PAPEL.h ? gy - 30 : gy + 40;
    opciones.forEach((o) => {
      const fondo = this.add.rectangle(x0 + w / 2, y0, w, h, COLOR.gris2).setStrokeStyle(2, COLOR.rojo3)
        .setInteractive({ useHandCursor: true });
      const t = this.add.text(x0 + w / 2, y0, o, { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      fondo.on('pointerover', () => fondo.setFillStyle(COLOR.rojo3));
      fondo.on('pointerout', () => fondo.setFillStyle(COLOR.gris2));
      fondo.on('pointerup', () => {
        this.elegidas[linea.hueco!] = o;
        audio.play('tecla');
        this.time.delayedCall(70, () => audio.play('tecla'));
        if (linea.tibias?.includes(o) && this.doc.pensamiento_tibio) this.pensar(this.doc.pensamiento_tibio);
        this.chips?.destroy(); this.chips = null;
        this.maquetar();
      });
      c.add([fondo, t]);
      x0 += w + 8;
    });
    this.chips = c;
  }

  private pensar(texto: string) {
    this.pensamiento.setText(texto).setAlpha(1);
    this.tweens.killTweensOf(this.pensamiento);
    this.tweens.add({ targets: this.pensamiento, alpha: 0, delay: 2600, duration: 600 });
  }

  private intentarEnviar() {
    if (!this.completo()) { this.pensar('Faltan cifras. Un parte incompleto es un parte desleal.'); return; }
    let tibias = 0;
    const datos: Datos = {};
    for (const l of this.huecos()) {
      const v = this.elegidas[l.hueco!];
      datos[l.hueco!] = v;
      if (l.tibias?.includes(v)) tibias++;
    }
    datos.tibias = tibias;
    audio.play('tubo');
    this.tweens.add({ targets: this.children.list.filter((o) => o !== this.pensamiento), y: '-=40', alpha: 0, duration: 500 });
    this.time.delayedCall(450, () => this.terminar({ resultado: 'enviado', datos }));
  }
}
