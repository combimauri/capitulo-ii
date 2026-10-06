"""Protagonista (20x40) en cuatro direcciones.

Las vistas frontal y trasera se definen por mitades (10 columnas) y se reflejan.
La vista lateral se dibuja completa; la izquierda es el reflejo de la derecha.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import K  # noqa: E402

W, H = 20, 40

PALETA = {
    "o": K("pelo", 0), "h": K("pelo", 1), "H": K("pelo", 3),
    "O": K("piel", 1), "S": K("piel", 2), "s": K("piel", 3), "l": K("piel", 4),
    "e": K("gris", 1), "m": K("piel", 1),
    "n": K("azul", 0), "d": K("azul", 1), "b": K("azul", 2), "B": K("azul", 3), "L": K("azul", 4),
    "w": K("gris", 2), "W": K("gris", 4),
}


def espejo(mitades):
    return [m + m[::-1] for m in mitades]


CUERPO_FRENTE = [
    "....nndbbL",
    "...ndbbbbL",
    "..ndbbbbbL",
    ".ndbbbbbbL",
    ".ndbBBbbbL",
    ".ndbBBbbbL",
    ".ndbbbbbbL",
    ".ndbnbbbbL",
    ".ndbnbbbbL",
    ".nddnbbbbL",
    ".nssnbbbbL",
    ".nssnddddd",
    "..nndbbbbL",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...nwWwwwn",
    "...nwwwwwn",
    "...nnnnnn.",
]

FRENTE = espejo([
    "......oooo",
    ".....ohhhh",
    "....ohhhHH",
    "...ohhhHHh",
    "...ohhHhhh",
    "...ohhhhhh",
    "...ohhsshh",
    "...ohsssss",
    "...Osoooss",
    "...Osseess",
    "..OSsseess",
    "..OSssssss",
    "...Osllsss",
    "...OssssSS",
    "...OSsssmm",
    "....OSssss",
    ".....OOSSS",
    ".......OSS",
] + CUERPO_FRENTE)

ESPALDA = espejo([
    "......oooo",
    ".....ohhhh",
    "....ohhHhh",
    "...ohhHHhh",
    "...ohhhHhh",
    "...ohhhhhh",
    "...ohhhhhh",
    "...ohhhhhh",
    "...ohhhhhh",
    "...Ohhhhhh",
    "..OSohhhhh",
    "..OSohhhhh",
    "...Oohhhhh",
    "...Oohhhhh",
    "....ohhhhh",
    ".....ooSSS",
    ".......OSS",
    ".......OSS",
] + [r.replace("L", "b").replace("B", "b") for r in CUERPO_FRENTE[:-9]] + CUERPO_FRENTE[-9:])
# costura central de la espalda
ESPALDA = [r[:9] + ("d" if r[9] == "b" else r[9]) + r[10:] for r in ESPALDA]

LADO_DER = [
    ".......oooooo.......",
    "......ohhhhhho......",
    ".....ohhhhHHhho.....",
    "....ohhhhhhHHhho....",
    "....ohhhhhhhhhhho...",
    "....ohhhhhhhhhhho...",
    "....ohhhhhhhsssso...",
    "....ohhhhhhsssssO...",
    "....ohhhhhsoossssO..",
    "....ohhhhSssessssO..",
    "....ohhhSSssesssssO.",
    "....ohhhSSsssssssO..",
    "....ohhhOSssssllsO..",
    ".....ohhOSsssmmmO...",
    ".....ohhOSsssssO....",
    "......ooOSSsssO.....",
    "........OSSSOO......",
    "........OSSO........",
    "......ndbbbLn.......",
    ".....ndbbbbbLn......",
    ".....ndbbbbbbLn.....",
    ".....ndbbbbbbbn.....",
    ".....ndbnBBbbbn.....",
    ".....ndbnBbbbbn.....",
    ".....ndbnBbbbbn.....",
    ".....ndbnBbbbbn.....",
    ".....ndbnBbbbbn.....",
    ".....ndbnsssbbn.....",
    ".....ndbnsssbbn.....",
    ".....nddddddddn.....",
    "......ndbbbbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......nwWwnwWwn.....",
    "......nwwwnwwwwn....",
    "......nnnn.nnnnn....",
]
LADO_IZQ = [r[::-1] for r in LADO_DER]

VISTAS = {"abajo": FRENTE, "derecha": LADO_DER, "arriba": ESPALDA, "izquierda": LADO_IZQ}

for nombre, filas in VISTAS.items():
    assert len(filas) == H, (nombre, len(filas))
    for i, f in enumerate(filas):
        assert len(f) == W, (nombre, i, len(f), f)


# Piernas por vista: (fila donde empiezan, columnas de la pierna A, columnas de la pierna B)
PIERNAS = {
    "abajo": (31, range(3, 10), range(10, 17)),
    "arriba": (31, range(3, 10), range(10, 17)),
    "derecha": (30, range(6, 11), range(10, 16)),
    "izquierda": (30, range(9, 14), range(4, 10)),
}


def levantar(filas, desde, columnas):
    """Sube 1 px las columnas de una pierna (paso) y vacía la última fila."""
    f = [list(r) for r in filas]
    for r in range(desde, H - 1):
        for c in columnas:
            f[r][c] = f[r + 1][c]
    for c in columnas:
        f[H - 1][c] = "."
    return ["".join(r) for r in f]


def fotogramas(vista):
    """[quieto, paso A, pasando, paso B, pasando]"""
    base = VISTAS[vista]
    desde, a, b = PIERNAS[vista]
    return [base, levantar(base, desde, a), base, levantar(base, desde, b), base]


ORDEN_HOJA = ["abajo", "izquierda", "derecha", "arriba"]


def hoja_sprites(ruta):
    """Hoja de 5 columnas (quieto + 4 de caminar) x 4 filas (direcciones), fotogramas de 20x40."""
    from pixel import Canvas
    cv = Canvas(W * 5, H * len(ORDEN_HOJA), bg=("gris", 0))
    cv.img = cv.img.convert("RGBA")
    cv.img.paste((0, 0, 0, 0), (0, 0, cv.w, cv.h))
    from PIL import ImageDraw
    cv.d = ImageDraw.Draw(cv.img)
    for fila, vista in enumerate(ORDEN_HOJA):
        for col, frame in enumerate(fotogramas(vista)):
            for r, row in enumerate(frame):
                for c, ch in enumerate(row):
                    if ch in PALETA:
                        cv.img.putpixel((col * W + c, fila * H + r), PALETA[ch] + (255,))
    cv.img.save(ruta)
    return ruta


def dibujar(cv, x, y, vista="abajo", sombra=None):
    if sombra:
        cv.ellipse(x + 2, y + 35, x + 18, y + 43, sombra)
    cv.grid(x, y, VISTAS[vista], PALETA)


if __name__ == "__main__":
    from pixel import Canvas
    cv = Canvas(4 * 32, 56, bg=("pared", 3))
    for i, v in enumerate(["abajo", "derecha", "arriba", "izquierda"]):
        dibujar(cv, 6 + i * 32, 6, v, sombra=K("pared", 1))
    prev = cv.save(Path(__file__).parent / "protagonista_hoja.png", preview_scale=6)
    print("ok", prev)
