"""Retrato del protagonista para el crimen facial (96x96).

La cara se construye por capas: hombros → cuello → cabeza → orejas → sombreado → pelo
→ ojos → cejas → nariz → boca → arrugas y efectos. Cada expresión es un conjunto de
parámetros de ojos, cejas y boca.

Uso: python3 art/personajes/retrato_protagonista.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from pixel import Canvas, K  # noqa: E402

S = 96
FONDO = K("pared", 1)


# ------------------------------------------------------------------ utilidades
def mezcla(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


# ------------------------------------------------------------------ partes
def hombros(cv):
    cv.poly([(4, 96), (14, 82), (30, 75), (66, 75), (82, 82), (92, 96)], K("azul", 2))
    cv.poly([(60, 75), (66, 75), (82, 82), (92, 96), (70, 96)], K("azul", 1))      # sombra derecha
    cv.poly([(4, 96), (14, 82), (22, 78), (16, 96)], K("azul", 3))                 # luz izquierda
    # cuello del mono (solapas en V) y cremallera
    cv.poly([(36, 75), (48, 90), (40, 75)], K("azul", 3))
    cv.poly([(60, 75), (48, 90), (56, 75)], K("azul", 1))
    cv.d.line([36, 75, 48, 90], fill=K("azul", 0)); cv.d.line([60, 75, 48, 90], fill=K("azul", 0))
    cv.vline(48, 90, 96, K("azul", 4))
    cv.d.line([30, 84, 30, 96], fill=K("azul", 1)); cv.d.line([66, 84, 66, 96], fill=K("azul", 0))


def cuello(cv, tendones=False):
    cv.rect(39, 58, 58, 80, K("piel", 2))
    cv.rect(39, 58, 58, 66, K("piel", 1))                                         # sombra de la mandíbula
    cv.poly([(39, 74), (48, 88), (57, 74)], K("piel", 2))
    cv.vline(39, 60, 76, K("piel", 1)); cv.vline(57, 60, 76, K("piel", 0))
    if tendones:
        cv.d.line([43, 66, 41, 78], fill=K("piel", 1)); cv.d.line([53, 66, 55, 78], fill=K("piel", 1))
        cv.d.line([44, 66, 42, 78], fill=K("piel", 3)); cv.d.line([52, 66, 54, 78], fill=K("piel", 3))


def cabeza(cv, femenina=False):
    mandibula = ([(28, 40), (30, 54), (36, 63), (43, 68), (53, 68), (60, 63), (66, 54), (68, 40)] if femenina else
                 [(27, 40), (29, 55), (35, 64), (43, 70), (53, 70), (61, 64), (67, 55), (69, 40)])
    cv.ellipse(27, 12, 70, 58, K("piel", 3))
    cv.poly(mandibula, K("piel", 3))
    # orejas
    for x0 in (22, 66):
        cv.ellipse(x0, 38, x0 + 9, 55, K("piel", 3), outline=K("piel", 1))
        cv.d.arc([x0 + 2, 41, x0 + 7, 52], 90 if x0 > 40 else 270, 270 if x0 > 40 else 90, fill=K("piel", 1))
    # sombra lateral derecha y luz izquierda
    cv.poly([(60, 24), (68, 38), (66, 55), (60, 64), (53, 70), (57, 60), (62, 46), (61, 32)], K("piel", 2))
    cv.poly([(31, 48), (34, 45), (38, 47), (39, 51), (36, 54), (32, 53)], K("piel", 4))           # pómulo
    cv.rect(35, 31, 43, 34, K("piel", 4))                                                          # frente
    cv.px(34, 32, K("piel", 4)); cv.px(43, 32, K("piel", 3))
    cv.d.line([(29, 42), (29, 50), (31, 56)], fill=K("piel", 4))                                   # filo de luz
    # contorno selectivo
    cv.d.line(mandibula, fill=K("piel", 1))
    cv.d.line([mandibula[-3], mandibula[-2], mandibula[-1]], fill=K("piel", 0))


def pelo(cv, femenino=False):
    if femenino:
        cv.poly([(16, 92), (17, 36), (22, 18), (32, 8), (48, 5), (62, 8), (73, 17), (79, 34), (80, 92),
                 (70, 92), (69, 54), (68, 34), (62, 24), (54, 28), (44, 24), (34, 30), (30, 36), (28, 54), (26, 92)],
                K("madera", 2))
        cv.poly([(19, 88), (20, 40), (24, 22), (30, 14), (27, 30), (24, 50), (24, 88)], K("madera", 4))      # luz
        cv.poly([(74, 30), (79, 40), (79, 90), (72, 90), (71, 50)], K("madera", 1))                       # sombra
        for (a, b) in [((36, 10), (30, 26)), ((46, 8), (40, 24)), ((58, 9), (60, 22)), ((66, 14), (68, 26))]:
            cv.d.line([a, b], fill=K("madera", 3))
        cv.d.line([(44, 24), (54, 28), (62, 24)], fill=K("madera", 1))
    else:
        contorno = [(23, 46), (21, 38), (22, 28), (25, 20), (30, 14), (36, 10), (44, 7), (52, 7), (60, 9),
                    (66, 13), (71, 19), (74, 27), (75, 36), (74, 46), (70, 46), (69, 40), (68, 34), (65, 29),
                    (62, 31), (60, 25), (57, 31), (54, 26), (50, 32), (47, 26), (43, 31), (40, 27), (36, 32),
                    (33, 28), (30, 34), (29, 40), (28, 46)]
        cv.poly(contorno, K("pelo", 1))
        # sombra en el lado derecho (lejos de la ventana)
        cv.poly([(64, 16), (70, 19), (74, 27), (75, 36), (74, 46), (70, 46), (69, 38), (68, 28)], K("pelo", 0))
        # mechones con brillo, siguiendo la curva del cráneo
        for trazo in ([(27, 30), (30, 21), (36, 14), (44, 10)],
                      [(31, 27), (35, 19), (42, 14)],
                      [(46, 10), (53, 9), (60, 12)],
                      [(29, 36), (31, 28), (35, 22)]):
            cv.d.line(trazo, fill=K("pelo", 3))
        for trazo in ([(48, 12), (55, 12), (62, 15), (66, 20)], [(38, 18), (46, 15), (54, 16)]):
            cv.d.line(trazo, fill=K("pelo", 2))
        # raya al lado
        cv.d.line([(41, 8), (39, 14), (38, 20)], fill=K("pelo", 0))
        cv.d.line([(42, 9), (40, 15)], fill=K("pelo", 3))
        # separación de las puntas del flequillo
        for (a, b) in [((47, 26), (49, 19)), ((54, 26), (55, 19)), ((60, 25), (61, 18)), ((40, 27), (42, 20)),
                       ((33, 28), (35, 22))]:
            cv.d.line([a, b], fill=K("pelo", 0))
        for (x, y) in [(50, 31), (44, 30), (57, 30), (37, 31)]:
            cv.px(x, y, K("pelo", 2))
        # patillas
        cv.rect(29, 44, 31, 49, K("pelo", 1)); cv.rect(66, 44, 68, 49, K("pelo", 1))
        cv.d.line(contorno[:14], fill=K("pelo", 0))


def ojo(cv, cx, cy, lado, apertura=3, mirada=(0, 0), inclinacion=0, cerrado_feliz=False, pestanas=False):
    """lado = +1 ojo izquierdo (el interior queda hacia +x), -1 ojo derecho."""
    if cerrado_feliz:
        for x in range(-4, 5):
            y = cy + 1 - (2 - abs(x) // 2)
            cv.px(cx + x, y, K("pelo", 0)); cv.px(cx + x, y + 1, K("pelo", 0))
        return
    # sombra de la cuenca
    cv.rect(cx - 5, cy - apertura - 2, cx + 6, cy - apertura, K("piel", 2))
    tops, bots = {}, {}
    for x in range(-4, 5):
        h = apertura * (1 - (x / 5.2) ** 2)
        t = round(cy - h * 0.7 + inclinacion * (x * lado) / 4)
        b = round(cy + h * 0.45)
        tops[x], bots[x] = t, max(t, b)
        for y in range(t, max(t, b) + 1):
            cv.px(cx + x, y, K("papel", 4))
    # iris, pupila y brillo
    ix, iy = cx + mirada[0], cy + mirada[1]
    for x in range(-1, 2):
        for y in range(-1, 2):
            px_, py_ = ix + x, iy + y
            dx = px_ - cx
            if -4 <= dx <= 4 and tops[dx] <= py_ <= bots[dx]:
                cv.px(px_, py_, K("madera", 2) if (x, y) != (0, 0) else K("gris", 0))
    if tops.get(ix - cx, 99) <= iy - 1:
        cv.px(ix - 1, iy - 1, K("papel", 4))
    # párpado superior (pestañas) e inferior
    for x in range(-4, 5):
        cv.px(cx + x, tops[x] - 1, K("pelo", 0))
    cv.px(cx - 5 * lado if lado < 0 else cx + 5, tops[4 if lado > 0 else -4], K("pelo", 0))
    exterior = -4 if lado > 0 else 4
    cv.px(cx + exterior - (1 if lado > 0 else -1), tops[exterior] - 1, K("pelo", 0))
    if pestanas:
        cv.px(cx + exterior - (2 if lado > 0 else -2), tops[exterior] - 2, K("pelo", 0))
        cv.px(cx + exterior - (1 if lado > 0 else -1), tops[exterior] - 2, K("pelo", 0))
    for x in range(-3, 4):
        cv.px(cx + x, bots[x] + 1, K("piel", 2))


def ceja(cv, cx, y, lado, alza=0, inclinacion=0, color=None):
    color = color or K("pelo", 1)
    for x in range(-5, 6):
        yy = round(y - alza + inclinacion * (x * lado) / 5 - (1 if abs(x) < 3 else 0))
        cv.px(cx + x, yy, color)
        if abs(x) < 5:
            cv.px(cx + x, yy + 1, K("pelo", 0))


def nariz(cv, aletas=False):
    cv.vline(46, 42, 54, K("piel", 4))
    cv.d.line([50, 44, 52, 55], fill=K("piel", 2))
    cv.px(47, 54, K("piel", 4))
    cv.hline(44, 53, 56, K("piel", 2))
    cv.px(44, 55, K("piel", 1)); cv.px(52, 55, K("piel", 1))
    if aletas:
        cv.px(43, 55, K("piel", 1)); cv.px(53, 55, K("piel", 1)); cv.px(43, 54, K("piel", 1)); cv.px(53, 54, K("piel", 1))


def boca(cv, tipo, femenina=False):
    labio = K("granate", 4) if femenina else K("piel", 2)
    if tipo == "cerrada":
        cv.hline(42, 55, 60, K("piel", 0)); cv.px(41, 60, K("piel", 1)); cv.px(55, 60, K("piel", 1))
        cv.hline(43, 54, 59, labio); cv.hline(44, 53, 61, K("piel", 4) if not femenina else labio)
        cv.hline(45, 52, 63, K("piel", 2))
    elif tipo == "sonrisa":
        cv.poly([(39, 57), (48, 59), (57, 57), (54, 63), (48, 65), (42, 63)], K("granate", 0))
        cv.hline(41, 56, 58, K("papel", 4)); cv.hline(42, 55, 59, K("papel", 4))
        for x in (44, 48, 52):
            cv.px(x, 59, K("papel", 2))
        cv.d.line([(42, 64), (48, 66), (54, 64)], fill=K("piel", 4))
        cv.d.line([37, 53, 37, 60], fill=K("piel", 1)); cv.d.line([59, 53, 59, 60], fill=K("piel", 1))
        cv.px(38, 57, K("piel", 0)); cv.px(58, 57, K("piel", 0))
    elif tipo == "dientes":           # gruñido de odio
        cv.poly([(40, 58), (56, 58), (55, 65), (41, 65)], K("granate", 0))
        cv.hline(41, 56, 59, K("papel", 4)); cv.hline(41, 56, 60, K("papel", 3))
        cv.hline(42, 55, 63, K("papel", 3)); cv.hline(42, 55, 64, K("papel", 2))
        for x in (44, 48, 52):
            cv.vline(x, 59, 61, K("papel", 2)); cv.vline(x, 63, 65, K("papel", 1))
        cv.d.line([(40, 57), (44, 56), (48, 57), (52, 56), (56, 57)], fill=K("piel", 0))
        cv.hline(41, 56, 66, K("piel", 1))
        cv.d.line([42, 54, 38, 62], fill=K("piel", 1)); cv.d.line([54, 54, 58, 62], fill=K("piel", 1))
    elif tipo == "grito":             # júbilo, boca muy abierta
        cv.ellipse(41, 57, 56, 70, K("granate", 0), outline=K("piel", 0))
        cv.ellipse(43, 65, 54, 70, K("granate", 3))
        cv.hline(44, 53, 58, K("papel", 4)); cv.hline(45, 52, 59, K("papel", 3))
        cv.d.line([37, 53, 38, 61], fill=K("piel", 1)); cv.d.line([59, 53, 58, 61], fill=K("piel", 1))
    elif tipo == "mueca":             # desprecio: comisura derecha levantada
        cv.d.line([(42, 61), (48, 61), (55, 57)], fill=K("piel", 0))
        cv.d.line([(49, 60), (55, 56)], fill=K("piel", 1))
        cv.hline(43, 50, 62, K("piel", 4))
        cv.px(56, 56, K("piel", 2)); cv.px(57, 55, K("piel", 2))
        cv.d.line([54, 53, 57, 58], fill=K("piel", 1))
        cv.px(41, 61, K("piel", 1))
    elif tipo == "triste":
        cv.hline(43, 54, 60, K("piel", 0)); cv.px(42, 61, K("piel", 0)); cv.px(54, 61, K("piel", 0))
        cv.px(41, 62, K("piel", 1)); cv.px(55, 62, K("piel", 1))
        cv.hline(44, 53, 61, K("piel", 4) if not femenina else labio)
        cv.hline(46, 51, 64, K("piel", 2)); cv.px(48, 66, K("piel", 2))


def mejillas(cv, alzadas=False):
    y = 50 if alzadas else 52
    cv.rect(33, y, 39, y + 3, K("piel", 4))
    cv.px(34, y + 3, K("granate", 5)); cv.px(36, y + 3, K("granate", 5))
    cv.px(60, y + 2, K("granate", 4)); cv.px(62, y + 2, K("granate", 4))


def arrugas(cv, tipo):
    if tipo == "odio":
        cv.vline(46, 37, 43, K("piel", 1)); cv.vline(50, 37, 43, K("piel", 1))
        cv.hline(45, 52, 44, K("piel", 2))
        for (x, y) in [(64, 26), (65, 27), (65, 28), (64, 29), (65, 30), (66, 31)]:
            cv.px(x, y, K("granate", 4))                                             # vena en la sien
    elif tipo == "duelo":
        cv.d.arc([40, 25, 56, 33], 200, 340, fill=K("piel", 2))
        cv.d.arc([42, 29, 54, 35], 200, 340, fill=K("piel", 2))
    elif tipo == "sonrisa":
        cv.d.line([30, 46, 32, 48], fill=K("piel", 2)); cv.d.line([66, 46, 64, 48], fill=K("piel", 2))


def lagrima(cv):
    for y in range(50, 57):
        cv.px(61, y, K("cielo", 6))
    cv.px(61, 57, K("cielo", 5)); cv.px(62, 51, K("papel", 4))
    cv.px(60, 47, K("papel", 4)); cv.px(38, 47, K("papel", 4))   # ojos húmedos


def grietas(cv):
    lineas = [
        [(29, 28), (34, 34), (38, 40), (36, 47), (40, 53), (44, 58)],
        [(63, 18), (60, 26), (62, 34), (57, 42), (60, 50), (55, 57), (58, 66)],
        [(38, 40), (42, 38)], [(60, 50), (65, 52)], [(36, 47), (31, 49)],
    ]
    for pts in lineas:
        cv.d.line(pts, fill=K("gris", 1))
        cv.d.line([(x + 1, y) for x, y in pts], fill=K("papel", 3))


def luz_telepantalla(cv):
    """Contraluz verde por la derecha: la telepantalla siempre está ahí."""
    img = cv.img
    for y in range(S):
        fila = [img.getpixel((x, y)) for x in range(S)]
        xs = [x for x in range(S) if fila[x] != FONDO]
        if not xs:
            continue
        derecha = max(xs)
        for k, t in ((0, 0.55), (1, 0.30), (2, 0.12)):
            x = derecha - k
            if x >= 0 and fila[x] != FONDO:
                img.putpixel((x, y), mezcla(fila[x], K("tele", 4), t))


# ------------------------------------------------------------------ expresiones
EXPRESIONES = {
    "NEUTRAL":     dict(ojos=dict(apertura=3), cejas=dict(alza=0, inclinacion=0), boca="cerrada"),
    "ENTUSIASMO":  dict(ojos=dict(apertura=4), cejas=dict(alza=3, inclinacion=-1), boca="sonrisa",
                        mejillas=True, arrugas="sonrisa"),
    "ODIO":        dict(ojos=dict(apertura=2, inclinacion=2), cejas=dict(alza=-2, inclinacion=3), boca="dientes",
                        arrugas="odio", aletas=True, tendones=True),
    "JUBILO":      dict(ojos=dict(cerrado_feliz=True), cejas=dict(alza=3, inclinacion=-1), boca="grito",
                        mejillas=True, arrugas="sonrisa"),
    "DESPRECIO":   dict(ojos=dict(apertura=2, mirada=(2, 0)), cejas_izq=dict(alza=-1, inclinacion=1),
                        cejas_der=dict(alza=3, inclinacion=-1), boca="mueca"),
    "DUELO":       dict(ojos=dict(apertura=3, mirada=(0, -1)), cejas=dict(alza=1, inclinacion=-3), boca="triste",
                        arrugas="duelo", lagrima=True),
}


def retrato(nombre, femenina=False, agrietada=False):
    e = EXPRESIONES[nombre]
    cv = Canvas(S, S, bg=("pared", 1))
    if femenina:
        pelo(cv, femenino=True)          # la melena va por detrás de los hombros
    hombros(cv)
    cuello(cv, tendones=e.get("tendones", False))
    cabeza(cv, femenina=femenina)
    if not femenina:
        pelo(cv)
    else:
        # flequillo de la melena por delante de la frente
        cv.poly([(28, 34), (30, 22), (38, 12), (50, 9), (62, 13), (68, 24), (68, 32), (62, 24), (54, 28),
                 (44, 24), (34, 30)], K("madera", 2))
        cv.d.line([(34, 30), (44, 24), (54, 28), (62, 24)], fill=K("madera", 1))
        cv.d.line([(36, 14), (31, 26)], fill=K("madera", 4))
        # mechones laterales por delante de las orejas
        cv.poly([(24, 30), (30, 28), (32, 40), (31, 56), (28, 68), (22, 62)], K("madera", 2))
        cv.d.line([(26, 34), (28, 48), (26, 62)], fill=K("madera", 4))
        cv.poly([(72, 30), (66, 28), (65, 40), (66, 56), (69, 68), (75, 62)], K("madera", 1))
        cv.d.line([(70, 36), (68, 50), (70, 62)], fill=K("madera", 2))
    if e.get("mejillas"):
        mejillas(cv, alzadas=True)
    nariz(cv, aletas=e.get("aletas", False))
    for cx, lado in ((38, 1), (58, -1)):
        ojo(cv, cx, 46, lado, pestanas=femenina, **e["ojos"])
    ci = e.get("cejas_izq", e.get("cejas"))
    cd = e.get("cejas_der", e.get("cejas"))
    color_ceja = K("madera", 1) if femenina else None
    ceja(cv, 38, 38, 1, color=color_ceja, **ci)
    ceja(cv, 58, 38, -1, color=color_ceja, **cd)
    boca(cv, e["boca"], femenina=femenina)
    if e.get("arrugas"):
        arrugas(cv, e["arrugas"])
    if e.get("lagrima"):
        lagrima(cv)
    if agrietada:
        grietas(cv)
    luz_telepantalla(cv)
    return cv.img


if __name__ == "__main__":
    nombres = list(EXPRESIONES) + ["AGRIETADA"]
    COLS, CW, CH = len(nombres), 104, 112
    hoja = Canvas(COLS * CW + 30, 2 * CH + 8, bg=("gris", 1))
    for fila, femenina in enumerate((False, True)):
        y = 6 + fila * CH
        hoja.text(4, y + 44, "M" if femenina else "H", K("papel", 3))
        for i, n in enumerate(nombres):
            x = 24 + i * CW
            img = retrato("ODIO", femenina, True) if n == "AGRIETADA" else retrato(n, femenina)
            hoja.img.paste(img, (x, y))
            hoja.text(x + (S - hoja.text_width(n)) // 2, y + S + 4, n, K("papel", 3))
    prev = hoja.save(Path(__file__).parent / "retratos_protagonista.png", preview_scale=2)
    print("ok", prev)
