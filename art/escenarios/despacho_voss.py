"""J2.04-C — Despacho del Subdirector Voss: austero, con la única ventana de la planta."""
from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 120, 360
WT, WB, FB = 30, 94, 230


def dibujar():
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="pared", base=2, motivo="rayas")
    # ventana estrecha
    cv.rect(162, 36, 186, 82, K("madera", 1)); cv.rect(165, 39, 183, 79, K("cielo", 4)); cv.vline(174, 39, 79, K("madera", 1))
    # telepantalla apagada (Voss puede apagarla)
    cv.rect(290, 40, 340, 76, K("gris", 1)); cv.rect(294, 44, 336, 72, K("gris", 0))
    cv.px(334, 74, K("gris", 3))
    # archivadores
    for ax in (126, 140):
        cv.rect(ax, 52, ax + 12, WB + 6, K("gris", 4)); cv.frame(ax, 52, ax + 12, WB + 6, K("gris", 2))
        for y in (60, 72, 84):
            cv.hline(ax + 2, ax + 10, y, K("gris", 2)); cv.px(ax + 6, y + 3, K("gris", 6))
    P.cartel_gran_hermano(cv, 214, 36, w=40, h=48)
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1)
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=2, semilla=4)
    cv.rect(180, 130, 300, 140, K("granate", 2))                                  # alfombra corta
    # mesa de Voss con carpetas, ficha y café de verdad
    cv.rect(196, 104, 286, 128, K("madera", 3)); cv.frame(196, 104, 286, 128, K("madera", 1)); cv.hline(197, 285, 105, K("madera", 4))
    cv.rect(196, 128, 286, 134, K("madera", 2))
    cv.rect(206, 108, 226, 122, K("papel", 3)); cv.rect(209, 106, 229, 120, K("papel", 4))
    cv.rect(236, 112, 248, 120, K("papel", 2)); cv.hline(237, 247, 114, K("gris", 5))
    cv.ellipse(262, 110, 272, 118, K("papel", 4), outline=K("gris", 4)); cv.ellipse(264, 112, 270, 116, K("madera", 0))
    for k in range(3):
        cv.px(266 + k % 2, 106 - k * 2, K("papel", 3))                            # vapor del café
    P.silla(cv, 234, 84, rampa="madera", base=2)
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    cv.add_light_fn(lambda x, y: 1 if (WB <= y < FB and 150 < x < 220 and (x - 150) > (y - WB) * 0.4) else 0)
    cv.bake_lighting()
    return cv
