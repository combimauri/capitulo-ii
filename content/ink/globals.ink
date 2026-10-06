// Estado narrativo global. ink es la única fuente de verdad (diseño técnico §2).

VAR duda = 0
VAR sospecha = 0
VAR jornada = 0

// Dónde está el protagonista (lo escribe el motor; el arresto se adapta al lugar)
VAR escena_actual = ""

// Opciones del jugador que cambian reglas (las escribe el motor, diseño técnico §9)
VAR opc_sigilo_reducido = false

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

LIST inventario = reloj_ivy, ficha, lapiz_amory, foto_ivy, diario, compas, zonificacion, nota_amory, metralla_sammy, tarjeta_crane, metralla_brillante, parte_alterado, foto_ivy_restaurada, llave_calderas, directiva, copia_planilla, hoja_planilla, libro, tubo, times_falso, sobre_miniver, times_original, chapa, foto_sotano, dibujos_amory, mapa_malabar, parte_original, carta

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

// ==================================================================== ACTO III
// Jornada 8
VAR gimnasia_j8 = false
VAR cf_j8_gimnasia = ""
VAR depto_j8_visto = false
VAR registro_j8_hecho = false
VAR registro_j8_lamina = "no"
VAR registro_j8_compas = "no"
VAR registro_j8_fallos = 0
VAR registro_j8_lamina_puesta = "no"
VAR directiva_leida = false
VAR pista_combinacion = false
VAR nell_j8 = false                    // J8.00: Nell espera en el cuarto de suministros (aceptar_tarde)
VAR calderas_vistas = false
VAR montacargas_j8 = ""                // "limpio" | "chirrido"
VAR planta11_vista = false
VAR planta11_vuelta = false
VAR guardia_entrante = false
VAR llave_ar = false
VAR llave_devuelta = false
VAR llaves_j8_fallos = 0
VAR cerrojo_llave = false
VAR cerrojo_j8 = ""                    // "abierta" | "fallo" | "tiempo"
VAR cerrojo_intentos = 0
VAR archivo_r_visto = false
VAR planilla_vista = false
VAR mercado_planilla = false
VAR estante_1979 = false
VAR prueba_sacada = ""                 // "copia" | "hoja"
VAR hoja_robada = false
VAR copia_lineas = 0
VAR copia_firma = false
VAR j8_salida = false
VAR nell_calderas = false
VAR nell_confianza = 0
VAR iniciacion_vida = ""               // "Sí" | "No" (O'Brien las reproduce desde la grabación de Crane)
VAR iniciacion_matar = ""
VAR iniciacion_mentir = ""
VAR iniciacion_callar = ""
VAR iniciacion_ivy = ""
VAR iniciacion_traicion = ""
VAR libro_fragmentos = 0
VAR diario_planilla = false
VAR diario_planilla_escrita = false
VAR diario_libro_guerra = false
VAR diario_libro_guerra_escrita = false
VAR noche_j8_vista = false

// Jornada 9
VAR gimnasia_j9 = false
VAR cf_j9_gimnasia = ""
VAR depto_j9_visto = false
VAR cf_j9_voss = ""
VAR nota_j9 = false
VAR tubo_entregado = false
VAR miniver_visto = false
VAR winston_j9 = false
VAR julia_j9 = false
VAR syme_hablado = false
VAR lavabos_vistos = false
VAR vaho = false
VAR abrigo_colgado = false
VAR cf_j9_lavabo = ""
VAR panel_abierto = false
VAR times_original_visto = false
VAR diario_times = false
VAR diario_times_escrita = false
VAR diario_libro_ignorancia = false
VAR diario_libro_ignorancia_escrita = false
VAR noche_j9_vista = false

// Jornada 10
VAR hilda_j10 = false
VAR cantina_j10 = false
VAR cf_j10_amory = ""
VAR cf_j10_mitin = ""
VAR cf_j10_mitin_bh = 0
VAR cf_j10_mitin_pancartas = 0
VAR pell_j10 = ""                      // "negacion" | "verdad"
VAR diario_amory_confesion = false
VAR diario_amory_confesion_escrita = false
VAR diario_estasia = false
VAR diario_estasia_escrita = false
VAR rectificacion_1 = ""
VAR rectificacion_2 = ""
VAR nota_nell_j10 = false
VAR cargando_prueba = false             // lleva encima el mapa o el parte (Voss solo importa entonces)
VAR mision_j10 = ""                    // "" | "hecha" | "fallida" | "tarde"
VAR brooke_distrae = false
VAR prueba_rectificacion = false
VAR rectificacion_hecha = false
VAR diario_libro_doblepensar = false
VAR diario_libro_doblepensar_escrita = false
VAR parsons_detenido = false
VAR noche_j10_vista = false

// Jornada 11
VAR depto_j11_visto = false
VAR cf_j11_voss = ""
VAR brooke_revelada = false
VAR minimor_visto = false
VAR lista_proles_vista = false
VAR funcionaria_fuera = false
VAR archivo_b_visto = false
VAR ivy_revelada = false
VAR dp_j11_ivy = ""                    // "aceptar" | "recordar"
VAR expediente_visto = false
VAR foto_sotano_cogida = false
VAR len_decision = ""                  // "cambio" | "nada" | "tachado" | "rabia"
VAR len_salvado = false
VAR len_sustituto = ""
VAR len_chico = false
VAR crane_sospechado = false
VAR charrington_visto = false
VAR cartel_arrancado = false
VAR fragmento_4 = false
VAR diario_ivy_verdad = false
VAR diario_ivy_verdad_escrita = false
VAR diario_len = false
VAR diario_len_escrita = false
VAR diario_libro_pasado = false
VAR diario_libro_pasado_escrita = false
VAR noche_j11_vista = false

// Jornada 12
VAR ejecucion_vista = false
VAR cf_j12_ejecucion = ""
VAR nell_aviso = false
VAR brooke_j12 = false
VAR crane_revelado = false
VAR crane_decision = ""                // "aceptar" | "fingir" | "negar" | "huir"
VAR crane_sigue = false
VAR estudio_j12_visto = false
VAR persecucion_vista = false
VAR atajo_usado = false
VAR casa_dot_vista = false
VAR mensaje_nell = false
VAR reloj_en_marcha = false
VAR diario_dot = false
VAR diario_dot_escrita = false

// Finales
VAR fb_variante = "temprano"           // "temprano" | "trato"

// La frase que se escribió en cada entrada del diario (el Capítulo II la reutiliza)
VAR diario_amory_frase = ""
VAR diario_sammy_frase = ""
VAR diario_cohetes_frase = ""
VAR diario_parte_frase = ""
VAR diario_ivy_frase = ""
VAR diario_chocolate_frase = ""
VAR diario_nell_frase = ""
VAR diario_planilla_frase = ""
VAR diario_libro_guerra_frase = ""
VAR diario_times_frase = ""
VAR diario_libro_ignorancia_frase = ""
VAR diario_amory_confesion_frase = ""
VAR diario_estasia_frase = ""
VAR diario_libro_doblepensar_frase = ""
VAR diario_ivy_verdad_frase = ""
VAR diario_len_frase = ""
VAR diario_libro_pasado_frase = ""
VAR diario_dot_frase = ""

// ==================================================================== ACTO IV
VAR metralla_cierre = false            // lo calcula el Capítulo II (intentó salvar a Sammy o guarda su metralla)
VAR cap_apertura = ""
VAR cap_mov1 = ""
VAR cap_mov2 = ""
VAR cap_mov3 = ""
VAR cap_mov4 = ""
VAR cap_cierre = ""
VAR cap_texto = ""
VAR cap_ivy_corregida = "no"
VAR cap_voces = 0
VAR final_en_curso = ""                // "C" | "D" | "E": el desenlace que se está jugando
VAR fc_variante = "sospecha"           // Final C: "sospecha" | "cripta" | "sin_libro" | "libro_vive"
VAR mapa_deducido = ""                 // "si": lo dedujo el jugador; "no": lo dedujo el protagonista
VAR mapa_derrumbes = 0
VAR san_clemente_deducido = false
VAR shadwell_visto = false
VAR tablon_abierto = false
VAR escondido = false                  // lo escribe el motor: el protagonista está en un nicho o un escondite
VAR silbido1 = false
VAR silbido2 = false
VAR impactos_esquivados = 0
VAR tunel1_visto = false
VAR taller_visto = false
VAR taller_pared = false
VAR taller_teles = false
VAR taller_mesa = false
VAR tunel3_visto = false
VAR crane_perdido = false
VAR crane_distancia = 0                // lo escribe el motor: distancia de Crane al protagonista en los túneles
VAR tunel4_visto = false
VAR cripta_vista = false
VAR crane_en_cripta = false
VAR carta_ivy = false
VAR pregunta_jaula = false
VAR crane_humillado = false
VAR capitulo_escrito = false
VAR cf_j13_sacar = ""
// Finales C y D
// Aspecto del protagonista en los finales: "" · "preso" · "golpeado" · "cafe" (cada uno, una hoja de sprites)
VAR prota_aspecto = ""
VAR choques = 0
VAR crane_alcanza = false
VAR hambre = 100
VAR palizas = 0
VAR fd_limehouse_visto = false
VAR celda_vista = false
VAR celda_evento = 0
VAR pan_dado = ""                      // "dado" | "comido"
VAR obrien_visto = false
VAR dial_respuesta = ""
VAR traicion_101 = ""                  // "nell" | "dot" | "brooke" | "len" | "ivy"
VAR cafe_visto = false
VAR fd_nombre_tiza = false
VAR fd_dot_vista = false
VAR cf_fd_dot = ""
VAR fd_escalera_vista = false
VAR fd_piso_visto = false
VAR fd_foto_pegada = false
VAR resistencia_d = ""                 // "aguanto" | "delatado"
VAR aguanto_24h = false
VAR libro_delatado = false
