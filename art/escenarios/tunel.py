"""J13.02 — Los túneles del metro cerrado (960x270, la cámara sigue al jugador).

Pared de ladrillo que se curva en bóveda, raíles oxidados, traviesas y agua (verde casi negro). La luz es tenue
y uniforme: el juego oscurece la escena por encima y la alumbra con la linterna de dinamo.

Variantes:
  None        — el túnel base (tramos de paso).
  "nichos"    — tramo 1: cuatro nichos de seguridad con su franja blanca descolorida.
  "derrumbe"  — tramo 3: el techo hundido, un hueco estrecho abajo y el puntal podrido.
  "carteles"  — tramo 4: túnel seco con carteles de antes de la Revolución y un plano de la red.
"""
import math
import random

from pixel import Canvas, K
import _luz as L

W, H = 960, 270
BOVEDA, MURO, LECHO, BORDE = 0, 100, 100, 230       # bóveda/pared y=0..100, lecho y=100..230, borde por debajo
RAILES = (150, 178)
NICHOS = [140, 380, 620, 860]                        # x0 de cada nicho (36 px de ancho, hueco y 40..100)
NICHO_W, NICHO_Y0 = 36, 40
DERRUMBE = (600, 100, 700, 200)                      # huella del montón de cascotes (hueco libre: y 200..230)
PUNTAL = (712, 40, 722, 110)                         # huella (710,100)-(724,108)
CARTELES = {"te": (120, 30, 180, 90), "teatro": (300, 30, 360, 90), "playa": (520, 30, 580, 90),
            "nina": (700, 28, 760, 92)}
PLANO = (850, 30, 940, 90)
LAMPARAS = [60, 270, 470, 800]                       # apliques muertos bajo la bóveda


# ---------------------------------------------------------------- pared y bóveda


def _ladrillo_boveda(cv, rnd):
    """Hiladas de ladrillo que se estrechan hacia arriba: la pared se curva y se convierte en techo."""
    y = 0
    filas = []
    alto = 2
    while y < MURO:
        filas.append((y, alto))
        y += alto
        if y > 6:
            alto = 3
        if y > 22:
            alto = 4
    for i, (y, h) in enumerate(filas):
        # en lo alto, más hollín (tonos más bajos)
        base = 1 if y < 10 else (2 if y < 26 else 2)
        cv.hline(0, W, y, K("granate", 0))
        largo = 4 + h * 2
        off = (i % 2) * (largo // 2)
        for x in range(-off, W, largo):
            b = base + rnd.choice([0, 0, 0, 1, -1])
            if rnd.random() < 0.08:
                c = K("gris", 1 + (y > 20))                     # ladrillo renegrido
            else:
                c = K("granate", b)
            cv.rect(max(0, x + 1), y + 1, min(W, x + largo), min(MURO, y + h), c)
    # la línea de arranque de la bóveda (donde la curva se hace pared)
    cv.hline(0, W, 24, K("granate", 0)); cv.hline(0, W, 25, K("granate", 3))
    # chorretones de humedad y salitre
    for _ in range(30):
        sx = rnd.randint(0, W - 2)
        sy = rnd.randint(26, 60)
        largo = rnd.randint(8, 40)
        col = K("pared", rnd.choice([0, 1])) if rnd.random() < 0.8 else K("papel", 0)
        for k in range(largo):
            if rnd.random() < 0.85:
                cv.px(sx + (k // 9) % 2, sy + k, col)
    # zócalo de hormigón al pie de la pared
    cv.rect(0, 92, W, MURO, K("gris", 2)); cv.hline(0, W, 92, K("gris", 4)); cv.hline(0, W, MURO - 1, K("gris", 1))
    for x in range(0, W, 48):
        cv.vline(x, 93, MURO - 1, K("gris", 1))


def _cables(cv, rnd):
    """Haz de cables viejos colgado bajo la bóveda, con ménsulas cada 40 px."""
    for k, (yb, col) in enumerate(((19, K("gris", 1)), (21, K("gris", 2)), (23, K("madera", 0)))):
        y = yb
        pts = []
        for x in range(0, W + 40, 40):
            pts += [(x, yb), (x + 20, yb + 2 + k % 2)]
        cv.d.line(pts, fill=col)
    for x in range(0, W, 40):
        cv.rect(x, 17, x + 2, 25, K("gris", 3)); cv.px(x, 17, K("gris", 5))


def _lampara(cv, x):
    """Aplique de mamparo, muerto, con la rejilla oxidada."""
    cv.rect(x - 4, 8, x + 5, 16, K("gris", 2)); cv.frame(x - 4, 8, x + 5, 16, K("gris", 1))
    cv.rect(x - 2, 10, x + 3, 14, K("cielo", 1))
    cv.vline(x, 10, 14, K("gris", 1)); cv.hline(x - 2, x + 3, 12, K("gris", 1))
    cv.px(x - 1, 10, K("cielo", 3))
    cv.px(x + 4, 15, K("madera", 3)); cv.px(x + 4, 16, K("madera", 2))


# ---------------------------------------------------------------- lecho de vías


def _lecho(cv, rnd):
    cv.rect(0, LECHO, W, BORDE, K("gris", 2))
    for _ in range(W * 9):                                                         # balasto
        x, y = rnd.randint(0, W - 2), rnd.randint(LECHO, BORDE - 2)
        b = rnd.choice([1, 2, 3, 3, 4])
        cv.px(x, y, K("gris", b))
        if b >= 3:
            cv.px(x + 1, y, K("gris", b - 1))
    # cuneta junto al zócalo
    cv.rect(0, LECHO, W, LECHO + 6, K("gris", 1)); cv.hline(0, W, LECHO + 6, K("gris", 3))
    # traviesas
    for x in range(4, W, 14):
        xx = x + rnd.randint(-1, 1)
        y0, y1 = RAILES[0] - 10, RAILES[1] + 10
        b = rnd.choice([1, 2, 2])
        cv.rect(xx, y0, xx + 7, y1, K("madera", b))
        cv.vline(xx, y0, y1, K("madera", b + 1)); cv.vline(xx + 6, y0, y1, K("madera", 0))
        cv.hline(xx, xx + 7, y1, K("gris", 0))
        if rnd.random() < 0.25:                                                    # traviesa partida
            yy = rnd.randint(y0 + 6, y1 - 6)
            cv.hline(xx, xx + 7, yy, K("madera", 0))


def _railes(cv, rnd, tono=None):
    for ry in RAILES:
        cv.hline(0, W, ry + 2, K("gris", 0))                                       # sombra del patín
        cv.rect(0, ry - 1, W, ry + 2, K("gris", 3))
        cv.hline(0, W, ry - 1, K("gris", 5))
        cv.hline(0, W, ry + 1, K("gris", 1))
        for x in range(0, W, 7):                                                   # óxido
            if rnd.random() < 0.55:
                w = rnd.randint(2, 7)
                cv.hline(x, x + w, ry, K("madera", rnd.choice([2, 3])))
            if rnd.random() < 0.3:
                cv.hline(x, x + rnd.randint(2, 5), ry - 1, K("ocre", 1))
        for x in range(10, W, 14):                                                 # sujeciones a la traviesa
            cv.px(x, ry + 2, K("gris", 4)); cv.px(x + 3, ry + 2, K("gris", 4))
        for x in range(0, W, 120):                                                 # bridas de junta
            cv.rect(x, ry - 1, x + 6, ry + 2, K("gris", 4)); cv.px(x + 1, ry, K("gris", 1)); cv.px(x + 4, ry, K("gris", 1))


CHARCOS = [(30, 116, 120, 140), (160, 160, 250, 196), (300, 108, 360, 128), (410, 140, 520, 200),
           (560, 196, 640, 222), (720, 120, 790, 146), (770, 166, 880, 206), (900, 112, 950, 132),
           (60, 200, 140, 224), (470, 206, 540, 226), (240, 206, 300, 224)]


def _charco(cv, x0, y0, x1, y1, rnd):
    """Agua quieta, verde casi negra. Los raíles se hunden en ella."""
    cv.ellipse(x0, y0, x1, y1, K("pared", 0))
    cv.ellipse(x0 + 2, y0 + 1, x1 - 2, y1 - 1, K("pared", 0), outline=K("pared", 1))
    # orilla mojada
    w, h = x1 - x0, y1 - y0
    for _ in range(w // 3):
        a = rnd.uniform(0, math.tau)
        cv.px(int((x0 + x1) / 2 + math.cos(a) * w / 2 * 1.05), int((y0 + y1) / 2 + math.sin(a) * h / 2 * 1.1), K("gris", 1))
    # reflejos y ondas
    for k in range(3):
        yy = y0 + 3 + k * max(3, h // 4)
        if yy < y1 - 2:
            xa = x0 + w // 4 + rnd.randint(-4, 4)
            cv.hline(xa, xa + rnd.randint(4, max(5, w // 3)), yy, K("pared", 1 + (k == 0)))
    cv.px(x0 + w // 3, y0 + h // 2, K("pared", 3))


def _sumergir_railes(cv, x0, y0, x1, y1):
    """Donde un charco cruza un raíl, el raíl se ve bajo el agua (más apagado)."""
    cx, cy, rx, ry_ = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 - 2, (y1 - y0) / 2 - 1
    for r in RAILES:
        for y in (r - 1, r, r + 1):
            if abs(y - cy) >= ry_:
                continue
            half = rx * math.sqrt(max(0.0, 1 - ((y - cy) / ry_) ** 2))
            col = K("pared", 2) if y == r - 1 else K("pared", 1)
            cv.hline(int(cx - half), int(cx + half), y, col)


def _borde(cv, rnd):
    """Por debajo del lecho: el canto del andén de servicio, oscuro."""
    cv.rect(0, BORDE, W, H, K("gris", 0))
    cv.rect(0, BORDE, W, BORDE + 4, K("gris", 2)); cv.hline(0, W, BORDE, K("gris", 3))
    for x in range(0, W, 32):
        cv.vline(x, BORDE, BORDE + 4, K("gris", 1))
    for _ in range(140):
        cv.px(rnd.randint(0, W - 1), rnd.randint(BORDE + 5, H - 1), K("gris", 1))


def _detritus(cv, rnd, seco=False):
    # ladrillos caídos, una lata, huesos de rata, papeles podridos
    for _ in range(26):
        x, y = rnd.randint(10, W - 20), rnd.randint(LECHO + 8, BORDE - 8)
        if DERRUMBE[0] - 20 < x < PUNTAL[2] + 10:
            continue
        t = rnd.random()
        if t < 0.5:
            b = rnd.choice([1, 2, 3])
            cv.rect(x, y, x + 6, y + 3, K("granate", b)); cv.hline(x, x + 6, y, K("granate", b + 1)); cv.hline(x, x + 6, y + 3, K("gris", 0))
        elif t < 0.7:
            cv.rect(x, y, x + 4, y + 3, K("gris", 4)); cv.px(x + 3, y, K("gris", 6)); cv.px(x, y + 3, K("madera", 2))
        elif t < 0.85:
            cv.rect(x, y, x + 7, y + 4, K("papel", 0 if not seco else 1)); cv.px(x + 2, y + 1, K("papel", 1 if not seco else 2))
        else:
            cv.hline(x, x + 5, y, K("papel", 2)); cv.px(x + 1, y + 1, K("papel", 1)); cv.px(x + 4, y + 1, K("papel", 1))


def _rata(cv, x, y):
    cv.rect(x, y, x + 6, y + 3, K("gris", 1)); cv.px(x + 6, y + 1, K("gris", 1)); cv.px(x + 7, y + 1, K("gris", 2))
    cv.px(x + 4, y - 1, K("gris", 2)); cv.px(x + 6, y, K("rojo", 1))
    cv.d.line([(x - 1, y + 2), (x - 6, y + 3)], fill=K("piel", 0))


# ---------------------------------------------------------------- variantes


def _nicho(cv, x0, rnd):
    x1, y0, y1 = x0 + NICHO_W, NICHO_Y0, MURO
    # franja blanca pintada alrededor (descolorida, desconchada)
    fx0, fy0, fx1 = x0 - 6, y0 - 8, x1 + 6
    cv.rect(fx1 - 2, fy0 + 10, fx1 + 1, y1, K("granate", 0))                        # sombra de la franja
    cv.rect(fx0, fy0 + 6, fx0 + 4, y1, K("papel", 2)); cv.rect(fx1 - 4, fy0 + 6, fx1, y1, K("papel", 2))
    cv.ellipse(fx0, fy0, fx1, fy0 + 26, K("papel", 2))
    # hueco: arco de medio punto
    cv.rect(x0 - 2, y0 + 6, x1 + 2, y1, K("granate", 0))
    cv.ellipse(x0 - 2, y0 - 4, x1 + 2, y0 + 18, K("granate", 0))
    cv.rect(x0, y0 + 6, x1, y1, K("gris", 0))
    cv.ellipse(x0, y0 - 2, x1, y0 + 16, K("gris", 0))
    # fondo del nicho: ladrillo en sombra, y su suelo
    for yy in range(y0 + 10, y1 - 4, 4):
        cv.hline(x0 + 3, x1 - 3, yy, K("granate", 0))
        for xx in range(x0 + 3 + (yy // 4 % 2) * 4, x1 - 3, 8):
            cv.px(xx, yy + 1, K("granate", 0)); cv.rect(xx + 1, yy + 1, xx + 7, yy + 3, K("gris", 1))
    cv.rect(x0, y1 - 5, x1, y1, K("gris", 1)); cv.hline(x0, x1, y1 - 5, K("gris", 2))
    # jambas en escorzo (el grosor del muro)
    cv.poly([(x0, y0 + 8), (x0 + 3, y0 + 10), (x0 + 3, y1 - 5), (x0, y1)], K("granate", 1))
    cv.poly([(x1, y0 + 8), (x1 - 3, y0 + 10), (x1 - 3, y1 - 5), (x1, y1)], K("granate", 0))
    # la franja se ha caído a trozos: desconchones donde asoma el ladrillo
    for _ in range(22):
        lado = rnd.choice(["i", "d", "a"])
        if lado == "i":
            px_, py_ = rnd.randint(fx0, fx0 + 3), rnd.randint(fy0 + 8, y1 - 3)
        elif lado == "d":
            px_, py_ = rnd.randint(fx1 - 4, fx1 - 1), rnd.randint(fy0 + 8, y1 - 3)
        else:
            a = rnd.uniform(math.pi * 1.05, math.pi * 1.95)
            px_, py_ = int((fx0 + fx1) / 2 + math.cos(a) * (fx1 - fx0) / 2.15), int(fy0 + 13 + math.sin(a) * 11)
        cv.rect(px_, py_, px_ + rnd.randint(1, 3), py_ + rnd.randint(1, 4), K("granate", 2))
    for _ in range(60):
        px_, py_ = rnd.randint(fx0, fx1 - 1), rnd.randint(fy0, y1 - 2)
        if cv.img.getpixel((px_, py_)) == K("papel", 2):
            cv.px(px_, py_, K("papel", 1))
    # un número de refugio pintado encima
    cv.rect(x0 + 12, fy0 - 9, x1 - 12, fy0 - 2, K("papel", 1))
    cv.text(x0 + 15, fy0 - 8, str(NICHOS.index(x0) + 1), K("gris", 1))


def _derrumbe(cv, rnd):
    x0, y0, x1, y1 = DERRUMBE
    cx = (x0 + x1) // 2
    # la bóveda reventada: un boquete irregular de tierra, con el borde de ladrillo partido
    borde = [(x0 - 10, 0)]
    for k in range(0, 13):
        t = k / 12
        bx = int(x0 - 10 + t * (x1 - x0 + 20))
        by = int(10 + 22 * math.sin(t * math.pi)) + rnd.randint(-3, 3)
        borde.append((bx, by))
    borde.append((x1 + 10, 0))
    cv.poly(borde, K("madera", 0))
    for (bx, by) in borde[1:-1]:                                                   # ladrillos partidos del borde
        cv.rect(bx - 3, by - 2, bx + 4, by + 1, K("granate", 1)); cv.hline(bx - 3, bx + 4, by + 1, K("gris", 0))
    for _ in range(140):                                                           # tierra y raíces
        px_, py_ = rnd.randint(x0 - 8, x1 + 8), rnd.randint(0, 30)
        if cv.img.getpixel((px_, py_)) == K("madera", 0):
            cv.rect(px_, py_, px_ + 2, py_ + 1, K("madera", rnd.choice([1, 1, 2])))
    cv.d.line([(x0 + 20, 2), (x0 + 24, 12), (x0 + 22, 20)], fill=K("madera", 2))
    cv.d.line([(x1 - 22, 0), (x1 - 26, 10)], fill=K("madera", 2))
    for k in range(6):                                                             # grietas que salen del boquete
        sx, sy = rnd.choice([x0 - 14, x0 - 4, x1 + 4, x1 + 12]) + rnd.randint(-4, 4), rnd.randint(8, 24)
        for j in range(rnd.randint(10, 30)):
            sx += rnd.choice([-1, 0, 1]) * (1 if sx > cx else 1); sy += 1
            cv.px(sx, sy, K("gris", 0))
    # silueta del montón: ancho abajo (toda la huella), estrecho arriba, hasta el boquete
    def ancho(y):
        ruido = 2.0 * math.sin(y / 4.0) + 1.2 * math.sin(y / 1.7 + 1.0)
        if y >= 100:
            return (x1 - x0) / 2 - 1 + ruido
        t = (100 - y) / 74
        return (x1 - x0) / 2 * (1 - 0.6 * t ** 1.2) + ruido
    for y in range(24, y1):
        a = ancho(y)
        cv.hline(int(cx - a), int(cx + a), y, K("madera", 1))
    # cascotes por capas, de atrás (arriba) hacia delante (abajo): los de abajo tapan a los de arriba
    piezas = []
    for _ in range(420):
        y = rnd.randint(26, y1 - 3)
        a = ancho(y) - 2
        x = rnd.randint(int(cx - a), int(cx + a) - 3)
        esc = 0.6 + 0.8 * (y - 26) / (y1 - 26)                                     # más grandes cuanto más cerca
        w, h = max(3, int(rnd.randint(5, 12) * esc)), max(2, int(rnd.randint(3, 7) * esc))
        piezas.append((y, x, w, h, rnd.random(), rnd.choice([1, 2, 2, 3])))
    for (y, x, w, h, tipo, b) in sorted(piezas):
        lado = -1 if x + w / 2 > cx + 10 else (1 if x + w / 2 < cx - 10 else 0)        # la cara izquierda, algo más clara
        b = max(1, min(4, b + (1 if lado > 0 else 0) - (1 if lado < 0 else 0)))
        if tipo < 0.55:                                                            # ladrillo
            cv.rect(x, y, x + w, y + h, K("granate", b)); cv.hline(x, x + w, y, K("granate", b + 1))
            cv.hline(x, x + w, y + h, K("granate", 0))
            if w > 7:
                cv.vline(x + w // 2, y + 1, y + h, K("granate", b - 1))
        elif tipo < 0.85:                                                          # hormigón y piedra
            g = b + 1
            cv.poly([(x, y + h), (x + 2, y), (x + w, y + 1), (x + w - 1, y + h)], K("gris", g))
            cv.hline(x + 2, x + w, y, K("gris", g + 2)); cv.hline(x, x + w, y + h, K("gris", 0))
        else:                                                                      # tierra
            cv.ellipse(x, y, x + w, y + h + 1, K("madera", 1 + (b > 2)))
    # un raíl arrancado que asoma, retorcido, y una traviesa clavada
    cv.d.line([(x0 + 14, 168), (x0 + 30, 124), (x0 + 42, 104)], fill=K("gris", 6))
    cv.d.line([(x0 + 15, 169), (x0 + 31, 125), (x0 + 43, 105)], fill=K("gris", 1))
    cv.poly([(x1 - 34, 112), (x1 - 27, 110), (x1 - 14, 160), (x1 - 21, 162)], K("madera", 2))
    cv.d.line([(x1 - 34, 112), (x1 - 21, 162)], fill=K("madera", 3))
    cv.d.line([(x1 - 27, 110), (x1 - 14, 160)], fill=K("madera", 0))
    # el pie del montón: lengua de cascote suelto, hasta y=200; por debajo, el hueco libre
    for _ in range(90):
        x, y = rnd.randint(x0, x1 - 4), rnd.randint(y1 - 8, y1 - 2)
        cv.rect(x, y, x + rnd.randint(2, 5), y + 2, K("granate", rnd.choice([1, 2, 3])))
        cv.hline(x, x + 4, y + 2, K("gris", 0))
    for x in range(x0, x1, 3):                                                     # sombra irregular en el balasto
        cv.vline(x, y1, y1 + rnd.randint(1, 3), K("gris", 0)); cv.vline(x + 1, y1, y1 + rnd.randint(1, 3), K("gris", 0))
        cv.vline(x + 2, y1, y1 + 1, K("gris", 0))
    # polvo que todavía cae del boquete
    for _ in range(50):
        cv.px(rnd.randint(cx - 30, cx + 30), rnd.randint(30, 70), K("papel", 0))
    # el pájaro de las alas cerradas de Amory: alguien lo marcó con tiza al lado
    bx, by = x0 - 34, 58
    for (dx, dy) in ((0, 2), (1, 1), (2, 1), (3, 0), (4, 1), (5, 2), (6, 2), (7, 2), (2, 3), (3, 3), (4, 3), (5, 3),
                     (6, 1), (7, 1), (8, 0), (3, 4), (4, 4)):
        cv.px(bx + dx, by + dy, K("papel", 3))


def _puntal(cv, rnd):
    x0, y0, x1, y1 = PUNTAL
    # durmiente arriba, contra la bóveda agrietada
    cv.rect(x0 - 12, y0 - 6, x1 + 12, y0, K("madera", 2)); cv.hline(x0 - 12, x1 + 12, y0 - 6, K("madera", 3))
    cv.hline(x0 - 12, x1 + 12, y0 - 1, K("madera", 0))
    cv.rect(x0 - 2, y0 - 2, x1 + 2, y0 + 2, K("madera", 1))                        # cuña
    # sombra en la pared
    cv.rect(x1, y0, x1 + 3, 100, K("granate", 0))
    # el poste
    cv.rect(x0, y0, x1, y1 - 4, K("madera", 2))
    cv.vline(x0, y0, y1 - 4, K("madera", 3)); cv.vline(x0 + 1, y0, y1 - 4, K("madera", 3))
    cv.vline(x1 - 1, y0, y1 - 4, K("madera", 0))
    for _ in range(14):                                                            # vetas y podredumbre
        yy = rnd.randint(y0 + 2, y1 - 8)
        cv.vline(rnd.randint(x0 + 2, x1 - 2), yy, yy + rnd.randint(3, 9), K("madera", 1))
    for (yy, w) in ((64, 4), (80, 6), (92, 3)):                                    # mordiscos de podrido
        cv.rect(x1 - w, yy, x1, yy + 5, K("madera", 0)); cv.px(x1 - w, yy + 2, K("papel", 1))
    for _ in range(10):                                                            # hongos blanquecinos
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(70, y1 - 6), K("papel", rnd.choice([1, 2])))
    cv.d.line([(x0 + 3, 52), (x0 + 6, 60), (x0 + 4, 68)], fill=K("madera", 0))     # grieta a lo largo
    # zapata en el suelo
    cv.rect(x0 - 2, y1 - 6, x1 + 2, y1 - 2, K("madera", 1)); cv.hline(x0 - 2, x1 + 2, y1 - 6, K("madera", 3))
    cv.rect(x0 - 1, y1 - 2, x1 + 4, y1, K("gris", 0))


def _cartel_base(cv, x0, y0, x1, y1, fondo, rnd):
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("granate", 0))                       # sombra en la pared
    cv.rect(x0, y0, x1, y1, fondo)
    cv.frame(x0, y0, x1, y1, K("papel", 0))


def _despegar(cv, x0, y0, x1, y1, rnd, esquinas=("ad",), roto=True):
    """Medio despegado: esquinas dobladas, jirones y engrudo desconchado."""
    for e in esquinas:
        if e == "ad":                                                              # arriba a la derecha, colgando
            cv.poly([(x1 - 14, y0), (x1, y0), (x1, y0 + 14)], K("granate", 1))
            cv.poly([(x1 - 14, y0), (x1, y0 + 14), (x1 - 10, y0 + 12)], K("papel", 1))
            cv.d.line([(x1 - 14, y0), (x1, y0 + 14)], fill=K("papel", 2))
        elif e == "ai":
            cv.poly([(x0, y0), (x0 + 12, y0), (x0, y0 + 10)], K("granate", 1))
            cv.poly([(x0 + 12, y0), (x0, y0 + 10), (x0 + 8, y0 + 12)], K("papel", 1))
        elif e == "bi":                                                            # abajo a la izquierda, arrancado
            cv.poly([(x0, y1 - 18), (x0 + 16, y1), (x0, y1)], K("granate", 2))
            cv.d.line([(x0, y1 - 18), (x0 + 16, y1)], fill=K("papel", 1))
        elif e == "bd":
            cv.poly([(x1, y1 - 12), (x1 - 20, y1), (x1, y1)], K("granate", 2))
            cv.poly([(x1 - 20, y1), (x1, y1 - 12), (x1 - 6, y1 + 4), (x1 - 18, y1 + 6)], K("papel", 1))
    if roto:
        for _ in range(3):                                                         # desconchones: asoma el papel de debajo
            jx, jy = rnd.randint(x0 + 2, x1 - 8), rnd.randint(y0 + 4, y1 - 6)
            cv.poly([(jx, jy), (jx + rnd.randint(3, 7), jy + 1), (jx + 2, jy + rnd.randint(3, 5))], K("papel", 1))
    for _ in range((x1 - x0) * (y1 - y0) // 30):                                   # moho y manchas
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), K("papel", 0))


def _cartel_te(cv, rnd):
    x0, y0, x1, y1 = CARTELES["te"]
    _cartel_base(cv, x0, y0, x1, y1, K("ocre", 2), rnd)
    cv.rect(x0 + 2, y0 + 2, x1 - 2, y0 + 18, K("granate", 3))
    L.texto_grande(cv, x0 + 6, y0 + 5, "TE", K("papel", 3), escala=2)
    cv.px(x0 + 14, y0 + 3, K("papel", 3)); cv.px(x0 + 15, y0 + 2, K("papel", 3))   # la tilde
    cv.text(x0 + 24, y0 + 6, "DE", K("papel", 3)); cv.text(x0 + 24, y0 + 12, "CEILAN", K("ocre", 3))
    # la tetera y la taza humeante
    tx, ty = x0 + 10, y0 + 28
    cv.ellipse(tx, ty, tx + 22, ty + 18, K("papel", 3), outline=K("papel", 1))
    cv.ellipse(tx + 3, ty + 3, tx + 12, ty + 10, K("papel", 4))
    cv.rect(tx + 8, ty - 3, tx + 14, ty + 1, K("papel", 2)); cv.px(tx + 10, ty - 4, K("papel", 1))
    cv.d.line([(tx + 21, ty + 8), (tx + 28, ty + 2)], fill=K("papel", 2)); cv.d.line([(tx + 22, ty + 9), (tx + 29, ty + 3)], fill=K("papel", 1))
    cv.d.arc([tx - 6, ty + 4, tx + 3, ty + 14], 90, 270, fill=K("papel", 1))
    cv.hline(tx + 2, tx + 20, ty + 9, K("rojo", 2))                                # una franja pintada
    cx, cy = x0 + 36, y0 + 40
    cv.ellipse(cx, cy, cx + 14, cy + 4, K("papel", 3)); cv.rect(cx + 1, cy + 2, cx + 13, cy + 9, K("papel", 3))
    cv.hline(cx + 1, cx + 13, cy + 9, K("papel", 1)); cv.ellipse(cx + 2, cy + 1, cx + 12, cy + 3, K("madera", 3))
    cv.d.arc([cx + 11, cy + 2, cx + 18, cy + 8], 270, 90, fill=K("papel", 2))
    cv.ellipse(cx - 3, cy + 8, cx + 18, cy + 12, K("papel", 2))                    # platillo
    for k in range(3):                                                             # vapor
        sx = cx + 4 + k * 3
        cv.px(sx, cy - 3, K("papel", 4)); cv.px(sx + 1, cy - 5, K("papel", 4)); cv.px(sx, cy - 7, K("papel", 3))
    cv.text(x0 + 22, y1 - 9, "LA MEJOR", K("granate", 2))
    _despegar(cv, x0, y0, x1, y1, rnd, esquinas=("ad", "bi"))


def _cartel_teatro(cv, rnd):
    x0, y0, x1, y1 = CARTELES["teatro"]
    _cartel_base(cv, x0, y0, x1, y1, K("gris", 1), rnd)
    # telón rojo recogido a los lados y escenario con un foco
    cv.rect(x0 + 3, y0 + 3, x1 - 3, y0 + 8, K("rojo", 2))
    for k in range(x0 + 3, x1 - 3, 4):
        cv.px(k, y0 + 8, K("rojo", 1))
    cv.poly([(x0 + 3, y0 + 8), (x0 + 16, y0 + 8), (x0 + 8, y0 + 40), (x0 + 3, y0 + 44)], K("rojo", 2))
    cv.poly([(x1 - 3, y0 + 8), (x1 - 16, y0 + 8), (x1 - 8, y0 + 40), (x1 - 3, y0 + 44)], K("rojo", 2))
    cv.d.line([(x0 + 6, y0 + 10), (x0 + 6, y0 + 38)], fill=K("rojo", 1)); cv.d.line([(x1 - 7, y0 + 10), (x1 - 7, y0 + 38)], fill=K("rojo", 1))
    cv.poly([(x0 + 26, y0 + 9), (x0 + 34, y0 + 9), (x0 + 44, y0 + 40), (x0 + 16, y0 + 40)], K("ocre", 1))   # el haz
    cv.ellipse(x0 + 18, y0 + 36, x0 + 42, y0 + 44, K("ocre", 2))
    # una bailarina diminuta en el haz
    bx = x0 + 29
    cv.rect(bx, y0 + 24, bx + 2, y0 + 26, K("piel", 3)); cv.poly([(bx - 3, y0 + 33), (bx + 5, y0 + 33), (bx + 1, y0 + 27)], K("papel", 4))
    cv.vline(bx + 1, y0 + 26, y0 + 33, K("papel", 4)); cv.vline(bx, y0 + 33, y0 + 38, K("piel", 3)); cv.vline(bx + 2, y0 + 33, y0 + 36, K("piel", 3))
    cv.d.line([(bx - 4, y0 + 25), (bx + 1, y0 + 28)], fill=K("piel", 3)); cv.d.line([(bx + 6, y0 + 25), (bx + 1, y0 + 28)], fill=K("piel", 3))
    cv.rect(x0 + 3, y0 + 44, x1 - 3, y0 + 46, K("madera", 3))                      # tablas del escenario
    cv.text(x0 + 6, y0 + 49, "TEATRO", K("ocre", 3))
    cv.text(x0 + 6, y0 + 55, "ESTRENO", K("papel", 2))
    _despegar(cv, x0, y0, x1, y1, rnd, esquinas=("ai", "bd"))


def _cartel_playa(cv, rnd):
    x0, y0, x1, y1 = CARTELES["playa"]
    _cartel_base(cv, x0, y0, x1, y1, K("cielo", 5), rnd)
    cv.rect(x0 + 1, y0 + 1, x1 - 1, y0 + 14, K("cielo", 6))
    cv.ellipse(x1 - 20, y0 + 5, x1 - 8, y0 + 17, K("ocre", 4))                     # sol
    cv.rect(x0 + 1, y0 + 26, x1 - 1, y0 + 36, K("azul", 4))                        # mar
    cv.hline(x0 + 1, x1 - 1, y0 + 26, K("cielo", 6))
    for k in range(x0 + 4, x1 - 4, 9):
        cv.hline(k, k + 4, y0 + 30 + (k // 9) % 3 * 2, K("cielo", 5))
    cv.rect(x0 + 1, y0 + 36, x1 - 1, y1 - 1, K("ocre", 3))                         # arena
    for _ in range(30):
        cv.px(rnd.randint(x0 + 1, x1 - 2), rnd.randint(y0 + 37, y1 - 2), K("ocre", 2))
    # sombrilla a rayas y una toalla
    ux, uy = x0 + 18, y0 + 22
    for i in range(6):
        cv.poly([(ux + 6, uy - 6), (ux + i * 3 - 3, uy + 4), (ux + i * 3, uy + 4)], K("rojo", 3) if i % 2 else K("papel", 4))
    cv.vline(ux + 6, uy - 6, uy + 24, K("madera", 2))
    cv.rect(ux + 12, y0 + 44, ux + 30, y0 + 50, K("rojo", 3))
    for k in range(ux + 12, ux + 30, 4):
        cv.vline(k, y0 + 44, y0 + 50, K("papel", 4))
    # gaviotas
    for (gx, gy) in ((x0 + 10, y0 + 8), (x0 + 22, y0 + 5)):
        cv.px(gx, gy, K("gris", 2)); cv.px(gx + 1, gy - 1, K("gris", 2)); cv.px(gx + 2, gy, K("gris", 2))
        cv.px(gx + 3, gy - 1, K("gris", 2)); cv.px(gx + 4, gy, K("gris", 2))
    cv.rect(x0 + 1, y1 - 10, x1 - 1, y1 - 1, K("azul", 2))
    cv.text(x0 + 4, y1 - 8, "LA COSTA", K("papel", 4))
    cv.text(x0 + 5, y0 + 2, "VISITE", K("azul", 2))
    _despegar(cv, x0, y0, x1, y1, rnd, esquinas=("ad",))
    # media hoja colgando por la esquina de abajo
    cv.poly([(x1 - 14, y1), (x1, y1 - 16), (x1, y1), (x1 - 4, y1 + 6), (x1 - 12, y1 + 5)], K("papel", 1))
    cv.d.line([(x1 - 14, y1), (x1, y1 - 16)], fill=K("papel", 2))


# la niña del helado: 30x36, mira de frente y enseña los dientes
NINA = [
    "..........oooooooooo..........",
    "........oohhhhhhhhhhoo........",
    "......oohhhhHHHHhhhhhhoo......",
    ".....ohhhhHHhhhhhhhhhhhho.....",
    "....ohhhhhhhhhhhhhhhhhhhho....",
    "...ohhhhhhhhhhhhhhhhhhhhhho...",
    "...ohhhhhhsssssssssshhhhhho...",
    "..ohhhhhsssssssssssssshhhhho..",
    "..ohhhhsssssssssssssssshhhho..",
    "..ohhhsssseesssssseessssshho..",
    "..ohhhssseeeessssseeeessshho..",
    "..ohhhsssssssssssssssssssShho.",
    "..ohhhrrsssssssssssssssrrShho.",
    "..ohhhrrrsssssSSssssssrrrShho.",
    "..ohhhssssssssssssssssssSShho.",
    "..ohhhsssmmmmmmmmmmmmsssSShho.",
    "..ohhhssmwwwwwwwwwwwwmssSShho.",
    "..ohhhsssmwwwwwwwwwwmsssShhho.",
    "..ohhhhsssmmmmmmmmmmsssShhhho.",
    "...ohhhhssssssssssssssShhhho..",
    "...ohhhhhSssssssssssSShhhhho..",
    "....ohhhhhhSSSSSSSShhhhhhho...",
    "....ohhhhhh.SSSSSS.hhhhhhho...",
    ".....ohhhh..cccccc..hhhhho....",
    "......ooo.cccccccccccc.ooo....",
    ".........cccccccccccccc.......",
    "........cccccccccccccccc......",
    "........cccccccccccccccc......",
]


def _cartel_nina(cv, rnd):
    x0, y0, x1, y1 = CARTELES["nina"]
    _cartel_base(cv, x0, y0, x1, y1, K("ocre", 3), rnd)
    cv.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 14, K("cielo", 5))
    for k in range(x0 + 2, x1 - 2, 6):                                             # rayos de sol de fondo
        cv.d.line([(x0 + 30, y0 + 30), (k, y0 + 2)], fill=K("cielo", 6))
    pal = {"o": K("madera", 1), "h": K("madera", 3), "H": K("madera", 5), "s": K("piel", 4), "S": K("piel", 3),
           "e": K("gris", 1), "r": K("rojo", 4), "m": K("rojo", 2), "w": K("papel", 4), "c": K("rojo", 3)}
    cv.grid(x0 + 15, y0 + 10, NINA, pal)
    for k in range(10, 22, 3):                                                     # los dientes, uno a uno
        cv.px(x0 + 15 + k, y0 + 10 + 16, K("papel", 2))
    cv.px(x0 + 26, y0 + 19, K("papel", 4)); cv.px(x0 + 35, y0 + 19, K("papel", 4))   # brillo en los ojos
    # lazo en el pelo
    cv.poly([(x0 + 38, y0 + 10), (x0 + 46, y0 + 6), (x0 + 46, y0 + 14)], K("rojo", 4))
    cv.poly([(x0 + 38, y0 + 10), (x0 + 32, y0 + 6), (x0 + 33, y0 + 13)], K("rojo", 4))
    # el helado: cucurucho en la mano, dos bolas
    hx, hy = x0 + 44, y0 + 30
    cv.poly([(hx, hy + 8), (hx + 10, hy + 8), (hx + 5, hy + 22)], K("ocre", 2))
    for k in range(3):
        cv.d.line([(hx + 1 + k * 3, hy + 9), (hx + 5, hy + 20)], fill=K("ocre", 1))
    cv.ellipse(hx - 1, hy + 1, hx + 11, hy + 10, K("papel", 4))
    cv.ellipse(hx + 1, hy - 5, hx + 10, hy + 4, K("granate", 5))
    cv.px(hx + 4, hy - 3, K("papel", 4)); cv.px(hx + 2, hy + 3, K("papel", 3))
    cv.rect(hx - 2, hy + 18, hx + 6, hy + 24, K("piel", 4)); cv.hline(hx - 2, hx + 6, hy + 23, K("piel", 3))   # la mano
    # pie del cartel
    cv.rect(x0 + 2, y1 - 14, x1 - 2, y1 - 2, K("rojo", 3))
    cv.text(x0 + 6, y1 - 12, "HELADOS", K("papel", 4))
    cv.text(x0 + 6, y1 - 6, "FRESCOS", K("ocre", 4))
    _despegar(cv, x0, y0, x1, y1, rnd, esquinas=("bd",), roto=False)
    for _ in range(2):
        jx, jy = rnd.randint(x0 + 3, x0 + 10), rnd.randint(y0 + 36, y0 + 48)
        cv.poly([(jx, jy), (jx + 5, jy + 1), (jx + 1, jy + 5)], K("papel", 1))


def _plano(cv, rnd):
    x0, y0, x1, y1 = PLANO
    cv.rect(x0 - 2, y0 - 2, x1 + 4, y1 + 4, K("granate", 0))
    cv.rect(x0 - 2, y0 - 2, x1 + 2, y1 + 2, K("madera", 1)); cv.hline(x0 - 2, x1 + 2, y0 - 2, K("madera", 3))
    cv.rect(x0, y0, x1, y1, K("papel", 3))
    for _ in range(90):
        cv.px(rnd.randint(x0, x1 - 1), rnd.randint(y0, y1 - 1), K("papel", 2))
    cv.text(x0 + 3, y0 + 2, "METRO", K("azul", 2))
    cv.hline(x0 + 2, x1 - 2, y0 + 8, K("papel", 1))
    # el río, serpenteando por abajo
    rio = [(x0, y0 + 52), (x0 + 20, y0 + 48), (x0 + 38, y0 + 54), (x0 + 58, y0 + 50), (x0 + 74, y0 + 55), (x1, y0 + 51)]
    cv.d.line(rio, fill=K("cielo", 5), width=3)
    lineas = [
        (K("rojo", 3), [(x0 + 2, y0 + 30), (x0 + 30, y0 + 30), (x0 + 50, y0 + 26), (x1 - 2, y0 + 26)]),
        (K("azul", 3), [(x0 + 10, y0 + 12), (x0 + 30, y0 + 22), (x0 + 50, y0 + 36), (x0 + 60, y0 + 56), (x0 + 64, y1 - 2)]),
        (K("ocre", 3), [(x0 + 24, y0 + 18), (x0 + 66, y0 + 18), (x0 + 72, y0 + 30), (x0 + 66, y0 + 42), (x0 + 24, y0 + 42),
                        (x0 + 18, y0 + 30), (x0 + 24, y0 + 18)]),
        (K("gris", 1), [(x0 + 44, y0 + 10), (x0 + 44, y0 + 30), (x0 + 40, y0 + 50), (x0 + 34, y1 - 2)]),
        (K("pared", 4), [(x0 + 2, y0 + 40), (x0 + 30, y0 + 38), (x0 + 56, y0 + 44), (x1 - 2, y0 + 44)]),
        (K("madera", 3), [(x0 + 6, y0 + 14), (x0 + 26, y0 + 26), (x0 + 48, y0 + 32), (x0 + 58, y0 + 60)]),
        (K("granate", 4), [(x0 + 14, y0 + 10), (x0 + 36, y0 + 24), (x0 + 70, y0 + 24), (x1 - 2, y0 + 16)]),
        (K("cielo", 2), [(x0 + 72, y0 + 10), (x0 + 60, y0 + 26), (x0 + 52, y0 + 40), (x0 + 48, y1 - 2)]),
    ]
    for col, pts in lineas:
        cv.d.line(pts, fill=col, width=1)
    # estaciones: muchas, puntos blancos con borde
    for col, pts in lineas:
        for (a, b) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) // 7))
            for k in range(n):
                t = k / n
                sx, sy = int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t)
                cv.px(sx, sy, K("papel", 4)); cv.px(sx + 1, sy, K("gris", 1))
    # intercambiadores
    for (sx, sy) in ((x0 + 30, y0 + 30), (x0 + 44, y0 + 18), (x0 + 50, y0 + 36), (x0 + 66, y0 + 42), (x0 + 24, y0 + 42)):
        cv.ellipse(sx - 2, sy - 2, sx + 3, sy + 3, K("papel", 4), outline=K("gris", 1))
    # leyenda abajo y una esquina rota
    for k in range(4):
        cv.hline(x0 + 4, x0 + 30, y1 - 8 + k * 2, K("papel", 1))
    cv.poly([(x1 - 16, y1), (x1, y1 - 10), (x1, y1)], K("granate", 1))
    cv.poly([(x1 - 16, y1), (x1, y1 - 10), (x1 - 4, y1 + 6)], K("papel", 2))
    # una cruz a lápiz sobre el Strand, y una flecha: alguien estuvo aquí antes
    cv.px(x0 + 41, y0 + 47, K("gris", 0)); cv.px(x0 + 43, y0 + 47, K("gris", 0)); cv.px(x0 + 42, y0 + 48, K("gris", 0))
    cv.px(x0 + 41, y0 + 49, K("gris", 0)); cv.px(x0 + 43, y0 + 49, K("gris", 0))


# ---------------------------------------------------------------- composición


def dibujar(variante=None):
    rnd = random.Random({"nichos": 1321, "derrumbe": 1323, "carteles": 1324}.get(variante, 1320))
    seco = variante == "carteles"
    cv = Canvas(W, H)
    _ladrillo_boveda(cv, rnd)
    _cables(cv, rnd)
    for lx in LAMPARAS:
        if variante == "derrumbe" and DERRUMBE[0] - 20 < lx < PUNTAL[2] + 20:
            continue
        _lampara(cv, lx)
    _lecho(cv, rnd)
    _railes(cv, rnd)
    if not seco:
        for (x0, y0, x1, y1) in CHARCOS:
            if variante == "derrumbe" and x1 > DERRUMBE[0] - 10 and x0 < PUNTAL[2] + 8:
                continue
            _charco(cv, x0, y0, x1, y1, rnd)
            _sumergir_railes(cv, x0, y0, x1, y1)
        # goteras: anillos en el agua y la mancha bajo cada una
        for gx in (200, 470, 820):
            cv.px(gx, 176, K("pared", 3)); cv.px(gx - 2, 176, K("pared", 2)); cv.px(gx + 2, 176, K("pared", 2))
    else:
        # polvo seco: el balasto, más claro y con regueros de arena
        for _ in range(500):
            cv.px(rnd.randint(0, W - 1), rnd.randint(LECHO + 6, BORDE - 1), K("gris", 4))
    _detritus(cv, rnd, seco=seco)
    _borde(cv, rnd)
    if variante == "nichos":
        for x in NICHOS:
            _nicho(cv, x, rnd)
    elif variante == "derrumbe":
        _derrumbe(cv, rnd)
        _puntal(cv, rnd)
    elif variante == "carteles":
        _cartel_te(cv, rnd)
        _cartel_teatro(cv, rnd)
        _cartel_playa(cv, rnd)
        _cartel_nina(cv, rnd)
        _plano(cv, rnd)
        # el nombre de una estación de antes, en una placa esmaltada
        cv.rect(400, 44, 480, 58, K("papel", 3)); cv.frame(400, 44, 480, 58, K("azul", 1))
        cv.rect(402, 46, 478, 56, K("azul", 2))
        cv.text(440 - cv.text_width("BLACKFRIARS") // 2, 49, "BLACKFRIARS", K("papel", 4))
    _rata(cv, 330, 214 if not seco else 120)
    _rata(cv, 905, 104)
    # luz: tenue y uniforme; la bóveda se hunde en la sombra hacia arriba, y el borde también
    cv.add_light(0, 0, W, 8, -2)
    cv.add_light(0, 8, W, 17, -1)
    cv.add_light(0, BORDE + 4, W, H, -1)
    cv.bake_lighting()
    return cv
