// ACTO IV · JORNADA 13 — Bajo las campanas (guion: docs/guion-detallado/04-acto-4.md)
// Shadwell, el mapa de los pájaros, los túneles (cohetes, el taller, Crane, los carteles), la cripta de San Clemente,
// la conversación con Goldstein, el Capítulo II y la decisión final.

// ==================================================================== J13.00 — Comprobación de entrada
=== j13_entrada ===
{ duda < 30:
    -> j13_arrepentimiento
}
CARTEL: Amanecer. # fx:negro # id:j13_00_cartel # escena:shadwell # pos:inicio
-> DONE

=== j13_arrepentimiento ===
PENSAMIENTO: Amanecer. Salgo de la despensa sin hacer ruido. Dot duerme en una silla, junto a la estufa. # fx:aclarar # id:j13_00a_pens_00
PENSAMIENTO: Los dibujos de Amory. El mensaje de Nell. La colección de Sammy. # esperar:1 # id:j13_00a_pens_01
PENSAMIENTO: Dejo el paquete sobre la mesa. Abro la puerta. Camino hacia la calle Cable. # id:j13_00a_pens_02
~ inventario -= dibujos_amory
PENSAMIENTO: Un día, dijo Crane. # esperar:1 # id:j13_00a_pens_03
PENSAMIENTO: Quiero que me devuelvan mi cansancio. Quiero que todo vuelva a estar en su sitio. # id:j13_00a_pens_04
~ fb_variante = "arrepentimiento"
-> final_b_arrepentimiento

// ==================================================================== J13.01 — Estación de Shadwell · Amanecer
=== shadwell ===

= entrar
{ shadwell_visto:
    -> DONE
}
~ shadwell_visto = true
PENSAMIENTO: La boca de metro, tapiada con tablones. Niebla del río. # fx:aclarar # id:j13_01_pens_00
PENSAMIENTO: Dot me acompaña hasta la esquina. No nos despedimos. Me aprieta el brazo una vez y se va. # id:j13_01_pens_01
{ crane_sigue:
    PENSAMIENTO: Al final de la calle, junto a una farola apagada, un sombrero. No se mueve. # id:j13_01_crane_01
    PENSAMIENTO: Sigue ahí. Toda la noche. Si entro, me seguirá. Si no entro… # id:j13_01_crane_02
}
-> DONE

= cartel_mirar
PENSAMIENTO: «Cerrado por reformas. Ministerio de la Abundancia.» Nunca reforman nada. # id:j13_01_cartel
-> DONE

= pintada_mirar
PENSAMIENTO: «¡MUERTE A ESTASIA!» Debajo, tachado: EURASIA. Los Espías corrigen deprisa. # id:j13_01_pintada
-> DONE

= crane_mirar
PENSAMIENTO: El sombrero. Ni se esconde. # id:j13_01_crane_mirar
-> DONE

= tablones_mirar
PENSAMIENTO: Clavos nuevos. Pero el tercer tablón… # id:j13_01_tablones_01
{ inventario ? dibujos_amory:
    PENSAMIENTO: En el dibujo de Amory, un pájaro diminuto posado justo en esta esquina de la entrada. El pájaro está aquí. # id:j13_01_tablones_02
}
-> DONE

= tablones
{ tablon_abierto:
    -> bajar
}
~ tablon_abierto = true
PENSAMIENTO: El tercer tablón gira sobre un solo clavo. Hueco suficiente para pasar. # sfx:chirrido # id:j13_01_tablon
PENSAMIENTO: Antes de bajar, extiendo los dibujos de Amory sobre las rodillas. # id:j13_02_mapa_00
PENSAMIENTO: «Usa lo que sabes.» # minijuego:tuneles,vars=mapa # id:j13_02_mapa_01
~ san_clemente_deducido = true
PENSAMIENTO: El único sitio de Londres donde no cae nunca un cohete. # esperar:1 # id:j13_02_mapa_02
PENSAMIENTO: Escondido a la sombra del Miniver. El viejo vive en el único lugar que el Partido protege. # id:j13_02_mapa_03
{ duda >= 50:
    PENSAMIENTO: ¿O es que el Partido le protege a él? # esperar:1 # id:j13_02_mapa_d2
}
-> bajar

= bajar
PENSAMIENTO: Me cuelo por el hueco. Abajo, oscuridad. # fx:negro # id:j13_02_bajar # escena:tunel1 # pos:inicio
-> DONE

// ==================================================================== J13.02 — Tramo 1 · Shadwell → Aldgate Este · El cohete
=== tunel1 ===

= entrar
{ tunel1_visto:
    -> DONE
}
~ tunel1_visto = true
PENSAMIENTO: Oscuridad casi total. Agua por los tobillos. Un goteo constante. # fx:aclarar # sfx:goteo # id:j13_02_t1_00
PENSAMIENTO: La linterna de dinamo de Dot. Si no le doy a la manivela, se apaga. # id:j13_02_t1_01
PENSAMIENTO: Aquí abajo no hay telepantallas. Por primera vez en mi vida, nadie me mira. # id:j13_02_t1_02
{ reloj_en_marcha:
    PENSAMIENTO: El reloj de Ivy anda. Las cinco y nueve. # esperar:0.8 # id:j13_02_t1_reloj_01
    PENSAMIENTO: El patrón de la semana: Whitechapel, a las cinco y diez. Y otro a las cinco y dieciocho. Lo sé. # id:j13_02_t1_reloj_02
}
-> DONE

= silbido
{ silbido1 and silbido2:
    -> DONE
}
{ not silbido1:
    ~ silbido1 = true
- else:
    ~ silbido2 = true
}
{ reloj_en_marcha:
    PENSAMIENTO: El reloj de Ivy. Ya casi. Un silbido, arriba. # sfx:silbido # reloj:inicio=05:09:55,limite=5,agotar=tunel1.impacto # id:j13_02_t1_silbido_reloj
    PENSAMIENTO: Un nicho. La franja blanca. # id:j13_02_t1_nicho_reloj
- else:
    PENSAMIENTO: Un silbido. Arriba. Cada vez más agudo. # sfx:silbido # reloj:inicio=05:09:57,limite=3,agotar=tunel1.impacto,oculto=si # id:j13_02_t1_silbido
    PENSAMIENTO: Un nicho. ¡Un nicho! # id:j13_02_t1_nicho
}
-> DONE

= impacto
PENSAMIENTO: El túnel tiembla. # fx:temblor # sfx:impacto # reloj:parar # id:j13_02_t1_impacto
{ escondido:
    ~ impactos_esquivados += 1
    PENSAMIENTO: Cae polvo y cascotes donde estaba hace un momento. # id:j13_02_t1_polvo
    { impactos_esquivados == 1:
        PENSAMIENTO: Arriba. Están bombardeando arriba. Whitechapel, la cuadrícula I-7. # id:j13_02_t1_arriba_01
        PENSAMIENTO: Lo habría registrado yo mañana por la mañana. # id:j13_02_t1_arriba_02
    - else:
        PENSAMIENTO: Ahí arriba alguien acaba de perder la casa. Mañana yo habría escrito «estasiático» en el libro. # id:j13_02_t1_segundo
    }
    -> DONE
}
PENSAMIENTO: Blanco. # fx:blanco # id:j13_02_t1_blanco
~ silbido1 = false
~ silbido2 = false
~ impactos_esquivados = 0
PENSAMIENTO: Otra vez. Desde el principio. # fx:aclarar # pos:inicio # id:j13_02_t1_otra
-> DONE

= nicho_mirar
PENSAMIENTO: Un nicho de seguridad. Una franja blanca descolorida alrededor. # id:j13_02_t1_nicho_mirar
-> DONE

= salir
{ impactos_esquivados < 2:
    PENSAMIENTO: El agua sigue. El túnel sigue. # id:j13_02_t1_sigue
    -> DONE
}
PENSAMIENTO: Aldgate Este. Una estación tapiada. # fx:negro # id:j13_02_t1_salir # escena:anden_taller # pos:entrada
-> DONE

// ==================================================================== Tramo 2 · Aldgate → Liverpool Street · El taller
=== taller ===

= entrar
{ taller_visto:
    -> DONE
}
~ taller_visto = true
PENSAMIENTO: Un andén. Velas consumidas. Una mesa de trabajo. Y telepantallas. Muchas. Muertas. # fx:aclarar # id:j13_02_t2_00
-> DONE

= teles_mirar
PENSAMIENTO: Una docena de telepantallas desmontadas, con los cables al aire. Etiquetas escritas a mano. # id:j13_02_t2_teles_01
PENSAMIENTO: «Minimor, pasillo 9.» «Bloque 4, Southwark.» «Minipax, planta 14, suministros.» # esperar:1 # id:j13_02_t2_teles_02
PENSAMIENTO: El cuarto de suministros. El hueco tapado con una tabla. # esperar:1 # id:j13_02_t2_teles_03
PENSAMIENTO: No la quitaron ellos. La quitamos nosotros. # id:j13_02_t2_teles_04
~ taller_teles = true
-> DONE

= mesa_mirar
PENSAMIENTO: Un mono de trabajo con un distintivo: «Servicio técnico de telepantallas · Ministerio de la Verdad». # id:j13_02_t2_mesa_01
PENSAMIENTO: En el bolsillo, una tarjeta: «T. Barlow». # id:j13_02_t2_mesa_02
PENSAMIENTO: El tabernero. Entraba en los ministerios a «reparar» telepantallas. Y las arreglaba para que no vieran. # esperar:1 # id:j13_02_t2_mesa_03
PENSAMIENTO: Barlow está en el Minimor. # id:j13_02_t2_mesa_04
~ taller_mesa = true
-> DONE

= pared_mirar
PENSAMIENTO: Escritos con tiza, con letras de distintas manos, decenas de nombres. Algunos tachados. # id:j13_02_t2_pared_01
PENSAMIENTO: Entre ellos: Ivy. Y debajo, con otra letra: «Felix A. (sin saberlo)». # esperar:1.4 # id:j13_02_t2_pared_02
PENSAMIENTO: Ivy. Escrito con tiza, en un andén donde no pasa ningún tren. # esperar:1 # id:j13_02_t2_pared_03
PENSAMIENTO: Es más que un cartel. # id:j13_02_t2_pared_04
{ not taller_pared:
    ~ taller_pared = true
    ~ sube_duda(5)
}
-> DONE

= salir
{ crane_sigue and not crane_perdido:
    PENSAMIENTO: Liverpool Street. # fx:negro # id:j13_02_t2_salir_crane # escena:tunel3 # pos:inicio
- else:
    PENSAMIENTO: Liverpool Street. Bank. Sigo. # fx:negro # id:j13_02_t2_salir # escena:tunel4 # pos:inicio
}
-> DONE

// ==================================================================== Tramo 3 · Liverpool Street → Bank · Crane
=== tunel3 ===

= entrar
{ tunel3_visto:
    -> DONE
}
~ tunel3_visto = true
PENSAMIENTO: Detrás, a lo lejos, el chapoteo de unos pasos en el agua. Una luz que no es la mía. # fx:aclarar # sfx:chapoteo # id:j13_02_t3_00
PENSAMIENTO: Me ha seguido. Está aquí abajo. # id:j13_02_t3_01
PENSAMIENTO: Sigue a mi luz. No corre. Camina. # id:j13_02_t3_02
-> DONE

= crane_mirar
PENSAMIENTO: Crane. Empapado hasta las rodillas. Camina sin prisa, como quien pasea. # id:j13_02_t3_crane_mirar
-> DONE

= derrumbe_mirar
PENSAMIENTO: Un derrumbe. Abajo queda un hueco estrecho. En el dibujo de Amory, un pájaro con las alas cerradas. # id:j13_02_t3_derrumbe
-> DONE

= puntal_mirar
PENSAMIENTO: Un puntal de madera podrida. Sostiene lo que queda del techo. # id:j13_02_t3_puntal_mirar
-> DONE

= puntal
{ crane_perdido:
    PENSAMIENTO: Ya no hay nada que tirar. # id:j13_02_t3_puntal_ya
    -> DONE
}
~ crane_perdido = true
PENSAMIENTO: Le doy una patada al puntal. Otra. Cruje. # sfx:golpes # id:j13_02_t3_puntal_01
PENSAMIENTO: El techo cede detrás de mí. # fx:temblor # sfx:impacto # refrescar # id:j13_02_t3_puntal_02
PENSAMIENTO: Al otro lado, alguien tose. # sfx:tos # esperar:1 # id:j13_02_t3_puntal_03
CRANE: Hay más túneles, camarada. Siempre hay más túneles. # id:j13_02_t3_crane_01
-> DONE

= salir
{ not crane_perdido and crane_distancia > 140:
    ~ crane_perdido = true
    PENSAMIENTO: Ya no oigo sus pasos. En la oscuridad, me ha perdido. # id:j13_02_t3_perdido
}
{ not crane_perdido:
    PENSAMIENTO: Sigue ahí. Detrás. # id:j13_02_t3_sigue
}
PENSAMIENTO: Bank. # fx:negro # id:j13_02_t3_salir # escena:tunel4 # pos:inicio
-> DONE

// ==================================================================== Tramo 4 · Bank → Temple · Los nombres
=== tunel4 ===

= entrar
{ tunel4_visto:
    -> DONE
}
~ tunel4_visto = true
PENSAMIENTO: Un túnel largo y seco. En las paredes, carteles de antes de la Revolución, medio despegados. # fx:aclarar # id:j13_02_t4_00
-> DONE

= nina_mirar
PENSAMIENTO: Una niña sonriendo. Con los dientes. # esperar:1 # id:j13_02_t4_nina_01
PENSAMIENTO: Ivy sonreía así. # esperar:1 # id:j13_02_t4_nina_02
PENSAMIENTO: Antes, alguien hacía carteles de gente sonriendo sin motivo. # id:j13_02_t4_nina_03
-> DONE

= plano_mirar
PENSAMIENTO: Cientos de estaciones. Toda una ciudad debajo de la ciudad. Y nadie la recuerda. # esperar:1 # id:j13_02_t4_plano_01
PENSAMIENTO: Amory la recordaba. La dibujó entera para que alguien la recordara. # id:j13_02_t4_plano_02
-> DONE

= carteles_mirar
PENSAMIENTO: Un té. Un teatro. Una playa. Cosas que no reconozco. # id:j13_02_t4_carteles
-> DONE

= salir
PENSAMIENTO: Temple. Una escalera de caracol de hierro sube desde un pozo de ventilación. # fx:negro # id:j13_02_t5_00
PENSAMIENTO: Al subir, oigo algo que nunca he oído: el silencio de un lugar cerrado y antiguo. # id:j13_02_t5_01
PENSAMIENTO: Y, muy débil, alguien que teclea en una máquina de escribir. # sfx:tecla # id:j13_02_t5_02
PENSAMIENTO: Naranjas y limones, dicen las campanas de San Clemente. # id:j13_02_t5_03
VOZ: …me debes tres peniques, dicen las campanas de San Martín. # sfx:tos # id:j13_02_t5_voz_01
VOZ: Sube. Llevo dos días con el té preparado. Ya estará frío. # id:j13_02_t5_voz_02 # escena:cripta # pos:escalera
-> DONE

// ==================================================================== J13.03 — La cripta de San Clemente
=== cripta ===

= entrar
{ final_en_curso == "E":
    -> DONE
}
{ cripta_vista:
    -> DONE
}
~ cripta_vista = true
~ crane_en_cripta = false
PENSAMIENTO: Una cripta bajo una iglesia en ruinas. Velas por todas partes. Libros. Libros de verdad. # fx:aclarar # id:j13_03_pens_00
PENSAMIENTO: Junto a una máquina de escribir, un anciano muy delgado, con una manta sobre los hombros. Pelo blanco y largo. Gafas remendadas con hilo. # id:j13_03_pens_01
PENSAMIENTO: La cara de los Dos Minutos de Odio. Treinta años más vieja. Más pequeña. # id:j13_03_pens_02
PENSAMIENTO: Mi cara se crispa sola. El puño se cierra. # fx:temblor # sfx:grieta # id:j13_03_cf_00
PENSAMIENTO: Mi cara le odia sola. Cinco años de entrenamiento. # esperar:1 # id:j13_03_cf_01
PENSAMIENTO: Es un viejo con una manta. # id:j13_03_cf_02
GOLDSTEIN: Lo sé. A todos os pasa. # id:j13_03_gold_01
PENSAMIENTO: Sirve té en dos tazas desportilladas. Sonríe. # id:j13_03_pens_03
GOLDSTEIN: La primera vez que alguien de la Hermandad me trajo un espejo, a mí también me pasó. # id:j13_03_gold_02
{ crane_sigue and not crane_perdido:
    PROTAGONISTA: Me han seguido. Un hombre. Crane. Debe de estar cerca. # id:j13_03_prot_crane
    GOLDSTEIN: Lo sé. Siempre viene alguien detrás. Siéntate. Tenemos un rato. # id:j13_03_gold_crane
}
-> conversacion

= goldstein_mirar
PENSAMIENTO: Emmanuel Goldstein. Un viejo con una manta. # id:j13_03_gold_mirar
-> DONE

= telefono_mirar
PENSAMIENTO: Un teléfono de campaña del Partido. Verde. Polvoriento. # id:j13_03_telefono
-> DONE

= campanas_mirar
PENSAMIENTO: Una estructura de madera para campanas. Vacía. Un solo gancho de hierro. # id:j13_03_campanas
-> DONE

= libros_mirar
PENSAMIENTO: Libros de verdad. Viejos. Prohibidos. Huelen a humedad y a vela. # id:j13_03_libros
-> DONE

// J13.04 — La conversación: los temas se desbloquean según lo que se sabe
= conversacion
* [«¿Usted existe de verdad?»]
    GOLDSTEIN: Eso me pregunto yo cada mañana. # sfx:tos # id:j13_04_existe_01
    GOLDSTEIN: Existo lo bastante para toser. Para escribir. Para que me odien dos minutos al día en todos los ministerios de Oceanía. # esperar:0.8 # id:j13_04_existe_02
    GOLDSTEIN: No sé si existo lo bastante para importar. # id:j13_04_existe_03
    -> conversacion
* {planilla_vista} [«He visto la Planilla Azul.»]
    PROTAGONISTA: He visto la Planilla Azul. Folkestone. Kent. # id:j13_04_guerra_01
    GOLDSTEIN: Entonces ya sabes más de lo que sabía yo cuando escribí el capítulo tercero. # id:j13_04_guerra_02
    GOLDSTEIN: Yo intuía que la guerra era un teatro. No sabía que el Partido había empezado a poner las bombas en el patio de butacas. # id:j13_04_guerra_03
    PROTAGONISTA: ¿Y Eurasia? ¿Y Estasia? # id:j13_04_guerra_04
    GOLDSTEIN: Existen. Tienen sus propios partidos, sus propios Grandes Hermanos con otras caras. Sus propios mercados bombardeados, supongo. # id:j13_04_guerra_05
    GOLDSTEIN: Los tres se necesitan como se necesitan las piedras de una bóveda. Si una cae, caen todas. # id:j13_04_guerra_06
    -> conversacion
* {ivy_revelada} [«Mi hermana. Ivy.»]
    -> ivy
* [«Los proles.»]
    GOLDSTEIN: Escribí que la esperanza está en los proles. Lo sigo creyendo. Pero no como lo escribí. # id:j13_04_proles_01
    GOLDSTEIN: Creía que un día se despertarían todos a la vez, como un gigante. No será así. # id:j13_04_proles_02
    GOLDSTEIN: Será una mujer que esconde a alguien en una despensa. Un niño que guarda metralla. Un tabernero que arregla telepantallas para que no vean. # id:j13_04_proles_03
    GOLDSTEIN: Mil puertas que se abren, una a una. Es más lento. Es lo único que el Partido no sabe vigilar. # id:j13_04_proles_04
    { dot_confianza >= 2:
        GOLDSTEIN: Tú ya lo has visto. Te han abierto puertas. # id:j13_04_proles_05
    }
    -> conversacion
* [«¿Cuántos somos?»]
    GOLDSTEIN: No lo sé. De verdad que no lo sé. Puede que mil. Puede que treinta. # id:j13_04_hermandad_01
    GOLDSTEIN: Puede que la Hermandad sea, sobre todo, la idea de que existe. Eso también es útil. Para nosotros. Y para ellos. # id:j13_04_hermandad_02
    -> conversacion
* {inventario ? dibujos_amory} [«Felix Amory. Los pájaros.»]
    GOLDSTEIN: El de los pájaros. # id:j13_04_amory_01
    GOLDSTEIN: Nell me trajo copias. Ese muchacho dibujó la red entera, estación por estación, de memoria y por intuición. Nunca supo que dibujaba para nosotros. # id:j13_04_amory_02
    GOLDSTEIN: Dibujaba porque no soportaba que algo existiera y nadie lo supiera. Esa es, al final, la única rebeldía. # id:j13_04_amory_03
    { amory_reaccion == "denuncia":
        PROTAGONISTA: Yo le denuncié. # id:j13_04_amory_04
        GOLDSTEIN: Lo sé. Nell me lo dijo. # esperar:1 # id:j13_04_amory_05
        GOLDSTEIN: Y aquí estás, con sus dibujos en la mano. No sé qué significa eso. Pero significa algo. # id:j13_04_amory_06
    }
    -> conversacion
* [«¿Por qué sigue vivo?»]
    PROTAGONISTA: Está a la sombra del Miniver. En el único sitio donde no cae ningún cohete. ¿De verdad no saben que está aquí? # id:j13_04_jaula_01
    PENSAMIENTO: Tarda mucho en contestar. Mira la estructura vacía de las campanas. # esperar:1.2 # id:j13_04_jaula_02
    GOLDSTEIN: Me lo pregunto cada noche. # id:j13_04_jaula_03
    GOLDSTEIN: Hay dos respuestas. O soy más listo que el Partido, cosa que dudo. O el Partido necesita que yo exista, y que escriba, y que tosa, y que de vez en cuando alguien como tú baje por esa escalera. # id:j13_04_jaula_04
    GOLDSTEIN: No sé cuál es peor. # id:j13_04_jaula_05
    PROTAGONISTA: ¿Y qué hace con eso? # id:j13_04_jaula_06
    GOLDSTEIN: Escribir. Igual. Si es una jaula, es la única jaula de Oceanía donde se puede escribir la verdad. Prefiero esta. # id:j13_04_jaula_07
    ~ pregunta_jaula = true
    -> conversacion
* [«Las campanas.»]
    GOLDSTEIN: Barlow se llevó la última para que no la fundieran. La tiene colgada en su bar. Así la oyen los proles cada noche. # id:j13_04_campana_01
    -> conversacion
+ [«El capítulo.»]
    -> j13_capitulo

= ivy
PROTAGONISTA: Mi hermana. Ivy {apellido}. Era de la Hermandad. # id:j13_04_ivy_01
PENSAMIENTO: Deja la taza. Se quita las gafas. Tarda en hablar. # esperar:1 # id:j13_04_ivy_02
GOLDSTEIN: La recuerdo. Nunca la vi, pero la recuerdo. Nell me traía sus cartas. Escribía muy deprisa, con faltas de ortografía. Siempre con prisa. # id:j13_04_ivy_03
GOLDSTEIN: Estaba escribiendo algo para mí. Para el libro. # id:j13_04_ivy_04
PROTAGONISTA: ¿Qué? # id:j13_04_ivy_05
GOLDSTEIN: El capítulo que yo no sé escribir. # esperar:1.4 # id:j13_04_ivy_06
PROTAGONISTA: Los documentos. La Policía del Pensamiento se llevó documentos de casa aquella noche. # id:j13_04_ivy_07
GOLDSTEIN: Tres páginas. Me había mandado la primera frase en una carta, la semana anterior. Para ver si me gustaba. # id:j13_04_ivy_08
PENSAMIENTO: Busca entre sus papeles con manos temblorosas. Un trozo de papel cuadriculado, arrancado de un cuaderno escolar, doblado muchas veces. # id:j13_04_ivy_09
GOLDSTEIN: Me gustó. # id:j13_04_ivy_10
~ carta_ivy = true
~ inventario += carta
PENSAMIENTO: Su letra. # documento:carta_ivy # objeto:carta # id:j13_04_ivy_11
PENSAMIENTO: «Dificil» sin tilde. Siempre se le olvidaba. # esperar:1.6 # id:j13_04_ivy_12
PENSAMIENTO: Ivy. # id:j13_04_ivy_13
~ sube_duda(10)
{ dp_j11_ivy == "aceptar":
    PENSAMIENTO: Traidora. # fx:temblor # sfx:pitido # id:j13_04_roto_01
    PENSAMIENTO: Su letra. # esperar:1 # id:j13_04_roto_02
    PENSAMIENTO: No puedo. No puedo sostener las dos cosas. # id:j13_04_roto_03
    ~ dp_j11_ivy = "roto"
}
-> conversacion

// ==================================================================== J13.05 — El Capítulo II
=== j13_capitulo ===
PENSAMIENTO: Pone una mano sobre el fajo de papeles mecanografiados. # id:j13_05_pens_00
GOLDSTEIN: Teoría y práctica del colectivismo oligárquico. Capítulo primero: la ignorancia es la fuerza. Capítulo tercero: la guerra es la paz. # id:j13_05_gold_01
GOLDSTEIN: Y en medio, nada. Treinta años sin el capítulo segundo. # id:j13_05_gold_02
PROTAGONISTA: La libertad es la esclavitud. # id:j13_05_prot_01
GOLDSTEIN: Lo he intentado cien veces. Siempre me sale un tratado. Explico por qué el individuo solo es débil y el Partido es inmortal, por qué rendirse al Partido parece una forma de no morir… y es mentira, porque nunca lo he sentido. # id:j13_05_gold_03
GOLDSTEIN: Yo nunca creí. Nunca grité en los Dos Minutos de verdad. Nunca lloré delante de un cartel. # esperar:1 # id:j13_05_gold_04
PENSAMIENTO: Me mira. # id:j13_05_pens_01
GOLDSTEIN: Tú sí. # esperar:1 # id:j13_05_gold_05
GOLDSTEIN: Solo quien ha creído puede explicar qué se entrega al creer. Y por qué cuesta tanto devolverlo. # id:j13_05_gold_06
{ carta_ivy:
    GOLDSTEIN: Tu hermana empezó. Termínalo tú. # id:j13_05_gold_07
}
{ inventario ? diario:
    GOLDSTEIN: Nell me dijo que escribías. Empieza por ahí. # id:j13_05_gold_08
- else:
    GOLDSTEIN: Nell me dijo que escribías. Lo que no esté escrito, lo pondré yo. # id:j13_05_gold_08b
}
{ inventario ? lapiz_amory and not lapiz_destruido:
    PENSAMIENTO: Saco el lápiz mordido. # id:j13_05_lapiz_01
    GOLDSTEIN: Ese lápiz ha sufrido. # id:j13_05_lapiz_02
    PROTAGONISTA: Era de un amigo. # id:j13_05_lapiz_03
- else:
    GOLDSTEIN: Toma. Los lápices aquí abajo no son de nadie. # id:j13_05_lapiz_04
}
PENSAMIENTO: Goldstein mete una hoja en la máquina. # minijuego:capitulo,vars=cap # id:j13_05_pens_02
~ capitulo_escrito = true
~ libro_fragmentos = 5
PENSAMIENTO: Termina de teclear. Saca la hoja. Cose las páginas del capítulo con hilo, en medio del fajo, entre el primero y el tercero. # id:j13_05_pens_03
PENSAMIENTO: Se queda mirando el libro entero en sus manos. # esperar:1 # id:j13_05_pens_04
GOLDSTEIN: Treinta años. # esperar:1 # id:j13_05_gold_09
GOLDSTEIN: Ahora está entero. # esperar:1 # id:j13_05_gold_10
GOLDSTEIN: Y ahora es peligroso de verdad. # id:j13_05_gold_11
-> j13_copias

// ==================================================================== J13.06 — Copias
=== j13_copias ===
GOLDSTEIN: Hay dos copias. Siempre hago dos. Una se queda aquí, conmigo. La otra tiene que salir. # id:j13_06_gold_01
PROTAGONISTA: ¿Adónde? # id:j13_06_prot_01
GOLDSTEIN: Adonde no la busquen. A una cocina. A una despensa. A los de abajo. # id:j13_06_gold_02
PENSAMIENTO: Pone la copia sobre la mesa, entre los dos. # id:j13_06_pens_00
GOLDSTEIN: Si sales con ella, te cogerán. No hoy, quizá. Pero te cogerán. Tu cara está en el expediente de Voss desde hace cinco años. # id:j13_06_gold_03
GOLDSTEIN: Si te quedas, puedes quedarte. Hay sitio. Hay libros. Hay té, aunque siempre está frío. # id:j13_06_gold_04
GOLDSTEIN: Y nadie te buscará aquí. Nunca buscan aquí. # id:j13_06_gold_05
PENSAMIENTO: «Nunca buscan aquí.» # id:j13_06_pens_01
{ crane_sigue and not crane_perdido:
    -> j13_crane
}
-> j13_final

// ==================================================================== J13.07 — Crane en la cripta
=== j13_crane ===
~ crane_en_cripta = true
PENSAMIENTO: Pasos en la escalera de caracol. Lentos. # sfx:golpes # id:j13_07_pens_00
PENSAMIENTO: Crane. Empapado hasta las rodillas, con el sombrero en una mano y una pistola en la otra. Sonríe. # refrescar # id:j13_07_pens_01
CRANE: Qué sitio tan… acogedor. Cuánto papel. # id:j13_07_crane_01
CRANE: Y usted debe de ser el viejo. Le hacía más alto. En las pantallas parece más alto. # id:j13_07_crane_02
GOLDSTEIN: Todos me dicen lo mismo. # id:j13_07_gold_01
CRANE: Queda usted detenido. Los dos. # id:j13_07_crane_03
GOLDSTEIN: Antes de hacer nada, hijo, pregunte a sus superiores. # id:j13_07_gold_02
PENSAMIENTO: Señala con la taza un rincón: un teléfono de campaña del Partido, verde y polvoriento, con un cable que sube por la pared. # id:j13_07_pens_02
GOLDSTEIN: Esa línea funciona. Siempre ha funcionado. Nunca la he usado. # id:j13_07_gold_03
PENSAMIENTO: Crane duda por primera vez. Sin dejar de apuntar, va hasta el teléfono. Descuelga. Marca. # id:j13_07_pens_03
CRANE: Aquí Crane, distrito Este. Estoy en… San Clemente. Tengo al viejo. # esperar:1.5 # id:j13_07_crane_04
CRANE: …Sí. # esperar:1 # id:j13_07_crane_05
CRANE: Sí, señor. # esperar:1 # id:j13_07_crane_06
CRANE: Pero… # esperar:1.2 # id:j13_07_crane_07
CRANE: Entendido, señor. # id:j13_07_crane_08
PENSAMIENTO: Cuelga despacio. Se le ha borrado la sonrisa. Por primera vez parece lo que es: un funcionario. # id:j13_07_pens_04
CRANE: Usted no está aquí. Usted nunca ha estado aquí. # esperar:1 # id:j13_07_crane_09
CRANE: Usted sí. # id:j13_07_crane_10
~ crane_humillado = true
PENSAMIENTO: «Pregunte a sus superiores.» Lo sabían. Siempre lo han sabido. # id:j13_07_pens_05
GOLDSTEIN: Ahora ya sabes cuál de las dos respuestas era. # esperar:1 # id:j13_07_gold_04
GOLDSTEIN: No cambia nada. El libro sigue siendo verdad. # id:j13_07_gold_05
-> j13_final

// ==================================================================== J13.08 — La decisión final
=== j13_final ===
PENSAMIENTO: Goldstein empuja la segunda copia hacia mí. La vela parpadea. # id:j13_08_pens_00
PENSAMIENTO: Arriba, muy lejos, un silbido de cohete que no cae aquí. Nunca cae aquí. # sfx:silbido # id:j13_08_pens_01
{ crane_humillado:
    -> con_crane
}
* [Sacar el libro. «Se lo llevaré a los de abajo.»] # decision:D-J13-FINAL
    PENSAMIENTO: Cojo la copia. La meto bajo el mono, contra el pecho. # id:j13_08_sacar
    -> final_d
* [Quedarse. «¿Queda té?»]
    -> final_e
* {crane_decision == "fingir"} [Entregar a Goldstein.]
    PENSAMIENTO: Me levanto. Subo la escalera. # id:j13_08_entregar
    ~ fb_variante = "san_clemente"
    -> final_b_san_clemente

= con_crane
* [Sacar el libro escondido, delante de Crane.] # decision:D-J13-FINAL
    PENSAMIENTO: Meto la copia bajo el mono. Crane me mira. # id:j13_08_c_sacar_00
    PENSAMIENTO: La cara. Que no se note nada. # cf:id=CF-J13-SACAR,expr=neutral,dif=dificil,golpes=12 # id:j13_08_c_sacar_01
    { cf_j13_sacar == "fallo":
        CRANE: Un momento. # id:j13_08_c_fallo_01
        PENSAMIENTO: Me registra. Encuentra la copia. La sostiene sobre una vela hasta que prende. # id:j13_08_c_fallo_02
        ~ fc_variante = "sin_libro"
        -> final_c_cripta
    }
    CRANE: Ya le registrarán en el Minimor. # id:j13_08_c_ok
    -> final_d
* [Dejar el libro. «Guárdelo usted.»]
    PENSAMIENTO: Dejo la copia sobre la mesa. Miro a Goldstein. # id:j13_08_c_dejar
    ~ fc_variante = "libro_vive"
    -> final_c_cripta
* [Pedir quedarse.]
    PROTAGONISTA: Déjeme aquí. Usted no tiene órdenes sobre mí en este sitio. # id:j13_08_c_quedarse_01
    CRANE: Sobre usted tengo todas las órdenes del mundo. # id:j13_08_c_quedarse_02
    ~ fc_variante = "cripta"
    -> final_c_cripta

