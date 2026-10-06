"""J8 — Ministerio de la Verdad, Departamento de Registro (960x270, la cámara sigue al jugador).

Interior de la pirámide blanca: todo papel y gris claro, muy luminoso. Una fila de cubículos de cristal
adosados a la pared del fondo (el de Winston en x 480–536), cada uno con máquina de escribir, habla-escribe
y las tres ranuras (tubo de entrada, tubo de salida y agujero de la memoria). Tubos neumáticos por el
techo, dos islas de cubículos espalda con espalda, el mostrador de entregas y la puerta de la escalera.
"""
import random

from pixel import Canvas, K
import props as P

W, H = 960, 270
WT, WB, FB = 18, 98, 246
CUBICULOS = [(x, x + 56) for x in range(120, 841, 60) if x + 56 <= 840]       # 12 cubículos de pared
CUBICULO_WINSTON = (480, 536)
ISLAS = [(200, 140, 380, 176), (520, 140, 700, 176)]                            # huellas en el suelo
MOSTRADOR = (32, 104, 104, 140)
PUERTA_ESCALERA = (900, 34, 940, 96)
ENTRADA = (40, 80)                                                              # hueco en el muro inferior


def _funcionario(cv, x, y, rnd, de_cara=False):
    """Busto de un funcionario sentado; (x, y) = base de los hombros."""
    ropa = rnd.choice([2, 2, 3, 1])
    pelo = rnd.choice([("pelo", 0), ("pelo", 1), ("madera", 2), ("ocre", 1), ("gris", 6)])
    cv.rect(x - 6, y - 8, x + 6, y, K("azul", ropa)); cv.hline(x - 6, x + 6, y - 8, K("azul", ropa + 1))
    if de_cara:
        piel = rnd.choice([2, 3, 4])
        cv.rect(x - 4, y - 16, x + 4, y - 8, K("piel", piel)); cv.rect(x - 4, y - 17, x + 4, y - 14, K(*pelo))
        cv.px(x - 2, y - 12, K("gris", 1)); cv.px(x + 1, y - 12, K("gris", 1))
    else:
        cv.ellipse(x - 4, y - 16, x + 5, y - 7, K(*pelo))


def _maquina(cv, x, y):
    """Máquina de escribir vista desde arriba-delante; (x, y) = esquina superior izquierda (16x9)."""
    cv.rect(x, y + 2, x + 16, y + 9, K("gris", 2)); cv.frame(x, y + 2, x + 16, y + 9, K("gris", 0))
    cv.rect(x + 2, y, x + 14, y + 3, K("gris", 4))
    cv.rect(x + 4, y - 3, x + 12, y + 1, K("papel", 4))
    for k in range(2):
        cv.hline(x + 2, x + 14, y + 5 + k * 2, K("gris", 5))


def _hablaescribe(cv, x, y, chico=False):
    """Micrófono del habla-escribe sobre su brazo articulado; (x, y) = base."""
    cv.rect(x - 2, y - 1, x + 3, y + 1, K("gris", 2))
    if chico:
        cv.vline(x, y - 5, y - 1, K("gris", 3))
        cv.rect(x - 1, y - 8, x + 3, y - 4, K("gris", 2)); cv.px(x, y - 7, K("gris", 5))
        return
    cv.d.line([(x, y - 1), (x + 3, y - 7), (x + 1, y - 11)], fill=K("gris", 3))
    cv.ellipse(x - 2, y - 15, x + 4, y - 9, K("gris", 2), outline=K("gris", 0)); cv.px(x, y - 13, K("gris", 5))


def _ranuras(cv, x, y):
    """Las tres ranuras de la pared: tubo de entrada, tubo de salida y agujero de la memoria."""
    for (tx, rot) in ((x, "ENT"), (x + 11, "SAL")):
        cv.ellipse(tx, y, tx + 8, y + 8, K("gris", 5), outline=K("gris", 3)); cv.ellipse(tx + 2, y + 2, tx + 6, y + 6, K("gris", 0))
    cv.rect(x + 23, y + 1, x + 41, y + 9, K("gris", 4)); cv.frame(x + 23, y + 1, x + 41, y + 9, K("gris", 3))
    cv.rect(x + 25, y + 3, x + 39, y + 7, K("gris", 0))                                     # agujero de la memoria
    for k in range(x + 27, x + 39, 3):
        cv.vline(k, y + 3, y + 7, K("gris", 2))                                             # rejilla
    cv.px(x + 32, y - 2, K("rojo", 3))                                                      # la única mota de color


def _cubiculo_pared(cv, x0, x1, rnd, ocupado):
    top = 30
    cv.rect(x0, top, x1, WB, K("gris", 8))                                                  # fondo del cubículo
    cv.rect(x0, top, x1, top + 3, K("gris", 6))
    _ranuras(cv, x0 + 7, 44)
    # tubos que bajan del techo a las dos bocas
    cv.rect(x0 + 10, WT - 2, x0 + 13, 44, K("gris", 6)); cv.vline(x0 + 10, WT - 2, 44, K("gris", 8))
    cv.rect(x0 + 21, WT - 2, x0 + 24, 44, K("gris", 6)); cv.vline(x0 + 21, WT - 2, 44, K("gris", 8))
    # mesa: tablero y frente
    cv.rect(x0 + 3, 70, x1 - 3, 80, K("gris", 7)); cv.hline(x0 + 3, x1 - 3, 70, K("gris", 9))
    cv.rect(x0 + 3, 80, x1 - 3, 88, K("gris", 5)); cv.hline(x0 + 3, x1 - 3, 87, K("gris", 3))
    cv.rect(x0 + 4, 88, x0 + 6, 96, K("gris", 4)); cv.rect(x1 - 6, 88, x1 - 4, 96, K("gris", 4))
    _maquina(cv, x0 + 20, 70)
    _hablaescribe(cv, x0 + 10, 78)
    cv.rect(x1 - 15, 72, x1 - 6, 78, K("papel", 4)); cv.hline(x1 - 13, x1 - 8, 74, K("gris", 7))  # hojas
    # silla (respaldo visto desde detrás)
    cv.rect(x0 + 22, 86, x0 + 34, 96, K("gris", 4)); cv.hline(x0 + 22, x0 + 34, 86, K("gris", 6))
    cv.rect(x0 + 24, 96, x0 + 26, WB, K("gris", 3)); cv.rect(x0 + 30, 96, x0 + 32, WB, K("gris", 3))
    if ocupado:
        _funcionario(cv, x0 + 28, 92, rnd)
    # mamparas de cristal: marco superior, montantes y luna delantera alta
    cv.rect(x0 - 2, top - 3, x1 + 2, top, K("gris", 5)); cv.hline(x0 - 2, x1 + 2, top - 3, K("gris", 7))
    for mx in (x0 - 2, x1):
        cv.rect(mx, top, mx + 2, WB, K("gris", 5)); cv.vline(mx, top, WB, K("gris", 7))
    cv.hline(x0, x1, 62, K("gris", 6))                                                      # travesaño de la luna
    cv.add_light(x0, top, x1, 62, 1)                                                        # el cristal aclara
    for k in range(0, 3):                                                                   # reflejos en diagonal
        bx = x0 + 6 + k * 18
        cv.d.line([(bx, 58), (bx + 12, 34)], fill=K("gris", 10))
        cv.d.line([(bx + 3, 58), (bx + 14, 37)], fill=K("gris", 10))


def _isla(cv, x0, y0, x1, y1, rnd):
    """Dos filas de cubículos de cristal espalda con espalda sobre la huella (x0, y0)-(x1, y1)."""
    alto = 24
    ym = (y0 + y1) // 2                                                                     # eje: la mampara central
    cv.rect(x0 + 4, y1, x1 + 4, y1 + 5, K("gris", 6))                                       # sombra en el suelo
    bay = (x1 - x0) // 3
    for i in range(3):
        bx = x0 + i * bay
        # fila de arriba: silla al norte, mesa contra la mampara (se ve a través del cristal)
        cv.rect(bx + 3, ym - 10, bx + bay - 3, ym - 1, K("gris", 7)); cv.hline(bx + 3, bx + bay - 3, ym - 10, K("gris", 9))
        _maquina(cv, bx + 20, ym - 10)
        _hablaescribe(cv, bx + 10, ym - 3, chico=True)
        cv.rect(bx + 22, y0 + 1, bx + 36, y0 + 7, K("gris", 4)); cv.hline(bx + 22, bx + 36, y0 + 1, K("gris", 6))
        if rnd.random() < 0.6:
            _funcionario(cv, bx + 29, y0 + 8, rnd, de_cara=True)
        # fila de abajo: mesa contra la mampara, silla al sur (de espaldas)
        cv.rect(bx + 3, ym + 2, bx + bay - 3, ym + 11, K("gris", 7)); cv.hline(bx + 3, bx + bay - 3, ym + 2, K("gris", 9))
        cv.rect(bx + 3, ym + 11, bx + bay - 3, ym + 13, K("gris", 5))
        _maquina(cv, bx + 20, ym + 3)
        _hablaescribe(cv, bx + 10, ym + 10, chico=True)
        cv.rect(bx + bay - 16, ym + 4, bx + bay - 7, ym + 10, K("papel", 4))
        cv.rect(bx + 22, y1 - 7, bx + 36, y1, K("gris", 4)); cv.hline(bx + 22, bx + 36, y1 - 7, K("gris", 6))
        if rnd.random() < 0.6:
            _funcionario(cv, bx + 29, y1 - 1, rnd)
        # tres bocas en la mampara central (las mismas ranuras, en pequeño)
        cv.ellipse(bx + 6, ym - alto + 4, bx + 11, ym - alto + 9, K("gris", 3)); cv.px(bx + 8, ym - alto + 6, K("gris", 0))
        cv.ellipse(bx + 13, ym - alto + 4, bx + 18, ym - alto + 9, K("gris", 3)); cv.px(bx + 15, ym - alto + 6, K("gris", 0))
        cv.rect(bx + 22, ym - alto + 5, bx + 34, ym - alto + 9, K("gris", 0))
    # mampara central: luna vista de frente, con marco
    cv.add_light(x0, ym - alto, x1, ym, 1)
    cv.rect(x0, ym - alto - 2, x1, ym - alto, K("gris", 5)); cv.hline(x0, x1, ym - alto - 2, K("gris", 7))
    cv.rect(x0, ym - 1, x1, ym + 2, K("gris", 5)); cv.hline(x0, x1, ym + 1, K("gris", 3))
    for k in range(x0 + 8, x1 - 10, 22):
        cv.d.line([(k, ym - 4), (k + 9, ym - alto + 3)], fill=K("gris", 10))
    # mamparas transversales (de canto): tiras de cristal con montante
    for i in range(4):
        mx = x0 + i * bay - (2 if i == 3 else 0)
        cv.rect(mx, y0 - alto, mx + 2, y1, K("gris", 6)); cv.vline(mx, y0 - alto, y1, K("gris", 8))
        cv.hline(mx, mx + 2, y0 - alto, K("gris", 4))
    cv.rect(x0, y1 - 2, x1, y1, K("gris", 5))                                               # zócalo de la isla


def _mostrador(cv, x0, y0, x1, y1):
    """Mostrador de entregas (huella x0..x1, y0..y1) con el tampón, bandejas y un timbre."""
    alto = 14
    cv.rect(x0 + 4, y1, x1 + 4, y1 + 4, K("gris", 6))                                        # sombra
    cv.rect(x0, y0 - alto, x1, y1 - alto, K("papel", 4)); cv.frame(x0, y0 - alto, x1, y1 - alto, K("papel", 2))
    cv.rect(x0, y1 - alto, x1, y1, K("papel", 3)); cv.hline(x0, x1, y1 - alto, K("papel", 2))
    for k in range(x0 + 8, x1, 16):
        cv.vline(k, y1 - alto + 1, y1, K("papel", 2))
    cv.hline(x0, x1, y1 - 1, K("papel", 1))
    t = y0 - alto
    # bandejas de entrada y salida con legajos
    for bx in (x0 + 4, x0 + 22):
        cv.rect(bx, t + 4, bx + 15, t + 14, K("gris", 6)); cv.frame(bx, t + 4, bx + 15, t + 14, K("gris", 4))
        for k in range(3):
            cv.rect(bx + 2, t + 9 - k * 2, bx + 13, t + 12 - k * 2, K("papel", 4 - k % 2))
    # el tampón: almohadilla de tinta y sello de mango de madera
    cv.rect(x0 + 44, t + 8, x0 + 54, t + 15, K("gris", 1)); cv.rect(x0 + 45, t + 9, x0 + 53, t + 14, K("rojo", 1))
    cv.rect(x0 + 57, t + 10, x0 + 63, t + 14, K("gris", 3))
    cv.rect(x0 + 58, t + 4, x0 + 62, t + 10, K("madera", 4)); cv.ellipse(x0 + 57, t + 1, x0 + 63, t + 6, K("madera", 5))
    # una hoja recién sellada
    cv.rect(x0 + 40, t + 18, x0 + 54, t + 28, K("papel", 4)); cv.hline(x0 + 42, x0 + 50, t + 20, K("gris", 7))
    cv.rect(x0 + 46, t + 23, x0 + 52, t + 27, K("rojo", 3)); cv.frame(x0 + 46, t + 23, x0 + 52, t + 27, K("rojo", 2))
    # timbre
    cv.ellipse(x0 + 8, t + 22, x0 + 16, t + 28, K("gris", 7), outline=K("gris", 4)); cv.px(x0 + 12, t + 22, K("gris", 3))


def _casillero(cv, x0, y0, x1, y1):
    """Casillero de madera clara para las entregas, colgado detrás del mostrador."""
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("gris", 7))
    cv.rect(x0, y0, x1, y1, K("madera", 5)); cv.frame(x0, y0, x1, y1, K("madera", 3))
    rnd = random.Random(3)
    for y in range(y0 + 2, y1 - 6, 9):
        for x in range(x0 + 2, x1 - 6, 10):
            cv.rect(x, y, x + 8, y + 7, K("madera", 2))
            if rnd.random() < 0.6:
                cv.rect(x + 1, y + 3, x + 7, y + 7, K("papel", rnd.choice([3, 4])))
    cv.rect(x0 + 8, y0 - 9, x1 - 8, y0 - 2, K("papel", 4)); cv.frame(x0 + 8, y0 - 9, x1 - 8, y0 - 2, K("gris", 6))
    cv.text((x0 + x1) // 2 - cv.text_width("ENTREGAS") // 2, y0 - 8, "ENTREGAS", K("gris", 2))


def _tubos_techo(cv, rnd):
    """La banda del techo: haces de tubos neumáticos con registros y cápsulas a la vista."""
    cv.rect(0, 0, W, WT, K("gris", 7))
    for i, ty in enumerate((3, 8, 13)):
        cv.rect(0, ty, W, ty + 4, K("gris", 6 - i % 2)); cv.hline(0, W, ty, K("gris", 9)); cv.hline(0, W, ty + 3, K("gris", 4))
    for x in range(20, W, 64):                                                              # abrazaderas
        cv.rect(x, 2, x + 3, WT, K("gris", 4))
    for x in range(52, W, 128):                                                             # registros acristalados con cápsula
        cv.rect(x, 7, x + 14, 13, K("gris", 9)); cv.frame(x, 7, x + 14, 13, K("gris", 4))
        cv.rect(x + 3 + rnd.randint(0, 4), 9, x + 9 + rnd.randint(0, 2), 11, K("ocre", 2))
    cv.rect(0, WT - 1, W, WT, K("gris", 5))


def _puerta_escalera(cv, x0, y0, x1, y1):
    cv.rect(x0 - 3, y0 - 3, x1 + 3, y1 + 2, K("gris", 5))
    cv.rect(x0, y0, x1, y1, K("gris", 6))
    cv.rect(x0 + 3, y0 + 4, x1 - 3, y0 + 26, K("gris", 0))                                  # mirilla: la escalera, a oscuras
    for k in range(4):
        cv.rect(x0 + 4, y0 + 20 - k * 5, x1 - 4, y0 + 22 - k * 5, K("gris", 2))
    cv.frame(x0 + 3, y0 + 30, x1 - 3, y1 - 4, K("gris", 5))
    cv.rect(x0 + 6, y0 + 36, x0 + 10, y0 + 38, K("gris", 3))                                # barra antipánico
    cv.hline(x0 + 6, x1 - 6, y0 + 37, K("gris", 4))
    cv.rect(x0 - 4, y0 - 17, x1 + 4, y0 - 1, K("papel", 4)); cv.frame(x0 - 4, y0 - 17, x1 + 4, y0 - 1, K("gris", 5))
    cx = (x0 + x1) // 2
    cv.text(cx - cv.text_width("ESCALERA") // 2, y0 - 15, "ESCALERA", K("gris", 2))
    cv.text(cx - cv.text_width("PLANTA 3") // 2, y0 - 8, "PLANTA 3", K("gris", 3))


def dibujar(variante=None):
    rnd = random.Random(1984)
    cv = Canvas(W, H)
    # pared del fondo: estuco blanco de la pirámide, con pilastras
    cv.rect(0, WT, W, WB, K("papel", 4))
    for x in range(0, W, 120):
        cv.rect(x + 108, WT, x + 116, WB, K("papel", 3)); cv.vline(x + 108, WT, WB, K("gris", 9))
    cv.hline(0, W, WT + 4, K("papel", 3))
    _tubos_techo(cv, rnd)
    # cubículos de pared (uno de cada tres, vacío; el de Winston, vacío y con la silla separada)
    for i, (x0, x1) in enumerate(CUBICULOS):
        ocupado = (x0, x1) != CUBICULO_WINSTON and i % 3 != 1
        _cubiculo_pared(cv, x0, x1, rnd, ocupado)
        cv.rect(x0 + 24, 27, x0 + 32, 30, K("gris", 9)); cv.text(x0 + 25 + (1 if i < 9 else -1), 22, str(i + 1), K("gris", 4))
    # mostrador de entregas con su casillero
    _casillero(cv, 22, 34, 104, 82)
    # puerta de la escalera
    _puerta_escalera(cv, *PUERTA_ESCALERA)
    # una telepantalla, alta, entre la última fila de cubículos y la puerta
    P.telepantalla(cv, 856, 40, 30, 22)
    P.zocalo(cv, 0, W, WB, alto=4, rampa="gris", base=7)
    # suelo pulido: losas grandes casi blancas
    P.baldosas(cv, 0, WB, W, FB, K("gris", 9), K("gris", 8), t=24, linea=K("gris", 7))
    for (x0, x1) in CUBICULOS:                                                              # reflejos de los montantes
        for mx in (x0 - 1, x1 + 1):
            cv.vline(mx, WB + 1, WB + 10, K("gris", 10))
    for (x0, y0, x1, y1) in ISLAS:                                                          # reflejo de las islas en el encerado
        for k in range(x0 + 6, x1 - 6, 30):
            cv.hline(k, k + 14, y1 + 9, K("gris", 10))
    # papeles caídos y una cápsula de tubo olvidada
    for (px_, py_) in [(150, 200), (420, 214), (760, 196), (880, 224)]:
        cv.rect(px_, py_, px_ + 8, py_ + 6, K("papel", 4)); cv.hline(px_ + 2, px_ + 6, py_ + 2, K("gris", 7))
    cv.rect(612, 206, 622, 211, K("ocre", 2)); cv.hline(612, 622, 206, K("ocre", 3)); cv.rect(622, 207, 624, 210, K("gris", 4))
    # islas de cubículos
    for (x0, y0, x1, y1) in ISLAS:
        _isla(cv, x0, y0, x1, y1, rnd)
    _mostrador(cv, *MOSTRADOR)
    # muro inferior con el hueco de entrada
    a, b = ENTRADA
    cv.rect(0, FB, a, FB + 12, K("gris", 6)); cv.rect(b, FB, W, FB + 12, K("gris", 6))
    cv.hline(0, a, FB, K("gris", 8)); cv.hline(b, W, FB, K("gris", 8))
    cv.rect(0, FB + 12, a, H, K("gris", 3)); cv.rect(b, FB + 12, W, H, K("gris", 3))
    cv.rect(a, FB, b, H, K("gris", 8))                                                      # el pasillo de entrada
    for y in range(FB, H, 24):
        cv.hline(a, b, y, K("gris", 7))
    cv.vline(a, FB, H, K("gris", 5)); cv.vline(b - 1, FB, H, K("gris", 5))
    # luz: blanca y pareja; solo un poco de oclusión junto a los muros
    cv.add_light_fn(lambda x, y: -1 if (WB <= y < WB + 4 or FB - 4 <= y < FB) and not (ENTRADA[0] <= x < ENTRADA[1] and y >= FB - 4) else 0)
    cv.add_light(a, FB + 12, b, H, -1)
    cv.glow_rgb = K("papel", 4)
    for gx in range(120, W, 240):
        cv.add_glow_suave(gx, 170, 150, 0.12, squash=1.6, limite=(0, WB, W, FB))
    cv.bake_lighting()
    return cv
