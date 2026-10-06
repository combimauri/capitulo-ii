"""J8.04 — El cerrojo de combinación del Archivo Restringido.

La puerta de acero del archivo, de cerca: la placa remachada con el rótulo estampado, cuatro ventanas
para las ruedas, la plaquita grabada con la pista y, a la derecha, el cerrojo de llave ya abierto con
la llave «A.R. – 1» todavía puesta. Las ruedas son tambores numerados (un fotograma por cifra) y las
flechas, botones moleteados.

  combinacion-fondo   480x270
  combinacion-rueda   hoja de 10 fotogramas de 40x56 (cifras 0-9)
  combinacion-flecha  hoja de 2 fotogramas de 24x22 (arriba, abajo)
"""
import random

from _base import CLAVE, Canvas, K, a_rgba, guardar, hoja, sprite, texto_escalado, ancho_escalado

W, H = 480, 270
PLACA = (100, 40, 380, 220)
RUEDAS_X = [157, 212, 267, 322]             # centros en el arte (el juego: 314 + i·110)
RUEDA_Y = (97, 153)
PISTA = (138, 181, 342, 199)                # plaquita bajo el texto «Código: …» (y=380 en el juego)


def _acero(cv, x0, y0, x1, y1, base=5, semilla=1):
    """Acero cepillado: vetas horizontales de un tono."""
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K("gris", base))
    for y in range(y0, y1):
        if rnd.random() < 0.35:
            a = rnd.randint(x0, x1 - 6)
            cv.hline(a, min(x1, a + rnd.randint(8, 40)), y, K("gris", base + rnd.choice([-1, 1])))


def _remache(cv, x, y):
    cv.ellipse(x - 3, y - 3, x + 4, y + 4, K("gris", 3))
    cv.ellipse(x - 2, y - 2, x + 3, y + 3, K("gris", 6))
    cv.px(x - 1, y - 1, K("gris", 8))


def fondo():
    rnd = random.Random(3)
    cv = Canvas(W, H, bg=("pared", 2))
    # pared del pasillo a los lados
    for x in range(0, W, 8):
        cv.vline(x, 0, H, K("pared", 1)); cv.vline(x + 4, 0, H, K("pared", 3))
    # marco y hoja de la puerta
    cv.rect(68, 0, 412, H, K("gris", 2)); cv.vline(68, 0, H, K("gris", 4)); cv.vline(411, 0, H, K("gris", 1))
    _acero(cv, 76, 0, 404, H, base=4, semilla=2)
    cv.vline(76, 0, H, K("gris", 6)); cv.vline(403, 0, H, K("gris", 2))
    for y in (8, 262):
        for x in range(84, 400, 20):
            cv.px(x, y, K("gris", 6)); cv.px(x + 1, y + 1, K("gris", 2))
    # la placa
    x0, y0, x1, y1 = PLACA
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("gris", 1))
    _acero(cv, x0, y0, x1, y1, base=6, semilla=5)
    cv.frame(x0, y0, x1, y1, K("gris", 3))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("gris", 8)); cv.vline(x0 + 1, y0 + 1, y1 - 1, K("gris", 7))
    cv.hline(x0 + 1, x1 - 1, y1 - 2, K("gris", 4)); cv.vline(x1 - 2, y0 + 1, y1 - 1, K("gris", 4))
    for (rx, ry) in ((110, 50), (370, 50), (110, 210), (370, 210)):
        _remache(cv, rx, ry)
    # rótulo estampado
    t = "ARCHIVO RESTRINGIDO"
    tw = ancho_escalado(t)
    texto_escalado(cv, 240 - tw // 2, 54, t, K("gris", 8))
    texto_escalado(cv, 240 - tw // 2, 53, t, K("gris", 2))
    cv.hline(150, 330, 68, K("gris", 4)); cv.hline(150, 330, 69, K("gris", 7))
    # ventanas de las ruedas: rebaje oscuro y biselado
    ry0, ry1 = RUEDA_Y
    for cx in RUEDAS_X:
        cv.rect(cx - 23, ry0 - 3, cx + 23, ry1 + 3, K("gris", 3))
        cv.hline(cx - 23, cx + 23, ry0 - 3, K("gris", 2)); cv.vline(cx - 23, ry0 - 3, ry1 + 3, K("gris", 2))
        cv.hline(cx - 23, cx + 23, ry1 + 2, K("gris", 8)); cv.vline(cx + 22, ry0 - 3, ry1 + 3, K("gris", 7))
        cv.rect(cx - 20, ry0, cx + 20, ry1, K("gris", 0))
        # marca índice a los lados
        for sx in (cx - 26, cx + 24):
            cv.rect(sx, 123, sx + 2, 127, K("ocre", 2)); cv.px(sx, 123, K("ocre", 3))
    # plaquita con la pista (el texto lo pone el juego)
    px0, py0, px1, py1 = PISTA
    cv.rect(px0 + 1, py0 + 1, px1 + 1, py1 + 1, K("gris", 3))
    cv.rect(px0, py0, px1, py1, K("gris", 8)); cv.frame(px0, py0, px1, py1, K("gris", 5))
    cv.hline(px0 + 1, px1 - 1, py0 + 1, K("gris", 9))
    for sx in (px0 + 3, px1 - 4):
        cv.px(sx, (py0 + py1) // 2, K("gris", 4))
    # cerrojo de llave, abierto, con la llave puesta y su etiqueta
    kx, ky = 352, 112
    cv.ellipse(kx - 7, ky - 7, kx + 8, ky + 8, K("gris", 3))                          # escudo de acero
    cv.ellipse(kx - 6, ky - 6, kx + 7, ky + 7, K("gris", 7)); cv.px(kx - 3, ky - 4, K("gris", 9))
    cv.ellipse(kx - 3, ky - 3, kx + 4, ky + 4, K("gris", 4))
    cv.rect(kx - 2, ky - 1, kx + 8, ky + 2, K("ocre", 0)); cv.hline(kx - 1, kx + 8, ky, K("ocre", 3))   # caña girada
    cv.ellipse(kx + 7, ky - 4, kx + 16, ky + 5, K("ocre", 0))                         # ojo de la llave
    cv.ellipse(kx + 8, ky - 3, kx + 15, ky + 4, K("ocre", 2)); cv.px(kx + 9, ky - 2, K("ocre", 4))
    cv.ellipse(kx + 10, ky - 1, kx + 13, ky + 2, K("gris", 5))
    kx += 3
    cv.d.line([(kx + 9, ky + 4), (kx + 10, ky + 12)], fill=K("papel", 1))
    cv.poly([(kx + 4, ky + 12), (kx + 17, ky + 13), (kx + 16, ky + 30), (kx + 3, ky + 29)], K("papel", 4))
    cv.d.polygon([(kx + 4, ky + 12), (kx + 17, ky + 13), (kx + 16, ky + 30), (kx + 3, ky + 29)], outline=K("papel", 1))
    cv.text(kx + 5, ky + 16, "AR", K("gris", 2)); cv.text(kx + 7, ky + 22, "1", K("gris", 2))
    # pasador del cerrojo, retirado
    cv.rect(372, 140, 380, 160, K("gris", 3)); cv.rect(373, 141, 379, 159, K("gris", 6))
    cv.hline(373, 379, 141, K("gris", 8))
    # arañazos alrededor de las ruedas (manos nerviosas)
    for _ in range(18):
        sx, sy = rnd.randint(130, 350), rnd.randint(158, 176)
        cv.hline(sx, sx + rnd.randint(2, 5), sy, K("gris", 8))
    # luz: fluorescente de pasillo, desde arriba
    cv.glow_rgb = K("cielo", 6)
    cv.add_glow_suave(240, -20, 260, 0.14, squash=1.4)
    cv.bake_lighting()
    return cv.img


CIFRAS_5x7 = {
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
}


def _cifra(cv, x, y, c, col, ex=3, ey=3):
    for r, fila in enumerate(CIFRAS_5x7[c]):
        for k, b in enumerate(fila):
            if b == "1":
                cv.rect(x + k * ex, y + r * ey, x + (k + 1) * ex, y + (r + 1) * ey, col)


def _rueda(n):
    cv = sprite(40, 56)
    cv.rect(0, 0, 40, 56, K("gris", 1))
    # tambor: tonos por bandas horizontales (cilindro)
    bandas = [(0, 6, 1), (6, 12, 2), (12, 18, 3), (18, 38, 4), (38, 44, 3), (44, 50, 2), (50, 56, 1)]
    for a, b, t in bandas:
        cv.rect(2, a, 38, b, K("gris", t))
    cv.vline(2, 0, 56, K("gris", 0)); cv.vline(37, 0, 56, K("gris", 0))
    cv.vline(3, 18, 38, K("gris", 5))
    # cifras vecinas, aplastadas y en sombra
    _cifra(cv, 13, 3, str((n - 1) % 10), K("gris", 5), ey=1)
    _cifra(cv, 13, 46, str((n + 1) % 10), K("gris", 5), ey=1)
    # cifra principal
    _cifra(cv, 14, 19, str(n), K("gris", 1))
    _cifra(cv, 13, 18, str(n), K("papel", 4))
    # separadores entre cifras
    cv.hline(3, 37, 13, K("gris", 0)); cv.hline(3, 37, 42, K("gris", 0))
    return a_rgba(cv)


def rueda():
    return hoja([_rueda(n) for n in range(10)])


def _flecha(arriba):
    cv = sprite(24, 22)
    cv.rect(1, 1, 24, 22, K("gris", 2))                                      # sombra
    cv.rect(0, 0, 23, 21, K("gris", 3))
    cv.rect(1, 1, 22, 20, K("gris", 5)); cv.hline(1, 22, 1, K("gris", 7)); cv.vline(1, 1, 20, K("gris", 6))
    cv.hline(1, 22, 19, K("gris", 4))
    for x in range(3, 21, 2):                                               # moleteado
        cv.px(x, 3, K("gris", 4)); cv.px(x, 17, K("gris", 6))
    pts = [(11.5, 6), (18, 15), (5, 15)] if arriba else [(11.5, 15), (18, 6), (5, 6)]
    cv.poly([(x, y + 1) for x, y in pts], K("gris", 7))
    cv.poly(pts, K("gris", 1))
    return a_rgba(cv)


def flecha():
    return hoja([_flecha(True), _flecha(False)])


def exportar(destino):
    return [guardar(fondo(), destino, "combinacion-fondo"), guardar(rueda(), destino, "combinacion-rueda"),
            guardar(flecha(), destino, "combinacion-flecha")]
