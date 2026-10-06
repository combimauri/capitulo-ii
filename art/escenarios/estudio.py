"""J5.03 — Estudio Crane: pequeño y cálido, paredes llenas de caras y un cuarto oscuro cerrado.

Variante "j6": la bombilla roja del cuarto oscuro, encendida (hay alguien, o algo, trabajando dentro).
"""
import random

from pixel import Canvas, K
import props as P

W, H = 480, 270
X0, X1 = 80, 400
WT, WB, FB = 20, 92, 236


def marco(cv, x, y, w, h, rnd):
    cv.rect(x, y, x + w, y + h, K("madera", rnd.choice([1, 2, 3])))
    cv.rect(x + 2, y + 2, x + w - 2, y + h - 2, K("papel", rnd.choice([1, 2, 3])))
    # una o dos caras, sin consignas
    for k in range(rnd.choice([1, 1, 2, 3])):
        fx = x + 4 + k * 5
        if fx + 3 < x + w - 2:
            cv.rect(fx, y + 4, fx + 3, y + 7, K("gris", 4)); cv.rect(fx - 1, y + 8, fx + 4, y + h - 3, K("gris", 3))


def dibujar(variante=None):
    rnd = random.Random(7)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    P.papel_pintado(cv, X0, WT, X1, WB, rampa="ocre", base=1, motivo="rombo")
    # la pared de las fotografías (izquierda y centro)
    for (fx, fy, fw, fh) in [(90, 28, 16, 20), (110, 26, 22, 16), (136, 30, 14, 18), (90, 54, 20, 16), (114, 48, 16, 22),
                             (134, 54, 22, 16), (160, 28, 18, 22), (182, 32, 14, 16), (160, 56, 24, 18), (188, 52, 14, 20),
                             (206, 28, 20, 16), (206, 50, 16, 22)]:
        marco(cv, fx, fy, fw, fh, rnd)
    # cuarto oscuro: puerta con cartel y bombilla roja apagada
    P.puerta(cv, 330, 44, w=30, h=48, rampa="gris", base=2)
    cv.rect(324, 34, 366, 41, K("papel", 3)); cv.text(345 - cv.text_width("NO ENTRAR") // 2, 35, "NO ENTRAR", K("rojo", 3))
    cv.ellipse(341, 24, 349, 32, K("rojo", 4) if variante == "j6" else K("granate", 2), outline=K("gris", 1))
    # recortes viejos enmarcados, «para practicar restauraciones»
    cv.rect(178, 76, 198, 90, K("madera", 2)); cv.rect(180, 78, 196, 88, K("papel", 2))
    for k in range(3):
        cv.hline(182, 194, 80 + k * 3, K("gris", 4))
    # fondos pintados enrollados (un jardín, una playa)
    cv.rect(240, 26, 312, 32, K("gris", 2))
    cv.rect(244, 32, 274, 86, K("tele", 3)); cv.rect(244, 70, 274, 86, K("tele", 2))
    cv.ellipse(250, 40, 262, 52, K("tele", 4))
    cv.rect(280, 32, 308, 86, K("cielo", 5)); cv.rect(280, 66, 308, 86, K("ocre", 4))
    P.zocalo(cv, X0, X1, WB, rampa="madera", base=1)
    P.tablones(cv, X0, WB, X1, FB, rampa="madera", base=2, semilla=12)
    cv.rect(150, 150, 300, 200, K("granate", 2)); cv.frame(150, 150, 300, 200, K("granate", 1))     # alfombra
    # la silla de terciopelo gastado
    cv.rect(262, 100, 286, 128, K("granate", 3)); cv.rect(262, 120, 286, 134, K("granate", 4)); cv.hline(262, 286, 100, K("granate", 5))
    cv.vline(264, 134, 140, K("madera", 1)); cv.vline(284, 134, 140, K("madera", 1))
    # el mostrador con lupas y pinceles
    cv.rect(96, 118, 176, 138, K("madera", 3)); cv.hline(96, 176, 118, K("madera", 4)); cv.rect(96, 138, 176, 146, K("madera", 1))
    cv.ellipse(104, 122, 112, 130, None, outline=K("gris", 6)); cv.d.line([(111, 129), (116, 134)], fill=K("madera", 1))
    for k in range(4):
        cv.vline(130 + k * 4, 121, 132, K("madera", 0)); cv.px(130 + k * 4, 120, K("gris", 1))
    cv.rect(150, 122, 170, 132, K("papel", 3))                                                       # sobres
    # la estufa apagada
    cv.rect(360, 120, 384, 160, K("gris", 2)); cv.frame(360, 120, 384, 160, K("gris", 1)); cv.rect(366, 140, 378, 152, K("gris", 0))
    cv.vline(372, 92, 120, K("gris", 3))
    # muros y puerta a la calle
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(200, 120, 140, 0.25, squash=1.3, limite=(X0, WT, X1, FB))
    if variante == "j6":
        cv.add_emissive(341, 24, 349, 32)
        cv.glow_rgb = K("rojo", 4)
        cv.add_glow_suave(345, 30, 40, 0.35, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
