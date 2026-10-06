/**
 * Visor de documentos (diseño técnico §6.3): un papel a pantalla completa, mecanografiado.
 * La Planilla Azul, el expediente de Ivy, la lista de prisioneros, las notas sin firma…
 *   # documento:planilla_s18   → content/documentos/planilla_s18.json
 * Las líneas admiten {variables} de ink y condiciones; «resaltar» marca líneas una a una, como con un
 * dedo que baja por el papel; «foto» pega una fotografía (que puede aparecer tachada).
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { lineas, se_cumple, type Linea } from '../../core/texto';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

export interface Documento {
  papel?: 'blanco' | 'azul' | 'amarillo' | 'gris';
  cabecera?: Linea[];
  lineas: Linea[];
  pie?: Linea[];
  /** Índices (en «lineas», tras filtrar) que se marcan uno a uno. */
  resaltar?: number[];
  foto?: { clave: string; tachada_si?: string; pie?: string };
  sello?: string;
  /** Tamaño de letra (por defecto se ajusta para que quepa). */
  letra?: number;
  /** Texto a mano, en lápiz (notas). */
  manuscrito?: boolean;
}

const DOCS = import.meta.glob('../../../content/documentos/*.json', { eager: true, import: 'default' }) as Record<string, Documento>;
const docDe = (id: string) => Object.entries(DOCS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];

const PAPEL = { blanco: 0xeeead9, azul: 0xc9d6e3, amarillo: 0xd9c590, gris: 0xd0d0cc } as const;
const TINTA = { blanco: 0x22252a, azul: 0x1d2a44, amarillo: 0x3d2c16, gris: 0x22252a } as const;
const HOJA = { w: 860, h: 470 };

export class DocumentoScene extends Minijuego {
  private listo = false;

  constructor() { super('Documento'); }

  create() {
    const { width, height } = this.scale;
    this.listo = false;
    const doc = docDe(this.params.id ?? '');
    if (!doc) { console.warn(`[documento] no existe ${this.params.id}`); this.time.delayedCall(0, () => this.terminar({ resultado: 'visto' }, 0)); return; }
    const papel = doc.papel ?? 'blanco';
    this.cameras.main.fadeIn(350, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0b0c0f, 0.96).setOrigin(0).setDepth(-20);
    const x0 = (width - HOJA.w) / 2, y0 = 22;
    // el papel, con una sombra y un borde algo gastado
    this.add.rectangle(x0 + 6, y0 + 6, HOJA.w, HOJA.h, 0x000000, 0.5).setOrigin(0).setDepth(-19);
    this.add.rectangle(x0, y0, HOJA.w, HOJA.h, PAPEL[papel]).setOrigin(0).setStrokeStyle(1, 0x8f8a7a).setDepth(-18);
    const rnd = new Phaser.Math.RandomDataGenerator([this.params.id ?? 'doc']);
    for (let i = 0; i < 14; i++) {
      this.add.circle(x0 + rnd.between(10, HOJA.w - 10), y0 + rnd.between(10, HOJA.h - 10), rnd.between(2, 9), 0x8f7a50, rnd.realInRange(0.04, 0.1)).setDepth(-17);
    }

    const cab = lineas(doc.cabecera), cuerpo = lineas(doc.lineas), pie = lineas(doc.pie);
    const total = cab.length + cuerpo.length + pie.length + (cab.length ? 1 : 0) + (pie.length ? 1 : 0);
    const anchoFoto = doc.foto ? 250 : 0;
    const maxCar = Math.max(...[...cab, ...cuerpo, ...pie].map((l) => l.length), 10);
    const letra = doc.letra ?? Math.min(24, Math.floor((HOJA.h - 40) / (total * 1.25)), Math.floor((HOJA.w - 60 - anchoFoto) / (maxCar * 0.5)));
    const alto = Math.round(letra * 1.25);
    const fuente = doc.manuscrito ? FUENTE.texto : FUENTE.maquina;
    const tinta = hex(doc.manuscrito ? 0x4a4a52 : TINTA[papel]);
    const est = (extra: Phaser.Types.GameObjects.Text.TextStyle = {}) => ({ fontFamily: fuente, fontSize: `${letra}px`, color: tinta, ...extra });

    let y = y0 + 22;
    for (const l of cab) { this.add.text(x0 + 30, y, l, est()); y += alto; }
    if (cab.length) {
      this.add.rectangle(x0 + 30, y + alto * 0.3, HOJA.w - 60, 2, COLOR.rojo3).setOrigin(0);
      y += alto;
    }
    const filas = cuerpo.map((l) => {
      const t = this.add.text(x0 + 30, y, l, est());
      y += alto;
      return t;
    });
    if (pie.length) y += alto * 0.5;
    for (const l of pie) { this.add.text(x0 + 30, y, l, est({ fontStyle: 'italic' })); y += alto; }

    if (doc.foto) this.foto(doc.foto, x0 + HOJA.w - 30 - 220, y0 + HOJA.h - 30 - 160);
    if (doc.sello) {
      const s = this.add.text(x0 + HOJA.w - 60, y0 + 40, doc.sello, {
        fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.rojo4), padding: { x: 8, y: 2 },
      }).setOrigin(1, 0).setAngle(-8).setAlpha(0.75);
      this.add.rectangle(s.x - s.width / 2, s.y + s.height / 2, s.width + 4, s.height, 0, 0).setStrokeStyle(3, COLOR.rojo4, 0.7).setAngle(-8);
    }

    void this.resaltar(filas, doc.resaltar ?? [], alto).then(() => {
      this.listo = true;
      const aviso = this.add.text(width / 2, height - 22, '[ toca para continuar ]', {
        fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel3),
      }).setOrigin(0.5);
      this.tweens.add({ targets: aviso, alpha: 0.3, duration: 600, yoyo: true, repeat: -1 });
    });
    const cerrar = () => { if (this.listo) this.terminar({ resultado: 'visto' }, 400); };
    this.input.on('pointerup', cerrar);
    this.input.keyboard?.on('keydown', cerrar);
  }

  /** La foto pegada al papel: con su borde blanco y, si toca, tachada a lápiz rojo. */
  private foto(f: NonNullable<Documento['foto']>, x: number, y: number) {
    if (!this.textures.exists(f.clave)) return;
    const img = this.add.image(x, y, f.clave).setOrigin(0).setAngle(2);
    img.setScale(Math.min(220 / img.width, 160 / img.height));
    if (f.pie) this.add.text(x, y + img.displayHeight + 6, f.pie, { fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.gris3) });
    if (f.tachada_si && se_cumple(f.tachada_si)) {
      const g = this.add.graphics().lineStyle(5, COLOR.rojo4, 0.85);
      g.lineBetween(x, y, x + img.displayWidth, y + img.displayHeight).lineBetween(x + img.displayWidth, y, x, y + img.displayHeight);
    }
  }

  private async resaltar(filas: Phaser.GameObjects.Text[], indices: number[], alto: number) {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    if (!indices.length) return espera(700);
    await espera(1100);
    for (const i of indices) {
      const t = filas[i];
      if (!t) continue;
      const marca = this.add.rectangle(t.x - 4, t.y + alto / 2 - 2, t.width + 8, alto, 0xf4dc94, 0.55).setOrigin(0, 0.5).setScale(0, 1).setDepth(-1);
      this.tweens.add({ targets: marca, scaleX: 1, duration: 500 });
      audio.play('plumilla');
      await espera(1100);
    }
  }
}
