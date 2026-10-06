"""J11.03 — Ministerio del Amor: pasillos del Archivo B (960x540, la cámara sigue al jugador).

Un laberinto de pasillos blancos idénticos. Cada bloque de pared muestra su cara superior (gris muy claro)
y, en su parte de abajo, una cara frontal de 24 px con puertas dobles numeradas. La puerta objetivo, B-4,
está en el muro de arriba (x 820–860) y solo se distingue por su número. Ninguna telepantalla a la vista:
como mucho, rejillas diminutas casi invisibles. Luz plana, sin sombras.
"""
from pixel import Canvas, K

W, H = 960, 540
CARA = 24
BLOQUES = [
    (0, 0, 960, 96), (0, 0, 32, 540), (928, 0, 960, 540), (0, 508, 960, 540),
    (96, 176, 288, 272), (352, 176, 608, 272), (672, 176, 864, 272),
    (32, 336, 288, 432), (352, 336, 544, 432), (608, 336, 864, 432),
]
ENTRADA = (48, 80)                                       # abertura en el muro inferior
PUERTA_OBJETIVO = (820, 860)                             # en la cara frontal del muro de arriba
# (x0 de la puerta, y0 de la cara, número); todas de 40 de ancho
PUERTAS = [
    (100, 72, "7"), (360, 72, "2"), (600, 72, "11"), (820, 72, "4"),
    (200, 248, "9"), (400, 248, "1"), (540, 248, "12"), (760, 248, "5"),
    (80, 408, "3"), (210, 408, "10"), (430, 408, "6"), (690, 408, "8"),
]
REJILLAS = [(450, 80), (160, 250), (720, 250), (300, 420), (860, 420)]

SUELO, JUNTA = K("gris", 10), K("gris", 9)
TAPA, TAPA_FILO, TAPA_BORDE = K("gris", 9), K("gris", 10), K("gris", 8)
CARA_COL, CARA_JUNTA, ZOCALO = K("papel", 4), K("gris", 9), K("gris", 8)


def _cara(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, CARA_COL)
    for y in range(y0 + 8, y1, 8):
        cv.hline(x0, x1, y, CARA_JUNTA)
    for x in range(x0 + 16, x1, 16):
        cv.vline(x, y0, y1 - 2, CARA_JUNTA)
    cv.rect(x0, y1 - 2, x1, y1, ZOCALO)
    if x0 > 0:
        cv.vline(x0, y0, y1, ZOCALO)
    if x1 < W:
        cv.vline(x1 - 1, y0, y1, ZOCALO)


def _tapa(cv, x0, y0, x1, y1):
    cv.rect(x0, y0, x1, y1, TAPA)
    cv.hline(x0, x1, y0, TAPA_FILO)


def _puerta(cv, x0, y0, numero):
    """Puerta doble de 40 de ancho en una cara frontal que empieza en y0."""
    x1, y1 = x0 + 40, y0 + CARA - 2
    cv.rect(x0, y0 + 1, x1, y1, K("gris", 8))                                               # marco
    cv.rect(x0 + 2, y0 + 3, x1 - 2, y1, K("gris", 9))
    cv.vline(x0 + 20, y0 + 3, y1, K("gris", 8))                                             # junta entre hojas
    cv.rect(x0 + 17, y0 + 13, x0 + 19, y0 + 15, K("gris", 6)); cv.rect(x0 + 21, y0 + 13, x0 + 23, y0 + 15, K("gris", 6))
    t = "B-" + numero
    w = cv.text_width(t) + 4
    px0 = x0 + 20 - w // 2
    cv.rect(px0, y0 + 5, px0 + w, y0 + 12, K("gris", 10)); cv.frame(px0, y0 + 5, px0 + w, y0 + 12, K("gris", 7))
    cv.text(px0 + 2, y0 + 6, t, K("gris", 5))


def _rejilla(cv, x, y):
    """Rejilla de ventilación diminuta (ahí detrás zumba algo)."""
    cv.rect(x - 2, y - 1, x + 3, y + 2, K("gris", 9))
    cv.px(x - 1, y, K("gris", 8)); cv.px(x + 1, y, K("gris", 8))


def dibujar(variante=None):
    cv = Canvas(W, H, bg=("gris", 10))
    # suelo blanco con juntas apenas visibles
    for y in range(0, H, 24):
        cv.hline(0, W, y, JUNTA)
    for x in range(0, W, 24):
        cv.vline(x, 0, H, JUNTA)
    # caras frontales primero; las tapas encima (así los muros que se cruzan quedan limpios)
    for (x0, y0, x1, y1) in BLOQUES:
        _cara(cv, x0, y1 - CARA, x1, y1)
    for (x0, y0, x1, y1) in BLOQUES:
        _tapa(cv, x0, y0, x1, y1 - CARA)
    # filo de las tapas contra el suelo y contra su cara (sin sombra: solo una línea)
    tapa = [[False] * W for _ in range(H)]
    for (x0, y0, x1, y1) in BLOQUES:
        for y in range(y0, y1 - CARA):
            fila = tapa[y]
            for x in range(x0, x1):
                fila[x] = True
    px = cv.img.load()
    for y in range(H):
        for x in range(W):
            if tapa[y][x] and any(0 <= x + dx < W and 0 <= y + dy < H and not tapa[y + dy][x + dx]
                                  for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = TAPA_BORDE
    cv.hline(0, W, 0, TAPA_FILO)
    for (x0, y0, n) in PUERTAS:
        _puerta(cv, x0, y0, n)
    for (x, y) in REJILLAS:
        _rejilla(cv, x, y)
    # entrada de servicio: abertura en el muro inferior
    a, b = ENTRADA
    cv.rect(a, 508, b, H, SUELO)
    for y in range(516, H, 24):
        cv.hline(a, b, y, JUNTA)
    cv.vline(a, 508, H, K("gris", 8)); cv.vline(b - 1, 508, H, K("gris", 8))
    cv.rect(a - 2, 516, a, H, K("gris", 9)); cv.rect(b, 516, b + 2, H, K("gris", 9))       # jambas
    cv.bake_lighting()                                                                      # luz plana
    return cv
