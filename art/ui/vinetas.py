"""Viñetas fijas de los montajes de los finales (480x270, el juego las dibuja a 2x).

plaza:    la Semana del Odio. La plaza llena, banderas, la tribuna y el Gran Hermano en una pantalla gigante.
patibulo: el Parque de la Victoria. El patíbulo con dos cuerdas; abajo, la multitud.
patibulo5: el mismo parque, una mañana gris: cinco cuerdas, cinco figuras (los prisioneros "estasiáticos").
foto_sotano / foto_iniciacion (160x110): las dos fotos de Crane, tomadas por el hueco de la pared del sótano
de La Campana. La primera en sepia (Ivy, Nell y Barlow, 1979); la segunda, reciente y en blanco y negro.
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import LOOKUP, Canvas, K  # noqa: E402
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


def patibulo5():
    rnd = random.Random(11)
    cv = Canvas(W, H, bg=("cielo", 3))
    for i, y in enumerate(range(0, 140, 20)):                         # mañana gris, cielo bajo y plano
        cv.rect(0, y, W, y + 20, K("cielo", 3 - (i % 2)))
    cv.rect(0, 120, W, 168, K("cielo", 4))                            # niebla baja sobre el parque
    for tx in (24, 70, 412, 458):
        cv.vline(tx, 50, 152, K("madera", 0)); cv.d.line([(tx, 78), (tx - 13, 58)], fill=K("madera", 0))
        cv.d.line([(tx, 96), (tx + 15, 72)], fill=K("madera", 0))
    # el patíbulo, más ancho: un travesaño, cinco cuerdas
    cv.rect(130, 40, 350, 46, K("madera", 1)); cv.rect(136, 46, 142, 160, K("madera", 1)); cv.rect(338, 46, 344, 160, K("madera", 1))
    cv.d.line([(142, 70), (160, 46)], fill=K("madera", 1), width=3); cv.d.line([(338, 70), (320, 46)], fill=K("madera", 1), width=3)
    cv.rect(120, 150, 360, 162, K("madera", 2)); cv.hline(120, 360, 150, K("madera", 3))
    for i, cx in enumerate((172, 208, 244, 280, 316)):
        ancho = 6 if i == 2 else 5                                       # el tercero, más fornido
        caida = (0, 2, 1, 0, 3)[i]
        cv.vline(cx, 46, 74 + caida, K("papel", 1))
        cv.ellipse(cx - 5, 72 + caida, cx + 5, 82 + caida, K("gris", 2))
        cv.rect(cx - ancho, 82 + caida, cx + ancho, 112 + caida, K("gris", 1))
        cv.vline(cx - 2, 112 + caida, 126 + caida, K("gris", 1)); cv.vline(cx + 2, 112 + caida, 126 + caida, K("gris", 1))
    multitud(cv, 168, 270, rnd, filas=7)
    cv.bake_lighting()
    return cv


# ---------------------------------------------------------------- las fotos del sótano (160x110)

FW, FH = 160, 110
# rampa de sepia hecha con tonos de la paleta (de oscuro a claro): sustituye a los 11 grises
SEPIA = [K("madera", i) for i in range(7)] + [K("papel", 2), K("papel", 2), K("papel", 3), K("papel", 4)]


def _g(i):
    return K("gris", i)


def _grid(cv, cx, y, filas):
    """Dibuja una rejilla de valores (0-9, a=10) centrando cada fila en cx."""
    for r, fila in enumerate(filas):
        x0 = cx - len(fila) // 2
        for c, ch in enumerate(fila):
            if ch != ".":
                cv.px(x0 + c, y + r, _g(10 if ch == "a" else int(ch)))


NELL = ["33333333", "334434434433", "34434443443443", "3443444344434443", "3444555555554443",
        "3445666666665443", "3456336666336543", "3456616666166543", "3456666666666543", "3456666556666543",
        "3456666666666543", "3345663333665433", "33456666665433", "33345555554333", "333444444333",
        "3333443333", "33433334"]
IVY = ["22222222", "222223322222", "22222332222222", "2222266666622222", "2226666666666222",
       "2266336666336622", "2266616666166622", "2266666666666622", "2266666556666622", "2266566666656622",
       "2266622222266622", "2266629919966622", "2266662222666622", "22666666666622", "226666666622",
       "2256666522", "5555"]
BARLOW = ["1111111111", "11112111121111", "1111112111111111", "111211111111112111", "111155555555551111",
          "111566666666665111", "115622666666226511", "115661666666166511", "155666666666666551",
          "155666665566666551", "155666655556666551", "115662222222266511", "115666622226666511",
          "115666633336666511", "1556666666666551", "55666666666655", "556666666655", "5555555555"]
PROTA = ["....11111111....", "..111111111111..", ".11111111111111.", ".11111111111111.", ".661111111111111",
         ".666611111111111", ".666666111111111", ".633666611111111", ".616666661111111", "6666666666111111",
         "6666666666611111", ".566666666611111", ".666666666661111", ".366666666661111", "..66666666666111",
         "..566666666661..", "...55666666666..", "......666666...."]


def _cuerpo(cv, cx, y, ancho, tono, base=FH):
    cv.poly([(cx - ancho, base), (cx - ancho + 2, y + 4), (cx - ancho + 6, y), (cx + ancho - 6, y),
             (cx + ancho - 2, y + 4), (cx + ancho, base)], _g(tono))


def _manos(cv, *xs):
    for x in xs:                                                                                # manos sobre la mesa
        cv.rect(x, 80, x + 5, 84, _g(5)); cv.hline(x + 1, x + 4, 80, _g(6)); cv.vline(x + 2, 81, 84, _g(4))


def _nell(cv, cx):
    _cuerpo(cv, cx, 58, 17, 2)
    cv.poly([(cx - 7, 62), (cx + 7, 62), (cx + 6, FH), (cx - 6, FH)], _g(4))                     # delantal
    cv.poly([(cx - 9, 50), (cx - 13, 62), (cx - 7, 58)], _g(3))                                 # nudo del pañuelo
    _grid(cv, cx, 36, NELL)
    _manos(cv, cx - 4, cx + 1)


def _ivy(cv, cx):
    _cuerpo(cv, cx, 56, 16, 6)                                                                  # blusa clara
    cv.vline(cx, 60, FH, _g(5)); cv.px(cx, 66, _g(3)); cv.px(cx, 73, _g(3))
    cv.poly([(cx - 5, 56), (cx + 5, 56), (cx, 62)], _g(4))                                      # escote
    cv.ellipse(cx - 9, 35, cx + 9, 53, _g(2))                                                   # melena recogida
    _grid(cv, cx, 37, IVY)
    for lado in (-1, 1):                                                                       # trenzas
        x = cx + lado * 7 - (1 if lado > 0 else 0)
        for k, yy in enumerate(range(49, 70, 3)):
            cv.rect(x - 1, yy, x + 2, yy + 3, _g(2 if k % 2 else 3)); cv.px(x, yy + 1, _g(1))
        cv.rect(x - 1, 70, x + 2, 72, _g(7))                                                    # lazo


def _barlow(cv, cx):
    _cuerpo(cv, cx, 55, 22, 7)                                                                  # camisa
    cv.poly([(cx - 20, 60), (cx - 8, 58), (cx - 4, FH), (cx - 22, FH)], _g(3))                  # chaleco
    cv.poly([(cx + 20, 60), (cx + 8, 58), (cx + 4, FH), (cx + 22, FH)], _g(3))
    cv.rect(cx - 1, 55, cx + 1, 76, _g(2))                                                      # corbata
    _grid(cv, cx, 36, BARLOW)
    _manos(cv, cx - 16, cx + 11)


def _protagonista_perfil(cv, cx):
    """De perfil, mirando a Nell (a la izquierda). Mono del Partido; nada fija su género."""
    _cuerpo(cv, cx + 2, 57, 15, 4)
    cv.poly([(cx - 9, 57), (cx, 57), (cx - 3, 64)], _g(5))                                      # cuello del mono
    cv.vline(cx - 3, 64, FH, _g(5)); cv.rect(cx + 7, 66, cx + 12, 72, _g(3))                    # cremallera, bolsillo
    _grid(cv, cx, 38, PROTA)


def _sotano(cv, figuras, vela_x=86):
    rnd = random.Random(vela_x)

    def ruido(d):
        return d + rnd.gauss(0, 2.5)                                                              # bordes de luz sin anillos duros

    # fondo: ladrillo y bóveda (el ángulo bajo deja ver las vigas del techo), apenas tocados por la vela
    cv.rect(0, 0, FW, FH, _g(1))
    for y in range(26, 84, 5):
        cv.hline(0, FW, y, _g(0))
        for x in range((y // 5 % 2) * 6, FW, 12):
            cv.vline(x, y, y + 5, _g(0))
    cv.rect(0, 0, FW, 24, _g(0))
    for x0, x1 in ((-4, 14), (38, 54), (104, 120), (148, 166)):
        cv.poly([(x0, 0), (x1, 0), (x1 - (x1 - 80) // 5, 24), (x0 - (x0 - 80) // 5, 24)], _g(1))
    cv.rect(0, 24, FW, 26, _g(2))
    cv.rect(140, 50, 160, 84, _g(2)); cv.hline(140, 160, 57, _g(0)); cv.hline(140, 160, 74, _g(0))   # barril
    cv.add_light_fn(lambda x, y: 2 if ruido(((x - vela_x) ** 2 + ((y - 64) * 1.4) ** 2) ** 0.5) < 34
                    else 1 if ruido(((x - vela_x) ** 2 + ((y - 64) * 1.4) ** 2) ** 0.5) < 70 else 0)
    cv.bake_lighting()
    # figuras en una capa aparte: se iluminan más y se recortan contra la pared con un perfil oscuro
    capa = Canvas(FW, FH, bg=("rojo", 0))
    for nombre, cx in figuras:
        {"nell": _nell, "ivy": _ivy, "barlow": _barlow, "prota": _protagonista_perfil}[nombre](capa, cx)
    mascara = [[capa.img.getpixel((x, y)) != K("rojo", 0) for x in range(FW)] for y in range(FH)]
    capa.add_light_fn(lambda x, y: 2 if ruido(((x - vela_x) ** 2 + ((y - 64) * 1.4) ** 2) ** 0.5) < 32
                      else 1 if ruido(((x - vela_x) ** 2 + ((y - 64) * 1.4) ** 2) ** 0.5) < 64 else 0)
    capa.bake_lighting()
    for y in range(FH):
        for x in range(FW):
            if mascara[y][x]:
                cv.px(x, y, capa.img.getpixel((x, y)))
            elif y < 84 and any(0 <= x + dx < FW and 0 <= y + dy < FH and mascara[y + dy][x + dx]
                                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                cv.px(x, y, _g(0))
    # el canto de la mesa, a la altura de la cámara, y la vela encima
    cv.rect(0, 84, FW, 89, _g(5)); cv.hline(0, FW, 84, _g(7)); cv.rect(0, 89, FW, FH, _g(1))
    cv.rect(vela_x - 2, 68, vela_x + 2, 84, _g(9)); cv.vline(vela_x + 1, 68, 84, _g(8))
    cv.poly([(vela_x - 5, 84), (vela_x + 5, 84), (vela_x + 4, 81), (vela_x - 4, 81)], _g(7))   # platillo
    cv.ellipse(vela_x - 2, 59, vela_x + 3, 68, _g(10)); cv.px(vela_x, 67, _g(2))


def _hueco(cv):
    """Ladrillos sueltos del hueco tapando las esquinas: la foto está hecha a escondidas."""
    for (x, y, w) in ((0, 0, 30), (0, 6, 18), (0, 12, 10), (FW - 22, 0, 22), (FW - 12, 6, 12),
                      (0, FH - 26, 8), (0, FH - 20, 16), (0, FH - 14, 26), (FW - 34, FH - 14, 34),
                      (FW - 18, FH - 20, 18), (FW - 8, FH - 26, 8)):
        cv.rect(x, y, x + w, y + 6, _g(0))
        cv.hline(x, x + w, y + (5 if y < FH // 2 else 0), _g(1))


def _foto(figuras, sepia):
    rnd = random.Random(1979 if sepia else 1984)
    cv = Canvas(FW, FH, bg=("gris", 0))
    _sotano(cv, figuras)
    _hueco(cv)
    for _ in range(420 if sepia else 200):                                                  # grano
        x, y = rnd.randrange(FW), rnd.randrange(FH)
        r, i = LOOKUP.get(cv.img.getpixel((x, y)), ("gris", 0))
        if r == "gris":
            cv.px(x, y, _g(max(0, min(10, i + rnd.choice((-1, 1))))))
    if sepia:                                                                               # a sepia, y envejecida
        px = cv.img.load()
        for y in range(FH):
            for x in range(FW):
                r, i = LOOKUP.get(px[x, y], ("gris", 0))
                fade = 1 if (FW - x) + (FH - y) * 1.3 < 46 or x + y < 22 else 0                # esquinas desvaídas
                px[x, y] = SEPIA[min(10, i + fade)] if r == "gris" else px[x, y]
        for _ in range(14):
            cv.px(rnd.randrange(8, FW - 8), rnd.randrange(8, FH - 12), K("papel", 3))        # motas
    borde = K("papel", 3) if sepia else K("gris", 10)
    for (x0, y0, x1, y1) in ((0, 0, FW, 6), (0, FH - 10, FW, FH), (0, 0, 6, FH), (FW - 6, 0, FW, FH)):
        cv.rect(x0, y0, x1, y1, borde)
    cv.frame(0, 0, FW, FH, K("papel", 1) if sepia else K("gris", 7))
    if sepia:
        cv.d.line([(0, 18), (5, 22)], fill=K("papel", 1)); cv.px(FW - 2, FH - 3, K("papel", 1))   # esquinas gastadas
    return cv


def foto_sotano():
    return _foto([("nell", 34), ("ivy", 61), ("barlow", 120)], sepia=True)


def foto_iniciacion():
    return _foto([("nell", 34), ("prota", 61), ("barlow", 120)], sepia=False)


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    plaza().img.save(destino / "plaza.png")
    plaza().img.convert("L").convert("RGB").save(destino / "plaza_gris.png")      # FA.04: hasta el rojo se vuelve gris
    patibulo().img.save(destino / "patibulo.png")
    patibulo5().img.save(destino / "patibulo5.png")
    foto_sotano().img.save(destino / "foto_sotano.png")
    foto_iniciacion().img.save(destino / "foto_iniciacion.png")
    return ["plaza", "patibulo", "patibulo5", "foto_sotano", "foto_iniciacion"]
