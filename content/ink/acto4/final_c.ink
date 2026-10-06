// FINAL C — «Habitación 101» (guion: docs/guion-detallado/05-finales.md)
// Variantes de entrada: C-sospecha (arresto, ver acto3/arresto.ink), C-cripta, C-sin libro, C-el libro vive.
// La celda, O'Brien, «¿Qué hora marca?», la Habitación 101, la declaración y el Café del Castaño.
// El Final D pasa por los mismos escenarios en versión abreviada (ver final_d.ink).

// FC.01 — En la cripta, con Crane
=== final_c_cripta ===
PENSAMIENTO: Crane me pone las esposas despacio. Con cuidado. Casi con ternura. # id:fcc_00_pens_00
CRANE: Ya se lo dije. Sobre usted tengo todas las órdenes del mundo. # id:fcc_00_crane_01
PENSAMIENTO: Goldstein no levanta la vista de la máquina de escribir. # esperar:1 # id:fcc_00_pens_01
PENSAMIENTO: Negro. # fx:negro # id:fcc_00_negro
-> final_c.llegada

=== final_c ===

= llegada
{ final_en_curso == "":
    ~ final_en_curso = "C"
}
~ prota_preso = true
PENSAMIENTO: El sonido de una furgoneta. Una puerta metálica. # sfx:sello # esperar:1.5 # id:fc_01_puerta
CARTEL: ? # id:fc_02_cartel # escena:celda # pos:banco
-> DONE

// ==================================================================== FC.02 — La celda
=== celda ===

= entrar
{ final_en_curso == "D":
    -> fd_celda
}
{ celda_vista:
    -> DONE
}
~ celda_vista = true
PENSAMIENTO: Una celda blanca. Sin ventanas. Una telepantalla en cada pared. Una luz blanca que no se apaga nunca. # fx:aclarar # id:fc_02_pens_00
PENSAMIENTO: Huele a orina y a desinfectante. En el banco, otros presos. Reconozco a dos. # id:fc_02_pens_01
PARSONS: ¡Camarada {apellido}! ¡Usted también! # id:fc_02_parsons_01
PENSAMIENTO: Se ríe, histérico. # id:fc_02_pens_02
PARSONS: ¡Mi hija! ¿Se lo he contado? ¡Me denunció mi hija! # id:fc_02_parsons_02
PARSONS: Estoy orgulloso de ella. Estoy tan orgulloso… # id:fc_02_parsons_03
-> DONE

= winston_mirar
PENSAMIENTO: Smith. Muy delgado, la cara amarilla, dos dientes menos. Mira la pared. # id:fc_02_winston_mirar
-> DONE

= winston
{ final_en_curso == "D":
    -> fd_winston
}
PROTAGONISTA: Camarada Smith. # id:fc_02_prot_01
PENSAMIENTO: Tarda en enfocarme. # id:fc_02_pens_03
WINSTON: …El del cuarto. Siempre puntual. # esperar:0.8 # id:fc_02_winston_01
WINSTON: ¿Por qué está aquí? # id:fc_02_winston_02
PROTAGONISTA: Porque recordé. # id:fc_02_prot_02
WINSTON: Yo también. # esperar:0.8 # id:fc_02_winston_03
WINSTON: Aquí te enseñan a dejar de hacerlo. # esperar:0.8 # id:fc_02_winston_04
WINSTON: ¿Le han llevado ya a la ciento uno? # id:fc_02_winston_05
PROTAGONISTA: ¿Qué es la ciento uno? # id:fc_02_prot_03
PENSAMIENTO: Me mira con algo parecido a la lástima. Vuelve la vista a la pared. # id:fc_02_pens_04
WINSTON: Ya lo sabrá. Todo el mundo lo sabe al final. # id:fc_02_winston_06
TELEPANTALLA: ¡Smith! ¡6079 Smith W.! ¡Las manos fuera de los bolsillos! ¡En la celda no se habla! # id:fc_02_tp_01
-> DONE

= parsons_mirar
PENSAMIENTO: Parsons, sin cinturón, temblando. # id:fc_02_parsons_mirar
-> DONE

= esqueleto_mirar
PENSAMIENTO: Un hombre esquelético, con la cara como una calavera. No aparta los ojos de la puerta. # id:fc_02_esqueleto
-> DONE

= puerta_mirar
PENSAMIENTO: Acero. Ni picaporte. # id:fc_02_puerta
-> DONE

= tele_mirar
PENSAMIENTO: Cuatro telepantallas. No hay ningún ángulo muerto. # id:fc_02_tele
-> DONE

= cubo_mirar
PENSAMIENTO: Un cubo. # id:fc_02_cubo
-> DONE

// El tiempo pasa: cada vez que el protagonista se sienta a esperar, ocurre algo
= esperar
{ final_en_curso == "D":
    PENSAMIENTO: Espero. # id:fd_04_esperar
    -> DONE
}
~ celda_evento += 1
{ celda_evento:
- 1:
    PENSAMIENTO: Me siento en el banco de acero. No sé cuánto tiempo pasa. # id:fc_02_e1_00
    PENSAMIENTO: Entra un guardia y se lleva a Parsons. # sfx:sello # refrescar # id:fc_02_e1_01
    PARSONS: ¡Gracias! ¡Gracias! # id:fc_02_e1_parsons
- 2:
    -> pan
- 3:
    -> paliza
- 4:
    PENSAMIENTO: Dos veces más. El pasillo, las botas. Pierdo la cuenta. # vineta:vineta-pasillo_suelo # sfx:golpes # fx:temblor # id:fc_02_e4_00
    PENSAMIENTO: Ya no hay días ni noches. # vineta:fin # id:fc_02_e4_01
    CARTEL: ? # id:fc_02_e4_cartel
    PENSAMIENTO: La puerta se abre. Esta vez me llevan a otra sala. # id:fc_02_e4_02 # escena:sala_obrien # pos:camilla
- else:
    PENSAMIENTO: Espero. # id:fc_02_espero
}
-> DONE

= pan
PENSAMIENTO: El hambre. Un guardia trae un trozo de pan y me lo tira a los pies. # id:fc_02_pan_00
PENSAMIENTO: El hombre de la cara de calavera lo mira. # id:fc_02_pan_01
* [Darle el pan.] # decision:D-FC-PAN
    ~ pan_dado = "dado"
    PENSAMIENTO: Se lo doy. # id:fc_02_pan_dar_01
    PENSAMIENTO: El guardia vuelve. Le golpea en la boca con la porra, delante de todos. Un diente rueda por el suelo blanco. Sangre. # sfx:golpes # fx:temblor # id:fc_02_pan_dar_02
    PENSAMIENTO: Nadie se mueve. # id:fc_02_pan_dar_03
* [Comérmelo.]
    ~ pan_dado = "comido"
    PENSAMIENTO: Me lo como. # id:fc_02_pan_comer_01
    PENSAMIENTO: El hombre llora en silencio. # id:fc_02_pan_comer_02
- -> DONE

= paliza
PENSAMIENTO: Dos guardias me sacan al pasillo. # sfx:sello # id:fc_02_paliza_00
PENSAMIENTO: El linóleo blanco. Las botas. # vineta:vineta-pasillo_suelo # id:fc_02_paliza_01
PENSAMIENTO: Un golpe. # sfx:golpes # fx:temblor # id:fc_02_paliza_02
PENSAMIENTO: Otro. # sfx:golpes # fx:temblor # id:fc_02_paliza_03
PENSAMIENTO: Vuelvo a la celda. No veo por un ojo. # vineta:fin # id:fc_02_paliza_04
-> DONE

// ==================================================================== FC.03 — O'Brien
=== sala_obrien ===

= entrar
{ final_en_curso == "D":
    -> fd_obrien
}
{ obrien_visto:
    -> DONE
}
~ obrien_visto = true
PENSAMIENTO: Una sala blanca. Una camilla de metal con correas. Un dial en la pared, del uno al cien. # fx:aclarar # id:fc_03_pens_00
PENSAMIENTO: Me atan. No puedo mover nada salvo los ojos. # id:fc_03_pens_01
PENSAMIENTO: De pie, junto a la camilla, un hombre corpulento con gafas. El del Gran Salón. # id:fc_03_pens_02
O'BRIEN: Le vi en los Dos Minutos de Odio. En el Miniver. Gritaba usted de verdad. # esperar:1 # id:fc_03_obrien_01
O'BRIEN: Por eso está aquí. Los que gritan de verdad son los que más cuesta curar. Y los que mejor quedan cuando se curan. # id:fc_03_obrien_02
-> j_grabacion -> j_objetos -> j_reloj -> j_goldstein ->
-> habitacion

// FC.03a — La grabación (o el diario)
= j_grabacion
{
- iniciacion_vida != "":
    PENSAMIENTO: Pulsa un botón. Una grabadora de bobinas. La voz de Nell, en el sótano. # sfx:chirrido # id:fc_03a_00
    GRABACIÓN: «¿Estás dispuest{o} a matar? ¿A alguien que no conoces…?» # id:fc_03a_nell_01
    GRABACIÓN: «{iniciacion_matar}.» # id:fc_03a_prot_01
    GRABACIÓN: «¿Estás dispuest{o} a que tu hermana deje de ser una mártir?» # id:fc_03a_nell_02
    GRABACIÓN: «{iniciacion_ivy}.» # id:fc_03a_prot_02
    O'BRIEN: Buena voz. Firme. # esperar:1 # id:fc_03a_obrien_01
    O'BRIEN: La señora Hask, por cierto, no dijo nada. Ni una palabra. Durante once días. # esperar:1 # id:fc_03a_obrien_02
    O'BRIEN: Al duodécimo lo dijo todo. Todos lo dicen todo al duodécimo día. # id:fc_03a_obrien_03
- diario_texto != "":
    PENSAMIENTO: Abre mi cuaderno sobre la mesa. Lee en voz alta, con buena dicción. # id:fc_03a_diario_00
    CARTEL: {diario_texto} # id:fc_03a_diario_texto
    O'BRIEN: Escribe usted bien. Escribía. # id:fc_03a_diario_01
- else:
    O'BRIEN: No hay grabación. No hay cuaderno. No nos hace falta: usted lo lleva todo en la cara. # id:fc_03a_nada
}
->->

// FC.03b — Los objetos de la mesa
= j_objetos
{ inventario ? lapiz_amory and not lapiz_destruido:
    O'BRIEN: «F.A.» # id:fc_03b_lapiz_01
    PENSAMIENTO: Lo hace girar entre los dedos. # id:fc_03b_lapiz_02
    O'BRIEN: Se lo prestó para siempre, sin saberlo. # id:fc_03b_lapiz_03
    PENSAMIENTO: Lo parte por la mitad. # sfx:tecla # id:fc_03b_lapiz_04
}
{ cartel_arrancado:
    PENSAMIENTO: Un cartel enmarcado. Ivy. Perfectamente restaurado, sin una arruga. # id:fc_03b_cartel_01
    O'BRIEN: Lo arrancó usted. Nosotros lo hemos vuelto a poner. Siempre lo volvemos a poner. # id:fc_03b_cartel_02
}
{ inventario ? foto_ivy_restaurada:
    O'BRIEN: El señor Crane hace un trabajo precioso. # esperar:1 # id:fc_03b_foto_01
    O'BRIEN: Le devolvió la cara de su hermana. Ahora se la vamos a quitar. # id:fc_03b_foto_02
}
PENSAMIENTO: Y el reloj de Ivy. # id:fc_03b_reloj
->->

// FC.03c — «¿Qué hora marca?»
= j_reloj
PENSAMIENTO: Lo sostiene delante de mis ojos. Las agujas marcan las nueve y cuarenta. # id:fc_03c_00
{ reloj_en_marcha:
    O'BRIEN: Lo he detenido. Por respeto. # id:fc_03c_detenido
}
O'BRIEN: ¿Qué hora marca este reloj? # minijuego:dial,ronda=1,resultado=dial_respuesta # id:fc_03c_r1
-> respuesta ->
O'BRIEN: El pasado no está en el reloj, {nombre}. Ni en el periódico. Ni en su cabeza. El pasado está donde el Partido dice que está. # id:fc_03c_pasado_01
O'BRIEN: ¿Qué hora marca? # minijuego:dial,ronda=2,resultado=dial_respuesta # id:fc_03c_r2
-> respuesta ->
PENSAMIENTO: Vomito sobre la camilla. Me limpia la frente con un paño. # id:fc_03c_pano
O'BRIEN: Usted lo sabía. Lo escribió en sus partes cada día. Es usted quien mejor lo sabe de todo Oceanía. # id:fc_03c_pasado_02
O'BRIEN: ¿Qué hora marca? # minijuego:dial,ronda=3,resultado=dial_respuesta # id:fc_03c_r3
-> respuesta ->
PENSAMIENTO: Mi voz ya no articula palabras. Solo sonidos. # id:fc_03c_sonidos
O'BRIEN: ¿Qué hora marca? # minijuego:dial,ronda=4,resultado=dial_respuesta # id:fc_03c_r4
-> respuesta ->
O'BRIEN: Mírelo. # minijuego:dial,ronda=5,resultado=dial_respuesta # id:fc_03c_r5
PENSAMIENTO: las on… las once y cu… # id:fc_03c_once
PENSAMIENTO: Sonríe por primera vez de verdad. # id:fc_03c_sonrie
O'BRIEN: ¿Las ve? ¿De verdad las ve? # id:fc_03c_ve
PENSAMIENTO: Las veo. # esperar:1 # id:fc_03c_veo
O'BRIEN: Bien. Ahora sí. # id:fc_03c_bien
PENSAMIENTO: Desabrocha una correa. # id:fc_03c_correa
O'BRIEN: Está usted mejorando mucho. # id:fc_03c_mejorando
->->

= respuesta
{ dial_respuesta:
- "nueve":
    O'BRIEN: No. # id:fc_03c_no
- "once":
    O'BRIEN: Me miente usted. Dice lo que cree que quiero oír. Sigue viendo las nueve y cuarenta. # id:fc_03c_miente
- else:
    O'BRIEN: El silencio también es una respuesta. Y también es incorrecta. # id:fc_03c_silencio
}
->->

// FC.03d — Goldstein
= j_goldstein
{ jornada >= 13 or pregunta_jaula:
    PROTAGONISTA: ¿Existe… Goldstein? # id:fc_03d_prot
    O'BRIEN: Existe. # esperar:1 # id:fc_03d_obrien_01
    O'BRIEN: Le cuidamos mucho. Le llevamos libros. Té, aunque nunca llega caliente. # esperar:1 # id:fc_03d_obrien_02
    O'BRIEN: Él escribe la verdad. Nosotros decidimos quién la lee. # esperar:1 # id:fc_03d_obrien_03
    O'BRIEN: Y cuándo. Y qué le pasa después. # id:fc_03d_obrien_04
}
->->

// ==================================================================== FC.04 — Habitación 101
= habitacion
O'BRIEN: Usted me preguntó, sin preguntarlo, qué hay en la habitación ciento uno. # esperar:1 # id:fc_04_obrien_01
O'BRIEN: Ya lo sabe. Siempre lo ha sabido. Lo sabe desde la calle Stepney. # id:fc_04_obrien_02
PENSAMIENTO: Un techo muy bajo que sigue bajando. Un hueco del tamaño de un cuerpo. Encima, una tolva llena de escombros. # vineta:vineta-habitacion101 # id:fc_04_pens_00
PENSAMIENTO: Me tumban en el hueco. Me atan. # id:fc_04_pens_01
O'BRIEN: Su hermana estuvo once minutos debajo. Respirando. # esperar:1 # id:fc_04_obrien_03
O'BRIEN: Usted la oyó cantar. # vineta:fin # id:fc_04_obrien_04
-> traicion

= traicion
{ final_en_curso == "D" and (aguanto_24h or libro_delatado):
    PENSAMIENTO: Silencio absoluto. # minijuego:h101,sin=dot,resultado=traicion_101 # id:fc_04_silencio_d
- else:
    PENSAMIENTO: Silencio absoluto. # minijuego:h101,resultado=traicion_101 # id:fc_04_silencio
}
PENSAMIENTO: El silbido se corta. Los cascotes dejan de caer. # id:fc_04_pens_02
O'BRIEN: Ya está. # id:fc_04_obrien_05
PENSAMIENTO: Me desatan. O'Brien me pone delante un papel y una pluma. # id:fc_04_pens_03
PENSAMIENTO: La misma pluma. El mismo sonido. # minijuego:declaracion # id:fc_04_pens_04
~ prota_preso = false
CARTEL: Algún tiempo después. # fx:negro # id:fc_05_cartel # escena:cafe # pos:mesa
-> DONE

// ==================================================================== FC.05 — El Café del Castaño
=== cafe ===

= entrar
{ cafe_visto:
    -> DONE
}
~ cafe_visto = true
PENSAMIENTO: Un café pequeño y casi vacío. Un tablero de ajedrez. Una telepantalla. Un camarero que rellena los vasos de ginebra sin que se lo pidan. # fx:aclarar # id:fc_05_pens_00
PENSAMIENTO: En la pared, el cartel de Ivy. # id:fc_05_pens_01
PENSAMIENTO: En otra mesa, Amory. Sin gafas, sin dientes, jugando solo al ajedrez. No levanta la vista. # id:fc_05_pens_02
{ amory_reaccion == "denuncia":
    PENSAMIENTO: Levanta la vista un instante. Me mira. Nada en su cara. Vuelve al tablero. # id:fc_05_amory_denuncia
}
-> noticia

// Consecuencias de la traición: la telepantalla del café, de fondo
= noticia
{ traicion_101:
- "nell":
    TELEPANTALLA: …ejecutada esta mañana la agente estasiática N. Hask, que durante años se infiltró en el Ministerio de la Paz disfrazada de limpiadora… # id:fc_05_tp_nell
- "dot":
    TELEPANTALLA: …detenida en Limehouse una red de acaparamiento de retales… # id:fc_05_tp_dot
    PENSAMIENTO: En la pantalla, la foto de Dot. # id:fc_05_dot_foto
- "brooke":
    PENSAMIENTO: Por la ventana me parece ver a Brooke, empujando el carrito de la limpieza del Minipax. Después ya no está. # id:fc_05_brooke
- "len":
    TELEPANTALLA: …capturado en Limehouse un prisionero estasiático que había escapado de forma fraudulenta de la justicia del Partido… # id:fc_05_tp_len
    PENSAMIENTO: La foto de Len, con el ancla. # id:fc_05_len_foto
- else:
    TELEPANTALLA: Recuerda a los traidores de Stepney. # id:fc_05_tp_ivy
    PENSAMIENTO: Han cambiado el texto del cartel. Y la cara de Ivy, en la pared del café, es la misma. Pero sus ojos son ahora los de una enemiga. # id:fc_05_ivy
}
-> DONE

= amory_mirar
PENSAMIENTO: Amory. Mueve una pieza. No sabe por qué. Yo tampoco. # id:fc_05_amory_mirar
-> DONE

= amory
PENSAMIENTO: Me levanto. Doy dos pasos. Me paro. Vuelvo a sentarme. # id:fc_05_amory_01
PENSAMIENTO: No hay nada que decir. No hay nadie a quien decírselo. # id:fc_05_amory_02
-> DONE

= cartel_mirar
PENSAMIENTO: Ivy. # id:fc_05_cartel_mirar
-> DONE

= ventana_mirar
PENSAMIENTO: Una calle gris. # id:fc_05_ventana
-> DONE

= camarero_mirar
PENSAMIENTO: Rellena el vaso. No me mira. Nunca me mira. # id:fc_05_camarero
-> DONE

// El final: la mesa, el tablero, la fanfarria
= mesa
PENSAMIENTO: Me siento frente al tablero. Muevo una pieza. No sé por qué. # id:fc_05_mesa_00
TELEPANTALLA: ¡Atención! ¡Atención! ¡Noticia gloriosa del frente! ¡Victoria aplastante sobre {jornada >= 10:Estasia|Eurasia}! # sfx:fanfarria # id:fc_05_tp_victoria
PENSAMIENTO: Levanto la vista hacia la telepantalla. Hacia el cartel de la pared. # id:fc_05_mesa_01
PENSAMIENTO: Ivy. # esperar:1.2 # id:fc_05_ivy_01
PENSAMIENTO: Mi pobre Ivy. Tan equivocada. # esperar:1.2 # id:fc_05_ivy_02
PENSAMIENTO: Ya está. Ya pasó todo. # id:fc_05_ivy_03
PENSAMIENTO: Me cae una lágrima. Sonrío. # id:fc_05_lagrima
CARTEL: Había vencido sobre sí mism{o}. # id:fc_05_cartel_01
{ final_en_curso == "D":
    CARTEL: Amaba al Gran Hermano. # id:fd_06_cartel
    -> fd_epilogo
}
CARTEL: Amaba al Gran Hermano. # id:fc_05_cartel_02
{ fc_variante == "libro_vive":
    CARTEL: En una cripta bajo una iglesia en ruinas, una vela sigue encendida junto a una máquina de escribir. # id:fc_05_libro_vive
}
CARTEL: FINAL C · HABITACIÓN 101 # id:fc_05_fin # final:C
-> DONE
