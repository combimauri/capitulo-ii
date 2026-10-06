"""Iconos de inventario (16x16) e ilustraciones del minijuego de los escombros."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from PIL import Image  # noqa: E402
from pixel import Canvas, K  # noqa: E402


def _rgba(cv):
    """Convierte el fondo (gris 0) en transparente."""
    img = cv.img.convert("RGBA")
    fondo = K("gris", 0) + (255,)
    datos = [(0, 0, 0, 0) if p == fondo else p for p in img.getdata()]
    img.putdata(datos)
    return img


def icono_reloj():
    cv = Canvas(16, 16)
    cv.rect(6, 1, 10, 4, K("madera", 2)); cv.rect(6, 12, 10, 15, K("madera", 2))
    cv.ellipse(2, 3, 14, 14, K("papel", 3), outline=K("gris", 2))
    cv.px(8, 8, K("gris", 0)); cv.px(8, 7, K("gris", 0)); cv.px(8, 6, K("gris", 0)); cv.px(9, 9, K("gris", 0))
    cv.d.line([4, 5, 12, 11], fill=K("cielo", 5))  # cristal roto
    return _rgba(cv)


def icono_ficha():
    cv = Canvas(16, 16)
    cv.rect(2, 2, 14, 14, K("papel", 2)); cv.frame(2, 2, 14, 14, K("papel", 0))
    cv.rect(4, 4, 8, 9, K("gris", 5)); cv.px(6, 5, K("piel", 3)); cv.rect(5, 6, 7, 8, K("azul", 2))
    for y in (5, 7, 9):
        cv.hline(9, 13, y, K("gris", 3))
    cv.ellipse(8, 9, 13, 14, None, outline=K("rojo", 3))
    return _rgba(cv)


def icono_lapiz():
    cv = Canvas(16, 16)
    cv.d.line([3, 13, 12, 4], fill=K("ocre", 2), width=2)
    cv.px(13, 3, K("gris", 1)); cv.px(12, 3, K("madera", 4))
    cv.px(3, 13, K("madera", 1)); cv.px(4, 12, K("madera", 1))
    return _rgba(cv)


def icono_foto():
    cv = Canvas(16, 16)
    cv.rect(2, 3, 14, 13, K("papel", 3)); cv.rect(3, 4, 13, 11, K("gris", 5))
    cv.px(6, 7, K("piel", 3)); cv.px(10, 7, K("piel", 3))
    cv.poly([(2, 3), (5, 3), (2, 7)], K("madera", 0))  # borde quemado
    return _rgba(cv)


def icono_diario():
    cv = Canvas(16, 16)
    cv.rect(3, 2, 13, 14, K("gris", 1)); cv.frame(3, 2, 13, 14, K("gris", 3))
    cv.vline(5, 2, 14, K("gris", 3)); cv.px(9, 7, K("papel", 3)); cv.px(10, 6, K("papel", 3))
    return _rgba(cv)


def icono_compas():
    cv = Canvas(16, 16)
    cv.ellipse(6, 1, 10, 5, K("ocre", 3), outline=K("ocre", 1))                    # bisagra
    cv.d.line([7, 4, 3, 14], fill=K("ocre", 2)); cv.d.line([9, 4, 13, 14], fill=K("ocre", 2))
    cv.px(3, 14, K("gris", 6)); cv.px(13, 14, K("gris", 1))                        # punta y mina
    cv.hline(5, 11, 9, K("ocre", 1))
    return _rgba(cv)


def icono_zonificacion():
    cv = Canvas(16, 16)
    cv.rect(2, 2, 14, 14, K("cielo", 6)); cv.frame(2, 2, 14, 14, K("cielo", 4))
    cv.poly([(3, 3), (9, 3), (8, 9), (3, 8)], K("papel", 4))                       # distritos del Partido
    cv.poly([(9, 3), (13, 3), (13, 13), (5, 13), (8, 9)], K("madera", 3))          # proletarios
    cv.ellipse(9, 9, 13, 13, None, outline=K("rojo", 3))                          # sello
    return _rgba(cv)


def icono_nota():
    cv = Canvas(16, 16)
    cv.poly([(2, 4), (13, 2), (14, 12), (3, 14)], K("papel", 3))
    for y in (6, 8, 10):
        cv.hline(4, 11, y, K("gris", 4))
    cv.px(11, 4, K("gris", 1)); cv.px(10, 3, K("gris", 1)); cv.px(12, 3, K("gris", 1))   # pájaro
    return _rgba(cv)


def icono_metralla():
    cv = Canvas(16, 16)
    cv.d.line([4, 1, 8, 6], fill=K("madera", 3)); cv.d.line([12, 1, 8, 6], fill=K("madera", 3))   # cordel
    cv.poly([(6, 6), (11, 5), (13, 9), (9, 14), (4, 11)], K("gris", 4))
    cv.d.line([(6, 6), (11, 5), (13, 9)], fill=K("gris", 6)); cv.px(8, 9, K("granate", 2))
    return _rgba(cv)


def icono_tarjeta():
    cv = Canvas(16, 16)
    cv.rect(1, 4, 15, 12, K("papel", 4)); cv.frame(1, 4, 15, 12, K("papel", 1))
    cv.rect(3, 6, 6, 9, K("gris", 2)); cv.px(4, 7, K("papel", 4))                 # una camarita
    cv.hline(8, 13, 7, K("gris", 3)); cv.hline(8, 12, 9, K("gris", 4))
    return _rgba(cv)


def icono_metralla_brillante():
    cv = Canvas(16, 16)
    cv.poly([(4, 7), (10, 3), (14, 8), (9, 13), (3, 11)], K("gris", 6))
    cv.d.line([(4, 7), (10, 3), (14, 8)], fill=K("papel", 4)); cv.px(9, 6, K("papel", 4)); cv.px(8, 7, K("gris", 8))
    return _rgba(cv)


def icono_parte():
    cv = Canvas(16, 16)
    cv.rect(3, 1, 13, 15, K("papel", 3)); cv.frame(3, 1, 13, 15, K("papel", 0))
    for y in (4, 6, 8, 10):
        cv.hline(5, 11, y, K("gris", 3))
    cv.ellipse(7, 10, 13, 15, None, outline=K("rojo", 3)); cv.px(10, 12, K("rojo", 3))
    return _rgba(cv)


def icono_foto_restaurada():
    cv = Canvas(16, 16)
    cv.rect(2, 3, 14, 13, K("papel", 4)); cv.rect(3, 4, 13, 11, K("papel", 1))
    cv.rect(5, 6, 7, 8, K("piel", 3)); cv.rect(9, 6, 11, 8, K("piel", 3))
    cv.hline(5, 7, 9, K("rojo", 3))                                       # la sonrisa de Ivy
    return _rgba(cv)


def icono_llave():
    cv = Canvas(16, 16)
    cv.ellipse(1, 3, 8, 10, None, outline=K("ocre", 1)); cv.ellipse(2, 4, 7, 9, None, outline=K("ocre", 2))
    cv.rect(7, 6, 15, 7, K("ocre", 1)); cv.rect(12, 8, 13, 10, K("ocre", 1)); cv.rect(14, 8, 15, 9, K("ocre", 1))
    cv.px(10, 6, K("madera", 2)); cv.px(4, 8, K("madera", 2))                       # óxido
    return _rgba(cv)


# ---------------------------------------------------------------- Acto III


def _hoja(cv, x0=3, y0=1, x1=13, y1=15, tono=3, borde=0):
    cv.rect(x0, y0, x1, y1, K("papel", tono)); cv.frame(x0, y0, x1, y1, K("papel", borde))


def icono_directiva():
    cv = Canvas(16, 16)
    _hoja(cv, tono=4)
    cv.poly([(5, 5), (8, 2), (11, 5)], K("gris", 2))                                 # membrete: la pirámide
    cv.hline(4, 12, 6, K("rojo", 3))
    for y in (8, 10, 12):
        cv.hline(5, 11, y, K("gris", 3))
    cv.hline(5, 9, 14, K("gris", 4))
    return _rgba(cv)


def icono_copia_planilla():
    cv = Canvas(16, 16)
    _hoja(cv, tono=3, borde=1)
    for y in (3, 6, 9, 12):                                                           # letra a lápiz, temblorosa
        for x in range(5, 12):
            cv.px(x, y + (x % 3 == 0), K("gris", 5))
    cv.d.line([12, 14, 15, 11], fill=K("ocre", 2)); cv.px(11, 15, K("gris", 2))      # el lápiz
    return _rgba(cv)


def icono_hoja_planilla():
    cv = Canvas(16, 16)
    _hoja(cv)
    cv.rect(3, 1, 13, 15, K("cielo", 6)); cv.frame(3, 1, 13, 15, K("cielo", 4))     # papel azul pálido
    cv.hline(5, 11, 3, K("azul", 1))
    for y, x1 in ((6, 12), (8, 11), (10, 12), (12, 9)):                               # renglones a máquina
        for x in range(5, x1):
            if (x * 7 + y) % 5:
                cv.px(x, y, K("azul", 2))
    return _rgba(cv)


def icono_libro():
    cv = Canvas(16, 16)
    for i, t in enumerate((1, 2, 3)):                                                 # fajo de hojas desalineadas
        cv.rect(3 + i, 3 - i, 13 + i, 14 - i, K("papel", t)); cv.frame(3 + i, 3 - i, 13 + i, 14 - i, K("papel", 0))
    for y in (4, 6, 8, 10):
        cv.hline(7, 14, y, K("gris", 4))
    for y in (2, 6, 10):                                                              # cosido con hilo
        cv.px(5, y, K("granate", 2)); cv.px(6, y + 1, K("granate", 3)); cv.px(5, y + 2, K("granate", 2))
    return _rgba(cv)


def _periodico(cv, a, b, c):
    cv.poly([(1, 3), (13, 2), (14, 13), (2, 14)], a)
    cv.d.line([(1, 3), (13, 2)], fill=c); cv.d.line([(7, 2), (8, 14)], fill=b)       # pliegue
    cv.d.line([(2, 4), (12, 4)], fill=K("gris", 2)); cv.d.line([(2, 5), (12, 5)], fill=K("gris", 3))  # cabecera del Times
    for y in (7, 9, 11):
        cv.hline(3, 7, y, K("gris", 4))
    cv.hline(9, 13, 11, K("gris", 4))
    cv.rect(9, 7, 13, 9, K("gris", 5))                                                # foto


def icono_times_falso():
    cv = Canvas(16, 16)
    _periodico(cv, K("papel", 4), K("papel", 2), K("gris", 10))
    return _rgba(cv)


def icono_times_original():
    cv = Canvas(16, 16)
    _periodico(cv, K("ocre", 4), K("ocre", 2), K("ocre", 3))
    cv.px(2, 13, K("ocre", 2)); cv.px(12, 3, K("ocre", 2)); cv.px(13, 12, K("madera", 4))   # manchas del tiempo
    return _rgba(cv)


def icono_sobre_encerado():
    cv = Canvas(16, 16)
    cv.rect(1, 4, 15, 13, K("ocre", 3)); cv.frame(1, 4, 15, 13, K("ocre", 1))
    cv.d.line([(1, 4), (8, 9), (14, 4)], fill=K("ocre", 1))                          # solapa
    cv.px(4, 10, K("ocre", 4)); cv.px(5, 11, K("ocre", 4)); cv.px(11, 6, K("papel", 4))   # brillo de la cera
    return _rgba(cv)


def icono_chapa():
    cv = Canvas(16, 16)
    cv.ellipse(6, 1, 10, 5, None, outline=K("gris", 5))                               # anilla
    cv.ellipse(2, 3, 14, 15, K("gris", 6), outline=K("gris", 3))
    cv.ellipse(4, 5, 12, 13, K("gris", 7))
    cv.text(4, 7, "41", K("gris", 2))
    cv.px(5, 5, K("gris", 9)); cv.px(4, 6, K("gris", 9))
    return _rgba(cv)


def icono_foto_sotano():
    cv = Canvas(16, 16)
    cv.rect(2, 2, 14, 14, K("papel", 4)); cv.rect(3, 3, 13, 12, K("madera", 2))      # sepia
    cv.ellipse(4, 3, 13, 12, K("madera", 4)); cv.ellipse(6, 5, 11, 10, K("madera", 5))   # halo de la vela
    cv.vline(8, 8, 11, K("papel", 4)); cv.px(8, 7, K("ocre", 4)); cv.px(8, 6, K("ocre", 3))   # la vela
    for x in (4, 11):                                                                 # dos figuras a contraluz
        cv.rect(x, 7, x + 2, 12, K("madera", 1)); cv.px(x + (1 if x < 8 else 0), 6, K("madera", 1))
    return _rgba(cv)


def icono_dibujos_amory():
    cv = Canvas(16, 16)
    cv.poly([(1, 5), (10, 2), (12, 11), (3, 13)], K("papel", 2))
    cv.poly([(4, 4), (14, 4), (14, 14), (4, 14)], K("papel", 4)); cv.frame(4, 4, 14, 14, K("papel", 1))
    for (x, y) in ((5, 6), (8, 10)):                                                  # pájaros en vuelo
        for dx, dy in ((0, 0), (1, 1), (2, 2), (3, 1), (4, 0)):
            cv.px(x + dx, y + dy, K("gris", 2))
    cv.px(11, 6, K("gris", 4)); cv.px(12, 7, K("gris", 4)); cv.px(13, 6, K("gris", 4))
    return _rgba(cv)


def icono_carpeta():
    cv = Canvas(16, 16)
    cv.rect(1, 3, 7, 5, K("madera", 4))                                               # pestaña
    cv.rect(1, 4, 15, 14, K("madera", 5)); cv.frame(1, 4, 15, 14, K("madera", 3))
    cv.rect(3, 2, 13, 4, K("papel", 4))                                               # hojas asomando
    cv.rect(4, 8, 12, 11, K("papel", 3)); cv.hline(5, 11, 9, K("gris", 4))           # etiqueta
    return _rgba(cv)


def icono_tubo():
    cv = Canvas(16, 16)
    cv.d.line([(2, 11), (11, 2)], fill=K("madera", 4), width=4)
    cv.d.line([(1, 10), (10, 1)], fill=K("madera", 5))
    cv.ellipse(9, 0, 14, 5, K("rojo", 2)); cv.ellipse(10, 1, 13, 4, K("rojo", 3)); cv.px(11, 2, K("rojo", 5))  # tapa lacrada
    cv.d.line([(5, 9), (8, 12)], fill=K("madera", 2)); cv.d.line([(1, 12), (3, 14)], fill=K("madera", 2))
    return _rgba(cv)


def icono_mapa_malabar():
    cv = Canvas(16, 16)
    for i, x in enumerate(range(1, 15, 5)):                                           # pliegues en acordeón
        cv.rect(x, 3, min(x + 5, 15), 14, K("papel", 4 if i % 2 == 0 else 3))
    cv.d.line([(1, 12), (6, 9), (10, 10), (14, 6)], fill=K("cielo", 3))              # el río
    for (x, y) in ((4, 9), (9, 8), (12, 5)):                                          # banderitas negras
        cv.vline(x, y - 4, y, K("gris", 2)); cv.rect(x + 1, y - 4, x + 3, y - 2, K("gris", 1))
    return _rgba(cv)


def icono_parte_original():
    cv = Canvas(16, 16)
    _hoja(cv, tono=3)
    cv.hline(4, 12, 3, K("gris", 2))
    for y in (5, 7, 9):
        cv.hline(5, 11, y, K("gris", 3))
    cv.ellipse(6, 9, 13, 15, K("rojo", 3)); cv.ellipse(7, 10, 12, 14, K("papel", 3))  # sello
    cv.hline(8, 11, 12, K("rojo", 3)); cv.px(9, 11, K("rojo", 3))
    return _rgba(cv)


# ---------------------------------------------------------------- Acto IV


def icono_carta_ivy():
    """Un trozo de papel cuadriculado, arrancado de un cuaderno escolar y doblado muchas veces."""
    cv = Canvas(16, 16)
    cv.rect(2, 3, 14, 14, K("papel", 4))
    cv.rect(8, 3, 14, 14, K("papel", 3))                                              # la mitad doblada, en sombra
    for x in (4, 7, 10, 13):                                                          # cuadrícula azul pálido
        cv.vline(x, 3, 14, K("cielo", 6))
    for y in (5, 8, 11):
        cv.hline(2, 14, y, K("cielo", 6))
    cv.vline(8, 3, 14, K("papel", 1))                                                 # pliegue central
    cv.hline(2, 14, 13, K("papel", 2))
    cv.frame(2, 3, 14, 14, K("papel", 1))
    for x in range(2, 14, 2):                                                         # borde arrancado del cuaderno
        cv.px(x, 3, K("gris", 0))
    for y, tramos in ((6, ((3, 6), (9, 13))), (9, ((3, 7), (9, 12))), (12, ((3, 5),))):   # letra a lápiz de una niña
        for x0, x1 in tramos:
            for x in range(x0, x1):
                cv.px(x, y - (x % 3 == 1), K("gris", 5))
    cv.poly([(11, 13), (13, 11), (13, 13)], K("papel", 2))                            # esquina doblada
    cv.px(13, 13, K("gris", 0)); cv.px(13, 12, K("papel", 1))
    return _rgba(cv)


def icono_linterna():
    """Linterna de dinamo: cuerpo de baquelita, cristal ámbar y la manivela plegada a un lado."""
    cv = Canvas(16, 16)
    cv.rect(2, 5, 12, 14, K("gris", 5)); cv.frame(2, 5, 12, 14, K("gris", 2))
    cv.hline(3, 11, 6, K("gris", 7)); cv.vline(3, 6, 13, K("gris", 6))               # brillo del borde
    cv.hline(3, 12, 13, K("gris", 4))
    cv.rect(11, 4, 15, 15, K("gris", 6)); cv.frame(11, 4, 15, 15, K("gris", 2))      # aro del cristal
    cv.rect(12, 6, 14, 13, K("ocre", 3)); cv.px(12, 7, K("ocre", 4)); cv.px(12, 8, K("ocre", 4))
    cv.vline(13, 7, 13, K("ocre", 2))
    cv.ellipse(5, 8, 10, 13, K("gris", 4), outline=K("gris", 2))                       # tapa de la dinamo
    cv.d.line([(7, 10), (4, 3)], fill=K("gris", 2))                                    # la manivela
    cv.px(7, 10, K("gris", 8))
    cv.rect(3, 1, 5, 3, K("madera", 4)); cv.px(3, 1, K("madera", 6))                  # pomo de madera
    return _rgba(cv)


def icono_tiza():
    """Un cabo de tiza, gastado por una punta, y el polvo que deja."""
    cv = Canvas(16, 16)
    cv.d.line([(3, 12), (11, 4)], fill=K("gris", 9), width=3)
    cv.d.line([(3, 11), (10, 4)], fill=K("gris", 10))
    cv.d.line([(4, 13), (12, 5)], fill=K("gris", 7))
    cv.px(12, 4, K("gris", 8)); cv.px(11, 3, K("gris", 9))                            # punta gastada
    cv.px(2, 12, K("gris", 8)); cv.px(3, 13, K("gris", 7))
    for (x, y) in ((11, 11), (13, 9), (12, 13), (14, 12)):                            # polvo
        cv.px(x, y, K("gris", 6))
    return _rgba(cv)


def icono_libro_completo():
    """El libro entero: un fajo grueso cosido con hilo; el capítulo nuevo, en medio, en papel más claro."""
    cv = Canvas(16, 16)
    cv.poly([(1, 7), (4, 2), (15, 2), (12, 7)], K("papel", 3))                       # hoja de arriba
    for y, x0, x1 in ((3, 7, 13), (5, 5, 11)):
        cv.hline(x0, x1, y, K("papel", 1))
    cv.d.line([(1, 7), (4, 2), (15, 2)], fill=K("papel", 1))
    cv.rect(1, 7, 13, 15, K("papel", 1))                                              # canto grueso de las hojas
    cv.poly([(12, 7), (15, 2), (15, 10), (12, 15)], K("papel", 0))                    # lado en sombra
    for y in (8, 10, 13):
        cv.hline(1, 13, y, K("papel", 2))
    cv.rect(1, 11, 13, 13, K("papel", 4))                                             # el capítulo nuevo: más claro
    cv.hline(1, 13, 14, K("papel", 0))
    for x in (3, 7):                                                                  # cosido con hilo por el lomo
        cv.d.line([(x + 2, 3), (x, 7)], fill=K("granate", 4))
        cv.vline(x, 7, 15, K("granate", 3))
    cv.px(9, 15, K("granate", 3)); cv.px(10, 15, K("granate", 2))                     # cabo del hilo
    return _rgba(cv)


ICONOS = {"icono-reloj": icono_reloj, "icono-ficha": icono_ficha, "icono-lapiz": icono_lapiz,
          "icono-foto": icono_foto, "icono-diario": icono_diario, "icono-compas": icono_compas,
          "icono-zonificacion": icono_zonificacion, "icono-nota": icono_nota, "icono-metralla": icono_metralla,
          "icono-tarjeta": icono_tarjeta, "icono-metralla-brillante": icono_metralla_brillante,
          "icono-parte": icono_parte, "icono-foto-restaurada": icono_foto_restaurada, "icono-llave": icono_llave,
          "icono-directiva": icono_directiva, "icono-copia_planilla": icono_copia_planilla,
          "icono-hoja_planilla": icono_hoja_planilla, "icono-libro": icono_libro,
          "icono-times_falso": icono_times_falso, "icono-times_original": icono_times_original,
          "icono-sobre_encerado": icono_sobre_encerado, "icono-chapa": icono_chapa,
          "icono-foto_sotano": icono_foto_sotano, "icono-dibujos_amory": icono_dibujos_amory,
          "icono-carpeta": icono_carpeta, "icono-tubo": icono_tubo, "icono-mapa_malabar": icono_mapa_malabar,
          "icono-parte_original": icono_parte_original,
          "icono-carta_ivy": icono_carta_ivy, "icono-linterna": icono_linterna, "icono-tiza": icono_tiza,
          "icono-libro_completo": icono_libro_completo}


def cascotes_fondo():
    """Primer plano: polvo, escombros y la mano de Ivy asomando (480x270)."""
    random.seed(79)
    cv = Canvas(480, 270, bg=("gris", 1))
    for _ in range(2600):
        x, y = random.randint(0, 479), random.randint(0, 269)
        cv.px(x, y, K("gris", random.choice([2, 2, 3])))
    # resplandor del fuego (arriba a la derecha), con caída gradual
    cv.glow_rgb = K("ocre", 2)
    cv.add_glow_suave(420, 20, 260, 0.35, squash=1.3)
    cv.bake_lighting()
    # escombros del fondo
    for _ in range(40):
        x, y = random.randint(140, 360), random.randint(150, 230)
        w, h = random.randint(16, 40), random.randint(8, 18)
        cv.rect(x, y, x + w, y + h, K("granate", random.choice([2, 3, 4])))
        cv.hline(x, x + w, y, K("granate", 5))
    # viga
    cv.poly([(110, 120), (370, 170), (366, 184), (106, 134)], K("madera", 1))
    cv.d.line([(110, 120), (370, 170)], fill=K("madera", 3))
    # la mano de Ivy (abierta, polvorienta) y la manga azul
    cv.poly([(168, 176), (226, 158), (232, 172), (172, 192)], K("azul", 1))
    cv.ellipse(222, 152, 246, 176, K("piel", 2))
    for i, (x0, y0) in enumerate([(244, 150), (246, 156), (246, 163), (244, 169)]):
        cv.rect(x0, y0, x0 + 9 - i, y0 + 4, K("piel", 3)); cv.hline(x0, x0 + 9 - i, y0, K("piel", 4))
    cv.rect(228, 147, 236, 153, K("piel", 3))  # pulgar
    # el reloj en la muñeca, parado
    cv.rect(214, 158, 222, 170, K("gris", 2)); cv.ellipse(215, 160, 221, 168, K("papel", 3))
    cv.px(218, 162, K("gris", 0)); cv.px(219, 164, K("gris", 0))
    for _ in range(140):  # polvo sobre la piel
        x, y = random.randint(214, 256), random.randint(148, 176)
        if cv.img.getpixel((x, y)) in (K("piel", 2), K("piel", 3), K("piel", 4)):
            cv.px(x, y, K("papel", 1))
    return cv.img


def cascote(i):
    random.seed(i * 13)
    cv = Canvas(52, 36)
    pts = [(4, 10), (20, 2), (46, 6), (50, 24), (34, 34), (8, 30)]
    cv.poly(pts, K("granate", 3 + i % 2))
    cv.poly([(4, 10), (20, 2), (46, 6), (40, 12), (12, 14)], K("granate", 5))
    cv.d.line(pts + [pts[0]], fill=K("granate", 1))
    for _ in range(30):
        cv.px(random.randint(10, 44), random.randint(10, 28), K("granate", 2))
    if i == 2:
        cv.rect(14, 16, 36, 22, K("papel", 2))   # trozo de yeso
    return _rgba(cv)


# cifras de esfera, más redondas que las de la fuente 3x5 (se pintan a doble tamaño)
CIFRAS = {"0": "111101101101111", "1": "010110010010111", "2": "111001111100111", "3": "111001011001111",
          "4": "101101111001001", "5": "111100111001111", "6": "111100111101111", "7": "111001001010010",
          "8": "111101111101111", "9": "111101111001111"}


def _texto2x(cv, x, y, s, col):
    """Cifras de 3x5 a doble tamaño (6x10)."""
    for ch in s:
        for i, b in enumerate(CIFRAS[ch]):
            if b == "1":
                cv.rect(x + (i % 3) * 2, y + (i // 3) * 2, x + (i % 3) * 2 + 2, y + (i // 3) * 2 + 2, col)
        x += 8


def reloj_ivy_grande():
    """La esfera del reloj de Ivy vista de cerca (160x160), sin agujas: el juego las dibuja encima.

    Centro en (80, 80) y esfera de radio 64. Caja de acero barato, números pintados, el cristal roto en
    diagonal (como en el icono) y la correa de cuero asomando arriba y abajo.
    """
    import math
    cv = Canvas(160, 160)
    C = 80
    # correa: arriba y abajo, cortada por el borde
    for y0, y1 in ((0, 30), (130, 160)):
        cv.rect(54, y0, 107, y1, K("madera", 3))
        cv.vline(54, y0, y1, K("madera", 1)); cv.vline(106, y0, y1, K("madera", 1))
        cv.vline(55, y0, y1, K("madera", 4)); cv.vline(105, y0, y1, K("madera", 2))
        for y in range(y0 + 1, y1, 4):                                                     # pespunte
            cv.vline(59, y, y + 2, K("madera", 5)); cv.vline(101, y, y + 2, K("madera", 5))
        for y in range(y0, y1, 9):                                                         # grano del cuero
            cv.hline(66, 72, y + 3, K("madera", 2)); cv.hline(84, 92, y + 7, K("madera", 2))
    cv.ellipse(76, 150, 85, 156, K("madera", 1)); cv.ellipse(77, 151, 84, 155, K("madera", 0))    # agujero de la hebilla
    cv.hline(77, 84, 155, K("madera", 4))
    # asas de la caja
    for x0 in (56, 94):
        for y0, y1 in ((20, 34), (126, 140)):
            cv.rect(x0, y0, x0 + 11, y1, K("gris", 6)); cv.vline(x0, y0, y1, K("gris", 8)); cv.vline(x0 + 10, y0, y1, K("gris", 4))
            cv.rect(x0 + 3, y0 + 2, x0 + 8, y1 - 2, K("gris", 5))
    # caja de acero
    cv.ellipse(10, 10, 150, 150, K("gris", 5), outline=K("gris", 2))
    cv.d.arc([12, 12, 148, 148], 150, 300, fill=K("gris", 8), width=3)                      # luz arriba a la izquierda
    cv.d.arc([12, 12, 148, 148], 330, 120, fill=K("gris", 3), width=3)                      # sombra abajo a la derecha
    # corona
    cv.rect(149, 72, 157, 89, K("gris", 6)); cv.frame(149, 72, 157, 89, K("gris", 2))
    for y in range(74, 88, 2):
        cv.hline(150, 156, y, K("gris", 4))
    cv.vline(149, 72, 89, K("gris", 3))
    # bisel y esfera
    cv.ellipse(15, 15, 145, 145, K("gris", 3))
    cv.ellipse(16, 16, 144, 144, K("papel", 3))
    cv.ellipse(19, 19, 141, 141, K("papel", 4))
    cv.d.arc([19, 19, 141, 141], 20, 110, fill=K("papel", 3), width=2)                      # la esfera, amarilleada
    # marcas de minutos y de horas
    for i in range(60):
        a = i / 60 * 2 * math.pi
        if i % 5 == 0:
            cv.d.line([(C + math.sin(a) * 51, C - math.cos(a) * 51), (C + math.sin(a) * 60, C - math.cos(a) * 60)],
                      fill=K("gris", 2), width=2)
        else:
            for r in range(57, 61):
                cv.px(int(C + math.sin(a) * r), int(C - math.cos(a) * r), K("gris", 5))
    # números
    for h in range(1, 13):
        a = h / 12 * 2 * math.pi
        t = str(h)
        w = len(t) * 8 - 2
        x, y = C + math.sin(a) * 42, C - math.cos(a) * 42
        _texto2x(cv, int(round(x - w / 2)), int(round(y - 5)), t, K("gris", 1))
    # cristal roto en diagonal (de arriba a la izquierda abajo a la derecha), con el punto del golpe y sus astillas
    grieta = [(22, 32), (31, 41), (38, 44), (47, 52), (55, 57), (63, 64), (71, 69), (80, 78), (89, 84), (98, 93),
              (106, 101), (114, 106), (122, 115), (130, 124), (137, 129)]
    cv.d.line(grieta, fill=K("gris", 3))
    cv.d.line([(x + 1, y - 1) for x, y in grieta], fill=K("gris", 10))                       # filo que brilla
    for rama in ([(55, 57), (50, 66)], [(55, 57), (60, 48)], [(55, 57), (46, 55)], [(55, 57), (64, 60)],
                 [(89, 84), (97, 80)], [(89, 84), (86, 92)], [(114, 106), (119, 101)], [(31, 41), (28, 48)]):
        cv.d.line(rama, fill=K("gris", 5))
        cv.d.line([(x + 1, y - 1) for x, y in rama[1:]] + [(rama[0][0] + 1, rama[0][1] - 1)], fill=K("gris", 10))
    cv.ellipse(52, 54, 59, 61, None, outline=K("gris", 6))                                  # el punto del golpe
    # reflejo del cristal
    cv.d.arc([24, 24, 136, 136], 205, 245, fill=K("gris", 10), width=2)
    cv.d.arc([30, 30, 130, 130], 215, 232, fill=K("gris", 10))
    return _rgba(cv)


def exportar(iconos_dir, minijuegos_dir):
    iconos_dir, minijuegos_dir = Path(iconos_dir), Path(minijuegos_dir)
    iconos_dir.mkdir(parents=True, exist_ok=True)
    minijuegos_dir.mkdir(parents=True, exist_ok=True)
    for nombre, f in ICONOS.items():
        f().save(iconos_dir / f"{nombre}.png")
    cascotes_fondo().save(minijuegos_dir / "cascotes-fondo.png")
    for i in (1, 2, 3):
        cascote(i).save(minijuegos_dir / f"cascote-{i}.png")
    reloj_ivy_grande().save(minijuegos_dir / "reloj-ivy-grande.png")
