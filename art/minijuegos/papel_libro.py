"""El libro de Goldstein (LibroScene): un fajo de hojas mecanografiadas, cosidas con hilo, leído a la luz de una vela.

Guion J8.08: «un fajo de hojas mecanografiadas, cosidas con hilo» que sale del hueco de los ladrillos. Sobre la mesa
del sótano de La Campana: la encuadernación vieja (unas tapas de cartón forradas de tela granate, gastadas hasta el
cartón en las esquinas), el canto de las hojas de debajo, el hilo que cose el fajo por el margen y, a la derecha,
la vela en su platillo. La luz de vela calienta la hoja por la derecha y oscurece un paso todo lo demás (biblia §4.2).

La hoja de encima tiene tres variantes (manchas, una quemadura, una esquina rota): la escena alterna una por página.

Pantalla → arte: HOJA (130, 20, 700×470) → (65, 10)-(415, 245). Agujeros del hilo: x 144, y 100 + 100·k → (72, 50 + 50·k).
"""
import math
import random

from pixel import Canvas, K
import papel as PP

HX0, HY0, HX1, HY1 = 65, 10, 415, 245
VELA = (450, 132)                                   # base de la vela
AGUJEROS = [50, 100, 150, 200]


def _ladrillo(cv, x, y):
    """El ladrillo suelto del escondite, apartado sobre la mesa, con mortero viejo pegado."""
    PP.sombra(cv, x, y, x + 34, y + 16, 3, 3)
    cv.rect(x, y, x + 34, y + 16, K("granate", 3)); cv.frame(x, y, x + 34, y + 16, K("granate", 1))
    cv.hline(x + 1, x + 33, y + 1, K("granate", 5)); cv.vline(x + 1, y + 1, y + 15, K("granate", 4))
    rnd = random.Random(2)
    for _ in range(26):
        cv.px(rnd.randint(x + 2, x + 31), rnd.randint(y + 3, y + 13), K("granate", rnd.choice([2, 4])))
    for xx in range(x + 2, x + 14):                                               # mortero
        cv.px(xx, y + 14 - (xx % 3 == 0), K("papel", 1))
    cv.rect(x + 26, y + 2, x + 32, y + 6, K("papel", 1))


def _taza(cv, x, y):
    """Taza de lata desconchada."""
    PP.sombra_elipse(cv, x - 10, y - 10, x + 11, y + 11, 3, 3)
    cv.ellipse(x - 10, y - 10, x + 11, y + 11, K("gris", 6), outline=K("gris", 2))
    cv.ellipse(x - 8, y - 8, x + 9, y + 9, K("gris", 2))
    cv.ellipse(x - 6, y - 6, x + 6, y + 6, K("madera", 1))                          # té frío
    cv.rect(x + 10, y - 3, x + 15, y + 3, K("gris", 5)); cv.rect(x + 11, y - 1, x + 14, y + 1, K("madera", 2))
    for (a, b) in ((x - 9, y + 2), (x + 4, y - 10), (x + 8, y + 6)):              # desconchones
        cv.px(a, b, K("gris", 0)); cv.px(a + 1, b, K("gris", 1))


def _cerillas_quemadas(cv, x, y):
    for k, (dx, dy, L) in enumerate(((0, 0, 12), (4, 6, 10), (-2, 11, 9))):
        cv.hline(x + dx, x + dx + L, y + dy, K("madera", 5))
        cv.hline(x + dx + L - 3, x + dx + L, y + dy, K("gris", 1))
        cv.px(x + dx + L, y + dy, K("gris", 0))


def _vela(cv):
    x, y = VELA
    PP.sombra_elipse(cv, x - 14, y - 7, x + 15, y + 8, 2, 3)
    cv.ellipse(x - 14, y - 7, x + 15, y + 8, K("gris", 5), outline=K("gris", 2))       # platillo de lata
    cv.ellipse(x - 11, y - 5, x + 12, y + 6, K("gris", 4))
    cv.d.arc([x - 14, y - 7, x + 15, y + 8], 190, 280, fill=K("gris", 7))
    for (a, b) in ((x - 9, y + 2), (x + 6, y + 3), (x + 8, y - 3)):                   # goterones de cera
        cv.ellipse(a, b, a + 4, b + 3, K("papel", 3))
    PP.vela(cv, x, y, alto=22, ancho=7)
    cv.vline(x + 2, y - 18, y - 9, K("papel", 4)); cv.px(x + 3, y - 10, K("papel", 4))  # chorreón de cera
    cv.px(x + 3, y - 9, K("papel", 4))


def dibujar(variante=0):
    rnd = random.Random(31)
    cv = Canvas(480, 270, ("madera", 1))
    PP.madera_mesa(cv, 0, 0, 480, 270, base=3, semilla=12, tabla=26)
    # gotas de cera de otras noches, marcas de navaja
    for _ in range(14):
        a, b = rnd.randint(420, 478), rnd.randint(40, 260)
        cv.px(a, b, K("papel", 2)); cv.px(a + 1, b, K("papel", 3))
    for _ in range(4):
        a, b = rnd.randint(4, 50), rnd.randint(10, 260)
        cv.d.line([a, b, a + rnd.randint(4, 9), b + rnd.randint(-2, 2)], fill=K("madera", 0))
    _ladrillo(cv, 12, 196)
    _taza(cv, 30, 34)
    _cerillas_quemadas(cv, 16, 118)
    _vela(cv)

    # --- la encuadernación vieja: tapas de cartón forradas de tela
    t0, t1, t2, t3 = HX0 - 8, HY0 - 6, HX1 + 9, HY1 + 9
    PP.sombra(cv, t0, t1, t2, t3, 3, 3)
    cv.rect(t0, t1, t2, t3, K("granate", 2)); cv.frame(t0, t1, t2, t3, K("granate", 0))
    cv.hline(t0 + 1, t2 - 1, t1 + 1, K("granate", 3)); cv.vline(t0 + 1, t1 + 1, t3 - 1, K("granate", 3))
    for y in range(t1 + 2, t3 - 1, 2):                                                    # trama de la tela
        for x in range(t0 + 2 + (y // 2) % 2, t2 - 1, 3):
            cv.px(x, y, K("granate", 1))
    for (cx, cy, sx, sy) in ((t0, t1, 1, 1), (t2 - 1, t1, -1, 1), (t0, t3 - 1, 1, -1), (t2 - 1, t3 - 1, -1, -1)):
        for k in range(5):                                                                 # esquinas: el cartón al aire
            for j in range(5 - k):
                cv.px(cx + j * sx, cy + k * sy, K("madera", 3) if (j + k) > 1 else K("madera", 4))
    for y in range(t1 + 6, t3 - 6, 9):                                                     # lomo cosido, a la izquierda
        cv.rect(t0 + 1, y, t0 + 5, y + 4, K("granate", 1))
    # hojas de debajo, desalineadas
    for k, (dx, dy, b) in enumerate(((5, 5, 1), (3, 4, 2), (1, 2, 2))):
        PP.hoja(cv, HX0 + dx, HY0 + dy, HX1 + dx, HY1 + dy, base=b, semilla=70 + k, muescas=2, sombra_mesa=False)

    # --- la hoja de encima
    rv = random.Random(100 + variante)
    m = PP.mascara_rect(HX0, HY0, HX1, HY1, rv, mordidas=0.05, muescas=3)
    if variante == 1:                                                                      # esquina arrancada
        for y in range(HY0, HY0 + 16):
            for x in range(HX1 - 22 + (y - HY0) + rv.randint(0, 2), HX1):
                m.discard((x, y))
    if variante == 2:                                                                      # quemadura en la esquina de abajo
        for y in range(HY1 - 24, HY1):
            for x in range(HX0, HX0 + 28):
                if math.hypot(x - HX0, (y - HY1) * 1.2) < 16 + rv.random() * 2.5:
                    m.discard((x, y))
    PP.pintar_hoja(cv, m, base=3, semilla=200 + variante, fibra=0.03)
    if variante == 2:
        for (x, y) in list(m):
            d = math.hypot(x - HX0, (y - HY1) * 1.2)
            if d < 25:
                n = rv.random() * 1.5
                cv.px(x, y, K("madera", 0) if d < 18.5 + n else K("madera", 2) if d < 20 + n else
                      K("ocre", 1) if d < 21.5 + n else K("papel", 1) if d < 23.5 + n else K("papel", 2))
    PP.manchas_papel(cv, HX0 + 4, HY0 + 4, HX1 - 4, HY1 - 4, 8 + variante * 3, semilla=300 + variante, radio=(2, 7))
    if variante == 0:                                                                      # cerco de una taza
        aro = set()
        for a in range(0, 360, 2):
            if not 40 < a < 80:
                aro.add((int(round(330 + math.cos(math.radians(a)) * 15)), int(round(48 + math.sin(math.radians(a)) * 13))))
        for (x, y) in aro:
            PP.desplazar(cv, x, y, x + 1, y + 1, -1)
    if variante == 1:                                                                      # gota de cera sobre el texto
        cv.ellipse(300, 196, 306, 201, K("papel", 4)); cv.px(301, 197, K("papel", 4))
    PP.desplazar(cv, HX0 + 2, (HY0 + HY1) // 2 + 1, HX1 - 2, (HY0 + HY1) // 2 + 2, -1, prob=0.5, rnd=rv, solo=("papel",))  # estuvo doblado

    # el hilo: entra por cada agujero y abraza el lomo
    for y in AGUJEROS:
        cv.ellipse(70, y - 2, 75, y + 3, K("papel", 0))
        cv.px(72, y, K("madera", 0)); cv.px(73, y, K("madera", 0))
        cv.d.line([72, y, HX0 - 4, y - 2], fill=K("granate", 4))
        cv.d.line([72, y + 1, HX0 - 4, y + 3], fill=K("granate", 3))
        cv.px(73, y - 1, K("granate", 5))

    # --- luz de vela: resplandor ámbar pequeño e intenso; −1 en el resto de la escena
    fx, fy = VELA[0], VELA[1] - 25
    cv.glow_rgb = K("ocre", 4)
    cv.add_glow_suave(fx, fy, 70, 0.30, squash=1.0)
    cv.add_glow_suave(fx, fy, 240, 0.10, squash=1.0)
    PP.luz_radial(cv, fx, fy, [(250, 380, -1), (400, 470, -1), (14, 30, 1)], squash=1.1)
    cv.bake_lighting()
    return cv


def exportar(destino):
    hechos = []
    for v in range(3):
        cv = dibujar(v)
        if v == 0:
            cv.img.save(destino / "libro-fondo.png"); hechos.append("libro-fondo.png")
        PP.recorte(cv, HX0, HY0, HX1, HY1).save(destino / f"libro-hoja-{v}.png"); hechos.append(f"libro-hoja-{v}.png")
    return hechos
