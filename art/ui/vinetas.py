"""Viñetas fijas de los montajes de los finales (480x270, el juego las dibuja a 2x).

plaza:    la Semana del Odio. La plaza llena, banderas, la tribuna y el Gran Hermano en una pantalla gigante.
patibulo: el Parque de la Victoria. El patíbulo con dos cuerdas; abajo, la multitud.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402
import props as P  # noqa: E402

W, H = 480, 270


def multitud(cv, y0, y1, rnd, filas=6):
    for f in range(filas):
        y = y0 + f * (y1 - y0) // filas
        x = rnd.randint(-4, 4)
        while x < W:
            tono = K("gris", 1 + (f % 2)) if rnd.random() > 0.08 else K("azul", 1)
            cv.ellipse(x, y, x + 9, y + 9, tono)
            cv.rect(x - 1, y + 7, x + 10, y + 20, tono)
            x += rnd.randint(9, 13)


def plaza():
    rnd = random.Random(1984)
    cv = Canvas(W, H, bg=("cielo", 3))
    # pantalla gigante con el rostro
    cv.rect(160, 10, 320, 110, K("gris", 1)); cv.rect(166, 16, 314, 104, K("tele", 1))
    cara = Canvas(24, 24, bg=("tele", 1))                 # el rostro, a 4x: ocupa la pantalla
    P.cara_gran_hermano(cara, 0, 0)
    cv.img.paste(cara.img.resize((72, 72), 0), (204, 24))
    cv.add_emissive(166, 16, 314, 104)
    # banderas
    for bx in (40, 110, 350, 420):
        cv.vline(bx, 20, 150, K("gris", 3)); cv.rect(bx + 1, 22, bx + 30, 60, K("rojo", 3)); cv.rect(bx + 10, 34, bx + 20, 46, K("papel", 3))
    # tribuna
    cv.rect(180, 118, 300, 150, K("gris", 2)); cv.hline(180, 300, 118, K("gris", 4))
    cv.rect(234, 104, 246, 120, K("gris", 0)); cv.ellipse(234, 96, 246, 106, K("piel", 2))      # el orador
    # efigie colgada
    cv.vline(140, 60, 100, K("madera", 1)); cv.rect(134, 100, 146, 130, K("granate", 2)); cv.ellipse(134, 90, 146, 102, K("papel", 2))
    multitud(cv, 150, 270, rnd, filas=8)
    cv.bake_lighting()
    return cv


def patibulo():
    rnd = random.Random(7)
    cv = Canvas(W, H, bg=("cielo", 4))
    for i, y in enumerate(range(0, 120, 20)):
        cv.rect(0, y, W, y + 20, K("cielo", 4 - (i % 2)))
    # árboles pelados del parque
    for tx in (30, 90, 400, 450):
        cv.vline(tx, 40, 150, K("madera", 0)); cv.d.line([(tx, 70), (tx - 14, 50)], fill=K("madera", 0)); cv.d.line([(tx, 90), (tx + 16, 66)], fill=K("madera", 0))
    # el patíbulo: travesaño, dos cuerdas, dos figuras (la del pañuelo, a la izquierda)
    cv.rect(170, 40, 310, 46, K("madera", 1)); cv.rect(176, 46, 182, 160, K("madera", 1)); cv.rect(298, 46, 304, 160, K("madera", 1))
    cv.rect(160, 150, 320, 162, K("madera", 2))
    for (cx, panuelo) in ((220, True), (262, False)):
        cv.vline(cx, 46, 74, K("papel", 1))
        cv.ellipse(cx - 5, 72, cx + 5, 82, K("gris", 2))
        if panuelo:
            cv.poly([(cx - 6, 74), (cx + 6, 74), (cx + 4, 70), (cx - 4, 70)], K("granate", 3))
        cv.rect(cx - 5, 82, cx + 5, 112, K("gris", 1)); cv.vline(cx - 2, 112, 126, K("gris", 1)); cv.vline(cx + 2, 112, 126, K("gris", 1))
    multitud(cv, 168, 270, rnd, filas=7)
    cv.bake_lighting()
    return cv


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    plaza().img.save(destino / "plaza.png")
    plaza().img.convert("L").convert("RGB").save(destino / "plaza_gris.png")      # FA.04: hasta el rojo se vuelve gris
    patibulo().img.save(destino / "patibulo.png")
    return ["plaza", "patibulo"]
