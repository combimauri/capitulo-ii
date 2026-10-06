/**
 * Capa de sigilo de LocationScene (diseño técnico §6.5).
 * Guardias que siguen una ruta con un cono de visión recortado por las paredes, telepantallas fijas,
 * telepantallas que giran y telepantallas ocultas que solo se notan por el zumbido. Un medidor de alerta
 * se llena mientras algo ve al protagonista; si se llena, le han visto.
 */
import Phaser from 'phaser';
import { cumple, dentroPoligono, type Dir, type LocationData, type Npc, type Point, type Vigia } from '../core/Location';
import { mision, narrativa } from '../core/juego';
import { audio } from './AudioDirector';

const VECTOR: Record<Dir, Point> = { abajo: { x: 0, y: 1 }, arriba: { x: 0, y: -1 }, izquierda: { x: -1, y: 0 }, derecha: { x: 1, y: 0 } };
const RAYOS = 16;
const LLENADO = 0.55;        // segundos a la vista hasta que te ven
const VACIADO = 0.7;         // por segundo, fuera de la vista
const QUIETO_SOCIAL = 3;     // segundos parado, sin la carpeta, antes de que el supervisor se acerque
const RADIO_RUIDO = 260;
const RADIO_ZUMBIDO = 90;

interface NpcVivo { npc: Npc; sprite: Phaser.GameObjects.Sprite; visible: boolean }

interface Guardia {
  n: NpcVivo;
  v: Vigia;
  i: number;               // punto de la ruta hacia el que va
  espera: number;          // ms que le quedan parado
  mira: Point;             // hacia dónde mira (vector unitario)
  giro: number;
  investigar: Point | null;
  cono: Point[];
}

export interface ContextoSigilo {
  prota: () => Point;
  /** ¿Hay una pared o un mueble en este punto? (recorta los conos) */
  bloquea: (p: Point) => boolean;
  /** El jugador se está moviendo este fotograma. */
  moviendose: () => boolean;
  visto: () => void;
}

export class Sigilo {
  private g: Phaser.GameObjects.Graphics;
  private guardias: Guardia[] = [];
  private rotativo = 0;
  private proximoGiro = 0;
  private quieto = 0;
  private zumbido = 0;
  private reloj = 0;

  constructor(private escena: Phaser.Scene, private loc: LocationData, npcs: Map<string, NpcVivo>, private ctx: ContextoSigilo) {
    this.g = escena.add.graphics().setDepth(7999);
    for (const n of npcs.values()) {
      const v = n.npc.vigia;
      if (!v) continue;
      n.npc.solido = false;   // los que caminan no bloquean el paso (rompería el A*)
      const g: Guardia = { n, v, i: 0, espera: 0, mira: VECTOR[n.npc.dir], giro: 0, investigar: null, cono: [] };
      this.colocar(g, v.ruta[0]);
      this.guardias.push(g);
    }
    this.proximoGiro = loc.conosRotativos?.periodo ?? 5000;
    mision.alerta = 0; mision.oculto = false; mision.carpeta = false;
    mision.social = !!loc.sigilo?.social;
    this.girar(0);
  }

  destroy() { this.g.destroy(); mision.social = false; mision.carpeta = false; mision.alerta = 0; mision.oculto = false; }

  /** Vuelta al punto de control: los guardias, a su sitio; la alerta, a cero. */
  reiniciar() {
    for (const g of this.guardias) {
      g.i = 0; g.espera = 0; g.investigar = null; g.giro = 0;
      g.mira = VECTOR[g.n.npc.dir];
      this.colocar(g, g.v.ruta[0]);
    }
    mision.alerta = 0; this.quieto = 0;
  }

  /** Un ruido (un charco, un cubo): los guardias cercanos van a mirar. */
  ruido(p: Point) {
    audio.play('chapoteo');
    for (const g of this.guardias) {
      if (!g.n.visible) continue;
      if (Math.hypot(g.n.sprite.x - p.x, g.n.sprite.y - p.y) < RADIO_RUIDO) { g.investigar = { ...p }; g.espera = 0; }
    }
  }

  /** activo = el jugador puede moverse (no hay diálogo). */
  update(dtMs: number, activo: boolean) {
    this.reloj += dtMs;
    if (activo) {
      for (const g of this.guardias) if (g.n.visible) this.moverGuardia(g, dtMs);
      if (this.loc.conosRotativos && this.reloj >= this.proximoGiro) {
        this.proximoGiro = this.reloj + this.loc.conosRotativos.periodo;
        this.girar((this.rotativo + 1) % this.loc.conosRotativos.conos.length);
      }
    }
    for (const g of this.guardias) g.cono = g.n.visible ? this.cono(g) : [];
    // fuera de su condición, la vigilancia no cuenta (y apenas se ve)
    const alerta = cumple(this.loc.sigilo?.condicion, (v) => narrativa.get(v));
    this.g.setAlpha(alerta ? 1 : 0.35);
    const ve = activo && alerta && this.alguienVe();
    if (activo) {
      const dt = dtMs / 1000;
      mision.alerta = Phaser.Math.Clamp(mision.alerta + (ve ? dt / LLENADO : -dt * VACIADO), 0, 1);
      if (mision.alerta >= 1) { mision.alerta = 0; this.quieto = 0; this.ctx.visto(); }
    }
    this.dibujar(ve);
    if (activo) this.notarOcultos(dtMs);
  }

  // ------------------------------------------------------------------ guardias
  private colocar(g: Guardia, p: Point) {
    const dx = p.x - g.n.sprite.x, dy = p.y - g.n.sprite.y;
    g.n.sprite.setPosition(p.x, p.y).setDepth(p.y);
    g.n.npc.x = p.x; g.n.npc.y = p.y;
    const h = g.n.npc.hotspot;
    h.x += dx; h.y += dy; h.aprox.x += dx; h.aprox.y += dy;
  }

  private moverGuardia(g: Guardia, dtMs: number) {
    const s = g.n.sprite;
    if (g.espera > 0) {
      g.espera -= dtMs;
      if (g.espera <= 0 && g.investigar) g.investigar = null;   // ya ha mirado: vuelve a su ronda
      return;
    }
    const destino = g.investigar ?? g.v.ruta[g.i];
    const dx = destino.x - s.x, dy = destino.y - s.y;
    const d = Math.hypot(dx, dy);
    const paso = g.v.velocidad * (g.investigar ? 1.4 : 1) * dtMs / 1000;
    if (d <= paso) {
      this.colocar(g, destino);
      g.espera = g.investigar ? 1800 : g.v.pausa;
      if (!g.investigar) {
        if (g.v.gira?.length) { g.mira = VECTOR[g.v.gira[g.giro % g.v.gira.length]]; g.giro++; }
        g.i = (g.i + 1) % g.v.ruta.length;
      }
      return;
    }
    g.mira = { x: dx / d, y: dy / d };
    this.colocar(g, { x: s.x + (dx / d) * paso, y: s.y + (dy / d) * paso });
    if (Math.abs(dx) > 0.5) s.setFlipX(dx < 0);
  }

  /** Cono de visión recortado por las colisiones: rayos que se paran en la primera pared. */
  private cono(g: Guardia): Point[] {
    const o = { x: g.n.sprite.x, y: g.n.sprite.y - 3 };
    const base = Math.atan2(g.mira.y, g.mira.x);
    const semi = Phaser.Math.DegToRad(g.v.angulo);
    const puntos = [o];
    for (let k = 0; k <= RAYOS; k++) {
      const a = base - semi + (2 * semi * k) / RAYOS;
      const cx = Math.cos(a), cy = Math.sin(a);
      let r = 8;
      while (r < g.v.alcance && !this.ctx.bloquea({ x: o.x + cx * r, y: o.y + cy * r })) r += 4;
      puntos.push({ x: o.x + cx * r, y: o.y + cy * r });
    }
    return puntos;
  }

  // ------------------------------------------------------------------ telepantallas
  private girar(i: number) {
    this.rotativo = i;
    const r = this.loc.conosRotativos;
    if (r?.variable) narrativa.set(r.variable, i === 0);
  }

  private conosTelepantalla(): Point[][] {
    const s = this.loc.sigilo;
    return [...(s?.fijos ?? []), ...(this.loc.conosRotativos ? [this.loc.conosRotativos.conos[this.rotativo]] : [])];
  }

  /** Las ocultas zumban cuando te acercas: un temblor y un sonido, y se adivina su contorno. */
  private notarOcultos(dtMs: number) {
    const p = this.ctx.prota();
    let cerca = 0;
    for (const c of this.loc.sigilo?.ocultos ?? []) cerca = Math.max(cerca, 1 - Math.hypot(c[0].x - p.x, c[0].y - p.y) / RADIO_ZUMBIDO);
    this.zumbido -= dtMs;
    if (cerca > 0 && this.zumbido <= 0) {
      this.zumbido = 900 - cerca * 500;
      audio.play('zumbido');
      this.escena.cameras.main.shake(140, 0.0015 + cerca * 0.003);
    }
  }

  // ------------------------------------------------------------------ detección
  private alguienVe(): boolean {
    if (mision.oculto) return false;
    const p = this.ctx.prota();
    const pie = { x: p.x, y: p.y - 2 };
    const social = this.loc.sigilo?.social;
    if (social) {
      // con la carpeta abierta y caminando, nadie repara en ti; parado sin ella, sí
      if (mision.carpeta) { this.quieto = 0; return false; }
      this.quieto = this.ctx.moviendose() ? 0 : this.quieto + this.escena.game.loop.delta / 1000;
      if (this.quieto > QUIETO_SOCIAL) return true;
    }
    if (this.guardias.some((g) => g.cono.length && dentroPoligono(pie, g.cono))) return true;
    if (this.conosTelepantalla().some((c) => dentroPoligono(pie, c))) return true;
    return (this.loc.sigilo?.ocultos ?? []).some((c) => dentroPoligono(pie, c));
  }

  private dibujar(ve: boolean) {
    const g = this.g.clear();
    const pinta = (poly: Point[], color: number) => {
      if (poly.length < 3) return;
      const v = poly.map((p) => new Phaser.Math.Vector2(p.x, p.y));
      g.fillStyle(color, ve ? 0.2 : 0.13).fillPoints(v, true).lineStyle(1, color, 0.55).strokePoints(v, true);
    };
    for (const c of this.conosTelepantalla()) pinta(c, ve ? 0xc8382f : 0x7fc496);
    for (const gu of this.guardias) pinta(gu.cono, ve ? 0xc8382f : 0xe0bf68);
    // las ocultas: un contorno tenue, solo de cerca
    const p = this.ctx.prota();
    for (const c of this.loc.sigilo?.ocultos ?? []) {
      const cerca = 1 - Math.hypot(c[0].x - p.x, c[0].y - p.y) / RADIO_ZUMBIDO;
      if (cerca <= 0) continue;
      g.lineStyle(1, 0x7fc496, cerca * 0.6).strokePoints(c.map((q) => new Phaser.Math.Vector2(q.x, q.y)), true);
    }
    // la carpeta abierta, delante del pecho (sigilo social)
    if (mision.carpeta) {
      g.fillStyle(0xc8a878, 1).fillRect(p.x - 7, p.y - 24, 14, 8);
      g.fillStyle(0xeeead9, 1).fillRect(p.x - 6, p.y - 23, 5, 6).fillRect(p.x + 1, p.y - 23, 5, 6);
    }
    // el medidor de alerta, sobre la cabeza
    if (mision.alerta > 0.02) {
      const x = p.x - 9, y = p.y - 48;
      g.fillStyle(0x000000, 0.6).fillRect(x - 1, y - 1, 20, 5);
      g.fillStyle(mision.alerta > 0.6 ? 0xc8382f : 0xe0bf68, 1).fillRect(x, y, 18 * mision.alerta, 3);
    }
  }
}
