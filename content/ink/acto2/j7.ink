// ACTO II · JORNADA 7 — Naranjas y limones (guion: docs/guion-detallado/02-acto-2.md)
// Decisión clave del acto: aceptar la petición de Nell (Acto III), negarse (Final A) o denunciarla (Final B temprano).

// ==================================================================== J7.01 — El piso · 07:15
=== j7_piso ===
{ gimnasia_j7:
    -> DONE
}
~ gimnasia_j7 = true
TELEPANTALLA: ¡Arriba, camaradas! ¡Uno, dos! ¡Más alto! # sfx:silbato # id:j7_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J7-GIMNASIA,expr=entusiasmo,dif=media,golpes=12,coro=¡Uno!/¡Dos! # id:j7_01_tp_02
{ cf_j7_gimnasia == "fallo":
    ~ sube_sospecha(3)
}
TELEPANTALLA: ¡Camaradas! ¡Faltan diez días para la Semana del Odio! ¡Diez días para mostrar al enemigo la furia de Oceanía! # id:j7_01_tp_03
{
- duda >= 50:
    PENSAMIENTO: Diez días para aprender a gritar sin creer. # id:j7_01_pens_d2
- duda >= 20:
    PENSAMIENTO: Diez días. Gritaré. Tengo que gritar. # id:j7_01_pens_d1
- else:
    PENSAMIENTO: Diez días. Este año gritaré más que nunca. # id:j7_01_pens_d0
}
-> DONE

// ==================================================================== J7.02 — Departamento
=== j7_entrar ===
{ depto_j7_visto:
    -> DONE
}
~ depto_j7_visto = true
~ cinta_rota = true
PENSAMIENTO: Me siento. La cinta de la máquina se rompe al primer golpe. # sfx:tecla # id:j7_02_pens_00
PELL: Cuarto de suministros. Al fondo del pasillo. Cintas en la tercera balda. # id:j7_02_pell_01
PENSAMIENTO: No me ha mirado. # id:j7_02_pens_01
-> DONE

=== j7_salir ===
{ nell_respuesta != "":
    PENSAMIENTO: La jornada se hace eterna. # id:j7_02_salir_tarde
    CARTEL: Esa noche. # fx:negro # id:j7_05_cartel_depto # escena:piso_noche # pos:puerta
    -> DONE
}
{ diario_confiscado and not hilda_en_minipax:
    ~ hilda_en_minipax = true
    PENSAMIENTO: Al pasar junto a la puerta de Voss, se abre. Sale Hilda. # id:j7_02_hilda_01
    PENSAMIENTO: Nos cruzamos. Me sonríe sin enseñar los dientes. # id:j7_02_hilda_02
    PENSAMIENTO: ¿Hilda? ¿Aquí? ¿En el Minipax? # id:j7_02_hilda_03
}
# escena:pasillo # pos:depto
-> DONE

// ==================================================================== J7.03 — Cuarto de suministros
=== suministros ===

= entrar
{ jornada == 8:
    -> j8_nell
}
{ suministros_visto:
    -> DONE
}
~ suministros_visto = true
PENSAMIENTO: Estrecho, sin ventanas. Papel, cintas, tinta, frascos de chinchetas. Una bombilla desnuda. # id:j7_03_pens_00
-> DONE

= hueco_mirar
PENSAMIENTO: Aquí había una telepantalla. La quitaron. ¿Por qué quitarían una telepantalla? # id:j7_03_hueco
-> DONE

= balda_mirar
PENSAMIENTO: Cintas de máquina, en la tercera balda. # id:j7_03_balda
-> DONE

= nell_mirar
PENSAMIENTO: La limpiadora. La mujer de la calle Stepney. La misma mirada. # id:j7_03_nell_mirar
-> DONE

= nell_hablar
-> j7_nell.preguntas

= cintas
{ nell_respuesta != "":
    PENSAMIENTO: Ya tengo la cinta. # id:j7_03_cinta_ya
    -> DONE
}
-> j7_nell

= salir
{ nell_suministros:
    PENSAMIENTO: El carrito bloquea la puerta. # id:j7_03_salir_bloqueada
    -> DONE
}
# escena:pasillo # pos:suministros
-> DONE

=== j7_nell ===
PENSAMIENTO: Busco en la tercera balda. Detrás de mí, la puerta se cierra con un clic. # sfx:cerrojo # id:j7_03_pens_01
~ nell_suministros = true
PENSAMIENTO: Me giro. # refrescar # prota:abajo # id:j7_03_pens_02
PENSAMIENTO: La limpiadora, delante de la puerta. El carrito bloquea la salida. # id:j7_03_pens_03
NELL: No grites. Aquí no te oye nadie. Pero los pasillos tienen orejas. # id:j7_03_nell_01
PROTAGONISTA: ¿Qué…? Déjeme salir. # id:j7_03_prot_01
NELL: Naranjas y limones, dicen las campanas de San Clemente. # sfx:naranjas # id:j7_03_nell_02
// el destello de la calle Stepney: Ivy cantando, la mujer del pañuelo apartando cascotes
PENSAMIENTO: La calle Stepney. La mano de Ivy. La mujer del pañuelo apartando cascotes. La misma mirada. # recuerdo:loc-stepney_ivy # id:j7_03_pens_04
PROTAGONISTA: …Usted. Usted estaba allí. # id:j7_03_prot_02
NELL: Yo estaba allí. Saqué tres piedras de encima de tu hermana antes de que llegara el hombre del abrigo. # id:j7_03_nell_03
NELL: Ella cantaba esa canción porque era la nuestra. # id:j7_03_nell_04
PROTAGONISTA: ¿La… nuestra? # id:j7_03_prot_03
NELL: Amory no fue el primero. Tu hermana tampoco. # id:j7_03_nell_05
~ diario_nell = true
-> preguntas

// Hasta cuatro preguntas antes de que Nell corte
= preguntas
{ preguntas_nell >= 4:
    NELL: Basta de preguntas. # id:j7_03_nell_basta
    -> peticion
}
~ preguntas_nell += 1
* [«¿Qué sabe usted de mi hermana?»]
    NELL: Que no murió por lo que te contaron. Y que tú no estás preparad{o} para oír el resto. Todavía no. # id:j7_03_nell_06
    -> preguntas
* [«¿Usted me puso el cuaderno en el abrigo?»]
    NELL: El cuaderno era de Felix. Lo saqué de su papelera antes de que lo hicieran ceniza. # id:j7_03_nell_07
    NELL: Felix no era de los nuestros. Solo era alguien que veía. Aquí, eso basta para desaparecer. # id:j7_03_nell_08
    { diario_confiscado:
        PENSAMIENTO: Saca algo del carrito. El cuaderno. # id:j7_03_pens_05
        NELL: Y esto estaba en el despacho del Comité de tu casa. Los proles también limpian allí. # id:j7_03_nell_09
        NELL: Tu vecina lee muy despacio. Ha llegado a la primera página. # id:j7_03_nell_10
        ~ inventario += diario
        ~ diario_confiscado = false
        ~ diario_escondite = ""
        PENSAMIENTO: Me lo da. # objeto:diario # id:j7_03_pens_06
    }
    -> preguntas
* [«¿Qué es lo "nuestro"? ¿Quiénes son ustedes?»]
    PENSAMIENTO: Una sonrisa torcida. La primera. # id:j7_03_pens_07
    NELL: Eso lo sabrás si das el siguiente paso. Si no, mejor que no lo sepas nunca. # id:j7_03_nell_11
    -> preguntas
* {patron_conclusion == "proles"} [«¿Por qué los cohetes solo caen sobre los proles?»]
    PENSAMIENTO: Me mira con algo parecido al respeto. # id:j7_03_pens_08
    NELL: Lo has visto tú solo. Bien. Esa es exactamente la pregunta. Y la respuesta está a tres plantas de aquí. # id:j7_03_nell_12
    -> preguntas
* [«Debería denunciarla ahora mismo.»]
    NELL: Deberías. # id:j7_03_nell_13
    PENSAMIENTO: No se mueve. # id:j7_03_pens_09
    NELL: La puerta está detrás de mí. Voss está a cuarenta pasos. Ve. # id:j7_03_nell_14
    -> preguntas
* [Escuchar lo que ha venido a decir.]
    -> peticion

= peticion
NELL: Hay un papel azul. En el Archivo Restringido de este ministerio, planta once, sala de los cerrojos dobles. Lo llaman la Planilla Azul. # id:j7_03_nell_15
NELL: En ese papel está escrito dónde caerá el próximo cohete. Antes de que caiga. # id:j7_03_nell_16
PROTAGONISTA: Eso es imposible. # id:j7_03_prot_04
NELL: Entonces no tienes nada que temer al buscarlo. # id:j7_03_nell_17
PROTAGONISTA: ¿Y si lo encuentro? # id:j7_03_prot_05
NELL: Entonces sabrás quién mató a Sammy. # id:j7_03_nell_18
NELL: Y a tu hermana. # esperar:1.2 # id:j7_03_nell_19
* [«…¿Cómo entro en el Archivo?»] # decision:D-J7-NELL
    -> aceptar
* [«No. No sé quién es usted. No quiero saberlo.»]
    -> negar
* [Apartar el carrito de un empujón y salir.]
    -> j7_denunciar

// J7.04-ACEPTAR
= aceptar
~ nell_respuesta = "aceptar"
PENSAMIENTO: Asiente una vez. # id:j7_04a_pens_00
NELL: Mañana por la noche. El turno de guardia de la planta once cambia a las once. Hay cuatro minutos en los que la escalera de servicio no la mira nadie. # id:j7_04a_nell_01
~ inventario += llave_calderas
PENSAMIENTO: Saca del carrito una llave grande y oxidada. # objeto:llave_calderas # id:j7_04a_pens_01
NELL: La sala de calderas comunica con el montacargas viejo. El montacargas para en la once. # id:j7_04a_nell_02
NELL: Si te cogen, no me conoces. Yo tampoco te conozco. Nunca te he visto. # id:j7_04a_nell_03
NELL: Eso no es una amenaza. Es lo único que puedo hacer por ti. # id:j7_04a_nell_04
{ sospecha >= 50:
    PENSAMIENTO: Antes de salir, se detiene. # id:j7_04a_pens_02
    NELL: Te están mirando. Lo sé por cómo te mira tu jefe. Ten cuidado con quién hablas fuera de aquí. Sobre todo con la gente amable. # id:j7_04a_nell_05
}
~ nell_suministros = false
PENSAMIENTO: Abre la puerta y sale empujando el carrito, con la cabeza gacha. Otra vez invisible. # refrescar # id:j7_04a_pens_03
PENSAMIENTO: Cojo una cinta de la tercera balda. # id:j7_04a_pens_04
-> DONE

// J7.04-DUDAR (negarse con Duda alta) · J7.04-NEGAR → Final A
= negar
{ duda >= 30:
    ~ nell_respuesta = "dudar"
    PENSAMIENTO: No se aparta. # id:j7_04d_pens_00
    NELL: Mientes mal. Lo veo en tu cara. Llevas días mintiendo mal. # id:j7_04d_nell_01
    NELL: Piénsalo esta noche. Mañana por la noche estaré aquí a las diez y media. Si no vienes, no volverás a verme. # id:j7_04d_nell_02
    ~ nell_suministros = false
    PENSAMIENTO: Sale. Me quedo solo en el cuarto. # refrescar # id:j7_04d_pens_01
    -> DONE
}
~ nell_respuesta = "negar"
PENSAMIENTO: Me mira largo. Algo se le apaga en la cara. # id:j7_04n_pens_00
NELL: Como tu hermana no. Ella habría dicho que sí. # id:j7_04n_nell_01
NELL: Que vivas mucho, camarada. # id:j7_04n_nell_02
~ nell_suministros = false
PENSAMIENTO: Sale. Cojo la cinta de la tercera balda. Me tiemblan las manos. Vuelvo a mi mesa. # refrescar # id:j7_04n_pens_01
CARTEL: Esa noche. # fx:negro # id:j7_04n_cartel # escena:piso_noche # pos:puerta
-> DONE

// J7.04-DENUNCIAR → Final B (versión temprana)
=== j7_denunciar ===
~ nell_respuesta = "denunciar"
~ nell_suministros = false
PENSAMIENTO: Aparto el carrito de un empujón y salgo al pasillo. # refrescar # id:j7_04b_pens_00
PENSAMIENTO: Camino hacia el despacho de Voss. A cada paso, el pasillo se alarga, como en el sueño de Ivy. # fx:negro # id:j7_04b_pens_01 # escena:despacho_voss # pos:puerta
-> DONE

// ==================================================================== J7.05 — El piso · Noche
=== j7_noche ===
{ nell_respuesta == "negar":
    -> final_a
}
{ noche_j7_vista:
    -> DONE
}
~ noche_j7_vista = true
PENSAMIENTO: La telepantalla emite música marcial. # id:j7_05_pens_00
{ nell_respuesta == "dudar":
    PENSAMIENTO: «Si no vienes, no volverás a verme.» # id:j7_05_dudar
}
-> DONE

=== j7_cartel_mirar ===
PENSAMIENTO: «Ella habría dicho que sí.» # id:j7_05_cartel_01
PENSAMIENTO: Eso no lo ha dicho. Pero lo ha pensado. Lo he visto en su cara. # id:j7_05_cartel_02
{ diario_escondite == "cartel":
    PENSAMIENTO: Toco el borde del cartel, donde está el cuaderno. # id:j7_05_cartel_03
}
PENSAMIENTO: ¿Habrías dicho que sí, Ivy? # id:j7_05_cartel_04
-> DONE

=== j7_dormir ===
{ nell_respuesta == "dudar":
    -> noche_decidir
}
-> fin_acto

// ◆ D-J7-NOCHE
= noche_decidir
PENSAMIENTO: «Si no vienes, no volverás a verme.» # id:j7_05_noche_01
* [Volver mañana al cuarto de suministros.] # decision:D-J7-NOCHE
    ~ nell_respuesta = "aceptar_tarde"
    -> fin_acto
* [No volver.]
    ~ nell_respuesta = "negar"
    -> final_a

= fin_acto
PENSAMIENTO: Me acuesto. # fx:negro # id:j7_05_dormir_01
PENSAMIENTO: Muy lejos, un silbido. Un impacto, en algún barrio prole. # sfx:silbido # esperar:2.6 # id:j7_05_dormir_02
{ nell_respuesta == "aceptar":
    PENSAMIENTO: Mañana sabré dónde caerá el próximo. # sfx:impacto # id:j7_05_dormir_03
- else:
    PENSAMIENTO: Mañana. A las diez y media. # sfx:impacto # id:j7_05_dormir_04
}
~ jornada = 8
~ desayunado = false
CARTEL: FIN DEL ACTO II # id:j7_05_fin_acto
CARTEL: ACTO III¶LA HERMANDAD # id:j7_05_acto3
CARTEL: JORNADA 8 # sfx:silbato # id:j7_05_jornada8
CARTEL: La guerra es la paz. # id:j7_05_fin # escena:piso # pos:cama
-> DONE
