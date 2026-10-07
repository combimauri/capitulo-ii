/**
 * Capa de interfaz siempre activa (diseño técnico §7): diálogo, pensamientos, telepantalla,
 * carteles, elecciones, acciones bloqueantes (minijuegos, pausas, efectos), foco de objetos,
 * controles táctiles, inventario, ojo de la Sospecha y depuración.
 */
import Phaser from 'phaser';
import { narrativa, registro, mano, mision, hora, EV, ITEMS, tactil } from '../core/juego';
import type { ChoiceOption, Line } from '../core/NarrativeBridge';
import type { Tag } from '../core/tags';
import type { ResultadoMinijuego } from './minijuegos/Minijuego';
import { audio } from '../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../ui/estilo';
import { SaveSystem } from '../core/SaveSystem';
import { destello, suave } from '../ui/destellos';
import { opciones as opc, CPS, alCambiarOpcion } from '../core/Opciones';

/** La caja de diálogo; con la interfaz al 125 % crece hacia arriba (diseño técnico §9). */
const caja = () => { const h = Math.round(132 * escala()); return { x: 40, y: 518 - h, w: 880, h }; };
const escala = () => opc.ui / 100;
const px = (n: number) => `${Math.round(n * escala())}px`;

/** Minijuegos por etiqueta: cf → Facecrime; minijuego:<tipo> → escena. */
const MINIJUEGOS: Record<string, string> = {
  cf: 'Facecrime', dp: 'Registro', cascotes: 'Cascotes', ficha: 'Ficha', parte: 'Parte', frente: 'Frente', pancarta: 'Pancarta', impactos: 'Impactos', sammy: 'Sammy', diario: 'Diario', comparar: 'Comparar', esconder: 'Esconder',
  documento: 'Documento', libro: 'Libro', copiar: 'Copiar', palanca: 'Palanca', llaves: 'Llaves', combinacion: 'Combinacion', rectificacion: 'Rectificacion', lista: 'Lista',
  tuneles: 'Tuneles', capitulo: 'Capitulo', dial: 'Dial', h101: 'Habitacion101', declaracion: 'Declaracion', resistencia: 'Resistencia', epilogo: 'Epilogo', creditos: 'Creditos', cf_auto: 'CFAutomatico',
};

interface FocoInfo { nombre: string; x: number; y: number; mirar: boolean; usar: boolean; hablar: boolean; raton?: boolean }

export class UIScene extends Phaser.Scene {
  private activo = false;
  private enAccion = false;
  private bloqueoHasta = 0;
  private escribiendo: Phaser.Time.TimerEvent | null = null;
  private textoCompleto = '';
  private destino: Phaser.GameObjects.Text | null = null;
  private esTactil = false;

  private caja!: Phaser.GameObjects.Container;
  private cajaFondo!: Phaser.GameObjects.Rectangle;
  private cajaFranja!: Phaser.GameObjects.Rectangle;
  private nombre!: Phaser.GameObjects.Text;
  private nombreFondo!: Phaser.GameObjects.Rectangle;
  private texto!: Phaser.GameObjects.Text;
  private indicador!: Phaser.GameObjects.Text;
  private pensamiento!: Phaser.GameObjects.Container;
  private pensamientoTexto!: Phaser.GameObjects.Text;
  private cartel!: Phaser.GameObjects.Container;
  private cartelTexto!: Phaser.GameObjects.Text;
  private velo!: Phaser.GameObjects.Rectangle;
  private opciones!: Phaser.GameObjects.Container;
  private opcionesLista: { fondo: Phaser.GameObjects.Rectangle; choice: ChoiceOption }[] = [];
  private opcionSel = 0;
  private foco!: Phaser.GameObjects.Container;
  private focoTexto!: Phaser.GameObjects.Text;
  private botones!: Phaser.GameObjects.Container;
  private joystick!: Phaser.GameObjects.Graphics;
  private inventario!: Phaser.GameObjects.Container;
  private ojo!: Phaser.GameObjects.Graphics;
  private depuracion!: Phaser.GameObjects.Text;
  private depurando = false;
  private inventarioAbiertoEn = 0;
  private consultando = false;
  private avisosPendientes: string[] = [];
  private enMano!: Phaser.GameObjects.Container;
  private aviso!: Phaser.GameObjects.Container;
  private reloj!: Phaser.GameObjects.Text;
  private carpeta!: Phaser.GameObjects.Container;
  private dinamo!: Phaser.GameObjects.Container;
  private medidor!: Phaser.GameObjects.Container;
  private medidorBarra!: Phaser.GameObjects.Rectangle;
  private medidorTexto!: Phaser.GameObjects.Text;
  private cargaDinamo!: Phaser.GameObjects.Rectangle;

  constructor() { super('UI'); }

  create() {
    this.activo = false; this.enAccion = false;
    this.esTactil = this.sys.game.device.input.touch;
    this.velo = this.add.rectangle(0, 0, 960, 540, 0x000000, 1).setOrigin(0).setAlpha(0).setDepth(28);   // bajo el texto: se narra a oscuras
    this.crearCaja();
    this.crearPensamiento();
    this.crearCartel();
    this.opciones = this.add.container(0, 0).setVisible(false).setDepth(30);
    this.crearFoco();
    this.crearBotonesTactiles();
    this.joystick = this.add.graphics().setDepth(25);
    this.inventario = this.add.container(0, 0).setVisible(false).setDepth(60);
    this.ojo = this.add.graphics().setDepth(20);
    this.crearAyudaOjo();
    this.enMano = this.add.container(0, 0).setDepth(22).setVisible(false);
    this.aviso = this.add.container(0, 0).setDepth(45).setVisible(false);
    this.crearMision();
    this.ajustarTamano();
    this.consultando = false;
    this.dibujarOjo(Number(narrativa.get('sospecha')) || 0);
    narrativa.observe('sospecha', (v) => this.dibujarOjo(Number(v)));
    this.depuracion = this.add.text(8, 8, '', {
      fontFamily: FUENTE.maquina, fontSize: '18px', color: '#ffd34d', backgroundColor: '#000000aa', padding: { x: 6, y: 4 },
    }).setVisible(false).setDepth(100);

    const ev = this.game.events;
    const iniciar = (ruta?: string) => this.iniciar(ruta);
    const foco = (info: FocoInfo | null) => this.mostrarFoco(info);
    const joy = () => this.dibujarJoystick();
    const manoCambia = () => this.dibujarMano();
    ev.on(EV.dialogoIniciar, iniciar);
    ev.on(EV.foco, foco);
    ev.on(EV.joystick, joy);
    ev.on(EV.mano, manoCambia);
    const quitar = narrativa.on('command', (t: Tag) => { if (t.key === 'objeto') this.avisarObjeto(t.value); });
    // opciones cambiadas desde la pausa: el tamaño y la mano dominante se aplican al momento
    const quitarOpciones = alCambiarOpcion((k) => {
      if (k === 'ui') this.ajustarTamano();
      if (k === 'mano') this.crearBotonesTactiles();
    });
    // la app pasa a segundo plano (móvil): al volver, el juego espera en pausa
    const oculto = () => this.pausar();
    ev.on(Phaser.Core.Events.HIDDEN, oculto);
    this.events.once('shutdown', () => {
      ev.off(EV.dialogoIniciar, iniciar); ev.off(EV.foco, foco); ev.off(EV.joystick, joy); ev.off(EV.mano, manoCambia); quitar();
      ev.off(Phaser.Core.Events.HIDDEN, oculto); quitarOpciones();
    });

    const kb = this.input.keyboard!;
    ['SPACE', 'ENTER', 'E'].forEach((k) => kb.on(`keydown-${k}`, () => this.confirmar()));
    kb.on('keydown-UP', () => this.moverSeleccion(-1));
    kb.on('keydown-DOWN', () => this.moverSeleccion(1));
    kb.on('keydown-W', () => this.moverSeleccion(-1));
    kb.on('keydown-S', () => this.moverSeleccion(1));
    kb.on('keydown-I', () => this.alternarInventario());
    kb.on('keydown-ESC', () => {
      if (this.inventario.visible) this.alternarInventario();
      else if (mano.item) this.soltarObjeto();
      else this.pausar();
    });
    kb.on('keydown-L', () => this.abrirRegistro());
    kb.on('keydown-C', () => { if (!this.activo) this.game.events.emit(EV.carpeta); });
    kb.on('keydown-F', () => { if (!this.activo) this.game.events.emit(EV.dinamo); });
    kb.on('keydown', (e: KeyboardEvent) => {
      audio.desbloquear();
      const n = Number(e.key);
      if (n >= 1 && n <= this.opcionesLista.length) this.elegir(n - 1);
    });
    kb.on('keydown-F1', () => this.alternarDepuracion());
    this.input.on('pointerdown', (p: Phaser.Input.Pointer) => {
      audio.desbloquear();
      if (this.registry.get('uiCapturo') === p.downTime) return;   // tocar el ojo no pasa la línea
      if (this.activo && !this.enAccion && !this.opciones.visible) this.confirmar();
    });

    if (this.registry.get('introPendiente')) {
      this.registry.set('introPendiente', false);
      this.game.events.emit(EV.dialogoIniciar);   // avisa también a LocationScene (bloquea el movimiento)
    }
  }

  update() {
    this.botones.setVisible(!this.activo && !this.inventario.visible && !this.consultando);
    this.enMano.setVisible(!!mano.item && !this.activo && !this.consultando);
    const r = mision.reloj;
    this.reloj.setVisible(!!r && !r.oculto && !this.consultando);
    if (r) {
      const queda = r.limite - r.transcurrido;
      this.reloj.setText(hora(r.inicio + r.transcurrido)).setColor(hex(queda < 30 ? COLOR.rojo4 : COLOR.papel4));
    }
    this.carpeta.setVisible(mision.social && !this.activo && !this.consultando);
    this.dinamo.setVisible(mision.oscuro && !this.consultando);
    const m = mision.medidor;
    this.medidor.setVisible(!!m && !this.activo && !this.consultando);
    if (m) {
      const v = Phaser.Math.Clamp(Number(narrativa.get(m.variable)) || 0, 0, 100) / 100;
      this.medidorTexto.setText(m.etiqueta.toUpperCase());
      this.medidorBarra.setSize(176 * v, 6).setFillStyle(v < 0.3 ? COLOR.rojo4 : COLOR.papel3);
    }
    this.cargaDinamo.setSize(176 * mision.carga, 6).setFillStyle(mision.carga < 0.2 ? COLOR.rojo4 : COLOR.ocre4);
    (this.carpeta.getData('fondo') as Phaser.GameObjects.Rectangle).setFillStyle(mision.carpeta ? COLOR.ocre4 : COLOR.gris1, 0.85);
    (this.carpeta.getData('texto') as Phaser.GameObjects.Text).setColor(hex(mision.carpeta ? COLOR.gris1 : COLOR.papel4));
    if (this.depurando) {
      this.depuracion.setText([
        'DEPURACIÓN (F1)',
        `duda ${narrativa.get('duda')} · sospecha ${narrativa.get('sospecha')} · jornada ${narrativa.get('jornada')}`,
        `${narrativa.get('nombre')} ${narrativa.get('apellido')} (${narrativa.get('genero')}) · ${narrativa.get('num')}`,
        `inventario: ${narrativa.list('inventario').join(', ')}`,
      ].join('\n'));
    }
  }

  // ------------------------------------------------------------------ construcción
  private crearCaja() {
    const CAJA = caja();
    this.cajaFondo = this.add.rectangle(0, 0, CAJA.w, CAJA.h, COLOR.papel3).setOrigin(0).setStrokeStyle(2, COLOR.gris2);
    this.cajaFranja = this.add.rectangle(0, 0, 8, CAJA.h, COLOR.rojo3).setOrigin(0);
    this.texto = this.add.text(28, 22, '', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.gris2), lineSpacing: 6,
      wordWrap: { width: CAJA.w - 56, useAdvancedWrap: true },
    });
    this.nombreFondo = this.add.rectangle(20, -14, 10, 28, COLOR.gris2).setOrigin(0);
    this.nombre = this.add.text(32, -10, '', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) });
    this.indicador = this.add.text(CAJA.w - 26, CAJA.h - 26, '▼', { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.rojo3) });
    this.tweens.add({ targets: this.indicador, alpha: 0.2, duration: 450, yoyo: true, repeat: -1 });
    this.caja = this.add.container(CAJA.x, CAJA.y,
      [this.cajaFondo, this.cajaFranja, this.texto, this.nombreFondo, this.nombre, this.indicador]).setVisible(false).setDepth(30);
  }

  /** Tamaño de la interfaz (100 % o 125 %): la caja, el pensamiento, el cartel y el foco. */
  private ajustarTamano() {
    const CAJA = caja();
    this.cajaFondo.setSize(CAJA.w, CAJA.h);
    this.cajaFranja.setSize(8, CAJA.h);
    this.caja.setPosition(CAJA.x, CAJA.y);
    this.indicador.setPosition(CAJA.w - 26, CAJA.h - 26);
    this.nombre.setFontSize(px(22));
    this.nombreFondo.setPosition(20, -10 - Math.round(4 * escala())).setSize(this.nombre.width + 24, Math.round(28 * escala()));
    this.nombre.setY(-6 - Math.round(4 * escala()));
    this.pensamientoTexto.setFontSize(px(22));
    this.cartelTexto.setFontSize(px(30));
    this.focoTexto.setFontSize(px(16));
  }

  private crearPensamiento() {
    const banda = this.add.rectangle(480, 0, 960, 10, 0x000000, 0.55).setOrigin(0.5, 0);
    this.pensamientoTexto = this.add.text(480, 24, '', {
      fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 6,
      wordWrap: { width: 820, useAdvancedWrap: true }, stroke: '#000000', strokeThickness: 3,
    }).setOrigin(0.5, 0);
    this.pensamiento = this.add.container(0, 0, [banda, this.pensamientoTexto]).setVisible(false).setDepth(30);
    this.pensamiento.setData('banda', banda);
  }

  private crearCartel() {
    const fondo = this.add.rectangle(0, 0, 960, 540, COLOR.negro, 0.94).setOrigin(0);
    this.cartelTexto = this.add.text(480, 270, '', {
      fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 8,
      wordWrap: { width: 760, useAdvancedWrap: true },
    }).setOrigin(0.5);
    this.cartel = this.add.container(0, 0, [fondo, this.cartelTexto]).setVisible(false).setDepth(50);
  }

  private crearFoco() {
    const fondo = this.add.rectangle(0, 0, 10, 24, COLOR.gris1, 0.85).setOrigin(0.5, 1).setStrokeStyle(1, COLOR.gris3);
    this.focoTexto = this.add.text(0, -12, '', { fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    this.foco = this.add.container(0, 0, [fondo, this.focoTexto]).setVisible(false).setDepth(15);
    this.foco.setData('fondo', fondo);
  }

  /**
   * Botones en pantalla (diseño técnico §8). En táctil, todos y del lado de la mano dominante; en escritorio,
   * objetos, registro y menú (usar y mirar ya son el clic), con su tecla al pasar el ratón.
   */
  private crearBotonesTactiles() {
    this.botones?.destroy();
    this.botones = this.add.container(0, 0).setDepth(20).setVisible(false);
    const zurdo = this.esTactil && opc.mano === 'izquierda';
    const ayuda = this.add.text(0, 0, '', {
      fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.papel4), backgroundColor: '#16181cdd', padding: { x: 6, y: 3 },
    }).setOrigin(1, 0.5).setVisible(false);
    const boton = (x0: number, y: number, r: number, etiqueta: string, tecla: string, alPulsar: () => void) => {
      const x = zurdo ? 960 - x0 : x0;
      const c = this.add.circle(x, y, r, COLOR.gris1, 0.55).setStrokeStyle(2, COLOR.papel3, 0.7).setInteractive({ useHandCursor: true });
      const t = this.add.text(x, y, etiqueta, { fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      c.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); alPulsar(); });
      c.on('pointerover', (p: Phaser.Input.Pointer) => {
        if (p.wasTouch) return;
        c.setFillStyle(COLOR.rojo3, 0.85);
        ayuda.setText(tecla).setPosition(x - r - 8, y).setVisible(true);
      });
      c.on('pointerout', () => { c.setFillStyle(COLOR.gris1, 0.55); ayuda.setVisible(false); });
      this.botones.add([c, t]);
    };
    if (this.esTactil) {
      boton(880, 450, 44, 'USAR', 'E · Espacio', () => this.game.events.emit(EV.accion, 'principal'));
      boton(790, 488, 34, 'MIRAR', 'Q', () => this.game.events.emit(EV.accion, 'mirar'));
    }
    boton(900, 92, 30, 'OBJ.', 'Objetos · I', () => this.alternarInventario());
    boton(900, 160, 30, 'REG.', 'Registro · L', () => this.abrirRegistro());
    boton(900, 228, 30, 'MENÚ', 'Pausa y opciones · Esc', () => this.pausar());
    this.botones.add(ayuda);
  }

  /** Abre la pausa (Esc, botón MENÚ o la app en segundo plano). No en mitad de un minijuego. */
  private pausar() {
    if (this.enAccion || this.consultando || this.scene.isActive('Pausa') || !this.scene.isActive()) return;
    if (this.inventario.visible) this.alternarInventario();
    this.scene.launch('Pausa');
    this.scene.bringToTop('Pausa');
  }

  /** El reloj de las misiones (arriba, en el centro) y el botón de la carpeta del sigilo social. */
  private crearMision() {
    this.reloj = this.add.text(480, 22, '', {
      fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4), backgroundColor: '#0b0c0fcc', padding: { x: 10, y: 2 },
    }).setOrigin(0.5, 0).setDepth(21).setVisible(false);
    const fondo = this.add.rectangle(0, 0, 190, 40, COLOR.gris1, 0.85).setStrokeStyle(2, COLOR.ocre4).setInteractive({ useHandCursor: true });
    const texto = this.add.text(0, 0, this.esTactil ? 'CARPETA' : 'C · CARPETA', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    fondo.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); this.game.events.emit(EV.carpeta); });
    this.carpeta = this.add.container(this.esTactil ? 760 : 840, this.esTactil ? 92 : 510, [fondo, texto]).setDepth(21).setVisible(false);
    this.carpeta.setData('fondo', fondo).setData('texto', texto);
    // la linterna de dinamo: cada toque es una vuelta de manivela
    const fd = this.add.rectangle(0, 0, 190, 46, COLOR.gris1, 0.85).setStrokeStyle(2, COLOR.ocre4).setInteractive({ useHandCursor: true });
    const td = this.add.text(0, -6, this.esTactil ? 'DINAMO' : 'F · DINAMO', { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    this.cargaDinamo = this.add.rectangle(-88, 14, 176, 6, COLOR.ocre4).setOrigin(0, 0.5);
    fd.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); this.game.events.emit(EV.dinamo); });
    this.dinamo = this.add.container(this.esTactil ? 760 : 840, this.esTactil ? 92 : 506, [fd, td, this.add.rectangle(-88, 14, 176, 6, 0x000000, 0.6).setOrigin(0, 0.5), this.cargaDinamo]).setDepth(21).setVisible(false);
    // un medidor que lee una variable de ink (el hambre de la celda): solo informa, no se toca
    this.medidorTexto = this.add.text(0, 0, '', { fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(COLOR.papel4) });
    this.medidorBarra = this.add.rectangle(2, 26, 176, 6, COLOR.papel3).setOrigin(0, 0.5);
    this.medidor = this.add.container(24, 18, [
      this.add.rectangle(-8, -4, 196, 42, COLOR.gris1, 0.75).setOrigin(0),
      this.medidorTexto, this.add.rectangle(2, 26, 176, 6, 0x000000, 0.6).setOrigin(0, 0.5), this.medidorBarra,
    ]).setDepth(21).setVisible(false);
  }

  // ------------------------------------------------------------------ flujo de diálogo
  private iniciar(ruta?: string) {
    if (ruta) narrativa.goTo(ruta);
    this.activo = true;
    this.bloqueoHasta = this.time.now + 180;
    this.foco.setVisible(false);
    if (this.inventario.visible) this.alternarInventario();
    this.iniciando = true;
    this.avanzar();
    this.iniciando = false;
  }

  /** Mientras se reparte el aviso de inicio: un knot sin nada que decir termina antes de que todos lo hayan oído. */
  private iniciando = false;

  private avanzar() {
    const paso = narrativa.next();
    if (paso.type === 'line') this.mostrarLinea(paso.line);
    else if (paso.type === 'accion') void this.ejecutarAcciones(paso.acciones, paso.line);
    else if (paso.type === 'choices') this.mostrarOpciones(paso.choices);
    else this.terminar();
  }

  private terminar() {
    this.activo = false;
    if (this.vinetaActual) { const v = this.vinetaActual; this.vinetaActual = null; this.tweens.add({ targets: v, alpha: 0, duration: 500, onComplete: () => v.destroy() }); }
    this.ocultarTodo();
    if (this.velo.alpha > 0) this.tweens.add({ targets: this.velo, alpha: 0, duration: 700 });
    // un diálogo vacío (volver a entrar al pub: «pub_visto» → DONE) acaba dentro del propio aviso de inicio;
    // el fin se avisa después, o el escenario lo recibiría antes que el inicio y se quedaría ocupado
    if (this.iniciando) queueMicrotask(() => { if (!this.activo) this.game.events.emit(EV.dialogoFin); });
    else this.game.events.emit(EV.dialogoFin);
  }

  private ocultarTodo() {
    this.caja.setVisible(false);
    this.pensamiento.setVisible(false);
    this.cartel.setVisible(false);
    this.opciones.setVisible(false).removeAll(true);
    this.opcionesLista = [];
  }

  private confirmar() {
    if (!this.activo || this.enAccion || this.time.now < this.bloqueoHasta) return;
    if (this.opciones.visible) return this.elegir(this.opcionSel);
    if (this.escribiendo) return this.completarTexto();
    this.avanzar();
  }

  // ------------------------------------------------------------------ acciones bloqueantes
  private async ejecutarAcciones(acciones: Tag[], linea: Line | null) {
    this.enAccion = true;
    for (const a of acciones) {
      if (a.key === 'sfx') {
        audio.play(a.value);
      } else if (a.key === 'esperar') {
        this.ocultarTodo();
        await this.esperar(Number(a.value) * 1000 || 1000);
      } else if (a.key === 'fx') {
        await this.efecto(a.value);
      } else if (a.key === 'recuerdo') {
        this.ocultarTodo();
        await this.recuerdo(a.value);
      } else if (a.key === 'vineta') {
        this.ocultarTodo();
        await this.vineta(a.value);
      } else {
        const tipo = a.key === 'minijuego' ? a.value.split(',')[0].trim() : a.key;
        const escena = MINIJUEGOS[tipo];
        if (!escena) { console.warn(`[minijuego] desconocido: ${tipo}`); continue; }
        this.ocultarTodo();
        // # documento:planilla_s18 → { id: 'planilla_s18' }
        const params = Object.keys(a.params).length || a.key === 'minijuego' ? a.params : { id: a.value };
        const r = await this.lanzarMinijuego(escena, params);
        // un resultado que no encaja nunca debe dejar el diálogo colgado (enAccion)
        try { this.aplicarResultado(tipo, params, r); } catch (e) { console.error(`[minijuego] ${tipo}`, e); }
      }
    }
    this.enAccion = false;
    this.bloqueoHasta = this.time.now + 150;
    if (linea) this.mostrarLinea(linea); else this.avanzar();
  }

  private esperar(ms: number) {
    return new Promise<void>((ok) => this.time.delayedCall(ms, ok));
  }

  private lanzarMinijuego(escena: string, params: Record<string, string>) {
    return new Promise<ResultadoMinijuego>((ok) => this.scene.launch(escena, { params, alTerminar: ok }));
  }

  private aplicarResultado(tipo: string, params: Record<string, string>, r: ResultadoMinijuego) {
    if (tipo === 'cf') {
      const id = (params.id ?? '').toLowerCase().replace(/^cf-/, '').replace(/-/g, '_');
      narrativa.set(`cf_${id}`, r.resultado);
      // datos extra que la historia quiera conocer: cf_<id>_transicion, cf_<id>_amory…
      for (const [k, v] of Object.entries(r.datos ?? {})) this.fijar(`cf_${id}_${k}`, v);
    } else if (tipo === 'dp') {
      // # dp:id=DP-J3-AMORY → dp_j3_amory = "aceptar" | "recordar"
      narrativa.set((params.id ?? '').toLowerCase().replace(/-/g, '_'), r.resultado);
    } else if (tipo === 'ficha' && r.datos) {
      for (const k of ['nombre', 'apellido', 'num']) narrativa.set(k, String(r.datos[k]));
      narrativa.call('fijar_genero', String(r.datos.genero));
    } else if (tipo === 'diario') {
      // la frase queda guardada para el Capítulo II; la entrada ya no se vuelve a ofrecer
      if (r.resultado && r.datos?.entrada) {
        narrativa.set(`${r.datos.entrada}_escrita`, true);
        if (narrativa.story.variablesState.GlobalVariableExistsWithName(`${r.datos.entrada}_frase`)) narrativa.set(`${r.datos.entrada}_frase`, r.resultado);
        narrativa.set('diario_ultima', r.resultado);
        narrativa.set('diario_texto', `${narrativa.get('diario_texto') || ''}¶${r.resultado}`);
        narrativa.set('diario_entradas', (Number(narrativa.get('diario_entradas')) || 0) + 1);
      }
    } else {
      if (tipo === 'capitulo' && r.datos) {
        // queda para siempre en la galería de Capítulos II
        SaveSystem.guardarCapitulo({ autor: `${narrativa.get('nombre')} ${narrativa.get('apellido')}`, texto: String(r.datos.texto), cierre: String(r.datos.cierre) });
      }
      if (params.resultado) narrativa.set(params.resultado, r.resultado);   // p. ej. # minijuego:pancarta,resultado=pancarta_j2
      if (params.vars && r.datos) for (const [k, v] of Object.entries(r.datos)) this.fijar(`${params.vars}_${k}`, v);
    }
  }

  /**
   * Escribe un dato de minijuego en ink solo si la historia lo declara, y con el tipo de la variable
   * (un número de pancartas no puede llegar como texto: ink no compara texto con números).
   */
  private fijar(nombre: string, v: unknown) {
    if (!narrativa.story.variablesState.GlobalVariableExistsWithName(nombre)) return;
    const actual = narrativa.get(nombre);
    if (typeof actual === 'number') narrativa.set(nombre, Number(v) || 0);
    else if (typeof actual === 'boolean') narrativa.set(nombre, v === true || v === 'si' || v === 'true');
    else narrativa.set(nombre, String(v));
  }

  /** Un recuerdo que asalta (≈2 s): la imagen en sepia, a golpes de luz.  # recuerdo:loc-stepney_ivy */
  private recuerdo(clave: string): Promise<void> {
    return new Promise((ok) => {
      if (!this.textures.exists(clave)) return ok();
      const img = this.add.image(480, 270, clave).setScale(2).setTint(0xc8a878).setDepth(45).setAlpha(0);
      audio.play('grieta');
      // con destellos reducidos, la imagen aparece y se va una sola vez, sin golpes de luz
      if (suave()) this.tweens.add({ targets: img, alpha: { from: 0, to: 0.9 }, duration: 500, yoyo: true, hold: 900, onComplete: () => { img.destroy(); ok(); } });
      else this.tweens.add({ targets: img, alpha: { from: 0, to: 0.95 }, duration: 90, yoyo: true, repeat: 4, hold: 260,
        onComplete: () => { img.destroy(); ok(); } });
    });
  }

  /**
   * Viñetas fijas de los montajes: una imagen a pantalla completa bajo el texto, hasta la siguiente viñeta
   * o «vineta:fin».  # vineta:loc-pasillo · # vineta:vineta-plaza,gris=si
   */
  private vinetaActual: Phaser.GameObjects.Image | null = null;
  private vineta(valor: string): Promise<void> {
    const [clave, ...resto] = valor.split(',');
    const gris = resto.some((r) => r.trim() === 'gris=si');
    return new Promise((ok) => {
      const vieja = this.vinetaActual;
      this.vinetaActual = null;
      if (vieja) this.tweens.add({ targets: vieja, alpha: 0, duration: 400, onComplete: () => vieja.destroy() });
      if (clave === 'fin' || !this.textures.exists(clave)) { this.time.delayedCall(vieja ? 400 : 0, ok); return; }
      const img = this.add.image(480, 270, clave).setDepth(25).setAlpha(0);
      img.setScale(Math.max(960 / img.width, 540 / img.height));
      if (gris) img.setTint(0x9a9a9a);
      this.vinetaActual = img;
      this.tweens.add({ targets: img, alpha: 1, duration: 600, onComplete: () => ok() });
    });
  }

  /** Efectos de pantalla: negro, blanco, fundido, temblor, destello. */
  private efecto(fx: string): Promise<void> {
    const loc = this.scene.get('Location');
    return new Promise((ok) => {
      switch (fx) {
        case 'negro':
          this.velo.setFillStyle(0x000000);
          this.tweens.add({ targets: this.velo, alpha: 1, duration: 500, onComplete: () => ok() });
          break;
        case 'aclarar':
          this.tweens.add({ targets: this.velo, alpha: 0, duration: 700, onComplete: () => ok() });
          break;
        case 'blanco':
          this.velo.setFillStyle(0xffffff);
          this.tweens.add({ targets: this.velo, alpha: 1, duration: 1400, onComplete: () => ok() });
          break;
        case 'destello':
          this.velo.setFillStyle(0xffffff).setAlpha(destello(1));
          this.tweens.add({ targets: this.velo, alpha: 0, duration: 900, onComplete: () => ok() });
          break;
        case 'temblor':
          loc?.cameras.main.shake(700, 0.012);
          this.time.delayedCall(700, () => ok());
          break;
        default:
          ok();
      }
    });
  }

  // ------------------------------------------------------------------ líneas
  private mostrarLinea(l: Line) {
    this.ocultarTodo();
    if (l.kind !== 'cartel') registro.anotar(l.id, l.kind === 'pensamiento' ? 'PENSAMIENTO' : l.kind === 'telepantalla' ? 'TELEPANTALLA' : l.speaker, l.text);
    if (l.kind === 'pensamiento') {
      this.pensamiento.setVisible(true);
      // sobre el blanco (fx:blanco), tinta oscura sin franja: la franja gris no deja leer
      const sobreBlanco = this.velo.alpha > 0.5 && this.velo.fillColor === 0xffffff;
      this.pensamientoTexto.setColor(sobreBlanco ? '#22252a' : hex(COLOR.papel4)).setStroke('#000000', sobreBlanco ? 0 : 3);
      this.escribir(this.pensamientoTexto, l.text);
      const banda = this.pensamiento.getData('banda') as Phaser.GameObjects.Rectangle;
      banda.setVisible(!sobreBlanco);
      banda.setSize(960, this.alturaFinal(this.pensamientoTexto, l.text) + 44);
      return;
    }
    if (l.kind === 'cartel') {
      this.cartel.setVisible(true).setAlpha(0);
      this.tweens.add({ targets: this.cartel, alpha: 1, duration: 300 });
      this.cartelTexto.setText(l.text.replace(/¶/g, '\n'));   // ¶ = salto de línea (ink no deja escribir otro)
      return;
    }
    const tele = l.kind === 'telepantalla';
    if (tele) audio.agachar(1.5 + l.text.length * 0.045);   // cuando habla la telepantalla, lo demás baja
    this.cajaFondo.setFillStyle(tele ? COLOR.tele1 : COLOR.papel3).setStrokeStyle(2, tele ? COLOR.tele4 : COLOR.gris2);
    this.cajaFranja.setFillStyle(tele ? COLOR.tele4 : COLOR.rojo3);
    this.texto.setStyle({ fontFamily: tele ? FUENTE.maquina : FUENTE.texto, fontSize: px(tele ? 28 : 22),
      color: hex(tele ? COLOR.tele5 : COLOR.gris2) });
    const quien = tele ? 'TELEPANTALLA' : l.speaker === 'PROTAGONISTA' ? String(narrativa.get('nombre')).toUpperCase() : (l.speaker ?? '');
    this.nombre.setText(quien).setColor(hex(tele ? COLOR.tele5 : COLOR.papel4));
    this.nombreFondo.setVisible(!!quien).setSize(this.nombre.width + 24, Math.round(28 * escala())).setFillStyle(tele ? COLOR.tele0 : COLOR.gris2);
    this.caja.setVisible(true);
    this.escribir(this.texto, l.text);
  }

  private alturaFinal(t: Phaser.GameObjects.Text, s: string) {
    const prev = t.text; t.setText(s); const h = t.height; t.setText(prev); return h;
  }

  private escribir(destino: Phaser.GameObjects.Text, texto: string) {
    this.escribiendo?.remove();
    this.destino = destino;
    this.textoCompleto = texto;
    this.indicador.setVisible(false);
    let n = 0;
    destino.setText('');
    const cps = CPS[opc.texto];
    if (!Number.isFinite(cps)) { this.completarTexto(); return; }
    this.escribiendo = this.time.addEvent({
      delay: 1000 / cps,
      repeat: texto.length - 1,
      callback: () => {
        n++;
        destino.setText(texto.slice(0, n));
        if (n >= texto.length) this.completarTexto();
      },
    });
  }

  private completarTexto() {
    this.escribiendo?.remove();
    this.escribiendo = null;
    this.destino?.setText(this.textoCompleto);
    this.indicador.setVisible(true);
  }

  // ------------------------------------------------------------------ elecciones
  private mostrarOpciones(choices: ChoiceOption[]) {
    this.caja.setVisible(false);
    this.opciones.removeAll(true);
    this.opcionesLista = [];
    const alto = Math.round(46 * escala()), sep = 10, ancho = Math.round(700 * escala());
    const y0 = 290 - (choices.length * (alto + sep)) / 2;
    choices.forEach((c, i) => {
      const y = y0 + i * (alto + sep);
      const fondo = this.add.rectangle(480, y, ancho, alto, COLOR.gris2, 0.95).setStrokeStyle(2, COLOR.gris3)
        .setInteractive({ useHandCursor: true });
      const t = this.add.text(480, y, `${i + 1}. ${c.text}`, {
        fontFamily: FUENTE.texto, fontSize: px(21), color: hex(COLOR.papel4), align: 'center', wordWrap: { width: ancho - 24, useAdvancedWrap: true },
      }).setOrigin(0.5);
      fondo.on('pointerover', () => this.seleccionar(i));
      fondo.on('pointerup', () => this.elegir(i));
      this.opciones.add([fondo, t]);
      this.opcionesLista.push({ fondo, choice: c });
    });
    this.opciones.setVisible(true);
    this.seleccionar(0);
    this.bloqueoHasta = this.time.now + 200;
  }

  private seleccionar(i: number) {
    this.opcionSel = i;
    this.opcionesLista.forEach((o, j) => o.fondo.setFillStyle(j === i ? COLOR.rojo3 : COLOR.gris2, 0.95));
  }

  private moverSeleccion(d: number) {
    if (!this.opciones.visible || !this.opcionesLista.length) return;
    this.seleccionar((this.opcionSel + d + this.opcionesLista.length) % this.opcionesLista.length);
  }

  private elegir(i: number) {
    if (!this.opciones.visible || this.time.now < this.bloqueoHasta) return;
    const o = this.opcionesLista[i];
    if (!o) return;
    narrativa.choose(o.choice.index);
    this.opciones.setVisible(false).removeAll(true);
    this.opcionesLista = [];
    this.avanzar();
  }

  // ------------------------------------------------------------------ foco, joystick, inventario
  private mostrarFoco(info: FocoInfo | null) {
    if (!info || this.activo) { this.foco.setVisible(false); return; }
    // con el ratón encima, el clic; si no, las teclas del que está al lado
    const acciones = this.esTactil && !info.raton ? '' : info.raton
      ? [info.usar ? `clic: ${info.hablar ? 'hablar' : 'usar'}` : '', info.mirar ? `${info.usar ? 'clic dcho.' : 'clic'}: mirar` : ''].filter(Boolean).join(' · ')
      : [info.usar ? (info.hablar ? 'E hablar' : 'E usar') : '', info.mirar ? 'Q mirar' : ''].filter(Boolean).join(' · ');
    this.focoTexto.setText(`${info.nombre}${acciones ? '   ' + acciones : ''}`);
    const fondo = this.foco.getData('fondo') as Phaser.GameObjects.Rectangle;
    fondo.setSize(this.focoTexto.width + 20, Math.round(24 * escala()));
    // a la derecha está la columna de botones (OBJ., REG., MENÚ): la etiqueta no se mete debajo
    const derecha = info.y < 270 ? 860 : 960;
    const x = Phaser.Math.Clamp(info.x, fondo.width / 2 + 4, derecha - fondo.width / 2 - 4);
    this.foco.setPosition(x, Phaser.Math.Clamp(info.y - 4, 30, 520)).setVisible(true);
  }

  private dibujarJoystick() {
    const g = this.joystick.clear();
    if (!tactil.activo) return;
    const { x: ox, y: oy } = tactil.origen;   // ya en coordenadas internas (960x540)
    g.fillStyle(COLOR.gris1, 0.35).fillCircle(ox, oy, 48).lineStyle(2, COLOR.papel3, 0.5).strokeCircle(ox, oy, 48);
    g.fillStyle(COLOR.papel3, 0.6).fillCircle(ox + tactil.x * 40, oy + tactil.y * 40, 18);
  }

  private alternarInventario() {
    const abrir = !this.inventario.visible && !this.activo;
    this.inventario.removeAll(true).setVisible(abrir);
    if (!abrir) return;
    const items = narrativa.list('inventario');
    const c = this.inventario;
    if (mano.item) this.soltarObjeto();
    this.inventarioAbiertoEn = this.time.now;
    // el mismo toque que abre el panel no debe cerrarlo al soltarse
    c.add(this.add.rectangle(0, 0, 960, 540, 0x000000, 0.6).setOrigin(0).setInteractive()
      .on('pointerup', () => { if (this.time.now - this.inventarioAbiertoEn > 300) this.alternarInventario(); }));
    c.add(this.add.rectangle(480, 270, 680, 380, 0x2e221b).setStrokeStyle(3, 0x1a1411));
    c.add(this.add.text(480, 104, 'OBJETOS', { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4) }).setOrigin(0.5));
    const desc = this.add.text(480, 370, items.length ? 'Toca un objeto.' : 'No llevas nada.', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3), align: 'center', wordWrap: { width: 580 },
    }).setOrigin(0.5);
    c.add(desc);
    // acciones sobre el objeto elegido: mirarlo o cogerlo para usarlo con algo del escenario
    let elegido: string | null = null;
    const accion = (x: number, etiqueta: string, alPulsar: () => void) => {
      const fondo = this.add.rectangle(x, 422, 170, 36, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      const t = this.add.text(x, 422, etiqueta, { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.papel4) }).setOrigin(0.5);
      fondo.on('pointerover', () => fondo.setFillStyle(COLOR.rojo3));
      fondo.on('pointerout', () => fondo.setFillStyle(COLOR.gris2));
      fondo.on('pointerup', () => { if (elegido) alPulsar(); });
      const b = this.add.container(0, 0, [fondo, t]).setVisible(false);
      c.add(b);
      return b;
    };
    const mirar = accion(390, 'MIRAR', () => {
      const ruta = ITEMS[elegido!]?.mirar;
      if (ruta && narrativa.hasPath(ruta)) { this.alternarInventario(); this.game.events.emit(EV.dialogoIniciar, ruta); }
    });
    const usar = accion(570, 'USAR CON…', () => {
      mano.item = elegido;
      this.alternarInventario();
      this.game.events.emit(EV.mano);   // redibuja el indicador (aquí) y el cono de la telepantalla (en el escenario)
    });
    const marcos: Phaser.GameObjects.Rectangle[] = [];
    items.forEach((id, i) => {
      const item = ITEMS[id];
      // hasta seis por fila
      const fila = Math.floor(i / 6), enFila = Math.min(6, items.length - fila * 6), col = i % 6;
      const x = 480 - (enFila - 1) * 50 + col * 100, y = 182 + fila * 96;
      const casilla = this.add.rectangle(x, y, 84, 84, 0x1a1411).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      marcos.push(casilla);
      c.add(casilla);
      if (item && this.textures.exists(item.icono)) c.add(this.add.image(x, y, item.icono).setScale(3.5));
      casilla.on('pointerup', () => {
        elegido = id;
        marcos.forEach((m) => m.setStrokeStyle(2, m === casilla ? COLOR.rojo4 : COLOR.gris3));
        desc.setText(item ? `${item.nombre}\n${item.descripcion}` : id);
        mirar.setVisible(!!item?.mirar);
        usar.setVisible(true).setX(item?.mirar ? 0 : -90);
      });
    });
  }

  /** Abre el registro de diálogos para consultarlo (fuera de los diálogos). */
  private abrirRegistro() {
    if (this.activo || this.enAccion || this.consultando) return;
    if (this.inventario.visible) this.alternarInventario();
    this.consultando = true;
    this.foco.setVisible(false);
    this.game.events.emit(EV.pausa, true);
    void this.lanzarMinijuego('Registro', {}).then(() => {
      this.consultando = false;
      this.game.events.emit(EV.pausa, false);
    });
  }

  /** Un objeto nuevo en el inventario: aviso breve arriba. */
  private avisarObjeto(id: string) {
    const item = ITEMS[id];
    if (!item) return;
    // si ya hay un aviso a la vista, este espera su turno
    if (this.aviso.visible) { this.avisosPendientes.push(id); return; }
    const a = this.aviso.removeAll(true).setVisible(true).setAlpha(0).setY(-20);
    a.add(this.add.rectangle(480, 164, 360, 58, COLOR.gris1, 0.92).setStrokeStyle(2, COLOR.ocre4));
    if (this.textures.exists(item.icono)) a.add(this.add.image(334, 164, item.icono).setScale(2.5));
    a.add(this.add.text(372, 150, item.nombre.toUpperCase(), { fontFamily: FUENTE.maquina, fontSize: '22px', color: hex(COLOR.ocre4) }));
    a.add(this.add.text(372, 172, 'en el inventario', { fontFamily: FUENTE.texto, fontSize: '15px', color: hex(COLOR.papel3) }));
    this.tweens.add({ targets: a, alpha: 1, y: 0, duration: 300 });
    this.tweens.add({
      targets: a, alpha: 0, delay: 2600, duration: 400,
      onComplete: () => { a.setVisible(false); const sig = this.avisosPendientes.shift(); if (sig) this.avisarObjeto(sig); },
    });
  }

  /** Indicador del objeto en la mano (arriba a la izquierda), con un aspa para soltarlo. */
  private dibujarMano() {
    const c = this.enMano.removeAll(true);
    const item = mano.item ? ITEMS[mano.item] : null;
    if (!item) { c.setVisible(false); return; }
    const texto = this.add.text(70, 30, `${item.nombre} · ${this.esTactil ? 'toca' : 'elige'} dónde usarlo`, {
      fontFamily: FUENTE.texto, fontSize: '17px', color: hex(COLOR.papel4),
    }).setOrigin(0, 0.5);
    const ancho = texto.width + 110;
    c.add(this.add.rectangle(16, 30, ancho, 40, COLOR.gris1, 0.9).setOrigin(0, 0.5).setStrokeStyle(2, COLOR.ocre4));
    if (this.textures.exists(item.icono)) c.add(this.add.image(42, 30, item.icono).setScale(2));
    c.add(texto);
    const x = this.add.text(16 + ancho - 22, 30, '✕', { fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel3) })
      .setOrigin(0.5).setInteractive({ useHandCursor: true });
    x.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); this.soltarObjeto(); });
    c.add(x);
  }

  private soltarObjeto() {
    mano.item = null;
    this.game.events.emit(EV.mano);
  }

  /**
   * Qué es el ojo: al pasar el ratón o al tocarlo, una línea que lo explica y dice cómo está ahora
   * (sin números: la Sospecha no se ve, se intuye).
   */
  private crearAyudaOjo() {
    const ayuda = this.add.text(892, 30, '', {
      fontFamily: FUENTE.texto, fontSize: '16px', color: hex(COLOR.papel4), backgroundColor: '#16181cee',
      padding: { x: 8, y: 5 }, align: 'right', lineSpacing: 2,
    }).setOrigin(1, 0.5).setDepth(46).setVisible(false);
    const texto = () => {
      const s = Number(narrativa.get('sospecha')) || 0;
      const ahora = s < 25 ? 'Ahora nadie se fija en ti.' : s < 50 ? 'Alguien ha tomado nota.' : s < 75 ? 'Te vigilan.' : 'Están a punto de venir a por ti.';
      return `El ojo del Partido: se abre a medida que sube la Sospecha.\n${ahora}`;
    };
    let ocultar: Phaser.Time.TimerEvent | null = null;
    const mostrar = (ms: number) => {
      ayuda.setText(texto()).setVisible(true);
      ocultar?.remove();
      ocultar = ms ? this.time.delayedCall(ms, () => ayuda.setVisible(false)) : null;
    };
    const zona = this.add.circle(920, 30, 22, 0x000000, 0.001).setDepth(21).setInteractive({ useHandCursor: true });
    zona.on('pointerover', (p: Phaser.Input.Pointer) => { if (!p.wasTouch) mostrar(0); });
    zona.on('pointerout', (p: Phaser.Input.Pointer) => { if (!p.wasTouch) ayuda.setVisible(false); });
    zona.on('pointerdown', (p: Phaser.Input.Pointer) => { this.registry.set('uiCapturo', p.downTime); mostrar(3500); });
  }

  /** El ojo se abre a medida que sube la Sospecha (biblia visual §8). */
  private dibujarOjo(sospecha: number) {
    const g = this.ojo, cx = 920, cy = 30, w = 22;
    const apertura = Phaser.Math.Clamp(sospecha / 100, 0, 1);
    g.clear();
    g.fillStyle(COLOR.gris1, 0.8).fillCircle(cx, cy, 20);
    if (apertura < 0.05) {
      g.lineStyle(2, COLOR.papel3).lineBetween(cx - w / 2, cy, cx + w / 2, cy);
      return;
    }
    const h = 2 + apertura * 12;
    g.fillStyle(COLOR.papel4).fillEllipse(cx, cy, w, h);
    g.fillStyle(apertura > 0.75 ? COLOR.rojo4 : COLOR.tele4).fillCircle(cx, cy, Math.min(5, h / 2));
    g.fillStyle(COLOR.negro).fillCircle(cx, cy, Math.min(2, h / 3));
    if (apertura > 0.75) {
      g.lineStyle(1, COLOR.rojo4).lineBetween(cx - 10, cy - 1, cx - 6, cy).lineBetween(cx + 6, cy + 1, cx + 10, cy);
    }
  }

  private alternarDepuracion() {
    this.depurando = !this.depurando;
    this.depuracion.setVisible(this.depurando);
    this.game.events.emit(EV.depurar, this.depurando);
  }
}
