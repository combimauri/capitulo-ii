/**
 * Crimen facial (diseño técnico §6.2, biblia visual §6.2).
 * Microjuego de ritmo: llegan marcas con una expresión; hay que acertarlas al compás.
 * Etiqueta de ink:  # cf:id=CF-J1-GIMNASIA,expr=entusiasmo,dif=facil,coro=¡Uno!/¡Dos!,tutorial=si
 * Varias fases:     # cf:id=CF-J2-ODIO,fases=odio:12/duelo:6,dif=media
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

export const EXPRESIONES = ['entusiasmo', 'odio', 'jubilo', 'desprecio', 'duelo'] as const;
type Expr = typeof EXPRESIONES[number];

const NOMBRE: Record<Expr, string> = {
  entusiasmo: 'ENTUSIASMO', odio: 'ODIO', jubilo: 'JÚBILO', desprecio: 'DESPRECIO', duelo: 'DUELO',
};
const COLOR_EXPR: Record<Expr, number> = {
  entusiasmo: 0xe0bf68, odio: 0xc8382f, jubilo: 0x7fc496, desprecio: 0x828c97, duelo: 0x5470a0,
};
const DIFICULTAD = {
  facil: { bpm: 72, ventana: 190, golpes: 12 },
  media: { bpm: 96, ventana: 140, golpes: 16 },
  dificil: { bpm: 120, ventana: 100, golpes: 20 },
} as const;

const PISTA = { y: 470, xGolpe: 210, xInicio: 900 };
const ANTICIPACION = 2400;   // ms que tarda una marca en cruzar la pista

interface Marca { t: number; expr: Expr; obj: Phaser.GameObjects.Container; resuelta: boolean }

export class FacecrimeScene extends Minijuego {
  private marcas: Marca[] = [];
  private inicio = 0;
  private aciertos = 0;
  private grietas = 0;
  private ventana = 150;
  private retrato!: Phaser.GameObjects.Image;
  private genero = 'h';
  private exprActual: Expr = 'entusiasmo';
  private coro: string[] = [];
  private textoCoro!: Phaser.GameObjects.Text;
  private exprs: Expr[] = [];
  private empezado = false;
  private fin = 0;

  constructor() { super('Facecrime'); }

  create() {
    const { width, height } = this.scale;
    this.marcas = []; this.aciertos = 0; this.grietas = 0; this.empezado = false;
    this.genero = narrativa.get('genero') === 'f' ? 'm' : 'h';
    const dif = DIFICULTAD[(this.params.dif as keyof typeof DIFICULTAD) ?? 'facil'] ?? DIFICULTAD.facil;
    this.ventana = dif.ventana;

    const fases = (this.params.fases ?? `${this.params.expr ?? 'entusiasmo'}:${dif.golpes}`)
      .split('/').map((f) => { const [e, n] = f.split(':'); return { expr: e as Expr, n: Number(n) || dif.golpes }; });
    this.exprs = [...new Set(fases.map((f) => f.expr))];
    this.exprActual = fases[0].expr;
    this.coro = (this.params.coro ?? '').split('/').filter(Boolean);

    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(width / 2, height / 2, width, height, COLOR.tele0);
    for (let y = 0; y < height; y += 3) this.add.rectangle(width / 2, y, width, 1, 0x000000, 0.25);

    // retrato del protagonista (96x96 a x3)
    this.add.rectangle(width / 2, 214, 300, 300, COLOR.tele1).setStrokeStyle(3, COLOR.tele4);
    this.retrato = this.add.image(width / 2, 214, this.claveRetrato('neutral')).setScale(3);
    this.add.text(width / 2, 30, 'LA TELEPANTALLA TE ESTÁ MIRANDO', {
      fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.tele5),
    }).setOrigin(0.5);
    this.textoCoro = this.add.text(width / 2, 382, '', {
      fontFamily: FUENTE.maquina, fontSize: '34px', color: hex(COLOR.papel4),
    }).setOrigin(0.5);

    // pista de ritmo
    this.add.rectangle(width / 2, PISTA.y, width - 80, 54, 0x000000, 0.45).setStrokeStyle(1, COLOR.tele1);
    this.add.circle(PISTA.xGolpe, PISTA.y, 26).setStrokeStyle(3, COLOR.papel4);

    // marcas programadas a partir de las fases
    const intervalo = 60000 / dif.bpm;
    let t = 1800;
    for (const f of fases) for (let i = 0; i < f.n; i++, t += intervalo) this.marcas.push({ t, expr: f.expr, obj: this.crearMarca(f.expr), resuelta: false });
    this.fin = t + 600;

    this.crearControles();
    if (this.params.tutorial === 'si') this.tutorial(); else this.empezar();
  }

  private claveRetrato(e: string) { return `retrato-prot_${this.genero}_${e}`; }

  private crearMarca(e: Expr) {
    const c = this.add.container(-100, PISTA.y);
    c.add(this.add.circle(0, 0, 20, COLOR_EXPR[e]).setStrokeStyle(2, 0x000000));
    if (this.exprs.length > 1) {
      c.add(this.add.text(0, 0, String(this.exprs.indexOf(e) + 1), { fontFamily: FUENTE.maquina, fontSize: '26px', color: '#000' }).setOrigin(0.5));
    }
    return c;
  }

  private crearControles() {
    const { width } = this.scale;
    const unica = this.exprs.length === 1;
    this.exprs.forEach((e, i) => {
      const w = unica ? 300 : 150, x = unica ? width - 190 : width - 100 - (this.exprs.length - 1 - i) * 160;
      const boton = this.add.rectangle(x, 400, w, 44, COLOR_EXPR[e], 0.9).setStrokeStyle(2, 0x000000)
        .setInteractive({ useHandCursor: true });
      this.add.text(x, 400, `${unica ? 'ESPACIO · ' : `${i + 1} · `}${NOMBRE[e]}`, {
        fontFamily: FUENTE.maquina, fontSize: '22px', color: '#000',
      }).setOrigin(0.5);
      boton.on('pointerdown', () => this.pulsar(e));
    });
    const kb = this.input.keyboard!;
    kb.on('keydown', (ev: KeyboardEvent) => {
      if (ev.code === 'Space' || ev.code === 'Enter') return this.pulsar(unica ? this.exprs[0] : this.exprActual);
      const n = Number(ev.key);
      if (n >= 1 && n <= this.exprs.length) this.pulsar(this.exprs[n - 1]);
    });
    if (unica) this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { if (p.y < 380) this.pulsar(this.exprs[0]); });
  }

  private tutorial() {
    const { width, height } = this.scale;
    const capa = this.add.container(0, 0).setDepth(20);
    capa.add(this.add.rectangle(width / 2, height / 2, width, height, 0x000000, 0.8));
    capa.add(this.add.text(width / 2, height / 2 - 40, [
      'La telepantalla te ve. Tu cara también habla.',
      'Mantén la expresión correcta.',
      '',
      this.exprs.length === 1 ? 'Pulsa ESPACIO o toca la pantalla cuando cada marca llegue al círculo.'
        : 'Pulsa la tecla o el botón de la expresión cuando su marca llegue al círculo.',
    ].join('\n'), { fontFamily: FUENTE.texto, fontSize: '22px', color: hex(COLOR.papel4), align: 'center', lineSpacing: 6 }).setOrigin(0.5));
    capa.add(this.add.text(width / 2, height / 2 + 90, '[ toca para empezar ]', {
      fontFamily: FUENTE.maquina, fontSize: '24px', color: hex(COLOR.tele5),
    }).setOrigin(0.5));
    const empezar = () => { capa.destroy(); this.empezar(); };
    this.time.delayedCall(400, () => {
      this.input.once('pointerdown', empezar);
      this.input.keyboard?.once('keydown', empezar);
    });
  }

  private empezar() {
    // El reloj de una escena relanzada conserva su último valor hasta el primer fotograma:
    // el inicio real se fija en el primer update().
    this.inicio = -1;
    this.empezado = true;
    this.retrato.setTexture(this.claveRetrato(this.exprActual));
  }

  update() {
    if (!this.empezado) return;
    if (this.inicio < 0) this.inicio = this.time.now;
    const ahora = this.time.now - this.inicio;
    const proxima = this.marcas.find((m) => !m.resuelta);
    if (proxima && proxima.expr !== this.exprActual && proxima.t - ahora < 900) this.exprActual = proxima.expr;

    for (const m of this.marcas) {
      const falta = m.t - ahora;
      if (!m.resuelta) {
        m.obj.x = PISTA.xGolpe + (falta / ANTICIPACION) * (PISTA.xInicio - PISTA.xGolpe);
        m.obj.setVisible(falta < ANTICIPACION);
        if (falta < -this.ventana) this.fallo(m);
      }
    }
    if (ahora > this.fin && this.marcas.every((m) => m.resuelta)) this.acabar();
  }

  private pulsar(e: Expr) {
    if (!this.empezado || this.inicio < 0) return;
    const ahora = this.time.now - this.inicio;
    const m = this.marcas.find((x) => !x.resuelta && Math.abs(x.t - ahora) <= this.ventana);
    if (!m) return;   // pulsar fuera de tiempo no penaliza: la cara se mantiene
    if (m.expr !== e) return this.fallo(m);
    m.resuelta = true;
    this.aciertos++;
    audio.play('acierto');
    this.retrato.setTexture(this.claveRetrato(m.expr));
    this.tweens.add({ targets: m.obj, scale: 1.8, alpha: 0, duration: 200, onComplete: () => m.obj.destroy() });
    if (this.coro.length) this.textoCoro.setText(this.coro[(this.aciertos - 1) % this.coro.length]);
  }

  private fallo(m: Marca) {
    m.resuelta = true;
    this.grietas++;
    audio.play('fallo');
    m.obj.destroy();
    this.cameras.main.shake(120, 0.005);
    this.retrato.setTexture(this.claveRetrato(`${this.exprActual}_grieta`));
    this.time.delayedCall(350, () => { if (this.scene.isActive()) this.retrato.setTexture(this.claveRetrato(this.exprActual)); });
  }

  private acabar() {
    if (!this.empezado) return;
    this.empezado = false;
    const total = this.marcas.length;
    const ratio = total ? this.aciertos / total : 1;
    const resultado = ratio >= 0.9 ? 'perfecto' : ratio >= 0.6 ? 'aceptable' : 'fallo';
    const texto = { perfecto: 'IMPECABLE', aceptable: 'CORRECTO', fallo: 'TU CARA TE HA DELATADO' }[resultado];
    this.add.text(this.scale.width / 2, 382, texto, {
      fontFamily: FUENTE.maquina, fontSize: '40px', color: hex(resultado === 'fallo' ? COLOR.rojo4 : COLOR.tele5),
      backgroundColor: '#000000', padding: { x: 16, y: 6 },
    }).setOrigin(0.5).setDepth(5);
    this.time.delayedCall(1300, () => this.terminar({ resultado, datos: { aciertos: this.aciertos, total } }));
  }
}
