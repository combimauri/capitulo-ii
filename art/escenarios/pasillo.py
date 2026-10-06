"""J3.05 — Pasillo de la planta 14 del Minipax (960x270, la cámara sigue al jugador).

Un pasillo de ministerio largo y gastado: yeso verdoso arriba, zócalo de friso oscuro abajo, tuberías de la
calefacción y una canaleta de cables bajo la cornisa, y cinco neones (el mapa los hace parpadear por código; aquí
se pintan encendidos). A lo largo de la pared: las puertas de Cartografía, del archivo y de la Sala 14-D, el tablón
de avisos (un nombre tachado en la lista de turnos), el reloj, el radiador, la telepantalla, el extintor, el cartel
del Gran Hermano, el cuarto de suministros y la salida a la escalera. Una junta de la tubería gotea en una lata.
El carrito de la limpieza de Nell espera en medio del pasillo.

Huellas del mapa (pasillo.tmj): pared del fondo y < 98, muro inferior y >= 196, suelo transitable 98-196,
muros de los extremos x < 8 y x >= 952.
"""
import math
import random

from pixel import Canvas, K, LOOKUP
import props as P

W, H = 960, 270
WT, WB, FB = 14, 98, 196            # arranque de la pared, pie de la pared (suelo), muro inferior
XL, XR = 8, 952                     # muros de los extremos
NEONES = (110, 290, 470, 650, 830)
RIEL = 67                           # moldura que separa el yeso del friso
PUERTA_Y = 40                       # dintel de las puertas (hotspots y 40-88)


# ---------------------------------------------------------------- ayudas


def _oscurecer(cv, x0, y0, x1, y1, n=-1):
    """Baja n pasos, dentro de su rampa, lo ya pintado (sombras proyectadas sobre la pared)."""
    px = cv.img.load()
    for y in range(max(0, y0), min(cv.h, y1)):
        for x in range(max(0, x0), min(cv.w, x1)):
            c = px[x, y]
            if c in LOOKUP:
                r, i = LOOKUP[c]
                px[x, y] = K(r, i + n)


def cartel_puerta(cv, x, w, texto, y=31):
    """Rótulo esmaltado sobre la puerta: placa clara, filo oscuro y dos tornillos."""
    _oscurecer(cv, x + 2, y + 2, x + w + 2, y + 9, -1)
    cv.rect(x, y, x + w, y + 7, K("papel", 3))
    cv.frame(x, y, x + w, y + 7, K("papel", 1))
    cv.hline(x + 1, x + w - 1, y + 1, K("papel", 4))
    cv.px(x + 2, y + 3, K("gris", 5)); cv.px(x + w - 3, y + 3, K("gris", 5))
    cv.text(x + w // 2 - cv.text_width(texto) // 2, y + 1, texto, K("gris", 1))


def puerta(cv, x, w=32, rampa="madera", base=2, cristal=False, luz=False, rejilla=False):
    """Puerta de oficina metida en su marco, del dintel (PUERTA_Y) al suelo."""
    y0, y1 = PUERTA_Y, WB
    _oscurecer(cv, x + w + 3, y0 - 1, x + w + 5, y1, -1)                                   # sombra del marco
    cv.rect(x - 3, y0 - 3, x + w + 3, y1, K(rampa, base))                                   # marco
    cv.hline(x - 3, x + w + 3, y0 - 3, K(rampa, base + 2))
    cv.vline(x - 3, y0 - 3, y1, K(rampa, base + 1)); cv.vline(x + w + 2, y0 - 2, y1, K(rampa, base - 1))
    cv.rect(x, y0, x + w, y1, K(rampa, base + 1))                                           # hoja
    cv.hline(x, x + w, y0, K(rampa, base - 1)); cv.vline(x, y0, y1, K(rampa, base))          # la sombra del marco en la hoja
    cv.vline(x + w - 1, y0 + 1, y1, K(rampa, base + 2))

    def cuarteron(a, b, c, d):
        cv.hline(a, c, b, K(rampa, base)); cv.vline(a, b, d, K(rampa, base))
        cv.hline(a + 1, c, d - 1, K(rampa, base + 2)); cv.vline(c - 1, b + 1, d, K(rampa, base + 2))

    if cristal:
        gx0, gy0, gx1, gy1 = x + 4, y0 + 4, x + w - 4, y0 + 25
        cv.rect(gx0 - 1, gy0 - 1, gx1 + 1, gy1 + 1, K(rampa, base - 1))
        cv.rect(gx0, gy0, gx1, gy1, K("cielo", 5 if luz else 2))                         # cristal esmerilado
        if luz:
            cv.rect(gx0, gy1 - 6, gx1, gy1, K("cielo", 6))
            for k in range(gx0 + 2, gx1 - 1, 5):                                           # siluetas de mesas al otro lado
                cv.px(k, gy1 - 4, K("cielo", 4)); cv.px(k + 1, gy1 - 4, K("cielo", 4))
        for k in range(0, gx1 - gx0 - 3, 6):                                               # reflejos
            cv.d.line([(gx0 + k + 3, gy0 + 1), (gx0 + k, gy0 + 4)], fill=K("cielo", 6 if luz else 4))
        cv.hline(gx0, gx1, gy0, K(rampa, base - 1))
    else:
        cuarteron(x + 4, y0 + 4, x + w - 4, y0 + 25)
    cuarteron(x + 4, y0 + 29, x + w - 4, y1 - 10)
    if rejilla:                                                                              # rejilla de ventilación en la hoja
        for k in range(y0 + 32, y1 - 13, 2):
            cv.hline(x + 7, x + w - 7, k, K(rampa, base - 1))
    cv.rect(x + 1, y1 - 7, x + w - 1, y1, K("gris", 5)); cv.hline(x + 1, x + w - 1, y1 - 7, K("gris", 7))  # chapa de patada
    cv.hline(x + 1, x + w - 1, y1 - 1, K("gris", 3))
    hx, hy = x + w - 7, y0 + 27                                                              # manilla de latón
    cv.rect(hx, hy - 2, hx + 3, hy + 5, K("ocre", 1)); cv.px(hx + 1, hy + 3, K("gris", 0))
    cv.hline(hx - 3, hx + 2, hy, K("ocre", 3)); cv.px(hx - 3, hy + 1, K("ocre", 2))


def rejilla(cv, x0, y0, x1, y1, polvo=True):
    """Rejilla de ventilación atornillada a la pared, con el tizne del aire sucio encima."""
    if polvo:
        rnd = random.Random(x0 * 7 + y0)
        for k in range(14):
            cv.px(rnd.randint(x0, x1 - 1), y0 - 1 - rnd.randint(0, 4), K("pared", 1))
        cv.hline(x0 + 1, x1 - 1, y0 - 1, K("pared", 1))
    _oscurecer(cv, x0 + 2, y0 + 2, x1 + 2, y1 + 2, -1)
    cv.rect(x0, y0, x1, y1, K("gris", 3)); cv.frame(x0, y0, x1, y1, K("gris", 1))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("gris", 5))
    for y in range(y0 + 3, y1 - 2, 2):
        cv.hline(x0 + 2, x1 - 2, y, K("gris", 0)); cv.hline(x0 + 2, x1 - 2, y + 1, K("gris", 4))
    for (a, b) in ((x0 + 1, y0 + 1), (x1 - 2, y0 + 1), (x0 + 1, y1 - 2), (x1 - 2, y1 - 2)):
        cv.px(a, b, K("gris", 7))


def reloj(cv, cx, cy):
    """Reloj de pared del ministerio: las seis en punto, la hora de salir."""
    _oscurecer(cv, cx - 7 + 2, cy - 7 + 2, cx + 8 + 2, cy + 8 + 2, -1)
    cv.rect(cx - 2, cy - 10, cx + 3, cy - 6, K("gris", 2))                                    # soporte
    cv.ellipse(cx - 7, cy - 7, cx + 8, cy + 8, K("gris", 2))
    cv.ellipse(cx - 6, cy - 6, cx + 7, cy + 7, K("papel", 3))
    cv.ellipse(cx - 4, cy - 4, cx + 5, cy + 5, K("papel", 4))
    for (dx, dy) in ((0, -5), (5, 0), (0, 5), (-5, 0)):
        cv.px(cx + dx, cy + dy, K("gris", 2))
    cv.vline(cx, cy - 4, cy + 1, K("gris", 0)); cv.vline(cx, cy, cy + 4, K("gris", 1))       # 18:00
    cv.px(cx, cy, K("rojo", 3))


def tablon(cv, x0, y0, x1, y1):
    """Tablón de avisos: turnos (con un nombre tachado), una circular y el aviso de la Semana del Odio."""
    _oscurecer(cv, x0 + 2, y0 + 2, x1 + 2, y1 + 2, -2)
    cv.rect(x0, y0, x1, y1, K("madera", 2)); cv.hline(x0, x1, y0, K("madera", 4))
    cv.vline(x0, y0, y1, K("madera", 3)); cv.hline(x0, x1, y1 - 1, K("madera", 1))
    rnd = random.Random(14)
    cv.rect(x0 + 2, y0 + 2, x1 - 2, y1 - 2, K("ocre", 1))                                     # corcho
    for _ in range(90):
        cv.px(rnd.randint(x0 + 2, x1 - 3), rnd.randint(y0 + 2, y1 - 3), K("ocre", rnd.choice((0, 2))))
    # turnos
    a, b = x0 + 4, y0 + 4
    cv.rect(a + 1, b + 1, a + 26, b + 24, K("ocre", 0))
    cv.rect(a, b, a + 25, b + 23, K("papel", 4))
    cv.text(a + 1, b + 1, "TURNOS", K("gris", 2))
    for k in range(6):
        cv.hline(a + 2, a + 21 - (k * 5) % 8, b + 8 + k * 2 + (k // 3), K("gris", 6))
    cv.rect(a + 2, b + 15, a + 19, b + 17, K("gris", 1))                                       # el nombre tachado
    cv.px(a + 12, b - 1, K("rojo", 4))
    # circular con sello
    a, b = x0 + 32, y0 + 6
    cv.rect(a + 1, b + 1, a + 17, b + 17, K("ocre", 0))
    cv.rect(a, b, a + 16, b + 16, K("papel", 3))
    for k in range(5):
        cv.hline(a + 2, a + 14 - (k % 2) * 4, b + 2 + k * 2, K("gris", 5))
    cv.ellipse(a + 9, b + 10, a + 15, b + 16, None, outline=K("rojo", 2))
    cv.px(a + 8, b - 1, K("gris", 7))
    # la Semana del Odio
    a, b = x0 + 51, y0 + 4
    cv.rect(a + 1, b + 1, a + 18, b + 23, K("ocre", 0))
    cv.rect(a, b, a + 17, b + 22, K("papel", 2))
    cv.rect(a, b, a + 17, b + 7, K("rojo", 2))
    cv.text(a + 1, b + 1, "ODIO", K("papel", 4))
    cv.rect(a + 5, b + 10, a + 12, b + 19, K("gris", 2)); cv.rect(a + 7, b + 11, a + 10, b + 14, K("gris", 4))
    cv.px(a + 8, b - 1, K("gris", 7))
    # restos de un aviso arrancado: la chincheta y una esquina de papel
    cv.px(x1 - 8, y1 - 9, K("gris", 7)); cv.rect(x1 - 9, y1 - 8, x1 - 5, y1 - 5, K("papel", 2))


def radiador(cv, x0, x1, y0):
    """Radiador de hierro colado, de pie sobre el suelo, con su llave y la tubería que baja de arriba."""
    y1 = WB + 1
    cv.rect(x0 + 3, y1 - 1, x1 + 4, y1 + 3, K("tela", 0))                                    # sombra en el suelo
    _oscurecer(cv, x0 + 2, y0 + 2, x1 + 3, y1, -1)
    for x in range(x0, x1, 4):                                                               # elementos
        cv.rect(x, y0 + 2, x + 3, y1 - 3, K("gris", 5))
        cv.vline(x, y0 + 2, y1 - 3, K("gris", 6)); cv.vline(x + 2, y0 + 2, y1 - 3, K("gris", 3))
        cv.rect(x, y0, x + 3, y0 + 2, K("gris", 7))                                           # la cara de arriba
        cv.vline(x + 3, y0 + 4, y1 - 5, K("gris", 1))
    cv.hline(x0, x1, y0 + 6, K("gris", 4)); cv.hline(x0, x1, y1 - 7, K("gris", 4))
    for fx in (x0 + 1, x1 - 4):
        cv.rect(fx, y1 - 3, fx + 3, y1, K("gris", 2))                                         # patas
    cv.rect(x1, y1 - 9, x1 + 4, y1 - 6, K("gris", 4))                                         # llave
    cv.rect(x1 + 2, y1 - 12, x1 + 5, y1 - 10, K("ocre", 2)); cv.px(x1 + 3, y1 - 12, K("ocre", 3))


def extintor(cv, x0, y0, x1, y1):
    cx = (x0 + x1) // 2                                                                       # placa FUEGO
    cv.rect(cx - 12, y0 - 14, cx + 12, y0 - 6, K("rojo", 2)); cv.hline(cx - 12, cx + 12, y0 - 7, K("rojo", 1))
    cv.text(cx - cv.text_width("FUEGO") // 2, y0 - 13, "FUEGO", K("papel", 4))
    _oscurecer(cv, x0 + 2, y0 + 2, x1 + 3, y1 + 2, -2)
    cv.rect(x0 - 2, y0 + 6, x1 + 2, y0 + 9, K("gris", 2))                                     # abrazadera
    cv.rect(x0, y0 + 4, x1, y1, K("rojo", 3)); cv.frame(x0, y0 + 4, x1, y1, K("rojo", 1))
    cv.vline(x0 + 2, y0 + 6, y1 - 2, K("rojo", 5)); cv.vline(x0 + 3, y0 + 6, y1 - 2, K("rojo", 4))
    cv.vline(x1 - 2, y0 + 6, y1 - 1, K("rojo", 2))
    cv.rect(x0 + 3, y0, x1 - 3, y0 + 4, K("gris", 4)); cv.hline(x0 + 3, x1 - 3, y0, K("gris", 6))
    cv.d.line([(x1 - 3, y0 + 1), (x1 + 2, y0 + 3), (x1 + 2, y0 + 20)], fill=K("gris", 1))       # manguera
    cv.rect(x0 + 2, y0 + 12, x1 - 2, y0 + 18, K("papel", 3))
    cv.hline(x0 + 3, x1 - 3, y0 + 14, K("gris", 3)); cv.hline(x0 + 3, x1 - 4, y0 + 16, K("gris", 3))
    # recuadro pintado en el suelo, delante
    cv.frame(x0 - 2, WB + 1, x1 + 3, WB + 10, K("rojo", 2))
    for k in range(x0, x1 + 1, 4):
        cv.d.line([(k, WB + 9), (k + 3, WB + 2)], fill=K("rojo", 1))


def cuadro_electrico(cv, x0, y0, x1, y1):
    cv.rect(x0 + (x1 - x0) // 2 - 1, 29, x0 + (x1 - x0) // 2 + 2, y0, K("gris", 3))          # tubo hasta la canaleta
    cv.vline(x0 + (x1 - x0) // 2 - 1, 29, y0, K("gris", 5))
    _oscurecer(cv, x0 + 2, y0 + 2, x1 + 2, y1 + 2, -2)
    cv.rect(x0, y0, x1, y1, K("gris", 4)); cv.frame(x0, y0, x1, y1, K("gris", 2))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("gris", 6))
    cv.frame(x0 + 2, y0 + 3, x1 - 2, y1 - 2, K("gris", 3))
    cv.rect(x1 - 5, y0 + 10, x1 - 3, y0 + 15, K("gris", 1))                                   # cerradura
    cx = (x0 + x1) // 2 - 2                                                                   # triángulo de peligro
    cv.poly([(cx, y0 + 5), (cx + 5, y0 + 13), (cx - 5, y0 + 13)], K("gris", 1))
    cv.poly([(cx, y0 + 7), (cx + 3, y0 + 12), (cx - 3, y0 + 12)], K("ocre", 3))
    cv.vline(cx, y0 + 8, y0 + 11, K("gris", 0))
    cv.rect(x0 + 4, y1 - 9, x1 - 6, y1 - 5, K("papel", 2))


def bajante(cv, x, y0, y1):
    """Tubería vertical pegada a la pared, con abrazaderas."""
    _oscurecer(cv, x + 4, y0, x + 6, y1, -2)
    cv.rect(x, y0, x + 4, y1, K("gris", 4))
    cv.vline(x, y0, y1, K("gris", 2)); cv.vline(x + 1, y0, y1, K("gris", 6)); cv.vline(x + 3, y0, y1, K("gris", 3))
    for y in range(y0 + 10, y1 - 4, 22):
        cv.rect(x - 1, y, x + 5, y + 3, K("gris", 2)); cv.hline(x - 1, x + 5, y, K("gris", 5))


def lata_goteo(cv, x, y):
    """La lata que alguien puso bajo la gotera, y el cerco de agua en el linóleo."""
    cv.ellipse(x - 5, y + 4, x + 13, y + 12, K("tela", 3))
    cv.ellipse(x - 3, y + 6, x + 11, y + 11, K("cielo", 2))
    cv.px(x + 9, y + 8, K("cielo", 4)); cv.px(x - 1, y + 9, K("cielo", 4))
    cv.rect(x + 1, y + 2, x + 9, y + 9, K("gris", 5)); cv.vline(x + 1, y + 2, y + 9, K("gris", 7))
    cv.vline(x + 8, y + 2, y + 9, K("gris", 3)); cv.hline(x + 2, x + 8, y + 5, K("gris", 4))
    cv.ellipse(x + 1, y, x + 9, y + 4, K("gris", 6))
    cv.ellipse(x + 2, y + 1, x + 8, y + 3, K("cielo", 3))


# ---------------------------------------------------------------- el carrito


def carrito(cv, x, y):
    """Carrito de la limpieza (vista 3/4): bastidor de metal con dos bandejas, cubo con agua y fregona,
    trapos, lejía y un cepillo. Bajo los trapos asoma la esquina de un papel (ahí van los dibujos).
    Ocupa x..x+37, y-14..y+31 (colisión del mapa: x, y+8 .. x+36, y+30)."""
    cv.ellipse(x + 1, y + 24, x + 40, y + 32, K("tela", 0))                                  # sombra en el suelo
    cv.rect(x + 4, y + 23, x + 38, y + 30, K("tela", 0))
    # ruedas
    for wx in (x + 1, x + 29):
        cv.rect(wx, y + 25, wx + 5, y + 29, K("gris", 1)); cv.hline(wx + 1, wx + 4, y + 25, K("gris", 4))
        cv.px(wx + 2, y + 27, K("gris", 3))
    # bandeja de abajo: cara de arriba y canto
    cv.rect(x, y + 19, x + 34, y + 22, K("gris", 6)); cv.hline(x, x + 34, y + 19, K("gris", 7))
    cv.rect(x, y + 22, x + 34, y + 25, K("gris", 4)); cv.hline(x, x + 34, y + 24, K("gris", 2))
    # trapos rojizos y una bolsa en la bandeja de abajo
    cv.rect(x + 2, y + 14, x + 15, y + 21, K("granate", 3)); cv.hline(x + 2, x + 15, y + 14, K("granate", 5))
    cv.hline(x + 3, x + 14, y + 17, K("granate", 1)); cv.vline(x + 15, y + 15, y + 21, K("granate", 1))
    # cubo galvanizado con agua sucia, sobre la bandeja de abajo
    cv.rect(x + 18, y + 9, x + 32, y + 21, K("gris", 6))
    cv.vline(x + 18, y + 9, y + 21, K("gris", 4)); cv.vline(x + 19, y + 10, y + 21, K("gris", 8))
    cv.vline(x + 31, y + 9, y + 21, K("gris", 4)); cv.vline(x + 30, y + 10, y + 21, K("gris", 5))
    cv.hline(x + 18, x + 32, y + 14, K("gris", 4)); cv.hline(x + 18, x + 32, y + 18, K("gris", 4))
    cv.ellipse(x + 17, y + 5, x + 33, y + 12, K("gris", 8))                                   # boca del cubo
    cv.ellipse(x + 18, y + 6, x + 32, y + 11, K("cielo", 3))
    cv.hline(x + 20, x + 23, y + 7, K("cielo", 5)); cv.px(x + 29, y + 9, K("cielo", 4))
    # fregona metida en el cubo: el palo y las tiras colgando del borde
    cv.vline(x + 25, y - 14, y + 9, K("madera", 4)); cv.vline(x + 26, y - 14, y + 9, K("madera", 2))
    cv.px(x + 25, y - 14, K("madera", 5)); cv.px(x + 26, y - 14, K("madera", 3))
    cv.rect(x + 22, y + 6, x + 30, y + 9, K("papel", 1))
    for k, dx in enumerate((21, 23, 28, 30)):
        cv.vline(x + dx, y + 8, y + 12 + k % 2 * 2, K("papel", 2)); cv.px(x + dx, y + 8, K("papel", 3))
    # postes y bandeja de arriba
    for px_ in (x, x + 33):
        cv.rect(px_, y + 3, px_ + 2, y + 25, K("gris", 3)); cv.vline(px_, y + 3, y + 25, K("gris", 5))
    cv.rect(x, y + 3, x + 16, y + 6, K("gris", 6)); cv.hline(x, x + 16, y + 3, K("gris", 7))
    cv.rect(x, y + 6, x + 16, y + 8, K("gris", 4)); cv.hline(x, x + 16, y + 7, K("gris", 2))
    # asa a la izquierda
    cv.d.line([(x + 1, y + 3), (x - 2, y - 1), (x - 2, y + 8), (x, y + 10)], fill=K("gris", 5))
    # en la bandeja de arriba: la lejía, los trapos doblados y, debajo, la esquina de un papel
    cv.rect(x + 1, y - 6, x + 5, y + 4, K("papel", 3))                                        # lejía
    cv.vline(x + 1, y - 6, y + 4, K("papel", 4)); cv.vline(x + 4, y - 5, y + 4, K("papel", 1))
    cv.rect(x + 2, y - 8, x + 4, y - 6, K("rojo", 3))
    cv.rect(x + 1, y - 2, x + 5, y + 1, K("rojo", 2))
    cv.rect(x + 7, y + 1, x + 14, y + 6, K("papel", 4)); cv.hline(x + 7, x + 14, y + 5, K("papel", 2))  # el papel
    for (dx, dy) in ((8, 4), (9, 3), (10, 4), (11, 3), (12, 4)):                              # un pájaro a lápiz
        cv.px(x + dx, y + dy, K("gris", 3))
    cv.rect(x + 6, y - 2, x + 17, y + 3, K("papel", 2)); cv.hline(x + 6, x + 17, y - 2, K("papel", 3))   # trapos
    cv.hline(x + 7, x + 16, y + 1, K("papel", 0)); cv.vline(x + 16, y - 1, y + 3, K("papel", 1))
    cv.rect(x + 7, y - 5, x + 15, y - 2, K("tela", 3)); cv.hline(x + 7, x + 15, y - 5, K("tela", 4))
    cv.hline(x + 7, x + 15, y - 3, K("tela", 1))
    # recogedor colgado del poste derecho
    cv.rect(x + 34, y + 9, x + 38, y + 17, K("gris", 4)); cv.vline(x + 37, y + 9, y + 17, K("gris", 2))
    cv.hline(x + 34, x + 38, y + 9, K("gris", 6))


# ---------------------------------------------------------------- dibujo


def _pared(cv, rnd):
    # cornisa / tapa del muro, con su filo
    cv.rect(0, 0, W, 2, K("gris", 0))
    P.tapa_muro(cv, 0, 2, W, WT)
    # yeso verdoso de arriba, con su textura gastada
    cv.rect(0, WT, W, RIEL, K("pared", 3))
    for _ in range(1300):
        cv.px(rnd.randint(0, W - 1), rnd.randint(WT, RIEL - 1), K("pared", rnd.choice((2, 2, 4))))
    cv.rect(0, WT, W, WT + 2, K("pared", 1)); cv.hline(0, W, WT + 2, K("pared", 2))           # moldura bajo la cornisa
    # moldura del friso
    cv.rect(0, RIEL, W, RIEL + 3, K("pared", 4)); cv.hline(0, W, RIEL, K("pared", 5)); cv.hline(0, W, RIEL + 2, K("pared", 2))
    # friso de paneles pintados, más oscuro
    cv.rect(0, RIEL + 3, W, WB - 6, K("pared", 2))
    for x in range(0, W, 30):
        cv.vline(x, RIEL + 3, WB - 6, K("pared", 1)); cv.vline(x + 1, RIEL + 3, WB - 6, K("pared", 3))
        cv.hline(x + 4, x + 27, RIEL + 6, K("pared", 1)); cv.vline(x + 4, RIEL + 6, WB - 9, K("pared", 1))
        cv.hline(x + 5, x + 27, WB - 9, K("pared", 3)); cv.vline(x + 26, RIEL + 7, WB - 9, K("pared", 3))
    # rodapié
    cv.rect(0, WB - 6, W, WB, K("gris", 2)); cv.hline(0, W, WB - 6, K("gris", 4)); cv.hline(0, W, WB - 1, K("gris", 1))
    # humedad que sube del suelo: cercos irregulares sobre el friso, con salitre
    for (a, b) in ((150, 232), (404, 452), (628, 744), (926, 952)):
        for x in range(a, b):
            t = (x - a) / (b - a)
            alto = 3 + 7 * math.sin(math.pi * t) ** 0.7 + 1.5 * math.sin(x / 5.3) + math.sin(x / 2.1)
            top = WB - 6 - max(1, int(alto))
            for y in range(top, WB - 6):
                cv.px(x, y, K("pared", 1))
            if (x // 3) % 4 != 0:
                cv.px(x, top - 1, K("pared", 1) if (x // 2) % 3 == 0 else K("pared", 2))


def _tuberias(cv):
    # tubería gruesa de la calefacción
    cv.hline(0, W, 17, K("gris", 2)); cv.hline(0, W, 18, K("gris", 6))
    cv.rect(0, 19, W, 22, K("gris", 5)); cv.hline(0, W, 21, K("gris", 4)); cv.hline(0, W, 22, K("gris", 2))
    _oscurecer(cv, 0, 23, W, 25, -2); _oscurecer(cv, 0, 25, W, 26, -1)
    # tubería fina
    cv.hline(0, W, 26, K("gris", 6)); cv.hline(0, W, 27, K("gris", 4)); cv.hline(0, W, 28, K("gris", 2))
    _oscurecer(cv, 0, 29, W, 30, -1)
    # juntas, abrazaderas y una llave de paso
    for x in range(36, W, 96):
        cv.rect(x, 16, x + 4, 24, K("gris", 4)); cv.vline(x, 16, 24, K("gris", 6)); cv.vline(x + 3, 16, 24, K("gris", 2))
    for x in range(12, W, 64):
        cv.rect(x, 25, x + 3, 30, K("gris", 1)); cv.px(x + 1, 29, K("gris", 4))
    vx = 214                                                                                  # llave de paso
    cv.rect(vx - 1, 16, vx + 8, 24, K("gris", 4)); cv.vline(vx - 1, 16, 24, K("gris", 6)); cv.vline(vx + 7, 16, 24, K("gris", 2))
    cv.rect(vx + 2, 12, vx + 5, 16, K("gris", 3))
    cv.hline(vx - 2, vx + 9, 11, K("rojo", 2)); cv.hline(vx - 1, vx + 8, 12, K("rojo", 1)); cv.px(vx + 3, 11, K("rojo", 3))


def _gotera(cv, x, rnd):
    """Junta oxidada que gotea: mancha de humedad que baja por el yeso hasta el friso."""
    cv.rect(x - 1, 16, x + 5, 24, K("madera", 2)); cv.px(x + 1, 18, K("ocre", 1)); cv.px(x + 3, 21, K("madera", 3))
    for k in range(6):                                                                        # óxido escurrido
        cv.px(x + 1 + k % 3, 24 + k, K("madera", 2))
    cv.px(x + 2, 31, K("cielo", 4)); cv.px(x + 2, 32, K("cielo", 5))                           # la gota
    # el cerco: manchas redondeadas que se van abriendo hacia abajo, con el borde más oscuro (marca de marea)
    blobs = [(x + 2, 29, 6), (x - 6, 31, 5), (x + 10, 31, 6), (x - 13, 34, 4), (x + 17, 34, 4), (x + 3, 35, 7),
             (x - 4, 38, 5), (x + 9, 39, 4)]
    blobs = [(bx + rnd.randint(-1, 1), by, r) for bx, by, r in blobs]

    def dentro(px_, py_, m=0):
        return any((px_ - bx) ** 2 + ((py_ - by) * 1.2) ** 2 < (r + m) ** 2 for bx, by, r in blobs)

    for y in range(24, RIEL):
        for xx in range(x - 16, x + 20):
            if dentro(xx, y):
                borde = not dentro(xx, y, -2)
                cv.px(xx, y, K("pared", 1) if borde else K("pared", 2))
            elif dentro(xx, y, 1) and (xx + y) % 3:
                cv.px(xx, y, K("papel", 0))                                                    # cerco de cal
    for (sx, y0, largo) in ((x - 4, 42, 22), (x + 3, 44, 30), (x + 10, 42, 14), (x - 11, 37, 9)):   # regueros
        for y in range(y0, min(WB - 7, y0 + largo)):
            cv.px(sx + (y - y0) // 15, y, K("pared", 1) if y < RIEL or y > RIEL + 2 else K("pared", 2))


def _desconchado(cv, x, y):
    """El yeso caído deja ver el ladrillo de debajo."""
    forma = ["....#######.......", "..############....", ".################.", "##################",
             ".#################", "..##############..", "....#########.....", "......####........"]
    for r, fila in enumerate(forma):
        for c, ch in enumerate(fila):
            if ch != "#":
                continue
            junta = r % 3 == 1 or (c + (r // 3) * 4) % 8 == 0                               # llagas del ladrillo
            cv.px(x + c, y + r, K("papel", 0) if junta else K("granate", 3 if (c // 8 + r // 3) % 2 else 2))
            if r == 0 or forma[r - 1][c] != "#":
                cv.px(x + c, y + r, K("granate", 1))                                          # el canto de yeso hace sombra
            if r + 1 >= len(forma) or forma[r + 1][c] != "#":
                cv.px(x + c, y + r + 1, K("pared", 5))                                        # canto roto, iluminado
    for k in range(4):                                                                        # trocitos en el suelo
        cv.px(x + 2 + k * 3, WB + 2 + k % 2, K("papel", 1))


def _escalera(cv):
    """Hueco de salida a la escalera (x 886-922): puerta abierta de par en par, peldaños que suben."""
    x0, x1, y0, y1 = 886, 922, 38, WB
    _oscurecer(cv, x1 + 3, y0 - 1, x1 + 6, y1, -1)
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1, K("gris", 3))
    cv.hline(x0 - 3, x1 + 3, y0 - 3, K("gris", 5)); cv.vline(x0 - 3, y0 - 3, y1, K("gris", 4))
    cv.vline(x1 + 2, y0 - 2, y1, K("gris", 1))
    cv.rect(x0, y0, x1, y1, K("gris", 0))
    for k in range(7):                                                                        # peldaños que suben
        yy = y1 - 6 - k * 8
        cv.rect(x0 + 1, yy, x1 - 1, yy + 6, K("gris", 1))
        cv.rect(x0 + 1, yy, x1 - 1, yy + 2, K("gris", 3 if k < 3 else 2))
        cv.hline(x0 + 1, x1 - 1, yy, K("gris", 4 if k < 3 else 3))
    cv.d.line([(x0 + 3, y1 - 12), (x0 + 3, y0 + 4)], fill=K("madera", 2))                    # pasamanos
    for k in range(4):
        cv.vline(x0 + 3, y1 - 12 - k * 14, y1 - 6 - k * 14, K("gris", 2))
    cv.rect(x0, y1 - 2, x1, y1, K("gris", 4))                                                 # umbral
    cv.rect(x0 - 3, y1, x1 + 3, y1 + 2, K("gris", 3))


def _suelo(cv, rnd):
    # linóleo en losetas grandes, con cenefa oscura junto a las paredes
    t = 16
    for y in range(WB, FB, t):
        for x in range(0, W, t):
            par = ((x // t) + (y - WB) // t) % 2 == 0
            cv.rect(x, y, x + t, min(y + t, FB), K("tela", 3) if par else K("tela", 2))
    for y in range(WB, FB, t):
        cv.hline(0, W, y, K("tela", 1))
    for x in range(0, W, t):
        cv.vline(x, WB, FB, K("tela", 1))
    cv.rect(0, WB, W, WB + 6, K("tela", 1)); cv.hline(0, W, WB + 6, K("tela", 0))              # cenefas
    cv.rect(0, FB - 6, W, FB, K("tela", 1)); cv.hline(0, W, FB - 7, K("tela", 0))
    for x in range(4, W, 8):
        cv.px(x, WB + 3, K("tela", 2)); cv.px(x, FB - 3, K("tela", 2))
    # el camino gastado por el centro: losetas descoloridas y marcas de tacón
    for x in range(0, W, 2):
        for y in range(132, 166, 3):
            if (x * 7 + y * 3) % 13 == 0 and abs(y - 149) < 14 - (x * 5 % 7):
                cv.px(x, y, K("tela", 4))
    for _ in range(46):
        x, y = rnd.randint(10, W - 20), rnd.randint(118, 182)
        cv.hline(x, x + rnd.randint(2, 5), y, K("tela", 0))
    # una loseta cambiada (de otro tono) y otra rajada
    cv.rect(337, 150, 352, 165, K("tela", 4)); cv.frame(337, 150, 352, 165, K("tela", 1))
    cv.d.line([(561, 167), (566, 172), (564, 178), (570, 181)], fill=K("tela", 0))
    # papelitos y una colilla de Victoria
    cv.rect(212, 176, 218, 180, K("papel", 3)); cv.hline(213, 217, 177, K("gris", 6))
    cv.px(498, 124, K("papel", 4)); cv.px(499, 124, K("papel", 4)); cv.px(500, 124, K("ocre", 2))
    cv.rect(812, 172, 819, 176, K("papel", 2))
    # los umbrales de las puertas
    for (a, b) in ((57, 95), (237, 275), (457, 495), (757, 795)):
        cv.rect(a, WB, b, WB + 2, K("gris", 3)); cv.hline(a, b, WB + 2, K("tela", 0))


def _muro_inferior(cv, rnd):
    """El muro de abajo visto desde arriba: tapa de hormigón ancha, con su filo y las juntas."""
    cv.rect(0, FB, W, H, K("gris", 3))
    cv.hline(0, W, FB, K("gris", 5)); cv.rect(0, FB + 1, W, FB + 3, K("gris", 4))
    cv.hline(0, W, FB + 12, K("gris", 2)); cv.hline(0, W, FB + 13, K("gris", 4))              # albardilla
    for x in range(0, W, 60):                                                                 # juntas de las losas
        cv.vline(x + 30, FB + 3, FB + 12, K("gris", 2))
    for x in range(0, W, 120):
        cv.vline(x, FB + 14, H, K("gris", 2)); cv.vline(x + 1, FB + 14, H, K("gris", 4))
    for _ in range(900):                                                                      # el árido del hormigón
        cv.px(rnd.randint(0, W - 1), rnd.randint(FB + 4, H - 1), K("gris", rnd.choice((2, 2, 4))))
    for (x, y) in ((140, 226), (402, 250), (611, 220), (780, 248)):                           # alguna grieta
        cv.d.line([(x, y), (x + 5, y + 3), (x + 9, y + 2), (x + 14, y + 6)], fill=K("gris", 1))


def _extremos(cv):
    """Los muros de los extremos (x < 8 y x >= 952), vistos desde arriba."""
    for (a, b) in ((0, XL), (XR, W)):
        cv.rect(a, WT - 12, b, FB, K("gris", 3))
        cv.vline(b - 1 if a == 0 else a, WT - 12, FB, K("gris", 5) if a == 0 else K("gris", 1))
        cv.vline(a if a == 0 else b - 1, WT - 12, FB, K("gris", 4))


def dibujar():
    rnd = random.Random(1405)
    cv = Canvas(W, H)
    _pared(cv, rnd)
    _tuberias(cv)
    # neones bajo la cornisa
    for nx in NEONES:
        cv.rect(nx - 25, 3, nx + 25, 11, K("gris", 2)); cv.hline(nx - 25, nx + 25, 3, K("gris", 4))
        cv.rect(nx - 23, 5, nx + 23, 8, K("papel", 4)); cv.hline(nx - 23, nx + 23, 7, K("papel", 3))
        cv.hline(nx - 23, nx + 23, 9, K("cielo", 6)); cv.hline(nx - 25, nx + 25, 10, K("gris", 1))
        for e in (nx - 25, nx + 24):
            cv.rect(e, 4, e + 1, 10, K("gris", 3))
        cv.add_emissive(nx - 23, 5, nx + 23, 10)
    _suelo(cv, rnd)
    # pared, de izquierda a derecha
    bajante(cv, 22, 23, WB - 6)
    rejilla(cv, 34, 78, 50, 88, polvo=False)
    puerta(cv, 60, rampa="madera", base=2, cristal=True, luz=True)
    cartel_puerta(cv, 52, 48, "CARTOGRAFIA")
    tablon(cv, 122, 40, 194, 72)
    rejilla(cv, 206, 34, 228, 46)
    puerta(cv, 240, rampa="madera", base=1)
    cartel_puerta(cv, 236, 40, "ARCHIVO")
    reloj(cv, 312, 46)
    cv.rect(333, 23, 336, 72, K("gris", 4)); cv.vline(333, 23, 72, K("gris", 6))               # tubería que baja al radiador
    cv.vline(335, 23, 72, K("gris", 2)); _oscurecer(cv, 336, 25, 338, 72, -2)
    radiador(cv, 290, 334, 72)
    P.telepantalla(cv, 352, 38, 46, 32)
    _gotera(cv, 430, rnd)
    puerta(cv, 460, rampa="madera", base=1, cristal=True)
    cartel_puerta(cv, 456, 40, "SALA 14-D")
    extintor(cv, 536, 60, 548, 91)
    P.cartel_gran_hermano(cv, 586, 34, w=36, h=46)
    _desconchado(cv, 652, 44)
    rejilla(cv, 690, 34, 714, 46)
    puerta(cv, 760, rampa="gris", base=3, rejilla=True)
    cartel_puerta(cv, 748, 56, "SUMINISTROS")
    cuadro_electrico(cv, 818, 44, 842, 74)
    _escalera(cv)
    cartel_puerta(cv, 880, 48, "ESCALERA")
    cv.rect(928, 40, 946, 52, K("papel", 3)); cv.frame(928, 40, 946, 52, K("gris", 2))       # número de planta
    cv.text(931, 44, "P14", K("gris", 1))
    bajante(cv, 940, 23, 38)
    lata_goteo(cv, 428, 101)
    carrito(cv, 700, 120)
    _muro_inferior(cv, rnd)
    _extremos(cv)

    # ---- luz: cada neón ilumina su tramo; entre uno y otro, penumbra
    def luz(x, y):
        if y < WT or x < XL or x >= XR:
            return 0
        d = min(abs(x - nx) for nx in NEONES)
        if y < WB:                                                   # cada tubo lava la pared en una cúpula de luz
            e = (d / 72) ** 2 + ((y - 4) / 92) ** 2
            return 1 if e < 0.3 else 0 if e < 1 else -1
        if y < FB:                                                   # y deja un charco de luz en el linóleo
            e = (d / 84) ** 2 + ((y - WB) / 64) ** 2
            n = 0 if e < 1 else -1
            if y < WB + 5 or y >= FB - 5:                            # oclusión junto a los muros
                n -= 1
            return n
        return -1 if y > 250 else 0                                  # el muro de abajo se apaga hacia el borde
    cv.add_light_fn(luz)
    cv.glow_rgb = K("cielo", 6)
    for nx in NEONES:
        cv.add_glow_suave(nx, 92, 100, 0.22, squash=1.6, limite=(XL, WT, XR, FB))
    cv.bake_lighting()
    # segunda pasada: el resplandor verde de la telepantalla
    cv.light = [[0] * W for _ in range(H)]
    cv.glow = [[0.0] * W for _ in range(H)]
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(375, 84, 84, 0.3, squash=1.3, limite=(XL, WT, XR, FB))
    cv.bake_lighting()
    return cv


if __name__ == "__main__":
    import sys
    from pathlib import Path
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("pasillo_prueba.png")
    dibujar().save(salida, preview_scale=2)
