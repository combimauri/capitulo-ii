"""J5.03 — Estudio Crane: pequeño y cálido, paredes llenas de caras y un cuarto oscuro cerrado.

Variante "j6": la bombilla roja del cuarto oscuro, encendida (hay alguien, o algo, trabajando dentro).
Variante "j12": de noche y a oscuras, salvo la bombilla roja. La puerta del cuarto oscuro, abierta: cubetas,
fotos colgadas de pinzas y una grabadora de bobinas cuyos cables salen por un agujero de la pared hacia
un panelito con etiquetas. En el mostrador, el juego de té.
"""
import math
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


def _cuarto_oscuro(cv, x0, y0, x1, y1):
    """Interior del cuarto oscuro visto por la puerta abierta (x0..x1, y0..y1 = hueco de la puerta)."""
    cv.rect(x0, y0, x1, y1, K("granate", 1))                                     # pared del fondo, en rojo
    cv.rect(x0, y0, x1, y0 + 3, K("granate", 0))
    cv.rect(x1 - 4, y0, x1, y1, K("granate", 0))                                 # pared lateral derecha
    # el agujero en la pared y el panelito con etiquetas encima
    cv.ellipse(x1 - 4, y0 + 22, x1, y0 + 27, K("gris", 0))
    cv.rect(x0 + 14, y0 + 6, x1 - 6, y0 + 15, K("gris", 2)); cv.frame(x0 + 14, y0 + 6, x1 - 6, y0 + 15, K("gris", 0))
    for k in range(3):
        cv.hline(x0 + 16 + k * 3, x0 + 18 + k * 3, y0 + 8, K("papel", 3))        # etiquetas
        cv.px(x0 + 16 + k * 3, y0 + 11, K("rojo", 5)); cv.px(x0 + 17 + k * 3, y0 + 12, K("gris", 5))   # pilotos y mandos
    # cuerda con fotos colgadas de pinzas
    cv.hline(x0 + 1, x0 + 14, y0 + 6, K("gris", 3))
    for k, fx in enumerate((x0 + 2, x0 + 7)):
        cv.px(fx + 2, y0 + 6, K("madera", 4)); cv.px(fx + 2, y0 + 7, K("madera", 4))
        cv.rect(fx, y0 + 8, fx + 5, y0 + 15, K("papel", 2)); cv.rect(fx + 1, y0 + 10, fx + 4, y0 + 13, K("granate", 3 - k))
    cv.hline(x0 + 1, x1 - 4, y0 + 18, K("gris", 3))
    for fx in (x0 + 3, x0 + 10, x0 + 17):
        cv.px(fx + 2, y0 + 18, K("madera", 4))
        cv.rect(fx, y0 + 19, fx + 5, y0 + 25, K("papel", 1)); cv.rect(fx + 1, y0 + 20, fx + 4, y0 + 23, K("granate", 2))
    # estante con la grabadora de bobinas
    cv.rect(x0, y0 + 34, x1 - 4, y0 + 36, K("madera", 2))
    cv.rect(x0 + 4, y0 + 26, x0 + 22, y0 + 34, K("gris", 2)); cv.frame(x0 + 4, y0 + 26, x0 + 22, y0 + 34, K("gris", 0))
    for rx in (x0 + 5, x0 + 14):
        cv.ellipse(rx, y0 + 25, rx + 7, y0 + 32, K("gris", 4), outline=K("gris", 1)); cv.px(rx + 3, y0 + 28, K("gris", 0))
    cv.hline(x0 + 8, x0 + 18, y0 + 32, K("madera", 1))                           # la cinta
    cv.d.line([(x0 + 22, y0 + 30), (x1 - 5, y0 + 27), (x1 - 3, y0 + 24)], fill=K("gris", 0))          # cables al agujero
    cv.d.line([(x0 + 22, y0 + 32), (x1 - 6, y0 + 30), (x1 - 3, y0 + 26)], fill=K("rojo", 1))
    cv.d.line([(x1 - 6, y0 + 15), (x1 - 3, y0 + 23)], fill=K("gris", 0))
    # banco de trabajo con tres cubetas de revelado
    cv.rect(x0, y0 + 38, x1 - 4, y0 + 43, K("madera", 3)); cv.rect(x0, y0 + 43, x1 - 4, y1, K("madera", 1))
    for k, tx in enumerate((x0 + 1, x0 + 9, x0 + 17)):
        cv.rect(tx, y0 + 38, tx + 7, y0 + 43, K("gris", 6)); cv.rect(tx + 1, y0 + 39, tx + 6, y0 + 42, K("granate", 3 + k % 2))
    cv.px(x0 + 12, y0 + 40, K("papel", 3)); cv.px(x0 + 13, y0 + 40, K("papel", 3))   # una hoja en el baño
    # la puerta, abierta hacia dentro contra la pared izquierda
    cv.rect(x0, y0, x0 + 3, y1, K("gris", 3)); cv.vline(x0 + 3, y0, y1, K("gris", 1)); cv.px(x0 + 2, y0 + 25, K("ocre", 3))


def _juego_te(cv, x, y):
    """Bandeja con tetera, dos tazas y azucarero sobre el mostrador. (x, y) = esquina de la bandeja."""
    cv.rect(x, y, x + 26, y + 12, K("ocre", 2)); cv.frame(x, y, x + 26, y + 12, K("ocre", 1))
    cv.ellipse(x + 2, y - 3, x + 12, y + 8, K("papel", 4), outline=K("papel", 1))     # tetera
    cv.rect(x + 5, y - 5, x + 9, y - 3, K("papel", 3)); cv.px(x + 7, y - 6, K("papel", 2))
    cv.hline(x + 12, x + 15, y + 1, K("papel", 3)); cv.px(x + 15, y, K("papel", 3))   # pitorro
    cv.vline(x + 1, y, y + 5, K("papel", 2))                                         # asa
    cv.hline(x + 4, x + 10, y + 3, K("azul", 3))                                     # filete azul
    for cx in (x + 15, x + 20):                                                      # tazas con su plato
        cv.ellipse(cx - 1, y + 6, cx + 6, y + 11, K("papel", 3))
        cv.ellipse(cx, y + 5, cx + 5, y + 9, K("papel", 4), outline=K("papel", 1)); cv.rect(cx + 1, y + 6, cx + 4, y + 8, K("madera", 2))
    cv.ellipse(x + 18, y - 1, x + 24, y + 4, K("papel", 4), outline=K("papel", 1))   # azucarero


def dibujar(variante=None):
    rnd = random.Random(7)
    cv = Canvas(W, H)
    P.tapa_muro(cv, X0 - 12, WT - 12, X1 + 12, WT)
    if variante == "j12":                                                # el papel ocre, apagado por la noche
        P.papel_pintado(cv, X0, WT, X1, WB, rampa="madera", base=2, motivo="rombo")
    else:
        P.papel_pintado(cv, X0, WT, X1, WB, rampa="ocre", base=1, motivo="rombo")
    # la pared de las fotografías (izquierda y centro)
    for (fx, fy, fw, fh) in [(90, 28, 16, 20), (110, 26, 22, 16), (136, 30, 14, 18), (90, 54, 20, 16), (114, 48, 16, 22),
                             (134, 54, 22, 16), (160, 28, 18, 22), (182, 32, 14, 16), (160, 56, 24, 18), (188, 52, 14, 20),
                             (206, 28, 20, 16), (206, 50, 16, 22)]:
        marco(cv, fx, fy, fw, fh, rnd)
    # cuarto oscuro: puerta con cartel y bombilla roja apagada
    P.puerta(cv, 330, 44, w=30, h=48, rampa="gris", base=2)
    cv.rect(324, 34, 366, 41, K("papel", 3)); cv.text(345 - cv.text_width("NO ENTRAR") // 2, 35, "NO ENTRAR", K("rojo", 3))
    cv.ellipse(341, 24, 349, 32, K("rojo", 4) if variante in ("j6", "j12") else K("granate", 2), outline=K("gris", 1))
    if variante == "j12":
        _cuarto_oscuro(cv, 330, 44, 360, 92)
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
    if variante == "j12":
        _juego_te(cv, 146, 122)
    else:
        cv.rect(150, 122, 170, 132, K("papel", 3))                                                   # sobres
    # la estufa apagada
    cv.rect(360, 120, 384, 160, K("gris", 2)); cv.frame(360, 120, 384, 160, K("gris", 1)); cv.rect(366, 140, 378, 152, K("gris", 0))
    cv.vline(372, 92, 120, K("gris", 3))
    # muros y puerta a la calle
    cv.rect(X0 - 12, WT, X0, FB + 12, K("gris", 3)); cv.rect(X1, WT, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(X0 - 12, FB, 224, FB + 12, K("gris", 3)); cv.rect(256, FB, X1 + 12, FB + 12, K("gris", 3))
    cv.rect(224, FB, 256, FB + 12, K("madera", 2))
    if variante == "j12":
        def oscuridad(x, y):
            if 330 <= x < 360 and 44 <= y < 92:
                return 0                                                     # el cuarto oscuro, en su luz roja
            d = math.hypot(x - 345, (y - 96) * 1.2)
            return -1 if d < 44 else -2
        cv.add_light_fn(oscuridad)
        cv.add_light(240, 26, 312, 86, -1)                                   # los fondos pintados, casi invisibles
        cv.add_emissive(341, 24, 349, 32)
        cv.glow_rgb = K("rojo", 4)
        cv.add_glow_suave(345, 30, 50, 0.4, limite=(X0, WT, X1, FB))
        cv.add_glow_suave(345, 96, 120, 0.3, squash=1.3, limite=(X0, 92, X1, FB))
        cv.bake_lighting()
        return cv
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(200, 120, 140, 0.25, squash=1.3, limite=(X0, WT, X1, FB))
    if variante == "j6":
        cv.add_emissive(341, 24, 349, 32)
        cv.glow_rgb = K("rojo", 4)
        cv.add_glow_suave(345, 30, 40, 0.35, limite=(X0, WT, X1, FB))
    cv.bake_lighting()
    return cv
