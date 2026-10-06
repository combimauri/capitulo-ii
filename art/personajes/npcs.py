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
    "dot": _por_nombre("DOT"),
    "crane": _por_nombre("CRANE"),
    "viejo": (E.construir("corto", "chaleco"), {**PELO("papel", 1), "H": K("papel", 3), **PIEL(0), "n": K("madera", 0),
              "d": K("madera", 1), "v": K("tela", 2), "V": K("tela", 1), "c": K("papel", 2), "t": K("madera", 0),
              "L": K("gris", 5), "p": K("tela", 1), **BOTAS}),
    "tabernero": (E.construir("despeinado", "chaleco"), {**PELO("pelo", 1), **PIEL(1), "n": K("granate", 0),
                  "d": K("granate", 1), "v": K("papel", 3), "V": K("papel", 2), "c": K("papel", 4), "t": K("granate", 1),
                  "L": K("gris", 5), "p": K("madera", 1), **BOTAS}),
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
    # --- Acto III -----------------------------------------------------------------------------
    "syme": (E.construir("corto", "mono_bajo", E.GAFAS_GRANDES),
             {**PELO("pelo", 0), "H": K("pelo", 2), **PIEL(0), **ropa("azul"), **BOTAS,
              "g": K("gris", 1), "G": K("cielo", 6), "q": K("papel", 4), "e": K("gris", 0)}),
    "charrington": (E.construir("canoso", "uniforme", E.CEJAS_NEGRAS),
                    {"o": K("gris", 6), "h": K("gris", 9), "H": K("gris", 10), **PIEL(0), **ropa("gris", 2), **BOTAS,
                     "y": K("pelo", 0), "z": K("gris", 0), "Z": K("gris", 6), "w": K("gris", 0), "W": K("gris", 3)}),
    "agente": (E.construir("gorra", "abrigo", [(7, c, "S") for c in range(4, 16)] + [(r, c, "n") for r in (16, 17)
                                                                                   for c in (5, 6, 13, 14)]),
               {**PELO("gris", 0), **PIEL(0), **ropa("gris", 2), **BOTAS, "g": K("gris", 0), "p": K("gris", 1),
                "f": K("gris", 0), "F": K("gris", 1), "x": K("gris", 0), "n": K("gris", 0)}),
    "funcionaria_minimor": (E.construir("cofia", "vestido"),
                            {**PELO("gris", 3), "H": K("gris", 5), **PIEL(1), "n": K("gris", 7), "d": K("gris", 8),
                             "b": K("gris", 10), "B": K("gris", 10), "L": K("gris", 9), "a": K("gris", 10),
                             "A": K("papel", 4), "f": K("gris", 7), "F": K("gris", 10), "x": K("gris", 9),
                             "w": K("gris", 8), "W": K("gris", 10)}),
    "supervisor": (E.construir("repeinado", "mono", E.BRAZALETE),
                   {**PELO("gris", 5), "H": K("gris", 8), **PIEL(0), **ropa("azul"), **BOTAS, "r": K("rojo", 4)}),
    "voss_camisa": (E.construir("repeinado", "chaleco", E.GUANTES),
                    {**PELO("gris", 0), "H": K("gris", 4), **PIEL(1), "n": K("gris", 5), "d": K("gris", 3),
                     "c": K("papel", 4), "v": K("papel", 4), "V": K("papel", 3), "t": K("gris", 1), "L": K("papel", 2),
                     "p": K("gris", 4), "g": K("gris", 0), **BOTAS}),
}


def tripode():
    """La cámara de fuelle de Crane sobre su trípode (no es un personaje: se dibuja aparte)."""
    from PIL import ImageDraw
    img = Image.new("RGBA", (20, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for (x0, x1) in [(10, 3), (10, 17), (10, 10)]:
        d.line([(x0, 20), (x1, 39)], fill=K("madera", 2) + (255,))
    d.rectangle([4, 9, 13, 19], fill=K("gris", 1) + (255,))                               # caja
    d.rectangle([13, 11, 17, 17], fill=K("madera", 1) + (255,))                           # fuelle
    d.line([(14, 11), (14, 17)], fill=K("madera", 3) + (255,)); d.line([(16, 11), (16, 17)], fill=K("madera", 3) + (255,))
    d.ellipse([16, 12, 19, 16], fill=K("gris", 6) + (255,))                               # objetivo
    d.rectangle([2, 6, 7, 9], fill=K("gris", 2) + (255,))                                 # paño negro
    return img


def carrito():
    """El carrito de la limpieza de Nell, para bloquear una puerta (no es un personaje)."""
    from PIL import ImageDraw
    img = Image.new("RGBA", (20, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rgba = lambda c: c + (255,)
    d.rectangle([1, 24, 18, 26], fill=rgba(K("gris", 6))); d.rectangle([1, 34, 18, 36], fill=rgba(K("gris", 5)))
    d.line([(1, 24), (1, 38)], fill=rgba(K("gris", 4))); d.line([(18, 24), (18, 38)], fill=rgba(K("gris", 4)))
    d.rectangle([10, 27, 17, 33], fill=rgba(K("gris", 5))); d.rectangle([10, 27, 17, 28], fill=rgba(K("cielo", 3)))
    d.rectangle([2, 18, 9, 24], fill=rgba(K("tela", 3))); d.line([(14, 8), (14, 27)], fill=rgba(K("madera", 3)))
    d.point([(3, 38), (16, 38)], fill=rgba(K("gris", 1)))
    return img


def carrito_volcado():
    """El carrito de Nell volcado en el pasillo: el cubo caído y un charco de lejía que nadie recoge."""
    from PIL import ImageDraw
    img = Image.new("RGBA", (20, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rgba = lambda c: c + (255,)
    d.ellipse([5, 31, 19, 39], fill=rgba(K("cielo", 5)))                                   # charco de lejía
    d.ellipse([8, 32, 18, 38], fill=rgba(K("cielo", 6)))
    d.point([(12, 34), (13, 34), (15, 36)], fill=rgba(K("papel", 4)))                       # reflejos
    # el carrito de costado (el mismo de carrito(), girado): estantes en vertical, ruedas al aire a la izquierda
    d.rectangle([1, 20, 14, 21], fill=rgba(K("gris", 4))); d.rectangle([1, 35, 14, 36], fill=rgba(K("gris", 3)))
    d.rectangle([3, 20, 5, 36], fill=rgba(K("gris", 5))); d.rectangle([12, 20, 14, 36], fill=rgba(K("gris", 6)))
    d.line([(12, 20), (12, 36)], fill=rgba(K("gris", 7)))
    for y in (20, 34):                                                                       # ruedas
        d.rectangle([0, y, 1, y + 2], fill=rgba(K("gris", 1)))
    d.rectangle([6, 29, 11, 35], fill=rgba(K("tela", 3))); d.line([(6, 29), (11, 29)], fill=rgba(K("tela", 4)))  # saco de trapos
    d.point([(7, 31), (9, 33)], fill=rgba(K("tela", 1)))
    d.polygon([(15, 22), (19, 23), (18, 27), (15, 26)], fill=rgba(K("papel", 2)))           # un trapo, fuera
    # el cubo, tumbado, con la boca hacia el charco
    d.polygon([(13, 27), (18, 28), (18, 34), (13, 33)], fill=rgba(K("gris", 5)))
    d.line([(13, 27), (18, 28)], fill=rgba(K("gris", 8))); d.line([(13, 27), (13, 33)], fill=rgba(K("gris", 3)))
    d.ellipse([17, 27, 19, 35], fill=rgba(K("gris", 2))); d.line([(18, 29), (18, 33)], fill=rgba(K("gris", 0)))
    return img


def sabana():
    """Sábana tendida en una cuerda (se repite en horizontal): tapa a una persona de pie salvo los pies."""
    from PIL import ImageDraw
    img = Image.new("RGBA", (20, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rgba = lambda c: c + (255,)
    d.rectangle([0, 4, 19, 34], fill=rgba(K("papel", 3)))
    for x, (y1, tono) in zip((3, 7, 12, 16), ((35, 2), (36, 1), (34, 2), (35, 1))):         # pliegues verticales
        d.line([(x, 6), (x, y1)], fill=rgba(K("papel", tono)))
        d.line([(x + 1, 6), (x + 1, y1 - 2)], fill=rgba(K("papel", 4)))
    for x, y1 in ((0, 35), (5, 36), (9, 37), (14, 35), (18, 36)):                         # bajo ondulado y húmedo
        d.line([(x, 34), (x, y1)], fill=rgba(K("papel", 2)))
    d.line([(0, 4), (19, 4)], fill=rgba(K("papel", 4)))                                     # dobladillo
    d.line([(0, 5), (19, 5)], fill=rgba(K("papel", 2)))
    d.line([(0, 3), (19, 3)], fill=rgba(K("madera", 3)))                                    # cuerda
    for x in (2, 17):                                                                       # pinzas
        d.rectangle([x, 2, x + 1, 5], fill=rgba(K("madera", 5))); d.point([(x, 5)], fill=rgba(K("madera", 2)))
    return img


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
    tripode().save(destino / "tripode.png")
    carrito().save(destino / "carrito.png")
    carrito_volcado().save(destino / "carrito_volcado.png")
    sabana().save(destino / "sabana.png")
    return list(NPCS) + ["tripode", "carrito", "carrito_volcado", "sabana"]
