"""Escenarios del juego. Cada módulo expone dibujar(...) -> Canvas."""
import subprocess
import sys
from pathlib import Path

ART = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ART / "lib"))
sys.path.insert(0, str(ART / "personajes"))
sys.path.insert(0, str(Path(__file__).resolve().parent))


def exportar(destino):
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    hechos = []
    import stepney
    stepney.dibujar("escombros").img.save(destino / "stepney.png"); hechos.append("stepney")
    stepney.dibujar("ivy").img.save(destino / "stepney_ivy.png"); hechos.append("stepney_ivy")
    for nombre, flags in (("piso", []), ("piso_noche", ["--noche"])):
        subprocess.run([sys.executable, str(ART / "pruebas" / "piso_hd.py"), "--sin-protagonista", *flags,
                        f"--salida={destino / (nombre + '.png')}"], check=True, capture_output=True)
        hechos.append(nombre)
    for modulo in ("escalera", "avenida", "vestibulo", "departamento", "cantina", "salon_odio", "despacho_voss", "centro", "sueno"):
        try:
            m = __import__(modulo)
        except ModuleNotFoundError:
            continue
        m.dibujar().img.save(destino / f"{modulo}.png")
        hechos.append(modulo)
    return hechos
