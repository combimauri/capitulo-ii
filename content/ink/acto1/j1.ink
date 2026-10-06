// ACTO I · JORNADA 1 — La rutina (guion: docs/guion-detallado/01-acto-1.md)

// ==================================================================== J1.01 — El piso · 07:15
=== piso ===

= entrar
{ final_en_curso == "D":
    -> fd_piso
}
{ jornada == 2:
    -> j2_piso
}
{ jornada == 3:
    -> j3_piso
}
{ jornada == 4:
    -> j4_piso
}
{ jornada == 5:
    -> j5_piso
}
{ jornada == 6:
    -> j6_piso
}
{ jornada == 7:
    -> j7_piso
}
{ jornada == 8:
    -> j8_piso
}
{ jornada == 9:
    -> j9_piso
}
{ jornada == 10:
    -> j10_piso
}
{ jornada == 11:
    -> j11_piso
}
{ jornada == 12:
    -> j12_piso
}
{ gimnasia_hecha or jornada != 1:
    -> DONE
}
~ gimnasia_hecha = true
TELEPANTALLA: ¡Buenos días, camaradas de entre treinta y cuarenta! ¡Arriba, arriba! ¡Tablas de gimnasia! # sfx:silbato # jornada:1 # id:j1_01_tp_01
TELEPANTALLA: ¡Brazos arriba! ¡Uno, dos! ¡Uno, dos! # id:j1_01_tp_02
// La etiqueta del minijuego va en la línea que se muestra DESPUÉS de jugarlo;
// la lógica que depende del resultado va detrás de esa línea (diseño técnico §4.5).
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J1-GIMNASIA,expr=entusiasmo,dif=facil,coro=¡Uno!/¡Dos!,tutorial=si # id:j1_01_tp_05
{ cf_j1_gimnasia == "fallo":
    ~ sube_sospecha(3)
    TELEPANTALLA: ¡{num} {apellido}! ¡Más energía! ¡Así no se gana una guerra! # id:j1_01_tp_04
- else:
    TELEPANTALLA: ¡{num} {apellido}! ¡Eso es! ¡Así se mueve {un} camarada de verdad! ¡Mirad todos! # id:j1_01_tp_03
    PENSAMIENTO: Me ha nombrado. Delante de todo el bloque. # id:j1_01_pens_01
}
-> DONE

= cartel_mirar
{ jornada >= 4:
    -> j4_cartel_mirar
}
PENSAMIENTO: Ivy. Cada mañana te lo prometo. Cada mañana. Eurasia pagará cada piedra de la calle Stepney. # id:piso_cartel_mirar
-> DONE

= cartel_usar
{ final_en_curso == "D":
    -> fd_cartel
}
PENSAMIENTO: Nunca la dibujaron sonriendo. Ella siempre sonreía. # id:piso_cartel_usar_01
PENSAMIENTO: Pero así está bien: una mártir no sonríe. # id:piso_cartel_usar_02
-> DONE

= reloj_mirar
{ jornada >= 3:
    PENSAMIENTO: Las nueve y cuarenta. Siempre las nueve y cuarenta. # id:j3_01_reloj_mirar
    -> DONE
}
PENSAMIENTO: Las nueve y cuarenta. Nunca le he dado cuerda. No quiero que vuelva a andar. # id:piso_reloj_mirar
-> DONE

= reloj_usar
PENSAMIENTO: No. Se queda así. # id:piso_reloj_usar
-> DONE

= tele_mirar
PENSAMIENTO: Se le puede bajar el volumen, pero no apagarla. Nadie querría apagarla. Sería como quedarse a oscuras. # id:piso_tele_mirar
-> DONE

= tele_usar
PENSAMIENTO: Está en el volumen justo. El Partido sabe cuál es el volumen justo. # id:piso_tele_usar
-> DONE

= ventana_mirar
PENSAMIENTO: Los cuatro ministerios. El de la Verdad, el del Amor, el de la Abundancia. # id:piso_ventana_mirar_01
PENSAMIENTO: Y el mío: el de la Paz. Desde aquí parecen montañas. # id:piso_ventana_mirar_02
-> DONE

= hornillo_mirar
PENSAMIENTO: Una sola llama, como todos los hornillos del bloque. # id:piso_hornillo_mirar
-> DONE

= hornillo_usar
{ desayunado:
    PENSAMIENTO: Ya he desayunado. Repetir sería acaparar. # id:piso_hornillo_usar_01
- else:
    ~ desayunado = true
    PENSAMIENTO: Café de la Victoria. Sabe a tierra mojada. # id:piso_hornillo_usar_02
    PENSAMIENTO: Pero está caliente, y eso es más de lo que tienen en Eurasia. # id:piso_hornillo_usar_03
}
-> DONE

= cama_mirar
PENSAMIENTO: La cama está hecha. Una cama deshecha es una mente deshecha. # id:piso_cama_mirar
-> DONE

= cajon_mirar
PENSAMIENTO: Ahí guardo lo único que saqué de la calle Stepney, aparte del reloj. # id:piso_cajon_mirar
-> DONE

= cajon_usar
{ cajon_disponible:
    -> j4_cajon_piso
}
PENSAMIENTO: Ahora no. # id:piso_cajon_usar_no
-> DONE

= abrigo_mirar
PENSAMIENTO: Mi abrigo. Gris, como todos los abrigos. # id:piso_abrigo_mirar
-> DONE

= armario_mirar
PENSAMIENTO: Dos monos azules, una camisa, el abrigo de invierno. Todo lo que necesito. # id:piso_armario_mirar
-> DONE

= puerta_usar
{ not desayunado:
    PENSAMIENTO: Primero el desayuno. Un estómago vacío es un estómago desleal. # id:piso_puerta_usar_01
    -> DONE
}
{ jornada == 5:
    -> j5_salir_piso
}
{ jornada == 6:
    -> j6_salir_piso
}
{ jornada == 10:
    # escena:escalera # pos:piso
    -> DONE
}
{ jornada == 12:
    -> j12_parque
}
{ jornada >= 3:
    -> j3_salir_piso
}
# escena:escalera # pos:piso
-> DONE

// ==================================================================== J1.02 — La escalera
=== escalera ===

= entrar
{ final_en_curso == "D":
    -> fd_escalera
}
{ jornada == 2:
    -> j2_parsons
}
{ jornada == 6:
    -> j6_hilda
}
{ jornada == 10:
    -> j10_escalera
}
{ escalera_vista:
    -> DONE
}
~ escalera_vista = true
PENSAMIENTO: Col hervida y cañerías viejas. Como todas las mañanas. # id:j1_02_pens_00
-> DONE

= ascensor_mirar
PENSAMIENTO: Averiado. Desde la Semana del Odio pasada. Lo arreglarán cuando termine la guerra. # id:j1_02_ascensor_01
PENSAMIENTO: O antes, si Hilda escribe otra carta. # id:j1_02_ascensor_02
-> DONE

= puerta_mirar
PENSAMIENTO: Mi puerta. 5B. # id:j1_02_puerta_mirar
-> DONE

= cartel_mirar
PENSAMIENTO: El Gran Hermano te vigila. En cada rellano. Así nadie está solo nunca. # id:j1_02_cartel_mirar
-> DONE

= parsons_mirar
PENSAMIENTO: Los Parsons. Se oye a los niños jugar a los espías. # id:j1_02_parsons_mirar
-> DONE

= parsons_npc_mirar
PENSAMIENTO: Parsons. Sudoroso y radiante, como siempre. # id:j2_02_parsons_mirar
-> DONE

= parsons_hablar
PARSONS: ¡A la Semana del Odio le quedan diez días! ¡Diez! ¡Magnífico! # id:j2_02_parsons_hablar
-> DONE

= hija_mirar
PENSAMIENTO: La niña lleva una libretita. Apunta cosas. # id:j2_02_hija_mirar
-> DONE

= hija_hablar
HIJA PARSONS: Usted dice un nombre. Lo he apuntado. # id:j2_02_hija_hablar
-> DONE

= nino_mirar
PENSAMIENTO: El pequeño de los Parsons. Pañuelo rojo de los Espías y una cuerda para ahorcar muñecos. # id:j2_02_nino_mirar
-> DONE

= sube_mirar
PENSAMIENTO: Arriba vive Smith, en el séptimo. # id:j1_02_sube_mirar
-> DONE

= winston_mirar
PENSAMIENTO: El camarada Smith, del séptimo. Trabaja en el Miniver. Siempre parece que acaba de despertarse de un mal sueño. # id:j1_02_winston_mirar
-> DONE

= winston
PROTAGONISTA: ¡Buenos días, camarada Smith! Hoy hay colecta para la Semana del Odio. ¿Ha visto los carteles nuevos? # id:j1_02_prot_01
WINSTON: …Sí. Buenos días. # id:j1_02_winston_01
PROTAGONISTA: ¿Vendrá esta noche al Centro de la Comunidad? Vamos a ensayar los cánticos. # id:j1_02_prot_02
WINSTON: Tengo… trabajo atrasado. # sfx:tos # id:j1_02_winston_02
WINSTON: Quizá. # id:j1_02_winston_03
~ winston_se_fue = true
PENSAMIENTO: "Quizá." Un miembro del Partido no dice "quizá". # refrescar # id:j1_02_pens_01
-> DONE

= hilda_mirar
PENSAMIENTO: Hilda Grubb, del Comité de la Casa. Lleva la lata de la colecta como si fuera un estandarte. # id:j1_02_hilda_mirar
-> DONE

= hilda
{ hilda_j1:
    HILDA: ¡Esta noche, ensayo de cánticos! ¡No faltes! # id:j1_02_hilda_ya
    -> DONE
}
~ hilda_j1 = true
HILDA: ¡{nombre} {apellido}! ¡Mi camarada más puntual! # id:j1_02_hilda_01
HILDA: Para la Semana del Odio. Este año vamos a hacer la efigie de Goldstein más grande del distrito. ¡Tres metros! ¡Con dientes! # id:j1_02_hilda_02
* [Tome. Todo lo que llevo.] # decision:D-J1-COLECTA
    ~ hilda_aprecio += 1
    HILDA: ¡Ojalá todo el bloque fuera como tú! # id:j1_02_hilda_03
* [Tome, camarada.]
    HILDA: Gracias, gracias. Cada moneda es un clavo en el ataúd de Goldstein. # id:j1_02_hilda_04
- HILDA: ¿Has visto a Smith? Nunca da más de lo justo. Nunca canta. Siempre tiene "trabajo atrasado". # id:j1_02_hilda_05
HILDA: Yo solo lo digo. # id:j1_02_hilda_06
* [Tiene razón. Lo vigilaré.] # decision:D-J1-SMITH
    HILDA: Ese es el espíritu. # id:j1_02_hilda_07
* [Estará enfermo. Tose mucho.]
    HILDA: Hum. La tos no le impide escribir… lo que sea que escribe. # id:j1_02_hilda_08
- HILDA: ¡Ah! Y esta semana sale el cartel nuevo de los mártires. Tu Ivy sale en primera fila. Deberías estar orgullos{o}. # id:j1_02_hilda_09
PROTAGONISTA: Lo estoy. # id:j1_02_prot_03
-> DONE

= bajar
{ jornada == 2:
    -> j2_bajar
}
{ jornada == 6:
    -> j6_bajar
}
{ jornada == 10:
    { rectificacion_hecha:
        PENSAMIENTO: A casa. # id:j10_06_bajar_no
        -> DONE
    }
    -> j10_bajar
}
{ not hilda_j1:
    HILDA: ¡{nombre}! ¡Espera, espera, que no se escapa nadie sin pasar por la lata! # id:j1_02_hilda_espera
    -> hilda
}
# escena:avenida # pos:portal
-> DONE

// ==================================================================== J1.03 — La calle
=== avenida ===

= entrar
{ jornada == 11:
    -> j11_avenida
}
{ avenida_vista:
    -> DONE
}
~ avenida_vista = true
PENSAMIENTO: La avenida de la Victoria. Al fondo, el Ministerio de la Paz. Mi Ministerio. # id:j1_03_pens_00
-> DONE

= portal
{ jornada == 11:
    -> j11_portal
}
-> portal_mirar

= portal_mirar
PENSAMIENTO: Las Mansiones Victoria. Ochocientas viviendas y un solo ascensor que funciona a veces. # id:j1_03_portal_mirar
-> DONE

= consignas_mirar
PENSAMIENTO: Tres verdades. Las aprendí antes de aprender a leer. Ivy las cantaba saltando a la comba. # id:j1_03_consignas_mirar
-> DONE

= helicoptero_mirar
PENSAMIENTO: La Patrulla. No me preocupa: quien no tiene nada que esconder no tiene nada que temer. # id:j1_03_heli_mirar
-> DONE

= proles_mirar
PENSAMIENTO: Dos proles discuten a gritos sobre un número de lotería. # id:j1_03_proles_mirar_01
PENSAMIENTO: Proles. Como animales. El Partido dice que a los proles y a los animales hay que dejarlos en paz. Es generoso por su parte. # id:j1_03_proles_mirar_02
-> DONE

= nino_mirar
PENSAMIENTO: Un niño prole. Lleva un trozo de metralla colgado al cuello con un cordel. # id:j1_03_nino_mirar
-> DONE

= nino
NIÑO: ¿Tiene un cigarrillo, camarada? ¿Una moneda? # id:j1_03_nino_01
PENSAMIENTO: Los Cigarrillos de la Victoria son para el Partido. # id:j1_03_nino_02
~ nino_se_fue = true
PENSAMIENTO: Se va silbando. # refrescar # id:j1_03_nino_03
-> DONE

= minipax
# escena:vestibulo # pos:entrada
-> DONE

// ==================================================================== J1.04 — Vestíbulo del Minipax
=== vestibulo ===

= entrar
{ ficha_revisada:
    -> DONE
}
PENSAMIENTO: Mármol. Siempre hace frío aquí dentro, incluso en agosto. # id:j1_04_pens_00
-> DONE

= titulo_mirar
PENSAMIENTO: Ministerio de la Paz. La guerra es la paz. Aquí se hace la paz cada día. # id:j1_04_titulo_mirar
-> DONE

= tele_mirar
PENSAMIENTO: "Victoria." Siempre hay una victoria en alguna parte. # id:j1_04_tele_mirar
-> DONE

= guardia_mirar
PENSAMIENTO: Uniforme negro, porra al cinto. No parpadean nunca. # id:j1_04_guardia_mirar
-> DONE

= guardia2_mirar
PENSAMIENTO: Otro guardia. Mira la puerta como si esperara a alguien en concreto. # id:j1_04_guardia2_mirar
-> DONE

= guardia
GUARDIA: Ficha. # id:j1_04_guardia_01
* [Entregar la ficha.]
    PENSAMIENTO: Me mira la cara. Luego la foto. Luego la cara otra vez. # id:j1_04_pens_01
    ~ ficha_revisada = true
    GUARDIA: Departamento de Partes y Cartografía. Planta catorce. El ascensor de la izquierda funciona. # refrescar # id:j1_04_guardia_02
    PENSAMIENTO: Aquí los ascensores siempre funcionan. # id:j1_04_pens_02
- -> DONE

= ascensor_mirar
PENSAMIENTO: El ascensor de la izquierda. Funciona. # id:j1_04_ascensor_mirar
-> DONE

= ascensor
{ not ficha_revisada:
    PENSAMIENTO: Primero, la ficha. # id:j1_04_ascensor_ficha
    -> DONE
}
# escena:departamento # pos:puerta
-> DONE

// ==================================================================== J1.05 — Departamento de Partes y Cartografía
=== depto ===

= entrar
{ jornada == 2:
    -> j2_entrar
}
{ jornada == 3:
    -> j3_entrar
}
{ jornada == 4:
    -> j4_entrar
}
{ jornada == 5:
    -> j5_entrar
}
{ jornada == 6:
    -> j6_entrar
}
{ jornada == 7:
    -> j7_entrar
}
{ jornada == 8:
    -> j8_entrar
}
{ jornada == 9:
    -> j9_entrar
}
{ jornada == 11:
    -> j11_entrar
}
{ jornada == 12:
    -> j12_entrar
}
{ depto_visto:
    -> DONE
}
~ depto_visto = true
VOSS: Camarada {apellido}. Un momento. # id:j1_05_voss_01
PENSAMIENTO: El Subdirector Voss. Partido Interior. Me habla a mí. # id:j1_05_pens_01
VOSS: Hoy sale el cartel nuevo de los mártires. Su hermana… # esperar:0.9 # id:j1_05_voss_02
VOSS: …calle Stepney. Una tragedia. De esas tragedias que nos hacen fuertes. # id:j1_05_voss_03
PROTAGONISTA: Sí, Subdirector. Gracias, Subdirector. # id:j1_05_prot_01
VOSS: El Partido no olvida a los suyos. # id:j1_05_voss_04
VOSS: Tiene un parte urgente en su tubo. Malabar. Que sea… memorable. # id:j1_05_voss_05
~ voss_presente = false
AMORY: ¿Te ha hablado Voss? ¿A ti? En dos años a mí solo me ha dicho "su lápiz hace ruido". # refrescar # id:j1_05_amory_01
AMORY: Mira. Nueva proyección. Con esta, Oceanía ocupa un cuarenta por ciento más de papel. # id:j1_05_amory_02
AMORY: Y no he mentido en nada, ¿eh? Solo he… estirado el mundo. # id:j1_05_amory_03
-> DONE

= amory_mirar
PENSAMIENTO: Felix Amory. Dibuja mapas con la lengua entre los dientes. En los márgenes, pájaros minúsculos. # id:j1_05_amory_mirar
-> DONE

= amory
{ jornada == 2:
    -> j2_amory
}
{ parte_j1_enviado:
    AMORY: ¡A la cantina! Hoy hay guiso. Bueno, siempre hay guiso. # id:j1_05_amory_cantina
    -> DONE
}
AMORY: ¿Qué? ¿Te gusta? # id:j1_05_amory_04
-> amory_preguntas

= amory_preguntas
* [¿Para qué son los pájaros?]
    AMORY: Para que los mapas tengan algo vivo. Los quito antes de entregarlos, tranquil{o}. # id:j1_05_amory_05
    -> amory_preguntas
* [¿Eso está autorizado?]
    AMORY: Todo lo que hace más grande a Oceanía está autorizado. Es casi una ley natural. # id:j1_05_amory_06
    -> amory_preguntas
* [Tengo que trabajar.]
    AMORY: ¡El deber! Ve, ve. Malabar no se va a conquistar sola. # id:j1_05_amory_07
    -> DONE
* -> DONE

= mesa_mirar
PENSAMIENTO: Mi mesa. Máquina de escribir, tubo neumático, telepantalla. Todo lo que hace falta para ganar una guerra. # id:j1_05_mesa_mirar
-> DONE

= mesa
{ jornada == 2:
    -> j2_mesa
}
{ jornada == 3:
    -> j3_mesa
}
{ parte_j1_enviado:
    PENSAMIENTO: El parte ya va camino de las telepantallas. # id:j1_05_mesa_hecha
    -> DONE
}
# sfx:tubo
PENSAMIENTO: Del tubo sale un cilindro con un papel enrollado. # id:j1_05_tubo
PENSAMIENTO: Esta noche lo leerán en todas las telepantallas de Oceanía. Mis palabras. # minijuego:parte,documento=parte_j1,vars=parte_j1 # id:j1_05_pens_02
{ parte_j1_tibias > 0:
    ~ sube_sospecha(2 * parte_j1_tibias)
}
~ parte_j1_enviado = true
# refrescar
-> DONE

= mapa_mirar
{ jornada == 3:
    -> j3_mapa
}
PENSAMIENTO: Malabar. Nuestras banderas rojas avanzan como sangre limpia. Las negras retroceden. Así es la historia. # id:j1_05_mapa_mirar
-> DONE

= memoria_mirar
PENSAMIENTO: El agujero de la memoria. Lo que cae ahí deja de existir. Los borradores, los errores… Es higiénico. # id:j1_05_memoria_mirar
-> DONE

= despacho_mirar
PENSAMIENTO: El despacho del Subdirector. El único con ventana de toda la planta. # id:j1_05_despacho_mirar
-> DONE

= despacho
{ jornada == 3:
    -> j3_despacho
}
PENSAMIENTO: No se entra sin ser llamad{o}. # id:j1_05_despacho_usar
-> DONE

= personal_mirar
PENSAMIENTO: El archivador del personal. Una ficha por cada uno de nosotros, por orden alfabético. # id:j1_05_personal_mirar
-> DONE

= personal
{ jornada == 3:
    -> j3_personal
}
PENSAMIENTO: No tengo nada que buscar ahí. # id:j1_05_personal_usar
-> DONE

= registro_mirar
{ jornada >= 4:
    -> j4_registro_mirar
}
PENSAMIENTO: La mesa del Registro de Impactos. Un mapa de Londres bajo un cristal. Hoy no la usa nadie. # id:j1_05_registro_mirar
-> DONE

= tele_mirar
PENSAMIENTO: La telepantalla de la sala. Nos ve a todos a la vez. Es un consuelo. # id:j1_05_tele_mirar
-> DONE

= funcionario_mirar
PENSAMIENTO: Teclea sin levantar la vista. Así se trabaja. # id:j1_05_func_mirar
-> DONE

= voss_mirar
PENSAMIENTO: Abrigo largo, aunque estemos dentro. Guantes. # id:j1_05_voss_mirar
-> DONE

= nell_mirar
~ nell_mirada = true
PENSAMIENTO: Una prole de la limpieza. # id:j1_05_nell_mirar
-> DONE

= nell_hablar
PENSAMIENTO: Tengo trabajo. # id:j1_05_nell_hablar
-> DONE

= salir
{ jornada == 2:
    -> j2_salir
}
{ jornada == 3:
    -> j3_salir
}
{ jornada == 4:
    -> j4_salir
}
{ jornada == 5:
    -> j5_salir
}
{ jornada == 7:
    -> j7_salir
}
{ jornada == 8:
    -> j8_salir
}
{ jornada >= 9:
    PENSAMIENTO: Hoy no es día de quedarse en la mesa. # id:j9_salir_depto
    -> DONE
}
{ not parte_j1_enviado:
    PENSAMIENTO: Primero el parte. Malabar no espera. # id:j1_05_salir_no
    -> DONE
}
# escena:cantina # pos:puerta
-> DONE

// ==================================================================== J1.06 — Cantina del Minipax
=== cantina ===

= entrar
{ jornada == 4:
    -> j4_cantina
}
{ jornada == 10:
    -> j10_cantina
}
{ cantina_vista:
    -> DONE
}
~ cantina_vista = true
AMORY: ¿Sabes lo que es un buen mapa? # id:j1_06_amory_01
AMORY: Un buen mapa no muestra dónde están las cosas. Muestra dónde el Partido necesita que estén. Es lo más bonito que existe. # id:j1_06_amory_02
PROTAGONISTA: Lo dices como si fuera poesía. # id:j1_06_prot_01
AMORY: ¡Es que lo es! En la próxima edición del Diccionario quitan "retirada". Ya no existirán las retiradas. Solo "avances rectificados". # id:j1_06_amory_03
AMORY: ¿No es precioso? Si no hay palabra, no hay retirada. Si no hay retirada… # id:j1_06_amory_04
PROTAGONISTA: …siempre ganamos. # id:j1_06_prot_02
AMORY: ¡Siempre ganamos! Por Malabar. # id:j1_06_amory_05
PENSAMIENTO: Amory habla demasiado rápido. Pero es de los buenos. De los que creen. # id:j1_06_pens_01
TELEPANTALLA: …la producción de botas en el último trimestre ha superado el plan en un noventa y ocho por ciento… # id:j1_06_tp_01
CARTEL: La tarde pasa entre partes y banderitas. # id:j1_06_cartel # escena:piso_noche # pos:puerta
-> DONE

= salir
{ jornada == 4:
    -> j4_cantina_salir
}
PENSAMIENTO: Todavía no he terminado de comer. # id:j1_06_salir_no
-> DONE

= amory
AMORY: Come, come. El guiso se enfría y luego sabe a guiso frío. # id:j1_06_amory_06
-> DONE

// ==================================================================== J1.07 — El piso · noche
=== piso_noche ===

= entrar
{ jornada == 3:
    -> j3_noche
}
{ jornada == 4:
    -> j4_noche
}
{ jornada == 5:
    -> j5_noche
}
{ jornada == 6:
    -> j6_noche
}
{ jornada == 7:
    -> j7_noche
}
{ jornada == 8:
    -> j8_noche
}
{ jornada == 9:
    -> j9_noche
}
{ jornada == 10:
    -> j10_noche
}
{ jornada == 11:
    -> j11_noche
}
{ noche_vista:
    -> DONE
}
~ noche_vista = true
# sfx:fanfarria
TELEPANTALLA: ¡Atención! ¡Atención! ¡Noticia gloriosa del frente de Malabar! # id:j1_07_tp_01
TELEPANTALLA: Nuestras gloriosas fuerzas han {parte_j1_verbo} en el sector del río Malabar, ganando {parte_j1_km} kilómetros de terreno. # id:j1_07_tp_02
TELEPANTALLA: Han sido capturados {parte_j1_prisioneros} prisioneros euroasiáticos. Las bajas enemigas se estiman en {parte_j1_bajas}. # id:j1_07_tp_03
TELEPANTALLA: ¡Gloria a nuestras tropas! ¡Gloria al Gran Hermano! # cf:id=CF-J1-NOTICIA,expr=jubilo,dif=facil,coro=¡Victoria!/¡Malabar!/¡Gran Hermano! # id:j1_07_tp_04
{ cf_j1_noticia == "fallo":
    ~ sube_sospecha(3)
}
PENSAMIENTO: Son mis palabras. Las está diciendo toda Oceanía. Ivy, ¿lo oyes? Esto es por ti. # id:j1_07_pens_01
-> DONE

= cartel_mirar
{ jornada >= 8:
    -> j8_cartel_noche
}
{ jornada == 7 and (nell_respuesta == "aceptar" or nell_respuesta == "dudar"):
    -> j7_cartel_mirar
}
{ jornada >= 3:
    PENSAMIENTO: Ivy. La miro mucho rato. # id:j3_06_cartel_mirar
    -> DONE
}
PENSAMIENTO: Hoy hemos ganado {parte_j1_km} kilómetros. Mañana ganaremos más. # id:j1_07_cartel_mirar
-> DONE

= cartel_usar
{ jornada == 11:
    -> j11_cartel_usar
}
-> cartel_mirar

= abrigo_mirar
PENSAMIENTO: Mi abrigo. Gris, como todos los abrigos. # id:j1_07_abrigo_mirar
-> DONE

= abrigo
{ jornada == 5:
    -> j5_abrigo
}
PENSAMIENTO: Mañana me hará falta. # id:j1_07_abrigo_usar
-> DONE

= hueco_mirar
-> j5_hueco_mirar

= ventana_mirar
{ jornada >= 3:
    -> j3_ventana
}
PENSAMIENTO: La ciudad a oscuras. Solo brillan los ministerios. # id:j1_07_ventana_mirar
-> DONE

= tele_mirar
{ jornada >= 3:
    PENSAMIENTO: Música marcial. Tambores, trompetas. Nada que pensar. # id:j3_06_tele_mirar
    -> DONE
}
PENSAMIENTO: El noticiero repite la victoria. Una y otra vez. Nunca me canso. # id:j1_07_tele_mirar
-> DONE

= cama_mirar
PENSAMIENTO: Mañana, a las siete y cuarto, el silbato. # id:j1_07_cama_mirar
-> DONE

= dormir
{ jornada == 3:
    -> j3_dormir
}
{ jornada == 4:
    -> j4_dormir
}
{ jornada == 5:
    -> j5_dormir
}
{ jornada == 6:
    -> j6_dormir
}
{ jornada == 7:
    -> j7_dormir
}
{ jornada == 8:
    -> j8_dormir
}
{ jornada == 9:
    -> j9_dormir
}
{ jornada == 10:
    -> j10_dormir
}
{ jornada == 11:
    -> j11_dormir
}
~ jornada = 2
~ desayunado = false
CARTEL: JORNADA 2 # fx:negro # id:j1_07_jornada2 # escena:piso # pos:cama
-> DONE
