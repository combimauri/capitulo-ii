/**
 * El diario (guion J5.08, «Composición de entradas»): se elige una de las entradas desbloqueadas
 * (variable de ink con su id a true) y, dentro de ella, una frase entre dos o tres. La frase se escribe
 * a lápiz y queda guardada para el Capítulo II. El protagonista duda al escribir el año.
 *   # minijuego:diario,fecha=19 de abril
 * Entradas y frases: content/diario/entradas.json ("si" filtra por el estado de ink).
 * Resultado: el texto escrito ("" si no escribe nada). Datos: entrada (id).
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { cumple } from '../../core/Location';
import { COLOR, FUENTE, hex } from '../../ui/estilo';
import datos from '../../../content/diario/entradas.json';

interface Frase { texto: string; si?: string }
interface Entrada { id: string; titulo: string; frases: Frase[] }
const ENTRADAS = (datos as { entradas: Entrada[] }).entradas;

const IZQ = { x: 132, y: 84, w: 330 };
const DER = { x: 500, y: 84, w: 330 };
const GRAFITO = 0x3b3c44;

export class DiarioScene extends Minijuego {
  private izquierda!: Phaser.GameObjects.Container;
  private escrito!: Phaser.GameObjects.Text;
  private escribiendo = false;

  constructor() { super('Diario'); }

  create() {
    const { width, height } = this.scale;
    this.escribiendo = false;
    this.cameras.main.fadeIn(400, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0b0c0f).setOrigin(0);
    // el cuaderno abierto: tapas negras, papel crema de antes de la Revolución
    this.add.rectangle(width / 2, 280, 760, 440, 0x16181c).setStrokeStyle(2, 0x2f3338);
    this.add.rectangle(IZQ.x - 14, 70, 360, 420, 0xe6dcc0).setOrigin(0);
    this.add.rectangle(DER.x - 14, 70, 360, 420, 0xece3c8).setOrigin(0);
    this.add.rectangle(width / 2, 280, 10, 420, 0x000000, 0.25);
    // renglones al paso de la letra (21 px + 7 de interlineado ≈ 27,5)
    for (let y = 112 + 25; y < 470; y += 27.5) this.add.rectangle(DER.x - 4, Math.round(y), 336, 1, 0xb9ae90).setOrigin(0, 0.5);
    // restos de las primeras páginas, arrancadas
    for (let y = 76; y < 484; y += 9) this.add.rectangle(width / 2 - 8, y, 6, 4, 0xd8ccae);
    // el pájaro diminuto de la tapa
    const g = this.add.graphics();
    g.lineStyle(2, GRAFITO).beginPath().moveTo(IZQ.x + 290, 98).lineTo(IZQ.x + 298, 104).lineTo(IZQ.x + 306, 96).strokePath();

    const lapiz = narrativa.list('inventario').includes('lapiz_amory') ? 'con el lápiz de Amory' : 'con un lápiz cualquiera';
    this.add.text(width / 2, 506, lapiz, { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.gris3) }).setOrigin(0.5);
    this.escrito = this.add.text(DER.x, 112, '', {
      fontFamily: FUENTE.texto, fontSize: '21px', color: hex(GRAFITO), lineSpacing: 7, wordWrap: { width: DER.w - 10, useAdvancedWrap: true },
    });
    this.izquierda = this.add.container(0, 0);
    this.mostrarEntradas();
  }

  private disponibles() {
    const leer = (v: string) => narrativa.get(v);
    return ENTRADAS.filter((e) => leer(e.id) === true && leer(`${e.id}_escrita`) !== true);
  }

  private titulo(s: string) {
    this.izquierda.add(this.add.text(IZQ.x, IZQ.y, s, { fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(GRAFITO) }));
  }

  private opcion(y: number, s: string, alPulsar: () => void) {
    const t = this.add.text(IZQ.x, y, s, {
      fontFamily: FUENTE.texto, fontSize: '19px', color: hex(GRAFITO), wordWrap: { width: IZQ.w - 10, useAdvancedWrap: true }, lineSpacing: 4,
    }).setInteractive({ useHandCursor: true });
    t.on('pointerover', () => t.setColor(hex(COLOR.rojo3)));
    t.on('pointerout', () => t.setColor(hex(GRAFITO)));
    t.on('pointerup', () => { if (!this.escribiendo) alPulsar(); });
    this.izquierda.add(t);
    return t.height;
  }

  private mostrarEntradas() {
    this.izquierda.removeAll(true);
    const entradas = this.disponibles();
    this.titulo('¿Qué escribo?');
    let y = IZQ.y + 50;
    entradas.forEach((e, i) => { y += this.opcion(y, `${i + 1}. ${e.titulo}`, () => this.mostrarFrases(e)) + 14; });
    y += 20;
    this.opcion(Math.max(y, 420), 'No escribir nada', () => this.terminar({ resultado: '' }));
  }

  private mostrarFrases(e: Entrada) {
    this.izquierda.removeAll(true);
    this.titulo(e.titulo);
    let y = IZQ.y + 50;
    const leer = (v: string) => narrativa.get(v);
    const interpolar = (t: string) => t.replace(/\{(\w+)\}/g, (_, v) => String(leer(v) ?? ''));
    e.frases.filter((f) => cumple(f.si, leer)).map((f) => interpolar(f.texto))
      .forEach((t) => { y += this.opcion(y, `— ${t}`, () => void this.escribir(e, t)) + 16; });
    this.opcion(440, '‹ Otra cosa', () => this.mostrarEntradas());
  }

  private async escribir(e: Entrada, texto: string) {
    this.escribiendo = true;
    this.izquierda.removeAll(true);
    const espera = (ms: number) => new Promise<void>((ok) => this.time.delayedCall(ms, ok));
    const trazar = async (s: string, base: string) => {
      for (let i = 1; i <= s.length; i++) {
        this.escrito.setText(base + s.slice(0, i));
        if (i % 3 === 0) audio.play('plumilla');
        await espera(s[i - 1] === ' ' ? 30 : 55);
      }
    };
    await trazar(texto, '');
    await espera(600);
    // la fecha: el año se resiste
    const fecha = `\n\n${this.params.fecha ?? ''} de 198`;
    await trazar(fecha, texto);
    await espera(1300);
    await trazar('4', texto + fecha);
    await espera(900);
    this.terminar({ resultado: texto, datos: { entrada: e.id } }, 600);
  }
}
