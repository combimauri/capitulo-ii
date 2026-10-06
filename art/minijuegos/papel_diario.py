"""El diario (DiarioScene): el cuaderno de tapas negras, abierto sobre la mesa de la cocina del piso, de noche.

Tapas de cartón negro con las esquinas gastadas, papel crema de antes de la Revolución (`papel 4`), el canto de las
hojas a los lados, el lomo cosido con la sombra de la curvatura, los restos de las primeras páginas arrancadas y el
pájaro que Amory dibujó a lápiz en la primera hoja. Renglones `cielo 5` en la página de escribir, al paso de la letra.
Sobre la mesa: un vaso de ginebra Victoria, las virutas del lápiz recién afilado y una caja de cerillas. La telepantalla
está fuera de cuadro, arriba a la derecha: su luz verde llega a la esquina de la mesa, no al cuaderno (el ángulo muerto).

Pantalla → arte: tapas (100, 60, 760×440) → (50, 30)-(430, 250); páginas (118|486, 70, 360×420) → (59|243, 35, 180×210).
"""
import math
import random

from pixel import Canvas, K
import papel as PP

TAPA = (50, 30, 430, 250)
IZQ = (59, 35, 239, 245)
DER = (243, 35, 423, 245)
# renglones de la escena: y = 112 + 25 + 27.5·k (px de pantalla), hasta 470
RENGLONES = [int((112 + 25 + 27.5 * k) // 2) for k in range(20) if 112 + 25 + 27.5 * k < 470]


def _vaso(cv, x, y):
    """Vaso de ginebra Victoria visto desde arriba, con un dedo de líquido aceitoso."""
    PP.sombra_elipse(cv, x - 12, y - 12, x + 13, y + 13, 3, 3)
    cv.ellipse(x - 12, y - 12, x + 13, y + 13, K("cielo", 3), outline=K("cielo", 1))
    cv.ellipse(x - 10, y - 10, x + 11, y + 11, K("cielo", 2))
    cv.ellipse(x - 7, y - 7, x + 8, y + 8, K("ocre", 1))
    cv.ellipse(x - 6, y - 6, x + 6, y + 5, K("ocre", 2))
    cv.d.arc([x - 12, y - 12, x + 13, y + 13], 190, 270, fill=K("cielo", 6))
    cv.d.arc([x - 10, y - 10, x + 11, y + 11], 20, 70, fill=K("cielo", 4))
    cv.px(x - 3, y - 3, K("ocre", 4)); cv.px(x - 2, y - 3, K("ocre", 3))


def _botella(cv, x, y):
    """La botella de ginebra Victoria tumbada en la penumbra, con su etiqueta blanca."""
    PP.sombra(cv, x, y, x + 54, y + 13, 2, 3)
    cv.rect(x + 4, y, x + 40, y + 13, K("cielo", 1))
    cv.rect(x + 40, y + 3, x + 52, y + 10, K("cielo", 1))
    cv.rect(x + 52, y + 2, x + 56, y + 11, K("gris", 2))
    cv.ellipse(x, y, x + 9, y + 13, K("cielo", 1))
    cv.hline(x + 4, x + 50, y + 2, K("cielo", 3)); cv.hline(x + 8, x + 30, y + 3, K("cielo", 4))
    cv.hline(x + 4, x + 40, y + 11, K("cielo", 0))
    cv.rect(x + 14, y + 2, x + 30, y + 11, K("papel", 3)); cv.frame(x + 14, y + 2, x + 30, y + 11, K("papel", 1))
    cv.text(x + 15, y + 4, "VIC", K("rojo", 3))


def _virutas(cv, x, y, rnd):
    """Virutas del lápiz recién afilado: rizos de madera con el filo pintado y polvo de grafito."""
    for k in range(4):
        cx, cy = x + rnd.randint(0, 22), y + rnd.randint(0, 12)
        for a in range(0, 300, 30):
            r = 3 - a / 150
            px_ = int(cx + math.cos(math.radians(a)) * r * 1.4); py = int(cy + math.sin(math.radians(a)) * r)
            cv.px(px_, py, K("madera", 6) if a < 200 else K("ocre", 2))
        cv.px(cx + 4, cy, K("rojo", 3))
    for _ in range(14):
        cv.px(x + rnd.randint(-4, 28), y + rnd.randint(-2, 16), K("gris", rnd.choice([2, 3])))


def _cerillas(cv, x, y):
    PP.sombra(cv, x, y, x + 22, y + 13, 2, 2)
    cv.rect(x, y, x + 22, y + 13, K("ocre", 2)); cv.frame(x, y, x + 22, y + 13, K("ocre", 0))
    cv.rect(x + 2, y + 2, x + 20, y + 11, K("rojo", 2))
    cv.rect(x + 6, y + 4, x + 16, y + 9, K("papel", 3))
    cv.hline(x + 8, x + 14, y + 6, K("gris", 2))
    for k in range(2):                                                         # dos cerillas gastadas
        cv.hline(x + 26 + k * 3, x + 36 + k * 3, y + 4 + k * 5, K("madera", 6))
        cv.px(x + 36 + k * 3, y + 4 + k * 5, K("gris", 0)); cv.px(x + 37 + k * 3, y + 4 + k * 5, K("gris", 1))


PAJARO = [
    "...........ggg......",
    "..........g...g.....",
    ".........g..o..ggg..",
    "........g......gg...",
    ".......g.......g....",
    "......g..sss....g...",
    "....gg..sssss...g...",
    "..gg.....ssss...g...",
    "gg.g...........g....",
    "...gg........gg.....",
    ".....ggggggggg......",
    "........g..g........",
    "........g..g........",
    ".sssssssssssssssss..",
]


def _pajaro(cv, x, y):
    """El pájaro de Amory, a lápiz: un gorrión posado en una ramita, mirando a la derecha (20×14 px)."""
    cv.grid(x, y, PAJARO, {"g": K("gris", 3), "s": K("gris", 7), "o": K("gris", 1)})


def dibujar():
    rnd = random.Random(19)
    cv = Canvas(480, 270, ("madera", 2))
    PP.madera_mesa(cv, 0, 0, 480, 270, base=2, semilla=7, tabla=22)
    _botella(cv, 6, 6)
    _vaso(cv, 24, 232)
    _virutas(cv, 440, 220, rnd)
    _cerillas(cv, 436, 70)
    for _ in range(9):                                                         # migas de pan negro
        cv.px(rnd.randint(4, 46), rnd.randint(40, 200), K("madera", 5))

    # --- el cuaderno: tapas negras de cartón forrado
    x0, y0, x1, y1 = TAPA
    PP.sombra(cv, x0, y0, x1, y1, 4, 4, fuerte=3)
    cv.rect(x0, y0, x1, y1, K("gris", 1))
    cv.frame(x0, y0, x1, y1, K("gris", 0))
    cv.hline(x0 + 1, x1 - 1, y0 + 1, K("gris", 3)); cv.vline(x0 + 1, y0 + 1, y1 - 1, K("gris", 2))
    for (cx, cy) in ((x0, y0), (x1 - 1, y0), (x0, y1 - 1), (x1 - 1, y1 - 1)):  # esquinas gastadas, cartón gris
        for k in range(3):
            cv.px(cx + (k if cx == x0 else -k), cy, K("gris", 4))
            cv.px(cx, cy + (k if cy == y0 else -k), K("gris", 4))
        cv.px(cx, cy, K("madera", 3))
    for _ in range(40):                                                        # roces en la tela de la tapa
        cv.px(rnd.randint(x0 + 2, x1 - 3), rnd.choice([rnd.randint(y0 + 1, y0 + 4), rnd.randint(y1 - 5, y1 - 2)]), K("gris", 2))
    cv.rect(237, y0, 245, y1, K("gris", 0))                                    # lomo
    cv.vline(240, y0, y1, K("gris", 2)); cv.vline(241, y0, y1, K("gris", 1))

    # --- el canto de las hojas (el bloque, visto por los lados)
    for k in range(3):
        cv.rect(IZQ[0] - 3 + k, IZQ[1] - 1 + k, IZQ[2], IZQ[3] + 2 - k, K("papel", 1 + k))
        cv.rect(DER[0], DER[1] - 1 + k, DER[2] + 3 - k, DER[3] + 2 - k, K("papel", 1 + k))

    # --- las dos páginas
    def tono_izq(x, y):
        d = IZQ[2] - x                                                         # curvatura hacia el lomo
        return -2 if d < 2 else -1 if d < 6 or (d < 10 and (x + y) % 2) else 0

    def tono_der(x, y):
        d = x - DER[0]
        return -2 if d < 2 else -1 if d < 6 or (d < 10 and (x + y) % 2) else 0

    mi = PP.mascara_rect(*IZQ, rnd, mordidas=0.03, muescas=0, esquinas=[(IZQ[0], IZQ[1]), (IZQ[0], IZQ[3] - 1)])
    md = PP.mascara_rect(*DER, rnd, mordidas=0.03, muescas=0, esquinas=[(DER[2] - 1, DER[1]), (DER[2] - 1, DER[3] - 1)])
    PP.pintar_hoja(cv, mi, base=4, semilla=3, fibra=0.025, tono=tono_izq)
    PP.pintar_hoja(cv, md, base=4, semilla=4, fibra=0.025, tono=tono_der)
    PP.manchas_papel(cv, IZQ[0] + 2, IZQ[1] + 2, IZQ[2] - 10, IZQ[3] - 2, 3, semilla=2, radio=(1, 3))
    PP.manchas_papel(cv, DER[0] + 10, DER[1] + 2, DER[2] - 2, DER[3] - 2, 2, semilla=5, radio=(1, 2))

    # renglones: claros en la hoja izquierda (no se escribe en ella: es el menú), cielo 5 en la derecha
    PP.renglones(cv, 248, 416, RENGLONES, K("cielo", 5))
    PP.renglones(cv, IZQ[0] + 6, IZQ[2] - 10, RENGLONES, K("papel", 3))
    cv.hline(DER[0] + 4, DER[2] - 4, 49, K("cielo", 4))                         # renglón de cabecera

    # restos de las primeras páginas, arrancadas, asomando del cosido: un filo roto y desigual
    w = 3
    for y in range(IZQ[1] + 1, IZQ[3] - 1):
        w = max(2, min(6, w + rnd.choice([-1, 0, 0, 0, 1])))
        xa = IZQ[2] - 3 - w
        cv.px(xa, y, K("papel", 1))
        for x in range(xa + 1, IZQ[2] - 3):
            cv.px(x, y, K("papel", 3))
        cv.px(IZQ[2] - 3, y, K("papel", 2))
    # las puntadas del hilo en el lomo
    for y in range(IZQ[1] + 14, IZQ[3] - 10, 30):
        cv.vline(240, y, y + 5, K("papel", 1)); cv.vline(241, y, y + 5, K("papel", 2))

    # el pájaro de Amory, dentro, en la esquina de la primera hoja
    _pajaro(cv, 204, 40)

    # la telepantalla, fuera de cuadro arriba a la derecha: alcanza la mesa, no el cuaderno
    cv.glow_rgb = K("tele", 4)
    cv.add_glow_suave(510, -20, 150, 0.40, squash=1.0)
    cv.bake_lighting()
    return cv


def exportar(destino):
    dibujar().img.save(destino / "diario-fondo.png")
    return ["diario-fondo.png"]
