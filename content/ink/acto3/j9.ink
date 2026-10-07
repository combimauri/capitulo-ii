// ACTO III · JORNADA 9 — La ignorancia es la fuerza (guion: docs/guion-detallado/03-acto-3.md)
// Mensajero en el Miniver: «sigilo social» entre los cubículos, Syme en la cantina, el panel bajo el lavabo
// y el Times original de 1979.

// ==================================================================== J9.01 — El piso · 07:15
=== j9_piso ===
{ gimnasia_j9:
    -> DONE
}
~ gimnasia_j9 = true
PENSAMIENTO: Apenas he dormido. # id:j9_01_pens_00
TELEPANTALLA: ¡Arriba, camaradas! ¡Uno, dos! ¡Uno, dos! # sfx:silbato # id:j9_01_tp_01
{ duda >= 60:
    TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J9-GIMNASIA,expr=entusiasmo,dif=dificil,interferencia=si # id:j9_01_tp_02
- else:
    TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J9-GIMNASIA,expr=entusiasmo,dif=media # id:j9_01_tp_02b
}
{ cf_j9_gimnasia == "fallo":
    ~ sube_sospecha(3)
    TELEPANTALLA: ¡{num} {apellido}! ¡Ese brazo! # id:j9_01_tp_03
}
PENSAMIENTO: Uno, dos. Folkestone. Uno, dos. Kent. # id:j9_01_pens_01
-> DONE

// ==================================================================== J9.02 — Departamento
=== j9_entrar ===
{ depto_j9_visto:
    -> DONE
}
~ depto_j9_visto = true
{ hoja_robada:
    ~ voss_presente = true
    PENSAMIENTO: Voss sale de su despacho. Recorre la sala despacio, mesa por mesa. Se detiene junto a la mía. # refrescar # id:j9_02_pens_00
    VOSS: Anoche alguien entró en la planta once. # esperar:0.8 # id:j9_02_voss_01
    VOSS: Falta un documento. Sin importancia, en realidad. Una hoja vieja. # id:j9_02_voss_02
    VOSS: Pero el Partido no tolera el desorden. ¿Usted no oyó nada, camarada? Trabaja usted hasta tan tarde… # id:j9_02_voss_03
    PROTAGONISTA: No, Subdirector. Me fui a las siete. # cf:id=CF-J9-VOSS,expr=neutral,dif=dificil,golpes=10 # id:j9_02_prot_01
    ~ sube_sospecha(10)
    { cf_j9_voss == "fallo":
        ~ sube_sospecha(10)
        PENSAMIENTO: Me ha mirado la boca. No los ojos: la boca. # id:j9_02_voss_fallo
    }
    PENSAMIENTO: Se aleja. # id:j9_02_pens_01
}
{ llave_ar and not llave_devuelta:
    PELL: Dicen que anoche faltaba una llave en el panel de la once. Que la encontraron en el suelo. # id:j9_02_pell_llave
    ~ sube_sospecha(10)
    PENSAMIENTO: No digo nada. Pell tampoco me mira. # id:j9_02_pens_llave
}
~ voss_presente = true
VOSS: Camarada {apellido}. Hoy hará de mensajero. # refrescar # id:j9_02_voss_04
VOSS: Las cartas corregidas de la ofensiva de mayo deben llegar al Departamento de Registro del Miniver antes de mediodía. En mano. # id:j9_02_voss_05
~ inventario += tubo
PENSAMIENTO: Me entrega un tubo de cartón sellado. # objeto:tubo # id:j9_02_pens_02
VOSS: No se entretenga. # id:j9_02_voss_06
~ voss_presente = false
PENSAMIENTO: El Miniver. Nell dijo que la próxima vez me buscarían ellos. # refrescar # id:j9_02_pens_03
PENSAMIENTO: Al coger el abrigo, un papel doblado en el bolsillo. Letra de imprenta, sin firma. # sfx:papel # id:j9_02_pens_04
~ inventario += times_falso
~ nota_j9 = true
PENSAMIENTO: Dentro del papel, otro papel: el Times de hoy. El de la fecha corregida de la muerte de Ivy. # documento:nota_j9 # objeto:times_falso # id:j9_02_pens_05
PENSAMIENTO: El señuelo. Hay que dejarlo a cambio. # id:j9_02_pens_06
CARTEL: Ministerio de la Verdad. # fx:negro # id:j9_03_cartel # escena:miniver # pos:entrada
-> DONE

// ==================================================================== J9.03 — El Miniver · Departamento de Registro
=== miniver ===

= entrar
{ miniver_visto:
    -> DONE
}
~ miniver_visto = true
PENSAMIENTO: Por fuera, idéntico al Minipax. Por dentro, un ruido constante: tubos neumáticos, máquinas de escribir, altavoces. # fx:aclarar # id:j9_03_pens_00
PENSAMIENTO: Una sala enorme de cubículos de cristal. Cada uno con su máquina, su habla-escribe y tres ranuras. # id:j9_03_pens_01
PENSAMIENTO: Aquí no hay que esconderse. Hay que parecer ocupad{o}. Con la carpeta abierta, leyendo, nadie te mira. # id:j9_03_pens_02
PENSAMIENTO: El que se para, en cambio, busca algo. # id:j9_03_pens_03
-> DONE

= visto
SUPERVISOR: ¿Busca algo, camarada? # id:j9_03_visto_01
PROTAGONISTA: El… el Departamento de Registro. # id:j9_03_visto_02
SUPERVISOR: Está usted en él. Circule. # id:j9_03_visto_03
~ sube_sospecha_sigilo(5)
PENSAMIENTO: Vuelvo sobre mis pasos. Carpeta abierta. Paso firme. # id:j9_03_visto_04
-> DONE

= mostrador
{ tubo_entregado:
    PENSAMIENTO: El tubo ya está entregado. # id:j9_03_mostrador_ya
    -> DONE
}
~ tubo_entregado = true
~ inventario -= tubo
PENSAMIENTO: Entrego el tubo. Una funcionaria firma el recibo sin levantar la vista. # sfx:sello # id:j9_03_mostrador_01
FUNCIONARIA: Firmado. La salida, por donde ha venido. # id:j9_03_func_01
PENSAMIENTO: Los lavabos de la planta tres están al otro lado de la sala. Sin justificación. # id:j9_03_mostrador_02
-> DONE

= mostrador_mirar
PENSAMIENTO: El mostrador de entregas. Un tampón, recibos, una funcionaria. # id:j9_03_mostrador_mirar
-> DONE

= cubiculos_mirar
PENSAMIENTO: Cubículos de cristal. Dentro, gente que dicta en voz baja y mete papeles en ranuras. # id:j9_03_cubiculos
-> DONE

= winston_mirar
{ winston_j9:
    PENSAMIENTO: Smith, encorvado sobre su habla-escribe. # id:j9_03_winston_ya
    -> DONE
}
~ winston_j9 = true
PENSAMIENTO: El vecino del séptimo. Smith. Dicta algo con cara de concentración absoluta. # id:j9_03_winston_01
PENSAMIENTO: Luego mete un papel en el agujero de la memoria con un gesto rapidísimo. # id:j9_03_winston_02
PENSAMIENTO: Así que esto es lo que hace todo el día. # id:j9_03_winston_03
{ duda >= 50:
    PENSAMIENTO: Así que esto es lo que me hicieron a mí. A mi parte. # id:j9_03_winston_d2
}
-> DONE

= julia_mirar
{ julia_j9:
    PENSAMIENTO: La chica de la Liga Anti-Sex. Ya no mira hacia aquí. # id:j9_03_julia_ya
    -> DONE
}
~ julia_j9 = true
PENSAMIENTO: La mujer de la faja escarlata, con un brazo en cabestrillo. Tropieza junto al cubículo de Smith y cae. # id:j9_03_julia_01
PENSAMIENTO: Smith la ayuda a levantarse. Durante un segundo, sus manos se tocan. Ella se aleja. # id:j9_03_julia_02
PENSAMIENTO: Le ha dado algo. Un papel. # esperar:1 # id:j9_03_julia_03
PENSAMIENTO: ¿O me lo he imaginado? # id:j9_03_julia_04
-> DONE

= supervisor_mirar
PENSAMIENTO: Un supervisor. Brazalete rojo. Mira a quien se para. # id:j9_03_supervisor
-> DONE

= ir_escalera
{ not tubo_entregado:
    PENSAMIENTO: Primero, el tubo. En mano. # id:j9_03_escalera_no
    -> DONE
}
PENSAMIENTO: La escalera baja a la cantina. Para subir a la planta tres hay que cruzarla. # id:j9_03_escalera # escena:cantina_miniver # pos:puerta
-> DONE

// ==================================================================== J9.04 — Cantina del Miniver
=== cantina_miniver ===

= entrar
PENSAMIENTO: La cantina del Miniver, abarrotada. Bandejas metálicas, guiso, ginebra. # id:j9_04_pens_00
-> DONE

= syme_mirar
PENSAMIENTO: Pequeño, moreno, gafas y ojos grandes. Habla con entusiasmo a quien quiera oírle. # id:j9_04_syme_mirar
-> DONE

= salir
{ not syme_hablado:
    -> j9_syme
}
PENSAMIENTO: La escalera de la planta tres. # id:j9_04_salir # escena:lavabos # pos:puerta
-> DONE

= gente_mirar
PENSAMIENTO: Nadie levanta la vista del guiso. # id:j9_04_gente
-> DONE

=== j9_syme ===
{ syme_hablado:
    SYME: ¡Colegas, camarada! ¡Colegas! # id:j9_04_syme_otra
    -> DONE
}
~ syme_hablado = true
SYME: ¡Minipax! ¿Cartografía? # id:j9_04_syme_01
PENSAMIENTO: No espera respuesta. # id:j9_04_pens_01
SYME: Siéntese, siéntese un minuto. Estoy trabajando en la undécima edición del Diccionario. ¿Sabe lo que hacemos? Destruimos palabras. Cientos cada día. # id:j9_04_syme_02
SYME: Es precioso. Si no existe la palabra, no existe la idea. # id:j9_04_syme_03
PROTAGONISTA: Lo sé. Un compañero mío decía lo mismo. # id:j9_04_prot_01
SYME: ¡Un hombre sensato! ¿Cómo se llama? Me gustaría conocerle. # id:j9_04_syme_04
* [«Felix Amory.»] # decision:D-J9-SYME
    PENSAMIENTO: Se le borra la sonrisa. Por primera vez. Baja la voz. # id:j9_04_pens_02
    SYME: …No conozco a ningún Amory. # esperar:0.8 # id:j9_04_syme_05
    SYME: Y usted tampoco debería. # id:j9_04_syme_06
    PENSAMIENTO: Se gira hacia otro comensal y sigue hablando como si nada. # id:j9_04_pens_03
    ~ sube_sospecha(3)
    ~ sube_duda(3)
* [«No me acuerdo.»]
    SYME: ¡Ja! Eso es doblepensar del bueno. ¡Excelente! # id:j9_04_syme_07
- SYME: Ustedes en Cartografía también destruyen, ¿sabe? Nosotros, palabras. Ustedes, lugares. Un río que se mueve, un frente que cambia de nombre… # id:j9_04_syme_08
SYME: Somos colegas. # id:j9_04_syme_09
PENSAMIENTO: Habla demasiado. Como Amory. # esperar:0.8 # id:j9_04_pens_04
PENSAMIENTO: No tardará en desaparecer. # id:j9_04_pens_05
-> DONE

// ==================================================================== J9.05 — Lavabos de la planta tres
=== lavabos ===

= entrar
{ lavabos_vistos:
    -> DONE
}
~ lavabos_vistos = true
PENSAMIENTO: Azulejo blanco. Cuatro lavamanos, un espejo largo. # id:j9_05_pens_00
PENSAMIENTO: Sobre la puerta, una telepantalla pequeña. Mira a los lavamanos. # id:j9_05_pens_01
PENSAMIENTO: «Panel bajo el lavabo del fondo.» Justo delante de ella. # id:j9_05_pens_02
-> DONE

= tele_mirar
{ vaho:
    PENSAMIENTO: Empañada. Una mancha gris que zumba. # id:j9_05_tele_vaho
- else:
    PENSAMIENTO: Pequeña, sobre el marco. Sin parpadear. # id:j9_05_tele
}
-> DONE

= espejo_mirar
{ vaho:
    PENSAMIENTO: El espejo, blanco de vaho. Mi cara ya no está. # id:j9_05_espejo_vaho
- else:
    PENSAMIENTO: Mi cara. Ojeras. La boca, quieta. Bien. # id:j9_05_espejo
}
-> DONE

= retretes_mirar
PENSAMIENTO: Tres retretes. Las puertas no llegan al suelo ni al techo. # id:j9_05_retretes
-> DONE

= percha_mirar
PENSAMIENTO: Una percha, justo debajo de la pantalla. # id:j9_05_percha_mirar
-> DONE

= panel_mirar
PENSAMIENTO: Bajo el último lavabo, un panel de madera pintado de blanco. Un tornillo menos que los demás. # id:j9_05_panel_mirar
-> DONE

// Opción A: el vaho del agua caliente empaña el espejo y la pantalla
= grifos
{ vaho:
    PENSAMIENTO: El vapor lo cubre todo. # id:j9_05_grifos_ya
    -> DONE
}
PENSAMIENTO: Si abro el agua caliente, el vaho tardará en subir. Mientras, hay que lavarse las manos. Con calma. # id:j9_05_grifos_01
* [Abrir el agua caliente.] # decision:D-J9-LAVABO
    PENSAMIENTO: El agua sale hirviendo. El espejo empieza a velarse. # cf:id=CF-J9-LAVABO,expr=neutral,dif=media,golpes=10 # id:j9_05_grifos_02
    { cf_j9_lavabo == "fallo":
        ~ sube_sospecha(5)
        TELEPANTALLA: ¿Se encuentra bien, camarada? # id:j9_05_grifos_tele
    }
    ~ vaho = true
    PENSAMIENTO: Veinte segundos. El espejo, blanco. La pantalla, también. # refrescar # id:j9_05_grifos_03
* [Ahora no.]
    PENSAMIENTO: Ahora no. # id:j9_05_grifos_no
- -> DONE

// Opción B: el abrigo en la percha (más rápido, pero alguien entra)
= percha
{ abrigo_colgado:
    PENSAMIENTO: Mi abrigo, justo debajo de la pantalla. # id:j9_05_percha_ya
    -> DONE
}
~ abrigo_colgado = true
PENSAMIENTO: Cuelgo el abrigo en la percha. Tapa media pantalla. # id:j9_05_percha_01
PENSAMIENTO: Se abre la puerta. # sfx:puerta # id:j9_05_percha_02
FUNCIONARIO: Ahí no se cuelga, camarada. # id:j9_05_func_01
~ sube_sospecha(3)
PENSAMIENTO: Se lava las manos y se va sin secárselas. El abrigo se queda. # id:j9_05_percha_03
-> DONE

= panel
{ panel_abierto:
    PENSAMIENTO: El panel está en su sitio. Como si nada. # id:j9_05_panel_ya
    -> DONE
}
{ not vaho and not abrigo_colgado:
    PENSAMIENTO: La telepantalla mira los lavamanos. Así no. # id:j9_05_panel_visto
    -> DONE
}
PENSAMIENTO: Me agacho. El panel se suelta con la uña. Despacio. Muy despacio. # esperar:1.5 # id:j9_05_panel_una
-> cambio

= panel_compas
{ panel_abierto or (not vaho and not abrigo_colgado):
    -> panel
}
PENSAMIENTO: La punta del compás en la rendija. El panel salta. # sfx:tecla # id:j9_05_panel_compas
-> cambio

= cambio
~ panel_abierto = true
~ inventario -= times_falso
~ inventario += sobre_miniver
PENSAMIENTO: Dentro, un sobre de papel encerado. Dejo el Times en su lugar y vuelvo a colocar el panel. # objeto:sobre_miniver # id:j9_05_cambio_01
{ abrigo_colgado:
    PENSAMIENTO: Recojo el abrigo de la percha. # id:j9_05_cambio_abrigo
}
-> DONE

= puerta
{ not panel_abierto:
    PENSAMIENTO: Todavía no. «Llévate lo que hay. Deja lo que traes.» # id:j9_05_puerta_no
    -> DONE
}
-> j9_times

// ==================================================================== J9.06 — El Times original
=== j9_times ===
CARTEL: Un banco, en un parque pequeño. De espaldas a la telepantalla. # fx:negro # musica:ivy # id:j9_06_cartel
PENSAMIENTO: Abro el sobre con cuidado. Dentro hay dos cosas. # sfx:papel # id:j9_06_pens_00
~ inventario -= sobre_miniver
~ inventario += times_original
PENSAMIENTO: Un ejemplar del Times, amarillento. De 1979. # documento:times_1979 # objeto:times_original # id:j9_06_pens_01
PENSAMIENTO: Lo pongo al lado del que llevaba de memoria. # comparar:documento=comparar_times_j9 # id:j9_06_pens_02
{ inventario ? reloj_ivy:
    -> reloj
}
-> pensar

= reloj
PENSAMIENTO: El reloj de Ivy. # id:j9_06_reloj_00
* [Sacarlo y ponerlo junto al periódico.]
    PENSAMIENTO: Las nueve y cuarenta. # esperar:1.2 # id:j9_06_reloj_01
    PENSAMIENTO: El reloj tenía razón. El periódico de hoy, no. # id:j9_06_reloj_02
* [Dejarlo en el bolsillo.]
    PENSAMIENTO: No me hace falta mirarlo. Sé lo que marca. # id:j9_06_reloj_03
- -> pensar

= pensar
PENSAMIENTO: Movieron la fecha un día. Para que coincidiera con la ofensiva. Para que Ivy fuera el motivo. # id:j9_06_pens_03
PENSAMIENTO: «Agentes de la Policía del Pensamiento se presentaron minutos después.» # esperar:1 # id:j9_06_pens_04
PENSAMIENTO: Minutos. ¿Por qué iba la Policía del Pensamiento a un bombardeo? ¿Qué documentos? # esperar:1.4 # id:j9_06_pens_05
PENSAMIENTO: ¿Qué guardabas, Ivy? # id:j9_06_pens_06
~ sube_duda(10)
~ times_original_visto = true
~ diario_times = true
PENSAMIENTO: Debajo del periódico, en el mismo sobre, unas hojas mecanografiadas cosidas con hilo. # id:j9_06_pens_07
// J9.07 — Fragmento II
PENSAMIENTO: «Pero para eso tendrían que saber.» # minijuego:libro,fragmento=2 # id:j9_07_pens_00
~ libro_fragmentos = 2
~ diario_libro_ignorancia = true
~ inventario += libro
PENSAMIENTO: Esta vez me las dejan. Las guardo dentro del mono, contra la piel. # objeto:libro # id:j9_07_pens_01
CARTEL: Esa noche. # fx:negro # id:j9_08_cartel # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== J9.08 — El piso · Noche
=== j9_noche ===
{ noche_j9_vista:
    -> DONE
}
~ noche_j9_vista = true
PENSAMIENTO: El Times de 1979 y el reloj de Ivy. Dos cosas que dicen lo mismo. # id:j9_08_pens_00
-> DONE

=== j9_dormir ===
~ nueva_jornada(10)
~ desayunado = false
CARTEL: JORNADA 10 # fx:negro # sfx:silbato # id:j9_08_jornada10
CARTEL: Semana del Odio. # id:j9_08_fin # escena:piso # pos:cama
-> DONE
