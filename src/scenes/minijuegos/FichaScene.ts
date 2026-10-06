/** P.03 — Ficha de Afiliación del Partido: creación del personaje como formulario oficial. */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const P = { x: 170, y: 14, w: 620, h: 512 };
const TINTA = hex(COLOR.gris2);
const ROJO = hex(COLOR.rojo3);
const TIEMPO_FIRMA = 1300;

export class FichaScene extends Minijuego {
  private nombre = '';
  private apellido = '';
  private genero: 'm' | 'f' | null = null;
  private digitos = String(Phaser.Math.Between(1000, 9999));
  private textoNum!: Phaser.GameObjects.Text;
  private textoIvy!: Phaser.GameObjects.Text;
  private botonesSexo: { g: 'm' | 'f'; fondo: Phaser.GameObjects.Rectangle }[] = [];
  private firma!: Phaser.GameObjects.Graphics;
  private zonaFirma!: Phaser.GameObjects.Rectangle;
  private avisoFirma!: Phaser.GameObjects.Text;
  private firmando: { inicio: number } | null = null;
  private firmado = false;

  constructor() { super('Ficha'); }

  preload() {
    this.load.image('ficha-fondo', 'assets/minijuegos/ficha-fondo.png');
  }

  create() {
    this.nombre = ''; this.apellido = ''; this.genero = null; this.firmado = false; this.firmando = null;
    this.botonesSexo = [];
    const { width, height } = this.scale;
    this.cameras.main.fadeIn(500, 11, 12, 15);
    // la mesa de acero, la ficha impresa (membrete, marco, renglones, foto, sello) y el tubo: arte en ficha-fondo
    this.add.rectangle(width / 2, height / 2, width, height, COLOR.negro);
    this.add.image(0, 0, 'ficha-fondo').setOrigin(0).setScale(2);

    const txt = (x: number, y: number, s: string, size = 22, color = TINTA) =>
      this.add.text(P.x + x, P.y + y, s, { fontFamily: FUENTE.maquina, fontSize: `${size}px`, color });

    txt(P.w / 2, 26, 'FICHA DE AFILIACIÓN', 34).setOrigin(0.5, 0);
    txt(P.w / 2, 60, 'PARTIDO EXTERIOR — INGSOC', 20, ROJO).setOrigin(0.5, 0);

    const fila = (y: number, etiqueta: string) => txt(36, y, etiqueta.toUpperCase(), 20);
    fila(108, 'Nombre');
    this.campo(200, 104, (v) => { this.nombre = v; this.actualizar(); });
    fila(146, 'Apellido');
    this.campo(200, 142, (v) => { this.apellido = v; this.actualizar(); });
    fila(186, 'Sexo');
    (['m', 'f'] as const).forEach((g, i) => {
      const x = P.x + 250 + i * 140, y = P.y + 196;
      const fondo = this.add.rectangle(x, y, 120, 30, 0xd8d2bd).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
      this.add.text(x, y, g === 'm' ? 'VARÓN' : 'MUJER', { fontFamily: FUENTE.maquina, fontSize: '22px', color: TINTA }).setOrigin(0.5);
      fondo.on('pointerup', () => { this.genero = g; audio.play('tecla'); this.actualizar(); });
      this.botonesSexo.push({ g, fondo });
    });
    fila(226, 'Edad');
    txt(200, 226, '34');
    fila(256, 'Número de afiliado');
    this.textoNum = txt(300, 256, '');
    fila(288, 'Destino');
    txt(200, 288, 'MINISTERIO DE LA PAZ', 20);
    txt(200, 308, 'DPTO. DE PARTES Y CARTOGRAFÍA DEL FRENTE', 18);
    this.sello(P.x + 520, P.y + 300, 'ASIGNADO', 16, -8);
    fila(340, 'Familiares');
    this.textoIvy = txt(200, 340, '');
    this.sello(P.x + 470, P.y + 352, 'MÁRTIR · CALLE STEPNEY · 1979', 16, -4);
    fila(380, '¿Familiares en crimental?');
    txt(360, 380, 'NO');
    this.sello(P.x + 450, P.y + 390, 'VERIFICADO', 14, 6);

    txt(P.w / 2, 418, 'Juro lealtad absoluta al Gran Hermano, al Partido', 20).setOrigin(0.5, 0);
    txt(P.w / 2, 438, 'y a los principios sagrados del Ingsoc.', 20).setOrigin(0.5, 0);

    // línea de firma: mantener pulsado
    this.zonaFirma = this.add.rectangle(P.x + P.w / 2, P.y + 478, 380, 44, 0x000000, 0.001).setInteractive({ useHandCursor: true });
    this.firma = this.add.graphics();
    this.avisoFirma = txt(P.w / 2, 494, 'MANTÉN PULSADO PARA FIRMAR', 16, ROJO).setOrigin(0.5, 0);
    this.zonaFirma.on('pointerdown', () => this.empezarFirma());
    this.input.on('pointerup', () => this.soltarFirma());
    this.input.keyboard?.on('keydown-ENTER', () => this.empezarFirma());
    this.input.keyboard?.on('keyup-ENTER', () => this.soltarFirma());

    this.actualizar();
  }

  private campo(x: number, y: number, alCambiar: (v: string) => void) {
    const el = document.createElement('input');
    el.type = 'text';
    el.maxLength = 14;
    el.autocomplete = 'off';
    el.spellcheck = false;
    el.setAttribute('autocapitalize', 'words');
    Object.assign(el.style, {
      width: '300px', font: '24px "VT323", monospace', color: TINTA, background: 'transparent',
      border: 'none', borderBottom: `2px solid ${hex(COLOR.gris3)}`, outline: 'none', padding: '0 4px',
    });
    el.addEventListener('input', () => {
      el.value = el.value.replace(/[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]/g, '');
      audio.play('tecla');
      const v = el.value.trim();
      alCambiar(v ? v[0].toUpperCase() + v.slice(1) : '');
    });
    el.addEventListener('keydown', (e) => e.stopPropagation());   // que WASD no mueva nada
    this.add.dom(P.x + x, P.y + y, el).setOrigin(0);
  }

  private sello(x: number, y: number, texto: string, size: number, angulo: number) {
    const t = this.add.text(x, y, texto, { fontFamily: FUENTE.maquina, fontSize: `${size}px`, color: ROJO }).setOrigin(0.5).setAngle(angulo);
    const r = this.add.rectangle(x, y, t.width + 12, t.height + 4).setStrokeStyle(2, COLOR.rojo3).setAngle(angulo);
    t.setAlpha(0.85); r.setAlpha(0.85);
  }

  private num() {
    const inicial = (this.apellido[0] ?? 'X').toUpperCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    return `${this.digitos} 0${inicial}`;
  }

  private listo() { return !!(this.nombre && this.apellido && this.genero); }

  private actualizar() {
    this.textoNum.setText(this.apellido ? this.num() : '—');
    this.textoIvy.setText(`IVY ${this.apellido.toUpperCase() || '______'}`);
    this.botonesSexo.forEach(({ g, fondo }) => fondo.setFillStyle(g === this.genero ? 0xeeead9 : 0xd8d2bd)
      .setStrokeStyle(2, g === this.genero ? COLOR.rojo3 : COLOR.gris3));
    this.avisoFirma.setText(this.listo() ? 'MANTÉN PULSADO PARA FIRMAR' : 'COMPLETE TODOS LOS CAMPOS');
  }

  private empezarFirma() {
    if (this.firmado) return;
    if (!this.listo()) { this.cameras.main.shake(120, 0.004); audio.play('fallo'); return; }
    this.firmando = { inicio: this.time.now };
  }

  private soltarFirma() {
    if (this.firmando && !this.firmado) { this.firmando = null; this.firma.clear(); }
  }

  update() {
    if (!this.firmando || this.firmado) return;
    const t = Math.min(1, (this.time.now - this.firmando.inicio) / TIEMPO_FIRMA);
    this.dibujarFirma(t);
    if (Math.random() < 0.3) audio.play('plumilla');
    if (t >= 1) this.firmar();
  }

  /** Una rúbrica procedural que avanza con el tiempo de pulsación. */
  private dibujarFirma(t: number) {
    const g = this.firma.clear().lineStyle(2, 0x1d2a44, 1);
    const x0 = P.x + P.w / 2 - 150, y0 = P.y + 484;
    const pasos = Math.floor(120 * t);
    g.beginPath();
    for (let i = 0; i <= pasos; i++) {
      const u = i / 120;
      const x = x0 + u * 300;
      const y = y0 + Math.sin(u * 26) * 8 * (1 - u * 0.5) - Math.sin(u * 7) * 6;
      if (i === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
    g.strokePath();
  }

  private firmar() {
    this.firmado = true;
    this.firmando = null;
    this.children.list.filter((o) => o instanceof Phaser.GameObjects.DOMElement)
      .forEach((o) => ((o as Phaser.GameObjects.DOMElement).node as HTMLInputElement).blur());
    const apto = this.add.text(P.x + P.w - 150, P.y + 150, 'APTO', {
      fontFamily: FUENTE.maquina, fontSize: '84px', color: ROJO,
    }).setOrigin(0.5).setAngle(-14).setScale(3).setAlpha(0);
    const marco = this.add.rectangle(apto.x, apto.y, 190, 90).setStrokeStyle(5, COLOR.rojo3).setAngle(-14).setScale(3).setAlpha(0);
    this.tweens.add({
      targets: [apto, marco], scale: 1, alpha: 0.9, duration: 220, ease: 'Quad.easeIn',
      onComplete: () => {
        audio.play('sello');
        this.cameras.main.shake(160, 0.006);
        this.time.delayedCall(1100, () => {
          audio.play('tubo');
          this.tweens.add({ targets: this.cameras.main, scrollY: -560, duration: 700, ease: 'Cubic.easeIn' });
          this.time.delayedCall(500, () => this.terminar({
            resultado: 'firmada',
            datos: { nombre: this.nombre, apellido: this.apellido, genero: this.genero!, num: this.num() },
          }, 400));
        });
      },
    });
  }
}
