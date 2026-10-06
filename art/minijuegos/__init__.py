"""Arte de los minijuegos (M6). Cada módulo expone exportar(destino) -> lista de PNG escritos.

Los PNG van a public/assets/minijuegos/ con el prefijo del minijuego (palanca-*, llaves-*, …) y cada
escena los carga en su propio preload().

Uso: python3 art/minijuegos/__init__.py   (o, desde otro script: import minijuegos; minijuegos.exportar(destino))
"""
import importlib
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

MODULOS = ("palanca", "llaves", "combinacion", "pancarta", "sammy", "resistencia")
# los minijuegos «de papel» (ficha, parte, diario, …) se exportan juntos desde papel.py
if (AQUI / "papel.py").exists():
    MODULOS += ("papel",)


def exportar(destino=None, modulos=MODULOS):
    destino = Path(destino) if destino else AQUI.parents[1] / "public" / "assets" / "minijuegos"
    hechos = []
    for nombre in modulos:
        hechos += importlib.import_module(nombre).exportar(destino)
    return hechos


if __name__ == "__main__":
    for n in exportar(modulos=sys.argv[1:] or MODULOS):
        print("ok", n)
