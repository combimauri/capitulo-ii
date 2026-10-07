/**
 * Apuntes: el cuaderno del protagonista (tecla N o botón NOTAS). Arriba, lo que hay que hacer ahora;
 * debajo, la gente que conoce y lo que ha averiguado. El contenido está en content/apuntes.json.
 */
import Phaser from 'phaser';
import { Minijuego } from './minijuegos/Minijuego';
import { narrativa } from '../core/juego';
import { objetivo, personas, pistas, type Apuntes } from '../core/apuntes';
import { interpolar } from '../core/texto';
import { COLOR, FUENTE, hex } from '../ui/estilo';
import datos from '../../content/apuntes.json';

const APUNTES = datos as Apuntes;
const LISTA = { x: 70, y: 74, w: 820, h: 372 };

/** Lo que hay que hacer ahora (también lo enseña la pausa). */
export const objetivoActual = () => interpolar(objetivo(APUNTES, (v) => narrativa.get(v)));

export class ApuntesScene extends Minijuego {
  private contenido!: Phaser.GameObjects.Container;
  private camLista!: Phaser.Cameras.Scene2D.Camera;
  private alto = 0;
  private desplazamiento = 0;

  constructor() { super('Apuntes'); }

  create() {
    this.desplazamiento = 0;
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(200, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, COLOR.negro, 0.94).setOrigin(0).setInteractive();
    this.add.rectangle(LISTA.x - 14, LISTA.y - 14, LISTA.w + 28, LISTA.h + 28, COLOR.papel3).setOrigin(0).setStrokeStyle(2, COLOR.gris3);
    this.add.text(width / 2, 30, 'APUNTES', { fontFamily: FUENTE.maquina, fontSize: '32px', color: hex(COLOR.papel4) }).setOrigin(0.5);

    this.contenido = this.add.container(0, 0);
    this.maquetar();
    // el listado se ve a través de su propia cámara: recorta sin máscaras y se desplaza con scrollY
    this.camLista = this.cameras.add(LISTA.x, LISTA.y, LISTA.w, LISTA.h).setScroll(LISTA.x, LISTA.y);
    this.cameras.main.ignore(this.contenido);
    this.children.list.forEach((o) => { if (o !== this.contenido) this.camLista.ignore(o); });

    const cerrar = this.add.text(width - 70, 30, 'CERRAR ✕', { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel3) })
      .setOrigin(0.5).setInteractive({ useHandCursor: true });
    cerrar.on('pointerup', () => this.cerrar());
    const ayuda = this.add.text(width / 2, 492, this.sys.game.device.os.desktop ? 'Rueda o flechas para desplazar · N o Esc para cerrar' : 'Desliza para desplazar', {
      fontFamily: FUENTE.texto, fontSize: '16px', color: '#8f8a7a',
    }).setOrigin(0.5);
    this.camLista.ignore([cerrar, ayuda]);

    this.input.on('wheel', (_p: unknown, _o: unknown, _dx: number, dy: number) => this.irA(this.desplazamiento + dy * 0.6));
    let arrastre: { y: number; d: number } | null = null;
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { arrastre = { y: p.y, d: this.desplazamiento }; });
    this.input.on('pointermove', (p: Phaser.Input.Pointer) => { if (arrastre && p.isDown) this.irA(arrastre.d - (p.y - arrastre.y)); });
    this.input.on('pointerup', () => { arrastre = null; });
    const kb = this.input.keyboard!;
    for (const [tecla, d] of [['UP', -40], ['W', -40], ['DOWN', 40], ['S', 40], ['PAGE_UP', -LISTA.h], ['PAGE_DOWN', LISTA.h]] as const) {
      kb.on(`keydown-${tecla}`, () => this.irA(this.desplazamiento + d));
    }
    this.time.delayedCall(150, () => {
      kb.on('keydown-N', () => this.cerrar());
      kb.on('keydown-ESC', () => this.cerrar());
    });
  }

  private maquetar() {
    const leer = (v: string) => narrativa.get(v);
    const x = LISTA.x + 24, ancho = LISTA.w - 48;
    let y = LISTA.y + 18;
    const titulo = (t: string) => {
      this.contenido.add(this.add.text(x, y, t, { fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.rojo3) }));
      this.contenido.add(this.add.rectangle(x, y + 30, ancho, 2, COLOR.rojo3).setOrigin(0));
      y += 44;
    };
    const parrafo = (t: string, cabeza?: string) => {
      if (cabeza) {
        this.contenido.add(this.add.text(x, y, cabeza, { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.gris2), fontStyle: 'bold' }));
        y += 26;
      }
      const txt = this.add.text(x + (cabeza ? 14 : 0), y, interpolar(t), {
        fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.gris3), lineSpacing: 4, wordWrap: { width: ancho - (cabeza ? 14 : 0), useAdvancedWrap: true },
      });
      this.contenido.add(txt);
      y += txt.height + 16;
    };

    titulo('AHORA');
    const ahora = this.add.text(x, y, interpolar(objetivo(APUNTES, leer)) || '—', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.gris1), lineSpacing: 5, wordWrap: { width: ancho, useAdvancedWrap: true },
    });
    this.contenido.add(ahora);
    y += ahora.height + 26;

    const gente = personas(APUNTES, leer);
    if (gente.length) {
      titulo('PERSONAS');
      for (const p of gente) parrafo(p.texto, interpolar(p.nombre));
      y += 8;
    }
    const sabido = pistas(APUNTES, leer);
    if (sabido.length) {
      titulo('LO QUE SÉ');
      for (const p of sabido) parrafo(p.texto, interpolar(p.titulo));
    }
    this.alto = y - LISTA.y;
  }

  private maxDesplazamiento() { return Math.max(0, this.alto - LISTA.h + 6); }

  private irA(d: number) {
    this.desplazamiento = Phaser.Math.Clamp(d, 0, this.maxDesplazamiento());
    this.camLista.setScroll(LISTA.x, LISTA.y + this.desplazamiento);
  }

  private cerrar() { this.terminar({ resultado: 'cerrado' }, 150); }
}
