"""Generador modular del elenco (vista frontal, 20x40; niños 16x27).

Cada personaje = cabeza (18 filas) + cuerpo (22 filas) + parches + paleta.
Las piezas se definen por mitades de 10 columnas y se reflejan (simetría frontal).

Letras comunes:
  pelo:  o contorno · h medio · H brillo
  piel:  O contorno · S sombra · s base · l luz · e ojo · m boca
  ropa:  n contorno · d sombra · b base · B luz · L acento (cremallera, botones)
  otros: w/W botas · g gafas o guantes · r brazalete · a/A delantal · c/v/t/p camisa, chaleco, corbata, pantalón
         k/K/j pañuelo · f/F/x sombrero · y barba
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402


def espejo(mitades):
    return [m + m[::-1] for m in mitades]


# ------------------------------------------------------------------ caras (filas 7-17)
CARA = [
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
]
CARA_FINA = [  # rasgos más suaves (versión femenina, Julia, Brooke…)
    "..ohhsssss",
    "..ohsoosss",
    "..ohseesss",
    "..ohseesss",
    "..ohssssss",
    "..ohsllsss",
    "..ohssssSs",
    "..ohSsssmm",
    "..ohhSssss",
    "...ohhOSSS",
    "....oohOSS",
]

# ------------------------------------------------------------------ cabezas (18 filas)
CABEZAS = {
    "corto": [
        "......oooo", ".....ohhhh", "....ohhhHH", "...ohhhHHh", "...ohhHhhh", "...ohhhhhh", "...ohhsshh",
    ] + CARA,
    "melena": [
        "......oooo", ".....ohhhh", "....ohhhHH", "...ohhhHHh", "..ohhhHhhh", "..ohhhhhhh", "..ohhhsshh",
    ] + CARA_FINA,
    "despeinado": [
        "....o..ooo", "...ohoohhh", "...ohhhhHH", "..ohhhHHhh", "..ohhhhhhh", "...ohhhhhh", "...ohhsshh",
    ] + CARA,
    "repeinado": [
        "......oooo", ".....ohhhh", "....ohhHHH", "...ohhhhhh", "...ohhhhhh", "...ohhhhhh", "...Ohsssss",
    ] + ["...Osssss s".replace(" ", "")] + CARA[1:],
    "mono": [  # moño tirante
        ".......ooo", "......ohhH", ".....oohhh", "...oohhhhh", "...ohhhhhh", "...ohhhHhh", "...ohhssss",
    ] + CARA,
    "panuelo": [
        "......kkkk", "....kkKKKK", "...kKKjKKK", "..kKKKKKKj", "..kKjKKKKK", "..kKKKKKjK", "..kKKKKKKK",
    ] + ["..kKssssss"] + ["..k" + r[3:] for r in CARA[1:6]] + CARA[6:],
    "sombrero": [
        "......ffff", ".....fFFFF", "....fFFFFF", "...fFFFFFF", "...ffxxxxx", ".fffffffff", "...ohhssss",
    ] + CARA,
    "gorra": [  # guardias y Policía del Pensamiento
        "......ffff", ".....fFFFF", "....fFFFFF", "...fFFFFFF", "...fxxxxxx", "..ffffffff", "...ohhssss",
    ] + CARA,
    "nino": None,  # los niños usan su propia plantilla
    "cofia": [  # enfermera del Minimor: cofia almidonada sobre el pelo recogido
        ".......fff", ".....fFFFF", "....fFFFFF", "...fFFFFFF", "...fxxxxxx", "...ohhhhhh", "...ohhssss",
    ] + CARA,
    "canoso": [  # anciano: pelo blanco, corto y ralo, entradas en las sienes
        "..........", "......oooo", "....oohhhh", "...ohhhHHh", "...ohhHhhh", "...ohhhhhh", "...Ohhssss",
    ] + ["...Osssss s".replace(" ", "")] + CARA[1:],
}

# ------------------------------------------------------------------ cuerpos (22 filas)
CUERPOS = {
    "mono": [
        "....nndbbL", "...ndbbbbL", "..ndbbbbbL", ".ndbbbbbbL", ".ndbBBbbbL", ".ndbBBbbbL", ".ndbbbbbbL",
        ".ndbnbbbbL", ".ndbnbbbbL", ".nddnbbbbL", ".nssnbbbbL", ".nssnddddd", "..nndbbbbL", "...ndbbbbn",
        "...ndbbbbn", "...ndbbbbn", "...ndbbbbn", "...ndbbbbn", "...ndbbbbn", "...nwWwwwn", "...nwwwwwn",
        "...nnnnnn.",
    ],
    "abrigo": [
        "....nnddbb", "...ndbbbbL", "..ndbbbbbL", ".ndbbbbbbL", ".ndbbbbbbL", ".ndbbbbbbB", ".ndbnbbbbL",
        ".ndbnbbbbL", ".ndbnbbbbB", ".ndbnbbbbL", ".nddnbbbbL", ".nggnbbbbL", ".nggnbbbbB", "..nnbbbbbL",
        "..ndbbbbbL", "..ndbbbbbL", "..ndbbbbbL", "..nnnnnnnn", "....nppn..", "....nppn..", "....nwWn..",
        "....nnnn..",
    ],
    "vestido": [
        "....nndbbb", "...ndbbbbb", "..ndbbbbbb", ".ndbbaaaaa", ".ndbbaAaaa", ".ndbbaaaaa", ".ndnbaaaaa",
        ".nSnbaaaaa", ".nsnbaaaaa", ".nssndaaaa", ".nssndaaaa", "..ndbaaaaa", "..ndbaaaaa", ".ndbbaaaaa",
        ".ndbbaaaaa", ".ndbbbaaaa", ".ndbbbbbbb", ".nnnnnnnnn", "....OssO..", "....OssO..", "....nwwn..",
        "....nnnn..",
    ],
    "chaleco": [
        "....nccccc", "...ncvvcct", "..ncvvvvct", ".nccvvvvvt", ".nccvvvvvt", ".nccvvvVvt", ".nccvvvvvt",
        ".ncnvvvvvt", ".ncnvvvvvL", ".ncnvvvvvL", ".nssnvvvvv", ".nssnddddd", "..nndppppp", "...ndpppn.",
        "...ndpppn.", "...ndpppn.", "...ndpppn.", "...ndpppn.", "...ndpppn.", "...nwWwwn.", "...nwwwwn.",
        "...nnnnnn.",
    ],
}
# variantes de cuerpo derivadas de las existentes
CUERPOS["mono_bajo"] = CUERPOS["mono"][:13] + CUERPOS["mono"][15:]   # dos filas menos de pierna (20 filas)
CUERPOS["uniforme"] = [  # Policía del Pensamiento: guerrera de hombros rectos, cinturón y botas altas
    "..nnnnnddL", ".nbBbbbbdL", ".ndbbbbbbL", ".ndbbbbbbd", ".ndbBbbbbL", ".ndbbbbbbd", ".ndbnbbbbL",
    ".ndbnbbbbd", ".ndbnbbbbL", ".ndbnbbbbd", ".nssnzzzzz", ".nssnzzzzZ", "..nndbbbbb", "...ndbbbbn",
    "...ndbbbbn", "...ndbbbbn", "...nwWwwwn", "...nwWwwwn", "...nwWwwwn", "...nwWwwwn", "...nwwwwwn",
    "...nnnnnn.",
]

NINO = espejo([
    "....cccc", "...cCCCC", "..cCCCCC", "..cCCCCC", ".ccccccc", "..ohssss", "..Osssss", "..Ossess",
    "..Ossess", ".OSslSss", "..Osssmm", "...OSsss", "....OOSS", "...nddbg", "..ndbbbb", ".ndbbbbb",
    ".ndbbbbb", ".nssbbbb", ".nssdddd", "..nppppp", "..nppppp", "...OssO.", "...OssO.", "...OssO.",
    "...nwwn.", "..nwwwn.", "..nnnnn.",
])


NINA = [r[:] for r in NINO]
NINA[0:5] = [x + x[::-1] for x in ["....oooo", "...ohhhh", "..ohhHhh", "..ohhhhh", ".oohhhhh"]]
NINA[13] = "...nrrrrrrrrn..."            # pañuelo rojo de los Espías
NINA = [list(r) for r in NINA]
for _r in range(6, 13):                    # trenzas
    NINA[_r][1] = "h"; NINA[_r][14] = "h"
NINA[13][1] = "o"; NINA[13][14] = "o"
NINA = ["".join(r) for r in NINA]
NINO_ESPIA = NINO[:13] + ["...nrrrrrrrrn..."] + NINO[14:]


def construir(cabeza, cuerpo, parches=()):
    filas = espejo(CABEZAS[cabeza] + CUERPOS[cuerpo])
    filas = [list(f) for f in filas]
    for (r, c, ch) in parches:
        filas[r][c] = ch
    return ["".join(f) for f in filas]


def rampa_ropa(rampa, base=2):
    return {"n": K(rampa, base - 2), "d": K(rampa, base - 1), "b": K(rampa, base),
            "B": K(rampa, base + 1), "L": K(rampa, base + 2)}


PIEL = lambda tono=0: {"O": K("piel", 1 + tono), "S": K("piel", 2 + tono), "s": K("piel", 3 + tono),
                       "l": K("piel", 4 + tono), "e": K("gris", 1), "m": K("piel", 1 + tono)}
PELO = lambda rampa, i=0: {"o": K(rampa, i), "h": K(rampa, i + 1), "H": K(rampa, i + 3)}
BOTAS = {"w": K("gris", 2), "W": K("gris", 4)}

# gafas redondas (filas 8-11): montura fina, cristal claro y los ojos visibles
GAFAS = ([(r, c, "g") for r in (8, 11) for c in (4, 5, 6, 7, 8, 11, 12, 13, 14, 15)]
         + [(r, c, "g") for r in (9, 10) for c in (4, 8, 11, 15)]
         + [(9, 9, "g"), (9, 10, "g")]
         + [(r, c, "G") for r in (9, 10) for c in (5, 7, 12, 14)])
PERILLA = [(r, c, "y") for r in (14, 15, 16) for c in (8, 9, 10, 11)] + [(17, 9, "y"), (17, 10, "y")]
BRAZALETE = [(21, c, "r") for c in (1, 2, 3)] + [(22, c, "r") for c in (1, 2, 3)]
SONRISA = [(14, 7, "m"), (14, 12, "m"), (13, 8, "s"), (13, 11, "s")]
# gafas de culo de botella con ojos saltones (Syme): el blanco del ojo asoma alrededor de la pupila
GAFAS_GRANDES = ([(r, c, "g") for r in (8, 12) for c in (4, 5, 6, 7, 8, 11, 12, 13, 14, 15)]
                 + [(r, c, "g") for r in (9, 10, 11) for c in (4, 8, 11, 15)]
                 + [(9, 9, "g"), (9, 10, "g")]
                 + [(r, c, "q") for r in (9, 10, 11) for c in (5, 6, 7, 12, 13, 14)]
                 + [(r, c, "e") for r in (10, 11) for c in (6, 13)]
                 + [(9, 5, "G"), (9, 12, "G")])
CEJAS_NEGRAS = [(8, c, "y") for c in (4, 5, 6, 7, 12, 13, 14, 15)]          # pobladas y aún negras
GUANTES = [(r, c, "g") for r in (28, 29) for c in (2, 3, 16, 17)]              # guantes sobre las manos del cuerpo

ELENCO = [
    # nombre, filas, paleta
    ("PROT. H", construir("corto", "mono"),
     {**PELO("pelo"), **PIEL(), **rampa_ropa("azul"), **BOTAS}),
    ("PROT. M", construir("melena", "mono"),
     {**PELO("madera", 1), **PIEL(), **rampa_ropa("azul"), **BOTAS}),
    ("AMORY", construir("despeinado", "mono", GAFAS),
     {**PELO("ocre", 0), **PIEL(1), **rampa_ropa("azul"), **BOTAS, "g": K("gris", 3), "G": K("cielo", 6)}),
    ("WINSTON", construir("corto", "mono"),
     {**PELO("madera", 1), **PIEL(1), **rampa_ropa("azul"), **BOTAS}),
    ("HILDA", construir("mono", "mono", BRAZALETE),
     {**PELO("pelo"), **PIEL(1), **rampa_ropa("azul"), **BOTAS, "r": K("rojo", 4)}),
    ("VOSS", construir("repeinado", "abrigo"),
     {**PELO("gris", 0), "H": K("gris", 4), **PIEL(1), **rampa_ropa("gris", 2), **BOTAS,
      "g": K("gris", 0), "p": K("gris", 1)}),
    ("NELL", construir("panuelo", "vestido"),
     {**PIEL(-1), **rampa_ropa("madera", 3), **BOTAS, "k": K("tela", 0), "K": K("tela", 2),
      "j": K("tela", 1), "a": K("papel", 1), "A": K("papel", 2)}),
    ("DOT", construir("panuelo", "vestido"),
     {**PIEL(0), **rampa_ropa("pared", 3), **BOTAS, "k": K("granate", 1), "K": K("granate", 4),
      "j": K("papel", 3), "a": K("papel", 3), "A": K("papel", 4)}),
    ("SAMMY", NINO,
     {**PIEL(0), "c": K("tela", 0), "C": K("tela", 2), "n": K("ocre", 0), "d": K("ocre", 1),
      "b": K("ocre", 2), "p": K("madera", 2), "g": K("gris", 7), **BOTAS}),
    ("CRANE", construir("sombrero", "chaleco", SONRISA),
     {**PELO("gris", 4), **PIEL(0), "n": K("granate", 0), "d": K("granate", 2), "v": K("granate", 4),
      "V": K("granate", 2), "c": K("papel", 3), "t": K("granate", 1), "L": K("ocre", 3),
      "p": K("tela", 2), "f": K("madera", 0), "F": K("madera", 2), "x": K("gris", 1), **BOTAS}),
    ("GOLDSTEIN", construir("despeinado", "abrigo", GAFAS + PERILLA),
     {**PELO("papel", 1), **PIEL(1), **rampa_ropa("madera", 2), **BOTAS,
      "g": K("gris", 4), "G": K("cielo", 6), "y": K("papel", 4), "p": K("madera", 1)}),
]


def dibujar(cv, x, y, filas, paleta, sombra):
    h, w = len(filas), len(filas[0])
    cv.ellipse(x + 2, y + h - 5, x + w - 2, y + h + 3, sombra)
    cv.grid(x, y, filas, paleta)


if __name__ == "__main__":
    COLS, CW, RH = 6, 44, 64
    cv = Canvas(COLS * CW + 8, 2 * RH + 8, bg=("pared", 3))
    for i, (nombre, filas, pal) in enumerate(ELENCO):
        col, fila = i % COLS, i // COLS
        x0, y0 = 4 + col * CW, 6 + fila * RH
        h = len(filas)
        dibujar(cv, x0 + (CW - len(filas[0])) // 2, y0 + 40 - h, filas, pal, K("pared", 1))
        cv.text(x0 + (CW - cv.text_width(nombre)) // 2, y0 + 50, nombre, K("papel", 4))
    prev = cv.save(Path(__file__).parent / "elenco.png", preview_scale=5)
    print("ok", prev)
