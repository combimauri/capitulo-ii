"""J1.05 — Departamento de Partes y Cartografía del Frente (Minipax, planta 14)."""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 16, 88, 246

# mesas: (x, y) de la esquina superior izquierda del tablero
MESAS = [(90, 116), (170, 116), (250, 116),
         (90, 172), (170, 172), (250, 172)]
MESA_PROTA = (170, 172)
MESA_AMORY = (250, 172)


def mapa_malabar(cv, x, y, w, h):
    rnd = random.Random(14)
    cv.rect(x - 3, y - 3, x + w + 3, y + h + 3, K("madera", 2))
    cv.rect(x, y, x + w, y + h, K("ocre", 2))                                # corcho
    for _ in range(300):
        cv.px(rnd.randint(x, x + w - 1), rnd.randint(y, y + h - 1), K("ocre", rnd.choice([1, 3])))
    cv.rect(x + 6, y + 5, x + w - 6, y + h - 5, K("papel", 3))               # mapa
    # costa y río Malabar serpenteando
    cv.poly([(x + 6, y + 5), (x + 40, y + 5), (x + 30, y + 22), (x + 6, y + 30)], K("cielo", 5))
    pts = [(x + 10, y + h - 6), (x + 30, y + 30), (x + 52, y + 36), (x + 70, y + 20), (x + 96, y + 26), (x + w - 8, y + 10)]
    cv.d.line(pts, fill=K("cielo", 3), width=2)
    for i, (px, py) in enumerate(pts[1:-1]):                                 # banderitas
        cv.vline(px - 4, py - 8, py - 2, K("gris", 1)); cv.rect(px - 3, py - 8, px + 1, py - 5, K("rojo", 4))
        cv.vline(px + 6, py - 2, py + 4, K("gris", 1)); cv.rect(px + 7, py - 2, px + 11, py + 1, K("gris", 0))
    for _ in range(40):                                                      # agujeros de alfiler
        px, py = rnd.choice(pts[1:-1])
        cv.px(px + rnd.randint(-8, 8), py + rnd.randint(-6, 6), K("gris", 2))
    cv.text(x + w // 2 - cv.text_width("MALABAR") // 2, y + h - 12, "MALABAR", K("gris", 1))


def dibujar():
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=3, motivo="rayas")
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=3)
    # tubos neumáticos a lo largo de la pared
    for i, ty in enumerate((22, 27)):
        cv.hline(X0, X1, ty, K("gris", 6 - i)); cv.hline(X0, X1, ty + 1, K("gris", 3))
    # despacho de Voss (cristal esmerilado)
    P.puerta(cv, 54, 38, w=34, h=50, rampa="madera", base=2, cristal=True)
    cv.rect(52, 30, 92, 36, K("papel", 3)); cv.text(72 - cv.text_width("SUBDIRECTOR") // 2, 31, "SUBDIRECTOR", K("gris", 1))
    # gran mapa del frente de Malabar
    mapa_malabar(cv, 150, 30, 150, 54)
    # agujero de la memoria
    cv.rect(330, 52, 360, 70, K("gris", 2)); cv.rect(334, 58, 356, 64, K("gris", 0))
    cv.text(345 - cv.text_width("MEMORIA") // 2, 46, "MEMORIA", K("gris", 1))
    # telepantalla de la sala
    P.telepantalla(cv, 382, 32, 44, 30)
    # suelo de linóleo
    P.baldosas(cv, X0, WB, X1, FB, K("tela", 3), K("tela", 2), t=16, linea=K("tela", 1))
    # mesas con máquinas de escribir, tubo y telepantallita
    for i, (mx, my) in enumerate(MESAS):
        P.mesa_oficina(cv, mx, my, telepantallita=True, semilla=i)
        cv.rect(mx + 20, my - 18, mx + 23, my, K("gris", 5))                 # tubo vertical
        P.silla(cv, mx + 14, my + 30, rampa="gris", base=4)
    # papeles con pájaros en la mesa de Amory
    ax, ay = MESA_AMORY
    cv.rect(ax + 26, ay + 2, ax + 40, ay + 14, K("papel", 4))
    for (bx, by) in [(ax + 29, ay + 5), (ax + 34, ay + 9), (ax + 37, ay + 4)]:
        cv.px(bx, by, K("gris", 1)); cv.px(bx + 1, by - 1, K("gris", 1)); cv.px(bx - 1, by - 1, K("gris", 1))
    # mesa del Registro (para la Jornada 4): mapa de Londres bajo cristal
    cv.rect(352, 120, 424, 160, K("madera", 3)); cv.rect(356, 124, 420, 156, K("papel", 3))
    for k in range(358, 420, 8):
        cv.vline(k, 124, 156, K("papel", 2))
    for k in range(126, 156, 8):
        cv.hline(356, 420, k, K("papel", 2))
    cv.d.line([(356, 146), (380, 138), (400, 142), (420, 132)], fill=K("cielo", 4), width=2)   # el Támesis
    cv.rect(352, 160, 424, 164, K("madera", 1))
    # papeleras
    for (px_, py_) in [(140, 140), (220, 140), (140, 196), (300, 196)]:
        P.papelera(cv, px_, py_)
    # muros laterales e inferior con la puerta a la cantina
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 380, FB + 12, K("gris", 3)); cv.rect(412, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(380, FB, 412, FB + 12, K("madera", 2))
    cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and (x < X0 + 5 or x >= X1 - 5)) else 0)
    cv.add_glow_suave(404, 76, 70, 0.2, squash=1.4, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
