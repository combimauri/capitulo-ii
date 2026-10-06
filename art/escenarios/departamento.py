"""J1.05 — Departamento de Partes y Cartografía del Frente (Minipax, planta 14).

Variante "j3": la mesa de Amory sin pájaros y su proyección, firmada por otro, clavada en el mapa.
Variante "noche" (J10.04, parte de "j3"): la Gran Rectificación, de madrugada. Sala a oscuras, lámparas
de mesa encendidas, papeles y mapas por todas partes, el cristal del despacho de Voss negro y el mapa
del frente acribillado de agujeros de alfiler vacíos, con solo unas pocas banderitas negras.
"""
import math
import random

from pixel import Canvas, K
import props as P
import _luz as L

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 16, 88, 246

# mesas: (x, y) de la esquina superior izquierda del tablero
MESAS = [(90, 116), (170, 116), (250, 116),
         (90, 172), (170, 172), (250, 172)]
MESA_PROTA = (170, 172)
MESA_AMORY = (250, 172)


def mapa_malabar(cv, x, y, w, h, rectificado=False):
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
    if rectificado:
        # todas las banderitas arrancadas: agujeros vacíos por todo el corcho y el mapa
        rh = random.Random(1004)
        for _ in range(300):
            hx, hy = rh.randint(x + 1, x + w - 3), rh.randint(y + 1, y + h - 3)
            if rh.random() < 0.6:                                            # más densos a lo largo del frente
                fx, fy = rh.choice(pts[1:-1])
                hx, hy = fx + rh.randint(-14, 14), fy + rh.randint(-10, 10)
            cv.px(hx, hy, K("gris", 1))
        for (px, py) in [pts[2], pts[4], (x + 118, y + 34)]:                 # las pocas banderitas negras que quedan
            cv.vline(px + 6, py - 4, py + 4, K("gris", 1)); cv.rect(px + 7, py - 4, px + 11, py - 1, K("gris", 0))
            cv.px(px + 6, py + 4, K("gris", 6))
        cv.text(x + w // 2 - cv.text_width("MALABAR") // 2, y + h - 12, "MALABAR", K("gris", 1))
        return
    for i, (px, py) in enumerate(pts[1:-1]):                                 # banderitas
        cv.vline(px - 4, py - 8, py - 2, K("gris", 1)); cv.rect(px - 3, py - 8, px + 1, py - 5, K("rojo", 4))
        cv.vline(px + 6, py - 2, py + 4, K("gris", 1)); cv.rect(px + 7, py - 2, px + 11, py + 1, K("gris", 0))
    for _ in range(40):                                                      # agujeros de alfiler
        px, py = rnd.choice(pts[1:-1])
        cv.px(px + rnd.randint(-8, 8), py + rnd.randint(-6, 6), K("gris", 2))
    cv.text(x + w // 2 - cv.text_width("MALABAR") // 2, y + h - 12, "MALABAR", K("gris", 1))


def proyeccion_pell(cv, x, y):
    """La proyección de Amory clavada sobre el mapa: el mundo estirado, sin pájaros, firmada «PELL A.»."""
    cv.rect(x + 2, y + 2, x + 38, y + 30, K("gris", 1))                       # sombra
    cv.rect(x, y, x + 36, y + 28, K("papel", 4))
    cv.d.ellipse([x + 3, y + 4, x + 33, y + 22], outline=K("cielo", 4))       # retícula ovalada
    cv.hline(x + 3, x + 33, y + 13, K("cielo", 5)); cv.vline(x + 18, y + 4, y + 22, K("cielo", 5))
    cv.poly([(x + 6, y + 9), (x + 15, y + 6), (x + 17, y + 12), (x + 9, y + 17)], K("granate", 4))   # Oceanía, enorme
    cv.poly([(x + 21, y + 7), (x + 29, y + 9), (x + 27, y + 14), (x + 22, y + 12)], K("gris", 5))
    cv.text(x + 4, y + 22, "PELL A.", K("gris", 2))
    cv.px(x + 18, y + 1, K("rojo", 4)); cv.px(x + 18, y + 2, K("gris", 2))      # chincheta


def archivador(cv, x, y):
    """Archivador del personal junto a la entrada: tres cajones con tarjetero."""
    cv.rect(x, y, x + 22, y + 8, K("gris", 6)); cv.hline(x, x + 22, y, K("gris", 7))
    cv.rect(x, y + 8, x + 22, y + 44, K("gris", 5)); cv.frame(x, y + 8, x + 22, y + 44, K("gris", 3))
    for k in range(3):
        cy = y + 11 + k * 11
        cv.frame(x + 2, cy, x + 20, cy + 9, K("gris", 3))
        cv.rect(x + 8, cy + 2, x + 14, cy + 4, K("papel", 3))                   # tarjetero
        cv.hline(x + 9, x + 13, cy + 6, K("gris", 7))                          # tirador


def _lampara(cv, x, y):
    """Lámpara de mesa con pantalla de latón; (x, y) = base. Devuelve el centro de la luz."""
    cv.rect(x - 3, y - 1, x + 4, y + 2, K("gris", 1)); cv.hline(x - 3, x + 4, y - 1, K("gris", 3))
    cv.vline(x, y - 9, y - 1, K("gris", 2))
    cv.poly([(x - 5, y - 9), (x - 2, y - 13), (x + 3, y - 13), (x + 6, y - 9)], K("ocre", 1))
    cv.hline(x - 2, x + 3, y - 13, K("ocre", 2))
    cv.rect(x - 4, y - 9, x + 6, y - 7, K("ocre", 4))                                   # boca encendida
    cv.add_emissive(x - 4, y - 9, x + 6, y - 7)
    return (x + 1, y - 4)


def _papeles(cv, x0, y0, x1, y1, n, rnd, mapas=0):
    """Hojas, partes y mapas desparramados (planos sobre la superficie)."""
    for _ in range(n):
        w, h = rnd.choice([(8, 10), (10, 8), (9, 11), (11, 7)])
        px_, py_ = rnd.randint(x0, x1 - w), rnd.randint(y0, y1 - h)
        cv.rect(px_, py_, px_ + w, py_ + h, K("papel", rnd.choice([2, 3, 3, 4])))
        cv.hline(px_ + 2, px_ + w - 2, py_ + 2, K("gris", 6)); cv.hline(px_ + 2, px_ + w - 3, py_ + 4, K("gris", 6))
        if rnd.random() < 0.3:
            cv.d.line([(px_ + 1, py_ + 6), (px_ + w - 2, py_ + 6)], fill=K("rojo", 3))     # tachón
    for _ in range(mapas):
        w, h = rnd.randint(16, 22), rnd.randint(11, 14)
        px_, py_ = rnd.randint(x0, x1 - w), rnd.randint(y0, y1 - h)
        cv.rect(px_, py_, px_ + w, py_ + h, K("papel", 3)); cv.frame(px_, py_, px_ + w, py_ + h, K("papel", 1))
        cv.d.line([(px_ + 2, py_ + h - 3), (px_ + w // 2, py_ + 4), (px_ + w - 2, py_ + 6)], fill=K("cielo", 4))
        cv.px(px_ + w // 2, py_ + 5, K("gris", 0)); cv.px(px_ + 4, py_ + 3, K("ocre", 3))


def dibujar(variante=None):
    noche = variante == "noche"
    j3 = variante in ("j3", "noche")
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=3, motivo="rayas")
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=3)
    # tubos neumáticos a lo largo de la pared
    for i, ty in enumerate((22, 27)):
        cv.hline(X0, X1, ty, K("gris", 6 - i)); cv.hline(X0, X1, ty + 1, K("gris", 3))
    # despacho de Voss (cristal esmerilado)
    P.puerta(cv, 54, 38, w=34, h=50, rampa="madera", base=2, cristal=True)
    if noche:                                                                # cristal negro: ni una luz en el despacho
        cv.rect(58, 43, 84, 60, K("gris", 0)); cv.px(80, 45, K("cielo", 2)); cv.px(81, 46, K("cielo", 2))
    cv.rect(52, 30, 92, 36, K("papel", 3)); cv.text(72 - cv.text_width("SUBDIRECTOR") // 2, 31, "SUBDIRECTOR", K("gris", 1))
    # gran mapa del frente de Malabar
    mapa_malabar(cv, 150, 30, 150, 54, rectificado=noche)
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
    ax, ay = MESA_AMORY
    if j3:
        # la misma mesa, con un parte a medio teclear; ni un pájaro
        cv.rect(ax + 26, ay + 2, ax + 40, ay + 14, K("papel", 3))
        for k in range(4):
            cv.hline(ax + 28, ax + 38 - (k % 2) * 3, ay + 4 + k * 2, K("gris", 5))
        proyeccion_pell(cv, 154, 48)
    else:
        # papeles con pájaros en la mesa de Amory
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
    cv.hline(384, 392, 162, K("ocre", 3))                                            # tirador de latón del cajón
    if j3:
        # el Libro de Registro (tapas de tela gris) y el frasco de chinchetas negras
        cv.rect(356, 138, 374, 156, K("gris", 5)); cv.frame(356, 138, 374, 156, K("gris", 3))
        cv.vline(358, 139, 155, K("gris", 3)); cv.rect(362, 143, 371, 146, K("papel", 3))
        cv.rect(410, 125, 418, 134, K("cielo", 6)); cv.frame(410, 125, 418, 134, K("cielo", 4))
        for (bx, by) in [(412, 129), (415, 131), (413, 132), (416, 128)]:
            cv.px(bx, by, K("gris", 0))
    archivador(cv, 414, 196)
    luces = []
    if noche:
        rnd = random.Random(1010)
        for i, (mx, my) in enumerate(MESAS):
            _papeles(cv, mx + 24, my + 2, mx + 42, my + 20, 3, rnd)            # montones sobre la mesa
            for k in range(4):
                cv.rect(mx + 30, my + 12 - k * 2, mx + 42, my + 20 - k * 2, K("papel", 2 + k % 3))
                cv.hline(mx + 30, mx + 42, my + 20 - k * 2, K("papel", 1))
            luces.append(_lampara(cv, mx + 27, my + 13))
        _papeles(cv, 360, 126, 420, 156, 5, rnd, mapas=2)                     # la mesa del Registro, hasta arriba
        luces.append(_lampara(cv, 416, 140))
        # papeles y mapas por el suelo (en los pasillos entre las mesas, sin bloquear el paso)
        for (a, b, c, d, n, m) in [(46, 96, 86, 240, 6, 1), (136, 150, 168, 170, 2, 0), (216, 150, 248, 170, 2, 1),
                                   (296, 96, 346, 240, 6, 1), (90, 214, 290, 240, 5, 2), (350, 168, 410, 236, 4, 1)]:
            _papeles(cv, a, b, c, d, n, rnd, mapas=m)
        cv.rect(306, 100, 334, 118, K("papel", 2)); cv.frame(306, 100, 334, 118, K("papel", 0))   # un mapa de Malabar arrancado
        cv.d.line([(308, 114), (318, 106), (332, 108)], fill=K("cielo", 3), width=2)
        for (hx, hy) in [(312, 103), (322, 110), (328, 104), (316, 115)]:
            cv.px(hx, hy, K("gris", 1))
    # papeleras
    for (px_, py_) in [(140, 140), (220, 140), (140, 196), (300, 196)]:
        P.papelera(cv, px_, py_)
    # muros laterales e inferior con la puerta a la cantina
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 380, FB + 12, K("gris", 3)); cv.rect(412, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(380, FB, 412, FB + 12, K("madera", 2))
    cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and (x < X0 + 5 or x >= X1 - 5)) else 0)
    if noche:
        def charcos(x, y):
            n = -3
            for (lx, ly) in luces:
                d = math.hypot(x - lx, (y - ly) * 1.25)
                if d < 16:
                    return -1
                if d < 30:
                    n = max(n, -2)
            return n
        cv.add_light_fn(charcos)
        cv.glow_rgb = K("ocre", 3)
        for (lx, ly) in luces:
            cv.add_glow_suave(lx, ly + 4, 34, 0.32, squash=1.2, limite=(X0, WT, X1, FB))
        cv.bake_lighting()
        L.glow_post(cv, 404, 76, 60, 0.22, K("tele", 4), squash=1.4, limite=(X0, WT, X1, FB))
        return cv
    cv.add_glow_suave(404, 76, 70, 0.2, squash=1.4, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
