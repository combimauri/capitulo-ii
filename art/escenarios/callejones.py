"""J12.06 — Limehouse de noche: la persecución (1440x270, la cámara sigue al jugador).

Callejones de ladrillo ennegrecido, adoquines mojados y charcos. Paleta nocturna (azules y grises
profundos) con charcos de luz cálida bajo las farolas de gas. Cobertizos y tapias parten el callejón,
sábanas tendidas para esconderse, portales hondos, dos puertas proles y, al final, la puerta verde del 11.
"""
import math
import random

from pixel import Canvas, K
import props as P
import _luz as L
from limehouse import ladrillo

W, H = 1440, 270
FACHADA, SUELO_FIN = 90, 250
OBSTACULOS = [(220, 140, 380, 190), (540, 140, 740, 190), (920, 140, 1100, 190), (1200, 140, 1320, 190)]
SABANAS = [(420, 460), (780, 820), (1130, 1170)]                  # tendederos: sábanas entre y 96 y 140
CHARCOS = [(300, 214, 324, 224), (640, 108, 664, 118), (980, 220, 1004, 230), (1250, 108, 1274, 118)]
FAROLAS = [150, 470, 850, 1160]
PORTALES = [(270, 300), (700, 730), (1020, 1050)]                 # portales hondos (escondites), y 40–90
PUERTAS_PROLES = [(600, 626), (880, 906)]                         # y 44–90
PUERTA_VERDE = (1380, 1410, 40, 90)
CUBO = (520, 96, 532, 108)


# ---------------------------------------------------------------- fachadas


def _ventana(cv, x, y, w, h, encendida, rnd):
    cv.rect(x - 1, y - 1, x + w + 1, y + h + 2, K("gris", 2))
    if encendida:
        cv.rect(x, y, x + w, y + h, K("ocre", 3))
        cv.rect(x, y, x + 3, y + h, K("granate", 3)); cv.rect(x + w - 3, y, x + w, y + h, K("granate", 3))   # cortinas
        cv.vline(x + w // 2, y, y + h, K("madera", 1)); cv.hline(x, x + w, y + h // 2, K("madera", 1))
        cv.add_emissive(x, y, x + w, y + h)
    else:
        cv.rect(x, y, x + w, y + h, K("azul", 0))
        if rnd.random() < 0.5:
            cv.px(x + 2, y + 2, K("cielo", 2)); cv.px(x + 3, y + 3, K("cielo", 2))          # un reflejo de la luna
        cv.vline(x + w // 2, y, y + h, K("gris", 2)); cv.hline(x, x + w, y + h // 2, K("gris", 2))
        if rnd.random() < 0.25:                                                              # tablones clavados
            cv.d.line([(x, y + 2), (x + w, y + h - 3)], fill=K("madera", 2))
    cv.hline(x - 2, x + w + 2, y + h + 1, K("gris", 4))                                      # alféizar


def _fachadas(cv, rnd, luces):
    x = 0
    huecos = PORTALES + PUERTAS_PROLES + [(PUERTA_VERDE[0], PUERTA_VERDE[1])]
    while x < W:
        w = rnd.randint(70, 110)
        top = rnd.randint(0, 12)
        ladrillo(cv, x, top, min(W, x + w), FACHADA, rnd, base=rnd.choice([1, 2]))
        cv.rect(x, top, min(W, x + w), top + 3, K("gris", 2)); cv.hline(x, min(W, x + w), top, K("gris", 4))  # cornisa
        if top > 0:
            cv.rect(x + 6, top - 6, x + 14, top, K("granate", 1)); cv.rect(x + 5, top - 7, x + 15, top - 5, K("gris", 2))  # chimenea
        for wx in range(x + 10, x + w - 18, 26):
            for wy in (top + 10, 50):
                if any(a - 8 < wx + 14 and wx < b + 8 for a, b in huecos) and (wy == 50 or wy + 17 > 28):
                    continue
                if wy == 50 and any(f - 10 < wx + 14 and wx < f + 10 for f in FAROLAS):
                    continue
                lit = rnd.random() < 0.1
                _ventana(cv, wx, wy, 13, 17 if wy != 50 else 15, lit, rnd)
                if lit:
                    luces.append((wx + 6, wy + 8))
        cv.vline(min(W, x + w) - 1, top, FACHADA, K("granate", 0))                          # junta entre casas
        x += w
    # bajante y canalón en algunas medianeras
    for gx in (205, 515, 760, 1110, 1335):
        cv.rect(gx, 4, gx + 2, FACHADA - 2, K("gris", 1)); cv.vline(gx, 4, FACHADA - 2, K("gris", 2))
        for by in range(14, FACHADA - 4, 22):
            cv.hline(gx - 1, gx + 3, by, K("gris", 0))                                           # abrazaderas
        cv.rect(gx - 1, FACHADA - 3, gx + 5, FACHADA, K("gris", 1))
    cv.rect(0, FACHADA, W, FACHADA + 3, K("gris", 2)); cv.hline(0, W, FACHADA, K("gris", 4))  # bordillo de la acera


def _portal_hondo(cv, x0, x1, y0=40, y1=90):
    """Portal hundido en la fachada: arco de ladrillo, jambas en escorzo y un rincón negro."""
    cv.rect(x0 - 3, y0 - 4, x1 + 3, y1, K("granate", 0))
    cv.ellipse(x0 - 3, y0 - 8, x1 + 3, y0 + 6, K("granate", 3), outline=K("granate", 1))      # arco
    cv.rect(x0, y0, x1, y1, K("gris", 0))
    cv.ellipse(x0, y0 - 5, x1, y0 + 9, K("gris", 0))                                          # hueco en arco
    cv.poly([(x0, y0 + 2), (x0 + 6, y0 + 8), (x0 + 6, y1 - 4), (x0, y1)], K("granate", 1))      # jamba izquierda en escorzo
    cv.poly([(x1, y0 + 2), (x1 - 6, y0 + 8), (x1 - 6, y1 - 4), (x1, y1)], K("granate", 0))
    cv.rect(x0 + 7, y0 + 10, x1 - 7, y1 - 4, K("madera", 0)); cv.frame(x0 + 7, y0 + 10, x1 - 7, y1 - 4, K("pelo", 0))   # puerta al fondo
    cv.rect(x0 - 2, y1, x1 + 2, y1 + 3, K("gris", 3)); cv.hline(x0 - 2, x1 + 2, y1, K("gris", 5))   # peldaño
    cv.rect(x0 + 6, y1 - 4, x1 - 6, y1, K("gris", 2))


def _puerta_prole(cv, x0, x1, y0=44, y1=90):
    P.puerta(cv, x0, y0, w=x1 - x0, h=y1 - y0, rampa="madera", base=1)
    cv.rect(x0 - 2, y1, x1 + 2, y1 + 3, K("gris", 3)); cv.hline(x0 - 2, x1 + 2, y1, K("gris", 5))


def _puerta_verde(cv, x0, x1, y0, y1):
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1, K("madera", 0))
    cv.rect(x0, y0, x1, y1, K("tele", 3)); cv.frame(x0, y0, x1, y1, K("tele", 1))
    cv.frame(x0 + 3, y0 + 10, x1 - 3, y0 + 24, K("tele", 2)); cv.frame(x0 + 3, y0 + 28, x1 - 3, y1 - 4, K("tele", 2))
    cv.vline(x0 + 1, y0 + 1, y1, K("tele", 4))
    cv.rect(x0 + (x1 - x0) // 2 - 4, y0 + 3, x0 + (x1 - x0) // 2 + 5, y0 + 9, K("ocre", 3))   # placa de latón
    cv.text(x0 + (x1 - x0) // 2 - 3, y0 + 4, "11", K("madera", 0))
    cv.px(x1 - 5, y0 + 27, K("ocre", 4)); cv.px(x1 - 5, y0 + 28, K("ocre", 2))                # pomo
    cv.rect(x0 + 8, y0 + 31, x1 - 8, y0 + 33, K("ocre", 2))                                   # buzón
    # montante de cristal encendido encima: alguien espera
    cv.rect(x0 - 1, y0 - 12, x1 + 1, y0 - 3, K("madera", 1))
    cv.rect(x0 + 1, y0 - 10, x1 - 1, y0 - 4, K("ocre", 4)); cv.add_emissive(x0 + 1, y0 - 10, x1 - 1, y0 - 4)
    for k in range(x0 + 6, x1 - 2, 6):
        cv.vline(k, y0 - 10, y0 - 4, K("madera", 1))
    cv.rect(x0 - 2, y1, x1 + 2, y1 + 4, K("papel", 1)); cv.hline(x0 - 2, x1 + 2, y1, K("papel", 3))   # escalón fregado


# ---------------------------------------------------------------- obstáculos


def _cobertizo(cv, x0, y0, x1, y1, rnd, alto=26):
    """Cobertizo de tablas con tejado de chapa ondulada (huella x0..x1, y0..y1)."""
    cv.rect(x0 + 4, y1, x1 + 5, y1 + 5, K("gris", 0))                                         # sombra
    cv.rect(x0, y1 - alto, x1, y1, K("madera", 2))                                            # frente de tablas
    for k in range(x0, x1, 7):
        cv.vline(k, y1 - alto, y1, K("madera", 1)); cv.vline(k + 1, y1 - alto, y1, K("madera", 3))
    cv.rect(x0 + (x1 - x0) // 2 - 9, y1 - alto + 6, x0 + (x1 - x0) // 2 + 9, y1, K("madera", 0))   # puerta con candado
    cv.px(x0 + (x1 - x0) // 2 + 5, y1 - 12, K("ocre", 2))
    # tejado: chapa ondulada vista desde arriba
    cv.rect(x0 - 2, y0 - alto, x1 + 2, y1 - alto, K("gris", 3))
    for k in range(x0 - 2, x1 + 2, 4):
        cv.vline(k, y0 - alto, y1 - alto, K("gris", 2)); cv.vline(k + 1, y0 - alto, y1 - alto, K("gris", 4))
    cv.hline(x0 - 2, x1 + 2, y1 - alto - 1, K("gris", 5))                                     # alero
    for _ in range(14):                                                                       # óxido
        rx, ry = rnd.randint(x0, x1 - 6), rnd.randint(y0 - alto, y1 - alto - 4)
        cv.rect(rx, ry, rx + rnd.randint(2, 6), ry + rnd.randint(1, 4), K("granate", 3))
    cv.rect(x0 + 20, y0 - alto + 6, x0 + 30, y0 - alto + 12, K("madera", 3))                 # tablón suelto encima


def _tapia(cv, x0, y0, x1, y1, rnd, alto=24, roto=False):
    """Tapia/caseta de ladrillo con albardilla (huella x0..x1, y0..y1)."""
    cv.rect(x0 + 4, y1, x1 + 5, y1 + 5, K("gris", 0))
    ladrillo(cv, x0, y1 - alto, x1, y1, rnd, base=2)
    cv.rect(x0, y0 - alto, x1, y1 - alto, K("granate", 1))                                    # cara superior
    for y in range(y0 - alto + 3, y1 - alto, 6):
        cv.hline(x0 + 2, x1 - 2, y, K("granate", 2))
    cv.frame(x0, y0 - alto, x1, y1 - alto, K("gris", 3)); cv.hline(x0, x1, y0 - alto, K("gris", 5))
    if roto:                                                                                 # boquete y ladrillos caídos encima
        cv.poly([(x0 + 40, y1 - alto), (x0 + 52, y1 - alto + 10), (x0 + 64, y1 - alto)], K("gris", 0))
        P.escombros(cv, x0 + 6, y0 - alto + 4, x1 - 6, y1 - alto - 4, n=8, semilla=x0)


def _carbonera(cv, x0, y0, x1, y1, rnd, alto=22):
    """Caseta de ladrillo con tejado de tela asfáltica y una trampilla de carbón."""
    _tapia(cv, x0, y0, x1, y1, rnd, alto=alto)
    cv.rect(x0, y0 - alto, x1, y1 - alto, K("gris", 2))                                       # tela asfáltica
    for y in range(y0 - alto + 4, y1 - alto, 8):
        cv.hline(x0, x1, y, K("gris", 1)); cv.hline(x0, x1, y + 1, K("gris", 3))
    cv.frame(x0, y0 - alto, x1, y1 - alto, K("gris", 1))
    for dx in (40, 120):                                                                      # puertas de los retretes
        cv.rect(x0 + dx, y1 - alto + 4, x0 + dx + 16, y1, K("madera", 1)); cv.frame(x0 + dx, y1 - alto + 4, x0 + dx + 16, y1, K("madera", 0))
        cv.rect(x0 + dx + 5, y1 - alto + 7, x0 + dx + 11, y1 - alto + 9, K("gris", 0))
    cv.rect(x0 + 168, y1 - 10, x0 + 186, y1 - 2, K("gris", 1)); cv.frame(x0 + 168, y1 - 10, x0 + 186, y1 - 2, K("gris", 3))  # trampilla
    for _ in range(12):
        cv.px(rnd.randint(x0 + 164, x0 + 190), rnd.randint(y1, y1 + 4), K("gris", 0))     # carbonilla


def _cajas_barriles(cv, x0, y0, x1, y1, rnd):
    """Cobertizo bajo con cajas y barriles apilados delante (llenan la huella)."""
    _cobertizo(cv, x0, y0, x1 - 60, y1 - 10, rnd, alto=24)
    for (bx, by) in [(x1 - 56, y1 - 22), (x1 - 34, y1 - 22), (x1 - 46, y1 - 40)]:             # barriles
        cv.ellipse(bx, by - 4, bx + 18, by + 4, K("madera", 3), outline=K("madera", 1))
        cv.rect(bx, by, bx + 18, by + 20, K("madera", 2)); cv.ellipse(bx, by - 4, bx + 18, by + 4, K("madera", 3), outline=K("madera", 1))
        cv.hline(bx, bx + 18, by + 6, K("gris", 2)); cv.hline(bx, bx + 18, by + 14, K("gris", 2))
    for (cx, cy, cw) in [(x1 - 28, y0 + 4, 24), (x1 - 22, y0 + 18, 20), (x0 + 4, y1 - 16, 22), (x0 + 28, y1 - 14, 18),
                         (x0 + 10, y1 - 30, 18), (x1 - 82, y1 - 18, 20), (x1 - 18, y1 - 17, 18)]:   # cajas
        cv.rect(cx, cy, cx + cw, cy + 4, K("madera", 4)); cv.rect(cx, cy + 4, cx + cw, cy + 16, K("madera", 3))
        cv.frame(cx, cy, cx + cw, cy + 16, K("madera", 1)); cv.d.line([(cx, cy + 4), (cx + cw - 1, cy + 15)], fill=K("madera", 1))
    cv.rect(x1 - 60, y1, x1 + 4, y1 + 4, K("gris", 0))


# ---------------------------------------------------------------- atrezo del suelo


def _tendedero(cv, x0, x1, rnd):
    """Cuerda de tender sobre dos postes, con sábanas colgando entre y 96 y 140 (escondite)."""
    for px_ in (x0 - 4, x1 + 2):                                                              # postes
        cv.rect(px_, 92, px_ + 3, 142, K("madera", 1)); cv.vline(px_, 92, 142, K("madera", 3))
        cv.ellipse(px_ - 2, 140, px_ + 5, 144, K("gris", 0))
    cv.d.line([(x0 - 3, 95), ((x0 + x1) // 2, 98), (x1 + 3, 95)], fill=K("gris", 4))
    cv.d.line([(x0 - 3, 93), (x0 - 18, 60)], fill=K("gris", 3))                               # la cuerda sube a una ventana
    cols = [("papel", 2), ("papel", 1), ("tela", 3)]
    x = x0
    i = 0
    while x < x1:
        w = min(x1 - x, rnd.randint(13, 20))
        ramp, b = cols[i % len(cols)]
        bot = 136 + rnd.randint(-3, 3)
        cv.rect(x, 97, x + w, bot, K(ramp, b))
        cv.vline(x + w - 1, 97, bot, K(ramp, b - 1)); cv.vline(x + w // 2, 99, bot - 2, K(ramp, b + 1))   # pliegues
        for k in range(x, x + w, 3):
            cv.px(k, bot, K(ramp, b - 1))                                                     # bajo ondulado
        cv.px(x + 1, 96, K("madera", 3)); cv.px(x + w - 2, 96, K("madera", 3))                # pinzas
        cv.rect(x + 2, bot + 6, x + w + 2, bot + 9, K("tela", 0))                             # sombra en el suelo
        x += w + 1
        i += 1


def _charco(cv, x0, y0, x1, y1, lit):
    cv.ellipse(x0, y0, x1, y1, K("azul", 1), outline=K("tela", 1))
    cv.hline(x0 + 4, x1 - 6, y0 + 3, K("cielo", 3))
    if lit:
        cv.hline(x0 + 7, x1 - 8, y0 + 5, K("ocre", 3)); cv.px(x0 + 9, y0 + 6, K("ocre", 4))
        cv.add_emissive(x0 + 7, y0 + 5, x1 - 8, y0 + 6)


def _cubo_tirado(cv, x0, y0, x1, y1):
    """Cubo de basura de latón volcado, con la tapa al lado y la basura desparramada."""
    cv.rect(x0 - 2, y1, x1 + 10, y1 + 2, K("gris", 0))
    cv.rect(x0, y0 + 2, x1, y1, K("ocre", 2)); cv.frame(x0, y0 + 2, x1, y1, K("ocre", 1))
    cv.hline(x0, x1, y0 + 4, K("ocre", 3)); cv.hline(x0, x1, y0 + 8, K("ocre", 1))
    cv.ellipse(x1 - 3, y0 + 1, x1 + 3, y1 + 1, K("gris", 0), outline=K("ocre", 3))             # boca, hacia la derecha
    cv.ellipse(x0 - 10, y0 + 6, x0 - 2, y0 + 11, K("ocre", 2), outline=K("ocre", 1))          # tapa
    for (bx, by, c) in [(x1 + 4, y0 + 6, ("papel", 2)), (x1 + 7, y0 + 9, ("granate", 2)), (x1 + 3, y0 + 10, ("gris", 4)),
                        (x1 + 9, y0 + 5, ("papel", 1)), (x1 + 11, y0 + 8, ("madera", 3))]:
        cv.rect(bx, by, bx + 3, by + 2, K(*c))


def dibujar(variante=None):
    rnd = random.Random(1212)
    cv = Canvas(W, H, bg=("azul", 0))
    luces_ventana = []
    _fachadas(cv, rnd, luces_ventana)
    for (a, b) in PORTALES:
        _portal_hondo(cv, a, b)
    for (a, b) in PUERTAS_PROLES:
        _puerta_prole(cv, a, b)
    _puerta_verde(cv, *PUERTA_VERDE)
    # suelo de adoquines mojados
    P.adoquines(cv, 0, FACHADA + 3, W, SUELO_FIN, semilla=12, rampa="tela", base=2)
    rw = random.Random(5)
    for _ in range(900):                                                                      # brillo de la lluvia
        x, y = rw.randint(0, W - 3), rw.randint(FACHADA + 4, SUELO_FIN - 2)
        cv.hline(x, x + rw.randint(1, 3), y, K("tela", 4))
    cv.rect(0, FACHADA + 3, W, FACHADA + 6, K("tela", 0))                                     # arroyo junto a la acera
    # charcos
    for (x0, y0, x1, y1) in CHARCOS:
        lit = any(abs((x0 + x1) // 2 - f) < 90 for f in FAROLAS)
        _charco(cv, x0, y0, x1, y1, lit)
    # obstáculos (de izquierda a derecha)
    _cobertizo(cv, *OBSTACULOS[0], rnd)
    _carbonera(cv, *OBSTACULOS[1], rnd)
    _cajas_barriles(cv, *OBSTACULOS[2], rnd)
    _tapia(cv, *OBSTACULOS[3], rnd, roto=True)
    # tendederos
    for (a, b) in SABANAS:
        _tendedero(cv, a, b, rnd)
    _cubo_tirado(cv, *CUBO)
    # un gato en la albardilla de la tapia, y periódicos mojados
    cv.rect(1290, 124, 1298, 128, K("gris", 0)); cv.rect(1296, 121, 1300, 125, K("gris", 0))
    cv.px(1296, 120, K("gris", 0)); cv.px(1299, 120, K("gris", 0)); cv.px(1297, 122, K("ocre", 4)); cv.add_emissive(1297, 122, 1298, 123)
    cv.d.line([(1290, 125), (1286, 130)], fill=K("gris", 0))
    for (px_, py_) in [(120, 230), (470, 200), (812, 236), (1060, 205), (1350, 230)]:
        cv.rect(px_, py_, px_ + 10, py_ + 7, K("papel", 1)); cv.hline(px_ + 2, px_ + 8, py_ + 2, K("papel", 0))
    # borde inferior: bordillo y muro bajo
    cv.rect(0, SUELO_FIN, W, SUELO_FIN + 3, K("gris", 3)); cv.hline(0, W, SUELO_FIN, K("gris", 5))
    ladrillo(cv, 0, SUELO_FIN + 3, W, H, rnd, base=1)
    # farolas de gas encendidas
    luces = [P.farola(cv, fx, 96, encendida=True) for fx in FAROLAS]

    # ---- luz: noche azul profunda; charcos cálidos bajo cada farola
    def pasos(x, y):
        n = -1
        for (lx, ly) in luces:
            d = math.hypot(x - lx, (y - (ly + 66)) * 1.5)
            if d < 46:
                return 1
            if d < 74:
                n = 0
        return n
    cv.add_light_fn(pasos)
    cv.glow_rgb = K("azul", 0)                                                                # velo nocturno (un resplandor oscuro)
    for y in range(H):
        fila = cv.glow[y]
        for x in range(W):
            d = min(math.hypot(x - lx, (y - (ly + 40)) * 1.1) for (lx, ly) in luces)
            k = 0.42 if d > 110 else 0.42 * max(0.0, (d - 40) / 70)
            fila[x] = round(k * 7 / 0.42) / 7 * 0.42
    cv.bake_lighting()
    for (lx, ly) in luces:
        L.glow_post(cv, lx, ly + 56, 90, 0.38, K("ocre", 3), squash=1.3)
        L.glow_post(cv, lx, ly, 14, 0.5, K("ocre", 4))
    for (wx, wy) in luces_ventana:
        L.glow_post(cv, wx, wy, 16, 0.25, K("ocre", 3))
    L.glow_post(cv, 1395, 34, 30, 0.35, K("ocre", 3))                                        # la luz sobre la puerta verde
    return cv
