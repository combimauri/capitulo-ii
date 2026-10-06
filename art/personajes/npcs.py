"""Personajes no jugables del corte vertical (vista frontal, 20x40; niño 16x27 centrado en 20x40)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image  # noqa: E402
from pixel import K  # noqa: E402
import elenco as E  # noqa: E402

PIEL, PELO, BOTAS, ropa = E.PIEL, E.PELO, E.BOTAS, E.rampa_ropa


def _por_nombre(nombre):
    return next((f, p) for n, f, p in E.ELENCO if n == nombre)


NPCS = {
    "winston": _por_nombre("WINSTON"),
    "hilda": _por_nombre("HILDA"),
    "amory": _por_nombre("AMORY"),
    "voss": _por_nombre("VOSS"),
    "nell": _por_nombre("NELL"),
    "nino": _por_nombre("SAMMY"),
    "guardia": (E.construir("gorra", "abrigo"),
                {**PELO("pelo"), **PIEL(0), **ropa("gris", 2), **BOTAS, "g": K("gris", 0), "p": K("gris", 1),
                 "f": K("gris", 0), "F": K("gris", 2), "x": K("rojo", 3)}),
    "funcionario1": (E.construir("corto", "mono"), {**PELO("pelo", 0), **PIEL(0), **ropa("azul"), **BOTAS}),
    "funcionario2": (E.construir("repeinado", "mono"), {**PELO("gris", 3), "H": K("gris", 6), **PIEL(1), **ropa("azul"), **BOTAS}),
    "funcionaria1": (E.construir("mono", "mono"), {**PELO("madera", 0), **PIEL(1), **ropa("azul"), **BOTAS}),
    "funcionaria2": (E.construir("melena", "mono"), {**PELO("ocre", 0), **PIEL(0), **ropa("azul"), **BOTAS}),
    "prole1": (E.construir("panuelo", "vestido"), {**PIEL(0), **ropa("granate", 3), **BOTAS, "k": K("tela", 0),
               "K": K("ocre", 2), "j": K("ocre", 1), "a": K("papel", 2), "A": K("papel", 3)}),
    "prole2": (E.construir("despeinado", "chaleco"), {**PELO("pelo", 0), **PIEL(-1), "n": K("madera", 0),
               "d": K("madera", 1), "v": K("madera", 3), "V": K("madera", 2), "c": K("papel", 2), "t": K("madera", 0),
               "L": K("gris", 5), "p": K("tela", 1), **BOTAS}),
    "oficial": (E.construir("repeinado", "abrigo"), {**PELO("gris", 0), "H": K("gris", 2), **PIEL(-1), **ropa("gris", 2),
                **BOTAS, "g": K("gris", 0), "p": K("gris", 1)}),
    "julia": (E.construir("melena", "mono", [(19 + k, 4 + k, "r") for k in range(11)] + [(19 + k, 5 + k, "r") for k in range(11)]),
              {**PELO("pelo", 0), **PIEL(0), **ropa("azul"), **BOTAS, "r": K("rojo", 4)}),
    "pell": (E.construir("corto", "mono"), {**PELO("gris", 2), "H": K("gris", 4), **PIEL(1), **ropa("azul", 1), **BOTAS}),
    "brooke": (E.construir("mono", "mono", E.GAFAS), {**PELO("gris", 4), "H": K("gris", 6), **PIEL(1), **ropa("azul"), **BOTAS,
               "g": K("gris", 1), "G": K("cielo", 6)}),
    "obrien": (E.construir("repeinado", "abrigo", E.GAFAS), {**PELO("gris", 1), "H": K("gris", 4), **PIEL(1), **ropa("gris", 2),
               **BOTAS, "g": K("gris", 0), "G": K("cielo", 6), "p": K("gris", 1)}),
    "parsons": (E.construir("corto", "mono"), {**PELO("ocre", 0), **PIEL(1), **ropa("azul"), **BOTAS}),
    "hija_parsons": (E.NINA, {**PELO("pelo", 1), **PIEL(1), "n": K("azul", 0), "d": K("azul", 1), "b": K("azul", 2),
                     "p": K("azul", 1), "r": K("rojo", 4), **BOTAS}),
    "nino_parsons": (E.NINO_ESPIA, {**PIEL(1), "c": K("azul", 0), "C": K("azul", 2), "n": K("azul", 0), "d": K("azul", 1),
                     "b": K("azul", 2), "p": K("azul", 1), "r": K("rojo", 4), "g": K("rojo", 4), **BOTAS}),
    "ivy_nina": (E.NINA, {"o": K("madera", 0), "h": K("madera", 2), "H": K("madera", 4), "O": K("papel", 0), "S": K("papel", 1),
                 "s": K("papel", 2), "l": K("papel", 3), "e": K("madera", 0), "m": K("madera", 1), "n": K("madera", 1),
                 "d": K("madera", 2), "b": K("papel", 2), "p": K("madera", 3), "r": K("papel", 3), "w": K("madera", 1), "W": K("madera", 2)}),
}


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    for nombre, (filas, pal) in NPCS.items():
        img = Image.new("RGBA", (20, 40), (0, 0, 0, 0))
        dx, dy = (20 - len(filas[0])) // 2, 40 - len(filas)
        for r, fila in enumerate(filas):
            for c, ch in enumerate(fila):
                if ch in pal:
                    img.putpixel((dx + c, dy + r), pal[ch] + (255,))
        img.save(destino / f"{nombre}.png")
    return list(NPCS)
