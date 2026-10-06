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

LIST inventario = reloj_ivy, ficha, lapiz_amory, foto_ivy, diario, compas, zonificacion, nota_amory, metralla_sammy, tarjeta_crane, metralla_brillante, parte_alterado, foto_ivy_restaurada, llave_calderas

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

// Jornada 3
VAR amory_borrado = false              // desde la mañana de la J3, Amory no ha existido nunca (para el mundo)
VAR gimnasia_j3 = false
VAR cf_j3_gimnasia = ""
VAR depto_j3_visto = false
VAR pell_hablado = false
VAR brooke_hablado = false
VAR voss_j3_visto = false
VAR voss_j3_insistir = false
VAR dp_j3_amory = ""                   // "aceptar" | "recordar"
VAR diario_amory = false               // pista para el diario (disponible desde la J5)
VAR lapiz_destruido = false
VAR pasillo_visto = false
VAR guardia_pasillo = false
VAR nell_se_fue = false
VAR noche_j3_vista = false

// Jornada 4
VAR gimnasia_j4 = false
VAR cf_j4_gimnasia = ""
VAR cf_j4_noticia = ""
VAR cajon_disponible = false
VAR foto_cogida = false
VAR depto_j4_visto = false
VAR registro_asignado = false
VAR cajon_abierto = false
VAR fieltro_levantado = false
VAR zonificacion_encontrada = false
VAR registro_j4_hecho = false
VAR registro_j4_lamina = "no"          // miró el mapa con la lámina de zonificación puesta
VAR registro_j4_compas = "no"
VAR registro_j4_fallos = 0
VAR cantina_j4_vista = false
VAR brooke_j4 = false
VAR ilegible_visto = false
VAR visita_prole_j4 = false
VAR ilegible_completado = false
VAR limehouse_visto = false
VAR casa_vista = false
VAR dot_hablado = false
VAR dot_confianza = 0
VAR crane_aparece = false
VAR crane_visto = false
VAR pub_visto = false
VAR viejo_hablado = false
VAR noche_j4_vista = false

// Jornada 5
VAR despertar_j5 = false
VAR foto_a_crane = false
VAR mercado_visto = false
VAR estudio_visto = false
VAR crane_info = 0
VAR cohete_caido = false
VAR sammy_j5 = ""                      // "correr" | "cubierto" | "paralizado"
VAR sammy_intento = false
VAR ruinas_vistas = false
VAR patrulla_llega = false
VAR metralla_brillante_cogida = false
VAR diario_sammy = false
VAR depto_j5_visto = false
VAR voss_espera = false
VAR registro_j5_hecho = false
VAR registro_j5_lamina = "no"
VAR registro_j5_compas = "no"
VAR registro_j5_fallos = 0
VAR registro_j5_lamina_puesta = "no"
VAR patron_conclusion = ""             // "proles" | "cobardes" | "casualidad"
VAR diario_cohetes = false
VAR noche_j5_vista = false
VAR diario_encontrado = false
VAR cono_avisado = false
VAR diario_iniciado = false
VAR diario_escondite = ""
// lo escrito en el diario (para el Capítulo II)
VAR diario_amory_escrita = false
VAR diario_sammy_escrita = false
VAR diario_cohetes_escrita = false
VAR diario_entradas = 0
VAR diario_ultima = ""
VAR diario_texto = ""

// Jornada 6
VAR gimnasia_j6 = false
VAR cf_j6_gimnasia = ""
VAR cf_j6_noticia = ""
VAR hilda_j6 = false
VAR depto_j6_visto = false
VAR archivo_visto = false
VAR archivo_revisado = false
VAR archivo_vigilado = false           // lo escribe el juego: ¿la telepantalla del techo mira hacia la mesa?
VAR prisioneros_j6 = ""
VAR dp_j6_parte = ""                   // "aceptar" | "recordar"
VAR diario_parte = false
VAR parte_en_mesa = false
VAR parte_cogido = false
VAR prueba_parte = false               // el parte alterado, prueba de buena fe ante la Hermandad (J8)
VAR bombilla_encendida = false
VAR estudio_j6_visto = false
VAR foto_restaurada = false
VAR diario_ivy = false
VAR crane_trastienda = false
VAR chocolate_visto = false
VAR diario_chocolate = false
VAR inspeccion_hecha = false
VAR escondite_j6_diario = ""
VAR escondite_j6_parte = ""
VAR escondite_j6_foto = ""
VAR diario_confiscado = false
VAR diario_hollin = false
VAR diario_escrito_hoy = 0
VAR diario_parte_escrita = false
VAR diario_ivy_escrita = false
VAR diario_chocolate_escrita = false
VAR comite_leyo = false                // el Comité leyó la primera página del diario: Sospecha mínima 40

// Jornada 7
VAR gimnasia_j7 = false
VAR cf_j7_gimnasia = ""
VAR depto_j7_visto = false
VAR cinta_rota = false
VAR hilda_en_minipax = false
VAR suministros_visto = false
VAR nell_suministros = false
VAR preguntas_nell = 0
VAR nell_respuesta = ""                // "aceptar" | "aceptar_tarde" | "dudar" | "negar" | "denunciar"
VAR diario_nell = false
VAR diario_nell_escrita = false
VAR noche_j7_vista = false
VAR cf_fb_ejecucion = ""
