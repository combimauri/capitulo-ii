import Phaser from 'phaser';
import { narrativa, registro, mano } from '../core/juego';
import { SaveSystem } from '../core/SaveSystem';
import { audio } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';

let avisoVisto = false;

export class MenuScene extends Phaser.Scene {
  constructor() { super('Menu'); }

  create() {
    if (!avisoVisto) this.aviso(); else this.menu();
  }

  /** Aviso de contenido (finales, pantalla previa al menú). */
  private aviso() {
    const { width, height } = this.scale;
    const t = this.add.text(width / 2, height / 2, [
      'Este juego contiene representaciones explícitas de tortura, ejecuciones,',
      'muerte de un menor, violencia psicológica y propaganda totalitaria.',
      'Está pensado para un público adulto.',
      '',
      'Basado libremente en 1984, de George Orwell.',
      '',
      '[ toca o pulsa una tecla para continuar ]',
    ].join('\n'), {
      fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3), align: 'center', lineSpacing: 6,
    }).setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: t, alpha: 1, duration: 600 });
    const seguir = () => { audio.desbloquear(); avisoVisto = true; this.scene.restart(); };
    this.input.once('pointerdown', seguir);
    this.input.keyboard?.once('keydown', seguir);
  }

  private menu() {
    const { width, height } = this.scale;
    this.add.rectangle(width / 2, height / 2, width, height, COLOR.negro);
    this.add.rectangle(width / 2, 150, 360, 4, COLOR.rojo3);
    this.add.text(width / 2, 108, 'CAPÍTULO II', {
      fontFamily: FUENTE.maquina, fontSize: '72px', color: hex(COLOR.papel4),
    }).setOrigin(0.5);
    this.add.text(width / 2, 176, 'Franja Aérea 1 · 1984', {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.rojo4),
    }).setOrigin(0.5);

    const partida = SaveSystem.cargar('auto');
    const opciones: [string, () => void][] = [];
    if (partida) opciones.push(['Continuar', () => this.continuar()]);
    opciones.push(['Nueva partida', () => this.nueva()]);

    opciones.forEach(([texto, accion], i) => {
      const y = 290 + i * 54;
      const fondo = this.add.rectangle(width / 2, y, 300, 40, COLOR.gris2).setStrokeStyle(1, COLOR.gris3)
        .setInteractive({ useHandCursor: true });
      this.add.text(width / 2, y, texto, { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel3) })
        .setOrigin(0.5);
      fondo.on('pointerover', () => fondo.setFillStyle(COLOR.rojo3));
      fondo.on('pointerout', () => fondo.setFillStyle(COLOR.gris2));
      fondo.on('pointerup', () => { audio.desbloquear(); accion(); });
    });
    this.input.keyboard?.once('keydown-ENTER', () => opciones[0][1]());

    if (!SaveSystem.disponible()) {
      this.add.text(width / 2, height - 40, 'Este navegador no permite guardar la partida.', {
        fontFamily: FUENTE.texto, fontSize: '14px', color: hex(COLOR.rojo4),
      }).setOrigin(0.5);
    }
    // líneas que dejan los finales alcanzados (guion, «Desbloqueos del menú principal»)
    const LINEAS: Record<string, string> = { A: 'Naranjas y limones…', B: 'Los proles también limpian.' };
    SaveSystem.finales().filter((f) => LINEAS[f]).forEach((f, i) => {
      this.add.text(width / 2, 290 + opciones.length * 54 + 10 + i * 24, LINEAS[f], {
        fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.gris3),
      }).setOrigin(0.5);
    });
    this.add.text(width - 12, height - 10, 'v0.1 · demo técnica', {
      fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.gris3),
    }).setOrigin(1, 1);
  }

  private nueva() {
    narrativa.reset();
    registro.vaciar();
    mano.item = null;
    this.registry.set('introPendiente', true);   // UIScene arranca el flujo principal al estar lista
    this.scene.start('Location', { escena: 'stepney', spawn: 'inicio', cargado: true });
    this.scene.launch('UI');
  }

  private continuar() {
    const p = SaveSystem.cargar('auto');
    if (!p) return this.nueva();
    narrativa.loadState(p.ink);
    registro.cargar(p.registro);
    mano.item = null;
    this.scene.start('Location', { escena: p.mundo.escena, x: p.mundo.x, y: p.mundo.y, dir: p.mundo.dir, cargado: true });
    this.scene.launch('UI');
  }
}
