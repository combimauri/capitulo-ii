// ACTO III · JORNADA 8 — La guerra es la paz (guion: docs/guion-detallado/03-acto-3.md)
// La misión del Archivo Restringido: calderas, montacargas, la planta once en cuatro minutos, la Planilla Azul,
// y esa misma noche, la iniciación en el sótano de La Campana.

// ==================================================================== J8.01 — El piso · 07:15
=== j8_piso ===
{ gimnasia_j8:
    -> DONE
}
~ gimnasia_j8 = true
TELEPANTALLA: ¡Arriba, camaradas! ¡Uno, dos! ¡Uno, dos! # sfx:silbato # id:j8_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J8-GIMNASIA,expr=entusiasmo,dif=media,golpes=12,coro=¡Uno!/¡Dos! # id:j8_01_tp_02
{ cf_j8_gimnasia == "fallo":
    ~ sube_sospecha(3)
}
TELEPANTALLA: …la gloriosa ofensiva de mayo en el frente de Malabar ha comenzado. ¡Nuestras tropas avanzan veinte kilómetros en el primer día! # sfx:fanfarria # id:j8_01_tp_03
{
- duda >= 50:
    PENSAMIENTO: Veinte kilómetros de corcho. # id:j8_01_pens_d2
- else:
    PENSAMIENTO: Veinte kilómetros. Desde un frente que en abril no se movió. Porque yo escribí que no se movió. # id:j8_01_pens_d1
    PENSAMIENTO: Porque alguien escribió que yo escribí. # id:j8_01_pens_d1b
}
-> DONE

// ==================================================================== J8.02 — Departamento · Día
=== j8_entrar ===
{ depto_j8_visto:
    -> DONE
}
~ depto_j8_visto = true
PENSAMIENTO: El tubo ya ha escupido los partes de la noche. Dos impactos. Al Libro de Registro. # sfx:tubo # id:j8_02_pens_00
-> DONE

=== j8_libro ===
{ registro_j8_hecho:
    PENSAMIENTO: Dos chinchetas más. El libro está al día. # id:j8_02_libro_hecho
    -> DONE
}
PENSAMIENTO: Bermondsey y Poplar. Esta vez no me sorprende ninguno. # id:j8_02_libro_01
PENSAMIENTO: Dos más. # minijuego:impactos,registro=j8,vars=registro_j8 # id:j8_02_hecho
~ registro_j8_hecho = true
PENSAMIENTO: En pardo, como siempre. Esta noche sabré si estaban escritos antes de caer. # id:j8_02_pens_01
PENSAMIENTO: El tubo silba otra vez. La directiva del día. # sfx:tubo # id:j8_02_pens_02
~ inventario += directiva
~ directiva_leida = true
PENSAMIENTO: Cero tres, cero cinco. La primera rectificación de mayo. # documento:directiva_j8 # objeto:directiva # id:j8_02_pens_03
PENSAMIENTO: Muevo las banderitas veinte kilómetros. Ya ni miro el corcho. # id:j8_02_pens_04
-> DONE

=== j8_salir ===
{ not registro_j8_hecho:
    PENSAMIENTO: Primero el Registro. Dos impactos. # id:j8_02_salir_no
    -> DONE
}
PENSAMIENTO: A la salida, el ascensor. Brooke entra detrás de mí. Estamos solos. # fx:negro # id:j8_02_ascensor_00
BROOKE: Las combinaciones de la planta once cambian cada vez que cambia el frente. # fx:aclarar # id:j8_02_brooke_01
BROOKE: Es lo que dicen. Yo no sé nada. # esperar:1 # id:j8_02_brooke_02
PENSAMIENTO: Se abren las puertas. Sale sin mirar atrás. # id:j8_02_ascensor_01
~ pista_combinacion = true
{ nell_respuesta == "aceptar_tarde":
    CARTEL: Esa noche. Las diez y media. # fx:negro # id:j8_00_cartel # escena:suministros # pos:puerta
- else:
    CARTEL: Esa noche. Las once menos diez. # fx:negro # id:j8_03_cartel # escena:calderas # pos:puerta
}
-> DONE

// ==================================================================== J8.00 — Cuarto de suministros · 22:30 (si dudó una noche)
=== j8_nell ===
{ nell_j8:
    -> DONE
}
~ nell_j8 = true
~ nell_suministros = true
PENSAMIENTO: La limpiadora espera sentada en un cubo vuelto del revés. No se levanta. # refrescar # id:j8_00_pens_00
NELL: Has tardado una noche. # id:j8_00_nell_01
NELL: Mejor una noche que nunca. Toma. # id:j8_00_nell_02
~ inventario += llave_calderas
PENSAMIENTO: Una llave grande y oxidada. # objeto:llave_calderas # id:j8_00_pens_01
NELL: La sala de calderas comunica con el montacargas viejo. El montacargas para en la once. A las once cambia la guardia: cuatro minutos. # id:j8_00_nell_03
NELL: Si te cogen, no me conoces. # id:j8_00_nell_04
~ nell_suministros = false
CARTEL: Las once menos diez. # fx:negro # id:j8_00_cartel_2 # escena:calderas # pos:puerta
-> DONE

// ==================================================================== J8.03 — Sala de calderas · 22:50
=== calderas ===

= entrar
{ j8_salida and not nell_calderas:
    -> j8_nell_calderas
}
{ calderas_vistas:
    -> DONE
}
~ calderas_vistas = true
PENSAMIENTO: La llave abre la puerta de servicio. Abajo hace un calor de horno. # sfx:cerrojo # id:j8_03_pens_00
PENSAMIENTO: Calderas enormes que resoplan. Tuberías por todas partes. Al fondo, el montacargas viejo. # id:j8_03_pens_01
-> DONE

= calderas_mirar
PENSAMIENTO: Aquí abajo hace un calor de horno. # id:j8_03_calderas_01
PENSAMIENTO: Aquí es donde acaba lo que tiramos al agujero de la memoria. # id:j8_03_calderas_02
-> DONE

= rejilla_mirar
PENSAMIENTO: A través de la rejilla se ven papeles ardiendo. Se arrugan, se ennegrecen, suben. # id:j8_03_rejilla_01
{ lapiz_destruido:
    PENSAMIENTO: El lápiz de Amory acabó aquí. # id:j8_03_rejilla_lapiz
- else:
    PENSAMIENTO: El lápiz de Amory acabaría aquí. # id:j8_03_rejilla_lapiz_no
}
-> DONE

= sacos_mirar
PENSAMIENTO: Sacos de carbón. Y papel, mucho papel, esperando turno. # id:j8_03_sacos
-> DONE

= palanca_mirar
PENSAMIENTO: Una palanca de latón, gastada por las manos de alguien que ya no baja aquí. # id:j8_03_palanca_mirar
-> DONE

= puerta
{ j8_salida:
    PENSAMIENTO: Por ahí no. Nell espera. # id:j8_03_puerta_salida
    -> DONE
}
PENSAMIENTO: Podría volver a casa. Nadie lo sabría. # id:j8_03_puerta_01
PENSAMIENTO: Yo lo sabría. # id:j8_03_puerta_02
-> DONE

= montacargas
{ j8_salida:
    PENSAMIENTO: Ya he bajado. No pienso volver a subir. # id:j8_03_montacargas_ya
    -> DONE
}
PENSAMIENTO: La reja chirría al abrirse. Dentro, polvo y una palanca de latón. # sfx:chirrido # id:j8_03_montacargas_01
PENSAMIENTO: Despacio. Sin soltarla. # id:j8_03_montacargas_02
PENSAMIENTO: El montacargas se detiene con un golpe sordo. # minijuego:palanca,resultado=montacargas_j8 # id:j8_03_montacargas_03
{ montacargas_j8 == "chirrido":
    ~ sube_sospecha(5)
    PENSAMIENTO: Ha chirriado. Todo el edificio lo habrá oído. O nadie. # id:j8_03_montacargas_chirrido
}
PENSAMIENTO: Planta once. # id:j8_03_montacargas_04 # escena:planta11 # pos:montacargas
-> DONE

// J8.07 — Nell, entre las calderas
=== j8_nell_calderas ===
~ nell_calderas = true
PENSAMIENTO: Abajo, entre las calderas, una sombra con un carrito. # refrescar # id:j8_07_pens_00
NELL: ¿Lo tienes? # id:j8_07_nell_01
PENSAMIENTO: Asiento. No puedo hablar. # id:j8_07_pens_01
PENSAMIENTO: Me mira a la cara. Mucho rato. # esperar:1.2 # id:j8_07_pens_02
NELL: Ya lo sabes. # id:j8_07_nell_02
NELL: Ven. Esta noche no deberías estar sol{o}. # id:j8_07_nell_03
CARTEL: Limehouse. Medianoche. # fx:negro # id:j8_07_cartel # escena:sotano_pub # pos:mesa
-> DONE

// ==================================================================== J8.04 — Planta once · 23:00
=== planta11 ===

= entrar
{ j8_salida:
    -> vuelta
}
{ planta11_vista:
    -> DONE
}
~ planta11_vista = true
PENSAMIENTO: Las once en punto. Al fondo, el guardia saliente firma en un libro y se marcha por la escalera. # reloj:inicio=23:00:00,limite=240,agotar=planta11.agotado # id:j8_04_pens_00
PENSAMIENTO: El entrante tarda. Cuatro minutos. # id:j8_04_pens_01
PENSAMIENTO: Dos telepantallas. Una, fija, sobre la garita. La otra barre el pasillo cada pocos segundos. # id:j8_04_pens_02
-> DONE

= vuelta
{ planta11_vuelta:
    -> DONE
}
~ planta11_vuelta = true
PENSAMIENTO: El pasillo otra vez. El guardia nuevo hace su ronda. # id:j8_07_pasillo_00
{ llave_ar and not llave_devuelta:
    PENSAMIENTO: La llave. Tengo que devolverla al panel. # id:j8_07_pasillo_01
}
-> DONE

// El reloj llega a 23:04 sin haber entrado: aparece el guardia entrante
= agotado
{ not guardia_entrante:
    ~ guardia_entrante = true
    PENSAMIENTO: Pasos al fondo del pasillo. El guardia entrante. # sfx:alto # refrescar # id:j8_04_agotado_01
    PENSAMIENTO: Esconderme. Detrás del carrito de correo. Ya. # id:j8_04_agotado_02
    ~ sube_sospecha(5)
    PENSAMIENTO: Hará su ronda. Cuando vuelva a la garita, tendré otro minuto y medio. # reloj:mas=90 # id:j8_04_agotado_03
- else:
    PENSAMIENTO: Otra vez tarde. El guardia mira el reloj de la pared. # id:j8_04_agotado_04
    ~ sube_sospecha(5)
    PENSAMIENTO: Respira. Otra vez. # reloj:mas=90 # id:j8_04_agotado_05
}
-> DONE

// Le han visto: ¡Alto! (el motor le devuelve al último punto de control)
= visto
{ guardia_entrante:
    GUARDIA: ¡Alto! ¿Quién anda ahí? # id:j8_04_visto_guardia
- else:
    TELEPANTALLA: ¡Usted! ¡Quédese donde está! # id:j8_04_visto_tele
}
PENSAMIENTO: Corro. Me pego a la pared de la escalera de servicio. Espero. Nadie baja. # id:j8_04_visto_01
~ sube_sospecha_sigilo(10)
PENSAMIENTO: Vuelvo. Más despacio. # id:j8_04_visto_02
-> DONE

= montacargas
{ not j8_salida:
    PENSAMIENTO: Todavía no. He venido a ver un papel. # id:j8_04_montacargas_no
    -> DONE
}
{ llave_ar and not llave_devuelta:
    -> sin_devolver
}
-> bajar

= sin_devolver
PENSAMIENTO: La llave sigue en mi bolsillo. # id:j8_07_bajar_llave
* [Volver a colgarla primero.]
    PENSAMIENTO: Antes, la llave. # id:j8_07_bajar_antes
    -> DONE
* [Bajar así.]
    PENSAMIENTO: Mañana alguien echará de menos una llave. # id:j8_07_bajar_asi
    -> bajar

= bajar
PENSAMIENTO: La palanca, despacio. Abajo, el calor. # fx:negro # id:j8_07_bajar # escena:calderas # pos:montacargas
-> DONE

= extintor_mirar
PENSAMIENTO: Un extintor. La telepantalla que barre no llega hasta aquí. # id:j8_04_extintor
-> DONE

= columna_mirar
PENSAMIENTO: Una columna. Detrás, una franja de sombra. # id:j8_04_columna
-> DONE

= carrito_mirar
PENSAMIENTO: Un carrito de correo con sacas. Cabe una persona detrás, si no respira. # id:j8_04_carrito
-> DONE

= tele_mirar
PENSAMIENTO: Gira sobre un brazo de metal. Mira un lado del pasillo; luego, el otro. # id:j8_04_tele
-> DONE

= tele_garita_mirar
PENSAMIENTO: Fija, sobre la garita. No ve lo que tiene justo debajo. # id:j8_04_tele_garita
-> DONE

= placa_mirar
PENSAMIENTO: «ARCHIVO RESTRINGIDO. SOLO PERSONAL AUTORIZADO DEL PARTIDO INTERIOR.» # id:j8_04_placa
-> DONE

= firmas_mirar
PENSAMIENTO: El libro de firmas. La última, de hace unos minutos. Una letra que se inclina hacia atrás. # id:j8_04_firmas
-> DONE

= ir_escalera
PENSAMIENTO: Por ahí sube el guardia. No. # id:j8_04_escalera
-> DONE

= panel
{ j8_salida:
    { llave_devuelta or not llave_ar:
        PENSAMIENTO: Doce llaves en sus ganchos. # id:j8_07_panel_lleno
    - else:
        ~ llave_devuelta = true
        PENSAMIENTO: Cuelgo la llave en su gancho. «A.R. – 1». Como si nunca se hubiera movido. # sfx:tecla # id:j8_07_panel_devolver
    }
    -> DONE
}
{ llave_ar:
    PENSAMIENTO: Ya tengo la llave. # id:j8_04_panel_ya
    -> DONE
}
PENSAMIENTO: El panel de la garita. Doce llaves, doce etiquetas. # id:j8_04_panel_01
PENSAMIENTO: Me tiemblan las manos. # minijuego:llaves,resultado=cerrojo_j8,vars=llaves_j8 # id:j8_04_panel_02
{ cerrojo_j8 == "tiempo":
    ~ cerrojo_j8 = ""
    -> agotado
}
~ cerrojo_j8 = ""
~ llave_ar = true
PENSAMIENTO: «A.R. – 1». Fría. # id:j8_04_panel_03
-> DONE

= puerta
{ j8_salida:
    PENSAMIENTO: No. Ya he visto bastante. # id:j8_07_puerta
    -> DONE
}
{ not cerrojo_llave:
    { llave_ar:
        ~ cerrojo_llave = true
        PENSAMIENTO: La llave gira. Un cerrojo menos. # sfx:cerrojo # id:j8_04_puerta_llave
    - else:
        PENSAMIENTO: Acero. Un cerrojo de llave y otro de cuatro ruedas numeradas. # id:j8_04_puerta_cerrada
        -> DONE
    }
}
PENSAMIENTO: Cuatro ruedas. Grabado en la placa, muy pequeño: «Código: última rectificación vigente». # id:j8_04_ruedas_01
{ pista_combinacion:
    PENSAMIENTO: «Cambian cada vez que cambia el frente.» La última rectificación… # id:j8_04_ruedas_pista
}
{ cerrojo_intentos >= 1:
    PENSAMIENTO: Una fecha. Una rectificación. Lo he tenido en la mano esta misma mañana. # id:j8_04_ruedas_ayuda
}
PENSAMIENTO: Las ruedas, frías. # minijuego:combinacion,codigo=0305,doc=directiva_j8,item=directiva,resultado=cerrojo_j8 # id:j8_04_ruedas_02
{ cerrojo_j8:
- "abierta":
    -> dentro
- "tiempo":
    ~ cerrojo_j8 = ""
    -> agotado
}
~ cerrojo_intentos += 1
~ cerrojo_j8 = ""
PENSAMIENTO: No. Me aparto. Pensar. # id:j8_04_ruedas_fallo
-> DONE

= dentro
PENSAMIENTO: Clic. La puerta cede. # sfx:cerrojo # reloj:parar # id:j8_04_dentro_01
PENSAMIENTO: Entro. Se cierra sola detrás de mí. # fx:negro # id:j8_04_dentro_02 # escena:archivo_restringido # pos:puerta
-> DONE

// ==================================================================== J8.05 — Archivo Restringido
=== archivo_r ===

= entrar
{ archivo_r_visto:
    -> DONE
}
~ archivo_r_visto = true
PENSAMIENTO: Sin ventanas. Techo bajo. Una sola bombilla con pantalla verde. # fx:aclarar # id:j8_05_pens_00
PENSAMIENTO: Filas de carpetas azules, idénticas, numeradas por semanas. Al fondo, carpetas más viejas, por años. # id:j8_05_pens_01
PENSAMIENTO: No hay telepantalla. # esperar:1 # id:j8_05_pens_02
PENSAMIENTO: Aquí no necesitan vigilar. Aquí nadie entra. # id:j8_05_pens_03
-> DONE

= semana_mirar
PENSAMIENTO: «Semana 18/84.» La semana en curso. # id:j8_05_semana_mirar
-> DONE

= mercado_mirar
PENSAMIENTO: «Semana 16/84. Del 16 al 22 de abril.» # id:j8_05_mercado_mirar
-> DONE

= anios_mirar
PENSAMIENTO: 1975… 1979… 1983. Carpetas más gruesas, con el lomo gastado. # id:j8_05_anios_mirar
-> DONE

= mesa_mirar
PENSAMIENTO: Una mesa de lectura. Un tampón, una lupa. Una silla. Alguien se sienta aquí a leer esto. # id:j8_05_mesa
-> DONE

// J8.06 — La Planilla Azul
= semana
{ planilla_vista:
    PENSAMIENTO: Ya la he leído. Ojalá no. # id:j8_06_ya
    -> DONE
}
PENSAMIENTO: Dentro, hojas de papel azul pálido, mecanografiadas. # sfx:papel # musica:minimor # id:j8_06_pens_00
PENSAMIENTO: Las dos primeras líneas. # documento:planilla_s18 # id:j8_06_pens_01
PENSAMIENTO: Bermondsey, H-10, 01:30. Poplar, K-7, 03:50. Los dos impactos que he registrado esta mañana. # id:j8_06_pens_02
PENSAMIENTO: «Batería cuatro. Folkestone. Kent.» # esperar:0.8 # id:j8_06_pens_03
PENSAMIENTO: Kent está en Oceanía. # esperar:0.8 # id:j8_06_pens_04
PENSAMIENTO: Los cohetes salen de Oceanía. # esperar:1.6 # id:j8_06_pens_05
PENSAMIENTO: «Excluir radio dos kilómetros de edificios ministeriales.» # id:j8_06_pens_06
PENSAMIENTO: «Índice de odio.» # esperar:1.2 # id:j8_06_pens_07
PENSAMIENTO: Nos bombardeamos. Nosotros. A nosotros. # id:j8_06_pens_08
~ sube_duda(20)
~ planilla_vista = true
~ diario_planilla = true
{ patron_conclusion:
- "proles":
    PENSAMIENTO: Lo sabía. Lo sabía desde las chinchetas. Saberlo no sirve para nada. Verlo escrito… # id:j8_06_proles
- "":
    PENSAMIENTO: Las chinchetas. Todas en pardo. Nunca en el centro. # id:j8_06_sin_patron
- else:
    PENSAMIENTO: Cobardes, dije. Casualidad, dije. # id:j8_06_cobardes_01
    PENSAMIENTO: Me río sin sonido, tapándome la boca. Lo dije yo. # id:j8_06_cobardes_02
}
-> DONE

// J8.06-B — La semana del mercado
= semana16
{ mercado_planilla:
    PENSAMIENTO: «Impacto de alta visibilidad.» No hace falta leerlo otra vez. # id:j8_06b_ya
    -> DONE
}
PENSAMIENTO: Semana dieciséis. La del mercado. # documento:planilla_s16 # id:j8_06b_pens_00
PENSAMIENTO: «Hora punta de mercado.» # esperar:1 # id:j8_06b_pens_01
PENSAMIENTO: Sammy. # esperar:1.2 # musica:ruinas # id:j8_06b_pens_02
PENSAMIENTO: Lo escribieron dos días antes. Alguien escribió a máquina «alta visibilidad» y se fue a comer. # id:j8_06b_pens_03
~ sube_duda(5)
~ mercado_planilla = true
~ diario_planilla = true
{ sammy_intento:
    PENSAMIENTO: Corrí hacia él como si se pudiera hacer algo. Estaba escrito a máquina. # id:j8_06b_sammy
}
-> DONE

= anios
{ estante_1979:
    PENSAMIENTO: 1979. No hay tiempo. # id:j8_05_1979_ya
    -> DONE
}
~ estante_1979 = true
PENSAMIENTO: 1979. Alargo la mano. # id:j8_05_1979_01
PENSAMIENTO: Pasos en el pasillo. # sfx:botas # musica:sigilo # id:j8_05_1979_02
PENSAMIENTO: Alguien prueba el picaporte. # esperar:2 # id:j8_05_1979_03
PENSAMIENTO: Un segundo eterno. # esperar:1.5 # id:j8_05_1979_04
PENSAMIENTO: Los pasos se alejan. # id:j8_05_1979_05
PENSAMIENTO: 1979. Otro día. # id:j8_05_1979_06
-> DONE

= salir
{ not planilla_vista:
    PENSAMIENTO: No he subido once plantas para irme sin mirar. # id:j8_05_salir_no
    -> DONE
}
{ prueba_sacada == "":
    -> decidir
}
-> salida

// ◆ D-J8-PLANILLA · ¿Cómo sacar la prueba?
= decidir
PENSAMIENTO: No puedo salir con las manos vacías. Nadie me creería. Yo no me creería. # musica:sigilo # id:j8_06_decidir
* [Copiar a mano lo que me dé tiempo.] # decision:D-J8-PLANILLA
    -> copiar
* {mercado_planilla} [Llevarme la hoja del mercado.]
    ~ hoja_robada = true
    ~ prueba_sacada = "hoja"
    ~ inventario += hoja_planilla
    PENSAMIENTO: La doblo en cuatro. Papel azul. Pesa más que cualquier cosa que haya llevado nunca. # objeto:hoja_planilla # id:j8_06_hoja
    -> salida

= copiar
{ inventario ? lapiz_amory:
    PENSAMIENTO: El lápiz de Amory. Ya sabe el camino. # minijuego:copiar,doc=planilla_s18,lapiz=si,vars=copia # id:j8_06_copiar_lapiz
- else:
    PENSAMIENTO: Un cabo de lápiz de la mesa de lectura. # minijuego:copiar,doc=planilla_s18,vars=copia # id:j8_06_copiar
}
{ copia_lineas > 0:
    ~ prueba_sacada = "copia"
    ~ inventario += copia_planilla
    PENSAMIENTO: Líneas torcidas, a lápiz, deprisa. # objeto:copia_planilla # id:j8_06_copia_hecha
- else:
    ~ prueba_sacada = "nada"
    PENSAMIENTO: No he copiado nada. Solo me queda lo que he visto. # id:j8_06_copia_nada
}
-> salida

// J8.07 — Salida: devolver la llave, esquivar al guardia nuevo y bajar
= salida
~ j8_salida = true
~ guardia_entrante = true
PENSAMIENTO: Salgo. El pasillo otra vez. # fx:negro # id:j8_07_salir # escena:planta11 # pos:archivo
-> DONE

// ==================================================================== J8.08 — Sótano de La Campana · Medianoche
=== sotano ===

= entrar
{ iniciacion_traicion != "":
    -> DONE
}
PENSAMIENTO: Una trampilla detrás de la barra. Una escalera de mano. Abajo huele a cerveza agria y a tierra. # fx:aclarar # id:j8_08_pens_00
PENSAMIENTO: El tabernero baja detrás de nosotros y cierra la trampilla. # sfx:trampilla # id:j8_08_pens_01
NELL: Tom. Tom Barlow. Ya le conoces: te ha servido cerveza. # id:j8_08_nell_00
NELL: Ponla en la mesa. # id:j8_08_nell_01
{ prueba_sacada:
- "hoja":
    PENSAMIENTO: Dejo la hoja azul sobre la madera. # id:j8_08_hoja
- "copia":
    PENSAMIENTO: Dejo las líneas copiadas a lápiz. # id:j8_08_copia
- else:
    PENSAMIENTO: No traigo nada. Solo lo que he visto. # id:j8_08_nada
}
{ prueba_sacada == "hoja" or prueba_sacada == "copia":
    PENSAMIENTO: Barlow lo lee a la luz de la vela y silba bajito. # id:j8_08_pens_02
    BARLOW: Folkestone. Sabía que era Folkestone. Mi cuñado trabajaba en el puerto. Decía que de noche se oían «los ensayos». # id:j8_08_barlow_01
    BARLOW: Lo vaporizaron en el 81. # id:j8_08_barlow_02
}
{ prueba_sacada == "copia":
    BARLOW: A lápiz. Cualquiera podría haberlo escrito. Pero nadie se inventa «Folkestone». # id:j8_08_barlow_copia
}
{ prueba_sacada == "nada":
    NELL: No importa. Lo has visto. Eso no te lo quita nadie. Tampoco te lo creería nadie. # id:j8_08_nell_nada
}
{ inventario ? parte_alterado:
    PENSAMIENTO: Saco también el parte. El de Mysore, con mi firma. # id:j8_08_parte_00
    NELL: «Resistido con firmeza.» Y tu firma. # id:j8_08_nell_parte_01
    PENSAMIENTO: Casi sonríe. # id:j8_08_parte_01
    NELL: Has traído tu propia mentira. Bien. Eso dice más de ti que cualquier juramento. # id:j8_08_nell_parte_02
    ~ nell_confianza += 1
}
NELL: Ahora escúchame. Lo que viene no es una ceremonia. Es una advertencia. # musica:hermandad # id:j8_08_nell_02
NELL: Te voy a hacer unas preguntas. Contesta la verdad. No a mí: a ti. # id:j8_08_nell_03
-> iniciacion

// J8.08-I — La iniciación (cada respuesta se guarda; el ladrillo suelto esconde un micrófono)
= iniciacion
NELL: ¿Estás dispuest{o} a dar tu vida? # id:j8_08i_nell_vida
* [«Sí.»] # decision:D-J8-INICIACION
    ~ iniciacion_vida = "Sí"
* [«No.»]
    ~ iniciacion_vida = "No"
    ~ nell_confianza -= 1
    NELL: Al menos lo sabes. # id:j8_08i_no_vida
- NELL: ¿Estás dispuest{o} a matar? ¿A alguien que no conoces, que quizá no ha hecho nada, si eso sirve a la causa? # id:j8_08i_nell_matar
* [«Sí.»]
    ~ iniciacion_matar = "Sí"
* [«No.»]
    ~ iniciacion_matar = "No"
    ~ nell_confianza -= 1
    NELL: Eso te honra. Y te hace inútil para algunas cosas. # id:j8_08i_no_matar
- NELL: ¿Estás dispuest{o} a mentir, a falsificar, a hacer el trabajo del Partido mejor que nadie para que nadie sospeche, durante años? # id:j8_08i_nell_mentir
* [«Sí.»]
    ~ iniciacion_mentir = "Sí"
* [«No.»]
    ~ iniciacion_mentir = "No"
    ~ nell_confianza -= 1
    NELL: Lo anoto. No con papel. # id:j8_08i_no_mentir
- NELL: ¿Estás dispuest{o} a que la próxima planilla lleve el nombre de un barrio donde vive gente que quieres, y a no avisar a nadie, si avisar nos delata? # id:j8_08i_nell_callar
* [«Sí.»]
    ~ iniciacion_callar = "Sí"
* [«No.»]
    ~ iniciacion_callar = "No"
    ~ nell_confianza -= 1
    NELL: Al menos lo sabes. # id:j8_08i_no_callar
- NELL: ¿Estás dispuest{o} a que tu hermana deje de ser una mártir? ¿A que su cartel siga en la pared y tú sepas que es mentira, cada mañana, durante el resto de tu vida? # id:j8_08i_nell_ivy
* [«Sí.»]
    ~ iniciacion_ivy = "Sí"
* [«No.»]
    ~ iniciacion_ivy = "No"
    ~ nell_confianza -= 1
    NELL: Eso te honra. Y te hace inútil para algunas cosas. # id:j8_08i_no_ivy
- NELL: Y si te cogen, y te cogerán… ¿estás dispuest{o} a traicionarnos? # id:j8_08i_nell_traicion
* [«No.»]
    ~ iniciacion_traicion = "No"
    NELL: Mientes. Todos traicionan. La pregunta es cuándo. # id:j8_08i_trai_no
* [«Sí.»]
    ~ iniciacion_traicion = "Sí"
    NELL: Bien. Es la primera respuesta honesta de la noche. # id:j8_08i_trai_si
- NELL: Aguanta veinticuatro horas. Es todo lo que te pido. # id:j8_08i_24h
NELL: Ya está. No hay carné, no hay contraseña más allá de la canción. No conocerás a más de tres de nosotros. Nunca sabrás cuántos somos. # esperar:0.8 # id:j8_08_nell_04
NELL: Puede que seamos cien. Puede que seamos estos tres. # id:j8_08_nell_05
PROTAGONISTA: ¿Y Goldstein? # id:j8_08_prot_01
BARLOW: Todos preguntan por el viejo. # id:j8_08_barlow_03
NELL: Existe. # esperar:1 # id:j8_08_nell_06
NELL: Y escribió un libro. # id:j8_08_nell_07
PENSAMIENTO: Mete la mano en el hueco de los ladrillos y saca un fajo de hojas mecanografiadas, cosidas con hilo. # id:j8_08_pens_03
NELL: No lo tenemos entero. Nadie lo tiene. Cada célula guarda unas páginas. Si cae una célula, cae un trozo, no el libro. # id:j8_08_nell_08
NELL: Lee esto aquí. No te lo puedes llevar todavía. # id:j8_08_nell_09
// J8.09 — Fragmento I
PENSAMIENTO: «Basta con que el pueblo crea que lo hizo.» # minijuego:libro,fragmento=1 # id:j8_09_pens_00
~ libro_fragmentos = 1
~ diario_libro_guerra = true
PENSAMIENTO: Yo lo creí. Cinco años. Cada mañana. # id:j8_09_pens_01
NELL: El resto, otro día. Si hay otro día. # id:j8_09_nell_01
PENSAMIENTO: Recoge las hojas. Barlow abre la trampilla. Es casi de madrugada. # sfx:trampilla # musica:taberna_lejos # id:j8_09_pens_02
CARTEL: Las tres de la mañana. # fx:negro # id:j8_10_cartel # escena:piso_noche # pos:puerta
-> DONE

= nell_mirar
PENSAMIENTO: Nell. A la luz de la vela parece más joven. O más vieja. # id:j8_08_nell_mirar
-> DONE

= barlow_mirar
PENSAMIENTO: El tabernero de La Campana. Tom Barlow. Manos de estibador. # id:j8_08_barlow_mirar
-> DONE

= hueco_mirar
PENSAMIENTO: Un hueco cuadrado en la pared, tapado con ladrillos sueltos. # id:j8_08_hueco_mirar
-> DONE

= barriles_mirar
PENSAMIENTO: Barriles. Huele a cerveza agria. # id:j8_08_barriles
-> DONE

// ==================================================================== J8.10 — El piso · 03:00
=== j8_noche ===
{ noche_j8_vista:
    -> DONE
}
~ noche_j8_vista = true
PENSAMIENTO: Entro sin encender la luz. La telepantalla emite el himno a volumen nocturno. # id:j8_10_pens_00
-> DONE

=== j8_dormir ===
~ nueva_jornada(9)
~ desayunado = false
CARTEL: JORNADA 9 # fx:negro # sfx:silbato # id:j8_10_jornada9
CARTEL: La ignorancia es la fuerza. # id:j8_10_fin # escena:piso # pos:cama
-> DONE
