/**
 * Crimen facial (diseño técnico §6.2, biblia visual §6.2).
 * Microjuego de ritmo: llegan marcas con una expresión; hay que acertarlas al compás.
 * Etiqueta de ink:  # cf:id=CF-J1-GIMNASIA,expr=entusiasmo,dif=facil,coro=¡Uno!/¡Dos!,tutorial=si
 * Varias fases:     # cf:id=CF-J2-ODIO  → configuración en content/cf/CF-J2-ODIO.json
 *                   (fases con su ritmo, imágenes de la telepantalla, pensamientos y coro)
 * Vecino opcional:  alguien sentado al lado al que se puede mirar de reojo (tecla A o tocándolo).
 *                   En el último tramo de su fase clave hace algo que solo ve quien lo está mirando.
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

interface FaseConfig {
  expr: Expr; golpes: number; bpm?: number; pantalla?: string; pantalla_mitad?: string;
  pensamiento?: string; coro?: string[]; transicion?: boolean;
}
interface VecinoConfig { retrato: string; nombre: string; fase: number }
interface CfConfig { dif?: keyof typeof DIFICULTAD; fases: FaseConfig[]; vecino?: VecinoConfig }
const CONFIGS = import.meta.glob('../../../content/cf/*.json', { eager: true, import: 'default' }) as Record<string, CfConfig>;
const configDe = (id?: string) => Object.entries(CONFIGS).find(([ruta]) => id && ruta.endsWith(`/${id}.json`))?.[1];

const PISTA = { y: 470, xGolpe: 210, xInicio: 900 };
const ANTICIPACION = 2400;   // ms que tarda una marca en cruzar la pista
const VECINO = { x: 588, y: 292, escala: 0.8, escalaMirando: 1.7, mirada: 1600, momento: 1300 };

interface Marca { t: number; expr: Expr; obj: Phaser.GameObjects.Container; resuelta: boolean; fase: number }
interface FaseActiva extends FaseConfig { inicio: number; fin: number }

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
  private fases: FaseActiva[] = [];
  private faseActual = -1;
  private pantalla: Phaser.GameObjects.Image | null = null;
  private textoPensamiento!: Phaser.GameObjects.Text;
  private fallosTransicion = 0;
  private vecino: (VecinoConfig & { img: Phaser.GameObjects.Image; marco: Phaser.GameObjects.Rectangle;
    etiqueta: Phaser.GameObjects.Text; mirandoHasta: number; visto: boolean }) | null = null;

  constructor() { super('Facecrime'); }

  create() {
    const { width, height } = this.scale;
    this.marcas = []; this.aciertos = 0; this.grietas = 0; this.empezado = false;
    this.faseActual = -1; this.fallosTransicion = 0; this.pantalla = null; this.vecino = null;
    this.genero = narrativa.get('genero') === 'f' ? 'm' : 'h';
    const config = configDe(this.params.id);
    const dif = DIFICULTAD[(config?.dif ?? this.params.dif as keyof typeof DIFICULTAD) ?? 'facil'] ?? DIFICULTAD.facil;
    this.ventana = dif.ventana;

    const fases: FaseConfig[] = config?.fases ?? [{
      expr: (this.params.expr ?? 'entusiasmo') as Expr,
      golpes: Number(this.params.golpes) || dif.golpes,
      coro: (this.params.coro ?? '').split('/').filter(Boolean),
    }];
    this.exprs = [...new Set(fases.map((f) => f.expr))];
    this.exprActual = fases[0].expr;
    this.coro = fases[0].coro ?? [];

    this.cameras.main.fadeIn(300, 11, 12, 15);
    this.add.rectangle(width / 2, height / 2, width, height, COLOR.tele0);
    for (let y = 0; y < height; y += 3) this.add.rectangle(width / 2, y, width, 1, 0x000000, 0.25);

    // con imágenes en la telepantalla: pantalla a la izquierda y retrato a la derecha
    const conPantalla = fases.some((f) => f.pantalla);
    const xRetrato = conPantalla ? 760 : width / 2;
    if (conPantalla) {
      this.add.rectangle(330, 214, 420, 316, 0x000000).setStrokeStyle(4, COLOR.gris3);
      this.pantalla = this.add.image(330, 214, `cf-${fases[0].pantalla}`).setScale(4);
    }
    this.add.rectangle(xRetrato, 214, conPantalla ? 248 : 300, conPantalla ? 248 : 300, COLOR.tele1).setStrokeStyle(3, COLOR.tele4);
    this.retrato = this.add.image(xRetrato, 214, this.claveRetrato('neutral')).setScale(conPantalla ? 2.5 : 3);
    this.textoPensamiento = this.add.text(width / 2, 384, '', {
      fontFamily: FUENTE.texto, fontSize: '20px', color: hex(COLOR.papel4), stroke: '#000', strokeThickness: 4,
      align: 'center', wordWrap: { width: 700 },
    }).setOrigin(0.5).setDepth(4);
    this.add.text(width / 2, 30, 'LA TELEPANTALLA TE ESTÁ MIRANDO', {
      fontFamily: FUENTE.maquina, fontSize: '26px', color: hex(COLOR.tele5),
    }).setOrigin(0.5);
    this.textoCoro = this.add.text(width / 2, 382, '', {
      fontFamily: FUENTE.maquina, fontSize: '34px', color: hex(COLOR.papel4),
    }).setOrigin(0.5);

    // pista de ritmo
    this.add.rectangle(width / 2, PISTA.y, width - 80, 54, 0x000000, 0.45).setStrokeStyle(1, COLOR.tele1);
    this.add.circle(PISTA.xGolpe, PISTA.y, 26).setStrokeStyle(3, COLOR.papel4);

    // marcas programadas a partir de las fases (cada fase con su ritmo)
    let t = 1800;
    this.fases = fases.map((f, i) => {
      const intervalo = 60000 / (f.bpm ?? dif.bpm);
      const inicio = t - 900;
      for (let k = 0; k < f.golpes; k++, t += intervalo) {
        this.marcas.push({ t, expr: f.expr, obj: this.crearMarca(f.expr), resuelta: false, fase: i });
      }
      t += 400;
      return { ...f, inicio, fin: t };
    });
    this.fin = t + 600;

    if (config?.vecino && conPantalla) this.crearVecino(config.vecino);
    this.crearControles();
    if (this.params.tutorial === 'si') this.tutorial(); else this.empezar();
  }

  /** El compañero de al lado, visto de reojo: atenuado hasta que el jugador lo mira. */
  private crearVecino(v: VecinoConfig) {
    const marco = this.add.rectangle(VECINO.x, VECINO.y, 96 * VECINO.escala + 6, 96 * VECINO.escala + 6, COLOR.tele1)
      .setStrokeStyle(2, COLOR.tele4).setDepth(6);
    const img = this.add.image(VECINO.x, VECINO.y, `retrato-${v.retrato}_neutral`).setScale(VECINO.escala).setDepth(6);
    const etiqueta = this.add.text(VECINO.x, VECINO.y + 48, `${v.nombre}${this.sys.game.device.os.desktop ? ' · A' : ''}`, {
      fontFamily: FUENTE.maquina, fontSize: '18px', color: hex(COLOR.tele5),
    }).setOrigin(0.5, 0).setDepth(6);
    this.vecino = { ...v, img, marco, etiqueta, mirandoHasta: 0, visto: false };
    this.atenuarVecino(true);
    marco.setInteractive({ useHandCursor: true }).on('pointerdown', () => this.mirarVecino());
    this.input.keyboard?.on('keydown-A', () => this.mirarVecino());
  }

  private atenuarVecino(reojo: boolean) {
    const v = this.vecino!;
    const escala = reojo ? VECINO.escala : VECINO.escalaMirando;
    this.tweens.killTweensOf([v.img, v.marco]);
    this.tweens.add({ targets: v.img, scale: escala, alpha: reojo ? 0.4 : 1, duration: 160 });
    this.tweens.add({ targets: v.marco, scale: reojo ? 1 : escala / VECINO.escala, alpha: reojo ? 0.4 : 1, duration: 160 });
    v.etiqueta.setAlpha(reojo ? 0.6 : 0);
  }

  private mirarVecino() {
    const v = this.vecino;
    if (!v || !this.empezado || this.inicio < 0) return;
    const ahora = this.time.now - this.inicio;
    const clave = this.fases[v.fase];
    // si lo mira durante su fase clave, sigue mirándolo hasta el final de ese tramo
    const hasta = ahora >= clave.inicio && ahora < clave.fin ? clave.fin : ahora + VECINO.mirada;
    if (v.mirandoHasta <= ahora) this.atenuarVecino(false);
    v.mirandoHasta = Math.max(v.mirandoHasta, hasta);
  }

  /** Fotograma del vecino según el momento: grita con el público salvo un segundo, al final del clímax. */
  private actualizarVecino(ahora: number) {
    const v = this.vecino;
    if (!v) return;
    const clave = this.fases[v.fase];
    const mirando = ahora < v.mirandoHasta;
    const callado = ahora >= clave.fin - VECINO.momento && ahora < clave.fin;
    const enOdio = ahora >= this.fases[0].inicio && ahora < this.fases[this.fases.length - 1].fin;
    const grito = Math.floor(ahora / 300) % 2 ? 'grita' : 'grita2';
    v.img.setTexture(`retrato-${v.retrato}_${callado ? 'gafas' : enOdio ? grito : 'neutral'}`);
    if (callado && mirando) v.visto = true;
    if (!mirando && v.img.alpha === 1 && !this.tweens.isTweening(v.img)) this.atenuarVecino(true);
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
    this.actualizarFase(ahora);
    this.actualizarVecino(ahora);
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

  /** Cambia la imagen de la telepantalla, el pensamiento y el coro al entrar en cada fase. */
  private actualizarFase(ahora: number) {
    const i = this.fases.findIndex((f) => ahora >= f.inicio && ahora < f.fin);
    if (i < 0) return;
    const f = this.fases[i];
    if (this.pantalla && f.pantalla_mitad && ahora > (f.inicio + f.fin) / 2) this.pantalla.setTexture(`cf-${f.pantalla_mitad}`);
    if (i === this.faseActual) return;
    this.faseActual = i;
    this.coro = f.coro ?? this.coro;
    if (this.pantalla && f.pantalla) {
      this.pantalla.setTexture(`cf-${f.pantalla}`);
      this.cameras.main.flash(120, 255, 255, 255);
    }
    if (f.pensamiento) {
      this.textoPensamiento.setText(f.pensamiento).setAlpha(1);
      this.tweens.killTweensOf(this.textoPensamiento);
      this.tweens.add({ targets: this.textoPensamiento, alpha: 0, delay: 2200, duration: 500 });
    }
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
    if (this.fases[m.fase]?.transicion) this.fallosTransicion++;
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
    const transicion = this.fallosTransicion > 0 ? 'fallo' : 'ok';
    const datos: Record<string, string | number> = { aciertos: this.aciertos, total, transicion };
    if (this.vecino) datos[this.vecino.retrato] = this.vecino.visto ? 'visto' : 'no';
    this.time.delayedCall(1300, () => this.terminar({ resultado, datos }));
  }
}
