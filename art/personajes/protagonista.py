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


# ---------------------------------------------------------------- aspectos (Minimor y después)
# Misma silueta, mismos fotogramas y misma hoja que la versión normal. Tres aspectos:
#   "preso":    ropa gris de preso, la cara intacta (llegada a la celda).
#   "golpeado": ropa gris de preso y la cara magullada: un ojo cerrado por la hinchazón, un moratón alrededor,
#               el labio partido y una costra en la frente. La espalda solo cambia de color.
#   "cafe":     el Final C, «algún tiempo después»: el mono azul de siempre sobre un cuerpo consumido (brazos y
#               torso 1 px más estrechos, cuello flaco, el pantalón le cae sobre los zapatos), el pelo ralo y canoso
#               y la cara recompuesta a medias: el ojo que estuvo cerrado ahora caído, una cicatriz que le parte
#               la ceja, la nariz torcida y la boca que ya no cierra recta.
ASPECTOS = ("preso", "golpeado", "cafe")

ROPA_PRESO = {"n": K("gris", 3), "d": K("gris", 4), "b": K("gris", 5), "B": K("gris", 6), "L": K("gris", 5),
              "w": K("gris", 1), "W": K("gris", 2)}
MAGULLADURAS = {"u": K("granate", 4), "U": K("granate", 3), "k": K("piel", 0), "R": K("rojo", 3),
                "q": K("granate", 2), "Q": K("rojo", 1)}
# canas: el contorno del pelo baja a gris medio y los mechones a gris claro; la cicatriz es rosada y lisa
CANAS = {"o": K("gris", 4), "h": K("gris", 7), "H": K("gris", 9), "c": K("granate", 5), "k": K("piel", 1)}
CANAS_F = {"o": K("gris", 4), "h": K("gris", 6), "H": K("gris", 8), "c": K("granate", 5), "k": K("piel", 1)}


def _pon(filas, cambios):
    f = [list(r) for r in filas]
    for r, c, ch in cambios:
        f[r][c] = ch
    return ["".join(x) for x in f]


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


def _golpear(filas, lateral=False):
    """_magullar y, además, una costra de sangre seca en la frente, en el lado del ojo sano."""
    f = _magullar(filas, lateral)
    if lateral:
        return _pon(f, [(7, 13, "q"), (7, 14, "Q")])
    return _pon(f, [(7, 6, "Q"), (7, 7, "q")])


# --- cafe: cuerpo consumido. Media fila frontal (se refleja); filas 18-39.
CUERPO_CAFE = [
    "....nndbOS",          # cuello del mono abierto: se le ve la clavícula
    "...ndbbbbO",
    "...ndbbbbL",          # hombros caídos
    "..ndnbbbbL",          # brazo de 1 px menos
    "..ndnBbbbL",
    "..ndnBbbbL",
    "..ndnbdbbL",          # el mono hace bolsa: un pliegue
    "..ndnbdbbL",
    "..ndnbbbbL",
    "..nnnbbbbL",          # puño de la manga, que le queda largo
    "..nsnbbdbL",          # mano huesuda
    "..nsnddddd",          # cinturón apretado, la tela fruncida debajo
    "..nndbdbdL",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",
    "...ndbbbbn",          # el pantalón le cae sobre los zapatos
    "...nwWwwwn",
    "...nnnnnn.",
]


# Cabeza calva por arriba (frente y espalda, media fila reflejada): coronilla de piel con brillo, canas a los
# lados y algún mechón suelto peinado por encima.
CRANEO_CAFE = [
    "......oOOO",
    ".....Oslll",
    "....ohslls",
    "...ohhssss",
    "...ohhssss",
    "...ohhhsss",
    "...ohhssss",
    "...ohsssss",
]
NUCA_CAFE = [
    "......oOOO",
    ".....Oslll",
    "....Ossllh",
    "...ohssshs",
    "...ohhssss",
    "...ohhhshs",
    "...ohhhhhh",
]
MECHONES = [(2, 12, "h"), (3, 9, "h"), (3, 10, "h"), (1, 13, "h"), (4, 13, "h")]


def _canas_mujer(filas, raya):
    """Melena canosa que clarea: la raya del pelo se abre y asoma el cuero cabelludo alrededor."""
    f = _pon(filas, [(r, c, "h") for r in range(0, 6) for c in range(W) if filas[r][c] == "H"])   # pelo sin brillo
    return _pon(f, [(r, c, "s") for r, c in raya if f[r][c] in "hH"])


def _cara_cafe_frente(filas, femenina):
    """Cara recompuesta torpemente (frente): la asimetría cae a la derecha de la imagen, el ojo que estuvo cerrado."""
    f = [list(r) for r in filas]
    for r in range(11, 13):                              # sin colorete
        for c in range(W):
            if f[r][c] == "l":
                f[r][c] = "s"
    cambios = [
        (11, 4, "l"), (12, 4, "S"), (12, 5, "S"),       # pómulo marcado y mejilla hundida (lado sano)
        (11, 6, "S"),                                    # ojera
        (8, 12, "o"), (8, 13, "o"), (8, 14, "c"), (8, 15, "s"), (9, 15, "o"),   # ceja partida que cae hacia fuera
        (7, 14, "c"),
        (9, 13, "S"), (9, 14, "S"), (10, 13, "e"), (10, 14, "e"),   # ojo caído: párpado pesado, una fila más abajo
        (11, 14, "c"), (12, 14, "c"), (12, 15, "S"),    # la cicatriz sigue por la mejilla
        (12, 9, "S"), (13, 8, "s"), (13, 9, "s"), (13, 10, "S"), (13, 11, "S"), (13, 12, "S"),   # nariz torcida
        (14, 11, "s"), (15, 11, "m"),                   # la boca cae por un lado
    ]
    if not femenina:
        cambios += [(14, 3, "."), (14, 4, "O"), (15, 4, "."), (15, 5, "O")]   # mandíbula hundida de un lado
    for r, c, ch in cambios:
        if f[r][c] != ".":
            f[r][c] = ch
    return ["".join(x) for x in f]


def _cuerpo_cafe(filas, cuello):
    return filas[:17] + [cuello] + espejo(CUERPO_CAFE)


def _frente_cafe(base, femenina):
    f = _cara_cafe_frente(base, femenina)
    if femenina:
        f = _cuerpo_cafe(f, "....oohhOSSOhhoo....")
        f = _canas_mujer(f, [(1, 9), (1, 10), (2, 9), (2, 10), (3, 9), (4, 9), (5, 9)])
        return _pon(f, [(r, c, ".") for r, c in ((16, 3), (17, 4), (15, 2), (14, 2), (16, 16), (17, 15), (15, 17))])
    f = espejo(CRANEO_CAFE) + f[8:]
    f = _cuerpo_cafe(f, "........OSSO........")
    return _pon(f, [(16, 5, "."), (16, 6, "O"), (16, 13, "O"), (16, 14, ".")] + MECHONES)   # cuello flaco


def _espalda_cafe(base, femenina):
    cuerpo = [r.replace("L", "b").replace("B", "b") for r in espejo(CUERPO_CAFE)[:-9]] + espejo(CUERPO_CAFE)[-9:]
    cuerpo = [r[:9] + ("d" if r[9] == "b" else r[9]) + r[10:] for r in cuerpo]
    cuerpo = _pon(cuerpo, [(0, 8, "O"), (0, 9, "S"), (0, 10, "S"), (0, 11, "O"), (1, 9, "d"), (1, 10, "b")])
    if femenina:
        f = _canas_mujer(base[:18], [(r, 9) for r in range(1, 7)] + [(1, 10), (2, 10)]) + cuerpo
        return _pon(f, [(r, c, ".") for r, c in ((19, 3), (20, 3), (19, 16), (20, 16), (17, 4), (17, 15))])
    f = espejo(NUCA_CAFE) + base[7:16] + ["........OSSO........", "........OSSO........"] + cuerpo
    f = _pon(f, [(15, 5, "."), (15, 6, "o"), (15, 13, "o"), (15, 14, "."), (2, 11, "h"), (1, 12, "h")])
    return _pon(f, [(13, 7, "o"), (13, 12, "o"), (14, 9, "S"), (14, 10, "S")])   # la nuca clarea


LADO_CAFE_CUERPO = [
    "........OSSOO.......",
    "........OSO.........",
    "......ndbOSn........",   # cuello del mono abierto
    ".....ndbbbbLn.......",
    ".....ndbbbbbLn......",
    ".....ndbbbbbbn......",
    ".....ndbnBbbbn......",
    ".....ndbnBbbbn......",
    ".....ndbnBdbbn......",
    ".....ndbnBdbbn......",
    ".....ndbnBbbbn......",
    ".....ndbnssbbn......",   # mano huesuda
    ".....ndbnssdbn......",
    ".....ndddddddn......",   # cinturón apretado
    "......ndbdbbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",
    "......ndbbnbbn......",   # el pantalón le cae sobre los zapatos
    "......nwWwnwWwn.....",
    "......nnnn.nnnnn....",
]


LADO_CAFE_CRANEO = [
    ".......OOOOOO.......",
    "......OslllssO......",
    ".....OsllllhssO.....",
    "....ohsllsshsssO....",
    "....ohhsssshssssO...",
    "....ohhhssssssssO...",
    "....ohhhhsssssssO...",
    "....ohhhhhhsssssO...",
]


def _lado_cafe(base, femenina):
    f = base[:16] + LADO_CAFE_CUERPO
    if not femenina:
        f = LADO_CAFE_CRANEO + f[8:]
    f = _pon(f, [
        (8, 11, "s"), (8, 12, "o"), (8, 13, "c"), (9, 14, "o"),   # ceja partida y caída hacia fuera
        (7, 13, "c"),
        (9, 12, "S"), (9, 13, "S"), (10, 12, "e"), (10, 13, "S"),  # ojo caído bajo un párpado pesado
        (11, 13, "c"), (12, 13, "c"),                             # la cicatriz sigue por la mejilla
        (12, 14, "s"), (12, 15, "s"), (11, 10, "S"),              # mejilla hundida, sin colorete
        (13, 13, "s"), (13, 14, "m"), (13, 15, "S"), (14, 14, "m"),   # boca que cae
        (14, 13, "s"), (15, 13, "O"), (14, 15, "O"),               # mandíbula flaca
    ])
    if femenina:
        f = _melena_lado(f)
        f = _canas_mujer(f, [(1, 8), (2, 9), (3, 10), (2, 10), (4, 11), (1, 9)])
        return _pon(f, [(r, 3, ".") for r in (15, 16, 17, 18, 19, 20)] + [(19, 4, "."), (20, 4, "."), (20, 5, "."),
                                                                      (18, 6, "d"), (19, 6, "d"), (20, 6, "n")])
    return f


def _con_izquierda(v):
    v["izquierda"] = [r[::-1] for r in v["derecha"]]
    return v


VISTAS_PRESO = {False: _con_izquierda({"abajo": FRENTE, "derecha": LADO_DER, "arriba": ESPALDA}),
                True: _con_izquierda({"abajo": FRENTE_F, "derecha": LADO_DER_F, "arriba": ESPALDA_F})}
VISTAS_GOLPEADO = {False: _con_izquierda({"abajo": _golpear(FRENTE), "derecha": _golpear(LADO_DER, lateral=True),
                                          "arriba": ESPALDA}),
                   True: _con_izquierda({"abajo": _golpear(FRENTE_F), "derecha": _golpear(LADO_DER_F, lateral=True),
                                         "arriba": ESPALDA_F})}
VISTAS_CAFE = {fem: _con_izquierda({"abajo": _frente_cafe(FRENTE_F if fem else FRENTE, fem),
                                    "derecha": _lado_cafe(LADO_DER, fem),
                                    "arriba": _espalda_cafe(ESPALDA_F if fem else ESPALDA, fem)})
               for fem in (False, True)}

# (femenina, aspecto) -> (vistas, paleta)
_TABLA = {
    (False, None): (VISTAS, PALETA),
    (True, None): (VISTAS_F, PALETA_F),
    (False, "preso"): (VISTAS_PRESO[False], {**PALETA, **ROPA_PRESO}),
    (True, "preso"): (VISTAS_PRESO[True], {**PALETA_F, **ROPA_PRESO}),
    (False, "golpeado"): (VISTAS_GOLPEADO[False], {**PALETA, **ROPA_PRESO, **MAGULLADURAS}),
    (True, "golpeado"): (VISTAS_GOLPEADO[True], {**PALETA_F, **ROPA_PRESO, **MAGULLADURAS}),
    (False, "cafe"): (VISTAS_CAFE[False], {**PALETA, **CANAS}),
    (True, "cafe"): (VISTAS_CAFE[True], {**PALETA_F, **CANAS_F}),
}

for (_fem, _asp), (_vistas, _pal) in _TABLA.items():
    for nombre, filas in _vistas.items():
        assert len(filas) == H, (_fem, _asp, nombre, len(filas))
        for i, f in enumerate(filas):
            assert len(f) == W, (_fem, _asp, nombre, i, len(f), f)
            assert all(ch == "." or ch in _pal for ch in f), (_fem, _asp, nombre, i, f)


def _aspecto(aspecto, preso):
    if preso and aspecto is None:                       # alias heredado: preso=True era la versión magullada
        aspecto = "golpeado"
    if aspecto not in (None,) + ASPECTOS:
        raise ValueError(f"aspecto desconocido: {aspecto!r} (usa None, {', '.join(ASPECTOS)})")
    return aspecto


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


def fotogramas(vista, femenina=False, aspecto=None, preso=False):
    """[quieto, paso A, pasando, paso B, pasando]"""
    aspecto = _aspecto(aspecto, preso)
    vistas = _TABLA[(femenina, aspecto)][0]
    if vista == "izquierda":
        return [[r[::-1] for r in fr] for fr in fotogramas("derecha", femenina, aspecto)]
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


def hoja_sprites(ruta, femenina=False, aspecto=None, preso=False):
    """Hoja de 5 columnas (quieto + 4 de caminar) x 4 filas (direcciones), fotogramas de 20x40.

    aspecto: None (el normal), "preso" (ropa gris, cara intacta), "golpeado" (ropa gris y cara magullada)
    o "cafe" (Final C: mono azul sobre un cuerpo consumido, canas y la cara recompuesta).
    Misma disposición en todos. preso=True se mantiene como alias de aspecto="golpeado".
    """
    aspecto = _aspecto(aspecto, preso)
    pal = _TABLA[(femenina, aspecto)][1]
    from pixel import Canvas
    cv = Canvas(W * 5, H * len(ORDEN_HOJA), bg=("gris", 0))
    cv.img = cv.img.convert("RGBA")
    cv.img.paste((0, 0, 0, 0), (0, 0, cv.w, cv.h))
    from PIL import ImageDraw
    cv.d = ImageDraw.Draw(cv.img)
    for fila, vista in enumerate(ORDEN_HOJA):
        for col, frame in enumerate(fotogramas(vista, femenina, aspecto)):
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
