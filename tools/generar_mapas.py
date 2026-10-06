"""Genera los mapas de Tiled (.tmj) del corte vertical.

Los mapas se pueden abrir y editar después en Tiled; este script es el punto de partida
y la fuente de verdad mientras no se editen a mano.
Uso: python3 tools/generar_mapas.py
"""
import json
from pathlib import Path

DESTINO = Path(__file__).resolve().parents[1] / "content" / "locations"


def props(d):
    return [{"name": k, "type": "string", "value": str(v)} for k, v in d.items() if v is not None]


class Mapa:
    def __init__(self, id, nombre, ancho=480, alto=270, **p):
        self.id, self.ancho, self.alto = id, ancho, alto
        self.p = {"nombre": nombre, "fondo": f"loc-{id}", **p}
        self.capas = {"colisiones": [], "hotspots": [], "spawns": [], "npcs": []}
        self.n = 1

    def _obj(self, capa, nombre, x, y, w=0, h=0, punto=False, **p):
        o = {"id": self.n, "name": nombre, "x": x, "y": y, "width": w, "height": h, "visible": True, "rotation": 0, "type": ""}
        if punto:
            o["point"] = True
        if p:
            o["properties"] = props(p)
        self.capas[capa].append(o)
        self.n += 1
        return self

    def col(self, x, y, w, h, nombre="", **p): return self._obj("colisiones", nombre, x, y, w, h, **p)
    def hot(self, nombre, x, y, w, h, **p): return self._obj("hotspots", nombre, x, y, w, h, **p)
    def spawn(self, nombre, x, y, orientacion="abajo"): return self._obj("spawns", nombre, x, y, punto=True, orientacion=orientacion)
    def npc(self, nombre, x, y, **p): return self._obj("npcs", nombre, x, y, punto=True, **p)

    def muros(self, x0=40, x1=440, fondo=90, suelo=246, puerta=None):
        """Pared del fondo, muros laterales e inferior (con hueco de puerta opcional (xa, xb))."""
        self.col(0, 0, self.ancho, fondo, "pared_fondo")
        self.col(0, 0, x0 + 4, self.alto, "muro_izq")
        self.col(x1 - 4, 0, self.ancho - x1 + 4, self.alto, "muro_der")
        if puerta:
            self.col(0, suelo - 2, puerta[0], self.alto - suelo + 2, "muro_inf_izq")
            self.col(puerta[1], suelo - 2, self.ancho - puerta[1], self.alto - suelo + 2, "muro_inf_der")
            self.col(puerta[0], suelo + 8, puerta[1] - puerta[0], self.alto, "umbral")
        else:
            self.col(0, suelo - 2, self.ancho, self.alto - suelo + 2, "muro_inf")
        return self

    def guardar(self):
        capas = [{"id": 1, "name": "fondo", "type": "imagelayer", "image": f"../../public/assets/locations/{self.id}.png",
                  "x": 0, "y": 0, "opacity": 1, "visible": True}]
        for i, (nombre, objs) in enumerate(self.capas.items(), start=2):
            capas.append({"id": i, "name": nombre, "type": "objectgroup", "objects": objs, "opacity": 1, "visible": True, "x": 0, "y": 0})
        mapa = {"type": "map", "version": "1.10", "orientation": "orthogonal", "renderorder": "right-down",
                "width": self.ancho // 16, "height": -(-self.alto // 16), "tilewidth": 16, "tileheight": 16,
                "infinite": False, "properties": props(self.p), "tilesets": [], "layers": capas,
                "nextlayerid": len(capas) + 1, "nextobjectid": self.n}
        (DESTINO / f"{self.id}.tmj").write_text(json.dumps(mapa, ensure_ascii=False, indent=1))
        return self.id


def a(x, y):
    return f"{x},{y}"


MAPAS = []

# ------------------------------------------------------------------ PRÓLOGO
m = Mapa("stepney", "Calle Stepney, 1979", prota_tinte="#9aa0b8")
m.col(0, 0, 480, 104, "fachadas").col(176, 166, 86, 36, "monton").col(330, 188, 38, 22, "telepantalla")
m.hot("telepantalla_rota", 326, 178, 48, 36, nombre_visible="Telepantalla rota", mirar="stepney.tele_mirar", aprox=a(350, 226), orientacion="arriba")
m.hot("fuego", 118, 26, 124, 72, nombre_visible="Fuego", mirar="stepney.fuego_mirar", aprox=a(180, 118), orientacion="arriba")
m.hot("cascotes", 172, 154, 96, 54, nombre_visible="Montón de cascotes", mirar="stepney.cascotes_mirar", usar="stepney.cascotes_usar", aprox=a(220, 220), orientacion="arriba")
m.spawn("inicio", 300, 238, "arriba")
MAPAS.append(m)

m = Mapa("stepney_ivy", "Calle Stepney, 1979", prota_tinte="#9aa0b8", al_entrar="stepney.ivy")
m.col(0, 0, 480, 104, "fachadas").col(168, 168, 136, 40, "ivy").col(330, 188, 38, 22, "telepantalla")
m.hot("ivy", 172, 168, 124, 40, nombre_visible="Ivy", mirar="stepney.ivy_mirar", aprox=a(204, 222), orientacion="arriba")
m.hot("reloj", 218, 198, 24, 16, nombre_visible="Reloj de Ivy", mirar="stepney.reloj_mirar", usar="stepney.reloj_usar", aprox=a(230, 224), orientacion="arriba", condicion="!reloj_cogido")
m.npc("nell", 150, 214, sprite="nell", condicion="p_nell", solido="false")
m.npc("oficial", 300, 140, sprite="oficial", condicion="p_oficial", solido="false")
m.spawn("ivy", 232, 228, "arriba")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 1
m = Mapa("piso", "Piso del protagonista", al_entrar="piso.entrar")
m.muros(puerta=None)
m.col(48, 60, 56, 116, "cama").col(284, 84, 46, 18, "armario").col(348, 118, 72, 52, "mesa").col(366, 138, 32, 46, "silla").col(198, 224, 16, 16, "perchero")
for h in [("cartel_ivy", 192, 24, 40, 50, "Cartel de Ivy", "piso.cartel_mirar", "piso.cartel_usar", (212, 98), "arriba"),
          ("reloj", 244, 38, 34, 20, "Reloj de Ivy", "piso.reloj_mirar", "piso.reloj_usar", (260, 98), "arriba"),
          ("telepantalla", 340, 18, 92, 62, "Telepantalla", "piso.tele_mirar", "piso.tele_usar", (388, 108), "arriba"),
          ("ventana", 100, 20, 84, 52, "Ventana", "piso.ventana_mirar", None, (142, 100), "arriba"),
          ("hornillo", 352, 120, 32, 26, "Hornillo", "piso.hornillo_mirar", "piso.hornillo_usar", (338, 136), "derecha"),
          ("cama", 48, 60, 56, 116, "Cama", "piso.cama_mirar", None, (116, 124), "izquierda"),
          ("armario", 288, 10, 38, 86, "Armario", "piso.armario_mirar", None, (306, 110), "arriba"),
          ("abrigo", 196, 176, 20, 64, "Abrigo", "piso.abrigo_mirar", None, (226, 226), "izquierda"),
          ("puerta", 222, 236, 36, 14, "Puerta", None, "piso.puerta_usar", (240, 236), "abajo")]:
    n, x, y, w, hh, nom, mi, us, ap, ori = h
    m.hot(n, x, y, w, hh, nombre_visible=nom, mirar=mi, usar=us, aprox=a(*ap), orientacion=ori)
m.spawn("cama", 118, 124, "abajo").spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

m = Mapa("escalera", "Mansiones Victoria · rellano", al_entrar="escalera.entrar")
m.muros(fondo=92)
m.col(40, 112, 84, 80, "escalera_sube").col(316, 168, 6, 54, "barandilla_v").col(318, 156, 122, 10, "barandilla_h")
m.hot("ascensor", 60, 26, 48, 58, nombre_visible="Ascensor", mirar="escalera.ascensor_mirar", aprox=a(84, 104), orientacion="arriba")
m.hot("puerta_piso", 186, 34, 30, 46, nombre_visible="Mi puerta", mirar="escalera.puerta_mirar", aprox=a(201, 102), orientacion="arriba")
m.hot("cartel_gh", 262, 22, 52, 58, nombre_visible="Cartel", mirar="escalera.cartel_mirar", aprox=a(288, 102), orientacion="arriba")
m.hot("puerta_parsons", 386, 34, 30, 46, nombre_visible="Puerta de los Parsons", mirar="escalera.parsons_mirar", aprox=a(401, 102), orientacion="arriba")
m.hot("escalera_sube", 40, 112, 84, 80, nombre_visible="Escalera", mirar="escalera.sube_mirar", aprox=a(136, 150), orientacion="izquierda")
m.hot("bajar", 324, 200, 112, 44, nombre_visible="Escalera abajo", usar="escalera.bajar", auto="true")
m.npc("winston", 150, 176, sprite="winston", nombre_visible="Hombre en la escalera", mirar="escalera.winston_mirar", hablar="escalera.winston", condicion="!winston_se_fue")
m.npc("hilda", 296, 216, sprite="hilda", nombre_visible="Hilda Grubb", mirar="escalera.hilda_mirar", hablar="escalera.hilda")
m.spawn("piso", 201, 106, "abajo")
MAPAS.append(m)

m = Mapa("avenida", "Avenida de la Victoria", ancho=960, al_entrar="avenida.entrar")
m.col(0, 0, 960, 120, "fachadas").col(0, 198, 960, 72, "calzada").col(496, 118, 68, 34, "puesto")
for fx in (150, 380, 640):
    m.col(fx - 4, 180, 8, 8, "farola")
m.hot("portal", 20, 62, 38, 50, nombre_visible="Mansiones Victoria", mirar="avenida.portal_mirar", aprox=a(40, 128), orientacion="arriba")
m.hot("consignas", 296, 50, 84, 42, nombre_visible="Cartel de las consignas", mirar="avenida.consignas_mirar", aprox=a(338, 128), orientacion="arriba")
m.hot("helicoptero", 462, 10, 50, 20, nombre_visible="Helicóptero", mirar="avenida.helicoptero_mirar", aprox=a(488, 128), orientacion="arriba")
m.hot("puesto", 496, 116, 68, 36, nombre_visible="Proles discutiendo", mirar="avenida.proles_mirar", aprox=a(530, 166), orientacion="arriba")
m.hot("minipax", 852, 70, 56, 44, nombre_visible="Ministerio de la Paz", usar="avenida.minipax", aprox=a(880, 128), orientacion="arriba")
m.npc("prole1", 512, 166, sprite="prole1", solido="true")
m.npc("prole2", 552, 168, sprite="prole2", solido="true")
m.npc("nino", 676, 176, sprite="nino", nombre_visible="Niño prole", hablar="avenida.nino", mirar="avenida.nino_mirar", condicion="!nino_se_fue")
m.spawn("portal", 40, 132, "abajo")
MAPAS.append(m)

m = Mapa("vestibulo", "Ministerio de la Paz · vestíbulo", al_entrar="vestibulo.entrar")
m.muros(fondo=104, puerta=(216, 264))
m.col(58, 96, 24, 144, "columna_izq").col(398, 96, 24, 144, "columna_der")
m.col(96, 138, 118, 18, "torniquetes_izq").col(260, 138, 122, 18, "torniquetes_der").col(376, 120, 48, 50, "garita")
m.col(214, 138, 46, 18, "barrera", condicion="!ficha_revisada")
m.hot("titulo", 140, 20, 200, 30, nombre_visible="Rótulo", mirar="vestibulo.titulo_mirar", aprox=a(240, 118), orientacion="arriba")
m.hot("telepantalla", 296, 46, 72, 46, nombre_visible="Telepantalla", mirar="vestibulo.tele_mirar", aprox=a(332, 118), orientacion="arriba")
m.hot("ascensor", 70, 50, 38, 48, nombre_visible="Ascensor", mirar="vestibulo.ascensor_mirar", usar="vestibulo.ascensor", aprox=a(89, 118), orientacion="arriba")
m.npc("guardia", 237, 134, sprite="guardia", nombre_visible="Guardia", hablar="vestibulo.guardia", mirar="vestibulo.guardia_mirar", aprox=a(237, 178), orientacion_jugador="arriba", condicion="!ficha_revisada")
m.npc("guardia_pasado", 196, 128, sprite="guardia", nombre_visible="Guardia", mirar="vestibulo.guardia_mirar", condicion="ficha_revisada", aprox=a(196, 116), orientacion_jugador="abajo")
m.npc("guardia2", 360, 200, sprite="guardia", nombre_visible="Guardia", mirar="vestibulo.guardia2_mirar")
m.spawn("entrada", 240, 236, "arriba").spawn("ascensor", 89, 122, "abajo")
MAPAS.append(m)

m = Mapa("departamento", "Departamento de Partes y Cartografía", al_entrar="depto.entrar")
m.muros(fondo=96, puerta=(380, 412))
for (mx, my) in [(90, 116), (170, 116), (250, 116), (90, 172), (170, 172), (250, 172)]:
    m.col(mx - 2, my - 4, 48, 38, "mesa").col(mx + 12, my + 26, 20, 22, "silla")
m.col(350, 116, 78, 50, "registro")
m.hot("mi_mesa", 170, 166, 44, 32, nombre_visible="Mi mesa", mirar="depto.mesa_mirar", usar="depto.mesa", aprox=a(172, 216), orientacion="arriba")
m.hot("mapa", 148, 28, 154, 58, nombre_visible="Mapa del frente", mirar="depto.mapa_mirar", aprox=a(226, 104), orientacion="arriba")
m.hot("memoria", 328, 44, 34, 28, nombre_visible="Agujero de la memoria", mirar="depto.memoria_mirar", aprox=a(345, 104), orientacion="arriba")
m.hot("despacho", 52, 30, 40, 58, nombre_visible="Despacho del Subdirector", mirar="depto.despacho_mirar", usar="depto.despacho", aprox=a(71, 104), orientacion="arriba")
m.hot("registro", 350, 116, 78, 50, nombre_visible="Mesa del Registro", mirar="depto.registro_mirar", aprox=a(388, 176), orientacion="arriba")
m.hot("telepantalla", 376, 26, 56, 42, nombre_visible="Telepantalla", mirar="depto.tele_mirar", aprox=a(404, 104), orientacion="arriba")
m.hot("salir", 380, 238, 32, 10, nombre_visible="Puerta", usar="depto.salir", aprox=a(396, 234), orientacion="abajo")
m.npc("voss", 72, 112, sprite="voss", nombre_visible="Subdirector Voss", mirar="depto.voss_mirar", condicion="voss_presente")
m.npc("amory", 304, 206, sprite="amory", nombre_visible="Felix Amory", hablar="depto.amory", mirar="depto.amory_mirar")
m.npc("func1", 114, 160, sprite="funcionario1", nombre_visible="Funcionario", mirar="depto.funcionario_mirar", aprox=a(152, 160), orientacion_jugador="izquierda")
m.npc("func2", 274, 160, sprite="funcionaria1", nombre_visible="Funcionaria", mirar="depto.funcionario_mirar", aprox=a(236, 160), orientacion_jugador="derecha")
m.npc("func3", 114, 216, sprite="funcionario2", nombre_visible="Funcionario", mirar="depto.funcionario_mirar", aprox=a(152, 224), orientacion_jugador="izquierda")
m.npc("nell", 340, 204, sprite="nell", nombre_visible="Limpiadora", mirar="depto.nell_mirar", hablar="depto.nell_hablar", condicion="parte_j1_enviado")
m.spawn("puerta", 396, 230, "arriba").spawn("mesa", 172, 216, "arriba")
MAPAS.append(m)

m = Mapa("cantina", "Cantina del Minipax", al_entrar="cantina.entrar")
m.muros(fondo=92)
m.col(40, 90, 46, 150, "mostrador")
for (mx, my) in [(110, 120), (250, 120), (110, 186), (250, 186)]:
    m.col(mx, my - 8, 72, 44, "mesa")
m.npc("amory", 216, 166, sprite="amory", nombre_visible="Felix Amory", hablar="cantina.amory", aprox=a(216, 182))
m.npc("f1", 140, 110, sprite="funcionaria2").npc("f2", 160, 176, sprite="funcionario1").npc("f3", 380, 176, sprite="funcionario2")
m.spawn("puerta", 340, 176, "izquierda")
MAPAS.append(m)

m = Mapa("piso_noche", "Piso del protagonista · noche", al_entrar="piso_noche.entrar")
m.muros()
m.col(48, 60, 56, 116, "cama").col(284, 84, 46, 18, "armario").col(348, 118, 72, 52, "mesa").col(366, 138, 32, 46, "silla").col(198, 224, 16, 16, "perchero")
m.hot("cartel_ivy", 192, 24, 40, 50, nombre_visible="Cartel de Ivy", mirar="piso_noche.cartel_mirar", aprox=a(212, 98), orientacion="arriba")
m.hot("cama", 48, 60, 56, 116, nombre_visible="Cama", mirar="piso_noche.cama_mirar", usar="piso_noche.dormir", aprox=a(116, 124), orientacion="izquierda")
m.hot("telepantalla", 340, 18, 92, 62, nombre_visible="Telepantalla", mirar="piso_noche.tele_mirar", aprox=a(388, 108), orientacion="arriba")
m.spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

if __name__ == "__main__":
    for mapa in MAPAS:
        print("ok", mapa.guardar())
