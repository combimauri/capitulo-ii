"""La declaración voluntaria (DeclaracionScene), en la sala blanca del Minimor.

Mesa de acero cepillado atornillada al suelo (gris 8–10), sin una sombra (biblia §3.1, regla 6: el blanco del
Minimor no proyecta sombras), sin rojo y sin verde. Encima, la hoja del impreso: papel `papel 4` con membrete gris
(pirámide y «MINIMOR»), número de impreso, marco fino y pie. Al lado, la pluma de acero, la misma del prólogo, sujeta
a la mesa con una cadenita, y un clip. Nada más.

Pantalla → arte: hoja (130, 40, 700×440) → (65, 20)-(415, 240). Título en y = 70, texto desde (150, 120).
"""
import random

from pixel import Canvas, K
import papel as PP

HX0, HY0, HX1, HY1 = 65, 20, 415, 240


def _pluma(cv, x, y):
    """Pluma de acero, tumbada, con una cadenita hasta una argolla atornillada en la mesa."""
    cv.rect(x, y, x + 34, y + 4, K("gris", 6))
    cv.hline(x, x + 34, y, K("gris", 9)); cv.hline(x, x + 34, y + 3, K("gris", 4))
    cv.rect(x + 34, y, x + 40, y + 4, K("gris", 5)); cv.hline(x + 34, x + 40, y, K("gris", 8))
    cv.poly([(x + 40, y), (x + 46, y + 2), (x + 40, y + 3)], K("gris", 7))
    cv.px(x + 45, y + 2, K("gris", 2)); cv.hline(x + 41, x + 45, y + 2, K("gris", 4))
    cv.rect(x + 4, y - 2, x + 18, y, K("gris", 7))                              # el clip del capuchón
    # cadenita hasta la argolla
    ax, ay = x + 12, y + 24
    for k in range(10):
        cx_ = x + 2 + k; cy_ = y + 5 + int(k * 1.6)
        cv.px(cx_, cy_, K("gris", 5) if k % 2 else K("gris", 7))
    cv.ellipse(ax - 3, ay - 3, ax + 4, ay + 4, K("gris", 6), outline=K("gris", 4))
    cv.px(ax, ay, K("gris", 3))


def _tornillo(cv, x, y):
    cv.ellipse(x - 2, y - 2, x + 3, y + 3, K("gris", 7), outline=K("gris", 6))
    cv.hline(x - 1, x + 2, y, K("gris", 5))


def dibujar():
    rnd = random.Random(4)
    cv = Canvas(480, 270, ("gris", 9))
    PP.chapa(cv, 0, 0, 480, 270, base=9, semilla=40)
    cv.hline(0, 480, 268, K("gris", 8))
    for (x, y) in ((10, 10), (470, 10), (10, 260), (470, 260)):
        _tornillo(cv, x, y)
    # junta de la plancha de acero
    cv.vline(36, 0, 270, K("gris", 8)); cv.vline(37, 0, 270, K("gris", 10))
    cv.vline(444, 0, 270, K("gris", 8)); cv.vline(445, 0, 270, K("gris", 10))

    # la hoja: sin sombra, recortada solo por su canto
    m = PP.mascara_rect(HX0, HY0, HX1, HY1, rnd, mordidas=0.0, muescas=0)
    PP.pintar_hoja(cv, m, base=4, semilla=5, fibra=0.012, borde_col=K("gris", 7))
    cv.frame(HX0 + 5, HY0 + 5, HX1 - 5, HY1 - 5, K("papel", 3))
    PP.piramide(cv, HX0 + 14, HY0 + 11, 9, K("gris", 6))
    PP.texto_c(cv, HX0 + 23, HY0 + 23, "MINIMOR", K("gris", 6))
    cv.text(HX1 - 64, HY0 + 10, "IMPRESO D-1", K("gris", 7))
    cv.text(HX1 - 64, HY0 + 17, "EJEMPLAR UNICO", K("gris", 7))
    cv.hline(HX0 + 12, HX1 - 12, HY0 + 32, K("gris", 8))
    cv.text(HX0 + 12, HY1 - 12, "MINISTERIO DEL AMOR - SIN ENMIENDAS NI TACHADURAS", K("gris", 8))

    # la pluma y un clip, en la mesa
    _pluma(cv, 424, 196)
    cv.frame(424, 60, 432, 64, K("gris", 6)); cv.frame(426, 61, 434, 63, K("gris", 6))
    return cv


def exportar(destino):
    dibujar().img.save(destino / "declaracion-fondo.png")
    return ["declaracion-fondo.png"]
