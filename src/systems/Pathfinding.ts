/**
 * A* sobre una cuadrícula fina (8 px) generada a partir de las colisiones.
 * La ruta se suaviza eliminando puntos intermedios con línea de visión.
 */
import type { Point } from '../core/Location';

export class NavGrid {
  readonly cols: number;
  readonly rows: number;
  private blocked: Uint8Array;

  constructor(width: number, height: number, readonly cell: number, isBlocked: (x: number, y: number) => boolean) {
    this.cols = Math.ceil(width / cell);
    this.rows = Math.ceil(height / cell);
    this.blocked = new Uint8Array(this.cols * this.rows);
    for (let r = 0; r < this.rows; r++) {
      for (let c = 0; c < this.cols; c++) {
        this.blocked[r * this.cols + c] = isBlocked(c * cell + cell / 2, r * cell + cell / 2) ? 1 : 0;
      }
    }
  }

  private idx(c: number, r: number) { return r * this.cols + c; }
  private free(c: number, r: number) {
    return c >= 0 && r >= 0 && c < this.cols && r < this.rows && !this.blocked[this.idx(c, r)];
  }
  private toCell(p: Point): [number, number] {
    return [Math.floor(p.x / this.cell), Math.floor(p.y / this.cell)];
  }
  private toPoint(c: number, r: number): Point {
    return { x: c * this.cell + this.cell / 2, y: r * this.cell + this.cell / 2 };
  }

  /** Celda libre más cercana (por si el destino cae dentro de un mueble). */
  nearestFree(p: Point): [number, number] | null {
    const [c0, r0] = this.toCell(p);
    for (let rad = 0; rad < 12; rad++) {
      for (let dr = -rad; dr <= rad; dr++) {
        for (let dc = -rad; dc <= rad; dc++) {
          if (Math.max(Math.abs(dc), Math.abs(dr)) !== rad) continue;
          if (this.free(c0 + dc, r0 + dr)) return [c0 + dc, r0 + dr];
        }
      }
    }
    return null;
  }

  lineOfSight(a: [number, number], b: [number, number]): boolean {
    let [x0, y0] = a; const [x1, y1] = b;
    const dx = Math.abs(x1 - x0), dy = -Math.abs(y1 - y0);
    const sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    let err = dx + dy;
    for (;;) {
      if (!this.free(x0, y0)) return false;
      if (x0 === x1 && y0 === y1) return true;
      const e2 = 2 * err;
      if (e2 >= dy) { err += dy; x0 += sx; }
      if (e2 <= dx) { err += dx; y0 += sy; }
    }
  }

  findPath(from: Point, to: Point): Point[] | null {
    const start = this.nearestFree(from);
    const goal = this.nearestFree(to);
    if (!start || !goal) return null;
    const key = (c: number, r: number) => this.idx(c, r);
    const g = new Map<number, number>([[key(...start), 0]]);
    const came = new Map<number, number>();
    const open: [number, number, number][] = [[0, ...start]];
    const h = (c: number, r: number) => {
      const dx = Math.abs(c - goal[0]), dy = Math.abs(r - goal[1]);
      return dx + dy + (Math.SQRT2 - 2) * Math.min(dx, dy);
    };
    const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
    while (open.length) {
      open.sort((a, b) => a[0] - b[0]);
      const [, c, r] = open.shift()!;
      if (c === goal[0] && r === goal[1]) {
        const cells: [number, number][] = [[c, r]];
        let k = key(c, r);
        while (came.has(k)) {
          k = came.get(k)!;
          cells.unshift([k % this.cols, Math.floor(k / this.cols)]);
        }
        return this.smooth(cells).map(([cc, rr]) => this.toPoint(cc, rr)).concat(this.free(...this.toCell(to)) ? [to] : []);
      }
      for (const [dc, dr] of dirs) {
        const nc = c + dc, nr = r + dr;
        if (!this.free(nc, nr)) continue;
        if (dc && dr && (!this.free(c + dc, r) || !this.free(c, r + dr))) continue; // sin cortar esquinas
        const ng = g.get(key(c, r))! + (dc && dr ? Math.SQRT2 : 1);
        const nk = key(nc, nr);
        if (ng < (g.get(nk) ?? Infinity)) {
          g.set(nk, ng);
          came.set(nk, key(c, r));
          open.push([ng + h(nc, nr), nc, nr]);
        }
      }
    }
    return null;
  }

  private smooth(cells: [number, number][]): [number, number][] {
    if (cells.length < 3) return cells.slice(1);
    const out: [number, number][] = [];
    let anchor = cells[0];
    for (let i = 2; i < cells.length; i++) {
      if (!this.lineOfSight(anchor, cells[i])) {
        out.push(cells[i - 1]);
        anchor = cells[i - 1];
      }
    }
    out.push(cells[cells.length - 1]);
    return out;
  }
}
