/**
 * Pistas visuales en los escenarios (opción «Pistas visuales»), pedidas en las primeras pruebas con jugadores:
 *   - un bocadillo sobre quien tiene algo nuevo que decir;
 *   - un destello en lo que esconde algo que aún no se ha leído (y un punto tenue si solo es mirarlo);
 *   - una flecha en las salidas que de verdad llevan a otro sitio ahora mismo.
 * Para saberlo se juega en seco cada acción en una copia de ink (NarrativeBridge.simular) y se compara con
 * las líneas ya leídas (el registro). El cálculo se reparte entre fotogramas para no dar tirones.
 * Las marcas están por debajo de la oscuridad de los túneles: allí solo se ven donde alumbra la linterna.
 */
import Phaser from 'phaser';
import type { Hotspot, LocationData } from '../core/Location';
import { analizar, type Analisis } from '../core/pistas';
import { narrativa, registro } from '../core/juego';
import { opciones } from '../core/Opciones';
import { COLOR } from './estilo';
import { objetivoActual } from '../scenes/ApuntesScene';

/** Sin tildes ni mayúsculas, para buscar el nombre de un hotspot dentro del objetivo. */
const plano = (t: string) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

type Tipo = 'objetivo' | 'salida' | 'persona' | 'objeto' | 'vistazo';
type Lado = 'arriba' | 'abajo' | 'izquierda' | 'derecha';

const PROFUNDIDAD = 8900;
/** Milisegundos por fotograma que se dedican a analizar hotspots. */
const PRESUPUESTO_MS = 4;

interface Marca { tipo: Tipo; sprite: Phaser.GameObjects.Image; tween: Phaser.Tweens.Tween; h: Hotspot; lado?: Lado }

export class Marcas {
  private marcas = new Map<Hotspot, Marca>();
  private pendientes: Hotspot[] = [];
  private estado = '';
  private leidas = new Set<string>();
  /** El objetivo de los apuntes, sin tildes: el hotspot que nombra lleva la marca de objetivo. */
  private objetivo = '';
  private visibles = true;

  constructor(private escena: Phaser.Scene, private loc: LocationData,
    /** El sprite de cada personaje, para poner el bocadillo sobre su cabeza (y seguirle si se mueve). */
    private personaje: (h: Hotspot) => Phaser.GameObjects.Sprite | null) {
    Marcas.texturas(escena);
  }

  /** Vuelve a mirar todos los hotspots visibles (al terminar un diálogo, al cambiar la historia). */
  actualizar(hotspots: Hotspot[]) {
    for (const [h, m] of this.marcas) if (!hotspots.includes(h)) this.quitar(h, m);
    if (opciones.pistas === 'ninguna') {
      for (const [h, m] of this.marcas) this.quitar(h, m);
      this.pendientes = [];
      return;
    }
    this.estado = narrativa.saveState();
    this.leidas = new Set(registro.entradas.map((e) => e.id));
    this.objetivo = plano(objetivoActual());
    this.pendientes = [...hotspots];
  }

  mostrar(v: boolean) {
    this.visibles = v;
    for (const m of this.marcas.values()) m.sprite.setVisible(v);
  }

  /** Cada fotograma: analiza unos cuantos hotspots pendientes y pone los bocadillos sobre quien se mueva. */
  seguir() {
    const fin = performance.now() + PRESUPUESTO_MS;
    while (this.pendientes.length && performance.now() < fin) {
      const h = this.pendientes.shift()!;
      this.colocar(h, analizar(h, this.estado, this.leidas, (r, e) => narrativa.simular(r, e)));
    }
    for (const m of this.marcas.values()) {
      if (m.tipo !== 'persona' && m.tipo !== 'objetivo') continue;
      const s = this.personaje(m.h);
      if (s) m.sprite.setX(s.x).setVisible(this.visibles && s.visible);
    }
  }

  destroy() {
    for (const [h, m] of this.marcas) this.quitar(h, m);
    this.pendientes = [];
  }

  // ------------------------------------------------------------------ dibujo
  private colocar(h: Hotspot, a: Analisis) {
    const persona = !!this.personaje(h) || !!h.hablar;
    // lo que nombra el objetivo de los apuntes («Siéntate en Mi mesa»): por encima de todo lo demás
    const nombre = plano(h.nombre ?? '');
    const objetivo = !h.auto && nombre.length >= 4 && new RegExp(`(^|[^a-z])${nombre.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([^a-z]|$)`).test(this.objetivo);
    const tipo: Tipo | null = objetivo ? 'objetivo'
      : a.salida && opciones.pistas === 'todas' ? 'salida'
      : a.nuevo ? (persona ? 'persona' : 'objeto')
      : a.vistazo ? 'vistazo' : null;
    const previa = this.marcas.get(h);
    if (previa?.tipo === tipo) return;
    if (previa) this.quitar(h, previa);
    if (!tipo) return;

    const e = this.escena;
    const cx = h.x + h.w / 2;
    let sprite: Phaser.GameObjects.Image, tween: Phaser.Tweens.Tween, lado: Lado | undefined;
    if (tipo === 'objetivo') {
      const s = this.personaje(h);
      const x = s ? s.x : cx, y = s ? s.y - s.displayHeight - 4 : Math.max(10, h.y - 3);
      sprite = e.add.image(x, y, 'marca-objetivo').setOrigin(0.5, 1);
      tween = e.tweens.add({ targets: sprite, y: y - 4, duration: 480, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    } else if (tipo === 'salida') {
      lado = this.lado(h);
      const { x, y } = this.puntoSalida(h, lado);
      sprite = e.add.image(x, y, 'marca-flecha').setAngle({ arriba: 0, derecha: 90, abajo: 180, izquierda: -90 }[lado]);
      const [dx, dy] = { arriba: [0, -1], abajo: [0, 1], izquierda: [-1, 0], derecha: [1, 0] }[lado];
      tween = e.tweens.add({ targets: sprite, x: x + dx * 2, y: y + dy * 2, alpha: { from: 0.95, to: 0.55 }, duration: 650, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    } else if (tipo === 'persona') {
      const s = this.personaje(h);
      const x = s ? s.x : cx, y = s ? s.y - s.displayHeight - 4 : h.y - 4;
      sprite = e.add.image(x, y, 'marca-bocadillo').setOrigin(0.5, 1);
      tween = e.tweens.add({ targets: sprite, scaleY: { from: 1, to: 1.12 }, scaleX: { from: 1, to: 0.94 }, duration: 520, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    } else if (tipo === 'objeto') {
      sprite = e.add.image(cx, Math.max(4, h.y - 3), 'marca-destello');
      tween = e.tweens.add({ targets: sprite, scale: { from: 0.5, to: 1 }, alpha: { from: 0.35, to: 1 }, duration: 700, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    } else {
      sprite = e.add.image(cx, Math.max(3, h.y - 2), 'marca-punto');
      tween = e.tweens.add({ targets: sprite, alpha: { from: 0.25, to: 0.7 }, duration: 1300, yoyo: true, repeat: -1, ease: 'Sine.inOut' });
    }
    sprite.setDepth(PROFUNDIDAD).setVisible(this.visibles);
    this.marcas.set(h, { tipo, sprite, tween, h, lado });
  }

  private quitar(h: Hotspot, m: Marca) {
    m.tween.remove();
    m.sprite.destroy();
    this.marcas.delete(h);
  }

  /** Hacia dónde lleva la salida: al borde más cercano si está pegada a uno; si no (una puerta en la pared), hacia arriba. */
  private lado(h: Hotspot): Lado {
    const cx = h.x + h.w / 2, cy = h.y + h.h / 2, W = this.loc.width, H = this.loc.height;
    const d: [Lado, number][] = [['izquierda', h.x], ['derecha', W - (h.x + h.w)], ['abajo', H - (h.y + h.h)], ['arriba', h.y]];
    const [lado, dist] = d.sort((a, b) => a[1] - b[1])[0];
    if (dist <= 24) return lado;
    return cy > H * 0.75 && cx > 0 ? 'abajo' : 'arriba';
  }

  private puntoSalida(h: Hotspot, lado: Lado) {
    const cx = h.x + h.w / 2, cy = h.y + h.h / 2, W = this.loc.width, H = this.loc.height;
    const dentro = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));
    switch (lado) {
      case 'izquierda': return { x: dentro(h.x + h.w + 6, 6, W - 6), y: dentro(cy, 8, H - 8) };
      case 'derecha': return { x: dentro(h.x - 6, 6, W - 6), y: dentro(cy, 8, H - 8) };
      case 'abajo': return { x: dentro(cx, 8, W - 8), y: dentro(h.y - 4, 6, H - 6) };
      default: return { x: dentro(cx, 8, W - 8), y: dentro(h.y - 5, 5, H - 6) };
    }
  }

  /** Los iconos, en píxeles del arte (la cámara los dobla): se dibujan una vez por partida. */
  private static texturas(e: Phaser.Scene) {
    if (e.textures.exists('marca-flecha')) return;
    const g = e.make.graphics({}, false);
    // flecha (chevron hacia arriba), ocre con borde oscuro
    g.fillStyle(COLOR.negro, 0.9).fillTriangle(6.5, 0, 13, 8, 0, 8);
    g.fillStyle(COLOR.ocre4, 1).fillTriangle(6.5, 2, 10.5, 7, 2.5, 7);
    g.generateTexture('marca-flecha', 13, 9);
    g.clear();
    // objetivo: una flecha gruesa hacia abajo, ocre, con borde oscuro
    g.fillStyle(COLOR.negro, 0.9).fillRect(3, 0, 7, 7).fillTriangle(0, 6, 13, 6, 6.5, 15);
    g.fillStyle(COLOR.ocre4, 1).fillRect(4.5, 1, 4, 7).fillTriangle(2, 7.5, 11, 7.5, 6.5, 13.5);
    g.generateTexture('marca-objetivo', 13, 15);
    g.clear();
    // bocadillo con puntos suspensivos
    g.fillStyle(COLOR.negro, 0.9).fillRect(0, 0, 11, 8).fillRect(3, 8, 3, 2);
    g.fillStyle(COLOR.papel4, 1).fillRect(1, 1, 9, 6).fillRect(4, 7, 1, 2);
    g.fillStyle(COLOR.gris2, 1).fillRect(2, 3, 1, 2).fillRect(5, 3, 1, 2).fillRect(8, 3, 1, 2);
    g.generateTexture('marca-bocadillo', 11, 10);
    g.clear();
    // destello: una cruz de cuatro puntas
    g.fillStyle(COLOR.papel4, 1).fillRect(3, 0, 1, 7).fillRect(0, 3, 7, 1);
    g.fillStyle(0xffffff, 1).fillRect(2, 2, 3, 3);
    g.generateTexture('marca-destello', 7, 7);
    g.clear();
    // punto: solo hay algo que mirar
    g.fillStyle(COLOR.papel3, 1).fillRect(0, 0, 2, 2);
    g.generateTexture('marca-punto', 2, 2);
    g.destroy();
  }
}
