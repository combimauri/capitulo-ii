"""J1.06 — Cantina del Minipax: techo bajo, mesas metálicas, guiso gris y ginebra."""
from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 40, 440
WT, WB, FB = 24, 84, 246
MESAS = [(110, 120), (250, 120), (110, 186), (250, 186)]


def mesa_metal(cv, x, y, w=72, d=20):
    cv.rect(x + 3, y + d + 3, x + w + 3, y + d + 10, K("gris", 2))
    cv.rect(x, y, x + w, y + d, K("gris", 6)); cv.frame(x, y, x + w, y + d, K("gris", 3))
    cv.hline(x + 1, x + w - 1, y + 1, K("gris", 8))
    cv.rect(x, y + d, x + w, y + d + 4, K("gris", 4))
    for k in range(x + 8, x + w - 8, 18):                                    # bandejas con guiso
        cv.rect(k, y + 4, k + 12, y + 12, K("gris", 4)); cv.rect(k + 2, y + 6, k + 10, y + 10, K("papel", 1))
        cv.px(k + 13, y + 6, K("cielo", 6))                                  # vaso de ginebra
    # bancos
    cv.rect(x, y - 8, x + w, y - 4, K("madera", 3)); cv.rect(x, y + d + 8, x + w, y + d + 12, K("madera", 3))


def dibujar():
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    cv.rect(X0, WT, X1, WB, K("pared", 2))
    cv.rect(X0, WT, X1, 40, K("pared", 1))
    for x in range(X0, X1, 16):                                              # azulejo blanco a media altura
        cv.rect(x, 54, x + 16, WB, K("papel", 3)); cv.frame(x, 54, x + 16, 70, K("papel", 2)); cv.frame(x, 70, x + 16, WB, K("papel", 2))
    # telepantalla grande con cifras de producción (barras)
    tx, ty, tw, th = 196, 28, 100, 44
    P.telepantalla(cv, tx, ty, tw, th, cara=False)
    for i, h in enumerate([12, 20, 16, 28, 34]):
        cv.rect(tx + 12 + i * 16, ty + th - 6 - h, tx + 22 + i * 16, ty + th - 6, K("tele", 4))
    cv.text(tx + 6, ty + 4, "BOTAS 98", K("tele", 6))
    P.zocalo(cv, X0, X1, WB, rampa="gris", base=3)
    P.baldosas(cv, X0, WB, X1, FB, K("gris", 5), K("gris", 4), t=12, linea=K("gris", 3))
    for (mx, my) in MESAS:
        mesa_metal(cv, mx, my)
    # mostrador con ollas
    cv.rect(X0, 92, 84, 236, K("gris", 4)); cv.rect(X0, 92, 84, 96, K("gris", 6))
    for oy in (104, 140, 176):
        cv.ellipse(48, oy, 76, oy + 20, K("gris", 2), outline=K("gris", 6)); cv.ellipse(52, oy + 3, 72, oy + 15, K("papel", 1))

    # muros
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 330, FB + 12, K("gris", 3)); cv.rect(362, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(330, FB, 362, FB + 12, K("madera", 2))                                   # puerta al pasillo
    cv.add_light(X0, WB, X1, FB, 0)
    cv.add_glow_suave(246, 80, 110, 0.18, squash=1.3, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
