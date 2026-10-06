"""Viñetas fijas de los finales C, D y E (480x270, el juego las dibuja a 2x).

pasillo_suelo:      FC.02 — las palizas. Vista desde el suelo de un pasillo blanco del Minimor: linóleo,
                    dos pares de botas negras, salpicaduras oscuras. Los golpes van en off.
habitacion101:      FC.04 — techo de hormigón muy bajo, el hueco en el suelo y la tolva de escombros;
                    altavoces en las cuatro esquinas. Fondo del minijuego: la mitad de abajo, limpia.
despacho_obrien(_crane): FE.04 — despacho del Partido Interior; el mapa del Registro de Impactos con el
                    círculo blanco de San Clemente. O'Brien de pie, Voss sentado (y Crane en un rincón).
patio_limehouse(_len): FD.08 — patio de Limehouse por la mañana, la niña que canta tendiendo sábanas y
                    Dot en la ventana (y Len a su lado, leyendo el libro cosido con hilo).
salon_odio_h / _m:  FE.03 — los Dos Minutos de Odio, años después: en la pantalla, la cara envejecida del
                    protagonista con rasgos de enemigo; Hilda lanza un zapato.
limehouse_manana:   FD.07 — Limehouse por la mañana, más vivo: luz cálida, niños, ropa tendida, alguien canta.
"""
import math
import random
import sys
from pathlib import Path

ART = Path(__file__).resolve().parents[1]
for _p in (ART / "lib", ART / "personajes", ART / "escenarios"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
from pixel import LOOKUP, Canvas, K  # noqa: E402
import props as P  # noqa: E402
import _luz as L  # noqa: E402

W, H = 480, 270


# ================================================================ utilidades

def _raycast(cv, cam, f, centro, superficie, limite=None):
    """Proyección de un pasillo/sala en caja: para cada píxel llama a superficie(dir) -> color."""
    cx, cy = centro
    x0, y0, x1, y1 = limite or (0, 0, cv.w, cv.h)
    px = cv.img.load()
    for sy in range(y0, y1):
        for sx in range(x0, x1):
            u, v = (sx - cx) / f, (cy - sy) / f
            col = superficie(u, v)
            if col is not None:
                px[sx, sy] = col


def _sombrea(cv, x0, y0, x1, y1, pasos, mascara=None):
    """Sube/baja `pasos` dentro de la rampa de cada píxel (como bake_lighting, pero inmediato)."""
    px = cv.img.load()
    for y in range(max(0, y0), min(cv.h, y1)):
        for x in range(max(0, x0), min(cv.w, x1)):
            if mascara and not mascara(x, y):
                continue
            c = px[x, y]
            if c in LOOKUP:
                r, i = LOOKUP[c]
                px[x, y] = K(r, i + pasos)


# ================================================================ 4. pasillo desde el suelo

def _bota(cv, x, y, s, lado, punta=True):
    """Bota negra militar vista de frente desde el suelo. (x, y) = centro de la suela; s = px por cm."""
    ancho, alto = max(4, round(10 * s)), round(26 * s)
    sx0, sx1 = x - ancho // 2, x + ancho // 2
    # caña
    cv.rect(sx0, y - alto, sx1, y - round(5 * s), K("gris", 1))
    cv.vline(sx0, y - alto, y - round(5 * s), K("gris", 0)); cv.vline(sx1 - 1, y - alto, y - round(5 * s), K("gris", 0))
    br = sx0 + max(1, ancho // 4) if lado < 0 else sx1 - max(2, ancho // 4) - 1
    cv.vline(br, y - alto + 2, y - round(7 * s), K("gris", 3))                         # brillo del cuero
    if s > 1.2:
        cv.vline(br + (1 if lado < 0 else -1), y - alto + round(4 * s), y - round(12 * s), K("gris", 2))
    # cordones
    for k in range(round(alto * 0.15), alto - round(9 * s), max(2, round(3 * s))):
        cv.hline(x - max(1, ancho // 5), x + max(1, ancho // 5) + 1, y - alto + k, K("gris", 2))
    # empeine y puntera, que vienen hacia la cámara
    pw = ancho + max(2, round(3 * s))
    ph = max(3, round(8 * s))
    cv.ellipse(x - pw // 2, y - ph, x + pw // 2 + 1, y + 1, K("gris", 1))
    cv.rect(x - pw // 2, y - ph // 2, x + pw // 2 + 1, y, K("gris", 1))
    cv.ellipse(x - pw // 4, y - ph + 1, x + pw // 4, y - ph // 2 + 1, K("gris", 3))   # brillo de la puntera
    if s > 1.2:
        cv.px(x - pw // 6, y - ph + 2, K("gris", 5))
    # suela gruesa
    cv.rect(x - pw // 2 - 1, y - max(1, round(1.5 * s)), x + pw // 2 + 2, y + 1, K("gris", 0))
    cv.hline(x - pw // 2, x + pw // 2 + 1, y - max(1, round(1.5 * s)) - 1, K("gris", 2))


def _piernas(cv, x, y_suelo, s, sep):
    """Pantalón negro de uniforme desde las botas hasta fuera del encuadre."""
    alto_bota = round(26 * s)
    ancho = round(14 * s)
    for lado in (-1, 1):
        cx = x + lado * sep // 2
        y_top = y_suelo - alto_bota + round(3 * s)
        # la pierna se abre un poco hacia arriba (contrapicado)
        cv.poly([(cx - ancho // 2, y_top), (cx + ancho // 2, y_top), (cx + ancho // 2 + lado * round(4 * s), -2),
                 (cx - ancho // 2 + lado * round(4 * s), -2)], K("gris", 2))
        cv.d.line([(cx - ancho // 2, y_top), (cx - ancho // 2 + lado * round(4 * s), 0)], fill=K("gris", 1))
        cv.d.line([(cx + ancho // 2 - 1, y_top), (cx + ancho // 2 - 1 + lado * round(4 * s), 0)], fill=K("gris", 1))
        cv.d.line([(cx + lado * 2, y_top - 2), (cx + lado * (2 + round(3 * s)), 0)], fill=K("gris", 3))   # raya del pliegue
        # el bajo del pantalón metido en la caña
        cv.rect(cx - ancho // 2 - 1, y_top - round(3 * s), cx + ancho // 2 + 1, y_top + 1, K("gris", 2))
        cv.hline(cx - ancho // 2 - 1, cx + ancho // 2 + 1, y_top + 1, K("gris", 0))
        _bota(cv, cx, y_suelo, s, lado)


def pasillo_suelo():
    cv = Canvas(W, H, bg=("gris", 9))
    cam = (0.25, 0.2)                       # (x, altura) de la cámara: a ras de suelo
    f, centro = 210, (300, 148)
    ancho, alto, fondo = (-1.0, 1.0), 2.5, 16.0

    def sup(u, v):
        hits = []
        if v < 0:
            hits.append((cam[1] / -v, "suelo"))
        if v > 0:
            hits.append(((alto - cam[1]) / v, "techo"))
        if u < 0:
            hits.append(((ancho[0] - cam[0]) / u, "izq"))
        if u > 0:
            hits.append(((ancho[1] - cam[0]) / u, "der"))
        z, cual = min(hits) if hits else (fondo + 1, "fondo")
        if z > fondo:
            z, cual = fondo, "fondo"
        X, Y = cam[0] + u * z, cam[1] + v * z
        if cual == "suelo":
            # linóleo blanco en losas de 50 cm, juntas finas que se pierden a lo lejos
            a, b = X / 0.5, z / 0.5
            da, db = abs(0.5 / f * z / 0.5), abs(z * z / cam[1] / f / 0.5)
            junta = (a % 1 < da * 1.0 and z < 9) or (b % 1 < db * 0.9)
            if junta:
                return K("gris", 8) if z < 6 else K("gris", 9)
            return K("gris", 10)
        if cual == "techo":
            # tubos fluorescentes cada 2,5 m en el eje del pasillo
            if abs(X) < 0.12 and (z % 2.5) < 1.2:
                return K("gris", 10)
            if abs(X) < 0.18 and (z % 2.5) < 1.3:
                return K("gris", 7)
            return K("gris", 8)
        if cual in ("izq", "der"):
            # azulejo de 25 cm, zócalo gris
            if Y < 0.08:
                return K("gris", 8)
            a, b = z / 0.25, Y / 0.25
            da = abs(z * z / abs((ancho[0] if cual == "izq" else ancho[1]) - cam[0]) / f / 0.25)
            db = abs(z / f / 0.25)
            if (a % 1 < da and z < 10) or b % 1 < db:
                return K("gris", 8)
            return K("gris", 9)
        # fondo: la puerta de acero del final del pasillo
        if -0.45 < X < 0.45 and Y < 2.0:
            if abs(X) < 0.02 or Y > 1.97:
                return K("gris", 5)
            return K("gris", 6)
        return K("gris", 9)

    _raycast(cv, cam, f, centro, sup)

    # una puerta lateral entreabierta, a medio pasillo (de ahí vienen)
    def proy(X, Y, z):
        return centro[0] + f * (X - cam[0]) / z, centro[1] - f * (Y - cam[1]) / z
    pts = [proy(-1.0, 0, 4.2), proy(-1.0, 2.0, 4.2), proy(-1.0, 2.0, 5.1), proy(-1.0, 0, 5.1)]
    cv.poly(pts, K("gris", 6))
    cv.poly([pts[0], pts[1], proy(-0.75, 2.0, 4.6), proy(-0.75, 0, 4.6)], K("gris", 7))   # la hoja, abierta
    cv.poly([proy(-1.0, 0.1, 4.25), proy(-1.0, 1.9, 4.25), proy(-1.0, 1.9, 5.05), proy(-1.0, 0.1, 5.05)], K("gris", 2))

    # salpicaduras: oscuras, pocas, aplastadas por la perspectiva
    rnd = random.Random(101)
    for (X, z, r) in [(0.05, 0.9, 0.05), (-0.15, 1.3, 0.035), (0.22, 0.75, 0.03), (0.4, 1.6, 0.04), (-0.05, 2.2, 0.05),
                      (0.12, 1.05, 0.02), (-0.28, 0.85, 0.018), (0.3, 1.1, 0.015)]:
        sx, sy = proy(X, 0, z)
        rw = max(1, round(f * r / z)); rh = max(1, round(rw * cam[1] / z * 1.2))
        cv.ellipse(round(sx - rw), round(sy - rh), round(sx + rw) + 1, round(sy + rh) + 1, K("gris", 3))
        for _ in range(3):                                                             # gotas sueltas
            gx, gy = sx + rnd.uniform(-rw * 2.5, rw * 2.5), sy + rnd.uniform(-rh * 2, rh * 2)
            cv.px(round(gx), round(gy), K("gris", 4))
    # un rastro arrastrado hacia la puerta
    for k in range(10):
        z = 1.8 + k * 0.25
        sx, sy = proy(-0.2 - k * 0.07, 0, z)
        cv.hline(round(sx) - 1, round(sx) + 2, round(sy), K("gris", 6))

    # las botas: un par lejos (a la derecha) y otro casi encima de la cámara (a la izquierda)
    for (X, z, sep) in ((0.62, 2.4, 0.26), (-0.42, 0.62, 0.24)):
        sx, sy = proy(X, 0, z)
        s = f / z / 100                                                                 # px por cm
        cv.ellipse(round(sx - sep * f / z / 2 - 9 * s), round(sy - 2 * s), round(sx + sep * f / z / 2 + 9 * s),
                   round(sy + 3 * s), K("gris", 8))                                     # el roce en el linóleo, no una sombra
        _piernas(cv, round(sx), round(sy), s, round(sep * f / z))
    return cv


# ================================================================ 5. habitación 101

def _altavoz(cv, x, y, s, lado):
    """Altavoz de bocina atornillado en una esquina; s = escala; lado = hacia dónde apunta (-1/+1)."""
    bw, bh = round(10 * s), round(8 * s)
    # soporte
    cv.rect(x - round(2 * s), y - round(6 * s), x + round(2 * s), y, K("gris", 2))
    # cuerpo y bocina, que se abre hacia el centro y hacia abajo
    cv.rect(x - bw // 2, y, x + bw // 2, y + bh, K("gris", 3)); cv.frame(x - bw // 2, y, x + bw // 2, y + bh, K("gris", 1))
    mx = x + lado * round(14 * s)
    pts = [(x + lado * bw // 2, y + 1), (mx, y - round(4 * s)), (mx, y + bh + round(9 * s)), (x + lado * bw // 2, y + bh - 1)]
    cv.poly(pts, K("gris", 4))
    cv.d.line([pts[0], pts[1]], fill=K("gris", 6)); cv.d.line([pts[3], pts[2]], fill=K("gris", 2))
    cv.ellipse(mx - round(3 * s), y - round(4 * s), mx + round(3 * s), y + bh + round(9 * s), K("gris", 1),
               outline=K("gris", 5))
    cv.ellipse(mx - round(1.5 * s), y + round(1 * s), mx + round(1.5 * s), y + bh + round(4 * s), K("gris", 0))
    if s > 1.5:                                                                          # cable
        cv.d.line([(x, y - round(6 * s)), (x - lado * round(10 * s), y - round(14 * s))], fill=K("gris", 1), width=2)


def habitacion101():
    cv = Canvas(W, H, bg=("gris", 1))
    cam = (0.0, 1.0)
    f, centro = 200, (240, 118)
    ancho, alto, fondo = (-3.2, 3.2), 1.62, 5.2
    hueco = (-0.42, 0.42, 2.2, 3.9, -0.6)                      # x0, x1, z0, z1, profundidad
    rnd = random.Random(101)
    manchas = [(rnd.uniform(-2.6, 2.6), rnd.uniform(1, 7), rnd.uniform(0.1, 0.35)) for _ in range(26)]

    def hormigon(a, b, base, ruido=True):
        """Tono de hormigón: tablilla de encofrado en a, manchas de humedad."""
        t = base
        if ruido and int(a * 7) % 3 == 0:
            t -= 1
        return t

    def sup(u, v):
        hits = []
        if v < 0:
            hits.append((cam[1] / -v, "suelo"))
        if v > 0:
            hits.append(((alto - cam[1]) / v, "techo"))
        if u < 0:
            hits.append(((ancho[0] - cam[0]) / u, "izq"))
        if u > 0:
            hits.append(((ancho[1] - cam[0]) / u, "der"))
        z, cual = min(hits) if hits else (fondo + 1, "fondo")
        if z > fondo:
            z, cual = fondo, "fondo"
        X, Y = cam[0] + u * z, cam[1] + v * z
        if cual == "suelo":
            hx0, hx1, hz0, hz1, hp = hueco
            if hx0 < X < hx1 and hz0 < z < hz1:
                # dentro del hueco: paredes del hueco o el fondo
                zb = (cam[1] - hp) / -v
                Xb = cam[0] + u * zb
                if zb > hz1:                                    # pared del fondo del hueco
                    yy = cam[1] + v * hz1
                    return K("gris", 3) if yy > -0.03 else K("gris", 2) if yy > -0.15 else K("gris", 1) if yy > hp * 0.6 else K("gris", 0)
                if Xb < hx0 or Xb > hx1:
                    return K("gris", 1)
                return K("gris", 0)
            # hormigón del suelo: losas grandes con juntas, polvo
            a, b = X / 1.2, z / 1.2
            da, db = abs(z / f / 1.2), abs(z * z / cam[1] / f / 1.2)
            if a % 1 < da or b % 1 < db * 0.9:
                return K("gris", 4)
            hx0, hx1, hz0, hz1, hp = hueco
            if hx0 - 0.03 < X < hx1 + 0.03 and hz0 - 0.03 < z < hz1 + 0.03:
                return K("gris", 6)                             # el canto del hueco, gastado
            return K("gris", 5)
        if cual == "techo":
            # encofrado de tablas a lo largo, con vigas cada 1,5 m: el techo pesa
            if (z % 1.5) < 0.18:
                return K("gris", 2) if (z % 1.5) < 0.05 else K("gris", 3)
            tabla = int((X + 3) / 0.22)
            return K("gris", 3 + (1 if tabla % 4 == 1 else 0) - (1 if tabla % 5 == 3 else 0))
        if cual in ("izq", "der"):
            if Y < 0.1:
                return K("gris", 2)
            a, b = z / 0.6, Y / 0.3
            da = abs(z * z / abs((ancho[0] if cual == "izq" else ancho[1]) - cam[0]) / f / 0.6)
            db = abs(z / f / 0.3)
            for (mx, mz, mr) in manchas:                        # chorretones de humedad
                if abs(mz - z) < mr * 0.08 and Y > alto - mr * 4:
                    return K("gris", 3)
            if a % 1 < da or b % 1 < db:
                return K("gris", 3)
            return K("gris", 4)
        # pared del fondo: bloques de hormigón y una puerta baja
        if 1.5 < X < 2.4 and Y < 1.5:
            return K("gris", 2) if X < 1.54 or X > 2.36 or Y > 1.46 else K("gris", 3)
        a, b = X / 0.6, Y / 0.3
        off = 0.5 if int(b) % 2 else 0
        if (a + off) % 1 < 1.2 * z / f / 0.6 or b % 1 < 1.2 * z / f / 0.3:
            return K("gris", 3)
        return K("gris", 4)

    _raycast(cv, cam, f, centro, sup)

    def proy(X, Y, z):
        return centro[0] + f * (X - cam[0]) / z, centro[1] - f * (Y - cam[1]) / z

    # guías de acero en las cuatro esquinas: el techo baja por ellas
    for X in (ancho[0] + 0.05, ancho[1] - 0.05):
        for z in (fondo - 0.05,):
            a, b = proy(X, 0, z), proy(X, alto, z)
            cv.rect(round(a[0]) - 1, round(b[1]), round(a[0]) + 2, round(a[1]), K("gris", 2))
            cv.vline(round(a[0]), round(b[1]), round(a[1]), K("gris", 5))
    # cadenas y la tolva colgando sobre el hueco
    zc = (hueco[2] + hueco[3]) / 2
    top_y, boca_y = alto, 0.82
    tw, bw = 0.95, 0.3                                         # semiancho arriba y en la boca
    d = 0.45                                                    # semifondo
    def P3(X, Y, z):
        x, y = proy(X, Y, z)
        return (round(x), round(y))
    # caras laterales (se ven por la perspectiva) y frontal
    cv.poly([P3(-tw, top_y, zc - d), P3(-tw, top_y, zc + d), P3(-bw, boca_y, zc + d * 0.4), P3(-bw, boca_y, zc - d * 0.4)], K("gris", 3))
    cv.poly([P3(tw, top_y, zc - d), P3(tw, top_y, zc + d), P3(bw, boca_y, zc + d * 0.4), P3(bw, boca_y, zc - d * 0.4)], K("gris", 4))
    frente = [P3(-tw, top_y, zc - d), P3(tw, top_y, zc - d), P3(bw, boca_y, zc - d * 0.4), P3(-bw, boca_y, zc - d * 0.4)]
    cv.poly(frente, K("gris", 6))
    cv.d.line([frente[0], frente[3]], fill=K("gris", 8)); cv.d.line([frente[1], frente[2]], fill=K("gris", 4))
    cv.d.line([frente[3], frente[2]], fill=K("gris", 3))
    # remaches y costuras de la chapa
    for t in (0.25, 0.55, 0.8):
        Y = top_y - (top_y - boca_y) * t
        hw = tw - (tw - bw) * t
        zz = zc - d + d * 0.6 * t
        a, b = P3(-hw, Y, zz), P3(hw, Y, zz)
        cv.hline(a[0] + 1, b[0], a[1], K("gris", 5))
        for k in range(a[0] + 4, b[0] - 2, 7):
            cv.px(k, a[1] - 2, K("gris", 8))
    # mirilla de inspección con los escombros dentro
    a, b = P3(-0.4, 1.4, zc - d * 0.85), P3(0.4, 1.18, zc - d * 0.85)
    cv.rect(a[0], a[1], b[0], b[1], K("gris", 1))
    for _ in range(40):
        ex, ey = rnd.randint(a[0] + 1, b[0] - 4), rnd.randint(a[1] + 1, b[1] - 3)
        cv.rect(ex, ey, ex + rnd.randint(2, 5), ey + rnd.randint(1, 3), K("granate", rnd.choice([1, 2, 3, 4])))
    for _ in range(30):
        cv.px(rnd.randint(a[0] + 1, b[0] - 1), rnd.randint(a[1] + 1, b[1] - 1), K("gris", rnd.choice([3, 5, 6])))
    for x in range(a[0] + 6, b[0], 8):                                                     # barrotes
        cv.vline(x, a[1], b[1], K("gris", 3))
    cv.frame(a[0] - 1, a[1] - 1, b[0] + 1, b[1] + 1, K("gris", 3))
    # la compuerta de la boca, cerrada, con cascotes asomando por la rendija
    bl, br_ = P3(-bw - 0.04, boca_y, zc - d * 0.4), P3(bw + 0.04, boca_y, zc - d * 0.4)
    cv.rect(bl[0], bl[1] - 2, br_[0], bl[1] + 4, K("gris", 2)); cv.hline(bl[0], br_[0], bl[1] - 2, K("gris", 5))
    for k in range(bl[0] + 2, br_[0] - 3, 5):
        cv.rect(k, bl[1] + 4, k + rnd.randint(2, 4), bl[1] + 5 + rnd.randint(0, 2), K("granate", rnd.choice([2, 3])))
    # palanca y cable de la compuerta
    pl = P3(bw + 0.05, boca_y + 0.1, zc - d * 0.4)
    cv.d.line([pl, (pl[0] + 14, pl[1] - 10)], fill=K("gris", 1), width=2)
    cv.d.line([(pl[0] + 14, pl[1] - 10), P3(1.2, alto, zc - 0.5)], fill=K("gris", 2))
    # cadenas al techo
    for X in (-tw * 0.8, tw * 0.8):
        p0, p1 = P3(X, alto, zc - d * 0.9), P3(X, top_y - 0.02, zc - d)
        for yy in range(min(p0[1], p1[1]) - 6, max(p0[1], p1[1]) + 1, 2):
            cv.px(p0[0], yy, K("gris", 6))
    # polvo que cae de la rendija, fino
    for k in range(14):
        cv.px(rnd.randint(bl[0] + 4, br_[0] - 4), bl[1] + 6 + rnd.randint(0, 26), K("gris", 6))
    # correas a los lados del hueco
    for X in (hueco[0] - 0.12, hueco[1] + 0.02):
        for z in (3.0, 3.6, 4.1):
            a = P3(X, 0, z); b = P3(X + 0.1, 0, z + 0.05)
            cv.rect(min(a[0], b[0]), a[1], max(a[0], b[0]) + 1, a[1] + 2, K("gris", 2))
            cv.px(max(a[0], b[0]), a[1], K("gris", 6))
    # silla de O'Brien, al borde
    sb = P3(1.05, 0, 3.0); st = P3(1.05, 0.45, 3.0); sr = P3(1.45, 0.45, 3.0); rt = P3(1.45, 0.95, 3.0)
    cv.rect(sb[0] + 2, sb[1] - 1, sr[0] + 3, sb[1] + 2, K("gris", 4))                       # roce en el suelo
    cv.rect(sb[0], st[1], sb[0] + 3, sb[1], K("gris", 2))                                   # patas de tubo
    cv.rect(sr[0] - 3, st[1], sr[0], sb[1], K("gris", 2))
    cv.rect(sb[0], st[1] - 2, sr[0], st[1] + 3, K("gris", 3)); cv.hline(sb[0], sr[0], st[1] - 2, K("gris", 6))   # asiento
    cv.rect(sr[0] - 4, rt[1], sr[0], st[1], K("gris", 3)); cv.vline(sr[0] - 4, rt[1], st[1], K("gris", 5))       # respaldo
    # altavoces en las cuatro esquinas: dos al fondo, dos encima de la cámara
    for X, lado in ((ancho[0] + 0.1, 1), (ancho[1] - 0.1, -1)):
        x, y = P3(X, alto - 0.1, fondo - 0.1)
        _altavoz(cv, x, y + 2, 0.9, lado)
    _altavoz(cv, 26, 14, 2.4, 1)
    _altavoz(cv, W - 26, 14, 2.4, -1)
    # una bombilla desnuda en el techo, sin pantalla
    bx, by = P3(-1.3, alto, 2.0)
    cv.vline(bx, by, by + 6, K("gris", 1)); cv.ellipse(bx - 2, by + 6, bx + 3, by + 11, K("papel", 4))
    cv.add_emissive(bx - 2, by + 6, bx + 3, by + 11)
    cv.glow_rgb = K("papel", 3)
    cv.add_glow_suave(bx, by + 8, 80, 0.12, squash=1.0)
    cv.bake_lighting()
    return cv


# ================================================================ 6. despacho del Partido Interior

RIO_MAPA = [(0, 7.0), (2, 7.4), (3.5, 8.3), (5, 8.6), (6.5, 8.3), (7.6, 9.0), (8.6, 9.1), (9.6, 8.7), (11, 8.2), (12, 8.6)]


def _rio_y(c):
    for (c0, f0), (c1, f1) in zip(RIO_MAPA, RIO_MAPA[1:]):
        if c0 <= c <= c1:
            return f0 + (f1 - f0) * (c - c0) / (c1 - c0)
    return RIO_MAPA[-1][1]


def _vista_londres(cv, x0, y0, x1, y1, rnd):
    """Todo Londres desde lo alto: cielo bajo, tejados, el río y las pirámides blancas de los ministerios."""
    for y in range(y0, y1):
        t = (y - y0) / (y1 - y0)
        cv.hline(x0, x1, y, K("cielo", 6 if t < 0.3 else 5 if t < 0.55 else 4))
    hz = y0 + (y1 - y0) * 58 // 100                                            # horizonte
    # pirámides de los ministerios, en terrazas, muy por encima de los tejados (luz por la izquierda)
    for (px_, base, w, hgt) in ((x0 + 32, hz + 8, 30, 40), (x0 + 80, hz + 6, 20, 26), (x0 + 128, hz + 10, 36, 50),
                                (x0 + 164, hz + 5, 14, 18)):
        paso = 4 if hgt > 30 else 3
        for k in range(0, hgt, paso):
            hw = max(1, round(w / 2 * (1 - k / hgt)))
            yb = base - k
            cv.rect(px_ - hw, yb - paso, px_, yb, K("papel", 4))
            cv.rect(px_, yb - paso, px_ + hw, yb, K("papel", 2))
            cv.hline(px_ - hw, px_ + hw, yb - paso, K("papel", 3))
            cv.px(px_ + hw - 1, yb - paso, K("papel", 1))
    # tejados en capas, cada vez más cerca y más oscuros
    for capa, (base, tono, hmin, hmax) in enumerate(((hz, 3, 1, 5), (hz + 6, 2, 2, 8), (hz + 15, 1, 3, 11))):
        x = x0
        while x < x1:
            w = rnd.randint(3, 9)
            h = rnd.randint(hmin, hmax)
            cv.rect(x, base - h, min(x1, x + w), y1, K("cielo", tono))
            if capa == 2 and rnd.random() < 0.3:
                cv.vline(x + 2, base - h - 3, base - h, K("cielo", 1))                       # chimenea
            x += w
    # el Támesis, plata, entre los tejados
    cv.poly([(x0, hz + 9), (x0 + 50, hz + 8), (x0 + 100, hz + 10), (x1, hz + 9), (x1, hz + 11), (x0 + 100, hz + 13),
             (x0 + 50, hz + 11), (x0, hz + 12)], K("cielo", 5))
    cv.hline(x0 + 20, x0 + 60, hz + 10, K("cielo", 6))
    # humo de un impacto, lejos, al este: una columna fina que se tuerce
    for i in range(14):
        cv.rect(x1 - 20 + i // 2, hz - 1 - i * 2, x1 - 17 + i // 2 + i // 5, hz + 1 - i * 2, K("cielo", 3))


def _mapa_impactos(cv, x0, y0, x1, y1, circulo, rnd):
    """El mapa del Registro de Impactos sobre la mesa: miles de chinchetas negras al este y al sur;
    junto al centro, un círculo blanco perfecto sin ninguna, con una cruz pequeña dentro (San Clemente)."""
    sx, sy = (x1 - x0) / 12, (y1 - y0) / 12

    def m2s(c, f):
        return x0 + c * sx, y0 + f * sy
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("madera", 1))                     # canto del papel sobre la mesa
    cv.rect(x0, y0, x1, y1, K("papel", 3))
    for c in range(1, 12):
        cv.vline(round(m2s(c, 0)[0]), y0, y1, K("papel", 2))
    for f in range(1, 12, 2):
        cv.hline(x0, x1, round(m2s(0, f)[1]), K("papel", 2))
    cv.frame(x0, y0, x1, y1, K("papel", 1))
    pts = [m2s(c, f) for c, f in RIO_MAPA]
    cv.d.line(pts, fill=K("cielo", 3), width=5)
    cv.d.line(pts, fill=K("cielo", 5), width=3)
    ccx, ccy, cr = circulo
    # chinchetas: densas al este y al sur del río; casi ninguna al noroeste
    n = 0
    while n < 1150:
        c, f = rnd.uniform(0, 12), rnd.uniform(0, 12)
        este = max(0.0, (c - 5.0) / 7.0)
        sur = 1.0 if f > _rio_y(c) + 0.15 else 0.0
        centro = 0.6 if (2.4 < c < 9 and 2.5 < f < 9.5) else 0.0
        p = 0.015 + 0.85 * max(este ** 1.2, sur * (0.5 + 0.5 * este), centro)
        if rnd.random() > p:
            continue
        x, y = round(m2s(c, f)[0]), round(m2s(c, f)[1])
        if (x - ccx) ** 2 + ((y - ccy) * 1.0) ** 2 <= (cr + 2) ** 2 or not (x0 + 1 < x < x1 - 1 and y0 + 2 < y < y1 - 1):
            continue
        cv.px(x, y, K("gris", 0)); cv.px(x + 1, y, K("gris", 1))                              # cabeza de la chincheta
        cv.px(x, y - 1, K("gris", 3))                                                          # brillo
        n += 1
    # el círculo blanco: perfecto, trazado a compás; dentro, una cruz pequeña
    cv.ellipse(ccx - cr, ccy - cr, ccx + cr + 1, ccy + cr + 1, K("papel", 4))
    cv.hline(ccx - 1, ccx + 2, ccy, K("gris", 3)); cv.vline(ccx, ccy - 1, ccy + 2, K("gris", 3))
    cv.text(x0 + 3, y0 + 3, "REGISTRO DE IMPACTOS", K("gris", 3))


def _cabeza(cv, cx, cy, w, h, piel=3):
    """Óvalo de cara con mandíbula, sombra a la derecha (la ventana queda a la izquierda)."""
    cv.ellipse(cx - w // 2, cy - h // 2, cx + w // 2 + 1, cy + h // 2 + 1, K("piel", piel))
    cv.ellipse(cx + w // 6, cy - h // 2 + 2, cx + w // 2 + 1, cy + h // 2, K("piel", piel - 1))
    cv.ellipse(cx - w // 2 + 2, cy - h // 2 + 3, cx + w // 6 + 1, cy + h // 2 - 2, K("piel", piel))


def _obrien(cv, x, y):
    """O'Brien de pie (x = eje, y = coronilla): corpulento, gafas, mono negro. El brazo derecho va aparte."""
    hombro = 31
    cv.poly([(x - hombro, y + 42), (x - hombro + 7, y + 31), (x - 9, y + 27), (x + 9, y + 27), (x + hombro - 7, y + 31),
             (x + hombro, y + 42), (x + hombro + 2, y + 150), (x - hombro - 2, y + 150)], K("gris", 1))
    # filo de luz de la ventana (contraluz) en el hombro y el brazo izquierdos
    cv.d.line([(x - hombro + 7, y + 31), (x - 9, y + 27)], fill=K("gris", 3))
    cv.d.line([(x - hombro, y + 42), (x - hombro + 7, y + 31)], fill=K("gris", 3))
    cv.poly([(x - 9, y + 27), (x, y + 38), (x + 9, y + 27), (x + 5, y + 27), (x, y + 32), (x - 5, y + 27)], K("gris", 2))  # cuello del mono
    cv.vline(x, y + 38, y + 150, K("gris", 2))                                                 # cremallera
    cv.rect(x - 23, y + 52, x - 11, y + 58, K("gris", 0)); cv.hline(x - 23, x - 11, y + 52, K("gris", 2))  # bolsillo
    cv.d.line([(x + 8, y + 70), (x + 22, y + 66)], fill=K("gris", 0))                         # pliegue
    # brazo izquierdo (a la derecha de la imagen), apoyado en la mesa con los nudillos
    cv.poly([(x + hombro, y + 42), (x + hombro + 9, y + 92), (x + hombro - 3, y + 96), (x + hombro - 9, y + 54)], K("gris", 1))
    cv.d.line([(x + hombro, y + 44), (x + hombro + 8, y + 92)], fill=K("gris", 0))
    # cuello de toro y cabeza grande
    cv.rect(x - 7, y + 20, x + 8, y + 29, K("piel", 2)); cv.vline(x + 5, y + 20, y + 28, K("piel", 1))
    _cabeza(cv, x, y + 14, 22, 26, piel=3)
    cv.poly([(x - 10, y + 18), (x - 8, y + 26), (x, y + 29), (x + 8, y + 26), (x + 11, y + 18)], K("piel", 3))   # mandíbula ancha
    cv.poly([(x + 4, y + 18), (x + 11, y + 18), (x + 8, y + 26), (x + 2, y + 28)], K("piel", 2))
    # pelo corto, negro, entrecano en las sienes
    cv.ellipse(x - 11, y, x + 12, y + 12, K("pelo", 0))
    cv.rect(x - 11, y + 5, x + 12, y + 8, K("pelo", 0))
    cv.rect(x - 11, y + 8, x - 9, y + 14, K("gris", 5)); cv.rect(x + 10, y + 8, x + 12, y + 14, K("gris", 4))
    cv.hline(x - 6, x + 5, y + 1, K("pelo", 2))
    # mira hacia abajo, al mapa: gafas con reflejo, cejas pesadas
    cv.hline(x - 8, x - 2, y + 11, K("pelo", 0)); cv.hline(x + 2, x + 8, y + 11, K("pelo", 0))
    for gx in (x - 8, x + 2):
        cv.rect(gx, y + 13, gx + 7, y + 18, K("cielo", 5)); cv.frame(gx, y + 13, gx + 7, y + 18, K("gris", 0))
        cv.hline(gx + 1, gx + 3, y + 14, K("papel", 4))
    cv.hline(x - 1, x + 2, y + 14, K("gris", 0))
    cv.vline(x, y + 18, y + 22, K("piel", 2)); cv.px(x + 1, y + 22, K("piel", 1))              # nariz
    cv.hline(x - 3, x + 4, y + 25, K("piel", 1))                                               # boca cerrada
    cv.px(x - 11, y + 15, K("piel", 2)); cv.px(x + 12, y + 15, K("piel", 1))                   # orejas


def _obrien_brazo(cv, x, y, mano):
    """El brazo derecho de O'Brien: del hombro al codo y del codo a la mano, que sostiene una chincheta
    (la punta queda en `mano`). Se dibuja después de la mesa: el brazo pasa por encima del borde."""
    hx, hy = mano
    hombro = (x - 25, y + 38)
    codo = (x - 36, y + 76)
    muneca = (hx + 2, hy - 10)
    cv.d.line([hombro, codo], fill=K("gris", 1), width=12)
    cv.d.line([codo, muneca], fill=K("gris", 1), width=11)
    cv.ellipse(codo[0] - 6, codo[1] - 6, codo[0] + 6, codo[1] + 6, K("gris", 1))
    cv.d.line([(hombro[0] - 6, hombro[1] + 2), (codo[0] - 6, codo[1])], fill=K("gris", 3))       # contraluz
    cv.d.line([(codo[0] - 6, codo[1]), (muneca[0] - 5, muneca[1])], fill=K("gris", 2))
    cv.rect(muneca[0] - 5, muneca[1] - 2, muneca[0] + 5, muneca[1] + 3, K("gris", 0))         # puño de la manga
    cv.ellipse(hx - 3, hy - 9, hx + 6, hy - 1, K("piel", 3)); cv.px(hx + 4, hy - 3, K("piel", 2))
    cv.hline(hx - 3, hx + 1, hy - 2, K("piel", 2))                                             # índice y pulgar, en pinza
    cv.vline(hx - 2, hy - 2, hy + 1, K("gris", 0)); cv.px(hx - 3, hy - 2, K("gris", 0)); cv.px(hx - 1, hy - 2, K("gris", 0))
    cv.px(hx - 2, hy - 2, K("gris", 3))                                                        # la chincheta, en el aire


def _voss(cv, x, y):
    """Voss sentado (x = eje, y = coronilla): más viejo, pelo gris repeinado, abrigo gris, guantes negros."""
    # respaldo alto del sillón
    cv.rect(x - 24, y - 6, x + 24, y + 60, K("granate", 1)); cv.frame(x - 24, y - 6, x + 24, y + 60, K("granate", 0))
    for bx in range(x - 20, x + 22, 8):
        for by in range(y - 2, y + 56, 8):
            cv.px(bx, by, K("granate", 3))                                                     # capitoné
    # abrigo gris, cruzado
    cv.poly([(x - 20, y + 36), (x - 14, y + 26), (x - 5, y + 23), (x + 5, y + 23), (x + 14, y + 26), (x + 20, y + 36),
             (x + 22, y + 70), (x - 22, y + 70)], K("gris", 5))
    cv.poly([(x - 20, y + 36), (x - 14, y + 26), (x - 5, y + 23), (x - 7, y + 30), (x - 17, y + 40), (x - 19, y + 70),
             (x - 22, y + 70)], K("gris", 6))
    cv.poly([(x - 5, y + 23), (x + 3, y + 40), (x + 9, y + 26), (x + 5, y + 23)], K("gris", 4))   # solapas
    cv.d.line([(x - 5, y + 23), (x + 3, y + 40)], fill=K("gris", 3)); cv.d.line([(x + 9, y + 26), (x + 3, y + 40)], fill=K("gris", 3))
    cv.poly([(x - 2, y + 23), (x + 3, y + 33), (x + 5, y + 23)], K("papel", 3))                 # camisa
    cv.vline(x + 1, y + 24, y + 31, K("gris", 1))                                              # corbata
    for by in (y + 46, y + 56):
        cv.px(x - 4, by, K("gris", 2)); cv.px(x + 6, by, K("gris", 2))                          # botones
    # cabeza fina, arrugas, pelo gris peinado hacia atrás
    cv.rect(x - 4, y + 17, x + 5, y + 24, K("piel", 2))
    _cabeza(cv, x, y + 11, 16, 21, piel=3)
    cv.ellipse(x - 8, y - 1, x + 9, y + 8, K("gris", 7))
    cv.rect(x - 8, y + 3, x + 9, y + 6, K("gris", 7))
    for k in range(-6, 8, 3):
        cv.vline(x + k, y, y + 5, K("gris", 6))                                                # surcos del peine
    cv.hline(x - 5, x + 6, y, K("gris", 8))
    cv.hline(x - 6, x - 2, y + 9, K("gris", 6)); cv.hline(x + 2, x + 6, y + 9, K("gris", 6))   # cejas canosas
    cv.px(x - 4, y + 11, K("gris", 1)); cv.px(x + 4, y + 11, K("gris", 1))                     # ojos
    cv.px(x - 5, y + 13, K("piel", 2)); cv.px(x + 5, y + 13, K("piel", 2))                     # bolsas
    cv.vline(x, y + 11, y + 15, K("piel", 2))
    cv.hline(x - 2, x + 3, y + 18, K("piel", 1)); cv.px(x - 3, y + 17, K("piel", 2)); cv.px(x + 3, y + 17, K("piel", 2))
    cv.d.line([(x - 5, y + 15), (x - 4, y + 18)], fill=K("piel", 2))                          # surco nasogeniano
    # manos enguantadas, cruzadas sobre la mesa
    cv.rect(x - 14, y + 62, x + 2, y + 70, K("gris", 0)); cv.rect(x - 2, y + 64, x + 14, y + 71, K("gris", 0))
    cv.hline(x - 13, x + 1, y + 62, K("gris", 2)); cv.hline(x - 1, x + 13, y + 64, K("gris", 2))
    cv.rect(x - 20, y + 60, x - 13, y + 69, K("gris", 5)); cv.rect(x + 13, y + 62, x + 20, y + 71, K("gris", 5))   # puños del abrigo


def _crane(cv, x, y):
    """Crane de pie en un rincón (x = eje, y = coronilla), con el sombrero en las manos. Sin sonrisa."""
    # piernas y zapatos
    cv.rect(x - 9, y + 70, x - 1, y + 120, K("tela", 2)); cv.rect(x + 1, y + 70, x + 9, y + 120, K("tela", 1))
    cv.vline(x - 6, y + 74, y + 118, K("tela", 3))
    cv.rect(x - 11, y + 118, x - 1, y + 123, K("madera", 0)); cv.rect(x + 1, y + 118, x + 11, y + 123, K("madera", 0))
    cv.hline(x - 10, x - 3, y + 118, K("madera", 2))
    # camisa y chaleco granate
    cv.poly([(x - 15, y + 30), (x - 10, y + 24), (x + 10, y + 24), (x + 15, y + 30), (x + 14, y + 72), (x - 14, y + 72)], K("papel", 3))
    cv.poly([(x - 11, y + 27), (x - 3, y + 26), (x, y + 44), (x + 3, y + 26), (x + 11, y + 27), (x + 11, y + 72), (x - 11, y + 72)],
            K("granate", 4))
    cv.vline(x - 10, y + 28, y + 72, K("granate", 5))
    cv.vline(x, y + 26, y + 46, K("granate", 1))                                             # corbata
    for by in (y + 48, y + 56, y + 64):
        cv.px(x + 1, by, K("ocre", 3))
    cv.hline(x - 11, x + 11, y + 70, K("granate", 2))
    # brazos: mangas de camisa, manos juntas delante
    cv.poly([(x - 15, y + 30), (x - 18, y + 58), (x - 8, y + 62), (x - 10, y + 36)], K("papel", 3))
    cv.poly([(x + 15, y + 30), (x + 18, y + 58), (x + 8, y + 62), (x + 10, y + 36)], K("papel", 2))
    # el sombrero, sujeto por el ala con las dos manos
    cv.ellipse(x - 14, y + 54, x + 15, y + 66, K("madera", 1))
    cv.ellipse(x - 9, y + 50, x + 10, y + 62, K("madera", 2))
    cv.hline(x - 8, x + 9, y + 58, K("gris", 1))                                               # cinta
    cv.ellipse(x - 12, y + 58, x - 4, y + 65, K("piel", 3)); cv.ellipse(x + 4, y + 58, x + 12, y + 65, K("piel", 2))
    # cabeza: pelo gris, mirada baja, la boca recta
    cv.rect(x - 4, y + 18, x + 5, y + 25, K("piel", 2))
    _cabeza(cv, x, y + 12, 16, 21, piel=3)
    cv.ellipse(x - 8, y, x + 9, y + 8, K("gris", 4)); cv.rect(x - 8, y + 4, x - 6, y + 12, K("gris", 4))
    cv.rect(x + 7, y + 4, x + 9, y + 12, K("gris", 3))
    cv.hline(x - 5, x - 2, y + 12, K("piel", 1)); cv.hline(x + 2, x + 5, y + 12, K("piel", 1))  # párpados bajos
    cv.vline(x, y + 12, y + 16, K("piel", 2))
    cv.hline(x - 2, x + 3, y + 19, K("piel", 1))
    cv.px(x - 8, y + 13, K("piel", 2))


def despacho_obrien(crane=False):
    rnd = random.Random(1984)
    cv = Canvas(W, H, bg=("madera", 1))
    # paneles de madera noble hasta el techo
    cv.rect(0, 0, W, 132, K("madera", 2))
    for x in range(-10, W, 52):
        cv.frame(x + 4, 8, x + 48, 62, K("madera", 1)); cv.hline(x + 5, x + 47, 9, K("madera", 3))
        cv.frame(x + 4, 70, x + 48, 124, K("madera", 1)); cv.hline(x + 5, x + 47, 71, K("madera", 3))
    cv.rect(0, 0, W, 4, K("madera", 1)); cv.rect(0, 64, W, 68, K("madera", 3)); cv.hline(0, W, 67, K("madera", 1))
    cv.rect(0, 124, W, 132, K("madera", 1)); cv.hline(0, W, 124, K("madera", 3))               # zócalo
    # la ventana de verdad: alta, con todo Londres
    wx0, wy0, wx1, wy1 = 160, 10, 360, 114
    cv.rect(wx0 - 6, wy0 - 6, wx1 + 6, wy1 + 8, K("madera", 1))
    _vista_londres(cv, wx0, wy0, wx1, wy1, rnd)
    for mx in (wx0 + 66, wx0 + 133):
        cv.rect(mx - 1, wy0, mx + 2, wy1, K("madera", 1))
    cv.rect(wx0, wy0 + 34, wx1, wy0 + 36, K("madera", 1))
    cv.rect(wx0 - 8, wy1 + 2, wx1 + 8, wy1 + 7, K("madera", 4)); cv.hline(wx0 - 8, wx1 + 8, wy1 + 6, K("madera", 2))
    for (cx0, cx1) in ((wx0 - 22, wx0 - 4), (wx1 + 4, wx1 + 22)):                              # cortinas pesadas
        cv.rect(cx0, wy0 - 8, cx1, wy1 + 14, K("granate", 2))
        for k in range(cx0 + 3, cx1, 5):
            cv.vline(k, wy0 - 8, wy1 + 14, K("granate", 1)); cv.vline(k + 1, wy0 - 8, wy1 + 14, K("granate", 3))
    # telepantalla APAGADA: cristal negro, sin piloto
    tx0, ty0, tx1, ty1 = 394, 26, 458, 74
    cv.rect(tx0 - 4, ty0 - 4, tx1 + 4, ty1 + 7, K("gris", 2)); cv.frame(tx0 - 4, ty0 - 4, tx1 + 4, ty1 + 7, K("gris", 1))
    cv.rect(tx0, ty0, tx1, ty1, K("gris", 0))
    cv.d.line([(tx0 + 4, ty0 + 14), (tx0 + 16, ty0 + 2)], fill=K("gris", 2))                  # reflejo de la ventana
    cv.d.line([(tx0 + 4, ty0 + 20), (tx0 + 22, ty0 + 2)], fill=K("gris", 1))
    cv.px(tx1 - 1, ty1 + 4, K("gris", 1))
    # un retrato del Gran Hermano a la izquierda, en marco dorado
    cv.rect(60, 18, 112, 84, K("ocre", 2)); cv.frame(60, 18, 112, 84, K("ocre", 1)); cv.hline(61, 111, 19, K("ocre", 3))
    cv.rect(64, 22, 108, 80, K("papel", 2))
    P.cara_gran_hermano(cv, 74, 34)
    # alfombra
    cv.rect(0, 132, W, H, K("granate", 2))
    cv.rect(20, 140, W - 20, H, K("granate", 3)); cv.frame(26, 146, W - 26, H + 4, K("ocre", 1))
    for x in range(34, W - 30, 10):
        cv.px(x, 142, K("ocre", 2))
    if crane:
        _crane(cv, 34, 96)
    vx, vy = 112, 98
    _voss(cv, vx, vy)
    ox, oy = 268, 66
    _obrien(cv, ox, oy)
    # la mesa: tablero de nogal con el mapa encima
    mx0, my0, mx1, my1 = 64, 156, 416, 234
    cv.rect(mx0 + 4, my1 + 22, mx1 + 6, my1 + 30, K("granate", 1))                            # sombra en la alfombra
    cv.rect(mx0, my0, mx1, my1, K("madera", 3)); cv.frame(mx0, my0, mx1, my1, K("madera", 1))
    cv.hline(mx0 + 1, mx1 - 1, my0 + 1, K("madera", 5))
    cv.rect(mx0, my1, mx1, my1 + 24, K("madera", 2)); cv.hline(mx0, mx1, my1, K("madera", 1))
    for k in range(mx0 + 8, mx1 - 8, 70):
        cv.frame(k, my1 + 4, k + 62, my1 + 20, K("madera", 1)); cv.rect(k + 27, my1 + 11, k + 35, my1 + 13, K("ocre", 2))
    circulo = (232, 186, 9)
    _mapa_impactos(cv, 140, my0 + 5, 384, my1 - 5, circulo, random.Random(7))
    # el café de verdad, una carpeta y la caja de chinchetas
    cv.ellipse(390, 196, 406, 206, K("papel", 2)); cv.ellipse(392, 192, 404, 202, K("papel", 4), outline=K("papel", 1))
    cv.ellipse(394, 194, 402, 200, K("madera", 0)); cv.px(405, 196, K("papel", 3))
    for k in range(3):
        cv.px(398 + k % 2, 188 - k * 2, K("papel", 3))
    cv.rect(392, 168, 408, 178, K("gris", 3)); cv.frame(392, 168, 408, 178, K("gris", 1))
    for k in range(6):
        cv.px(394 + k * 2, 171 + k % 3, K("gris", 0))
    cv.rect(78, 196, 116, 226, K("papel", 1)); cv.rect(80, 194, 118, 224, K("ocre", 1)); cv.frame(80, 194, 118, 224, K("ocre", 0))
    cv.rect(90, 202, 108, 206, K("rojo", 3))
    # las manos enguantadas de Voss, sobre la mesa
    cv.rect(vx - 14, vy + 66, vx + 2, vy + 73, K("gris", 0)); cv.rect(vx - 2, vy + 68, vx + 14, vy + 75, K("gris", 0))
    cv.hline(vx - 13, vx + 1, vy + 66, K("gris", 2)); cv.hline(vx - 1, vx + 13, vy + 68, K("gris", 2))
    cv.rect(vx - 20, vy + 63, vx - 13, vy + 73, K("gris", 5)); cv.rect(vx + 13, vy + 65, vx + 20, vy + 75, K("gris", 5))
    # nudillos de O'Brien sobre la mesa y su brazo derecho, con la chincheta sobre el círculo
    cv.ellipse(ox + 34, oy + 92, ox + 46, oy + 99, K("piel", 3)); cv.hline(ox + 35, ox + 45, oy + 95, K("piel", 2))
    _obrien_brazo(cv, ox, oy, (circulo[0] + 2, circulo[1] - 13))
    # luz: la ventana por detrás, el resto en penumbra silenciosa
    cv.add_light_fn(lambda x, y: -1 if (x < 140 or x > 380) and y < 132 else 0)
    cv.glow_rgb = K("cielo", 6)
    cv.add_glow_suave(260, 100, 220, 0.12, squash=1.3, pasos=12)
    cv.bake_lighting()
    return cv


def despacho_obrien_crane():
    return despacho_obrien(crane=True)


# ================================================================ 7. patio de Limehouse (epílogo del Final D)

def _ladrillo_calido(cv, x0, y0, x1, y1, rnd, rampa="granate", base=4):
    cv.rect(x0, y0, x1, y1, K(rampa, base - 1))
    for fila, y in enumerate(range(y0, y1, 4)):
        off = (fila % 2) * 4
        for x in range(x0 - off, x1, 8):
            c = K(rampa, base + rnd.choice([0, 0, 0, -1, 1])) if rnd.random() > 0.08 else K("ocre", 2)
            cv.rect(max(x0, x + 1), y + 1, min(x1, x + 7), min(y1, y + 3), c)


def _cuerda(cv, x0, y0, x1, y1, comba=6):
    pts = []
    for k in range(0, 41):
        t = k / 40
        pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + comba * 4 * t * (1 - t)))
    cv.d.line(pts, fill=K("gris", 4))
    return lambda x: y0 + (y1 - y0) * ((x - x0) / (x1 - x0)) + comba * 4 * ((x - x0) / (x1 - x0)) * (1 - (x - x0) / (x1 - x0))


def _prendas(cv, cuerda, x0, x1, rnd, sabanas=False, libre=None):
    colores = [("ocre", 3), ("granate", 5), ("cielo", 5), ("papel", 4), ("pared", 5), ("tela", 4), ("ocre", 4), ("rojo", 4)]
    x = x0
    while x < x1 - 8:
        y = round(cuerda(x)) + 1
        r, b = rnd.choice(colores)
        corto = libre is not None and libre[0] - 40 < x < libre[1]                           # no tapar la ventana
        if (sabanas or rnd.random() < 0.25) and not corto:
            w, h = rnd.randint(28, 40), rnd.randint(30, 40)
            r, b = ("papel", 4)
            cv.poly([(x, y), (x + w, round(cuerda(x + w)) + 1), (x + w + 1, y + h + 2), (x + w // 2, y + h + 4), (x - 1, y + h)], K(r, b))
            cv.vline(x + w // 3, y + 2, y + h, K("papel", 3)); cv.vline(x + 2 * w // 3, y + 3, y + h + 1, K("papel", 3))
            cv.d.line([(x - 1, y + h), (x + w // 2, y + h + 4), (x + w + 1, y + h + 2)], fill=K("papel", 2))
        elif rnd.random() < 0.5 and not corto:
            w, h = 16, 14                                                                     # camisa
            cv.rect(x, y, x + w, y + h, K(r, b)); cv.rect(x - 3, y, x + 1, y + 7, K(r, b)); cv.rect(x + w - 1, y, x + w + 3, y + 7, K(r, b))
            cv.vline(x + w // 2, y + 1, y + h, K(r, b - 1)); cv.hline(x, x + w, y + h - 1, K(r, b - 1))
        else:
            w, h = rnd.randint(8, 12), rnd.randint(10, 16) if not corto else rnd.randint(6, 9)   # trapo, calcetín, enaguas
            cv.rect(x, y, x + w, y + h, K(r, b)); cv.vline(x + w - 1, y, y + h, K(r, b - 1))
        cv.px(x + 1, y - 1, K("madera", 4)); cv.px(x + w - 2, round(cuerda(x + w)) , K("madera", 4))   # pinzas
        x += w + rnd.randint(3, 7)


def _nina(cv, x, y, s=1.5):
    """Niña de unos ocho años, de perfil hacia la derecha, de puntillas, prendiendo una sábana (y = pies)."""
    def P_(dx, dy):
        return (round(x + dx * s), round(y + dy * s))

    def R(dx0, dy0, dx1, dy1, col):
        (a, b), (c, d) = P_(dx0, dy0), P_(dx1, dy1)
        cv.rect(a, b, c, d, col)
    # piernas, calcetines y zapatos
    R(-4, -18, -1, -2, K("piel", 3)); R(1, -18, 4, -3, K("piel", 2))
    R(-4, -7, -1, -2, K("papel", 4)); R(1, -8, 4, -3, K("papel", 3))
    R(-5, -3, 1, 0, K("madera", 1)); R(1, -4, 6, -1, K("madera", 1))
    # vestido de cuadros desvaídos, abierto en campana
    cv.poly([P_(-7, -40), P_(5, -40), P_(10, -16), P_(-11, -16)], K("ocre", 3))
    cv.poly([P_(1, -40), P_(5, -40), P_(10, -16), P_(3, -16)], K("ocre", 2))
    for k in range(-37, -17, 5):
        a, b = P_(-9 - k // 8, k), P_(8 + k // 10, k)
        cv.hline(a[0], b[0], a[1], K("granate", 4))
    R(-7, -30, 6, -28, K("papel", 4)); R(-10, -30, -6, -25, K("papel", 4))                  # delantal atado
    R(-11, -31, -8, -29, K("rojo", 4))                                                        # lazo
    # brazos en alto, hacia la cuerda
    cv.d.line([P_(-2, -38), P_(5, -58)], fill=K("piel", 3), width=round(2 * s))
    cv.d.line([P_(3, -38), P_(11, -56)], fill=K("piel", 2), width=round(2 * s))
    cv.ellipse(*P_(3, -61), *P_(7, -57), K("piel", 3)); cv.ellipse(*P_(9, -59), *P_(13, -55), K("piel", 2))   # manos
    # cabeza levantada, cantando
    cv.ellipse(*P_(-6, -54), *P_(7, -40), K("piel", 3))
    cv.rect(*P_(6, -49), *P_(8, -47), K("piel", 3)); cv.px(*P_(7, -47), K("piel", 2))         # nariz
    cv.rect(*P_(4, -44), *P_(6, -43), K("granate", 1))                                        # boca abierta
    cv.rect(*P_(3, -49), *P_(4, -48), K("pelo", 0))                                           # ojo
    cv.rect(*P_(0, -46), *P_(2, -45), K("granate", 5))                                        # mejilla
    # pelo castaño claro con trenza a la espalda y un lazo
    cv.ellipse(*P_(-8, -57), *P_(5, -50), K("madera", 4))
    R(-7, -53, -2, -44, K("madera", 4)); R(-5, -56, 2, -55, K("madera", 6))
    cv.px(*P_(-1, -48), K("piel", 2))                                                         # oreja
    for k in range(5):
        R(-8 - k / 2, -44 + k * 3, -5 - k / 2, -41 + k * 3, K("madera", 3 + k % 2))
    R(-10, -29 + 0, -7, -27, K("madera", 3))
    R(-11, -30, -6, -29, K("rojo", 4))


def _notas(cv, x, y):
    """Tres notas que suben y se las lleva el aire (la canción)."""
    for k, (dx, dy) in enumerate([(0, 0), (10, -9), (21, -15)]):
        nx, ny = x + dx, y + dy
        cv.ellipse(nx, ny + 4, nx + 4, ny + 7, K("papel", 4 - (k == 2)))
        cv.vline(nx + 3, ny - 2, ny + 5, K("papel", 4 - (k == 2)))
        if k != 1:
            cv.px(nx + 4, ny - 2, K("papel", 4)); cv.px(nx + 5, ny - 1, K("papel", 4))


def _dot_ventana(cv, x, y):
    """Dot en la ventana de la cocina (x = eje, y = coronilla): pañuelo rojo de lunares, pelo canoso."""
    cv.poly([(x - 15, y + 40), (x - 12, y + 24), (x - 5, y + 21), (x + 5, y + 21), (x + 12, y + 24), (x + 15, y + 40)], K("pared", 4))
    cv.poly([(x - 5, y + 30), (x + 5, y + 30), (x + 6, y + 40), (x - 6, y + 40)], K("papel", 3))   # pechera del delantal
    cv.d.line([(x - 5, y + 30), (x - 4, y + 22)], fill=K("papel", 3)); cv.d.line([(x + 5, y + 30), (x + 4, y + 22)], fill=K("papel", 3))
    cv.rect(x - 3, y + 17, x + 4, y + 23, K("piel", 2))
    cv.ellipse(x - 7, y + 3, x + 8, y + 20, K("piel", 3))
    cv.rect(x + 3, y + 6, x + 8, y + 18, K("piel", 2))
    cv.rect(x - 7, y + 8, x - 4, y + 15, K("gris", 8)); cv.rect(x + 5, y + 8, x + 8, y + 14, K("gris", 7))    # pelo canoso
    cv.ellipse(x - 9, y, x + 10, y + 11, K("granate", 3))                                    # pañuelo
    cv.rect(x - 9, y + 5, x + 10, y + 9, K("granate", 3))
    for (dx, dy) in [(-5, 2), (0, 1), (5, 3), (-2, 6), (3, 7), (-7, 7), (7, 6)]:
        cv.px(x + dx, y + dy, K("papel", 4))
    cv.poly([(x + 8, y + 7), (x + 13, y + 11), (x + 9, y + 12)], K("granate", 2))           # nudo
    cv.px(x - 3, y + 12, K("pelo", 0)); cv.px(x + 3, y + 12, K("pelo", 0))                  # ojos que sonríen
    cv.hline(x - 4, x - 2, y + 11, K("piel", 2)); cv.hline(x + 2, x + 4, y + 11, K("piel", 2))
    cv.d.line([(x - 2, y + 16), (x, y + 17), (x + 3, y + 16)], fill=K("piel", 1))          # media sonrisa
    cv.px(x - 5, y + 14, K("granate", 5)); cv.px(x + 5, y + 14, K("granate", 4))
    # brazos fuertes apoyados en el alféizar
    cv.rect(x - 16, y + 34, x - 4, y + 40, K("piel", 3)); cv.rect(x + 4, y + 34, x + 16, y + 40, K("piel", 2))


def _len_ventana(cv, x, y):
    """Len a su lado: mayor y fornido, el ancla tatuada en el cuello, leyendo el libro cosido con hilo."""
    cv.poly([(x - 20, y + 42), (x - 17, y + 25), (x - 7, y + 21), (x + 7, y + 21), (x + 17, y + 25), (x + 20, y + 42)], K("tela", 2))
    cv.poly([(x - 20, y + 42), (x - 17, y + 25), (x - 7, y + 21), (x - 9, y + 28), (x - 17, y + 42)], K("tela", 3))
    cv.poly([(x - 5, y + 21), (x, y + 28), (x + 5, y + 21)], K("papel", 2))                  # cuello de la camisa
    cv.rect(x - 5, y + 15, x + 6, y + 23, K("piel", 2))
    # el ancla en el cuello
    cv.vline(x + 3, y + 16, y + 21, K("azul", 2)); cv.hline(x + 2, x + 5, y + 17, K("azul", 2))
    cv.px(x + 1, y + 20, K("azul", 2)); cv.px(x + 5, y + 20, K("azul", 2)); cv.hline(x + 2, x + 5, y + 21, K("azul", 2))
    # cabeza grande, mirando abajo; pelo gris cortísimo
    cv.ellipse(x - 9, y + 1, x + 10, y + 20, K("piel", 2))
    cv.rect(x + 3, y + 4, x + 10, y + 18, K("piel", 1))
    cv.ellipse(x - 9, y, x + 10, y + 8, K("gris", 6)); cv.rect(x - 9, y + 4, x - 7, y + 10, K("gris", 6))
    cv.hline(x - 5, x - 1, y + 10, K("gris", 4)); cv.hline(x + 2, x + 6, y + 10, K("gris", 4))
    cv.hline(x - 5, x - 2, y + 12, K("pelo", 0)); cv.hline(x + 2, x + 5, y + 12, K("pelo", 0))   # ojos bajos, leyendo
    cv.vline(x, y + 11, y + 15, K("piel", 1)); cv.hline(x - 2, x + 3, y + 17, K("piel", 0))
    cv.rect(x - 3, y + 2, x + 5, y + 3, K("piel", 3))                                          # una venda vieja, ya no
    # el fajo de papeles cosidos con hilo, sostenido con las dos manos
    cv.rect(x - 14, y + 28, x + 14, y + 42, K("papel", 3)); cv.rect(x - 13, y + 27, x + 13, y + 40, K("papel", 4))
    for k in range(y + 30, y + 39, 2):
        cv.hline(x - 9, x + 10 - (k % 3) * 3, k, K("gris", 6))
    for k in range(y + 28, y + 40, 3):
        cv.px(x - 12, k, K("granate", 2))                                                     # puntadas del hilo
    cv.vline(x - 12, y + 27, y + 41, K("papel", 2))
    cv.rect(x - 19, y + 32, x - 12, y + 40, K("piel", 2)); cv.rect(x + 12, y + 32, x + 19, y + 40, K("piel", 1))


def patio_limehouse(len_=False):
    rnd = random.Random(1990)
    cv = Canvas(W, H, bg=("cielo", 6))
    # cielo de mañana limpia, con un calor de sol bajo
    for i, y in enumerate(range(0, 40, 5)):
        cv.rect(0, y, W, y + 5, K("cielo", 6) if i < 4 else K("ocre", 4))
    # tejados y chimeneas al fondo
    cv.poly([(0, 34), (120, 22), (240, 34)], K("granate", 2)); cv.poly([(220, 36), (360, 18), (480, 32), (480, 40), (220, 40)], K("granate", 2))
    for (cx, cy) in [(60, 18), (180, 20), (300, 12), (420, 16)]:
        cv.rect(cx, cy, cx + 10, cy + 20, K("granate", 3)); cv.rect(cx - 1, cy - 2, cx + 11, cy, K("granate", 4))
        cv.rect(cx + 2, cy - 6, cx + 4, cy - 2, K("ocre", 2)); cv.rect(cx + 6, cy - 5, cx + 8, cy - 2, K("ocre", 2))
    # la casa del fondo: ladrillo cálido, recién soleado
    _ladrillo_calido(cv, 0, 36, W, 206, rnd, rampa="granate", base=4)
    cv.rect(0, 36, W, 40, K("granate", 2))                                                   # alero
    # la puerta verde del patio, con su escalón de piedra
    cv.rect(52, 128, 90, 206, K("pared", 2)); cv.rect(55, 131, 87, 204, K("pared", 5))
    cv.frame(59, 136, 83, 166, K("pared", 4)); cv.frame(59, 172, 83, 200, K("pared", 4))
    cv.vline(55, 131, 204, K("pared", 6)); cv.px(83, 170, K("ocre", 4)); cv.px(83, 171, K("ocre", 3))
    cv.rect(48, 204, 94, 210, K("papel", 2)); cv.hline(48, 94, 204, K("papel", 3))
    # una tina de zinc colgada y un bajante
    cv.rect(234, 40, 238, 206, K("gris", 5)); cv.vline(234, 40, 206, K("gris", 7))
    for by in (70, 120, 170):
        cv.rect(232, by, 240, by + 2, K("gris", 4))
    cv.ellipse(410, 120, 456, 146, K("gris", 6), outline=K("gris", 4)); cv.ellipse(414, 124, 452, 142, K("gris", 7))
    cv.hline(420, 446, 126, K("gris", 8))
    # la ventana de la cocina, pintada de verde, con macetas de geranios
    wx0, wy0, wx1, wy1 = 284, 88, 392, 150
    cv.rect(wx0 - 4, wy0 - 4, wx1 + 4, wy1 + 2, K("pared", 3))
    cv.rect(wx0, wy0, wx1, wy1, K("madera", 1))
    cv.rect(wx0, wy0, wx1, wy0 + 20, K("madera", 2))
    for k in range(wx0 + 8, wx1 - 8, 12):                                                    # tazas en la balda, al fondo
        cv.rect(k, wy0 + 14, k + 5, wy0 + 19, K("papel", 3))
    cv.hline(wx0, wx1, wy0 + 19, K("madera", 3))
    if len_:
        _dot_ventana(cv, 318, 102)
        _len_ventana(cv, 360, 98)
    else:
        _dot_ventana(cv, 336, 102)
    # el marco de guillotina, abierto: la hoja de arriba
    cv.rect(wx0, wy0, wx1, wy0 + 4, K("pared", 5)); cv.hline(wx0, wx1, wy0 + 4, K("pared", 3))
    cv.rect(wx0 - 6, wy1, wx1 + 6, wy1 + 6, K("papel", 3)); cv.hline(wx0 - 6, wx1 + 6, wy1 + 5, K("papel", 1))  # alféizar
    for (fx, c) in [(wx0 - 2, 4), (wx1 - 10, 5)]:                                            # geranios
        cv.rect(fx, wy1 - 6, fx + 10, wy1, K("granate", 3)); cv.hline(fx, fx + 10, wy1 - 6, K("granate", 4))
        cv.ellipse(fx - 2, wy1 - 16, fx + 12, wy1 - 5, K("pared", 4))
        for (dx, dy) in [(1, -14), (6, -15), (9, -12), (3, -10)]:
            cv.px(fx + dx, wy1 + dy, K("rojo", c)); cv.px(fx + dx + 1, wy1 + dy, K("rojo", c - 1))
    # suelo del patio: losas y adoquines claros, un cubo, una escoba
    P.adoquines(cv, 0, 206, W, H, semilla=12, rampa="papel", base=2)
    cv.rect(0, 206, W, 208, K("granate", 2))
    cv.rect(110, 236, 128, 252, K("gris", 6)); cv.ellipse(110, 232, 128, 240, K("gris", 7), outline=K("gris", 5))
    cv.ellipse(112, 234, 126, 239, K("cielo", 5))
    cv.d.line([(440, 160), (452, 230)], fill=K("madera", 3), width=2)
    cv.poly([(446, 226), (458, 224), (462, 240), (446, 242)], K("ocre", 2))
    # ropa tendida de lado a lado, en tres cuerdas
    c1 = _cuerda(cv, -4, 46, W + 4, 56, comba=10)
    _prendas(cv, c1, 6, W - 6, rnd, libre=(280, 400))
    c2 = _cuerda(cv, -4, 82, 250, 70, comba=8)
    _prendas(cv, c2, 120, 240, rnd)
    # la cuerda baja, donde la niña prende las sábanas
    c3 = _cuerda(cv, 10, 138, 280, 134, comba=6)
    cv.rect(278, 128, 282, 206, K("madera", 2)); cv.vline(278, 128, 206, K("madera", 4))   # el palo de la cuerda
    for (sx, w, h) in ((22, 44, 46), (178, 40, 44)):
        y = round(c3(sx)) + 1
        cv.poly([(sx, y), (sx + w, round(c3(sx + w)) + 1), (sx + w + 2, y + h), (sx + w // 2, y + h + 5), (sx - 1, y + h + 2)], K("papel", 4))
        cv.vline(sx + w // 3, y + 2, y + h, K("papel", 3)); cv.vline(sx + 2 * w // 3, y + 3, y + h + 2, K("papel", 3))
        cv.px(sx + 1, y - 1, K("madera", 4)); cv.px(sx + w - 2, round(c3(sx + w)), K("madera", 4))
    # la sábana que está prendiendo ahora: aún suelta de un lado, el viento la abomba
    sx = 112
    y = round(c3(sx)) + 1
    cv.poly([(sx, y), (sx + 46, round(c3(sx + 46)) + 1), (sx + 52, y + 26), (sx + 44, y + 50), (sx + 14, y + 52), (sx + 4, y + 30)], K("papel", 4))
    cv.d.line([(sx + 30, y + 3), (sx + 36, y + 48)], fill=K("papel", 3))
    cv.d.line([(sx + 4, y + 30), (sx + 14, y + 52), (sx + 44, y + 50)], fill=K("papel", 2))
    cv.px(sx + 44, round(c3(sx + 44)), K("madera", 4))
    # sombras en el suelo (la luz viene de la derecha y de arriba)
    for (a, b) in ((20, 70), (108, 166), (176, 222)):
        cv.poly([(a - 6, 222), (b - 6, 222), (b - 12, 230), (a - 12, 230)], K("papel", 1))
    _nina(cv, 100, 226)
    _notas(cv, 128, 122)
    # luz de mañana: sol cálido en lo alto de la pared, el patio aún en sombra suave
    cv.add_light_fn(lambda x, y: 1 if (36 <= y < 206 and y < 230 - (W - x) * 0.45) else 0)
    cv.add_light_fn(lambda x, y: 1 if y >= 206 and x > 200 + (y - 206) * 1.2 else 0)
    cv.glow_rgb = K("ocre", 4)
    cv.add_glow_suave(420, 40, 300, 0.16, squash=0.9, pasos=10)
    cv.bake_lighting()
    return cv


def patio_limehouse_len():
    return patio_limehouse(len_=True)


# ================================================================ 8. los Dos Minutos de Odio, años después

def _cara_enemigo(femenina):
    """La cara del protagonista, envejecida y convertida en cara de enemigo (96x96, en sus colores).
    Parte del retrato del crimen facial: mismas capas, con canas, gafas, arrugas, la boca torcida
    y la mirada de lado. Devuelve (Canvas, color_de_fondo)."""
    import retrato_protagonista as RP
    cv = Canvas(RP.S, RP.S, bg=("pared", 1))
    if femenina:
        RP.pelo(cv, femenino=True)
    RP.hombros(cv)
    RP.cuello(cv, tendones=True)
    RP.cabeza(cv, femenina=femenina)
    if not femenina:
        RP.pelo(cv)
    else:
        cv.poly([(28, 34), (30, 22), (38, 12), (50, 9), (62, 13), (68, 24), (68, 32), (62, 24), (54, 28),
                 (44, 24), (34, 30)], K("madera", 2))
        cv.poly([(24, 30), (30, 28), (32, 40), (31, 56), (28, 68), (22, 62)], K("madera", 2))
        cv.poly([(72, 30), (66, 28), (65, 40), (66, 56), (69, 68), (75, 62)], K("madera", 1))
    # canas: el pelo pasa a gris, con mechones claros
    px = cv.img.load()
    pelo = {K("pelo", i): K("gris", 4 + i * 2) for i in range(4)}
    pelo.update({K("madera", i): K("gris", 3 + i) for i in range(1, 5)})
    for y in range(RP.S):
        for x in range(RP.S):
            if px[x, y] in pelo and (y < 40 or x < 30 or x > 66):
                px[x, y] = pelo[px[x, y]]
    RP.nariz(cv, aletas=True)
    # mirada de traidor: ojos estrechos, de lado; una ceja hundida y la otra arriba
    for cx, lado in ((38, 1), (58, -1)):
        RP.ojo(cv, cx, 46, lado, apertura=2, mirada=(2, 0), inclinacion=2, pestanas=femenina)
    RP.ceja(cv, 38, 38, 1, alza=-2, inclinacion=3, color=K("gris", 5))
    RP.ceja(cv, 58, 38, -1, alza=2, inclinacion=-1, color=K("gris", 5))
    RP.boca(cv, "mueca", femenina=femenina)
    cv.d.line([(42, 61), (38, 64)], fill=K("piel", 0))                                       # comisura caída
    # gafas de montura gruesa
    for gx in (31, 51):
        cv.frame(gx, 41, gx + 15, 51, K("gris", 1)); cv.frame(gx + 1, 42, gx + 14, 50, K("gris", 2))
    cv.hline(46, 51, 44, K("gris", 1))
    cv.hline(23, 31, 43, K("gris", 1)); cv.hline(66, 73, 43, K("gris", 1))
    # arrugas de la edad: frente, patas de gallo, surcos, papada
    for y in (27, 31):
        cv.d.line([(36, y), (44, y - 1), (52, y), (60, y - 1)], fill=K("piel", 2))
    for (a, b) in (((29, 46), (26, 44)), ((29, 48), (26, 50)), ((68, 46), (71, 44)), ((68, 48), (71, 50))):
        cv.d.line([a, b], fill=K("piel", 1))
    cv.d.line([(41, 53), (37, 60), (38, 64)], fill=K("piel", 1)); cv.d.line([(55, 53), (60, 59)], fill=K("piel", 1))
    cv.d.line([(40, 69), (48, 71), (56, 69)], fill=K("piel", 1))
    cv.rect(33, 52, 38, 54, K("piel", 2)); cv.rect(58, 52, 63, 54, K("piel", 1))              # ojeras
    # sombra dura desde abajo, de cartel de propaganda
    for y in range(RP.S):
        for x in range(RP.S):
            c = px[x, y]
            if c in LOOKUP and LOOKUP[c][0] == "piel" and (x > 56 or y > 62):
                px[x, y] = K("piel", LOOKUP[c][1] - 1)
    return cv, K("pared", 1)


def _a_tele(img, fondo):
    """Pasa una imagen a los verdes de la telepantalla según su luminancia; el fondo queda transparente."""
    from PIL import Image
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    src, dst = img.load(), out.load()
    for y in range(img.height):
        for x in range(img.width):
            c = src[x, y]
            if c == fondo:
                continue
            l = (0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]) / 255
            i = max(1, min(6, round(l * 6.6 + 0.4)))
            dst[x, y] = K("tele", i) + (255,)
    return out


def _soldados(cv, x0, y0, x1, y1, rnd):
    """Columnas de soldados estasiáticos que avanzan, con banderas amarillas, en los verdes de la pantalla."""
    for fila, (yb, esc, tono) in enumerate(((y0 + 44, 0.7, 1), (y0 + 70, 0.95, 2), (y0 + 104, 1.3, 2), (y0 + 150, 1.75, 3))):
        paso = round(8 * esc)
        for x in range(x0 + 2 + rnd.randint(0, paso // 2), x1 - round(6 * esc) - 2, paso):
            h = round(24 * esc)
            cv.rect(x, yb - h, x + round(5 * esc), yb, K("tele", tono))                              # cuerpo
            cv.rect(x - 1, yb - h - round(4 * esc), x + round(5 * esc) + 1, yb - h, K("tele", tono + 1))   # casco
            cv.hline(x - 1, x + round(5 * esc) + 1, yb - h - round(4 * esc), K("tele", tono + 2))
            cv.vline(x + round(5 * esc), yb - h - round(8 * esc), yb - h + round(8 * esc), K("tele", tono + 2))   # fusil al hombro
        if fila < 3:
            for bx in range(x0 + rnd.randint(0, 30), x1, round(70 * esc)):                           # banderas amarillas
                mast = yb - round(44 * esc)
                cv.vline(bx, mast, yb - round(20 * esc), K("tele", tono + 2))
                cv.poly([(bx + 1, mast), (bx + round(16 * esc), mast + round(2 * esc)), (bx + round(15 * esc), mast + round(10 * esc)),
                         (bx + 1, mast + round(9 * esc))], K("ocre", 3 if fila == 0 else 4))
                cv.d.line([(bx + 1, mast + round(9 * esc)), (bx + round(15 * esc), mast + round(10 * esc))], fill=K("ocre", 2))


def _espectador(cv, x, y, esc, rnd, puno=False):
    """Funcionario de espaldas: cabeza y hombros (y = base de los hombros)."""
    ropa = rnd.choice([("azul", 2), ("azul", 2), ("azul", 1), ("azul", 3), ("gris", 2)])
    pelo = rnd.choice([("pelo", 0), ("pelo", 1), ("pelo", 2), ("madera", 2), ("ocre", 1), ("gris", 5), ("gris", 7)])
    w = round(9 * esc)
    cv.rect(x - w, y - round(9 * esc), x + w, y + round(4 * esc), K(*ropa))
    cv.hline(x - w, x + w, y - round(9 * esc), K(ropa[0], ropa[1] + 1))
    cv.ellipse(x - round(5 * esc), y - round(20 * esc), x + round(5 * esc), y - round(7 * esc), K(*pelo))
    cv.rect(x - round(2 * esc), y - round(9 * esc), x + round(3 * esc), y - round(7 * esc), K("piel", 2))   # nuca
    if puno:
        lado = rnd.choice([-1, 1])
        bx = x + lado * round(8 * esc)
        cv.d.line([(bx, y - round(8 * esc)), (bx + lado * round(3 * esc), y - round(26 * esc))], fill=K(*ropa), width=max(2, round(3 * esc)))
        cv.ellipse(bx + lado * round(3 * esc) - round(2 * esc), y - round(31 * esc), bx + lado * round(3 * esc) + round(3 * esc),
                   y - round(25 * esc), K("piel", 3))


def _hilda(cv, x, y):
    """Hilda, más vieja, de pie en primera fila, el brazo estirado: acaba de lanzar su zapato (y = cintura)."""
    cv.rect(x - 9, y - 22, x + 9, y + 6, K("azul", 2)); cv.hline(x - 9, x + 9, y - 22, K("azul", 3))
    cv.vline(x - 9, y - 20, y + 6, K("azul", 1))
    cv.rect(x - 11, y - 19, x - 7, y - 15, K("rojo", 4))                                       # brazalete
    cv.d.line([(x + 7, y - 20), (x + 16, y - 34), (x + 26, y - 42)], fill=K("azul", 2), width=4)   # brazo lanzando
    cv.ellipse(x + 24, y - 46, x + 30, y - 40, K("piel", 3))
    cv.d.line([(x - 8, y - 18), (x - 14, y - 6)], fill=K("azul", 1), width=3)
    cv.rect(x - 3, y - 25, x + 3, y - 21, K("piel", 2))
    cv.ellipse(x - 6, y - 36, x + 6, y - 23, K("gris", 6))                                    # pelo canoso, tirante
    cv.ellipse(x - 4, y - 42, x + 4, y - 34, K("gris", 7)); cv.px(x - 1, y - 40, K("gris", 8))   # el moño
    cv.hline(x - 5, x + 5, y - 30, K("gris", 5))
    cv.px(x + 6, y - 29, K("piel", 2))                                                        # oreja


def salon_odio_final(femenina=False):
    rnd = random.Random(2004)
    cv = Canvas(W, H, bg=("gris", 0))
    # paredes del salón, en penumbra, con los estandartes
    cv.rect(0, 0, W, 170, K("papel", 1))
    for x in range(0, W, 36):
        cv.vline(x, 0, 170, K("papel", 0))
    for sx in (14, 432):
        cv.rect(sx, 6, sx + 34, 150, K("rojo", 3)); cv.vline(sx + 17, 12, 140, K("papel", 3))
        cv.poly([(sx, 150), (sx + 17, 160), (sx + 34, 150)], K("rojo", 3))
    # la telepantalla gigante
    tx0, ty0, tx1, ty1 = 64, 6, 416, 160
    cv.rect(tx0 - 6, ty0 - 4, tx1 + 6, ty1 + 6, K("gris", 1)); cv.frame(tx0 - 6, ty0 - 4, tx1 + 6, ty1 + 6, K("gris", 0))
    cv.rect(tx0, ty0, tx1, ty1, K("tele", 0))
    _soldados(cv, tx0, ty0, tx1, ty1, rnd)
    # la cara, a 2x, recortada de la coronilla al pecho, encima de los soldados
    cara, fondo = _cara_enemigo(femenina)
    tele = _a_tele(cara.img.crop((8, 4, 88, 81)), fondo)
    from PIL import Image
    tele = tele.resize((tele.width * 2, tele.height * 2), Image.NEAREST)
    cv.img.paste(tele, ((tx0 + tx1) // 2 - tele.width // 2, ty0), tele)
    # rótulo
    rot = "TRAIDORA" if femenina else "TRAIDOR"
    cv.rect(tx0, ty1 - 20, tx1, ty1, K("tele", 1)); cv.hline(tx0, tx1, ty1 - 20, K("tele", 4))
    L.texto_grande(cv, (tx0 + tx1) // 2 - L.ancho_grande(rot, 3) // 2, ty1 - 17, rot, K("tele", 6), escala=3)
    P.lineas_barrido(cv, tx0, ty0, tx1, ty1)
    cv.add_emissive(tx0, ty0, tx1, ty1)
    # el suelo y las hileras de espaldas, de la primera (lejos) a la última (aquí)
    cv.rect(0, 166, W, H, K("madera", 1))
    filas = [(178, 0.75), (196, 0.95), (218, 1.2), (246, 1.55), (282, 2.0)]
    for i, (y, esc) in enumerate(filas):
        paso = round(22 * esc)
        x = rnd.randint(-paso // 2, 0) + (paso // 2 if i % 2 else 0)
        while x < W + paso:
            if i == 0 and 128 < x < 168:                                                         # hueco de Hilda
                x += paso
                continue
            _espectador(cv, x, y, esc, rnd, puno=rnd.random() < 0.3)
            x += paso
        if i == 0:
            _hilda(cv, 146, 176)
    # el zapato, volando hacia la pantalla
    zx, zy = 206, 98
    for k, (a, b) in enumerate(((0.45, 0.58), (0.64, 0.74), (0.8, 0.88))):                       # estela, a trazos
        hx, hy = 176, 128
        cv.d.line([(round(hx + (zx - hx) * a), round(hy + (zy - hy) * a)), (round(hx + (zx - hx) * b), round(hy + (zy - hy) * b))],
                  fill=K("tele", 4 + k))
    zapato = ["..oooo.......",
              ".obllbo......",
              ".obbbbbo.....",
              ".obbbbbboooo.",
              "obbbbbbbbllbo",
              "obbbbbbbbbbbo",
              "osssssssssso.",
              "oss.........."]
    cv.grid(zx - 6, zy - 4, zapato, {"o": K("madera", 0), "b": K("madera", 2), "l": K("madera", 4), "s": K("gris", 1)})
    # luz: todo el salón bañado por la pantalla
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(240, 100, 300, 0.32, squash=1.2, pasos=10)
    cv.bake_lighting()
    return cv


def salon_odio_h():
    return salon_odio_final(femenina=False)


def salon_odio_m():
    return salon_odio_final(femenina=True)


# ================================================================ 9. Limehouse por la mañana

def _ventana_manana(cv, wx, wy, rnd, abierta=False):
    """Ventana de guillotina a la luz de la mañana: cristal que refleja el cielo, a veces abierta."""
    cv.rect(wx, wy, wx + 12, wy + 16, K("cielo", 5))
    cv.rect(wx, wy, wx + 12, wy + 3, K("cielo", 6)); cv.d.line([(wx + 2, wy + 14), (wx + 8, wy + 4)], fill=K("cielo", 6))
    cv.vline(wx + 6, wy, wy + 16, K("madera", 2)); cv.hline(wx, wx + 12, wy + 8, K("madera", 2))
    cv.hline(wx - 1, wx + 13, wy + 16, K("papel", 3))
    if abierta:
        cv.rect(wx, wy + 8, wx + 12, wy + 16, K("madera", 1))
        cv.rect(wx + 1, wy + 9, wx + 11, wy + 13, K("granate", 3))                                 # cortina
    if rnd.random() < 0.35:                                                                      # maceta
        cv.rect(wx + 2, wy + 13, wx + 7, wy + 16, K("granate", 3)); cv.px(wx + 3, wy + 12, K("rojo", 4)); cv.px(wx + 5, wy + 11, K("pared", 5))


def _cantante(cv, wx, wy):
    """Una mujer asomada a la ventana, cantando (wx, wy = esquina de la ventana)."""
    cv.rect(wx, wy, wx + 12, wy + 16, K("madera", 1))
    cv.ellipse(wx + 2, wy + 2, wx + 10, wy + 10, K("piel", 3))
    cv.ellipse(wx + 1, wy + 1, wx + 11, wy + 6, K("ocre", 2)); cv.rect(wx + 1, wy + 3, wx + 3, wy + 9, K("ocre", 2))   # pelo recogido
    cv.px(wx + 5, wy + 6, K("pelo", 0)); cv.px(wx + 8, wy + 6, K("pelo", 0))
    cv.rect(wx + 6, wy + 8, wx + 8, wy + 10, K("granate", 1))                                   # boca abierta
    cv.rect(wx + 1, wy + 10, wx + 11, wy + 16, K("tela", 3))
    cv.rect(wx - 2, wy + 13, wx + 4, wy + 16, K("piel", 3)); cv.rect(wx + 8, wy + 13, wx + 14, wy + 16, K("piel", 2))   # brazos en el alféizar
    cv.hline(wx - 1, wx + 13, wy + 16, K("papel", 3))
    _notas(cv, wx + 16, wy - 2)


def _rayuela(cv, x, y):
    """Una rayuela pintada con tiza en los adoquines."""
    casillas = [(0, 0), (0, -9), (-6, -18), (6, -18), (0, -27), (-6, -36), (6, -36), (0, -45)]
    for (dx, dy) in casillas:
        cv.frame(x + dx - 6, y + dy - 8, x + dx + 6, y + dy + 1, K("papel", 4))
    cv.text(x - 1, y - 6, "1", K("papel", 3)); cv.text(x - 1, y - 51, "8", K("papel", 3))


def limehouse_manana():
    import elenco as E
    import limehouse as LH
    rnd = random.Random(1999)
    cv = Canvas(W, H)
    FACHADA, CALLE = LH.FACHADA, LH.CALLE
    # cielo de mañana: azul pálido arriba, sol cálido sobre los tejados
    for i, y in enumerate(range(0, 48, 6)):
        cv.rect(0, y, W, y + 6, (K("cielo", 5), K("cielo", 6), K("cielo", 6), K("papel", 4), K("ocre", 4), K("ocre", 4),
                                  K("ocre", 3), K("ocre", 3))[i])
    for (nx, ny, nw) in [(40, 8, 46), (210, 4, 60), (360, 12, 38)]:                             # nubes de buen tiempo
        cv.ellipse(nx, ny, nx + nw, ny + 8, K("papel", 4)); cv.hline(nx + 6, nx + nw - 6, ny + 7, K("papel", 3))
    # casas adosadas (las mismas de la calle), con las ventanas a la luz del día
    x, n = -20, 0
    casas = []
    while x < W:
        w = rnd.randint(64, 88)
        if 270 <= x < 370:
            w = 92
        top = rnd.randint(26, 40)
        LH.casa(cv, x, w, top, rnd, puerta_verde=(n == 1), luz=0.0)
        casas.append((x, w, top))
        x += w
        n += 1
    cv.emissive.clear()
    abiertas = 0
    for (x, w, top) in casas:
        for wx in range(x + 8, x + w - 14, 22):
            abierta = rnd.random() < 0.3
            _ventana_manana(cv, wx, top + 10, rnd, abierta)
    # el pub «La Campana» (abriendo), con la puerta de par en par
    px_ = 288
    cv.rect(px_, 60, px_ + 74, FACHADA, K("madera", 2)); cv.frame(px_, 60, px_ + 74, FACHADA, K("madera", 0))
    cv.rect(px_ + 4, 64, px_ + 70, 74, K("granate", 3)); cv.text(px_ + 37 - cv.text_width("LA CAMPANA") // 2, 66, "LA CAMPANA", K("ocre", 4))
    for wx in (px_ + 6, px_ + 52):
        cv.rect(wx, 78, wx + 16, 96, K("cielo", 5)); cv.vline(wx + 8, 78, 96, K("madera", 0)); cv.hline(wx, wx + 16, 87, K("madera", 0))
    cv.rect(px_ + 28, FACHADA - 30, px_ + 46, FACHADA, K("madera", 0)); cv.rect(px_ + 29, FACHADA - 29, px_ + 33, FACHADA, K("madera", 3))
    cv.ellipse(px_ + 33, 52, px_ + 41, 60, K("ocre", 4), outline=K("ocre", 2)); cv.hline(px_ + 30, px_ + 44, 52, K("gris", 2))
    # alguien canta en una ventana de arriba
    cx_, cw_, ctop = casas[1]
    _cantante(cv, cx_ + 8, ctop + 10)
    # el mercado, reconstruido a medias: un puesto con toldo y un andamio de tablones
    cv.rect(392, 70, 394, FACHADA + 30, K("madera", 2)); cv.rect(452, 70, 454, FACHADA + 30, K("madera", 2))
    for yy in (70, 88):
        cv.rect(390, yy, 456, yy + 3, K("madera", 4)); cv.hline(390, 456, yy + 3, K("madera", 1))
    cv.d.line([(394, 73), (452, 88)], fill=K("madera", 1))
    # ropa tendida de lado a lado
    for (a, b, y) in [(-4, 120, 30), (130, 280, 26), (370, 486, 32)]:
        LH.ropa_tendida(cv, a, b, y, rnd)
    # calle
    P.adoquines(cv, 0, FACHADA, W, CALLE, semilla=8, rampa="papel", base=2)
    cv.ellipse(380, 196, 420, 204, K("cielo", 5)); cv.hline(388, 410, 198, K("cielo", 6))     # un charco que brilla
    _rayuela(cv, 120, 214)
    # el puesto del mercado: toldo a rayas, cajas de verdura
    cv.rect(392, FACHADA + 2, 456, FACHADA + 26, K("madera", 3)); cv.hline(392, 456, FACHADA + 2, K("madera", 5))
    for k, xx in enumerate(range(394, 454, 10)):
        cv.rect(xx, FACHADA + 4, xx + 8, FACHADA + 12, K(("ocre", "granate", "pared", "ocre", "rojo", "pared")[k % 6], 3))
    for k in range(0, 66, 8):
        cv.rect(390 + k, FACHADA - 8, 394 + k, FACHADA, K("papel", 4) if (k // 8) % 2 else K("granate", 4))
    # niños: dos juegan a la rayuela, uno corre con un aro
    nino_pal = {**E.PIEL(0), "c": K("tela", 1), "C": K("tela", 3), "n": K("ocre", 0), "d": K("ocre", 1),
                "b": K("ocre", 3), "p": K("madera", 2), "g": K("gris", 7), **E.BOTAS}
    nina_pal = {**E.PIEL(1), "o": K("madera", 2), "h": K("madera", 4), "H": K("madera", 5), "n": K("granate", 2),
                "d": K("granate", 3), "b": K("granate", 5), "p": K("granate", 4), "r": K("papel", 4), **E.BOTAS}
    nina2_pal = {**E.PIEL(-1), "o": K("pelo", 0), "h": K("pelo", 1), "H": K("pelo", 3), "n": K("pared", 2),
                 "d": K("pared", 4), "b": K("pared", 5), "p": K("pared", 4), "r": K("ocre", 4), **E.BOTAS}
    for (sx, sy, filas, pal) in ((96, 172, E.NINA, nina_pal), (138, 186, E.NINA, nina2_pal), (236, 168, E.NINO, nino_pal)):
        cv.ellipse(sx + 2, sy + 24, sx + 15, sy + 29, K("gris", 3))
        cv.grid(sx, sy, filas, pal)
    cv.ellipse(254, 172, 270, 196, None, outline=K("madera", 1))                                # el aro
    cv.d.line([(250, 182), (258, 186)], fill=K("madera", 1))
    # gente: una vecina con la cesta en el puesto y un viejo que pasa
    for (nombre, sx, sy) in (("prole1", 404, 104), ("viejo", 330, 140)):
        import npcs as N
        filas, pal = N.NPCS[nombre]
        cv.ellipse(sx + 2, sy + 36, sx + 18, sy + 42, K("papel", 1))
        cv.grid(sx, sy, filas, pal)
    cv.rect(398, 128, 408, 134, K("madera", 3)); cv.d.arc([398, 122, 408, 132], 180, 360, fill=K("madera", 2))   # cesta
    # un gato al sol en un escalón
    cv.rect(198, 104, 206, 108, K("ocre", 2)); cv.rect(204, 101, 208, 105, K("ocre", 2)); cv.px(204, 100, K("ocre", 2)); cv.px(207, 100, K("ocre", 2))
    cv.d.line([(198, 106), (194, 104)], fill=K("ocre", 2))
    # bordillo y muro bajo de enfrente
    cv.rect(0, CALLE, W, CALLE + 4, K("gris", 4)); cv.hline(0, W, CALLE, K("gris", 7))
    LH.ladrillo(cv, 0, CALLE + 4, W, H, rnd, base=3)
    for fx in (150, 470):
        P.farola(cv, fx, 168, encendida=False)
    # luz de mañana: sol bajo por el este (derecha), sombra fresca bajo los aleros
    cv.add_light_fn(lambda x, y: 1 if (y < FACHADA and y > 20) or (FACHADA <= y < CALLE and x > 120 + (y - FACHADA) * 0.8) else 0)
    cv.add_light(0, FACHADA, W, FACHADA + 8, -1)
    cv.glow_rgb = K("ocre", 4)
    cv.add_glow_suave(470, 30, 420, 0.22, squash=1.0, pasos=10)
    cv.bake_lighting()
    return cv


# ================================================================ export

def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    hechos = []
    for nombre, fn in (("pasillo_suelo", pasillo_suelo), ("habitacion101", habitacion101),
                       ("despacho_obrien", despacho_obrien), ("despacho_obrien_crane", despacho_obrien_crane),
                       ("patio_limehouse", patio_limehouse), ("patio_limehouse_len", patio_limehouse_len),
                       ("salon_odio_h", salon_odio_h), ("salon_odio_m", salon_odio_m),
                       ("limehouse_manana", limehouse_manana)):
        fn().img.save(destino / f"{nombre}.png"); hechos.append(nombre)
    return hechos
