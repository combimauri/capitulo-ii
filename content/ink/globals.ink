// Estado narrativo global. ink es la única fuente de verdad (diseño técnico §2).

VAR duda = 0
VAR sospecha = 0
VAR jornada = 0

// Identidad del protagonista (se fija en la Ficha de Afiliación, P.03).
VAR nombre = ""
VAR apellido = ""
VAR num = ""
VAR genero = "m"

// Variables cortas de concordancia de género (diseño técnico §4.3).
VAR o = "o"
VAR a_ = ""
VAR el = "el"
VAR El = "El"
VAR un = "un"
VAR del_ = "del"
VAR lo_ = "lo"

LIST inventario = reloj_ivy, ficha, lapiz_amory, foto_ivy, diario

// Prólogo
VAR ivy_vista = false
VAR reloj_cogido = false
VAR p_nell = false
VAR p_oficial = false

// Jornada 1
VAR gimnasia_hecha = false
VAR cf_j1_gimnasia = ""
VAR desayunado = false
VAR escalera_vista = false
VAR winston_se_fue = false
VAR hilda_j1 = false
VAR hilda_aprecio = 0
VAR avenida_vista = false
VAR nino_se_fue = false
VAR ficha_revisada = false
VAR voss_presente = true
VAR depto_visto = false
VAR parte_j1_enviado = false
VAR parte_j1_verbo = ""
VAR parte_j1_km = ""
VAR parte_j1_prisioneros = ""
VAR parte_j1_bajas = ""
VAR parte_j1_tibias = 0
VAR amory_charla = false
VAR nell_mirada = false
VAR cantina_vista = false
VAR noche_vista = false
VAR cf_j1_noticia = ""

// Jornada 2
VAR gimnasia_j2 = false
VAR cf_j2_gimnasia = ""
VAR parsons_j2 = false
VAR cf_j2_odio = ""
VAR cf_j2_odio_transicion = ""
VAR cf_j2_odio_amory = "no"            // "visto" si miró a Amory justo cuando se limpiaba las gafas
VAR odio_hecho = false
VAR depto_j2_visto = false
VAR frente_j2 = ""
VAR amory_reaccion = ""
VAR despacho_visto = false
VAR centro_visto = false
VAR pancarta_j2 = ""
VAR sueno_visto = false
