import Phaser from 'phaser';
import { narrativa, registro, mano, mision, LOCALIZACIONES } from '../core/juego';
import { SaveSystem } from '../core/SaveSystem';
import { audio } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';
import { pwa } from '../core/pwa';
import { alternarPantallaCompleta, botonPantallaCompleta } from '../ui/pantalla';

let avisoVisto = false;

export class MenuScene extends Phaser.Scene {
  constructor() { super('Menu'); }

  create() {
    audio.musica.poner(null);
    audio.ambiente.poner([]);
    audio.pararLargos();
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
      ...(this.iosSinInstalar() ? ['', 'En iPhone o iPad: Compartir → «Añadir a pantalla de inicio» para jugar a pantalla completa.'] : []),
    ].join('\n'), {
      fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3), align: 'center', lineSpacing: 6, wordWrap: { width: 860 },
    }).setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: t, alpha: 1, duration: 600 });
    const seguir = () => { audio.desbloquear(); avisoVisto = true; this.scene.restart(); };
    // en móvil, el primer toque pone la pantalla completa (en iOS no se puede: se instala como app).
    // Al soltar el dedo: es el gesto que los navegadores aceptan para pedirla.
    this.input.once('pointerup', (p: Phaser.Input.Pointer) => { if (p.wasTouch) alternarPantallaCompleta(this, true); seguir(); });
    this.input.keyboard?.once('keydown', seguir);
  }

  /** Safari de iOS fuera de la app instalada: allí no hay pantalla completa (diseño técnico §8.1). */
  private iosSinInstalar() {
    const nav = navigator as Navigator & { standalone?: boolean };
    const ios = /iP(hone|ad|od)/.test(nav.userAgent) || (nav.platform === 'MacIntel' && nav.maxTouchPoints > 1);
    return ios && !nav.standalone;
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
    opciones.push(['Nueva partida', () => (partida
      ? this.confirmar('Empezar de nuevo borra la partida guardada.\n¿Seguir?', () => this.nueva(), 'Empezar', 'Volver')
      : this.nueva())]);
    if (SaveSystem.capitulos().length) opciones.push(['Capítulos II', () => this.galeria()]);
    opciones.push(['Opciones', () => this.opciones()]);

    opciones.forEach(([texto, accion], i) => {
      const y = 270 + i * 54;
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
    const finales = SaveSystem.finales();
    const cierre = SaveSystem.cierreD();
    const LINEAS: Record<string, string> = {
      A: 'Naranjas y limones…', B: 'Los proles también limpian.', C: '¿Qué hora marca?',
      D: cierre ? `«${cierre}»` : '', E: 'Nunca buscan aquí.',
    };
    const lineas = ['A', 'B', 'C', 'D', 'E'].filter((f) => finales.includes(f) && LINEAS[f]).map((f) => LINEAS[f]);
    if (['A', 'B', 'C', 'D', 'E'].every((f) => finales.includes(f))) lineas.push('Él escribe la verdad. Nosotros decidimos quién la lee.');
    lineas.forEach((l, i) => {
      this.add.text(width / 2, 270 + opciones.length * 54 + 6 + i * 24, l, {
        fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.gris3), align: 'center', wordWrap: { width: 760 },
      }).setOrigin(0.5);
    });
    this.add.text(width - 12, height - 10, 'v0.4', {
      fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.gris3),
    }).setOrigin(1, 1);
    botonPantallaCompleta(this, width - 36, 36);
    // una versión nueva de la app: se instala solo si el jugador quiere, desde aquí
    const version = () => {
      if (!pwa.actualizar || !this.scene.isActive()) return;
      const t = this.add.text(12, height - 10, 'Hay una versión nueva · toca para actualizar', {
        fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.ocre4), backgroundColor: '#0b0c0fcc', padding: { x: 6, y: 4 },
      }).setOrigin(0, 1).setInteractive({ useHandCursor: true });
      t.on('pointerup', () => { t.setText('Actualizando…'); pwa.actualizar?.(); });
    };
    pwa.alHaberVersion = version;
    this.events.once('shutdown', () => { pwa.alHaberVersion = null; });
    version();
  }

  /** Opciones (diseño técnico §9): sonido, juego y accesibilidad, y la partida (exportar e importar). */
  private opciones() {
    this.scene.pause();
    this.scene.launch('Opciones', { desde: 'menu', alCerrar: () => this.scene.restart() });
    this.scene.bringToTop('Opciones');
  }

  /** Un aviso con «Sí» y «No» (empezar de nuevo encima de una partida guardada, una partida que no carga). */
  private confirmar(pregunta: string, si: (() => void) | null, textoSi = 'Sí', textoNo = 'No') {
    const { width, height } = this.scale;
    const capa = this.add.container(0, 0).setDepth(20);
    capa.add(this.add.rectangle(0, 0, width, height, 0x000000, 0.75).setOrigin(0).setInteractive());
    capa.add(this.add.rectangle(width / 2, height / 2, 560, 200, COLOR.gris1).setStrokeStyle(2, COLOR.rojo3));
    capa.add(this.add.text(width / 2, height / 2 - 40, pregunta, {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), align: 'center', wordWrap: { width: 500 }, lineSpacing: 4,
    }).setOrigin(0.5));
    const botones: [string, number, () => void][] = si ? [[textoSi, -100, () => { capa.destroy(); si(); }], [textoNo, 100, () => capa.destroy()]]
      : [[textoNo, 0, () => capa.destroy()]];
    for (const [t, dx, f] of botones) {
      const b = this.add.rectangle(width / 2 + dx, height / 2 + 50, 170, 40, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
      b.on('pointerover', () => b.setFillStyle(COLOR.rojo3));
      b.on('pointerout', () => b.setFillStyle(COLOR.gris2));
      b.on('pointerup', f);
      capa.add([b, this.add.text(width / 2 + dx, height / 2 + 50, t, { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4) }).setOrigin(0.5)]);
    }
  }

  /** Galería de los Capítulos II escritos en distintas partidas, de uno en uno. */
  private galeria() {
    const { width, height } = this.scale;
    const caps = SaveSystem.capitulos().slice().reverse();
    let i = 0;
    const capa = this.add.container(0, 0).setDepth(10);
    const pintar = () => {
      capa.removeAll(true);
      const c = caps[i];
      capa.add(this.add.rectangle(0, 0, width, height, 0x0b0c0f, 0.97).setOrigin(0).setInteractive());
      capa.add(this.add.rectangle(width / 2, 262, 820, 440, 0xe8dfc4).setStrokeStyle(1, 0x8f8a7a));
      capa.add(this.add.text(width / 2, 58, `${c.autor} · ${new Date(c.fecha).toLocaleDateString('es')}`, {
        fontFamily: FUENTE.maquina, fontSize: '20px', color: '#6a5c44',
      }).setOrigin(0.5));
      capa.add(this.add.text(100, 84, c.texto.split('¶').join('\n'), {
        fontFamily: FUENTE.maquina, fontSize: '15px', color: '#2a2218', wordWrap: { width: 760 }, lineSpacing: 3,
      }));
      const boton = (x: number, texto: string, accion: () => void) => {
        const f = this.add.rectangle(x, height - 34, 150, 36, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
        capa.add([f, this.add.text(x, height - 34, texto, { fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3) }).setOrigin(0.5)]);
        f.on('pointerup', accion);
      };
      if (i > 0) boton(width / 2 - 180, '‹ anterior', () => { i--; pintar(); });
      boton(width / 2, 'cerrar', () => capa.destroy());
      if (i < caps.length - 1) boton(width / 2 + 180, 'siguiente ›', () => { i++; pintar(); });
    };
    pintar();
  }

  private nueva() {
    narrativa.reset();
    registro.vaciar();
    mano.item = null;
    mision.reloj = null;
    this.registry.set('introPendiente', true);   // UIScene arranca el flujo principal al estar lista
    this.scene.start('Location', { escena: 'stepney', spawn: 'inicio', cargado: true });
    this.scene.launch('UI');
  }

  private continuar() {
    const p = SaveSystem.cargar('auto');
    if (!p) return this.nueva();
    try {
      narrativa.loadState(p.ink);
      registro.cargar(p.registro);
      if (!LOCALIZACIONES[p.mundo.escena]) throw new Error(`escena ${p.mundo.escena}`);
    } catch (e) {
      // el guion cambió y el estado guardado ya no encaja (diseño técnico §10.2)
      console.error('[guardado]', e);
      narrativa.reset();
      this.confirmar('Esta partida guardada no es compatible con esta versión del juego.', null, '', 'Entendido');
      return;
    }
    mano.item = null;
    mision.reloj = null;
    this.scene.start('Location', { escena: p.mundo.escena, x: p.mundo.x, y: p.mundo.y, dir: p.mundo.dir, cargado: true, reloj: p.mundo.reloj ?? null });
    this.scene.launch('UI');
  }
}
