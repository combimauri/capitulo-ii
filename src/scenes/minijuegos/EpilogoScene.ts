/**
 * Epílogo del Final D (guion FD.07): sobre papel claro, sin la paleta del Partido, una nota académica sobre
 * el «Capítulo II». Se desplaza despacio, con «Naranjas y limones» al piano. Habla del régimen en pasado.
 *   # minijuego:epilogo   → content/finales/nota.json ({variables} de ink, «si» filtra por el estado)
 * Y los créditos:  # minijuego:creditos,final=D
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { interpolar, se_cumple } from '../../core/texto';
import { FUENTE } from '../../ui/estilo';
import nota from '../../../content/finales/nota.json';

interface Parrafo { texto: string; si?: string; cita?: boolean }

export class EpilogoScene extends Minijuego {
  private texto!: Phaser.GameObjects.Container;
  private fin = 0;
  private listo = false;

  constructor() { super('Epilogo'); }

  create() {
    const { width, height } = this.scale;
    this.listo = false;
    this.cameras.main.fadeIn(2500, 240, 236, 222);
    this.add.rectangle(0, 0, width, height, 0xf0ecde).setOrigin(0);
    const inicial = String(narrativa.get('nombre') ?? '').charAt(0).toUpperCase();
    this.texto = this.add.container(0, height + 20);
    let y = 0;
    const titulo = this.add.text(width / 2, y, nota.titulo, { fontFamily: FUENTE.libro, fontSize: '26px', color: '#2a2a2a', align: 'center', wordWrap: { width: 700 } }).setOrigin(0.5, 0);
    this.texto.add(titulo);
    y += titulo.height + 36;
    for (const p of nota.parrafos as Parrafo[]) {
      if (!se_cumple(p.si)) continue;
      const t = this.add.text(p.cita ? 200 : 140, y, interpolar(p.texto.replace('{inicial}', `${inicial}.`)), {
        fontFamily: FUENTE.libro, fontSize: p.cita ? '21px' : '20px', color: p.cita ? '#3a3a3a' : '#2a2a2a',
        fontStyle: p.cita ? 'italic' : 'normal', wordWrap: { width: p.cita ? 560 : 680 }, lineSpacing: 7,
      });
      this.texto.add(t);
      y += t.height + 22;
    }
    this.fin = -(y - height / 2);
    // la canción, al piano, muy lenta
    this.time.delayedCall(1500, () => audio.play('naranjas'));
    this.time.addEvent({ delay: 16000, loop: true, callback: () => audio.play('naranjas') });
    this.input.on('pointerup', () => { if (this.listo) this.terminar({ resultado: 'leido' }, 2000); });
    this.input.keyboard?.on('keydown', () => { if (this.listo) this.terminar({ resultado: 'leido' }, 2000); });
  }

  update(_t: number, dt: number) {
    if (this.texto.y > this.fin) this.texto.y -= dt * 0.024;
    else if (!this.listo) {
      this.listo = true;
      const a = this.add.text(480, 520, '[ toca para continuar ]', { fontFamily: FUENTE.maquina, fontSize: '20px', color: '#8a8a80' }).setOrigin(0.5, 1);
      this.tweens.add({ targets: a, alpha: 0.3, duration: 700, yoyo: true, repeat: -1 });
    }
  }
}

/** Créditos: sobre negro, despacio. Con la máquina de escribir de fondo en el Final E. */
export class CreditosScene extends Minijuego {
  private lista!: Phaser.GameObjects.Text;

  constructor() { super('Creditos'); }

  create() {
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(1500, 0, 0, 0);
    this.add.rectangle(0, 0, width, height, 0x000000).setOrigin(0);
    const lineas = [
      'CAPÍTULO II', '', '', 'Basado libremente en', '1984, de George Orwell', '', '',
      'Guion, código, arte y sonido', 'hechos a mano, línea a línea', '', '',
      'Phaser · ink · TypeScript · Python', '', '', '',
      'A todos los que corrigieron un documento', 'sabiendo que mentían.', '', '',
      'Y a los que no.',
    ];
    this.lista = this.add.text(width / 2, height + 20, lineas.join('\n'), {
      fontFamily: FUENTE.maquina, fontSize: '28px', color: '#d8d2bd', align: 'center', lineSpacing: 8,
    }).setOrigin(0.5, 0);
    if (this.params.final === 'E') this.time.addEvent({ delay: 180, loop: true, callback: () => { if (Math.random() < 0.6) audio.play('tecla'); } });
    else this.time.delayedCall(800, () => audio.play('naranjas'));
    this.input.on('pointerup', () => this.terminar({ resultado: 'fin' }, 1500));
  }

  update(_t: number, dt: number) {
    this.lista.y -= dt * 0.04;
    if (this.lista.y + this.lista.height < -20) this.terminar({ resultado: 'fin' }, 1500);
  }
}
