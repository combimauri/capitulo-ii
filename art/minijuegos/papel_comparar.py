"""El comparador (ComparadorScene): un recuerdo en sepia frente al documento.

A la izquierda, el recuerdo: una hoja tostada por la luz de la memoria (resplandor `ocre` sobre `papel`), con los
bordes que se deshacen en píxeles sueltos. A la derecha, el documento real, con su soporte según el sitio:
  · archivo (J6.03, el parte en el archivo del departamento): mesa de consulta de acero, cajas de cartón abiertas
    con sus legajos; el parte archivado, con membrete y filete rojo.
  · banco (J9.06, el Times en el banco de un parque): las tablas del banco y la grava entre ellas; el periódico,
    con su doble filete negro de cabecera y el pliegue; el sobre del Miniver al lado.

Pantalla → arte: recuerdo (60, 70, 400×380) → (30, 35)-(230, 225); documento (500, 70) → (250, 35)-(450, 225).
El filete de la cabecera del documento (Y0 + 44) va horneado: y = 57.
"""
import random

from pixel import Canvas, K
import papel as PP

REC = (30, 35, 230, 225)
DOC = (250, 35, 450, 225)


def _recuerdo(cv, semilla):
    """La hoja del recuerdo: papel cálido teñido de ámbar, con los bordes deshaciéndose (tramado)."""
    rnd = random.Random(semilla)
    x0, y0, x1, y1 = REC
    m = set()
    for y in range(y0 - 4, y1 + 4):
        for x in range(x0 - 4, x1 + 4):
            e = min(x - x0, x1 - 1 - x, y - y0, y1 - 1 - y)              # distancia al borde (negativa: fuera)
            if e >= 5:
                m.add((x, y))
            elif e >= -4:
                umbral = ((e + 4) / 9) ** 1.5                            # 0 fuera … 1 dentro
                if umbral * 16 > PP.BAYER4[y % 4][x % 4] + rnd.random() * 4 - 1:
                    m.add((x, y))
    p = cv.img.load()
    for (x, y) in m:
        e = min(x - x0, x1 - 1 - x, y - y0, y1 - 1 - y)
        t = 2 if e < 3 else 3
        if rnd.random() < 0.04:
            t -= 1
        p[x, y] = K("papel", t)
    PP.manchas_papel(cv, x0 + 6, y0 + 6, x1 - 6, y1 - 6, 6, semilla=semilla + 1, radio=(2, 5))
    # el renglón de cabecera del recuerdo, como lo recuerda (borroso)
    for x in range(x0 + 10, x1 - 10):
        if rnd.random() < 0.7:
            cv.px(x, 57, K("madera", 5))
    return m


def _halo(cv, radio=22, fuerza=0.45, pasos=5):
    """Bruma ámbar alrededor del recuerdo: un resplandor rectangular con caída cuantizada."""
    x0, y0, x1, y1 = REC
    p = cv.img.load()
    g = K("ocre", 2)
    for y in range(max(0, y0 - radio), min(cv.h, y1 + radio)):
        for x in range(max(0, x0 - radio), min(cv.w, x1 + radio)):
            dx = max(x0 - x, 0, x - (x1 - 1)); dy = max(y0 - y, 0, y - (y1 - 1))
            d = (dx * dx + dy * dy) ** 0.5 / radio
            if d >= 1:
                continue
            k = round(fuerza * (1 - d) ** 1.4 * pasos / fuerza) / pasos * fuerza
            c = p[x, y]
            p[x, y] = tuple(int(c[i] * (1 - k) + g[i] * k) for i in range(3))


def _tenir_recuerdo(cv, m, fuerza=0.42):
    """El ámbar de la memoria, mezclado sobre el papel (el único color que se mezcla: un resplandor)."""
    p = cv.img.load()
    g = K("ocre", 3)
    for (x, y) in m:
        if 0 <= x < cv.w and 0 <= y < cv.h:
            c = p[x, y]
            p[x, y] = tuple(int(c[i] * (1 - fuerza) + g[i] * fuerza) for i in range(3))


def _caja(cv, x, y, etiqueta, rnd):
    """Caja de archivo de cartón, abierta, con legajos asomando (vista desde arriba)."""
    PP.sombra(cv, x, y, x + 64, y + 46, 3, 3)
    cv.rect(x, y, x + 64, y + 46, K("ocre", 1)); cv.frame(x, y, x + 64, y + 46, K("ocre", 0))
    cv.rect(x + 3, y + 3, x + 61, y + 43, K("madera", 1))
    for k in range(6):                                                       # legajos de canto
        b = rnd.choice([2, 3, 3, 4])
        cv.rect(x + 5 + k * 9, y + 5, x + 12 + k * 9, y + 41, K("papel", b))
        cv.vline(x + 5 + k * 9, y + 5, y + 41, K("papel", b - 1))
        cv.rect(x + 7 + k * 9, y + 6, x + 11 + k * 9, y + 9, K("gris", 6) if k % 2 else K("rojo", 3))
    cv.rect(x - 2, y + 46, x + 66, y + 54, K("ocre", 2)); cv.frame(x - 2, y + 46, x + 66, y + 54, K("ocre", 0))
    cv.rect(x + 12, y + 47, x + 52, y + 53, K("papel", 3))
    cv.text(x + 14, y + 48, etiqueta, K("gris", 2))


def _archivo(cv):
    rnd = random.Random(61)
    PP.chapa(cv, 0, 0, 480, 270, base=4, semilla=17)
    cv.hline(0, 480, 268, K("gris", 2)); cv.hline(0, 480, 269, K("gris", 1))
    _caja(cv, 408, -30, "84-04", rnd)
    _caja(cv, -40, 196, "84-03", rnd)
    # partes sueltos, ya revisados, apilados a la derecha
    for k in range(3):
        PP.hoja(cv, 456 + k * 2, 80 + k * 3, 490, 150 + k * 3, base=3 + (k == 2), semilla=80 + k, muescas=1)
    # el documento: el parte archivado
    x0, y0, x1, y1 = DOC
    PP.hoja(cv, x0, y0, x1, y1, base=4, semilla=91, mordidas=0.04, muescas=2, fibra=0.025)
    PP.piramide(cv, x1 - 26, y0 + 6, 8, K("gris", 3))
    cv.hline(x0 + 10, x1 - 10, 57, K("rojo", 3))
    cv.text(x1 - 30, y0 + 16, "ARCH.", K("papel", 1))
    for x in range(x0 + 3, x1 - 3):                                            # el sello de entrada, una línea de puntos
        if x % 3 == 0:
            cv.px(x, y1 - 4, K("papel", 2))
    cv.bake_lighting()


def _banco(cv):
    rnd = random.Random(62)
    cv.rect(0, 0, 480, 270, K("pared", 1))                                   # grava y tierra entre las tablas
    for _ in range(1800):
        cv.px(rnd.randint(0, 479), rnd.randint(0, 269), K("gris", rnd.choice([2, 3, 4])))
    for y in range(-6, 270, 30):                                            # tablas del banco, a lo ancho
        cv.rect(0, y, 480, y + 26, K("madera", 4))
        cv.hline(0, 480, y, K("madera", 6)); cv.hline(0, 480, y + 25, K("madera", 2))
        for _ in range(9):
            vy = rnd.randint(y + 3, y + 23); a = rnd.randint(-20, 470)
            cv.hline(a, a + rnd.randint(20, 90), vy, K("madera", 3))
        for _ in range(4):                                                  # pintura verde-gris descascarillada
            a, b = rnd.randint(0, 470), rnd.randint(y + 2, y + 20)
            cv.rect(a, b, a + rnd.randint(3, 9), b + rnd.randint(1, 3), K("pared", 4))
        for x in (36, 240, 444):                                            # tornillos de las tablas
            cv.px(x, y + 12, K("gris", 1)); cv.px(x + 1, y + 12, K("gris", 6))
    for (x, y) in ((14, 240), (238, 10), (466, 150), (8, 60)):              # hojas secas
        cv.ellipse(x, y, x + 7, y + 4, K("ocre", 1)); cv.px(x + 3, y + 2, K("madera", 2))
    # el sobre del Miniver, abierto, bajo el periódico
    PP.sombra(cv, 404, 196, 474, 250, 3, 3)
    cv.rect(404, 196, 474, 250, K("papel", 2)); cv.frame(404, 196, 474, 250, K("papel", 0))
    cv.poly([(404, 196), (439, 222), (474, 196)], K("papel", 1))
    cv.d.line([(404, 196), (439, 222), (474, 196)], fill=K("papel", 0))
    cv.text(412, 238, "MINIVER", K("gris", 4))
    # el periódico: papel de prensa, doble filete negro de cabecera y el pliegue del medio
    x0, y0, x1, y1 = DOC
    PP.hoja(cv, x0, y0, x1, y1, base=3, semilla=92, mordidas=0.02, muescas=1, fibra=0.025)
    cv.hline(x0 + 10, x1 - 10, 56, K("gris", 2)); cv.hline(x0 + 10, x1 - 10, 58, K("gris", 2))
    for y in range(y0 + 3, y1 - 3):                                        # pliegue vertical, a la mitad
        if y % 3:
            cv.px((x0 + x1) // 2 + 30, y, K("papel", 2))
    for x in range(x0 + 2, x1 - 2, 2):
        cv.px(x, y1 - 3, K("papel", 2))
    cv.bake_lighting()


def dibujar(mesa="archivo"):
    cv = Canvas(480, 270, ("gris", 4))
    if mesa == "banco":
        _banco(cv)
    else:
        _archivo(cv)
    _halo(cv)
    m = _recuerdo(cv, 7 if mesa == "archivo" else 8)
    _tenir_recuerdo(cv, m)
    return cv


def exportar(destino):
    hechos = []
    for mesa in ("archivo", "banco"):
        dibujar(mesa).img.save(destino / f"comparar-fondo-{mesa}.png"); hechos.append(f"comparar-fondo-{mesa}.png")
    return hechos
