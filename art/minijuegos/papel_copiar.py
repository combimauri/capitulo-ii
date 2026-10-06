"""Copiar la Planilla Azul a mano (CopiarScene), en la mesa de lectura del Archivo Restringido (planta 11).

Mesa vieja de madera con polvo (menos donde se ha apoyado alguien), una sola bombilla encima. A la izquierda, la
carpeta azul abierta con la Planilla de Impactos: papel azul pálido (`cielo 6`), la tabla impresa con su cabecera de
columnas y sus filetes, el bloque del pie con la pirámide del Minipax y el sello ALTO SECRETO. A la derecha, el
cuaderno donde se copia: tapas negras, renglones `cielo 5` y margen.

Pantalla → arte: planilla (20, 60, 600×440) → (10, 30)-(310, 250); filas de texto en y = 80 + 34·i (17 px VT323,
6,8 px por carácter). Cuaderno (636, 60, 304×440) → (318, 30)-(470, 250); renglones en y = 92 + 24·k; margen x = 670.
"""
import random

from pixel import Canvas, K
import papel as PP

PL = (10, 24, 310, 250)           # la planilla (se alarga hacia arriba para la cabecera de columnas)
CU = (318, 30, 470, 250)
FILAS = [(80 + 34 * i) // 2 for i in range(8)]                 # y (arte) de cada línea copiable
COLUMNAS = [(7.5, "BAT."), (27, "ORIGEN"), (47.5, "OBJETIVO"), (56, "CUADR"), (65, "FECHA"), (72, "HORA"), (None, "CARGA")]
INICIOS = [0, 9, 28, 49, 57, 66, 73]                            # carácter donde empieza cada columna


def _x_car(c):
    return int((32 + c * 6.8) / 2)


def dibujar():
    rnd = random.Random(8)
    cv = Canvas(480, 270, ("madera", 2))
    PP.madera_mesa(cv, 0, 0, 480, 270, base=3, semilla=21, tabla=30, vertical=False)
    # polvo de años sobre la mesa
    for _ in range(900):
        x, y = rnd.randint(0, 479), rnd.randint(0, 269)
        if not (40 < x < 440 and 40 < y < 250):
            cv.px(x, y, K("madera", 5) if rnd.random() < 0.7 else K("papel", 1))

    # la bombilla, encima de la mesa: un charco de luz y los bordes en penumbra (solo la mesa; los papeles, parejos)
    PP.luz_radial(cv, 240, 135, [(150, 230, -1), (240, 300, -1), (0, 90, 1)], squash=1.5)
    cv.bake_lighting()
    cv.light = [[0] * cv.w for _ in range(cv.h)]

    # --- la carpeta azul, abierta debajo de la planilla
    f0, f1, f2, f3 = PL[0] - 6, PL[1] - 3, PL[2] + 5, 266
    PP.sombra(cv, f0, f1, f2, f3, 3, 3)
    cv.rect(f0, f1, f2, f3, K("azul", 2)); cv.frame(f0, f1, f2, f3, K("azul", 0))
    cv.hline(f0 + 1, f2 - 1, f1 + 1, K("azul", 3)); cv.vline(f0 + 1, f1 + 1, f3 - 1, K("azul", 3))
    for y in range(f1 + 3, f3 - 2, 3):
        for x in range(f0 + 2 + (y % 2), f2 - 2, 4):
            cv.px(x, y, K("azul", 1))
    cv.rect(f0 + 16, f3 - 10, f0 + 76, f3 - 2, K("papel", 3)); cv.frame(f0 + 16, f3 - 10, f0 + 76, f3 - 2, K("azul", 0))
    cv.text(f0 + 19, f3 - 8, "S. 18 - 84", K("azul", 1))

    # --- la planilla
    x0, y0, x1, y1 = PL
    PP.hoja(cv, x0, y0, x1, y1, rampa="cielo", base=6, semilla=33, mordidas=0.03, muescas=1, fibra=0.03,
            sombra_mesa=False)
    # cabecera de columnas impresa sobre una banda
    cv.rect(x0 + 2, y0 + 2, x1 - 2, FILAS[0] - 4, K("cielo", 5))
    for (c, nombre), ini in zip(COLUMNAS, INICIOS):
        cv.text(_x_car(ini), y0 + 4, nombre, K("azul", 1))
    # filetes de la tabla: horizontales entre filas, verticales entre columnas (solo en las cinco baterías)
    for i in range(6):
        cv.hline(x0 + 3, x1 - 3, FILAS[i] - 3, K("cielo", 4))
    cv.hline(x0 + 3, x1 - 3, FILAS[5] - 1, K("cielo", 4))
    for c, _ in COLUMNAS[:-1]:
        cv.vline(_x_car(c), y0 + 2, FILAS[5] - 2, K("cielo", 4))
    for i in (6, 7, 8):
        for x in range(x0 + 6, x1 - 6, 2):
            cv.px(x, FILAS[i - 1] + 14 if i < 8 else FILAS[7] + 14, K("cielo", 5))
    # el pie impreso: pirámide, ministerio, título y sello
    by = 186
    cv.hline(x0 + 6, x1 - 6, by - 4, K("azul", 1))
    PP.piramide(cv, x0 + 8, by + 4, 9, K("azul", 1))
    PP.texto_c(cv, x0 + 17, by + 15, "MINIPAX", K("azul", 1))
    cv.text(x0 + 40, by + 3, "DIRECCION DE MORAL INTERIOR", K("azul", 1))
    cv.text(x0 + 40, by + 11, "PLANILLA DE IMPACTOS PROGRAMADOS", K("azul", 2))
    cv.text(x0 + 40, by + 18, "SEMANA 18-84  -  COPIA 2 DE 3", K("azul", 2))
    cv.text(x0 + 40, by + 32, "PROHIBIDA SU REPRODUCCION", K("cielo", 3))
    PP.sello_rect(cv, x1 - 92, by + 22, x1 - 14, by + 38, K("rojo", 3), "ALTO SECRETO", semilla=4, tinta=0.78)
    PP.sello_rect(cv, x1 - 90, by + 24, x1 - 16, by + 36, K("rojo", 3), "", semilla=5, tinta=0.5)
    PP.manchas_papel(cv, x0 + 3, y0 + 3, x1 - 3, y1 - 3, 3, semilla=9, rampa="cielo", radio=(1, 3))
    # grapa arriba a la izquierda
    cv.hline(x0 + 4, x0 + 12, y0 + 1, K("gris", 7)); cv.px(x0 + 4, y0 + 2, K("gris", 5)); cv.px(x0 + 11, y0 + 2, K("gris", 5))

    # --- el cuaderno de tapas negras
    c0, c1, c2, c3 = CU
    PP.sombra(cv, c0 - 3, c1 - 3, c2 + 3, c3 + 3, 3, 3)
    cv.rect(c0 - 3, c1 - 3, c2 + 3, c3 + 3, K("gris", 1)); cv.frame(c0 - 3, c1 - 3, c2 + 3, c3 + 3, K("gris", 0))
    cv.hline(c0 - 2, c2 + 2, c1 - 2, K("gris", 3))
    for k in range(2):                                                        # canto de las hojas
        cv.rect(c0 + k, c1 + k, c2 + 1 - k, c3 + 1 - k, K("papel", 2 + k))
    PP.hoja(cv, c0, c1, c2, c3, base=4, semilla=44, mordidas=0.02, muescas=0, fibra=0.02, sombra_mesa=False)
    PP.renglones(cv, c0 + 4, c2 - 4, [(92 + 24 * k) // 2 for k in range(17) if 92 + 24 * k < 496], K("cielo", 5))
    cv.vline(670 // 2, c1 + 1, c3 - 1, K("granate", 5))
    cv.hline(c0 + 4, c2 - 4, c1 + 3, K("cielo", 4))
    return cv


def exportar(destino):
    dibujar().img.save(destino / "copiar-fondo.png")
    return ["copiar-fondo.png"]
