/**
 * Comparador de documentos (guion J6.03): a la izquierda, en sepia, el recuerdo; a la derecha, el documento.
 * Las diferencias se marcan una a una. Lo que coincide (la firma) es lo peor.
 *   # comparar:documento=comparar_parte_j6   → content/documentos/comparar_parte_j6.json ({variables} de ink)
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

interface Campo { etiqueta: string; recuerdo: string; documento: string }
interface Comparacion { recuerdo: string; documento: string; campos: Campo[] }
const DOCS = import.meta.glob('../../../content/documentos/*.json', { eager: true, import: 'default' }) as Record<string, Comparacion>;
const docDe = (id: string) => Object.entries(DOCS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];
const interpolar = (s: string) => s.replace(/\{(\w+)\}/g, (_, v) => String(narrativa.get(v) ?? ''));

const SEPIA = { fondo: 0xc4ab7e, tinta: 0x5a3d22 };
const IZQ = 60, DER = 500, ANCHO = 400, Y0 = 70;

export class ComparadorScene extends Minijuego {
  private marcas: Phaser.GameObjects.GameObject[] = [];
  private filas: { campo: Campo; derecha: Phaser.GameObjects.Text; y: number }[] = [];

  constructor() { super('Comparar'); }

  create() {
    const doc = docDe(this.params.documento ?? '')!;
    const { width, height } = this.scale;
    this.marcas = []; this.filas = [];
    this.cameras.main.fadeIn(400, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x1a1411).setOrigin(0);
    // el recuerdo: sepia, con los bordes difuminados
    this.add.rectangle(IZQ, Y0, ANCHO, 380, SEPIA.fondo).setOrigin(0).setAlpha(0.92);
    for (let i = 0; i < 6; i++) this.add.rectangle(IZQ - i, Y0 - i, ANCHO + i * 2, 380 + i * 2).setOrigin(0).setStrokeStyle(1, SEPIA.fondo, 0.5 - i * 0.08);
    this.add.text(IZQ + 20, Y0 + 14, doc.recuerdo, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(SEPIA.tinta) });
    // el documento del archivo
    this.add.rectangle(DER, Y0, ANCHO, 380, COLOR.papel4).setOrigin(0).setStrokeStyle(1, 0x8f8a7a);
    this.add.text(DER + 20, Y0 + 14, doc.documento, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.gris2) });
    this.add.rectangle(DER + 20, Y0 + 44, ANCHO - 40, 2, COLOR.rojo3).setOrigin(0);

    doc.campos.forEach((c, i) => {
      const y = Y0 + 64 + i * 44;
      const est = (color: number) => ({ fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(color), wordWrap: { width: ANCHO - 170 } });
      this.add.text(IZQ + 20, y, c.etiqueta.toUpperCase(), est(SEPIA.tinta)).setAlpha(0.8);
      this.add.text(IZQ + 160, y, interpolar(c.recuerdo), est(SEPIA.tinta));
      this.add.text(DER + 20, y, c.etiqueta.toUpperCase(), est(COLOR.gris3));
      const doc_ = interpolar(c.documento);
      const derecha = this.add.text(DER + 160, y, doc_ || '(eliminado)', est(doc_ ? COLOR.gris2 : COLOR.gris3));
      this.filas.push({ campo: c, derecha, y });
    });

    const boton = (x: number, texto: string, alPulsar: () => void) => {
      const f = this.add.rectangle(x, height - 44, 220, 40, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      this.add.text(x, height - 44, texto, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      f.on('pointerup', alPulsar);
    };
    boton(width / 2 - 130, 'LEER OTRA VEZ', () => void this.comparar());
    boton(width / 2 + 130, 'DEJAR EL PARTE', () => this.terminar({ resultado: 'visto' }, 500));
    this.time.delayedCall(700, () => void this.comparar());
  }

  /** Recorre los campos: las diferencias se subrayan en rojo; lo que coincide, en gris. */
  private async comparar() {
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    this.marcas.forEach((m) => m.destroy());
    this.marcas = [];
    for (const f of this.filas) {
      const igual = interpolar(f.campo.recuerdo) === interpolar(f.campo.documento);
      const linea = this.add.rectangle(f.derecha.x, f.y + 24, f.derecha.width, 2, igual ? COLOR.gris3 : COLOR.rojo4).setOrigin(0, 0.5).setScale(0, 1);
      this.tweens.add({ targets: linea, scaleX: 1, duration: 220 });
      this.marcas.push(linea);
      if (!igual) {
        const flecha = this.add.text(DER - 16, f.y, '≠', { fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.rojo4) });
        this.marcas.push(flecha);
      }
      audio.play(igual ? 'sello' : 'tecla');
      await espera(igual ? 900 : 450);
    }
  }
}
