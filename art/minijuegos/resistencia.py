"""FD.04 — Aguantar veinticuatro horas en la sala blanca del Minimor, con O'Brien.

Azulejo blanco, tubos fluorescentes, luz plana y sin sombras (biblia §1.2: solo gris alto y papel
pálido). O'Brien, detrás de su consola de acero (la consola es una pieza aparte que tapa el borde del
retrato), y en la pared el reloj que avanza a saltos: un fotograma por hora (0-11), las agujas siempre
en punto.

  resistencia-fondo    480x270
  resistencia-reloj    hoja de 12 fotogramas de 72x72 (la aguja de las horas en 0..11)
  resistencia-consola  136x62 (va delante del retrato)
  resistencia-obrien   96x96 (el retrato neutral de O'Brien con el fondo vaciado)
"""
import math
import sys

from _base import ART, Canvas, K, a_rgba, guardar, hoja, sprite

if str(ART / "personajes") not in sys.path:
    sys.path.insert(0, str(ART / "personajes"))
import retrato_obrien  # noqa: E402

W, H = 480, 270
TECHO, ZOCALO = 9, 186
BLANCO, BLANCO2, JUNTA = K("gris", 10), K("papel", 4), K("gris", 9)


def fondo():
    cv = Canvas(W, H, bg=("gris", 10))
    # techo con tres tubos fluorescentes
    cv.rect(0, 0, W, TECHO, K("gris", 9)); cv.hline(0, W, TECHO - 1, K("gris", 8))
    for x in (40, 200, 360):
        cv.rect(x, 2, x + 80, 6, K("gris", 8)); cv.rect(x + 2, 3, x + 78, 5, BLANCO2)
    # azulejo de la pared
    for y in range(TECHO, ZOCALO, 8):
        cv.hline(0, W, y, JUNTA)
    for x in range(0, W, 8):
        cv.vline(x, TECHO, ZOCALO, JUNTA)
    # rejilla de ventilación y puerta de acero a la derecha
    cv.rect(208, 22, 240, 38, K("gris", 8)); cv.frame(208, 22, 240, 38, K("gris", 6))
    for y in range(25, 36, 2):
        cv.hline(211, 237, y, K("gris", 5))
    dx0, dx1 = 466, 480
    cv.rect(dx0 - 3, 92, dx1, ZOCALO, K("gris", 7)); cv.rect(dx0, 95, dx1, ZOCALO, K("gris", 8))
    cv.vline(dx0, 95, ZOCALO, K("gris", 6))
    cv.rect(dx0 + 6, 104, dx0 + 20, 116, K("gris", 6)); cv.rect(dx0 + 7, 105, dx0 + 19, 115, K("cielo", 6))
    cv.rect(dx0 + 4, 140, dx0 + 7, 150, K("gris", 5))
    # zócalo y suelo de baldosa grande
    cv.rect(0, ZOCALO, W, ZOCALO + 4, K("gris", 8)); cv.hline(0, W, ZOCALO, K("gris", 7))
    cv.rect(0, ZOCALO + 4, W, H, BLANCO2)
    for y in range(ZOCALO + 4, H, 18):
        cv.hline(0, W, y, JUNTA)
    for i, y in enumerate(range(ZOCALO + 4, H, 18)):
        for x in range(-12 * (i % 2), W, 24):
            cv.vline(x, y, min(H, y + 18), JUNTA)
    # el cable de la consola, por el suelo, hacia la camilla (fuera de campo, abajo)
    pts = [(112, 196), (106, 206), (88, 228), (74, 250), (70, 270)]
    cv.d.line(pts, fill=K("gris", 3), width=2)
    # sumidero
    cv.rect(300, 236, 314, 242, K("gris", 7))
    for x in range(301, 314, 2):
        cv.vline(x, 237, 241, K("gris", 5))
    return cv.img


def _reloj(hora):
    cv = sprite(72, 72)
    c = 36
    cv.ellipse(c - 34, c - 34 + 2, c + 35, c + 35 + 2, K("gris", 8))            # resalte (no sombra)
    cv.ellipse(c - 34, c - 34, c + 35, c + 35, K("gris", 3))
    cv.ellipse(c - 32, c - 32, c + 33, c + 33, K("gris", 6))
    cv.ellipse(c - 29, c - 29, c + 30, c + 30, BLANCO2)
    for m in range(60):
        a = math.radians(m * 6 - 90)
        if m % 5 == 0:
            r0, col, w = 22 if m % 15 == 0 else 24, K("gris", 2), 2 if m % 15 == 0 else 1
        else:
            r0, col, w = 27, K("gris", 7), 1
        cv.d.line([(c + r0 * math.cos(a), c + r0 * math.sin(a)), (c + 28 * math.cos(a), c + 28 * math.sin(a))], fill=col, width=w)
    # minutero, siempre en punto
    cv.rect(c - 1, c - 25, c + 1, c + 1, K("gris", 1))
    # aguja de las horas
    a = math.radians(hora * 30 - 90)
    cv.d.line([(c, c), (round(c + 16 * math.cos(a)), round(c + 16 * math.sin(a)))], fill=K("gris", 1), width=3)
    cv.ellipse(c - 3, c - 3, c + 3, c + 3, K("gris", 1)); cv.px(c - 1, c - 1, K("gris", 6))
    return a_rgba(cv)


def reloj():
    return hoja([_reloj(h) for h in range(12)])


def consola():
    w, h = 136, 62
    cv = sprite(w, h)
    # tablero
    cv.rect(0, 0, w, 10, K("gris", 9)); cv.hline(0, w, 0, BLANCO); cv.frame(0, 0, w, 10, K("gris", 6))
    # frente de la consola
    cv.rect(2, 10, w - 2, 52, K("gris", 8)); cv.frame(2, 10, w - 2, 52, K("gris", 6))
    cv.hline(3, w - 3, 11, K("gris", 9))
    # interruptores
    for k in range(6):
        x = 10 + k * 10
        cv.rect(x, 18, x + 6, 26, K("gris", 6)); cv.rect(x + 1, 19, x + 5, 25, K("gris", 9))
        cv.rect(x + 2, 16 if k % 3 else 22, x + 4, 22 if k % 3 else 28, K("gris", 2))
        cv.hline(x, x + 6, 30, K("gris", 6))
    # escala pequeña y el mando grande
    mx, my = 104, 31
    for v in range(0, 11):
        a = math.radians(150 + v * 24)
        cv.px(round(mx + 15 * math.cos(a)), round(my + 15 * math.sin(a)), K("gris", 3))
    cv.text(mx - 16, my + 13, "1", K("gris", 4)); cv.text(mx + 6, my + 13, "100", K("gris", 4))
    cv.ellipse(mx - 10, my - 10, mx + 11, my + 11, K("gris", 3))
    cv.ellipse(mx - 9, my - 9, mx + 10, my + 10, K("gris", 1))
    cv.ellipse(mx - 7, my - 8, mx + 6, my + 3, K("gris", 2))
    cv.d.line([(mx, my), (mx - 6, my + 5)], fill=K("gris", 9), width=2)
    # piloto apagado y rejilla del altavoz
    cv.ellipse(76, 16, 84, 24, K("gris", 6)); cv.ellipse(77, 17, 83, 23, BLANCO2); cv.px(79, 18, BLANCO)
    for y in range(36, 48, 2):
        cv.hline(10, 66, y, K("gris", 6))
    # patas
    for x in (6, w - 10):
        cv.rect(x, 52, x + 4, h, K("gris", 6)); cv.vline(x, 52, h, K("gris", 7))
    return a_rgba(cv)


def obrien():
    """El retrato neutral, con su fondo plano vaciado (relleno desde los bordes)."""
    img = retrato_obrien.retrato("neutral").convert("RGBA")
    px = img.load()
    fondo_col = px[0, 0]
    pila = [(x, y) for x in range(img.width) for y in (0, img.height - 1)] + \
           [(x, y) for y in range(img.height) for x in (0, img.width - 1)]
    visto = set()
    while pila:
        x, y = pila.pop()
        if (x, y) in visto or not (0 <= x < img.width and 0 <= y < img.height):
            continue
        visto.add((x, y))
        if px[x, y] != fondo_col:
            continue
        px[x, y] = (0, 0, 0, 0)
        pila += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return img


def exportar(destino):
    return [guardar(fondo(), destino, "resistencia-fondo"), guardar(reloj(), destino, "resistencia-reloj"),
            guardar(consola(), destino, "resistencia-consola"), guardar(obrien(), destino, "resistencia-obrien")]
