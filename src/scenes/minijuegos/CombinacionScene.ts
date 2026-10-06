/**
 * El cerrojo de combinación del Archivo Restringido (guion J8.04): cuatro ruedas numeradas.
 * Grabado en la placa: «Código: última rectificación vigente». Tres intentos fallidos y el protagonista
 * se aparta a pensar (ink le da una pista). Si lleva la directiva de la mañana, puede releerla aquí.
 *   # minijuego:combinacion,codigo=0305,doc=directiva_j8,item=directiva,resultado=cerrojo_j8
 *   → "abierta" | "fallo" | "tiempo"
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { mision, hora, narrativa } from '../../core/juego';
import { lineas } from '../../core/texto';
import type { Documento } from './DocumentoScene';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

const DOCS = import.meta.glob('../../../content/documentos/*.json', { eager: true, import: 'default' }) as Record<string, Documento>;
const docDe = (id: string) => Object.entries(DOCS).find(([ruta]) => ruta.endsWith(`/${id}.json`))?.[1];
const INTENTOS = 3;

export class CombinacionScene extends Minijuego {
  private ruedas = [0, 0, 0, 0];
  private textos: Phaser.GameObjects.Text[] = [];
  private marcos: Phaser.GameObjects.Rectangle[] = [];
  private sel = 0;
  private fallos = 0;
  private hecho = false;
  private reloj!: Phaser.GameObjects.Text;
  private nota: Phaser.GameObjects.Container | null = null;

  constructor() { super('Combinacion'); }

  create() {
    const { width, height } = this.scale;
    this.ruedas = [0, 0, 0, 0]; this.textos = []; this.marcos = []; this.sel = 0; this.fallos = 0; this.hecho = false; this.nota = null;
    this.cameras.main.fadeIn(250, 11, 12, 15);
    this.add.rectangle(0, 0, width, height, 0x0d0f12).setOrigin(0);
    this.add.rectangle(width / 2, 260, 560, 360, 0x5c6066).setStrokeStyle(4, 0x2a2c30);
    for (const [x, y] of [[220, 100], [740, 100], [220, 420], [740, 420]]) this.add.circle(x, y, 7, 0x3a3c40);
    this.add.text(width / 2, 116, 'ARCHIVO RESTRINGIDO', { fontFamily: FUENTE.maquina, fontSize: '28px', color: '#1d1f22' }).setOrigin(0.5);
    this.add.text(width / 2, 380, 'Código: última rectificación vigente', { fontFamily: FUENTE.maquina, fontSize: '22px', color: '#2a2c30' }).setOrigin(0.5);
    this.reloj = this.add.text(width / 2, 20, '', { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.papel4) }).setOrigin(0.5, 0);

    for (let i = 0; i < 4; i++) {
      const x = width / 2 - 165 + i * 110;
      this.marcos.push(this.add.rectangle(x, 250, 80, 110, 0x1d1f22).setStrokeStyle(3, 0x2a2c30));
      this.textos.push(this.add.text(x, 250, '0', { fontFamily: FUENTE.maquina, fontSize: '72px', color: hex(COLOR.papel4) }).setOrigin(0.5));
      const arriba = this.add.text(x, 172, '▲', { fontFamily: FUENTE.texto, fontSize: '28px', color: hex(COLOR.papel3) }).setOrigin(0.5).setInteractive({ useHandCursor: true });
      const abajo = this.add.text(x, 330, '▼', { fontFamily: FUENTE.texto, fontSize: '28px', color: hex(COLOR.papel3) }).setOrigin(0.5).setInteractive({ useHandCursor: true });
      arriba.on('pointerup', () => { this.sel = i; this.girar(1); });
      abajo.on('pointerup', () => { this.sel = i; this.girar(-1); });
      this.marcos[i].setInteractive().on('pointerup', () => { this.sel = i; this.girar(1); });
    }
    this.boton(width / 2 - 120, height - 50, 'PROBAR', () => this.probar());
    const item = this.params.item, doc = this.params.doc;
    if (doc && (!item || narrativa.list('inventario').includes(item))) this.boton(width / 2 + 120, height - 50, 'DOCUMENTOS', () => this.documentos(doc));
    this.marcar();

    const kb = this.input.keyboard!;
    kb.on('keydown-LEFT', () => { this.sel = (this.sel + 3) % 4; this.marcar(); });
    kb.on('keydown-RIGHT', () => { this.sel = (this.sel + 1) % 4; this.marcar(); });
    kb.on('keydown-UP', () => this.girar(1));
    kb.on('keydown-DOWN', () => this.girar(-1));
    kb.on('keydown-ENTER', () => this.probar());
    kb.on('keydown', (e: KeyboardEvent) => {
      if (/^\d$/.test(e.key)) { this.ruedas[this.sel] = Number(e.key); this.textos[this.sel].setText(e.key); this.sel = (this.sel + 1) % 4; this.marcar(); audio.play('tecla'); }
    });
  }

  private boton(x: number, y: number, texto: string, alPulsar: () => void) {
    const f = this.add.rectangle(x, y, 200, 44, COLOR.gris2).setStrokeStyle(2, COLOR.gris3).setInteractive({ useHandCursor: true });
    this.add.text(x, y, texto, { fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.papel4) }).setOrigin(0.5);
    f.on('pointerup', alPulsar);
  }

  private marcar() { this.marcos.forEach((m, i) => m.setStrokeStyle(3, i === this.sel ? COLOR.ocre4 : 0x2a2c30)); }

  private girar(d: number) {
    if (this.hecho || this.nota) return;
    this.ruedas[this.sel] = (this.ruedas[this.sel] + d + 10) % 10;
    this.textos[this.sel].setText(String(this.ruedas[this.sel]));
    this.marcar();
    audio.play('tecla');
  }

  private probar() {
    if (this.hecho || this.nota) return;
    if (this.ruedas.join('') === (this.params.codigo ?? '0000')) {
      this.hecho = true;
      audio.play('sello');
      this.marcos.forEach((m) => m.setStrokeStyle(3, COLOR.tele5));
      this.time.delayedCall(700, () => this.terminar({ resultado: 'abierta' }));
      return;
    }
    this.fallos++;
    audio.play('fallo');
    this.cameras.main.shake(150, 0.004);
    if (this.fallos >= INTENTOS) { this.hecho = true; this.time.delayedCall(500, () => this.terminar({ resultado: 'fallo' })); }
  }

  /** Lo que se leyó esta mañana, de memoria (o del bolsillo). */
  private documentos(id: string) {
    if (this.nota) { this.nota.destroy(); this.nota = null; return; }
    const d = docDe(id);
    if (!d) return;
    const texto = [...lineas(d.cabecera), '', ...lineas(d.lineas), '', ...lineas(d.pie)].join('\n');
    const t = this.add.text(480, 270, texto, { fontFamily: FUENTE.maquina, fontSize: '24px', color: '#22252a', align: 'left', lineSpacing: 4 }).setOrigin(0.5);
    const fondo = this.add.rectangle(480, 270, t.width + 60, t.height + 50, COLOR.papel4).setStrokeStyle(2, 0x8f8a7a);
    this.nota = this.add.container(0, 0, [fondo, t]).setDepth(10);
    fondo.setInteractive().on('pointerup', () => { this.nota?.destroy(); this.nota = null; });
    audio.play('papel');
  }

  update(_t: number, dt: number) {
    const r = mision.reloj;
    if (!r) return this.reloj.setText('');
    if (!this.hecho) r.transcurrido += dt / 1000;
    this.reloj.setText(hora(r.inicio + r.transcurrido)).setColor(hex(r.limite - r.transcurrido < 30 ? COLOR.rojo4 : COLOR.papel4));
    if (!this.hecho && r.transcurrido >= r.limite) { this.hecho = true; this.terminar({ resultado: 'tiempo' }); }
  }
}
