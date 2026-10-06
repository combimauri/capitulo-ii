"""J1.06 — Cantina del Minipax: techo bajo, mesas metálicas, guiso gris y ginebra.

Variante "miniver": la cantina del Ministerio de la Verdad, abarrotada y ruidosa. Misma planta;
pared de azulejo blanco y gris azulado, luz fría de fluorescentes, bandejas por todas partes,
comensales en los bancos y un cartel enorme de INGSOC.
"""
import random

from pixel import Canvas, K
import props as P
import _luz as L

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 24, 84, 246
MESAS = [(110, 120), (250, 120), (110, 186), (250, 186)]


def mesa_metal(cv, x, y, w=72, d=20, llena=False):
    cv.rect(x + 3, y + d + 3, x + w + 3, y + d + 10, K("gris", 2))
    cv.rect(x, y, x + w, y + d, K("gris", 6)); cv.frame(x, y, x + w, y + d, K("gris", 3))
    cv.hline(x + 1, x + w - 1, y + 1, K("gris", 8))
    cv.rect(x, y + d, x + w, y + d + 4, K("gris", 4))
    for k in range(x + 8, x + w - 8, 18):                                    # bandejas con guiso
        cv.rect(k, y + 4, k + 12, y + 12, K("gris", 4)); cv.rect(k + 2, y + 6, k + 10, y + 10, K("papel", 1))
        cv.px(k + 13, y + 6, K("cielo", 6))                                  # vaso de ginebra
    if llena:                                                                # segunda fila de bandejas, cucharas y migas
        for k in range(x + 4, x + w - 10, 14):
            cv.rect(k, y + 13, k + 11, y + 19, K("gris", 7)); cv.frame(k, y + 13, k + 11, y + 19, K("gris", 4))
            cv.rect(k + 2, y + 14, k + 7, y + 18, K("ocre", 1) if (k // 14) % 2 else K("papel", 1))
            cv.hline(k + 8, k + 10, y + 15, K("gris", 9))
    # bancos
    cv.rect(x, y - 8, x + w, y - 4, K("madera", 3)); cv.rect(x, y + d + 8, x + w, y + d + 12, K("madera", 3))


def _comensal(cv, x, y, rnd, de_cara):
    """Funcionario sentado en el banco. de_cara: banco de arriba (se le ve la cara); si no, de espaldas."""
    ropa, b = rnd.choice([("azul", 2), ("azul", 2), ("azul", 3), ("azul", 1), ("tela", 2)])
    pelo = rnd.choice([("pelo", 0), ("pelo", 1), ("madera", 2), ("ocre", 1), ("gris", 6)])
    piel = rnd.choice([2, 3, 3, 4])
    cv.rect(x - 6, y - 8, x + 6, y + 1, K(ropa, b)); cv.hline(x - 6, x + 6, y - 8, K(ropa, b + 1))
    cv.vline(x - 7, y - 6, y + 1, K(ropa, b - 1)); cv.vline(x + 6, y - 6, y + 1, K(ropa, b - 1))
    if de_cara:
        cv.rect(x - 4, y - 16, x + 4, y - 8, K("piel", piel)); cv.rect(x - 4, y - 17, x + 4, y - 14, K(*pelo))
        cv.px(x - 2, y - 12, K("gris", 1)); cv.px(x + 1, y - 12, K("gris", 1))
        if rnd.random() < 0.5:                                              # boca abierta: habla, ríe, grita
            cv.hline(x - 1, x + 1, y - 10, K("piel", 0))
        cv.hline(x - 6, x + 6, y + 1, K(ropa, b - 1))
    else:
        cv.ellipse(x - 4, y - 16, x + 5, y - 7, K(*pelo)); cv.vline(x - 4, y - 12, y - 9, K("piel", piel - 1))


def _cartel_ingsoc(cv, x, y, w, h):
    cv.rect(x + 2, y + 2, x + w + 2, y + h + 2, K("gris", 3))                # sombra
    cv.rect(x, y, x + w, y + h, K("rojo", 3)); cv.frame(x, y, x + w, y + h, K("rojo", 1))
    cv.frame(x + 2, y + 2, x + w - 2, y + h - 2, K("papel", 3))
    # la pirámide blanca del Ministerio sobre el lema
    pcx = x + w // 2
    for i, pw in enumerate([18, 14, 10, 6, 2]):
        cv.rect(pcx - pw, y + 20 - i * 3, pcx + pw, y + 23 - i * 3, K("papel", 4 if i % 2 == 0 else 3))
    cv.rect(pcx - 20, y + 23, pcx + 20, y + 24, K("rojo", 1))
    L.texto_grande(cv, pcx - L.ancho_grande("INGSOC") // 2 + 1, y + 28, "INGSOC", K("rojo", 1))
    L.texto_grande(cv, pcx - L.ancho_grande("INGSOC") // 2, y + 27, "INGSOC", K("papel", 4))
    t = "MINIVER"
    cv.text(pcx - cv.text_width(t) // 2, y + h - 8, t, K("papel", 3))
    for (cx, cy) in [(x + 1, y + 1), (x + w - 2, y + 1)]:
        cv.px(cx, cy, K("gris", 8))


def dibujar(variante=None):
    mv = variante == "miniver"
    rnd = random.Random(1949)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    if mv:
        cv.rect(X0, WT, X1, WB, K("cielo", 4))
        cv.rect(X0, WT, X1, 40, K("cielo", 3))
        for x in range(X0, X1, 12):                                          # azulejo blanco hasta más arriba
            for y in range(44, WB, 10):
                cv.rect(x, y, x + 12, y + 10, K("papel", 4)); cv.frame(x, y, x + 12, y + 10, K("papel", 2))
        cv.hline(X0, X1, 43, K("cielo", 2))
    else:
        cv.rect(X0, WT, X1, WB, K("pared", 2))
        cv.rect(X0, WT, X1, 40, K("pared", 1))
        for x in range(X0, X1, 16):                                              # azulejo blanco a media altura
            cv.rect(x, 54, x + 16, WB, K("papel", 3)); cv.frame(x, 54, x + 16, 70, K("papel", 2)); cv.frame(x, 70, x + 16, WB, K("papel", 2))
    # telepantalla grande con cifras de producción (barras)
    tx, ty, tw, th = 196, 28, 100, 44
    P.telepantalla(cv, tx, ty, tw, th, cara=False)
    for i, h in enumerate([12, 20, 16, 28, 34] if not mv else [10, 14, 20, 26, 34]):
        cv.rect(tx + 12 + i * 16, ty + th - 6 - h, tx + 22 + i * 16, ty + th - 6, K("tele", 4))
    cv.text(tx + 6, ty + 4, "BOTAS 98" if not mv else "CHOCOLATE 20 G", K("tele", 6))
    if mv:
        _cartel_ingsoc(cv, 328, 26, 84, 50)
        # tablón de menú: GUISO · PAN · GINEBRA VICTORIA
        cv.rect(98, 30, 168, 62, K("gris", 2)); cv.frame(98, 30, 168, 62, K("gris", 1))
        for i, t in enumerate(["MENU", "GUISO", "PAN 1", "GINEBRA"]):
            cv.text(103, 33 + i * 7, t, K("papel", 4 if i == 0 else 2))
        cv.px(166, 32, K("gris", 6))
        for fx in (130, 250, 370):                                           # fluorescentes del techo
            cv.rect(fx - 26, WT - 6, fx + 26, WT - 1, K("gris", 2)); cv.rect(fx - 24, WT - 5, fx + 24, WT - 2, K("papel", 4))
            cv.add_emissive(fx - 24, WT - 5, fx + 24, WT - 2)
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=3)
    if mv:
        P.baldosas(cv, X0, WB, X1, FB, K("gris", 6), K("gris", 5), t=12, linea=K("gris", 4))
    else:
        P.baldosas(cv, X0, WB, X1, FB, K("gris", 5), K("gris", 4), t=12, linea=K("gris", 3))
    for (mx, my) in MESAS:
        mesa_metal(cv, mx, my, llena=mv)
    if mv:
        for (mx, my) in MESAS:                                               # bancos abarrotados
            for x in range(mx + 7, mx + 70, 12):
                if rnd.random() < 0.85:
                    _comensal(cv, x + rnd.randint(-1, 1), my - 5, rnd, de_cara=True)
            for x in range(mx + 7, mx + 70, 12):
                if rnd.random() < 0.85:
                    _comensal(cv, x + rnd.randint(-1, 1), my + 35, rnd, de_cara=False)
    # mostrador con ollas
    cv.rect(X0, 92, 84, 236, K("gris", 4)); cv.rect(X0, 92, 84, 96, K("gris", 6))
    for oy in (104, 140, 176):
        cv.ellipse(48, oy, 76, oy + 20, K("gris", 2), outline=K("gris", 6)); cv.ellipse(52, oy + 3, 72, oy + 15, K("papel", 1))
    if mv:
        for k in range(6):                                                   # pila de bandejas limpias
            cv.rect(46, 222 - k * 2, 78, 230 - k * 2, K("gris", 7 if k % 2 else 8)); cv.hline(46, 78, 230 - k * 2, K("gris", 4))
        for (vx, vy) in [(50, 126), (58, 128), (66, 126), (54, 162), (62, 162)]:   # vasos de ginebra en fila
            cv.rect(vx, vy, vx + 4, vy + 6, K("cielo", 6)); cv.hline(vx, vx + 4, vy + 5, K("cielo", 4))

    # muros
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 330, FB + 12, K("gris", 3)); cv.rect(362, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(330, FB, 362, FB + 12, K("madera", 2))                                   # puerta al pasillo
    cv.add_light(X0, WB, X1, FB, 0)
    if mv:
        cv.add_light_fn(lambda x, y: -1 if (WB <= y < FB and (x < X0 + 5 or x >= X1 - 5 or y >= FB - 5)) else 0)
        cv.glow_rgb = K("cielo", 6)
        for fx in (130, 250, 370):
            cv.add_glow_suave(fx, 120, 120, 0.2, squash=1.2, limite=(X0, WT, X1, FB))
        cv.bake_lighting()
        L.glow_post(cv, 246, 80, 70, 0.14, K("tele", 4), squash=1.3, limite=(X0, WT, X1, FB))
        return cv
    cv.add_glow_suave(246, 80, 110, 0.18, squash=1.3, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
