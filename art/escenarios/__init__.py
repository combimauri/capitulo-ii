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
    for modulo in ("escalera", "avenida", "vestibulo", "departamento", "cantina", "salon_odio", "despacho_voss", "centro", "sueno", "pasillo", "limehouse", "pub", "mercado", "estudio", "archivo", "suministros",
                   "calderas", "planta11", "archivo_restringido", "sotano_pub", "lavabos", "casa_dot",
                   "miniver", "minimor", "minimor_archivo", "callejones",
                   "celda", "sala_obrien", "cafe", "shadwell", "tunel", "anden_taller", "cripta"):
        try:
            m = __import__(modulo)
        except ModuleNotFoundError:
            continue
        m.dibujar().img.save(destino / f"{modulo}.png")
        hechos.append(modulo)
        if modulo == "departamento":
            m.dibujar("j3").img.save(destino / "departamento_j3.png"); hechos.append("departamento_j3")
        if modulo == "estudio":
            m.dibujar("j6").img.save(destino / "estudio_j6.png"); hechos.append("estudio_j6")
            m.dibujar("j12").img.save(destino / "estudio_j12.png"); hechos.append("estudio_j12")
        for (base, variante) in (("cantina", "miniver"), ("escalera", "odio"), ("departamento", "noche"),
                                 ("avenida", "furgoneta"), ("lavabos", "vaho")):
            if modulo == base:
                m.dibujar(variante).img.save(destino / f"{base}_{variante}.png"); hechos.append(f"{base}_{variante}")
        if modulo == "tunel":
            for variante in ("nichos", "derrumbe", "carteles"):
                m.dibujar(variante).img.save(destino / f"tunel_{variante}.png"); hechos.append(f"tunel_{variante}")
        if modulo == "mercado":
            m.dibujar("ruinas").img.save(destino / "mercado_ruinas.png"); hechos.append("mercado_ruinas")
    return hechos
