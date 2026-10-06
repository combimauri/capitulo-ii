// ACTO I · JORNADA 3 — La grieta (guion: docs/guion-detallado/01-acto-1.md)
// Los knots de los escenarios compartidos (piso, depto, despacho, piso_noche) desvían aquí cuando jornada == 3.

// ==================================================================== J3.01 — El piso · 07:15
=== j3_piso ===
{ gimnasia_j3:
    -> DONE
}
~ gimnasia_j3 = true
TELEPANTALLA: ¡Arriba, camaradas! ¡Tablas de gimnasia! ¡Uno, dos! # sfx:silbato # id:j3_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J3-GIMNASIA,expr=entusiasmo,dif=facil,golpes=8,coro=¡Uno!/¡Dos! # id:j3_01_tp_02
{ cf_j3_gimnasia == "fallo":
    ~ sube_sospecha(3)
}
TELEPANTALLA: …y recuerden, camaradas: la Semana del Odio está cada vez más cerca. ¡El enemigo tiembla! # id:j3_01_tp_03
-> DONE

=== j3_salir_piso ===
CARTEL: Ministerio de la Paz. Planta catorce. # fx:negro # id:j3_01_cartel # escena:departamento # pos:puerta
-> DONE

// ==================================================================== J3.02 — Departamento · La mesa vacía
=== j3_entrar ===
{ voss_j3_visto and dp_j3_amory == "":
    -> j3_doblepensar
}
{ depto_j3_visto:
    -> DONE
}
~ depto_j3_visto = true
PENSAMIENTO: En la mesa de Amory hay otra persona. Un hombre gris que escribe a máquina con dos dedos. # id:j3_02_pens_00
PENSAMIENTO: Los dibujos de pájaros han desaparecido. La silla es la misma. # id:j3_02_pens_01
PENSAMIENTO: ¿Amory se ha cambiado de mesa? # id:j3_02_pens_02
-> DONE

=== j3_pell ===
{ pell_hablado:
    PELL: Tengo trabajo, camarada. # id:j3_02_pell_otra
    -> DONE
}
~ pell_hablado = true
PROTAGONISTA: Disculpe, camarada. ¿Sabe dónde se ha sentado hoy Amory? # id:j3_02_prot_01
PELL: ¿Quién? # id:j3_02_pell_01
PROTAGONISTA: Felix Amory. Esta es su mesa. # id:j3_02_prot_02
PENSAMIENTO: Deja de teclear. Me mira sin ninguna expresión. # id:j3_02_pens_03
PELL: Esta mesa es mía. Siempre ha sido mía. Llevo aquí… # id:j3_02_pell_02
PELL: …siempre. # esperar:1 # id:j3_02_pell_03
PENSAMIENTO: Miente. O está loco. O… # id:j3_02_pens_04
-> DONE

=== j3_pell_mirar ===
PENSAMIENTO: Un hombre de mediana edad, gris y anodino. Escribe a máquina con dos dedos, muy despacio. # id:j3_02_pell_mirar
-> DONE

=== j3_brooke ===
{ brooke_hablado:
    PENSAMIENTO: Brooke teclea sin levantar la vista. Más deprisa que antes. # id:j3_02_brooke_otra
    -> DONE
}
~ brooke_hablado = true
PROTAGONISTA: Camarada Brooke, ¿ha visto a Amory? # id:j3_02_prot_03
PENSAMIENTO: Los ojos se le van un instante hacia la telepantalla. # id:j3_02_pens_05
BROOKE: …No conozco a ningún Amory. # id:j3_02_brooke_01
PROTAGONISTA: Comíamos los tres juntos los martes. # id:j3_02_prot_04
BROOKE: No sé de qué me habla, camarada. Y usted tampoco. # id:j3_02_brooke_02
~ sube_sospecha(3)
PENSAMIENTO: «Y usted tampoco.» ¿Qué ha querido decir? # id:j3_02_pens_06
-> DONE

=== j3_brooke_mirar ===
PENSAMIENTO: La camarada Brooke. Lleva aquí más años que nadie. Hoy no me mira. # id:j3_02_brooke_mirar
-> DONE

=== j3_proyeccion ===
PENSAMIENTO: Han clavado una hoja sobre el mapa del frente. Es la nueva proyección: las mismas líneas, su mundo «estirado». # id:j3_02_proyeccion_01
PENSAMIENTO: Pero sin pájaros. En la esquina, la firma: «Pell, A.» # id:j3_02_proyeccion_02
PENSAMIENTO: Es su mapa. Y lo firma Pell. # id:j3_02_proyeccion_03
-> DONE

=== j3_personal ===
PENSAMIENTO: Busco en la A. # sfx:tecla # id:j3_02_personal_00
CARTEL: PERSONAL · PARTES Y CARTOGRAFÍA¶…¶ALDRIDGE, M.¶AMES, T.¶ATKINS, R.¶… # id:j3_02_personal_ficha
PENSAMIENTO: Ames, Atkins… No hay Amory. # id:j3_02_personal_01
PENSAMIENTO: La ficha está más blanca que las demás. Como si la hubieran escrito esta mañana. # id:j3_02_personal_02
-> DONE

=== j3_papelera ===
PENSAMIENTO: Vacía. Limpia. Como si nunca hubiera tenido nada dentro. # id:j3_02_papelera
-> DONE

=== j3_mapa ===
PENSAMIENTO: Malabar. Las mismas banderitas. Los mismos agujeros de alfiler. # id:j3_02_mapa_mirar
-> DONE

=== j3_mesa ===
{ dp_j3_amory == "":
    PENSAMIENTO: Mi mesa. No puedo dejar de mirar la de al lado. # id:j3_02_mesa
- else:
    PENSAMIENTO: Hoy no llega nada por el tubo. Como si el día ya estuviera escrito. # id:j3_04_mesa
}
-> DONE

=== j3_despacho ===
{ voss_j3_visto:
    PENSAMIENTO: Ya he hablado con el Subdirector. # id:j3_02_despacho_ya
    -> DONE
}
{ not (pell_hablado and brooke_hablado):
    PENSAMIENTO: No se entra sin ser llamad{o}. Pero si nadie más me responde… # id:j3_02_despacho_no
    -> DONE
}
PENSAMIENTO: Llamo a la puerta del Subdirector. # id:j3_02_despacho_llamar # escena:despacho_voss # pos:puerta
-> DONE

// ==================================================================== J3.02-V — Despacho de Voss
=== j3_voss ===
{ voss_j3_visto:
    -> DONE
}
~ voss_j3_visto = true
PROTAGONISTA: Subdirector, disculpe. El camarada Amory no ha venido hoy y su mesa… # id:j3_02v_prot_01
PENSAMIENTO: Me mira con paciencia. Como a un niño. # id:j3_02v_pens_00
VOSS: No hay ningún Amory en esta sección, camarada {apellido}. # id:j3_02v_voss_01
{ amory_reaccion == "denuncia":
    PROTAGONISTA: Pero ayer… ayer vine a este despacho. Le hablé de él. Usted anotó su nombre. # id:j3_02v_prot_02
    VOSS: Ayer usted vino a este despacho a informar de un… exceso de cansancio. Lo recuerdo perfectamente. # id:j3_02v_voss_02
    VOSS: Y aquí está otra vez, cansad{o}. Le recomiendo descansar, camarada. El cansancio produce recuerdos que no existen. # id:j3_02v_voss_03
    ~ sube_duda(5)
- else:
    VOSS: ¿Se encuentra bien? Está pálid{o}. Quizá debería descansar. # id:j3_02v_voss_04
    VOSS: El cansancio produce… recuerdos que no existen. # id:j3_02v_voss_05
}
* [«Tiene razón, Subdirector. Estoy cansad{o}.»] # decision:D-J3-VOSS
    VOSS: Eso pensaba. # id:j3_02v_voss_06
* [«Le vi ayer. Le vi con mis propios ojos.»]
    ~ voss_j3_insistir = true
    ~ sube_sospecha(10)
    PENSAMIENTO: Un silencio largo. Escribe algo en una ficha. # esperar:1.2 # id:j3_02v_pens_01
    VOSS: Puede retirarse. # id:j3_02v_voss_07
- PENSAMIENTO: Vuelvo a mi mesa. # fx:negro # id:j3_02v_pens_02 # escena:departamento # pos:mesa
-> DONE

// ==================================================================== J3.03 — Doblepensar
// Se dispara al volver a la mesa desde el despacho (j3_entrar).
=== j3_doblepensar ===
PENSAMIENTO: Me siento. Las teclas, el tubo, la telepantallita. Todo en su sitio. # id:j3_03_pens_00
PENSAMIENTO: La pantalla se oscurece por los bordes. # sfx:chirrido # id:j3_03_pens_01
// la etiqueta va en la línea que se muestra después del doblepensar (diseño técnico §4.5)
PENSAMIENTO: La telepantalla vuelve a su volumen de siempre. # dp:id=DP-J3-AMORY # id:j3_03_pens_02
{ dp_j3_amory == "aceptar":
    ~ baja_duda(5)
    ~ baja_sospecha(5)
    PENSAMIENTO: Me he confundido. El cansancio. Voss tiene razón: el cansancio produce recuerdos que no existen. # id:j3_03_aceptar_01
    PENSAMIENTO: Una mesa, una silla, un hombre gris que escribe con dos dedos. Siempre ha sido así. # id:j3_03_aceptar_02
- else:
    ~ sube_duda(15)
    ~ diario_amory = true
    PENSAMIENTO: Felix Amory. Ojos de pájaro. Mordía los lápices. Decía que los mapas eran poesía. # id:j3_03_recordar_01
    PENSAMIENTO: Felix Amory existía ayer. Y hoy no ha existido nunca. # id:j3_03_recordar_02
}
// J3.04 — El lápiz
PENSAMIENTO: Meto la mano en el bolsillo del mono. Hay algo. # objeto:lapiz_amory # id:j3_04_pens_00
-> DONE

=== j3_lapiz_agujero ===
{ dp_j3_amory == "":
    PENSAMIENTO: Es el lápiz de Amory. Tengo que devolvérselo. # id:j3_04_agujero_antes
    -> DONE
}
PENSAMIENTO: La ranura del agujero de la memoria. Sube un aire caliente. # id:j3_04_agujero_01
* [Tirar el lápiz.] # decision:D-J3-LAPIZ
    ~ inventario -= lapiz_amory
    ~ lapiz_destruido = true
    ~ baja_duda(10)
    PENSAMIENTO: El lápiz cae por la ranura. Se oye el aire caliente que sube desde los hornos. # sfx:tubo # id:j3_04_tirar_01
    PENSAMIENTO: Higiénico. # id:j3_04_tirar_02
* [Guardarlo.]
    PENSAMIENTO: Retiro la mano. # id:j3_04_guardar_01
    PENSAMIENTO: …Mañana. Lo tiraré mañana. # id:j3_04_guardar_02
- -> DONE

=== j3_salir ===
{ dp_j3_amory == "":
    PENSAMIENTO: Todavía no. Alguien tiene que saber dónde está Amory. # id:j3_02_salir_no
    -> DONE
}
CARTEL: Fin de la jornada. # fx:negro # id:j3_05_cartel # escena:pasillo # pos:depto
-> DONE

// ==================================================================== J3.05 — Pasillo del Minipax · Salida
=== pasillo ===

= entrar
{ jornada == 7 and not suministros_visto:
    PENSAMIENTO: El cuarto de suministros, al fondo del pasillo. # id:j7_02_pasillo
    -> DONE
}
{ pasillo_visto:
    -> DONE
}
~ pasillo_visto = true
PENSAMIENTO: El pasillo de la planta catorce. Los neones parpadean. # id:j3_05_pens_00
PENSAMIENTO: Al fondo, junto al cuarto de suministros, la limpiadora con su carrito. # id:j3_05_pens_01
-> DONE

= nell_mirar
PENSAMIENTO: Tiene unas hojas en la mano. Las dobla con cuidado y las mete bajo los trapos del carrito. # id:j3_05_nell_mirar_00
{ dp_j3_amory == "recordar":
    PENSAMIENTO: Mapas. Con pájaros diminutos en los márgenes. # id:j3_05_nell_recordar_01
    PENSAMIENTO: Esos pájaros… Son los dibujos de Amory. Los de los márgenes. # id:j3_05_nell_recordar_02
- else:
    PENSAMIENTO: Papeles con… pájaros. Alguien dibujaba pájaros. # id:j3_05_nell_aceptar_01
    PENSAMIENTO: Un pinchazo en la sien. No sé quién. # fx:temblor # id:j3_05_nell_aceptar_02
}
-> DONE

= encuentro
{ nell_se_fue:
    -> DONE
}
PENSAMIENTO: Doy un paso hacia ella. # id:j3_05_pens_02
PENSAMIENTO: La limpiadora levanta la vista. Por primera vez. Me mira a los ojos. # esperar:0.8 # id:j3_05_pens_03
PENSAMIENTO: Una mirada dura y larga. # id:j3_05_pens_04
~ guardia_pasillo = true
PENSAMIENTO: Pasos. Un guardia dobla la esquina del pasillo. # refrescar # prota:izquierda # id:j3_05_pens_05
PENSAMIENTO: Me giro un instante. # id:j3_05_pens_06
~ nell_se_fue = true
PENSAMIENTO: Cuando vuelvo a mirar, el carrito sigue ahí. # refrescar # prota:derecha # id:j3_05_pens_07
PENSAMIENTO: Pero la limpiadora ya no está. # id:j3_05_pens_08
PENSAMIENTO: ¿Dónde…? # id:j3_05_pens_09
-> DONE

= carrito_mirar
{ nell_se_fue:
    PENSAMIENTO: Trapos. Cubos. Lejía. Ni rastro de los dibujos. # id:j3_05_carrito_01
- else:
    PENSAMIENTO: El carrito de la limpieza. Trapos, un cubo, lejía. # id:j3_05_carrito_00
}
-> DONE

= ir_suministros
{ jornada == 7:
    # escena:suministros # pos:puerta
    -> DONE
}
-> suministros_mirar

= suministros_mirar
{ nell_se_fue:
    PENSAMIENTO: Cerrado con llave. ¿Por dónde ha salido? # id:j3_05_suministros_01
- else:
    PENSAMIENTO: El cuarto de suministros. # id:j3_05_suministros_00
}
-> DONE

= guardia_mirar
PENSAMIENTO: Un guardia. Pasa de largo sin mirarme. # id:j3_05_guardia_mirar
-> DONE

= tele_mirar
PENSAMIENTO: La telepantalla del pasillo. También a esta hora. # id:j3_05_tele_mirar
-> DONE

= cartel_mirar
PENSAMIENTO: El Gran Hermano te vigila. Al final del pasillo, también. # id:j3_05_cartel_mirar
-> DONE

= puerta_depto_mirar
PENSAMIENTO: Partes y Cartografía. Mañana, otra vez. # id:j3_05_depto_mirar
-> DONE

= puerta_depto
PENSAMIENTO: La jornada ha terminado. # id:j3_05_depto_usar
-> DONE

= salir
{ jornada == 7:
    { nell_respuesta == "":
        PENSAMIENTO: Primero, la cinta. # id:j7_02_salir_cinta
    - else:
        CARTEL: Esa noche. # fx:negro # id:j7_05_cartel_pasillo # escena:piso_noche # pos:puerta
    }
    -> DONE
}
{ not nell_se_fue:
    PENSAMIENTO: La limpiadora me está mirando. # id:j3_05_salir_no
    -> DONE
}
CARTEL: Esa noche. # fx:negro # id:j3_05_cartel_noche # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== J3.06 — El piso · Noche · Cierre del Acto I
=== j3_noche ===
{ noche_j3_vista:
    -> DONE
}
~ noche_j3_vista = true
PENSAMIENTO: Música marcial en la telepantalla. Por la ventana, el Ministerio de la Paz brilla blanco en la oscuridad. # sfx:fanfarria # id:j3_06_pens_00
{ dp_j3_amory == "recordar":
    PENSAMIENTO: Felix Amory existía. Felix Amory existía. # id:j3_06_recordar_01
    PENSAMIENTO: Si alguien puede dejar de haber existido de un día para otro… # id:j3_06_recordar_02
    PENSAMIENTO: No. El Partido sabe lo que hace. Amory era un traidor. Lo de Pekín… era una señal. El Partido lo vio antes que yo. # esperar:0.6 # id:j3_06_recordar_03
    PENSAMIENTO: Eso es todo. # id:j3_06_recordar_04
- else:
    { duda < 10:
        PENSAMIENTO: Un día largo. Un día raro. Mañana todo estará en su sitio. Siempre lo está. # id:j3_06_aceptar_01
        PENSAMIENTO: Buenas noches, Ivy. Mañana ganaremos más kilómetros. # id:j3_06_aceptar_02
    - else:
        PENSAMIENTO: Un día largo. Mañana todo estará en su sitio. # id:j3_06_aceptar_03
        PENSAMIENTO: ¿Por qué no recuerdo con quién comía los martes? # id:j3_06_aceptar_04
    }
}
{ amory_reaccion == "denuncia":
    PENSAMIENTO: Yo fui a ese despacho. Yo dije su nombre. # id:j3_06_denuncia_01
    PENSAMIENTO: Hice lo correcto. # esperar:1.2 # id:j3_06_denuncia_02
}
PENSAMIENTO: Debería acostarme. # id:j3_06_pens_99
-> DONE

=== j3_ventana ===
PENSAMIENTO: El Ministerio de la Paz brilla blanco en la oscuridad. Desde aquí no se ven las ventanas de la planta catorce. # id:j3_06_ventana
-> DONE

=== j3_dormir ===
PENSAMIENTO: Me acuesto vestid{o}. # fx:negro # id:j3_06_dormir_00
PENSAMIENTO: Muy lejos, el silbido de un cohete. # sfx:silbido # esperar:2.6 # id:j3_06_dormir_01
PENSAMIENTO: Un impacto amortiguado, en otro barrio. No me muevo. # sfx:impacto # id:j3_06_dormir_02
CARTEL: FIN DEL ACTO I # id:j3_06_fin_acto
CARTEL: ACTO II¶LA GRIETA # id:j3_06_acto2
~ jornada = 4
~ desayunado = false
CARTEL: JORNADA 4 # sfx:silbato # id:j3_06_jornada4 # escena:piso # pos:cama
-> DONE
