"""J13.01 — Estación de Shadwell, al amanecer, con la niebla del río.

Una boca de metro de azulejo granate tapiada con tablones (el tercero, suelto, gira sobre un solo clavo),
un cartel descolorido del Ministerio de la Abundancia, la pintada de los Espías con EURASIA tachado y una farola
apagada. Al fondo, más allá de los tejados, las grúas del muelle. Todo frío, gris azulado, lavado por la niebla.
"""
import math
import random

from pixel import Canvas, K, FONT3x5
import props as P
import _luz as L
from limehouse import ladrillo

W, H = 480, 270
FACHADA, SUELO_FIN = 92, 250
BOCA = (200, 30, 280, 92)                 # la boca tapiada
TABLON_SUELTO = (204, 58, 276, 66)        # el tercer tablón (de arriba abajo)
CARTEL = (186, 14, 294, 28)
PINTADA = (50, 40, 170, 76)
FAROLA = (420, 96)                        # base; huella (416,92)-(424,100)


# ---------------------------------------------------------------- letra


def texto_estrecho(cv, x, y, s, col, espacio=2):
    """Fuente 3x5 con los espacios en blanco más estrechos (para que quepa el nombre del ministerio)."""
    for ch in s.upper():
        if ch == " ":
            x += espacio
            continue
        bits = FONT3x5.get(ch, FONT3x5[" "])
        for i, b in enumerate(bits):
            if b == "1":
                cv.px(x + i % 3, y + i // 3, col)
        x += 4
    return x


def ancho_estrecho(s, espacio=2):
    return sum(espacio if c == " " else 4 for c in s) - 1


def spray(cv, x, y, s, col, rnd, escala=2, gotas=0.12, alto_gota=(1, 4)):
    """Letras pintadas con bote: la fuente a escala 2, con bordes mordidos y chorretones."""
    for ch in s.upper():
        if ch in "¡!":
            # exclamación: un palo y un punto (el ¡ va al revés)
            palo, punto = (range(0, 7), 8) if ch == "!" else (range(3, 10), 0)
            for k in palo:
                cv.rect(x, y + k, x + 2, y + k + 1, col)
            cv.rect(x, y + punto, x + 2, y + punto + 2, col)
            x += 4
            continue
        bits = ANCHAS.get(ch) or FONT3x5.get(ch, FONT3x5[" "])
        ancho = 5 if ch in ANCHAS else 3
        for i, b in enumerate(bits):
            if b == "1":
                px_, py_ = x + (i % ancho) * escala, y + (i // ancho) * escala
                cv.rect(px_, py_, px_ + escala, py_ + escala, col)
                if rnd.random() < 0.08:                                   # salpicadura del bote
                    cv.px(px_ + rnd.choice([-1, escala]), py_ + rnd.randint(0, escala - 1), col)
                if i // ancho == 4 and rnd.random() < gotas:                  # chorretón desde la base de la letra
                    gx = px_ + rnd.randint(0, escala - 1)
                    cv.vline(gx, py_ + escala, py_ + escala + rnd.randint(*alto_gota), col)
        x += (ancho + 1) * escala
    return x


ANCHAS = {"M": "10001" "11011" "10101" "10001" "10001"}


# ---------------------------------------------------------------- fachadas


def _ventana(cv, x, y, w, h, rnd, tapiada=False):
    cv.rect(x - 2, y - 2, x + w + 2, y + h + 1, K("gris", 3))                         # dintel y jambas de piedra
    cv.hline(x - 2, x + w + 2, y - 2, K("gris", 5))
    cv.rect(x, y, x + w, y + h, K("azul", 0))
    if tapiada:
        for yy in range(y, y + h, 4):
            cv.rect(x, yy, x + w, yy + 3, K("madera", 2)); cv.hline(x, x + w, yy + 3, K("madera", 0))
        return
    cv.vline(x + w // 2, y, y + h, K("gris", 2)); cv.hline(x, x + w, y + h // 2, K("gris", 2))
    if rnd.random() < 0.6:                                                           # el cielo blanco reflejado
        cv.px(x + 2, y + 2, K("cielo", 4)); cv.px(x + 3, y + 3, K("cielo", 4)); cv.px(x + 2, y + 3, K("cielo", 3))
    if rnd.random() < 0.3:                                                           # cristal roto
        cv.poly([(x + w // 2 + 1, y), (x + w, y), (x + w, y + 4)], K("gris", 0))
    cv.rect(x - 3, y + h, x + w + 3, y + h + 2, K("gris", 4)); cv.hline(x - 3, x + w + 3, y + h + 1, K("gris", 2))   # alféizar


def _grua(cv, x, base, alto, brazo, col):
    """Silueta de una grúa del muelle, lejos, comida por la niebla."""
    cv.rect(x, base - alto, x + 4, base, col)
    for yy in range(base - alto, base, 6):
        cv.d.line([(x, yy), (x + 3, yy + 5)], fill=K("cielo", 3))
    cv.rect(x - 6, base - alto - 6, x + 10, base - alto, col)                       # cabina
    cv.d.line([(x + 2, base - alto - 4), (x + brazo, base - alto - 14)], fill=col)   # pluma
    cv.d.line([(x + 2, base - alto - 3), (x + brazo, base - alto - 13)], fill=col)
    cv.d.line([(x + 2, base - alto - 12), (x + brazo, base - alto - 14)], fill=col)  # tirante
    cv.vline(x + brazo - 2, base - alto - 13, base - alto + 10, col)                 # gancho
    cv.rect(x + brazo - 4, base - alto + 10, x + brazo, base - alto + 13, col)


def _edificio_izquierdo(cv, rnd):
    """Almacén de ladrillo ennegrecido: aquí pintan los Espías."""
    ladrillo(cv, 0, 4, 178, FACHADA, rnd, base=2)
    cv.rect(0, 0, 178, 6, K("gris", 2)); cv.hline(0, 178, 5, K("gris", 4))         # cornisa
    for wx in (14, 48, 82, 116, 150):
        _ventana(cv, wx, 13, 14, 18, rnd, tapiada=(wx == 82))
    cv.rect(0, 35, 178, 37, K("gris", 3)); cv.hline(0, 178, 35, K("gris", 5))     # imposta entre plantas
    # bajante
    cv.rect(38, 6, 41, FACHADA - 2, K("gris", 1)); cv.vline(38, 6, FACHADA - 2, K("gris", 3))
    for by in (16, 40, 64):
        cv.hline(37, 42, by, K("gris", 0))
    cv.rect(36, FACHADA - 4, 44, FACHADA, K("gris", 1))
    # puerta de carga, cerrada con cadena (a la izquierda de la pintada)
    cv.rect(6, 50, 32, FACHADA, K("madera", 1)); cv.frame(6, 50, 32, FACHADA, K("madera", 0))
    for k in range(8, 32, 6):
        cv.vline(k, 51, FACHADA, K("madera", 0)); cv.vline(k + 1, 51, FACHADA, K("madera", 2))
    cv.d.line([(10, 70), (28, 74)], fill=K("gris", 5)); cv.d.line([(10, 74), (28, 70)], fill=K("gris", 4))
    cv.rect(17, 71, 21, 75, K("gris", 6)); cv.px(19, 74, K("gris", 1))
    # restos de un cartel arrancado a tiras, sobre la puerta de carga
    cv.poly([(8, 40), (30, 40), (30, 44), (22, 47), (14, 44), (8, 46)], K("papel", 1))
    cv.hline(8, 30, 40, K("papel", 2)); cv.px(9, 41, K("rojo", 2)); cv.px(10, 41, K("rojo", 2))


def _cornisa_estacion(cv, x0, x1):
    cv.rect(x0, 0, x1, 12, K("granate", 3))
    cv.hline(x0, x1, 0, K("granate", 5)); cv.hline(x0, x1, 9, K("granate", 1))
    for k in range(x0 + 2, x1 - 2, 6):                                               # dentículos
        cv.rect(k, 10, k + 3, 12, K("granate", 4)); cv.px(k + 2, 11, K("granate", 1))


def _azulejo_granate(cv, x0, y0, x1, y1):
    """Bloques de terracota vidriada (las bocas de metro de antes de la Revolución)."""
    cv.rect(x0, y0, x1, y1, K("granate", 3))
    for y in range(y0, y1, 8):
        cv.hline(x0, x1, y, K("granate", 1))
        cv.hline(x0, x1, y + 1, K("granate", 4))
        for x in range(x0 + (y // 8 % 2) * 6, x1, 12):
            cv.vline(x, y, min(y + 8, y1), K("granate", 1))
            if x + 2 < x1:
                cv.px(x + 2, y + 2, K("granate", 5))                                 # brillo del vidriado


def _estacion(cv, rnd):
    x0, x1 = 178, 302
    _azulejo_granate(cv, x0, 12, x1, FACHADA)
    _cornisa_estacion(cv, x0 - 2, x1 + 2)
    # pilastras a los lados de la boca
    for px_ in (x0, x1 - 16):
        cv.rect(px_, 12, px_ + 16, FACHADA, K("granate", 2))
        cv.vline(px_, 12, FACHADA, K("granate", 4)); cv.vline(px_ + 15, 12, FACHADA, K("granate", 0))
        for y in range(16, FACHADA, 10):
            cv.hline(px_ + 1, px_ + 15, y, K("granate", 1))
        cv.rect(px_ - 1, FACHADA - 6, px_ + 17, FACHADA, K("gris", 3)); cv.hline(px_ - 1, px_ + 17, FACHADA - 6, K("gris", 5))  # basa
    # la boca: arco de medio punto, y la oscuridad de la escalera detrás de los tablones
    bx0, by0, bx1, by1 = BOCA
    cv.rect(bx0 - 4, by0 - 2, bx1 + 4, by1, K("granate", 1))
    cv.rect(bx0, by0 + 4, bx1, by1, K("gris", 0))
    cv.ellipse(bx0, by0 - 2, bx1, by0 + 14, K("gris", 0))
    cv.d.arc([bx0 - 4, by0 - 6, bx1 + 3, by0 + 18], 180, 360, fill=K("granate", 4))
    cv.d.arc([bx0 - 2, by0 - 4, bx1 + 1, by0 + 16], 180, 360, fill=K("granate", 0))
    # los primeros peldaños, apenas
    for k, yy in enumerate((80, 84, 88)):
        cv.hline(bx0 + 2, bx1 - 2, yy, K("gris", 1 + (k > 0)))


def _tablones(cv, rnd):
    bx0, by0, bx1, by1 = BOCA
    cv.d.line([(bx0 + 4, by0 + 4), (bx1 - 6, by1 - 2)], fill=K("madera", 0))         # un tablón viejo, caído detrás
    cv.d.line([(bx0 + 5, by0 + 4), (bx1 - 5, by1 - 2)], fill=K("madera", 1))
    # tablones clavados (y 34–42, 46–54, [58–66 suelto], 70–78, 82–90), con clavos nuevos
    for i, y in enumerate((34, 46, 58, 70, 82)):
        if i == 2:
            continue
        x0, x1 = bx0 - 2 + rnd.randint(0, 1), bx1 + 2 - rnd.randint(0, 1)
        cv.rect(x0 + 1, y + 2, x1 + 1, y + 9, K("gris", 0))                         # sombra
        cv.rect(x0, y, x1, y + 8, K("madera", 3))
        cv.hline(x0, x1, y, K("madera", 5)); cv.hline(x0, x1, y + 7, K("madera", 1))
        for _ in range(3):                                                           # vetas
            gx = rnd.randint(x0 + 4, x1 - 16)
            cv.hline(gx, gx + rnd.randint(6, 14), y + rnd.randint(2, 5), K("madera", 2))
        for nx in (x0 + 3, x1 - 4):
            cv.px(nx, y + 3, K("gris", 8)); cv.px(nx, y + 4, K("gris", 5))       # clavos nuevos, brillantes
    # el tercero: más corto, torcido, sujeto por un solo clavo a la izquierda
    x0, y0, x1, y1 = TABLON_SUELTO
    cv.poly([(x0 + 1, y0 + 2), (x1 + 1, y0 + 4), (x1 + 1, y1 + 3), (x0 + 1, y1 + 1)], K("gris", 0))   # sombra
    cv.poly([(x0, y0), (x1 - 1, y0 + 2), (x1 - 1, y1 + 1), (x0, y1 - 1)], K("madera", 2))
    cv.d.line([(x0, y0), (x1 - 1, y0 + 2)], fill=K("madera", 4))
    cv.d.line([(x0, y1 - 1), (x1 - 1, y1 + 1)], fill=K("madera", 0))
    cv.d.line([(x0 + 10, y0 + 3), (x0 + 30, y0 + 4)], fill=K("madera", 1))
    cv.d.line([(x0 + 40, y0 + 5), (x0 + 58, y0 + 6)], fill=K("madera", 3))
    cv.px(x0 + 3, y0 + 3, K("gris", 6)); cv.px(x0 + 3, y0 + 4, K("gris", 3))       # el único clavo (viejo)
    cv.px(x1 - 5, y0 + 4, K("madera", 0)); cv.px(x1 - 5, y0 + 5, K("madera", 0))  # el agujero del que falta
    # la rendija negra que deja a cada lado
    cv.rect(bx0, y0, x0, y1, K("gris", 0)); cv.rect(x1, y0 + 1, bx1, y1 + 1, K("gris", 0))


def _cartel(cv, rnd):
    x0, y0, x1, y1 = CARTEL
    cv.rect(x0 + 2, y0 + 2, x1 + 2, y1 + 2, K("granate", 0))                         # sombra en la cornisa
    cv.rect(x0, y0, x1, y1, K("papel", 2))
    cv.frame(x0, y0, x1, y1, K("papel", 0))
    for _ in range(70):                                                              # moho y meados de paloma
        cv.px(rnd.randint(x0 + 1, x1 - 2), rnd.randint(y0 + 1, y1 - 2), K("papel", rnd.choice([1, 1, 3])))
    cv.poly([(x1 - 10, y0), (x1, y0), (x1, y0 + 8)], K("granate", 3))                # esquina arrancada
    cv.d.line([(x1 - 10, y0), (x1, y0 + 8)], fill=K("papel", 3))
    t1 = "CERRADO POR REFORMAS"
    cv.text(x0 + (x1 - x0 - cv.text_width(t1)) // 2 + 1, y0 + 2, t1, K("rojo", 2))
    t2 = "MINISTERIO DE LA ABUNDANCIA"
    texto_estrecho(cv, x0 + (x1 - x0 - ancho_estrecho(t2)) // 2, y0 + 8, t2, K("papel", 0))
    cv.px(x0 + 2, y0 + 2, K("gris", 5)); cv.px(x1 - 3, y1 - 3, K("gris", 5))        # chinchetas
    cv.px(x0 + 2, y1 - 3, K("gris", 5))


def _pintada(cv, rnd):
    x0, y0, x1, y1 = PINTADA
    # «EURASIA», más vieja y desvaída, tachada con rabia
    xe = x0 + 40
    spray(cv, xe, y0 + 27, "EURASIA", K("papel", 1), rnd, gotas=0.1)
    ancho = (7 * 4 - 1) * 2
    cv.d.line([(xe - 4, y0 + 35), (xe + ancho + 4, y0 + 28)], fill=K("rojo", 3))     # tachado de un brochazo
    cv.d.line([(xe - 4, y0 + 36), (xe + ancho + 4, y0 + 29)], fill=K("rojo", 3))
    # «¡MUERTE A ESTASIA!», fresca, en rojo
    spray(cv, x0 + 2, y0, "¡MUERTE A", K("rojo", 3), rnd)
    spray(cv, x0 + 44, y0 + 13, "ESTASIA!", K("rojo", 3), rnd)


def _edificio_derecho(cv, rnd):
    """Bloque de viviendas obreras, de ladrillo más claro; tejado bajo y, detrás, el cielo del río."""
    top = 22
    ladrillo(cv, 302, top, W, FACHADA, rnd, base=2, rampa="granate")
    cv.rect(302, top - 4, W, top, K("gris", 2)); cv.hline(302, W, top - 4, K("gris", 4))
    cv.rect(330, top - 12, 340, top - 4, K("granate", 1)); cv.rect(328, top - 14, 342, top - 11, K("gris", 2))   # chimeneas
    cv.rect(440, top - 10, 448, top - 4, K("granate", 1)); cv.rect(438, top - 12, 450, top - 9, K("gris", 2))
    for wx in (316, 352, 388, 452):
        _ventana(cv, wx, top + 8, 13, 16, rnd, tapiada=(wx == 388))
    # tienda cerrada con persiana metálica
    cv.rect(320, 54, 392, FACHADA, K("gris", 2))
    cv.rect(318, 50, 394, 56, K("madera", 1)); cv.hline(318, 394, 50, K("madera", 3))
    cv.text(334, 51, "ULTRAMARINOS", K("madera", 3))
    for yy in range(57, FACHADA, 3):
        cv.hline(322, 390, yy, K("gris", 3)); cv.hline(322, 390, yy + 1, K("gris", 4))
    cv.rect(352, FACHADA - 6, 360, FACHADA - 2, K("gris", 1)); cv.px(355, FACHADA - 4, K("gris", 6))   # candado
    # portal
    P.puerta(cv, 446, 58, w=22, h=34, rampa="madera", base=1)


def _cielo(cv, rnd):
    """Solo se ve por encima del bloque de la derecha: blanco sucio, con las grúas del muelle."""
    for i, y in enumerate(range(0, 22, 4)):
        cv.rect(302, y, W, y + 4, K("cielo", 4 + (i > 2)))
    _grua(cv, 372, 22, 12, 40, K("cielo", 3))
    _grua(cv, 446, 22, 8, -30, K("cielo", 3))


def _calle(cv, rnd):
    # acera de losas
    cv.rect(0, FACHADA, W, 120, K("gris", 3))
    for y in range(FACHADA, 120, 9):
        cv.hline(0, W, y, K("gris", 2))
        for x in range((y // 9 % 2) * 11, W, 22):
            cv.vline(x, y, min(120, y + 9), K("gris", 2))
            if rnd.random() < 0.3:
                cv.hline(x + 2, x + rnd.randint(5, 12), y + 1, K("gris", 4))
    cv.rect(0, 120, W, 124, K("gris", 4)); cv.hline(0, W, 120, K("gris", 6)); cv.hline(0, W, 123, K("gris", 1))   # bordillo
    # calzada de adoquín
    P.adoquines(cv, 0, 124, W, SUELO_FIN, semilla=1301, rampa="gris", base=3)
    cv.rect(0, 124, W, 127, K("gris", 1))                                            # arroyo
    # vías del tranvía, sin uso desde hace años: el adoquín se las va comiendo
    for ry in (168, 186):
        cv.hline(0, W, ry, K("gris", 5)); cv.hline(0, W, ry + 1, K("gris", 1))
        for x in range(rnd.randint(0, 30), W, 53):
            cv.hline(x, x + rnd.randint(4, 12), ry, K("madera", 3))                   # óxido
    # alcantarilla, charcos y papeles
    cv.rect(228, 124, 248, 128, K("gris", 0))
    for k in range(230, 247, 3):
        cv.vline(k, 124, 128, K("gris", 3))
    for (cx, cy, rw) in ((96, 176, 22), (330, 214, 16), (170, 232, 12)):
        cv.ellipse(cx - rw, cy - 5, cx + rw, cy + 5, K("cielo", 2), outline=K("gris", 2))
        cv.hline(cx - rw + 5, cx + rw - 8, cy - 2, K("cielo", 5))
        cv.hline(cx - rw + 9, cx + rw - 14, cy, K("cielo", 4))
    for (px_, py_) in ((268, 104), (60, 112), (380, 190), (440, 230)):
        cv.rect(px_, py_, px_ + 9, py_ + 6, K("papel", 2)); cv.hline(px_ + 1, px_ + 8, py_ + 2, K("papel", 0))
    # una rata junto a la boca
    cv.rect(286, 100, 292, 103, K("gris", 1)); cv.px(292, 101, K("gris", 1)); cv.px(293, 101, K("gris", 1))
    cv.d.line([(285, 102), (280, 104)], fill=K("gris", 1))
    # fondo: el pretil del río (abajo), piedra y bolardos de hierro
    cv.rect(0, SUELO_FIN, W, SUELO_FIN + 3, K("gris", 4)); cv.hline(0, W, SUELO_FIN, K("gris", 6))
    cv.rect(0, SUELO_FIN + 3, W, H, K("gris", 2))
    for x in range(0, W, 24):
        cv.vline(x, SUELO_FIN + 3, H, K("gris", 1))
        cv.hline(x + 2, x + 20, SUELO_FIN + 5, K("gris", 3))
    for bx in range(30, W, 96):
        cv.ellipse(bx, SUELO_FIN - 6, bx + 10, SUELO_FIN + 2, K("gris", 1), outline=K("gris", 0))
        cv.ellipse(bx + 2, SUELO_FIN - 5, bx + 8, SUELO_FIN - 1, K("gris", 3))


def _niebla(cv):
    """Velo de niebla: denso a ras de la acera, más ralo arriba y abajo, con jirones que se mueven al este."""
    px = cv.img.load()
    color = K("cielo", 5)
    for y in range(H):
        for x in range(W):
            # perfil vertical: el banco de niebla del río se posa sobre la calle
            if y < FACHADA:
                base = 0.1 + 0.26 * (y / FACHADA) ** 2
            else:
                t = (y - FACHADA) / (SUELO_FIN - FACHADA)
                base = 0.4 - 0.26 * t
            # jirones: bandas onduladas
            j = math.sin(x / 61.0 + y / 4.0) + 0.6 * math.sin(x / 23.0 - y / 3.0 + 1.7) + 0.5 * math.sin(x / 97.0 + 2.3)
            k = base + (0.09 if j > 0.9 else (0.04 if j > 0.2 else 0.0))
            k = round(k / 0.06) * 0.06
            if k <= 0:
                continue
            col = px[x, y]
            px[x, y] = tuple(int(col[c] * (1 - k) + color[c] * k) for c in range(3))


def dibujar(variante=None):
    rnd = random.Random(1301)
    cv = Canvas(W, H, bg=("cielo", 4))
    _cielo(cv, rnd)
    _edificio_izquierdo(cv, rnd)
    _pintada(cv, rnd)
    _edificio_derecho(cv, rnd)
    _estacion(cv, rnd)
    _tablones(cv, rnd)
    _cartel(cv, rnd)
    _calle(cv, rnd)
    P.farola(cv, *FAROLA, encendida=False)
    # luz de amanecer: plana y fría; las bocas y portales hundidos, más oscuros
    cv.add_light(0, 0, W, H, 0)
    cv.add_light(0, SUELO_FIN, W, H, -1)
    cv.glow_rgb = K("azul", 2)
    cv.add_glow_suave(240, 180, 400, 0.12, squash=1.6, pasos=4)
    cv.bake_lighting()
    _niebla(cv)
    # el sol, apenas una mancha más clara detrás de la niebla, por el este (derecha)
    L.glow_post(cv, 470, 6, 120, 0.22, K("papel", 3), squash=1.4, pasos=5)
    return cv
