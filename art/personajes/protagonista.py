"""Protagonista (20x40) en cuatro direcciones.

Las vistas frontal y trasera se definen por mitades (10 columnas) y se reflejan.
La vista lateral se dibuja completa; la izquierda es el reflejo de la derecha.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
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


# ---------------------------------------------------------------- versión femenina
def _melena_espalda(filas):
    f = [list(r) for r in filas]
    for r in range(13, 21):                       # el pelo cae hasta los hombros
        for c in range(3, 17):
            if r >= 18 and not (3 <= c <= 5 or 14 <= c <= 16):
                continue
            f[r][c] = "o" if c in (3, 16) else ("H" if c in (8, 11) and r < 17 else "h")
    return ["".join(x) for x in f]


def _melena_lado(filas):
    f = [list(r) for r in filas]
    for r in range(11, 21):                       # melena por detrás de la oreja
        for c in range(3, 8):
            if f[r][c] in ".o" or (r >= 18 and c < 7):
                f[r][c] = "o" if c == 3 else "h"
    return ["".join(x) for x in f]


def _frente_f():
    import elenco
    return elenco.construir("melena", "mono")


FRENTE_F = _frente_f()
ESPALDA_F = _melena_espalda(ESPALDA)
LADO_DER_F = _melena_lado(LADO_DER)
LADO_IZQ_F = [r[::-1] for r in LADO_DER_F]
VISTAS_F = {"abajo": FRENTE_F, "derecha": LADO_DER_F, "arriba": ESPALDA_F, "izquierda": LADO_IZQ_F}
PALETA_F = {**PALETA, "o": K("madera", 1), "h": K("madera", 2), "H": K("madera", 4)}

for _vistas in (VISTAS, VISTAS_F):
    for nombre, filas in _vistas.items():
        assert len(filas) == H, (nombre, len(filas))
        for i, f in enumerate(filas):
            assert len(f) == W, (nombre, i, len(f), f)


# ---------------------------------------------------------------- versión presa (Minimor)
# Misma silueta y mismos fotogramas; ropa gris de preso y la cara magullada: un ojo cerrado por la hinchazón,
# un moratón alrededor y el labio partido. La espalda solo cambia de color.
ROPA_PRESO = {"n": K("gris", 3), "d": K("gris", 4), "b": K("gris", 5), "B": K("gris", 6), "L": K("gris", 5),
              "w": K("gris", 1), "W": K("gris", 2)}
MAGULLADURAS = {"u": K("granate", 4), "U": K("granate", 3), "k": K("piel", 0), "R": K("rojo", 3)}


def _magullar(filas, lateral=False):
    """Cierra el ojo de la derecha de la imagen (en la vista lateral, el único que se ve) y parte el labio."""
    f = [list(r) for r in filas]
    ojo = [(r, c) for r in range(6, 13) for c in range(W) if f[r][c] == "e" and (lateral or c >= W // 2)]
    filas_ojo = sorted({r for r, _ in ojo})
    cols = sorted({c for _, c in ojo})
    for r, c in ojo:                                    # párpado hinchado y una raya oscura: el ojo cerrado
        f[r][c] = "u" if r == filas_ojo[0] and len(filas_ojo) > 1 else "k"
    piel = set("sSl")
    abajo = filas_ojo[-1] + 1
    for c in range(cols[0] - 1, cols[-1] + 2):          # moratón debajo y a los lados
        if f[abajo][c] in piel:
            f[abajo][c] = "U" if c in cols else "u"
    for c in (cols[0] - 1, cols[-1] + 1):
        for r in filas_ojo:
            if f[r][c] in piel:
                f[r][c] = "u"
    boca = [(r, c) for r in range(11, 17) for c in range(W) if f[r][c] == "m"]
    if boca:                                            # labio partido: la comisura y una gota debajo
        r, c = max(boca, key=lambda rc: (rc[1], rc[0])) if not lateral else min(boca, key=lambda rc: rc[1])
        c = c - 1 if not lateral else c
        f[r][c] = "R"
        if f[r + 1][c] in piel:
            f[r + 1][c] = "U"
    return ["".join(x) for x in f]


VISTAS_P = {"abajo": _magullar(FRENTE), "derecha": _magullar(LADO_DER, lateral=True), "arriba": ESPALDA}
VISTAS_P["izquierda"] = [r[::-1] for r in VISTAS_P["derecha"]]
VISTAS_PF = {"abajo": _magullar(FRENTE_F), "derecha": _magullar(LADO_DER_F, lateral=True), "arriba": ESPALDA_F}
VISTAS_PF["izquierda"] = [r[::-1] for r in VISTAS_PF["derecha"]]
PALETA_P = {**PALETA, **ROPA_PRESO, **MAGULLADURAS}
PALETA_PF = {**PALETA_F, **ROPA_PRESO, **MAGULLADURAS}


# Piernas por vista: (fila donde empiezan, columnas de la pierna A, columnas de la pierna B)
PIERNAS = {
    "abajo": (31, range(3, 10), range(10, 17)),
    "arriba": (31, range(3, 10), range(10, 17)),
    "derecha": (30, range(6, 11), range(10, 16)),
}
# Manos en la vista frontal/trasera (filas, columnas izquierda, columnas derecha)
MANOS = (range(27, 30), range(1, 4), range(16, 19))


def levantar(filas, desde, columnas, px=2):
    """Sube unos píxeles las columnas de una pierna: el pie que avanza hacia la cámara (o se aleja)."""
    f = [list(r) for r in filas]
    for r in range(desde, H):
        for c in columnas:
            f[r][c] = f[r + px][c] if r + px < H else "."
    return ["".join(r) for r in f]


def bajar_torso(filas, desde):
    """Rebote del paso: en el apoyo, todo lo que está por encima de las piernas baja 1 px."""
    return ["." * W] + filas[:desde] + filas[desde + 1:]


def mover_manos(filas, arriba, abajo):
    """Balanceo de brazos en la vista frontal: una mano sube 1 px y la otra baja 1 px."""
    f = [list(r) for r in filas]
    filas_m = MANOS[0]
    for cols, d in ((arriba, -1), (abajo, 1)):
        orig = [[filas[r][c] for c in cols] for r in filas_m]
        for i, r in enumerate(filas_m):
            for j, c in enumerate(cols):
                f[r][c] = "n" if orig[i][j] != "." and f[r][c] != "." else f[r][c]
        for i, r in enumerate(filas_m):
            for j, c in enumerate(cols):
                if orig[i][j] in "sS":
                    f[r + d][c] = orig[i][j]
    return ["".join(r) for r in f]


def zancada(filas, desde, atras, delante, lejana_delante=False):
    """Vista lateral: las piernas se abren en V. Si la pierna que va delante es la lejana, va en sombra."""
    f = [list(r) for r in filas]
    sombra = {"b": "d", "B": "d", "W": "w"}
    for r in range(desde + 1, H):
        k = 0 if r < desde + 3 else 1 if r < desde + 6 else 2
        orig = filas[r]
        for c in range(min(atras) - 3, max(delante) + 4):
            if 0 <= c < W:
                f[r][c] = "."
        capas = [(delante, 1, True), (atras, -1, False)] if lejana_delante else [(atras, -1, False), (delante, 1, False)]
        for cols, sentido, oscura in capas:
            for c in cols:
                if orig[c] != "." and 0 <= c + k * sentido < W:
                    f[r][c + k * sentido] = sombra.get(orig[c], orig[c]) if oscura else orig[c]
    return ["".join(r) for r in f]


def mano_lateral(filas, dx):
    """El brazo cercano se balancea: la mano se desplaza dx px."""
    f = [list(r) for r in filas]
    for r in (26, 27, 28):
        fila = filas[r]
        seg = [c for c in range(8, 13) if fila[c] in "sS"]
        for c in seg:
            f[r][c] = "b"
        for c in seg:
            f[r][c + dx] = fila[c]
    return ["".join(r) for r in f]


def fotogramas(vista, femenina=False, preso=False):
    """[quieto, paso A, pasando, paso B, pasando]"""
    if preso:
        vistas = VISTAS_PF if femenina else VISTAS_P
    else:
        vistas = VISTAS_F if femenina else VISTAS
    if vista == "izquierda":
        return [[r[::-1] for r in fr] for fr in fotogramas("derecha", femenina, preso)]
    base = vistas[vista]
    desde, a, b = PIERNAS[vista]
    if vista == "derecha":
        paso_a = mano_lateral(zancada(base, desde, a, b), -1)
        paso_b = mano_lateral(zancada(base, desde, a, b, lejana_delante=True), 1)
    else:
        izq, der = MANOS[1], MANOS[2]
        paso_a = mover_manos(levantar(base, desde, a), arriba=der, abajo=izq)
        paso_b = mover_manos(levantar(base, desde, b), arriba=izq, abajo=der)
    return [base, bajar_torso(paso_a, desde), base, bajar_torso(paso_b, desde), base]


ORDEN_HOJA = ["abajo", "izquierda", "derecha", "arriba"]


def hoja_sprites(ruta, femenina=False, preso=False):
    """Hoja de 5 columnas (quieto + 4 de caminar) x 4 filas (direcciones), fotogramas de 20x40.

    preso=True: la misma hoja (misma disposición) con la ropa gris de preso y la cara magullada.
    """
    from pixel import Canvas
    cv = Canvas(W * 5, H * len(ORDEN_HOJA), bg=("gris", 0))
    cv.img = cv.img.convert("RGBA")
    cv.img.paste((0, 0, 0, 0), (0, 0, cv.w, cv.h))
    from PIL import ImageDraw
    cv.d = ImageDraw.Draw(cv.img)
    for fila, vista in enumerate(ORDEN_HOJA):
        if preso:
            pal = PALETA_PF if femenina else PALETA_P
        else:
            pal = PALETA_F if femenina else PALETA
        for col, frame in enumerate(fotogramas(vista, femenina, preso)):
            for r, row in enumerate(frame):
                for c, ch in enumerate(row):
                    if ch in pal:
                        cv.img.putpixel((col * W + c, fila * H + r), pal[ch] + (255,))
    cv.img.save(ruta)
    return ruta


def dibujar(cv, x, y, vista="abajo", sombra=None):
    if sombra:
        cv.ellipse(x + 2, y + 35, x + 18, y + 43, sombra)
    cv.grid(x, y, VISTAS[vista], PALETA)


def hoja_paseo(ruta):
    """Vista previa: los 5 fotogramas de cada dirección, H y M."""
    from pixel import Canvas
    cv = Canvas(10 * 24 + 8, 4 * 44 + 8, bg=("pared", 3))
    for g, fem in enumerate((False, True)):
        pal = PALETA_F if fem else PALETA
        for fila, vista in enumerate(ORDEN_HOJA):
            for col, frame in enumerate(fotogramas(vista, fem)):
                cv.grid(4 + (g * 5 + col) * 24, 4 + fila * 44, frame, pal)
    return cv.save(ruta, preview_scale=5)


if __name__ == "__main__":
    from pixel import Canvas
    print("ok", hoja_paseo(Path(__file__).parent / "protagonista_paseo.png"))
    cv = Canvas(4 * 32, 56, bg=("pared", 3))
    for i, v in enumerate(["abajo", "derecha", "arriba", "izquierda"]):
        dibujar(cv, 6 + i * 32, 6, v, sombra=K("pared", 1))
    prev = cv.save(Path(__file__).parent / "protagonista_hoja.png", preview_scale=6)
    print("ok", prev)
