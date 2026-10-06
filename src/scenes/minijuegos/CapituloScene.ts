/**
 * Composición del Capítulo II (guion J13.05): cinco movimientos hechos con lo que el jugador escribió en el diario.
 * Apertura (la frase de Ivy, con su falta de ortografía, si se tiene su carta), cuatro movimientos con las entradas
 * compatibles (o la frase que dicta Goldstein, en cursiva: su voz, no la tuya), conectores según la Duda y un cierre.
 * Al final, Goldstein lo mecanografía línea a línea.
 *   # minijuego:capitulo,vars=cap   → cap_apertura, cap_mov1…cap_mov4, cap_cierre, cap_texto (líneas separadas por ¶),
 *                                     cap_ivy_corregida (si/no), cap_voces (frases de Goldstein)
 */
import Phaser from 'phaser';
import { Minijuego } from './Minijuego';
import { audio } from '../../systems/AudioDirector';
import { narrativa } from '../../core/juego';
import { se_cumple } from '../../core/texto';
import { COLOR, FUENTE, hex } from '../../ui/estilo';

interface Movimiento { titulo: string; entradas: string[]; defecto: string }

const MOVIMIENTOS: Movimiento[] = [
  { titulo: 'I · Lo que se entrega', entradas: ['diario_ivy', 'diario_ivy_verdad', 'diario_times'],
    defecto: 'El creyente entrega su memoria a cambio de no tener miedo.' },
  { titulo: 'II · El odio como alimento', entradas: ['diario_sammy', 'diario_cohetes', 'diario_planilla', 'diario_libro_guerra'],
    defecto: 'El Partido da de comer odio a quien tiene hambre de sentido.' },
  { titulo: 'III · El pasado redactado', entradas: ['diario_amory', 'diario_parte', 'diario_chocolate', 'diario_estasia', 'diario_amory_confesion', 'diario_libro_pasado', 'diario_libro_doblepensar'],
    defecto: 'Lo que no se recuerda no se puede echar de menos.' },
  { titulo: 'IV · Los de abajo', entradas: ['diario_dot', 'diario_nell', 'diario_len', 'diario_libro_ignorancia'],
    defecto: 'Nadie mira a quien limpia. Por eso quien limpia lo ve todo.' },
];

const CIERRES: { texto: string; si?: string }[] = [
  { texto: 'La libertad no es un lugar. Es un reloj que alguien decide volver a poner en marcha.', si: 'reloj_en_marcha' },
  { texto: 'Fui libre catorce días. Lo bastante para saber exactamente lo que me van a quitar.' },
  { texto: 'No sé si la libertad existe. Sé que la esclavitud tenía la cara de mi hermana, y que me hacía sentir en casa.', si: 'carta_ivy' },
  { texto: 'Un niño coleccionaba metralla para que nunca le cayera un cohete. Eso era la fe. Esto es otra cosa.', si: 'metralla_cierre' },
  { texto: 'Elegí quién moría con una máquina de escribir. Ya no puedo decir que no soy uno de ellos. Puedo decir que lo sé.', si: 'len_salvado' },
];

const IVY = 'Nos dijeron que la libertad es la esclavitud. Nadie nos dijo que la esclavitud también puede ser un hogar, y que por eso es tan dificil salir de ella.';
const LAPIZ = 'Tiré su lápiz al fuego. Me pareció lo higiénico.';

/** Una línea del capítulo: el texto y si es la voz de Goldstein (cursiva). */
interface Linea { texto: string; goldstein?: boolean; titulo?: boolean }

export class CapituloScene extends Minijuego {
  private capa!: Phaser.GameObjects.Container;
  private lineas: Linea[] = [];
  private datos: Record<string, string | number> = {};
  private voces = 0;

  constructor() { super('Capitulo'); }

  preload() {
    for (const k of ['fondo', 'rodillo', 'hoja', 'tarjeta', 'tarjeta-luz']) this.load.image(`capitulo-${k}`, `assets/minijuegos/capitulo-${k}.png`);
  }

  create() {
    this.lineas = []; this.datos = {}; this.voces = 0;
    this.cameras.main.fadeIn(500, 11, 12, 15);
    // la mesa de la cripta a la luz de las velas, con el cuerpo de la máquina de Goldstein abajo: capitulo-fondo
    this.add.image(0, 0, 'capitulo-fondo').setOrigin(0).setScale(2);
    this.capa = this.add.container(0, 0);
    // el carro de la máquina, por encima de la hoja (el papel sale de detrás del rodillo)
    this.add.image(0, 484, 'capitulo-rodillo').setOrigin(0).setScale(2);
    void this.componer();
  }

  // ------------------------------------------------------------------ utilidades de interfaz
  private limpiar(titulo: string, ayuda = '') {
    this.capa.removeAll(true);
    this.capa.add(this.add.text(480, 40, titulo, { fontFamily: FUENTE.maquina, fontSize: '30px', color: hex(COLOR.ocre4) }).setOrigin(0.5));
    if (ayuda) this.capa.add(this.add.text(480, 76, ayuda, { fontFamily: FUENTE.texto, fontSize: '18px', color: hex(COLOR.papel3), align: 'center', wordWrap: { width: 820 } }).setOrigin(0.5, 0));
  }

  /** Opciones como tarjetas de papel; resuelve con el índice elegido. */
  private elegir(opciones: { texto: string; nota?: string; goldstein?: boolean }[], y0 = 130): Promise<number> {
    return new Promise((ok) => {
      const alto = Math.min(76, Math.floor((480 - y0) / opciones.length) - 10);
      opciones.forEach((o, i) => {
        const y = y0 + i * (alto + 10) + alto / 2;
        // un papelito por opción (nine-slice, 820 × alto); al pasar por encima, el mismo papel más claro
        const papel = (clave: string) => this.add.nineslice(480, y, clave, undefined, 410, Math.round(alto / 2), 8, 8, 8, 8).setScale(2);
        const f = papel('capitulo-tarjeta').setInteractive({ useHandCursor: true });
        const luz = papel('capitulo-tarjeta-luz').setVisible(false);
        const t = this.add.text(90, y - (o.nota ? 8 : 0), o.texto, {
          fontFamily: FUENTE.texto, fontSize: '19px', color: o.goldstein ? '#5a4a30' : '#2a2218', fontStyle: o.goldstein ? 'italic' : 'normal',
          wordWrap: { width: 780 },
        }).setOrigin(0, 0.5);
        this.capa.add([f, luz, t]);
        if (o.nota) this.capa.add(this.add.text(870, y + alto / 2 - 6, o.nota, { fontFamily: FUENTE.maquina, fontSize: '16px', color: '#6a5c44' }).setOrigin(1, 1));
        f.on('pointerover', () => luz.setVisible(true));
        f.on('pointerout', () => luz.setVisible(false));
        f.once('pointerup', () => { audio.play('plumilla'); ok(i); });
      });
    });
  }

  private espera(ms: number) { return new Promise<void>((ok) => this.time.delayedCall(ms, ok)); }

  // ------------------------------------------------------------------ composición
  private async componer() {
    const v = (n: string) => narrativa.get(n);
    // apertura
    if (v('carta_ivy')) {
      this.limpiar('APERTURA', 'La frase de Ivy, con su letra. Sin tilde en «dificil». Siempre se le olvidaba.');
      const i = await this.elegir([{ texto: IVY, nota: 'dejarla así' }, { texto: IVY.replace('dificil', 'difícil'), nota: 'corregir la tilde' }]);
      const corregida = i === 1;
      this.datos.ivy_corregida = corregida ? 'si' : 'no';
      this.datos.apertura = corregida ? IVY.replace('dificil', 'difícil') : IVY;
      this.lineas.push({ texto: 'Capítulo II — La libertad es la esclavitud', titulo: true }, { texto: `«${this.datos.apertura}» — I.` });
    } else {
      this.datos.ivy_corregida = 'no';
      this.datos.apertura = 'Capítulo II — La libertad es la esclavitud.';
      this.lineas.push({ texto: 'Capítulo II — La libertad es la esclavitud', titulo: true });
    }
    // los cuatro movimientos
    const conector = this.conector();
    for (let m = 0; m < MOVIMIENTOS.length; m++) {
      const mov = MOVIMIENTOS[m];
      const escritas = mov.entradas.filter((e) => v(`${e}_escrita`) && v(`${e}_frase`)).map((e) => ({ entrada: e, texto: String(v(`${e}_frase`)) }));
      let texto: string, goldstein = false;
      if (escritas.length) {
        this.limpiar(mov.titulo, 'Elige una de las cosas que escribiste.');
        const i = await this.elegir(escritas.map((e) => ({ texto: e.texto })));
        texto = escritas[i].texto;
        if (m === 2 && escritas[i].entrada === 'diario_amory' && v('lapiz_destruido')) texto += ` ${LAPIZ}`;
      } else {
        this.limpiar(mov.titulo, 'No escribiste nada sobre esto. Goldstein dicta:');
        await this.elegir([{ texto: mov.defecto, goldstein: true, nota: 'escribirla' }]);
        texto = mov.defecto; goldstein = true; this.voces++;
      }
      this.datos[`mov${m + 1}`] = texto;
      this.lineas.push({ texto: mov.titulo, titulo: true }, { texto, goldstein });
      if (m < MOVIMIENTOS.length - 1) this.lineas.push({ texto: conector[m % conector.length] });
    }
    // el cierre
    narrativa.set('metralla_cierre', !!v('sammy_intento') || narrativa.list('inventario').includes('metralla_brillante'));
    const cierres = CIERRES.filter((c) => se_cumple(c.si));
    this.limpiar('V · La libertad', 'La última frase.');
    const c = await this.elegir(cierres.map((x) => ({ texto: x.texto })));
    this.datos.cierre = cierres[c].texto;
    this.lineas.push({ texto: 'V · La libertad', titulo: true }, { texto: this.datos.cierre as string });
    await this.mecanografiar();
  }

  /** Las frases de enlace del protagonista, según la Duda y lo que hizo con el doblepensar de J11. */
  private conector(): string[] {
    const duda = Number(narrativa.get('duda')) || 0, dp = String(narrativa.get('dp_j11_ivy'));
    if (dp === 'aceptar') return ['Escribo esto y no sé si lo creo. Lo escribo igual.', 'No sé si fue así. Lo escribo por si lo fue.', 'Me tiembla la mano. Sigo.'];
    if (duda >= 70) return ['Esto lo vi yo. No me lo contó nadie.', 'Lo escribo con mi nombre.', 'Esto también ocurrió.'];
    return ['No sé si esto prueba algo. Sé que ocurrió.', 'Puede que me equivoque. No en esto.', 'Lo recuerdo. Eso es todo lo que tengo.'];
  }

  /** Goldstein lo teclea en la máquina, línea a línea. */
  private async mecanografiar() {
    this.capa.removeAll(true);
    const hoja = this.add.image(50, 20, 'capitulo-hoja').setOrigin(0).setScale(2);   // 860 × 1400, como antes
    this.capa.add(hoja);
    let y = 34;
    for (const l of this.lineas) {
      const t = this.add.text(l.titulo ? 480 : 80, y, '', {
        fontFamily: l.titulo ? FUENTE.maquina : FUENTE.maquina, fontSize: l.titulo ? '20px' : '17px',
        color: l.goldstein ? '#6a5a40' : '#2a2218', fontStyle: l.goldstein ? 'italic' : 'normal', wordWrap: { width: 800 },
      }).setOrigin(l.titulo ? 0.5 : 0, 0);
      this.capa.add(t);
      for (let i = 1; i <= l.texto.length; i++) {
        t.setText(l.texto.slice(0, i));
        if (i % 2 === 0) audio.play('tecla');
        await this.espera(14);
      }
      y += t.height + (l.titulo ? 4 : 8);
      // si no cabe, la hoja sube
      if (y + this.capa.y > 490) this.tweens.add({ targets: this.capa, y: 490 - y, duration: 300 });
      await this.espera(160);
    }
    audio.play('sello');
    const texto = this.lineas.map((l) => l.texto).join('¶');
    const aviso = this.add.text(480, 528, '[ toca para continuar ]', {
      fontFamily: FUENTE.maquina, fontSize: '20px', color: hex(COLOR.papel3), stroke: hex(COLOR.negro), strokeThickness: 4,   // sobre la guía del carro
    }).setOrigin(0.5, 1);
    this.tweens.add({ targets: aviso, alpha: 0.3, duration: 600, yoyo: true, repeat: -1 });
    await this.espera(600);
    this.input.once('pointerup', () => this.terminar({ resultado: 'escrito', datos: { ...this.datos, texto, voces: this.voces } }, 800));
  }
}
