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
          ("puerta", 222, 236, 36, 14, "Puerta", None, "piso.puerta_usar", (240, 236), "abajo"),
          ("cajon", 400, 150, 18, 14, "Cajón de la mesa", "piso.cajon_mirar", "piso.cajon_usar", (424, 180), "izquierda")]:
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
m.npc("winston", 150, 176, sprite="winston", nombre_visible="Hombre en la escalera", mirar="escalera.winston_mirar", hablar="escalera.winston", condicion="jornada==1 && !winston_se_fue")
m.npc("hilda", 296, 216, sprite="hilda", nombre_visible="Hilda Grubb", mirar="escalera.hilda_mirar", hablar="escalera.hilda", condicion="jornada==1")
m.npc("hilda6", 150, 176, sprite="hilda", nombre_visible="Hilda Grubb", mirar="escalera.hilda_mirar", hablar="j6_hilda_otra", condicion="jornada==6 && !hilda_j6")
m.npc("parsons", 392, 132, sprite="parsons", nombre_visible="Parsons", mirar="escalera.parsons_npc_mirar", hablar="escalera.parsons_hablar", condicion="jornada==2")
m.npc("hija_parsons", 362, 136, sprite="hija_parsons", nombre_visible="La hija de Parsons", mirar="escalera.hija_mirar", hablar="escalera.hija_hablar", condicion="jornada==2")
m.npc("nino_parsons", 414, 124, sprite="nino_parsons", nombre_visible="El hijo de Parsons", mirar="escalera.nino_mirar", condicion="jornada==2")
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

m = Mapa("departamento", "Departamento de Partes y Cartografía", al_entrar="depto.entrar",
         fondo_alt="loc-departamento_j3", fondo_alt_si="amory_borrado")
m.muros(fondo=96, puerta=(380, 412))
for (mx, my) in [(90, 116), (170, 116), (250, 116), (90, 172), (170, 172), (250, 172)]:
    m.col(mx - 2, my - 4, 48, 38, "mesa").col(mx + 12, my + 26, 20, 22, "silla")
m.col(350, 116, 78, 50, "registro").col(414, 204, 24, 40, "archivador")
m.hot("mi_mesa", 170, 166, 44, 32, nombre_visible="Mi mesa", mirar="depto.mesa_mirar", usar="depto.mesa", aprox=a(172, 216), orientacion="arriba")
m.hot("mapa", 148, 28, 154, 58, nombre_visible="Mapa del frente", mirar="depto.mapa_mirar", aprox=a(226, 104), orientacion="arriba")
m.hot("memoria", 328, 44, 34, 28, nombre_visible="Agujero de la memoria", mirar="depto.memoria_mirar", aprox=a(345, 104), orientacion="arriba",
      con="lapiz_amory=j3_lapiz_agujero")
m.hot("despacho", 52, 30, 40, 58, nombre_visible="Despacho del Subdirector", mirar="depto.despacho_mirar", usar="depto.despacho", aprox=a(71, 104), orientacion="arriba")
m.hot("registro", 350, 116, 78, 50, nombre_visible="Mesa del Registro", mirar="depto.registro_mirar", aprox=a(388, 176), orientacion="arriba")
m.hot("telepantalla", 376, 26, 56, 42, nombre_visible="Telepantalla", mirar="depto.tele_mirar", aprox=a(404, 104), orientacion="arriba")
m.hot("salir", 380, 238, 32, 10, nombre_visible="Puerta", usar="depto.salir", aprox=a(396, 234), orientacion="abajo")
m.hot("personal", 414, 196, 24, 48, nombre_visible="Archivador del personal", mirar="depto.personal_mirar", usar="depto.personal", aprox=a(402, 222), orientacion="derecha")
m.hot("libro", 356, 136, 20, 22, nombre_visible="Libro de Registro", mirar="j4_libro_mirar", usar="j4_libro", aprox=a(366, 176), orientacion="arriba", condicion="registro_asignado")
m.hot("cajon_registro", 378, 156, 24, 10, nombre_visible="Cajón del Registro", mirar="j4_cajon_mirar", usar="j4_cajon", aprox=a(390, 176), orientacion="arriba", condicion="registro_asignado")
m.hot("proyeccion", 154, 48, 38, 30, nombre_visible="Proyección nueva", mirar="j3_proyeccion", aprox=a(172, 104), orientacion="arriba", condicion="amory_borrado")
m.hot("papelera_amory", 296, 190, 14, 16, nombre_visible="Papelera", mirar="j3_papelera", aprox=a(318, 196), orientacion="izquierda", condicion="amory_borrado")
m.npc("voss", 72, 112, sprite="voss", nombre_visible="Subdirector Voss", mirar="depto.voss_mirar", condicion="voss_presente")
m.npc("voss_mesa", 150, 214, sprite="voss", nombre_visible="Subdirector Voss", mirar="depto.voss_mirar", condicion="voss_espera", aprox=a(152, 236))
m.npc("amory", 304, 206, sprite="amory", nombre_visible="Felix Amory", hablar="depto.amory", mirar="depto.amory_mirar", condicion="!amory_borrado")
m.npc("pell", 304, 206, sprite="pell", nombre_visible="Camarada Pell", hablar="j3_pell", mirar="j3_pell_mirar", condicion="amory_borrado")
m.npc("func1", 114, 160, sprite="funcionario1", nombre_visible="Funcionario", mirar="depto.funcionario_mirar", aprox=a(152, 160), orientacion_jugador="izquierda")
m.npc("func2", 274, 160, sprite="funcionaria1", nombre_visible="Funcionaria", mirar="depto.funcionario_mirar", aprox=a(236, 160), orientacion_jugador="derecha", condicion="!amory_borrado")
m.npc("brooke", 274, 160, sprite="brooke", nombre_visible="Camarada Brooke", hablar="j3_brooke", mirar="j3_brooke_mirar", aprox=a(236, 160), orientacion_jugador="derecha", condicion="amory_borrado")
m.npc("func3", 114, 216, sprite="funcionario2", nombre_visible="Funcionario", mirar="depto.funcionario_mirar", aprox=a(152, 224), orientacion_jugador="izquierda")
m.npc("nell", 340, 204, sprite="nell", nombre_visible="Limpiadora", mirar="depto.nell_mirar", hablar="depto.nell_hablar", condicion="parte_j1_enviado && jornada==1")
m.spawn("puerta", 396, 230, "arriba").spawn("mesa", 172, 216, "arriba").spawn("despacho", 71, 106, "abajo")
MAPAS.append(m)

m = Mapa("cantina", "Cantina del Minipax", al_entrar="cantina.entrar")
m.muros(fondo=92)
m.col(40, 90, 46, 150, "mostrador")
for (mx, my) in [(110, 120), (250, 120), (110, 186), (250, 186)]:
    m.col(mx, my - 8, 72, 44, "mesa")
m.npc("amory", 216, 166, sprite="amory", nombre_visible="Felix Amory", hablar="cantina.amory", aprox=a(216, 182), condicion="!amory_borrado")
m.hot("salir", 330, 238, 32, 10, nombre_visible="Puerta", usar="cantina.salir", aprox=a(346, 234), orientacion="abajo")
m.hot("silla", 280, 208, 26, 10, nombre_visible="Silla vacía", mirar="j4_silla_mirar", aprox=a(296, 234), orientacion="arriba", condicion="amory_borrado")
m.npc("pell", 140, 176, sprite="pell", nombre_visible="Camarada Pell", mirar="j4_pell_mirar", aprox=a(140, 234), orientacion_jugador="arriba", condicion="amory_borrado")
m.npc("brooke", 400, 110, sprite="brooke", nombre_visible="Camarada Brooke", hablar="j4_brooke", mirar="j3_brooke_mirar", aprox=a(400, 128), condicion="amory_borrado")
m.npc("f1", 140, 110, sprite="funcionaria2").npc("f2", 160, 176, sprite="funcionario1", condicion="!amory_borrado").npc("f3", 380, 176, sprite="funcionario2")
m.spawn("puerta", 340, 176, "izquierda")
MAPAS.append(m)

CONO_PISO = "386,70;328,88;286,116;234,116;230,90;40,90;40,246;440,246;440,90"
DIARIO_VISTO = "diario=j5_diario_cono"
m = Mapa("piso_noche", "Piso del protagonista · noche", al_entrar="piso_noche.entrar", cono=CONO_PISO)
m.muros()
m.col(48, 60, 56, 116, "cama").col(284, 84, 46, 18, "armario").col(348, 118, 72, 52, "mesa").col(366, 138, 32, 46, "silla").col(198, 224, 16, 16, "perchero")
m.hot("cartel_ivy", 192, 24, 40, 50, nombre_visible="Cartel de Ivy", mirar="piso_noche.cartel_mirar", aprox=a(212, 98), orientacion="arriba", con=DIARIO_VISTO)
m.hot("cama", 48, 60, 56, 116, nombre_visible="Cama", mirar="piso_noche.cama_mirar", usar="piso_noche.dormir", aprox=a(116, 124), orientacion="izquierda", con=DIARIO_VISTO)
m.hot("telepantalla", 340, 18, 92, 62, nombre_visible="Telepantalla", mirar="piso_noche.tele_mirar", aprox=a(388, 108), orientacion="arriba", con=DIARIO_VISTO)
m.hot("ventana", 100, 20, 84, 52, nombre_visible="Ventana", mirar="piso_noche.ventana_mirar", aprox=a(142, 100), orientacion="arriba", con=DIARIO_VISTO)
m.hot("abrigo", 196, 176, 20, 64, nombre_visible="Abrigo", mirar="piso_noche.abrigo_mirar", usar="piso_noche.abrigo", aprox=a(226, 226), orientacion="izquierda", con=DIARIO_VISTO)
m.hot("hueco", 236, 84, 44, 26, nombre_visible="Hueco junto al armario", mirar="piso_noche.hueco_mirar", aprox=a(258, 104), orientacion="arriba", con="diario=j5_hueco")
m.spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 2
m = Mapa("salon_odio", "Ministerio de la Verdad · Gran Salón", al_entrar="odio.entrar")
m.col(0, 0, 480, 100, "pantalla").col(0, 0, 28, 270, "muro_izq").col(452, 0, 28, 270, "muro_der").col(0, 250, 480, 20, "muro_inf")
for y in (118, 146, 174, 202, 230):
    m.col(34, y - 14, 186, 24, "fila").col(260, y - 14, 186, 24, "fila")
m.hot("pantalla", 126, 12, 228, 78, nombre_visible="Telepantalla", mirar="odio.pantalla_mirar", aprox=a(240, 110), orientacion="arriba")
m.hot("asiento", 186, 160, 22, 22, nombre_visible="Mi asiento", usar="odio.sentarse", mirar="odio.asiento_mirar", aprox=a(238, 176), orientacion="izquierda")
m.npc("amory", 226, 146, sprite="amory", nombre_visible="Felix Amory", hablar="odio.amory", mirar="odio.amory_mirar", aprox=a(244, 150), orientacion_jugador="izquierda")
m.npc("julia", 270, 166, sprite="julia", nombre_visible="Mujer de la faja escarlata", mirar="odio.julia_mirar", aprox=a(246, 168), orientacion_jugador="derecha")
m.npc("obrien", 256, 118, sprite="obrien", nombre_visible="Hombre del Partido Interior", mirar="odio.obrien_mirar", aprox=a(236, 132), orientacion_jugador="derecha", solido="false")
m.npc("winston", 130, 222, sprite="winston", nombre_visible="Winston Smith", mirar="odio.winston_mirar", aprox=a(150, 248), orientacion_jugador="arriba")
m.spawn("entrada", 240, 244, "arriba")
MAPAS.append(m)

m = Mapa("despacho_voss", "Despacho del Subdirector", al_entrar="voss_despacho.entrar")
m.col(0, 0, 480, 100, "pared").col(0, 0, 124, 270, "izq").col(356, 0, 124, 270, "der").col(0, 228, 480, 42, "inf").col(194, 100, 94, 36, "mesa")
m.npc("voss", 241, 100, sprite="voss", nombre_visible="Subdirector Voss", mirar="voss_despacho.voss_mirar", solido="true", aprox=a(241, 150))
m.spawn("puerta", 240, 220, "arriba")
MAPAS.append(m)

m = Mapa("centro", "Centro de la Comunidad", al_entrar="centro.entrar")
m.muros(fondo=90, puerta=(224, 256))
m.col(68, 116, 104, 62, "pingpong").col(358, 90, 74, 46, "piano").col(380, 138, 30, 12, "banqueta").col(188, 188, 144, 36, "pancarta")
m.hot("martires", 180, 24, 96, 54, nombre_visible="Cartel de los mártires", mirar="centro.martires_mirar", aprox=a(228, 100), orientacion="arriba")
m.hot("piano", 358, 90, 74, 46, nombre_visible="Piano", mirar="centro.piano_mirar", usar="centro.piano_usar", aprox=a(370, 152), orientacion="arriba")
m.hot("pancarta", 188, 188, 144, 36, nombre_visible="Pancarta", mirar="centro.pancarta_mirar", usar="centro.pancarta_usar", aprox=a(260, 234), orientacion="arriba")
m.hot("pingpong", 68, 116, 104, 62, nombre_visible="Mesa de ping-pong", mirar="centro.pingpong_mirar", aprox=a(120, 190), orientacion="arriba")
m.hot("salir", 224, 240, 32, 10, nombre_visible="Puerta", usar="centro.salir", aprox=a(240, 236), orientacion="abajo")
m.npc("hilda", 252, 140, sprite="hilda", nombre_visible="Hilda Grubb", hablar="centro.hilda", mirar="centro.hilda_mirar")
m.npc("parsons", 320, 160, sprite="parsons", nombre_visible="Parsons", hablar="centro.parsons", mirar="centro.parsons_mirar")
m.npc("hija_parsons", 346, 176, sprite="hija_parsons", nombre_visible="La hija de Parsons", mirar="centro.hija_mirar")
m.npc("f1", 110, 210, sprite="funcionaria1").npc("f2", 140, 214, sprite="funcionario2")
m.spawn("puerta", 240, 236, "arriba")
MAPAS.append(m)

m = Mapa("sueno", "Sueño", ancho=960, al_entrar="sueno.entrar")
m.col(0, 0, 960, 122, "fachadas")
for fx in (120, 400, 680):
    m.col(fx - 4, 154, 8, 8, "farola")
m.npc("ivy", 420, 200, sprite="ivy_nina", nombre_visible="Ivy", mirar="sueno.ivy_mirar", huye="120", solido="false")
m.hot("final", 860, 120, 100, 150, nombre_visible="", usar="sueno.final", auto="true")
m.spawn("inicio", 60, 200, "derecha")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 3
m = Mapa("pasillo", "Minipax · pasillo de la planta 14", ancho=960, al_entrar="pasillo.entrar", parpadeo="true")
m.col(0, 0, 960, 98, "pared").col(0, 196, 960, 74, "muro_inf").col(0, 0, 8, 270, "fondo_izq").col(952, 0, 8, 270, "fondo_der")
m.col(700, 128, 36, 22, "carrito")
m.hot("puerta_depto", 60, 40, 32, 48, nombre_visible="Cartografía", mirar="pasillo.puerta_depto_mirar", usar="pasillo.puerta_depto", aprox=a(76, 110), orientacion="arriba")
m.hot("telepantalla", 352, 38, 46, 32, nombre_visible="Telepantalla", mirar="pasillo.tele_mirar", aprox=a(375, 110), orientacion="arriba")
m.hot("cartel", 586, 34, 36, 46, nombre_visible="Cartel", mirar="pasillo.cartel_mirar", aprox=a(604, 110), orientacion="arriba")
m.hot("suministros", 760, 40, 32, 48, nombre_visible="Cuarto de suministros", mirar="pasillo.suministros_mirar", usar="pasillo.ir_suministros", aprox=a(776, 110), orientacion="arriba")
m.hot("carrito", 698, 106, 40, 44, nombre_visible="Carrito de la limpieza", mirar="pasillo.carrito_mirar", aprox=a(718, 162), orientacion="arriba")
m.hot("salir", 886, 38, 36, 52, nombre_visible="Escalera", usar="pasillo.salir", aprox=a(904, 110), orientacion="arriba")
m.hot("encuentro", 630, 98, 12, 98, usar="pasillo.encuentro", auto="true", condicion="!nell_se_fue")
m.npc("nell", 752, 150, sprite="nell", nombre_visible="Limpiadora", mirar="pasillo.nell_mirar", hablar="pasillo.encuentro", aprox=a(752, 168), condicion="!nell_se_fue")
m.npc("guardia", 540, 172, sprite="guardia", nombre_visible="Guardia", mirar="pasillo.guardia_mirar", condicion="guardia_pasillo && jornada==3")
m.spawn("depto", 76, 114, "abajo").spawn("suministros", 776, 114, "abajo")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 4
m = Mapa("limehouse", "Limehouse", ancho=960, al_entrar="limehouse.entrar")
m.col(0, 0, 960, 108, "fachadas").col(0, 232, 960, 38, "muro").col(716, 108, 210, 34, "escombros")
for fx in (150, 470, 640):
    m.col(fx - 4, 162, 8, 8, "farola")
m.hot("altavoz", 552, 4, 26, 100, nombre_visible="Altavoz", mirar="limehouse.altavoz_mirar", aprox=a(566, 122), orientacion="arriba")
m.hot("ropa", 380, 22, 140, 22, nombre_visible="Ropa tendida", mirar="limehouse.ropa_mirar", aprox=a(450, 122), orientacion="arriba")
m.hot("pub", 288, 54, 74, 50, nombre_visible="Pub «La Campana»", mirar="limehouse.pub_mirar", usar="limehouse.entrar_pub", aprox=a(325, 118), orientacion="arriba")
m.hot("casa", 690, 20, 200, 86, nombre_visible="Casa alcanzada", mirar="limehouse.casa_mirar", usar="limehouse.casa", aprox=a(770, 150), orientacion="arriba")
m.hot("llegar", 650, 108, 12, 124, usar="limehouse.casa", auto="true", condicion="!casa_vista")
m.hot("volver", 0, 108, 10, 124, usar="limehouse.volver", auto="true")
m.npc("sammy", 744, 202, sprite="nino", nombre_visible="Niño de la lata", hablar="limehouse.sammy", mirar="limehouse.sammy_mirar")
m.npc("dot", 806, 196, sprite="dot", nombre_visible="Mujer del pañuelo", hablar="limehouse.dot", mirar="limehouse.dot_mirar")
m.npc("prole1", 872, 176, sprite="prole2", nombre_visible="Proles", mirar="limehouse.proles_mirar")
m.npc("prole2", 900, 196, sprite="prole1", nombre_visible="Proles", mirar="limehouse.proles_mirar")
m.npc("crane", 600, 204, sprite="crane", nombre_visible="Hombre de la cámara", hablar="limehouse.crane", mirar="limehouse.crane_mirar", condicion="crane_aparece")
m.npc("tripode", 622, 200, sprite="tripode", solido="false", condicion="crane_aparece")
m.spawn("entrada", 28, 172, "derecha").spawn("pub", 325, 122, "abajo")
MAPAS.append(m)

m = Mapa("pub", "Pub «La Campana»", al_entrar="pub.entrar")
m.muros(fondo=92, puerta=(224, 256))
m.col(52, 92, 190, 38, "barra")
for (mx, my) in [(290, 120), (370, 120), (300, 190)]:
    m.col(mx, my, 40, 20, "mesa")
m.hot("campana", 138, 22, 20, 22, nombre_visible="Campana", mirar="pub.campana_mirar", aprox=a(148, 146), orientacion="arriba")
m.hot("diana", 298, 36, 30, 30, nombre_visible="Diana", mirar="pub.diana_mirar", aprox=a(312, 106), orientacion="arriba")
m.hot("salir", 224, 240, 32, 10, nombre_visible="Puerta", usar="pub.salir", aprox=a(240, 236), orientacion="abajo")
m.npc("tabernero", 150, 92, sprite="tabernero", nombre_visible="Tabernero", hablar="pub.tabernero", mirar="pub.tabernero_mirar", aprox=a(150, 146), orientacion_jugador="arriba", solido="false")
m.npc("viejo", 352, 212, sprite="viejo", nombre_visible="Viejo", hablar="pub.viejo", mirar="pub.viejo_mirar", aprox=a(372, 226), orientacion_jugador="izquierda")
m.npc("p1", 300, 116, sprite="prole1", nombre_visible="Proles", mirar="pub.proles_mirar", aprox=a(272, 118), orientacion_jugador="derecha")
m.npc("p2", 410, 140, sprite="prole2", nombre_visible="Proles", mirar="pub.proles_mirar")
m.spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 5
PUESTOS = [(40, 70), (180, 76), (330, 80), (650, 60)]

def mercado(m):
    m.col(0, 0, 960, 104, "fachadas").col(0, 232, 960, 38, "muro")
    for (x, w) in PUESTOS:
        m.col(x - 2, 104, w + 4, 46, "puesto")
    m.col(118, 212, 74, 20, "puesto").col(718, 212, 74, 20, "puesto")
    return m

m = mercado(Mapa("mercado", "Mercado de Watney Street", ancho=960, al_entrar="mercado.entrar"))
m.hot("estudio", 820, 30, 96, 70, nombre_visible="Estudio Crane", mirar="mercado.estudio_mirar", usar="mercado.ir_estudio", aprox=a(891, 112), orientacion="arriba")
m.hot("cordones", 650, 128, 60, 22, nombre_visible="Puesto de cordones", mirar="mercado.cordones_mirar", aprox=a(680, 160), orientacion="arriba")
m.hot("patatas", 180, 128, 76, 22, nombre_visible="Puesto de patatas", mirar="mercado.patatas_mirar", aprox=a(218, 160), orientacion="arriba")
m.hot("salir", 0, 104, 10, 128, usar="mercado.salir", auto="true")
m.hot("cohete", 760, 104, 12, 128, usar="mercado.cohete", auto="true", condicion="estudio_visto && !cohete_caido")
m.npc("dot", 370, 162, sprite="dot", nombre_visible="Dot", hablar="mercado.dot", mirar="mercado.dot_mirar")
m.npc("sammy", 512, 170, sprite="nino", nombre_visible="Sammy", hablar="mercado.sammy", mirar="mercado.sammy_mirar")
m.npc("tuerto", 680, 124, sprite="viejo", nombre_visible="Vendedor de cordones", mirar="mercado.cordones_mirar", solido="false", aprox=a(680, 160))
m.npc("p1", 250, 176, sprite="prole1", nombre_visible="Gente", mirar="mercado.gente_mirar")
m.npc("p2", 600, 196, sprite="prole2", nombre_visible="Gente", mirar="mercado.gente_mirar")
m.npc("p3", 120, 168, sprite="funcionaria2", nombre_visible="Gente", mirar="mercado.gente_mirar")
m.spawn("inicio", 30, 172, "derecha").spawn("estudio", 891, 114, "abajo")
MAPAS.append(m)

m = mercado(Mapa("mercado_ruinas", "Mercado de Watney Street", ancho=960, al_entrar="ruinas.entrar", prota_tinte="#a9a9a9"))
m.col(486, 172, 68, 22, "crater")
m.hot("metralla", 470, 194, 14, 14, nombre_visible="Trozo de metralla brillante", mirar="ruinas.metralla_mirar", usar="ruinas.metralla", aprox=a(470, 218), orientacion="arriba", condicion="!metralla_brillante_cogida")
m.hot("salir", 0, 104, 10, 128, usar="ruinas.salir", auto="true")
m.npc("dot", 560, 206, sprite="dot", nombre_visible="Dot", mirar="ruinas.dot_mirar", hablar="ruinas.dot", aprox=a(590, 210), orientacion_jugador="izquierda")
m.npc("oficial", 420, 176, sprite="oficial", nombre_visible="Oficial", mirar="ruinas.oficial_mirar", condicion="patrulla_llega")
m.npc("g1", 640, 176, sprite="guardia", nombre_visible="Patrulla", mirar="ruinas.patrulla_mirar", condicion="patrulla_llega")
m.npc("g2", 610, 216, sprite="guardia", nombre_visible="Patrulla", mirar="ruinas.patrulla_mirar", condicion="patrulla_llega")
m.spawn("puesto", 218, 166, "derecha").spawn("calzada", 450, 210, "derecha")
MAPAS.append(m)

m = Mapa("estudio", "Estudio Crane", al_entrar="estudio.entrar", fondo_alt="loc-estudio_j6", fondo_alt_si="bombilla_encendida")
m.muros(x0=80, x1=400, fondo=96, puerta=(224, 256))
m.col(96, 114, 82, 34, "mostrador").col(260, 98, 28, 44, "silla").col(358, 116, 28, 46, "estufa")
m.hot("fotos", 88, 24, 140, 70, nombre_visible="Fotografías", mirar="estudio.fotos_mirar", aprox=a(158, 160), orientacion="arriba")
m.hot("cuarto", 330, 44, 30, 48, nombre_visible="Cuarto oscuro", mirar="estudio.cuarto_mirar", usar="estudio.cuarto", aprox=a(345, 108), orientacion="arriba")
m.hot("fondos", 240, 26, 72, 62, nombre_visible="Fondos pintados", mirar="estudio.fondos_mirar", aprox=a(240, 104), orientacion="arriba")
m.hot("salir", 224, 240, 32, 10, nombre_visible="Puerta", usar="estudio.salir", aprox=a(240, 236), orientacion="abajo")
m.hot("recorte", 178, 76, 20, 14, nombre_visible="Recorte enmarcado", mirar="j6_recorte_mirar", usar="j6_recorte_usar", aprox=a(190, 160), orientacion="arriba", condicion="jornada==6")
m.npc("crane", 200, 176, sprite="crane", nombre_visible="Abel Crane", hablar="estudio.crane", mirar="estudio.crane_mirar")
m.npc("camara", 320, 186, sprite="tripode", nombre_visible="Cámara", mirar="estudio.camara_mirar", solido="false", aprox=a(300, 196), orientacion_jugador="derecha")
m.spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 6
m = Mapa("archivo", "Sala de archivo", al_entrar="archivo.entrar",
         conos="60,50;300,130;300,200;170,200|60,50;150,214;40,236;40,90", cono_var="archivo_vigilado")
m.muros(fondo=96, puerta=(224, 256))
m.col(42, 100, 26, 112, "estanteria_izq").col(412, 100, 28, 112, "estanteria_der").col(192, 150, 98, 28, "mesa").col(230, 178, 22, 18, "silla")
m.hot("estanterias", 70, 26, 340, 66, nombre_visible="Estanterías", mirar="archivo.estanterias_mirar", usar="archivo.estanterias", aprox=a(240, 110), orientacion="arriba")
m.hot("telepantalla", 46, 34, 26, 18, nombre_visible="Telepantalla del techo", mirar="archivo.tele_mirar", aprox=a(86, 112), orientacion="arriba")
m.hot("lampara", 260, 132, 24, 12, nombre_visible="Lámpara verde", mirar="archivo.lampara_mirar", aprox=a(304, 164), orientacion="izquierda")
m.hot("parte", 228, 150, 26, 14, nombre_visible="Parte alterado", mirar="archivo.parte_mirar", usar="archivo.parte_coger", aprox=a(270, 196), orientacion="arriba", condicion="parte_en_mesa && !parte_cogido")
m.hot("salir", 224, 240, 32, 10, nombre_visible="Puerta", usar="archivo.salir", aprox=a(240, 236), orientacion="abajo")
m.spawn("puerta", 240, 232, "arriba")
MAPAS.append(m)

# ------------------------------------------------------------------ JORNADA 7
m = Mapa("suministros", "Cuarto de suministros", al_entrar="suministros.entrar")
m.muros(x0=120, x1=360, fondo=94, suelo=230, puerta=(224, 256))
m.col(132, 188, 44, 26, "cajas").col(316, 184, 28, 22, "cajas")
m.hot("hueco_tele", 218, 32, 46, 32, nombre_visible="Hueco tapado", mirar="suministros.hueco_mirar", aprox=a(240, 108), orientacion="arriba")
m.hot("balda_izq", 126, 62, 82, 16, nombre_visible="Tercera balda", mirar="suministros.balda_mirar", usar="suministros.cintas", aprox=a(168, 108), orientacion="arriba")
m.hot("balda_der", 276, 62, 80, 16, nombre_visible="Tercera balda", mirar="suministros.balda_mirar", usar="suministros.cintas", aprox=a(316, 108), orientacion="arriba")
m.hot("salir", 224, 226, 32, 10, nombre_visible="Puerta", usar="suministros.salir", aprox=a(240, 218), orientacion="abajo")
m.npc("nell", 232, 214, sprite="nell", nombre_visible="Limpiadora", mirar="suministros.nell_mirar", hablar="suministros.nell_hablar", condicion="nell_suministros", aprox=a(232, 180), orientacion_jugador="abajo")
m.npc("carrito", 254, 222, sprite="carrito", condicion="nell_suministros", solido="false")
m.spawn("puerta", 240, 200, "arriba")
MAPAS.append(m)

if __name__ == "__main__":
    for mapa in MAPAS:
        print("ok", mapa.guardar())
