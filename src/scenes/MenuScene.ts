import Phaser from 'phaser';
import { narrativa, registro, mano, mision } from '../core/juego';
import { SaveSystem } from '../core/SaveSystem';
import { audio, type Canal } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';

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
    this.add.text(width - 12, height - 10, 'v0.3', {
      fontFamily: FUENTE.maquina, fontSize: '16px', color: hex(COLOR.gris3),
    }).setOrigin(1, 1);
  }

  /** Opciones de sonido: los cuatro volúmenes (diseño técnico §9). Mientras está abierto suena algo para oírlos. */
  private opciones() {
    const { width, height } = this.scale;
    const capa = this.add.container(0, 0).setDepth(10);
    capa.add(this.add.rectangle(0, 0, width, height, 0x0b0c0f, 1).setOrigin(0).setInteractive());
    capa.add(this.add.text(width / 2, 70, 'OPCIONES · SONIDO', { fontFamily: FUENTE.maquina, fontSize: '36px', color: hex(COLOR.papel4) }).setOrigin(0.5));
    audio.musica.poner('prole');
    audio.ambiente.poner(['calle']);
    const CANALES: [Canal, string][] = [['general', 'General'], ['musica', 'Música'], ['efectos', 'Efectos'], ['ambiente', 'Ambiente']];
    const ANCHO = 320, X0 = width / 2 - 60;
    CANALES.forEach(([canal, nombre], i) => {
      const y = 160 + i * 74;
      capa.add(this.add.text(X0 - 40, y, nombre, { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(1, 0.5));
      const pista = this.add.rectangle(X0, y, ANCHO, 8, COLOR.gris2).setOrigin(0, 0.5);
      const lleno = this.add.rectangle(X0, y, ANCHO * audio.volumenes[canal], 8, COLOR.rojo3).setOrigin(0, 0.5);
      const asa = this.add.rectangle(X0 + ANCHO * audio.volumenes[canal], y, 16, 30, COLOR.papel4).setStrokeStyle(2, COLOR.gris1);
      const valor = this.add.text(X0 + ANCHO + 24, y, '', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel3) }).setOrigin(0, 0.5);
      // zona de toque generosa: toda la fila (44 px de alto como mínimo)
      const zona = this.add.rectangle(X0 - 10, y, ANCHO + 20, 48, 0, 0).setOrigin(0, 0.5).setInteractive({ useHandCursor: true });
      capa.add([pista, lleno, asa, valor, zona]);
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
    const cerrar = this.add.rectangle(width / 2, height - 60, 180, 40, COLOR.gris2).setStrokeStyle(1, COLOR.gris3).setInteractive({ useHandCursor: true });
    capa.add([cerrar, this.add.text(width / 2, height - 60, 'cerrar', { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3) }).setOrigin(0.5)]);
    cerrar.on('pointerup', () => { audio.musica.poner(null); audio.ambiente.poner([]); this.scene.restart(); });
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
    narrativa.loadState(p.ink);
    registro.cargar(p.registro);
    mano.item = null;
    mision.reloj = null;
    this.scene.start('Location', { escena: p.mundo.escena, x: p.mundo.x, y: p.mundo.y, dir: p.mundo.dir, cargado: true, reloj: p.mundo.reloj ?? null });
    this.scene.launch('UI');
  }
}
