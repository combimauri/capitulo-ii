// ACTO I · JORNADA 2 — Dos Minutos de Odio (guion: docs/guion-detallado/01-acto-1.md)
// Los knots de los escenarios compartidos (piso, escalera, depto) desvían aquí cuando jornada == 2.

// ==================================================================== J2.01 — El piso · 07:15
=== j2_piso ===
{ gimnasia_j2:
    -> DONE
}
~ gimnasia_j2 = true
TELEPANTALLA: ¡Buenos días, camaradas! ¡Hoy, tablas cortas: hay sesión especial de Odio! ¡Brazos arriba! # sfx:silbato # id:j2_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J2-GIMNASIA,expr=entusiasmo,dif=facil,golpes=8,coro=¡Uno!/¡Dos! # id:j2_01_tp_02
{ cf_j2_gimnasia == "fallo":
    ~ sube_sospecha(3)
    TELEPANTALLA: ¡{num} {apellido}! ¡Ayer lo hizo mejor! # id:j2_01_tp_03
}
TELEPANTALLA: ¡Buenas noticias de la Minindancia! Gracias al esfuerzo de nuestro pueblo, la ración de chocolate aumenta a veinte gramos semanales. ¡Gracias, Gran Hermano! # id:j2_01_tp_04
PENSAMIENTO: Veinte gramos. ¡Veinte! El Partido cuida de nosotros. # id:j2_01_pens_01
-> DONE

// ==================================================================== J2.02 — La escalera · Los Parsons
=== j2_parsons ===
{ parsons_j2:
    -> DONE
}
~ parsons_j2 = true
NIÑO PARSONS: ¡Traidor! ¡Espía euroasiático! ¡A la horca! # id:j2_02_nino_01
PARSONS: ¡Camarada {apellido}! ¡Magnífico, magnífico! ¿Has visto a mis pequeños? Llevan toda la semana pidiendo ir al ahorcamiento de prisioneros del parque. # id:j2_02_parsons_01
PARSONS: Les he dicho que si se portan bien… ¡Toma! Para la Semana del Odio. Estoy en el comité de banderines. # id:j2_02_parsons_02
PROTAGONISTA: Gracias, camarada Parsons. Sus hijos son un ejemplo. # id:j2_02_prot_01
PARSONS: ¡Lo son! ¡Lo son! El mes pasado la pequeña denunció a un vendedor de cordones. ¡Por sus zapatos! Decía que eran zapatos extranjeros. Tenía un ojo… # id:j2_02_parsons_03
HIJA PARSONS: Usted habla dormid{o}. # id:j2_02_hija_01
PROTAGONISTA: …¿Qué? # id:j2_02_prot_02
HIJA PARSONS: Por la noche. A través de la pared. Dice un nombre. # id:j2_02_hija_02
PARSONS: ¡Ja, ja! ¡Qué imaginación! Venga, venga, a vestirse. # id:j2_02_parsons_04
~ sube_sospecha(2)
PENSAMIENTO: Un nombre. Ivy, seguramente. No es ningún crimen soñar con una mártir. # id:j2_02_pens_01
-> DONE

=== j2_bajar ===
CARTEL: Ministerio de la Verdad. Sesión conjunta de los cuatro ministerios. Aniversario de la Victoria de Malabar. # fx:negro # id:j2_02_cartel # escena:salon_odio # pos:entrada
-> DONE

// ==================================================================== J2.03 — Dos Minutos de Odio
=== odio ===

= entrar
{ odio_hecho:
    -> DONE
}
PENSAMIENTO: Delegaciones de los cuatro ministerios. Mi asiento está en la tercera fila, junto a Amory. # id:j2_03_pens_00
-> DONE

= pantalla_mirar
PENSAMIENTO: Dos Minutos de Odio. A las once. Se me acelera el pulso solo de leerlo. # id:j2_03_pantalla_mirar
-> DONE

= asiento_mirar
PENSAMIENTO: Mi asiento. Tercera fila. # id:j2_03_asiento_mirar
-> DONE

= julia_mirar
PENSAMIENTO: Liga Anti-Sex. Esas chicas son las más ortodoxas de todas. Da gusto verlas. # id:j2_03_julia_mirar
-> DONE

= obrien_mirar
PENSAMIENTO: Partido Interior. Se ajusta las gafas de una forma… casi amable. Como un aristócrata de los libros de historia, antes de que la Revolución los barriera. # id:j2_03_obrien_mirar
-> DONE

= winston_mirar
PENSAMIENTO: Smith. Al menos ha venido. # id:j2_03_winston_mirar
-> DONE

= amory_mirar
PENSAMIENTO: Amory ya está sentado, frotándose las manos. # id:j2_03_amory_mirar
-> DONE

= amory
{ odio_hecho:
    AMORY: Necesito una ginebra. O dos. # id:j2_03_amory_despues
    -> DONE
}
AMORY: ¡Siéntate, que empieza! Hoy dicen que sale Goldstein en persona. Bueno, su cara. # id:j2_03_amory_antes
-> DONE

= sentarse
{ odio_hecho:
    PENSAMIENTO: Ya ha terminado. Me tiemblan las piernas. # id:j2_03_sentarse_despues
    -> DONE
}
~ odio_hecho = true
PENSAMIENTO: Las luces bajan. # sfx:chirrido # fx:negro # id:j2_03_pens_01
TELEPANTALLA: …la libertad de expresión… la paz con Eurasia… la libertad de prensa… # fx:aclarar # id:j2_03_tp_01
PENSAMIENTO: Goldstein. # id:j2_03_pens_02
PENSAMIENTO: Las luces vuelven. El público, agotado y sudoroso, se dispersa. # cf:id=CF-J2-ODIO # id:j2_03_pens_03
{ cf_j2_odio == "fallo":
    ~ sube_sospecha(5)
}
{ cf_j2_odio_transicion == "fallo":
    ~ sube_sospecha(5)
}
{ cf_j2_odio == "perfecto":
    PENSAMIENTO: El hombre del Partido Interior me mira de reojo. Un instante. # id:j2_03_obrien_mira
}
AMORY: Uf. Siempre me deja como si hubiera corrido diez kilómetros. Tú gritabas de verdad, ¿eh? Te vi. Daba miedo. # id:j2_03_amory_01
PROTAGONISTA: Es lo mínimo que le debo a Ivy. # id:j2_03_prot_01
AMORY: Claro. Claro que sí. # id:j2_03_amory_02
{ cf_j2_odio_amory == "visto":
    PENSAMIENTO: Al final se quedó callado, limpiándose las gafas. Solo un segundo. # id:j2_03_amory_gafas
    PENSAMIENTO: Se le empañarían. Con tanto grito. # id:j2_03_amory_gafas_2
}
CARTEL: De vuelta en el Ministerio de la Paz. # fx:negro # id:j2_03_cartel # escena:departamento # pos:mesa
-> DONE

// ==================================================================== J2.04 — Departamento · La broma
=== j2_entrar ===
{ depto_j2_visto:
    -> DONE
}
~ depto_j2_visto = true
PENSAMIENTO: Llega una directiva por el tubo. Cartografía. # sfx:tubo # id:j2_04_pens_00
-> DONE

=== j2_amory ===
{ amory_reaccion == "":
    AMORY: ¿Ya tienes la directiva? Doce kilómetros, como siempre. # id:j2_04_amory_antes
- else:
    AMORY: ¡Cartografía comparte! # id:j2_04_amory_despues
}
-> DONE

=== j2_mesa ===
{ frente_j2 != "":
    PENSAMIENTO: El frente ya está en su sitio. # id:j2_04_mesa_hecha
    -> DONE
}
PENSAMIENTO: Las banderitas, en su sitio. Así es la historia. # minijuego:frente,resultado=frente_j2 # id:j2_04_pens_01
AMORY: ¿Te has fijado en que el frente de Malabar lleva tres años en el mismo río? Mira los agujeros. # id:j2_04_amory_01
AMORY: Este mapa tiene más agujeros que un queso de la Minindancia. Avanzamos doce, retrocedemos… perdón, rectificamos doce. Avanzamos doce. # id:j2_04_amory_02
AMORY: Si sumas todos los partes del año, ya deberíamos estar desayunando en Pekín. # id:j2_04_amory_03
AMORY: Toma, usa el mío. El tuyo no tiene punta. Que no se diga que Cartografía no comparte. # id:j2_04_amory_04
~ inventario += lapiz_amory
PENSAMIENTO: La telepantalla de la mesa está encendida, a medio metro. ¿Lo habrá oído? # id:j2_04_pens_02
* [Reírse: «Pekín. Me gusta.»] # decision:D-J2-AMORY
    ~ amory_reaccion = "risa"
    ~ sube_duda(5)
    ~ sube_sospecha(5)
    AMORY: ¡Ja! Sabía que tenías sentido del humor, {apellido}. Lo escondes muy bien. # id:j2_04_amory_05
    -> DONE
* [Reprenderle: «Amory. Eso suena a crimental.»]
    ~ amory_reaccion = "reprimenda"
    AMORY: Es… una broma geográfica, camarada. Una broma de cartógrafos. Olvídalo. # id:j2_04_amory_06
    -> DONE
* [Denunciarle ante Voss.]
    ~ amory_reaccion = "denuncia"
    PENSAMIENTO: Me levanto. El despacho del Subdirector está a veinte pasos. # id:j2_04_pens_03 # escena:despacho_voss # pos:puerta
    -> DONE

=== voss_despacho ===
= entrar
{ jornada == 3:
    -> j3_voss
}
{ amory_reaccion != "denuncia" or despacho_visto:
    -> DONE
}
~ despacho_visto = true
VOSS: ¿Sí? # id:j2_04c_voss_01
PROTAGONISTA: Subdirector. El camarada Amory ha hecho un comentario sobre el frente de Malabar. Ha dicho que… que el frente no se mueve. # id:j2_04c_prot_01
VOSS: ¿Con esas palabras? # esperar:1.2 # id:j2_04c_voss_02
PROTAGONISTA: Ha dicho que deberíamos estar en Pekín. Que los partes, sumados… # id:j2_04c_prot_02
VOSS: Suficiente. # id:j2_04c_voss_03
VOSS: Ha hecho usted lo correcto, camarada {apellido}. El Partido valora la vigilancia. Especialmente en alguien con su… historia familiar. # id:j2_04c_voss_04
PROTAGONISTA: Gracias, Subdirector. # id:j2_04c_prot_03
VOSS: Vuelva a su mesa. Y, camarada… # esperar:1 # id:j2_04c_voss_05
VOSS: No comente esto con nadie. Por su propio bien. # id:j2_04c_voss_06
~ baja_sospecha(10)
PENSAMIENTO: He hecho lo correcto. He hecho lo correcto. ¿Por qué me tiemblan las manos? # id:j2_04c_pens_01 # escena:departamento # pos:despacho
-> DONE

= voss_mirar
PENSAMIENTO: Me mira como se mira un expediente. # id:j2_04c_voss_mirar
-> DONE

=== j2_salir ===
{ frente_j2 == "":
    PENSAMIENTO: Primero, el frente. # id:j2_04_salir_no
    -> DONE
}
{ amory_reaccion == "denuncia":
    PENSAMIENTO: Amory me sonríe desde su mesa, ajeno a todo, y me saluda con la mano. # id:j2_04_amory_saluda
}
CARTEL: Esa noche. Centro de la Comunidad. # fx:negro # id:j2_04_cartel # escena:centro # pos:puerta
-> DONE

// ==================================================================== J2.05 — Centro de la Comunidad
=== centro ===

= entrar
{ centro_visto:
    -> DONE
}
~ centro_visto = true
HILDA: ¡{nombre}! ¡Justo a tiempo! Necesito manos para las pancartas. La de Goldstein con colmillos está quedando divina. # id:j2_05_hilda_01
-> DONE

= hilda_mirar
PENSAMIENTO: Hilda dirige los ensayos con un silbato. Nadie desafina dos veces. # id:j2_05_hilda_mirar
-> DONE

= hilda
HILDA: Smith no ha venido. Otra vez. Tercera ausencia este mes. Yo solo apunto. Apuntar no es delatar, es ser ordenada. # id:j2_05_hilda_02
{ hilda_aprecio >= 1:
    HILDA: Tú en cambio… Voy a proponer tu nombre para el comité de la Semana del Odio. ¡A la hermana de una mártir no le pueden decir que no! # id:j2_05_hilda_03
}
-> DONE

= parsons_mirar
PENSAMIENTO: Parsons, con más banderines. Siempre más banderines. # id:j2_05_parsons_mirar
-> DONE

= parsons
PARSONS: ¿Sabes que el año pasado colgamos cuatro kilómetros de banderines en el distrito? ¡Cuatro! Este año quiero llegar a cinco. ¡Magnífico, magnífico! # id:j2_05_parsons_01
-> DONE

= hija_mirar
PENSAMIENTO: La hija de Parsons me mira y escribe algo en una libretita. # id:j2_05_hija_mirar
-> DONE

= martires_mirar
PENSAMIENTO: Diez rostros heroicos. En primera fila, Ivy. Ahí estás. Entre los mejores. # id:j2_05_martires_01
PENSAMIENTO: Le han cambiado la nariz. Da igual. Es ella. Es lo que significa. # id:j2_05_martires_02
-> DONE

= piano_mirar
PENSAMIENTO: Un piano desafinado. Le faltan dos teclas. # id:j2_05_piano_mirar
-> DONE

= piano_usar
PENSAMIENTO: Unas teclas, sin pensar… # sfx:naranjas # esperar:3.2 # id:j2_05_piano_01
PENSAMIENTO: ¿Por qué me sé esto? …Ivy. Ivy la cantaba. # id:j2_05_piano_02
-> DONE

= pingpong_mirar
PENSAMIENTO: El ping-pong es un deporte comunitario. Nadie juega solo. # id:j2_05_pingpong_mirar
-> DONE

= pancarta_mirar
PENSAMIENTO: "¡MUERTE A EURASIA!", a medio pintar. # id:j2_05_pancarta_mirar
-> DONE

= pancarta_usar
{ pancarta_j2 != "":
    PENSAMIENTO: Ya está pintada. # id:j2_05_pancarta_hecha
    -> DONE
}
PENSAMIENTO: A ver ese pulso. # minijuego:pancarta,resultado=pancarta_j2 # id:j2_05_pancarta_01
{ pancarta_j2 == "bien":
    ~ hilda_aprecio += 1
    HILDA: ¡Preciosa! ¡Eso es pintar con odio! # id:j2_05_pancarta_bien
- else:
    HILDA: Bueno… la intención es lo que cuenta. El Partido valora la intención. # id:j2_05_pancarta_mal
}
-> DONE

= salir
CARTEL: Esa noche. # fx:negro # id:j2_05_cartel # escena:sueno # pos:inicio
-> DONE

// ==================================================================== J2.06 — Sueño
=== sueno ===

= entrar
{ sueno_visto:
    -> DONE
}
~ sueno_visto = true
IVY (NIÑA): Naranjas y limones, dicen las campanas de San Clemente… # sfx:naranjas # id:j2_06_ivy_01
-> DONE

= ivy_mirar
PENSAMIENTO: Ivy. Salta a la comba. Cada vez que me acerco, la calle se alarga. # id:j2_06_ivy_mirar
-> DONE

= final
IVY (NIÑA): ¿Qué hora es? # sfx:silbido # id:j2_06_ivy_02
PENSAMIENTO: Miro mi muñeca. Llevo su reloj. Las nueve y cuarenta. # id:j2_06_pens_01
CARTEL: 21:40 # sfx:impacto # fx:destello # id:j2_06_cartel
~ jornada = 3
~ desayunado = false
~ amory_borrado = true
CARTEL: JORNADA 3 # fx:negro # sfx:silbato # id:j2_06_jornada3 # escena:piso # pos:cama
-> DONE
