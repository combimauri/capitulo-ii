"""P.03 — Ficha de Afiliación del Partido (FichaScene).

Mesa de acero de una oficina de registro del Partido, 1979. La ficha, en papel amarillento (`papel 2`), ocupa casi
toda la mesa: membrete con la pirámide, marco impreso doble, renglones de puntos, recuadro para la fotografía,
taladros de archivador y el sello circular del Ingsoc junto a la firma. A la izquierda, el tampón y el sello de
goma (el APTO está esperando); a la derecha, la boca del tubo neumático, abierta, y la cápsula que se llevará la ficha.

Coordenadas: la escena coloca el papel en P = (170, 14, 620×512) de pantalla → (85, 7)-(395, 263) aquí.
"""
import random

from pixel import Canvas, K
import papel as PP

PX0, PY0, PX1, PY1 = 85, 7, 395, 263


def _r(rx, ry):
    """Coordenadas relativas al papel de la escena (px de pantalla) → px de arte."""
    return PX0 + rx // 2, PY0 + ry // 2


def _tampon(cv, x, y):
    """Caja de lata del tampón, abierta, con la almohadilla roja, y el sello de goma al lado."""
    PP.sombra(cv, x, y, x + 34, y + 22, 2, 2)
    cv.rect(x, y, x + 34, y + 22, K("gris", 3)); cv.frame(x, y, x + 34, y + 22, K("gris", 1))
    cv.hline(x + 1, x + 33, y + 1, K("gris", 5))
    cv.rect(x + 3, y + 3, x + 31, y + 19, K("rojo", 1))
    for yy in range(y + 4, y + 18, 2):
        for xx in range(x + 4 + (yy // 2) % 2, x + 30, 3):
            cv.px(xx, yy, K("rojo", 2))
    cv.hline(x + 4, x + 30, y + 4, K("rojo", 2))
    # la tapa abierta, por encima
    cv.rect(x, y - 10, x + 34, y - 1, K("gris", 4)); cv.frame(x, y - 10, x + 34, y - 1, K("gris", 2))
    cv.hline(x + 1, x + 33, y - 9, K("gris", 6))
    cv.text(x + 5, y - 8, "TINTA", K("gris", 2))
    # sello de goma: mango de madera torneado visto desde arriba, base metálica
    sx, sy = x + 8, y + 32
    PP.sombra(cv, sx - 6, sy - 4, sx + 18, sy + 8, 2, 2)
    cv.rect(sx - 6, sy - 4, sx + 18, sy + 8, K("gris", 5)); cv.frame(sx - 6, sy - 4, sx + 18, sy + 8, K("gris", 2))
    cv.hline(sx - 5, sx + 17, sy - 3, K("gris", 7))
    cv.rect(sx - 4, sy + 5, sx + 16, sy + 8, K("rojo", 2))                    # la goma, entintada
    cv.ellipse(sx, sy - 6, sx + 13, sy + 4, K("madera", 3), outline=K("madera", 1))
    cv.ellipse(sx + 2, sy - 5, sx + 9, sy, K("madera", 5))
    cv.px(sx + 4, sy - 4, K("madera", 6))


def _pluma(cv, x, y):
    """Portaplumas de oficina, con su plumín, tumbado en una bandeja de baquelita."""
    PP.sombra(cv, x, y, x + 52, y + 14, 2, 2)
    cv.rect(x, y, x + 52, y + 14, K("gris", 1)); cv.frame(x, y, x + 52, y + 14, K("gris", 0))
    cv.hline(x + 2, x + 50, y + 2, K("gris", 3)); cv.hline(x + 2, x + 50, y + 11, K("gris", 0))
    # mango
    cv.rect(x + 6, y + 5, x + 36, y + 9, K("azul", 1))
    cv.hline(x + 6, x + 36, y + 5, K("azul", 3)); cv.hline(x + 6, x + 36, y + 8, K("azul", 0))
    cv.rect(x + 36, y + 5, x + 40, y + 9, K("ocre", 2)); cv.hline(x + 36, x + 40, y + 5, K("ocre", 3))
    # plumín
    cv.poly([(x + 40, y + 5), (x + 47, y + 7), (x + 40, y + 8)], K("gris", 7))
    cv.px(x + 46, y + 7, K("gris", 0)); cv.hline(x + 41, x + 46, y + 7, K("gris", 5))


def _fichas_en_blanco(cv, x, y):
    """Un taco de fichas sin rellenar, desalineadas."""
    rnd = random.Random(5)
    for i in range(4):
        dx, dy = rnd.randint(-2, 2), -i * 2
        PP.hoja(cv, x + dx, y + dy, x + dx + 54, y + dy + 70, base=2, semilla=40 + i, muescas=1,
                sombra_mesa=(i == 0))
    tx, ty = x + 2, y - 6
    PP.piramide(cv, tx + 4, ty + 6, 6, K("gris", 3))
    cv.hline(tx + 3, tx + 50, ty + 16, K("rojo", 3))
    for k in range(7):
        cv.hline(tx + 4, tx + 26, ty + 22 + k * 6, K("papel", 1))
        for xx in range(tx + 28, tx + 49, 2):
            cv.px(xx, ty + 23 + k * 6, K("papel", 1))


def _tubo(cv, x, y):
    """Terminal del tubo neumático: la boca de latón empotrada en la mesa, con la tapa abierta y su placa."""
    PP.sombra(cv, x - 2, y - 2, x + 46, y + 40, 3, 3)
    cv.rect(x - 2, y - 2, x + 46, y + 40, K("gris", 2)); cv.frame(x - 2, y - 2, x + 46, y + 40, K("gris", 1))
    cv.hline(x - 1, x + 45, y - 1, K("gris", 4))
    for (a, b) in ((x + 1, y + 1), (x + 41, y + 1), (x + 1, y + 35), (x + 41, y + 35)):   # tornillos
        cv.px(a, b, K("gris", 6)); cv.px(a + 1, b + 1, K("gris", 0))
    cv.ellipse(x + 6, y + 4, x + 38, y + 30, K("ocre", 1))                     # brida de latón
    cv.ellipse(x + 7, y + 5, x + 37, y + 29, K("ocre", 2))
    cv.ellipse(x + 10, y + 8, x + 34, y + 27, K("gris", 0))                    # la boca
    cv.ellipse(x + 12, y + 11, x + 32, y + 26, K("gris", 1))
    cv.ellipse(x + 15, y + 15, x + 29, y + 24, K("gris", 0))
    cv.d.arc([x + 7, y + 5, x + 36, y + 28], 200, 300, fill=K("ocre", 3))
    # la tapa, abierta hacia arriba (vista casi de canto)
    cv.rect(x + 9, y - 10, x + 35, y - 2, K("ocre", 2)); cv.frame(x + 9, y - 10, x + 35, y - 2, K("ocre", 0))
    cv.hline(x + 10, x + 34, y - 9, K("ocre", 3))
    cv.rect(x + 19, y - 3, x + 25, y + 5, K("ocre", 1))                        # bisagra
    # placa
    cv.rect(x + 8, y + 31, x + 36, y + 38, K("papel", 3)); cv.frame(x + 8, y + 31, x + 36, y + 38, K("gris", 3))
    cv.text(x + 11, y + 32, "TUBO 7", K("gris", 2))


def _capsula(cv, x, y):
    """Cápsula del tubo, tumbada: cuerpo de acero, cabezas de fieltro granate y anillo de latón."""
    PP.sombra(cv, x, y, x + 40, y + 12, 2, 3)
    cv.rect(x + 5, y, x + 35, y + 12, K("gris", 6))
    cv.hline(x + 5, x + 35, y + 2, K("gris", 8)); cv.hline(x + 5, x + 35, y + 3, K("gris", 7))
    cv.hline(x + 5, x + 35, y + 10, K("gris", 4)); cv.hline(x + 5, x + 35, y + 11, K("gris", 3))
    for xx in (x, x + 35):
        cv.rect(xx, y + 1, xx + 5, y + 11, K("granate", 3)); cv.frame(xx, y + 1, xx + 5, y + 11, K("granate", 1))
        cv.vline(xx + 1, y + 2, y + 10, K("granate", 5))
    cv.rect(x + 18, y, x + 21, y + 12, K("ocre", 2)); cv.vline(x + 18, y, y + 12, K("ocre", 3))


def dibujar():
    cv = Canvas(480, 270, ("gris", 4))
    PP.chapa(cv, 0, 0, 480, 270, base=4, semilla=3)
    cv.hline(0, 480, 268, K("gris", 2)); cv.hline(0, 480, 269, K("gris", 1))     # canto de la mesa

    # --- izquierda: tampón, sello y pluma; derecha: tubo y cápsula
    _tampon(cv, 26, 40)
    _pluma(cv, 14, 112)
    _fichas_en_blanco(cv, 16, 170)
    _tubo(cv, 418, 34)
    _capsula(cv, 424, 108)
    for (x, y) in ((440, 160), (452, 200), (430, 236)):                       # clips sueltos
        cv.frame(x, y, x + 6, y + 3, K("gris", 7)); cv.px(x + 1, y + 1, K("gris", 7))

    # --- el vade de hule oscuro sobre el que se rellena
    PP.sombra(cv, PX0 - 12, PY0 - 4, PX1 + 12, 270, 2, 2)
    cv.rect(PX0 - 12, PY0 - 4, PX1 + 12, 270, K("tela", 1)); cv.frame(PX0 - 12, PY0 - 4, PX1 + 12, 271, K("tela", 0))
    cv.hline(PX0 - 11, PX1 + 11, PY0 - 3, K("tela", 2))
    for x in (PX0 - 9, PX1 + 8):
        cv.vline(x, PY0, 270, K("tela", 2))

    # --- la ficha
    PP.sombra(cv, PX0, PY0, PX1, PY1, 3, 4, fuerte=2)
    PP.hoja(cv, PX0, PY0, PX1, PY1, base=2, semilla=11, mordidas=0.05, muescas=4, fibra=0.03,
            sombra_mesa=False, amarilleo=2)
    PP.manchas_papel(cv, PX0 + 3, PY0 + 3, PX1 - 3, PY1 - 3, 7, semilla=4, radio=(1, 3))
    # marco impreso doble
    cv.frame(PX0 + 5, PY0 + 5, PX1 - 5, PY1 - 5, K("papel", 0))
    cv.frame(PX0 + 7, PY0 + 7, PX1 - 7, PY1 - 7, K("papel", 1))
    # membrete: la pirámide del ministerio, la sigla y el número de impreso
    PP.piramide(cv, PX0 + 15, PY0 + 16, 12, K("gris", 2))
    PP.texto_c(cv, PX0 + 27, PY0 + 31, "INGSOC", K("gris", 2))
    cv.text(PX1 - 58, PY0 + 14, "IMPRESO A-1", K("papel", 0))
    cv.text(PX1 - 58, PY0 + 21, "REG. 1979", K("papel", 0))
    cv.hline(_r(30, 0)[0], _r(590, 0)[0], _r(0, 88)[1], K("rojo", 3))         # filete rojo bajo el título
    cv.hline(_r(30, 0)[0], _r(590, 0)[0], _r(0, 92)[1], K("rojo", 2))
    # renglones de puntos para cada casilla (las de nombre y apellido llevan su raya de máquina)
    for ry in (176, 218, 248, 280, 332, 372, 408):
        y = _r(0, ry)[1]
        for x in range(_r(30, 0)[0], _r(590, 0)[0], 2):
            cv.px(x, y, K("papel", 1))
    # recuadro de la fotografía, con sus esquineros y una grapa
    fx0, fy0 = _r(518, 98); fx1, fy1 = _r(596, 186)
    cv.rect(fx0, fy0, fx1, fy1, K("papel", 3)); cv.frame(fx0, fy0, fx1, fy1, K("papel", 1))
    for (a, b, sx, sy) in ((fx0, fy0, 1, 1), (fx1 - 1, fy0, -1, 1), (fx0, fy1 - 1, 1, -1), (fx1 - 1, fy1 - 1, -1, -1)):
        for k in range(4):
            cv.px(a + k * sx, b, K("papel", 0)); cv.px(a, b + k * sy, K("papel", 0))
    PP.texto_c(cv, (fx0 + fx1) // 2, (fy0 + fy1) // 2 - 6, "FOTO", K("papel", 1))
    PP.texto_c(cv, (fx0 + fx1) // 2, (fy0 + fy1) // 2 + 1, "4X5", K("papel", 1))
    cv.hline(fx0 + 12, fx0 + 26, fy0 - 2, K("gris", 6)); cv.px(fx0 + 12, fy0 - 1, K("gris", 5)); cv.px(fx0 + 25, fy0 - 1, K("gris", 5))
    # taladros de archivador en el margen izquierdo
    PP.agujeros(cv, PX0 + 4, (PY0 + 50, PY1 - 50), K("gris", 3), K("papel", 0))
    # línea de firma y sello circular del Partido junto a ella
    fx, fy = _r(140, 492)
    cv.hline(fx, fx + 170, fy, K("gris", 2))
    cv.text(fx, fy - 7, "X", K("papel", 0))
    PP.sello_redondo(cv, PX0 + 34, PY1 - 30, 20, K("rojo", 3), "INGSOC", semilla=9, tinta=0.78)

    # la luz de la telepantalla de la oficina, desde arriba a la derecha (fuera de cuadro)
    cv.add_glow_suave(500, -20, 260, 0.16, squash=1.2)
    cv.bake_lighting()
    return cv


def exportar(destino):
    dibujar().img.save(destino / "ficha-fondo.png")
    return ["ficha-fondo.png"]
