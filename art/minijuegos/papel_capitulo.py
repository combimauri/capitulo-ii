"""El Capítulo II (CapituloScene): se compone en la mesa de la cripta de San Clemente y Goldstein lo mecanografía.

- capitulo-fondo: el tablero viejo de la mesa de la cripta, a la luz de cuatro grupos de velas en las esquinas
  (resplandor `ocre`, la paleta más cálida del juego), libros apilados y cera derramada. Abajo, el cuerpo de la
  máquina de escribir de Goldstein.
- capitulo-rodillo: el carro de la máquina (rodillo de caucho, mandos, barra de papel, guía con su escala y las
  bobinas de cinta). Va por encima de la hoja: el papel sale de detrás del rodillo.
- capitulo-hoja: la hoja larga donde se teclea (860×1400 de pantalla), con su sombra translúcida.
- capitulo-tarjeta / capitulo-tarjeta-luz: el papelito de cada opción (nine-slice, 24×24, bordes de 8 px).

Pantalla → arte: la hoja va en x 50…910 (25…455); el texto, hasta y ≈ 490 (245): el rodillo empieza en 488 (244).
"""
import math
import random

from PIL import Image
from pixel import Canvas, K
import papel as PP

ROD_Y = 242                     # y (arte) donde se coloca el sprite del rodillo


def _libros(cv, x, y, rnd):
    """Una pila de libros viejos vista desde arriba (el de encima, abierto de canto)."""
    for k in range(3):
        w, h = 40 - k * 3, 28 - k * 2
        dx, dy = rnd.randint(-2, 2) + k * 2, -k * 3
        c = rnd.choice(["granate", "madera", "tela"])
        if k == 0:
            PP.sombra(cv, x + dx, y + dy, x + dx + w, y + dy + h, 2, 2)
        cv.rect(x + dx, y + dy, x + dx + w, y + dy + h, K(c, 3)); cv.frame(x + dx, y + dy, x + dx + w, y + dy + h, K(c, 1))
        cv.hline(x + dx + 1, x + dx + w - 1, y + dy + 1, K(c, 4))
        cv.rect(x + dx + w - 3, y + dy + 1, x + dx + w - 1, y + dy + h - 1, K("papel", 2))     # el canto de las hojas
        cv.rect(x + dx + 4, y + dy + 4, x + dx + 16, y + dy + 7, K("ocre", 2))                   # tejuelo dorado


def _grupo_velas(cv, x, y, n, rnd):
    llamas = []
    for k in range(n):
        vx, vy = x + rnd.randint(-8, 8), y + rnd.randint(-4, 6)
        llamas.append(PP.vela(cv, vx, vy, alto=rnd.randint(8, 18), ancho=rnd.choice([4, 5, 6])))
    return llamas


def fondo():
    rnd = random.Random(13)
    cv = Canvas(480, 270, ("madera", 1))
    PP.madera_mesa(cv, 0, 0, 480, 270, base=2, semilla=33, tabla=34)
    for _ in range(40):                                                      # gotas de cera de años
        a, b = rnd.randint(0, 479), rnd.randint(0, 269)
        cv.px(a, b, K("papel", 2)); cv.px(a + 1, b, K("papel", 3))
    _libros(cv, -12, 118, rnd)
    _libros(cv, 448, 150, rnd)
    # tintero y una pluma vieja, abajo a la izquierda
    PP.sombra_elipse(cv, 12, 160, 28, 176, 2, 2)
    cv.ellipse(12, 160, 28, 176, K("gris", 2), outline=K("gris", 0))
    cv.ellipse(16, 164, 24, 172, K("azul", 0)); cv.px(17, 165, K("cielo", 5))
    cv.d.line([22, 184, 4, 196], fill=K("madera", 5)); cv.px(23, 183, K("gris", 6))
    llamas = []
    llamas += _grupo_velas(cv, 22, 40, 3, rnd)
    llamas += _grupo_velas(cv, 458, 44, 2, rnd)
    llamas += _grupo_velas(cv, 18, 236, 2, rnd)
    llamas += _grupo_velas(cv, 460, 232, 3, rnd)
    cv.glow_rgb = K("ocre", 4)
    for (lx, ly) in llamas:
        cv.add_glow_suave(lx, ly, 50, 0.32)
        cv.add_glow_suave(lx, ly, 150, 0.14)
    cv.add_light(0, 0, 480, 270, -1)                                         # la mesa, en penumbra…
    for (lx, ly) in llamas:                                                  # …salvo junto a las velas
        PP.luz_radial(cv, lx, ly, [(40, 70, 1), (6, 18, 1)])

    # el cuerpo de la máquina de escribir, abajo en el centro (el carro va en otro sprite)
    cv.rect(70, 258, 410, 270, K("gris", 2)); cv.hline(70, 410, 258, K("gris", 4))
    cv.rect(58, 262, 422, 270, K("gris", 1))
    cv.bake_lighting()
    return cv


def rodillo():
    """El carro: rodillo de caucho negro de punta a punta, mandos a los lados, barra y guía con escala."""
    cv = Canvas(480, 28, ("rojo", 5))                       # rojo 5 = transparente (no se usa en el carro)
    # el cuerpo de la máquina bajo el carro: opaco, para que la hoja no asome por debajo
    cv.rect(18, 14, 462, 28, K("gris", 2)); cv.hline(18, 462, 24, K("gris", 3))
    cv.rect(30, 25, 450, 28, K("gris", 1))
    # bobinas de cinta, debajo, a los lados (asoman)
    for bx in (96, 384):
        cv.ellipse(bx - 14, 16, bx + 15, 36, K("gris", 3), outline=K("gris", 1))
        cv.ellipse(bx - 9, 19, bx + 10, 33, K("rojo", 1))
        cv.ellipse(bx - 3, 23, bx + 4, 29, K("gris", 6))
    cv.rect(110, 20, 370, 24, K("rojo", 1)); cv.hline(110, 370, 20, K("rojo", 2))              # la cinta
    # la guía de la hoja, con su escala
    cv.rect(18, 17, 462, 22, K("gris", 6)); cv.hline(18, 462, 17, K("gris", 8)); cv.hline(18, 462, 21, K("gris", 4))
    for x in range(26, 456, 6):
        cv.vline(x, 18, 20 if (x - 26) % 30 else 21, K("gris", 3))
    cv.rect(236, 16, 244, 23, K("gris", 8)); cv.px(240, 22, K("gris", 2))                      # el punto de escritura
    # el rodillo: un cilindro de caucho negro (luz arriba, sombra abajo)
    filas = [0, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    for k, t in enumerate(filas):
        cv.hline(18, 462, k + 1, K("gris", t))
    for x in range(22, 460, 7):                                                              # el caucho gastado
        cv.px(x, 6 + (x // 7) % 5, K("gris", 2))
    # barra de papel con sus dos rodillitos, por delante
    cv.hline(24, 456, 11, K("gris", 8)); cv.hline(24, 456, 12, K("gris", 5))
    for rx in (130, 350):
        cv.rect(rx - 7, 9, rx + 7, 15, K("gris", 2)); cv.frame(rx - 7, 9, rx + 7, 15, K("gris", 0))
        cv.hline(rx - 6, rx + 6, 10, K("gris", 4))
    # los mandos del rodillo, estriados
    for (x0, x1) in ((1, 18), (462, 479)):
        cv.rect(x0, 0, x1, 19, K("gris", 2)); cv.frame(x0, 0, x1, 19, K("gris", 0))
        for y in range(2, 18, 2):
            cv.hline(x0 + 1, x1 - 1, y, K("gris", 4))
        cv.vline(x0 + 3, 1, 18, K("gris", 6)); cv.vline(x1 - 3, 1, 18, K("gris", 1))
    # palanca de retorno del carro, a la izquierda
    cv.rect(0, 20, 22, 23, K("gris", 6)); cv.hline(0, 22, 20, K("gris", 8))
    return PP.rgba(cv.img, K("rojo", 5))


def hoja():
    """La hoja larga del capítulo: papel viejo de Goldstein, con su sombra translúcida a la derecha."""
    w, h = 430, 700
    cv = Canvas(w + 3, h, ("gris", 0))
    rnd = random.Random(70)
    m = PP.mascara_rect(0, 0, w, h, rnd, mordidas=0.04, muescas=3)
    PP.pintar_hoja(cv, m, base=4, semilla=71, fibra=0.03, tono=lambda x, y: -1 if (x < 3 or x > w - 4) and (x + y) % 3 else 0)
    PP.manchas_papel(cv, 4, 4, w - 4, h - 4, 10, semilla=72, radio=(2, 5))
    g = K("ocre", 4)                                                             # la luz de las velas sobre el papel
    px_ = cv.img.load()
    for (x, y) in m:
        c = px_[x, y]
        px_[x, y] = tuple(int(c[i] * 0.86 + g[i] * 0.14) for i in range(3))
    img = cv.img.convert("RGBA")
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    op, ip = out.load(), img.load()
    for (x, y) in m:
        if 0 <= x + 3 < w + 3:
            op[x + 3, min(h - 1, y + 3)] = (11, 12, 15, 110)
    for (x, y) in m:
        op[x, y] = ip[x, y]
    return out


def tarjeta(base=3):
    """Papelito para cada opción: nine-slice 24×24 con bordes de 8 px. Plano por dentro (se estira sin manchas):
    canto `papel 0`, filo de luz arriba a la izquierda, filo de sombra abajo a la derecha y esquinas romas."""
    cv = Canvas(24, 24, ("gris", 0))
    cv.rect(0, 0, 24, 24, K("papel", base))
    cv.frame(0, 0, 24, 24, K("papel", 0))
    cv.hline(1, 23, 1, K("papel", base + 1)); cv.vline(1, 1, 23, K("papel", base + 1))
    cv.hline(1, 23, 22, K("papel", base - 1)); cv.vline(22, 1, 23, K("papel", base - 1))
    for (x, y) in ((0, 0), (23, 0), (0, 23), (23, 23)):
        cv.px(x, y, K("gris", 0))
    for (x, y) in ((1, 1), (22, 1), (1, 22), (22, 22)):
        cv.px(x, y, K("papel", 0))
    return PP.rgba(cv.img)


def exportar(destino):
    fondo().img.save(destino / "capitulo-fondo.png")
    rodillo().save(destino / "capitulo-rodillo.png")
    hoja().save(destino / "capitulo-hoja.png")
    tarjeta(3).save(destino / "capitulo-tarjeta.png")
    tarjeta(4).save(destino / "capitulo-tarjeta-luz.png")
    return ["capitulo-fondo.png", "capitulo-rodillo.png", "capitulo-hoja.png", "capitulo-tarjeta.png",
            "capitulo-tarjeta-luz.png"]
