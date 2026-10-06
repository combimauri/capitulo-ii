// ACTO II · JORNADA 6 — El parte (guion: docs/guion-detallado/02-acto-2.md)
// Los knots de los escenarios compartidos desvían aquí cuando jornada == 6.

// ==================================================================== J6.01 — El piso · 07:15
=== j6_piso ===
{ gimnasia_j6:
    -> DONE
}
~ gimnasia_j6 = true
TELEPANTALLA: ¡Arriba, camaradas! ¡Más rápido! ¡Uno, dos! ¡Uno, dos! # sfx:silbato # id:j6_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J6-GIMNASIA,expr=entusiasmo,dif=media,golpes=12,coro=¡Uno!/¡Dos! # id:j6_01_tp_02
{ cf_j6_gimnasia == "fallo":
    ~ sube_sospecha(3)
}
TELEPANTALLA: …el balance del cobarde ataque de ayer sobre Limehouse asciende a siete víctimas. El Partido… # cf:id=CF-J6-NOTICIA,expr=duelo,dif=media,golpes=10,coro=¡Muerte!/¡A Eurasia! # id:j6_01_tp_03
{ cf_j6_noticia == "fallo":
    ~ sube_sospecha(3)
}
{
- duda >= 50:
    PENSAMIENTO: Siete. «Retiren eso.» # id:j6_01_pens_d2
- duda >= 20:
    PENSAMIENTO: Siete. Un paréntesis. # id:j6_01_pens_d1
- else:
    PENSAMIENTO: Siete. Siete camaradas. Eurasia pagará. # id:j6_01_pens_d0
}
-> DONE

=== j6_salir_piso ===
# escena:escalera # pos:piso
-> DONE

// ==================================================================== J6.02 — La escalera
=== j6_hilda ===
{ hilda_j6:
    -> DONE
}
PENSAMIENTO: Hilda baja con prisas, con una carpeta bajo el brazo. # id:j6_02_pens_00
HILDA: ¡{nombre}! ¿Te has enterado? Ayer cayó uno en Limehouse. En el mercado. Siete. # id:j6_02_hilda_01
HILDA: Bueno, siete proles. Ya sabes. # id:j6_02_hilda_02
* [«Siete muertos son siete muertos.»] # decision:D-J6-HILDA
    PENSAMIENTO: Se detiene. Me mira con atención. # id:j6_02_pens_01
    HILDA: …Claro. Claro que sí. # id:j6_02_hilda_03
    ~ sube_sospecha(5)
    ~ hilda_aprecio -= 1
    PENSAMIENTO: Anota algo. # id:j6_02_pens_02
* [«Eurasia pagará.»]
    HILDA: ¡Eso es! Este sábado, ensayo del cántico de la efigie. # id:j6_02_hilda_04
* [Callar.]
    { sammy_intento:
        HILDA: ¿Estás bien? Tienes mala cara. ¿Y esa mano? # id:j6_02_hilda_05
        PROTAGONISTA: Me corté. # id:j6_02_prot_01
    - else:
        HILDA: ¿Estás bien? Tienes mala cara. # id:j6_02_hilda_06
    }
- HILDA: ¡Ah! Esta tarde paso por tu piso. Inspección del Comité de la Casa. Rutina, rutina. Que no se diga que el bloque no está listo para la Semana del Odio. # id:j6_02_hilda_07
~ hilda_j6 = true
PENSAMIENTO: Inspección. Esta tarde. # refrescar # id:j6_02_pens_03
{ diario_escondite == "cartel":
    PENSAMIENTO: El cartel de Ivy. # id:j6_02_pens_04
}
-> DONE

=== j6_hilda_otra ===
HILDA: ¡Esta tarde, {nombre}! ¡Inspección! # id:j6_02_hilda_otra
-> DONE

=== j6_bajar ===
CARTEL: Ministerio de la Paz. # fx:negro # id:j6_02_cartel # escena:departamento # pos:puerta
-> DONE

// ==================================================================== J6.03 — El archivo
=== j6_entrar ===
{ depto_j6_visto:
    -> DONE
}
~ depto_j6_visto = true
~ voss_presente = true
VOSS: Camarada {apellido}. Necesito el resumen trimestral del frente de Malabar. Recupere del archivo todos los partes de abril. # refrescar # id:j6_03_voss_01
~ voss_presente = false
CARTEL: Sala de archivo. # fx:negro # id:j6_03_cartel # escena:archivo # pos:puerta
-> DONE

=== archivo ===

= entrar
{ archivo_visto:
    -> DONE
}
~ archivo_visto = true
PENSAMIENTO: Estanterías metálicas. Cajas grises numeradas por fecha. Una mesa de consulta con una lámpara verde. # id:j6_03_pens_00
PENSAMIENTO: Arriba, en un ángulo del techo, una telepantalla pequeña. Gira. # id:j6_03_pens_01
-> DONE

= tele_mirar
PENSAMIENTO: Gira despacio, de un lado a otro. Unos segundos hacia la mesa; otros hacia la puerta. # id:j6_03_tele_mirar
-> DONE

= lampara_mirar
PENSAMIENTO: Una lámpara verde. La única luz cálida de toda la planta. # id:j6_03_lampara
-> DONE

= estanterias_mirar
PENSAMIENTO: Las cajas están mal colocadas. Alguien las ha sacado y vuelto a meter deprisa. # id:j6_03_estanterias_mirar
-> DONE

= estanterias
{ archivo_revisado:
    PENSAMIENTO: Ya tengo los partes de abril. # id:j6_03_estanterias_hecho
    -> DONE
}
-> cajas

= cajas
PENSAMIENTO: «Abril 84 · Malabar.» ¿Cuál es? # id:j6_03_cajas
* [84-03 · MARZO · MALABAR]
    -> mal
* [84-04 · ABRIL · MYSORE]
    -> mal
* [84-40 · ABRIL · MALABAR]
    PENSAMIENTO: Cuarenta. Mal numerada. # id:j6_03_cajas_40
    -> mal
* [84-04 · ABRIL · MALABAR]
    -> partes
* [84-05 · MAYO · MALABAR]
    PENSAMIENTO: Mayo. Todavía no ha llegado mayo. # id:j6_03_cajas_mayo
    -> mal

= mal
PENSAMIENTO: No. Esta no es. # id:j6_03_cajas_mal
-> cajas

= partes
PENSAMIENTO: Dentro, una pila de partes. Los reviso uno por uno. # id:j6_03_partes_00
CARTEL: PARTE N.º 1 · 3.4.84 · MALABAR¶«Avance de 12 km. 3.000 prisioneros.» # id:j6_03_parte_1
CARTEL: PARTE N.º 2 · 8.4.84 · MALABAR¶«Avance de 12 km. Posiciones consolidadas.» # id:j6_03_parte_2
PENSAMIENTO: El tercero es el mío. # id:j6_03_partes_01
{ parte_j1_prisioneros:
- "800":
    ~ prisioneros_j6 = "80"
- "12.000":
    ~ prisioneros_j6 = "1.200"
- else:
    ~ prisioneros_j6 = "300"
}
// la etiqueta va en la línea que se muestra después del comparador (diseño técnico §4.5)
PENSAMIENTO: Pero no dice lo que escribí. # comparar:documento=comparar_parte_j6 # id:j6_03_partes_02
PENSAMIENTO: Esto no es lo que escribí. # esperar:0.8 # id:j6_03_pens_02
PENSAMIENTO: La telepantalla lo leyó. Toda Oceanía lo oyó. {parte_j1_km} kilómetros… «{parte_j1_verbo}»… Yo lo oí en mi propia casa. # id:j6_03_pens_03
PENSAMIENTO: La telepantalla del techo zumba. # sfx:chirrido # id:j6_03_pens_04
PENSAMIENTO: La lámpara verde parpadea. # dp:id=DP-J6-PARTE # id:j6_03_pens_05
{ dp_j6_parte == "aceptar":
    ~ baja_duda(5)
    ~ baja_sospecha(5)
    PENSAMIENTO: «Resistido con firmeza.» Eso escribí. Siempre lo escribí. # id:j6_03_aceptar
- else:
    ~ sube_duda(15)
    ~ diario_parte = true
    PENSAMIENTO: Escribí «{parte_j1_verbo}». Escribí {parte_j1_km} kilómetros. Lo oí. # id:j6_03_recordar
    { diario_iniciado:
        PENSAMIENTO: Lo apuntaré. Esta noche. Cada número. # id:j6_03_recordar_diario
    }
}
~ archivo_revisado = true
~ parte_en_mesa = true
PENSAMIENTO: Dejo el parte sobre la mesa de consulta. El resumen se escribe solo: Malabar resistió en abril. # refrescar # id:j6_03_pens_06
-> DONE

= parte_mirar
PENSAMIENTO: Mi firma, debajo de lo que no escribí. Podría guardármelo… si la telepantalla no mirase. # id:j6_03_parte_mirar
-> DONE

// ◆ D-J6-COPIA (opcional, arriesgada): la telepantalla del techo gira cada cinco segundos
= parte_coger
{ archivo_vigilado:
    ~ sube_sospecha(15)
    ~ parte_en_mesa = false
    PENSAMIENTO: Lo doblo en cuatro. Lo meto dentro del mono. # id:j6_03_copia_vista_01
    VOSS: ¿Encuentra lo que busca, camarada? # id:j6_03_voss_02
    PENSAMIENTO: Voss, en la puerta. ¿Desde cuándo? # id:j6_03_copia_vista_02
    PROTAGONISTA: Estaba… ordenando, Subdirector. # id:j6_03_prot_01
    PENSAMIENTO: Lo devuelvo a la caja. Las manos no me obedecen. # refrescar # id:j6_03_copia_vista_03
- else:
    ~ parte_cogido = true
    ~ prueba_parte = true
    ~ inventario += parte_alterado
    PENSAMIENTO: Ahora no mira. Lo doblo en cuatro y lo meto dentro del mono. # objeto:parte_alterado # refrescar # id:j6_03_copia
}
-> DONE

= salir
{ not archivo_revisado:
    PENSAMIENTO: Primero, los partes de abril. # id:j6_03_salir_no
    -> DONE
}
PENSAMIENTO: Le entrego el resumen trimestral. Voss lo hojea. # id:j6_03_pens_07
VOSS: Correcto. Malabar resistió en abril. Mayo será otra historia. # id:j6_03_voss_03
VOSS: Buen trabajo. # id:j6_03_voss_04
{ foto_a_crane:
    ~ bombilla_encendida = true
    CARTEL: Atardecer. Calle Cable. # fx:negro # id:j6_03_cartel_crane # escena:estudio # pos:puerta
- else:
    CARTEL: Esa tarde. # fx:negro # id:j6_03_cartel_casa # escena:piso_noche # pos:puerta
}
-> DONE

// ==================================================================== J6.04 — Estudio Crane · Atardecer
=== j6_estudio ===
{ estudio_j6_visto:
    -> DONE
}
~ estudio_j6_visto = true
PENSAMIENTO: Crane me espera con un sobre de papel marrón. # id:j6_04_pens_00
CRANE: Tres días, le dije. Han sido dos. No podía dormir. Ábralo. # id:j6_04_crane_01
~ inventario += foto_ivy_restaurada
~ foto_restaurada = true
{ genero == "f":
    PENSAMIENTO: El mismo parque. Los mismos dos niños. Ivy, con el uniforme de los Espías, sonríe abiertamente. Le falta un diente. # objeto:foto_ivy_restaurada # vineta:vineta-foto_ivy_restaurada_m # id:j6_04_pens_01m
- else:
    PENSAMIENTO: El mismo parque. Los mismos dos niños. Ivy, con el uniforme de los Espías, sonríe abiertamente. Le falta un diente. # objeto:foto_ivy_restaurada # vineta:vineta-foto_ivy_restaurada_h # id:j6_04_pens_01
}
PENSAMIENTO: Yo, a su lado, le tiro de una trenza. # id:j6_04_pens_02
PENSAMIENTO: Sonríe. # esperar:1.2 # id:j6_04_pens_03
PENSAMIENTO: En el cartel no sonríe. # vineta:fin # id:j6_04_pens_04
PENSAMIENTO: Esta es su cara. Esta es su nariz. # id:j6_04_pens_05
~ sube_duda(5)
~ diario_ivy = true
CRANE: ¿Es ella? # id:j6_04_crane_02
PROTAGONISTA: Es ella. # id:j6_04_prot_01
PENSAMIENTO: Se sienta frente a mí y sirve dos tazas de té de verdad. Huele distinto. # id:j6_04_pens_06
CRANE: Aquí no hay telepantalla, ¿sabe? Bueno, eso ya lo habrá notado. En este barrio la gente habla. Es lo único que nos queda. # id:j6_04_crane_03
CRANE: Usted parece alguien que tiene muchas cosas dentro. # id:j6_04_crane_04
CRANE: ¿Su hermana era tan… entusiasta como dicen los carteles? # id:j6_04_crane_05
* [«Era una camarada ejemplar.»] # decision:D-J6-CRANE
* [«No lo sé. Ya no sé lo que era.»]
    ~ crane_info += 1
    ~ sube_sospecha(5)
- CRANE: Ayer estuvo usted en el mercado, ¿verdad? Lo siento mucho por el niño de Dot. # id:j6_04_crane_06
* [«Fue un ataque euroasiático.»]
* [«Ese cohete… no debería haber caído ahí.»]
    ~ crane_info += 1
    ~ sube_sospecha(5)
- CRANE: Si alguna vez necesita un sitio donde pensar en voz alta… mi trastienda está siempre abierta. # id:j6_04_crane_07
* [«Gracias. No será necesario.»]
* [«Puede que lo necesite.»]
    ~ crane_info += 1
    ~ sube_sospecha(3)
    ~ crane_trastienda = true
- CRANE: Cuando quiera, camarada. Aquí las caras esperan. # id:j6_04_crane_08
-> DONE

=== j6_recorte_mirar ===
PENSAMIENTO: Un recorte del Times de marzo de 1984: «La ración de chocolate se mantiene en 30 gramos semanales, gracias a la gestión de la Minindancia.» # id:j6_04_recorte_01
{ not chocolate_visto:
    ~ chocolate_visto = true
    ~ sube_duda(5)
    ~ diario_chocolate = true
}
PENSAMIENTO: Treinta gramos. En marzo. # esperar:1 # id:j6_04_recorte_02
PENSAMIENTO: Y hace unos días la telepantalla dijo que «aumentaba» a veinte. # id:j6_04_recorte_03
-> DONE

=== j6_recorte_usar ===
CRANE: Ese no, camarada. Es de mi colección. # id:j6_04_recorte_usar
PENSAMIENTO: Lo ha dicho sin girarse. # id:j6_04_recorte_usar_2
-> DONE

// ==================================================================== J6.05 — El piso · La inspección de Hilda
=== j6_noche ===
{ inspeccion_hecha:
    -> DONE
}
~ inspeccion_hecha = true
PENSAMIENTO: Apenas cierro la puerta, llaman. Tres golpes secos. # sfx:golpes # id:j6_05_pens_00
HILDA: ¡Inspección del Comité, {nombre}! ¡Abre, que vengo cargada! # id:j6_05_hilda_01
{ inventario ? diario or inventario ? parte_alterado:
    -> esconder
}
-> j6_inspeccion

= esconder
PENSAMIENTO: Abro la puerta. # minijuego:esconder,vars=escondite_j6 # id:j6_05_abrir
{ escondite_j6_diario:
- "cartel":
    ~ diario_escondite = "cartel"
- "hornillo":
    ~ diario_escondite = "hornillo"
    ~ diario_hollin = true
}
{ inventario ? diario and escondite_j6_diario != "cartel" and escondite_j6_diario != "hornillo":
    -> j6_descubierto
}
-> j6_parte_visto

=== j6_descubierto ===
{
- escondite_j6_diario == "colchon":
    PENSAMIENTO: Hilda se sienta en la cama para apuntar. Nota el bulto. # id:j6_05_colchon
- escondite_j6_diario == "cajon":
    HILDA: A ver ese cajón, que hay gente que guarda propaganda vieja. # id:j6_05_cajon
- else:
    PENSAMIENTO: El cuaderno sigue en mi mano cuando Hilda entra. # id:j6_05_mano
}
PENSAMIENTO: Lo hojea. # id:j6_05_hojea
{ hilda_aprecio >= 2:
    { diario_iniciado:
        HILDA: ¿Qué es esto? ¿Estás escribiendo una novela? ¿Para el Departamento de Ficción? # id:j6_05_hilda_02
    - else:
        HILDA: Un cuaderno de antes. En blanco. ¿Para qué quieres tú esto? # id:j6_05_hilda_03
    }
    PROTAGONISTA: …Ejercicios. Para el comité de la Semana del Odio. Lemas. # id:j6_05_prot_01
    HILDA: …Mucho cuidado con los cuadernos, {nombre}. A la gente le da por escribir y luego… # id:j6_05_hilda_04
    ~ sube_sospecha(15)
    ~ hilda_aprecio = 0
- else:
    HILDA: Esto me lo llevo. Lo revisará el Comité. # id:j6_05_hilda_05
    ~ sube_sospecha(25)
    ~ inventario -= diario
    ~ diario_confiscado = true
    ~ comite_leyo = true
    ~ diario_escondite = "comite"
    PENSAMIENTO: Se lo guarda bajo el brazo. # id:j6_05_pens_01
}
-> j6_parte_visto

=== j6_parte_visto ===
{ inventario ? parte_alterado and escondite_j6_parte != "cartel" and escondite_j6_parte != "hornillo":
    HILDA: ¿Y este papel con sello? Esto es del Ministerio. # id:j6_05_parte_01
    ~ sube_sospecha(10)
    ~ inventario -= parte_alterado
    ~ prueba_parte = false
    PENSAMIENTO: Se lo queda. No dice nada más. # id:j6_05_parte_02
}
-> j6_inspeccion

=== j6_inspeccion ===
HILDA: Telepantalla en funcionamiento… sí. Retrato del Gran Hermano… sí. Volumen adecuado… sí. # id:j6_05_hilda_06
PENSAMIENTO: Se para delante del cartel de Ivy. # id:j6_05_pens_02
HILDA: Ay, qué preciosidad. Está un poco torcido. # id:j6_05_hilda_07
PENSAMIENTO: Alarga la mano. # id:j6_05_pens_03
{ diario_escondite == "cartel":
    -> cartel
}
HILDA: …Ya está. Perfecto. # id:j6_05_hilda_08
-> despedida

// ◆ D-J6-CARTEL
= cartel
* [«¡No! No lo toque, por favor. Lo pegué yo. Con mis manos. Es lo único que me queda.»] # decision:D-J6-CARTEL
    HILDA: Ay, {nombre}… Claro, claro. Perdona. # id:j6_05_hilda_09
    PENSAMIENTO: Se emociona. Retira la mano. # id:j6_05_pens_04
    { hilda_aprecio >= 1:
        ~ hilda_aprecio += 1
    }
* [No decir nada.]
    PENSAMIENTO: Endereza el cartel con cuidado. Se oye un leve roce de papel. # id:j6_05_pens_05
    HILDA: …Ya está. Perfecto. # esperar:1 # id:j6_05_hilda_10
    ~ sube_sospecha(5)
- -> despedida

= despedida
HILDA: Por cierto. # id:j6_05_hilda_11
HILDA: Me han dicho que te vieron en Limehouse. Dos veces. No es asunto mío, claro. Pero la gente habla. Y yo apunto. # id:j6_05_hilda_12
{ visita_prole_j4 and foto_a_crane:
    ~ sube_sospecha(5)
}
PENSAMIENTO: Se va. Me quedo apoyad{o} en la puerta. # id:j6_05_pens_06
-> DONE

// El diario, otra noche (J6 y J7): desde el hueco, una entrada por noche
=== j6_hueco ===
{ diario_confiscado:
    PENSAMIENTO: El cuaderno lo tiene el Comité. # id:j6_05_hueco_sin
    -> DONE
}
{ diario_escrito_hoy == jornada:
    PENSAMIENTO: Ya he escrito esta noche. # id:j6_05_hueco_ya
    -> DONE
}
PENSAMIENTO: El hueco entre el armario y la pared. Aquí no llega. # id:j6_05_hueco_01
* [Escribir.]
    ~ temp antes = diario_entradas
    { jornada:
    - 6:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=20 de abril # id:j6_05_cerrar
    - 7:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=21 de abril # id:j7_cerrar
    - 8:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=4 de mayo # id:j8_cerrar
    - 9:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=4 de mayo # id:j9_cerrar
    - 10:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=6 de mayo # id:j10_cerrar
    - else:
        PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=7 de mayo # id:j11_cerrar
    }
    { diario_entradas > antes:
        ~ diario_iniciado = true
        ~ diario_escrito_hoy = jornada
        PENSAMIENTO: 1984. Creo. # id:j6_05_anio
    }
* [Ahora no.]
    PENSAMIENTO: Ahora no. # id:j6_05_ahora_no
-
{ jornada == 11 and not fragmento_4:
    -> j11_fragmento ->
}
{ diario_escondite == "hornillo" or cartel_arrancado:
    ~ diario_escondite = "hornillo"
    PENSAMIENTO: Lo vuelvo a meter en el hornillo. Huele a hollín. # id:j6_05_esconder_hornillo
- else:
    ~ diario_escondite = "cartel"
    PENSAMIENTO: Lo vuelvo a esconder detrás del cartel de Ivy. # id:j6_05_esconder
}
-> DONE

=== j6_dormir ===
~ jornada = 7
~ desayunado = false
CARTEL: JORNADA 7 # fx:negro # sfx:silbato # id:j6_05_jornada7
CARTEL: Jornada 7. # id:j6_05_fin # escena:piso # pos:cama
-> DONE
