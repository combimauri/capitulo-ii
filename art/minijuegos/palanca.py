"""J8.03 — La palanca del montacargas viejo del Miniver.

Dentro de la cabina, mirando a la reja de tijera. Por la reja se ve el hueco (ladrillo, forjados y las
puertas de cada planta con una raya de luz por debajo), que en el juego se desplaza al subir.
Delante, la placa de latón con la ranura graduada de S a 11 y la palanca gastada.

Piezas (todas a la resolución del pixel art; el juego las muestra a 2x):
  palanca-fondo   480x270  cabina, con el hueco de la reja transparente
  palanca-reja    360x198  la reja de tijera (va encima del hueco y debajo de la cabina)
  palanca-hueco   360x120  una planta del hueco, en mosaico vertical
  palanca-mango    54x24   la palanca (el centro de la imagen es el centro de la ranura)
"""
import random

from _base import CLAVE, Canvas, K, a_rgba, guardar, sprite, texto_escalado, ancho_escalado

W, H = 480, 270
HUECO = (60, 38, 420, 236)            # en el arte; en el juego (120, 76) - (840, 472)
PLACA = (200, 50, 280, 230)
RANURA = (236, 62, 244, 218)          # en el juego x 472-488, y 124-436 (RIEL 140..420 + margen)
ARRIBA, ABAJO = 70, 210               # RIEL.arriba / RIEL.abajo a la mitad
PLANTAS = 11


def _tablas_verticales(cv, x0, y0, x1, y1, semilla):
    rnd = random.Random(semilla)
    cv.rect(x0, y0, x1, y1, K("madera", 2))
    x = x0
    while x < x1:
        w = rnd.choice([9, 10, 11])
        b = rnd.choice([2, 2, 3])
        cv.rect(x, y0, min(x + w, x1), y1, K("madera", b))
        cv.vline(x, y0, y1, K("madera", 0))
        cv.vline(x + 1, y0, y1, K("madera", b + 1))
        for _ in range(3):                                    # vetas
            gy = rnd.randint(y0 + 4, y1 - 12)
            cv.vline(x + rnd.randint(3, max(3, w - 3)), gy, gy + rnd.randint(5, 14), K("madera", b - 1))
        for yy in (y0 + 6, y1 - 30):                          # clavos
            cv.px(x + w // 2, yy, K("gris", 6))
        x += w


def _chapa_lagrimada(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, K("gris", 2))
    for y in range(y0 + 2, y1, 6):
        for x in range(x0 + 1 + (y // 6 % 2) * 4, x1 - 1, 8):
            cv.hline(x, x + 3, y, K("gris", 3)); cv.px(x + 1, y - 1, K("gris", 4))
    cv.hline(x0, x1, y0, K("gris", 4)); cv.hline(x0, x1, y0 + 1, K("gris", 1))


def fondo():
    cv = Canvas(W, H, bg=("gris", 1))
    hx0, hy0, hx1, hy1 = HUECO
    # techo de tablas y viga
    cv.rect(0, 0, W, hy0, K("madera", 1))
    for y in range(2, hy0 - 6, 5):
        cv.hline(0, W, y, K("madera", 0)); cv.hline(0, W, y + 1, K("madera", 2))
    cv.rect(0, hy0 - 8, W, hy0, K("gris", 3)); cv.hline(0, W, hy0 - 8, K("gris", 5)); cv.hline(0, W, hy0 - 1, K("gris", 1))
    for x in range(8, W, 24):
        cv.px(x, hy0 - 5, K("gris", 6)); cv.px(x, hy0 - 4, K("gris", 2))
    # paredes laterales de tablas
    _tablas_verticales(cv, 0, hy0, hx0, hy1, 3)
    _tablas_verticales(cv, hx1, hy0, W, hy1, 8)
    for x0, x1 in ((0, hx0), (hx1, W)):                       # chapa de rozaduras abajo
        cv.rect(x0, hy1 - 22, x1, hy1, K("gris", 3)); cv.hline(x0, x1, hy1 - 22, K("gris", 5))
        for x in range(x0 + 4, x1, 12):
            cv.px(x, hy1 - 19, K("gris", 6))
    # marco de la reja
    cv.rect(hx0 - 4, hy0, hx0, hy1, K("gris", 3)); cv.vline(hx0 - 4, hy0, hy1, K("gris", 5))
    cv.rect(hx1, hy0, hx1 + 4, hy1, K("gris", 3)); cv.vline(hx1 + 3, hy0, hy1, K("gris", 1))
    # suelo de chapa lagrimada, con polvo y una colilla
    _chapa_lagrimada(cv, 0, hy1, W, H)
    rnd = random.Random(4)
    for _ in range(90):
        cv.px(rnd.randint(0, W - 1), rnd.randint(hy1 + 3, H - 1), K("gris", rnd.choice([3, 4])))
    cv.rect(352, 246, 357, 248, K("papel", 3)); cv.px(357, 246, K("ocre", 1)); cv.px(357, 247, K("gris", 4))
    # el hueco de la reja: transparente (aquí, color clave)
    cv.rect(hx0, hy0, hx1, hy1, CLAVE)

    # aviso de carga en la pared izquierda
    cv.rect(13, 71, 49, 99, K("gris", 0))
    cv.rect(12, 70, 48, 98, K("papel", 2)); cv.frame(12, 70, 48, 98, K("papel", 0))
    for i, t in enumerate(("CARGA", "MAX.", "500 KG")):
        cv.text(30 - cv.text_width(t) // 2, 74 + i * 7, t, K("gris", 2))
    cv.px(30, 71, K("gris", 5))
    # marcas de alguien que contaba viajes, rayadas en la madera de la derecha
    for g in range(4):
        gx = 432 + g * 10
        for k in range(4):
            cv.vline(gx + k * 2, 112, 121, K("madera", 5))
        cv.d.line([(gx - 1, 119), (gx + 7, 113)], fill=K("madera", 5))
    for k in range(3):
        cv.vline(432 + k * 2, 126, 135, K("madera", 5))
    # timbre de alarma de latón
    cv.rect(446, 60, 462, 76, K("ocre", 0)); cv.rect(447, 61, 461, 75, K("ocre", 1))
    cv.ellipse(450, 64, 459, 73, K("rojo", 2)); cv.px(452, 66, K("rojo", 4))

    # indicador de planta (el texto lo pone el juego)
    cv.rect(190, 4, 290, 33, K("ocre", 0)); cv.rect(192, 6, 288, 31, K("ocre", 2))
    cv.hline(192, 288, 6, K("ocre", 3)); cv.rect(195, 9, 285, 28, K("gris", 0))
    cv.hline(195, 285, 9, K("gris", 1))
    for x in (194, 286):
        cv.px(x, 8, K("ocre", 4)); cv.px(x, 29, K("ocre", 1))
    cv.add_emissive(195, 9, 285, 28)
    # bombilla en su jaula
    bx = 392
    cv.vline(bx, 0, 6, K("gris", 1))
    cv.ellipse(bx - 4, 6, bx + 5, 17, K("ocre", 4)); cv.px(bx - 1, 9, K("papel", 4))
    for k in (-4, -1, 2, 4):
        cv.vline(bx + k, 6, 17, K("gris", 2))
    cv.hline(bx - 4, bx + 5, 11, K("gris", 2)); cv.hline(bx - 3, bx + 4, 17, K("gris", 2))
    cv.add_emissive(bx - 3, 7, bx + 4, 16)

    # la placa de latón, sobre un pie
    px0, py0, px1, py1 = PLACA
    cv.rect(232, py1, 248, hy1 + 4, K("gris", 2)); cv.vline(233, py1, hy1 + 4, K("gris", 4))
    cv.rect(226, hy1 + 2, 254, hy1 + 6, K("gris", 3)); cv.hline(226, 254, hy1 + 2, K("gris", 5))
    cv.rect(px0 + 3, py0 + 3, px1 + 3, py1 + 3, K("gris", 0))                     # sombra 2-3 px
    cv.rect(px0, py0, px1, py1, K("ocre", 0))
    cv.rect(px0 + 1, py0 + 1, px1 - 1, py1 - 1, K("ocre", 2))
    cv.hline(px0 + 1, px1 - 1, py0 + 1, K("ocre", 3)); cv.vline(px0 + 1, py0 + 1, py1 - 1, K("ocre", 3))
    cv.hline(px0 + 1, px1 - 1, py1 - 2, K("ocre", 1)); cv.vline(px1 - 2, py0 + 1, py1 - 1, K("ocre", 1))
    rnd = random.Random(9)
    for _ in range(70):                                                             # pátina
        cv.px(rnd.randint(px0 + 3, px1 - 4), rnd.randint(py0 + 3, py1 - 4), K("ocre", 1))
    # el latón brillante donde se apoyan las manos, a la derecha de la ranura
    cv.rect(246, 64, 253, 216, K("ocre", 3)); cv.vline(248, 66, 214, K("ocre", 4))
    for (sx, sy) in ((px0 + 4, py0 + 4), (px1 - 6, py0 + 4), (px0 + 4, py1 - 6), (px1 - 6, py1 - 6)):
        cv.rect(sx, sy, sx + 3, sy + 3, K("ocre", 1)); cv.px(sx + 1, sy + 1, K("ocre", 3)); cv.hline(sx, sx + 3, sy + 1, K("ocre", 0))
    t = "MONTACARGAS"
    cv.text(240 - cv.text_width(t) // 2 + 1, 53, t, K("ocre", 3))
    cv.text(240 - cv.text_width(t) // 2, 52, t, K("ocre", 0))
    # la ranura
    rx0, ry0, rx1, ry1 = RANURA
    cv.rect(rx0 - 1, ry0 - 1, rx1 + 1, ry1 + 1, K("ocre", 0))
    cv.rect(rx0, ry0, rx1, ry1, K("gris", 0)); cv.vline(rx1 - 1, ry0, ry1, K("gris", 1))
    cv.hline(rx0 - 1, rx1 + 1, ry1 + 1, K("ocre", 4))
    # escala grabada: S, 1 ... 11
    for k in range(PLANTAS + 1):
        y = round(ARRIBA + k * (ABAJO - ARRIBA) / PLANTAS)
        largo = 7 if k in (0, PLANTAS) else 5
        cv.hline(233 - largo, 233, y, K("ocre", 0)); cv.hline(233 - largo, 233, y + 1, K("ocre", 3))
        s = "S" if k == 0 else str(k)
        if k in (0, PLANTAS):
            w = ancho_escalado(s)
            texto_escalado(cv, 224 - w + 1, y - 4, s, K("ocre", 3))
            texto_escalado(cv, 224 - w, y - 5, s, K("ocre", 0))
        else:
            w = cv.text_width(s)
            cv.text(226 - w + 1, y - 1, s, K("ocre", 3))
            cv.text(226 - w, y - 2, s, K("ocre", 0))

    # luz: la bombilla calienta la cabina; más oscuro abajo a la izquierda
    cv.add_light_fn(lambda x, y: -1 if y > 258 else 0)
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(bx, 12, 260, 0.2, squash=1.3)
    mascara = [(x, y) for y in range(H) for x in range(W) if cv.img.getpixel((x, y)) == CLAVE]
    cv.bake_lighting()
    for x, y in mascara:
        cv.img.putpixel((x, y), CLAVE)
    return a_rgba(cv)


def reja():
    hx0, hy0, hx1, hy1 = HUECO
    w, h = hx1 - hx0, hy1 - hy0
    cv = sprite(w, h)
    paso = 30
    # tijeras: aspas entre cada par de pletinas
    for x in range(0, w, paso):
        for y in range(-paso, h + paso, paso):
            for (a, b) in (((x, y), (x + paso, y + paso)), ((x + paso, y), (x, y + paso))):
                cv.d.line([a, b], fill=K("gris", 2), width=3)
    for x in range(0, w, paso):
        for y in range(-paso, h + paso, paso):
            cv.d.line([(x + 1, y), (x + paso + 1, y + paso)], fill=K("gris", 5))
            cv.d.line([(x + paso, y + 1), (x + 1, y + paso)], fill=K("gris", 4))
            cx, cy = x + paso // 2, y + paso // 2                    # remache del aspa
            cv.rect(cx - 1, cy - 1, cx + 2, cy + 2, K("gris", 6)); cv.px(cx - 1, cy - 1, K("gris", 8))
    # pletinas verticales
    for x in range(0, w + 1, paso):
        x0 = min(max(0, x - 2), w - 4)
        cv.rect(x0, 0, x0 + 4, h, K("gris", 4)); cv.vline(x0, 0, h, K("gris", 6)); cv.vline(x0 + 3, 0, h, K("gris", 2))
        for y in range(paso // 2, h, paso):
            cv.px(x0 + 1, y, K("gris", 8)); cv.px(x0 + 2, y, K("gris", 3))
    # carriles de arriba y de abajo
    for y0 in (0, h - 7):
        cv.rect(0, y0, w, y0 + 7, K("gris", 3)); cv.hline(0, w, y0, K("gris", 5)); cv.hline(0, w, y0 + 6, K("gris", 1))
        for x in range(6, w, 15):
            cv.px(x, y0 + 3, K("gris", 6))
    # el tirador de la reja, de latón
    cv.rect(w - 22, 90, w - 16, 116, K("ocre", 0)); cv.rect(w - 21, 91, w - 17, 115, K("ocre", 2))
    cv.vline(w - 21, 92, 114, K("ocre", 3))
    return a_rgba(cv)


def hueco():
    w, h = HUECO[2] - HUECO[0], 120
    rnd = random.Random(21)
    cv = Canvas(w, h, bg=("gris", 1))
    # ladrillo ennegrecido
    for fila, y in enumerate(range(0, 100, 5)):
        off = (fila % 2) * 6
        for x in range(-off, w, 12):
            b = rnd.choice([0, 1, 1, 1, 2])
            cv.rect(max(0, x + 1), y + 1, min(w, x + 11), y + 5, K("granate", b))
            if b and rnd.random() < 0.3:
                cv.hline(max(0, x + 1), min(w, x + 11), y + 1, K("granate", b + 1))
    # forjado de hormigón
    cv.rect(0, 100, w, h, K("gris", 3)); cv.hline(0, w, 100, K("gris", 5)); cv.hline(0, w, 101, K("gris", 4))
    cv.hline(0, w, h - 1, K("gris", 1))
    for _ in range(40):
        cv.px(rnd.randint(0, w - 1), rnd.randint(103, h - 2), K("gris", rnd.choice([2, 4])))
    # puerta de la planta, cerrada, con luz por debajo
    dx0, dx1 = 34, 124
    cv.rect(dx0 - 5, 18, dx1 + 5, 100, K("gris", 2)); cv.frame(dx0 - 5, 18, dx1 + 5, 100, K("gris", 3))
    cv.rect(dx0, 22, dx1, 99, K("madera", 1))
    for x in range(dx0, dx1, 10):
        cv.vline(x, 22, 99, K("madera", 0)); cv.vline(x + 1, 22, 99, K("madera", 2))
    cv.rect(dx0, 56, dx1, 60, K("madera", 2)); cv.hline(dx0, dx1, 59, K("madera", 0))
    cv.hline(dx0 + 2, dx1 - 2, 99, K("ocre", 3)); cv.hline(dx0 + 6, dx1 - 6, 100, K("ocre", 2))
    cv.add_emissive(dx0 + 2, 99, dx1 - 2, 101)
    # guías del montacargas
    for gx in (8, w - 14):
        cv.rect(gx, 0, gx + 6, h, K("gris", 2)); cv.vline(gx + 1, 0, h, K("gris", 4))
        for y in range(10, h, 30):
            cv.px(gx + 3, y, K("gris", 6))
    # cables de contrapeso
    for cx in (290, 296):
        cv.vline(cx, 0, 100, K("gris", 4)); cv.vline(cx + 1, 0, 100, K("gris", 2))
    cv.glow_rgb = K("ocre", 3)
    cv.add_glow_suave(79, 104, 80, 0.18, squash=3.0)
    cv.bake_lighting()
    return cv.img


def mango():
    cv = sprite(54, 24)
    # carro que corre por la ranura
    cv.rect(22, 5, 32, 19, K("gris", 1)); cv.rect(23, 6, 31, 18, K("gris", 3)); cv.hline(23, 31, 6, K("gris", 5))
    cv.px(25, 8, K("gris", 6)); cv.px(29, 16, K("gris", 6))
    # brazo de latón
    cv.rect(16, 9, 45, 16, K("ocre", 0))
    cv.rect(17, 10, 44, 15, K("ocre", 2)); cv.hline(17, 44, 10, K("ocre", 4)); cv.hline(17, 44, 11, K("ocre", 3))
    cv.hline(17, 44, 14, K("ocre", 1))
    cv.rect(13, 8, 18, 17, K("ocre", 0)); cv.rect(14, 9, 17, 16, K("ocre", 1)); cv.vline(14, 9, 16, K("ocre", 3))   # contera
    # pomo, gastado por las manos
    cv.ellipse(40, 5, 54, 19, K("ocre", 0))
    cv.ellipse(41, 6, 53, 18, K("ocre", 2))
    cv.ellipse(42, 7, 50, 15, K("ocre", 3))
    cv.rect(44, 8, 47, 10, K("ocre", 4)); cv.px(44, 11, K("ocre", 4))
    cv.hline(44, 51, 17, K("ocre", 1))
    return a_rgba(cv)


def exportar(destino):
    return [guardar(fondo(), destino, "palanca-fondo"), guardar(reja(), destino, "palanca-reja"),
            guardar(hueco(), destino, "palanca-hueco"), guardar(mango(), destino, "palanca-mango")]
