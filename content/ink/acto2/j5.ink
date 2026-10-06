// ACTO II · JORNADA 5 — El mercado (guion: docs/guion-detallado/02-acto-2.md)
// Los knots de los escenarios compartidos desvían aquí cuando jornada == 5.

// ==================================================================== J5.01 — El piso · 06:40
=== j5_piso ===
{ despertar_j5:
    -> DONE
}
~ despertar_j5 = true
PENSAMIENTO: Antes del silbato. No he dormido. # id:j5_01_pens_00
{ inventario ? tarjeta_crane and inventario ? foto_ivy:
    PENSAMIENTO: El estudio de la calle Cable abre a las siete. Me da tiempo antes del Minipax si voy por el mercado. # id:j5_01_pens_01
- else:
    PENSAMIENTO: Bajo la puerta hay un periódico doblado, el Times de la comunidad que reparte Hilda. En la última página, un anuncio pequeño. # id:j5_01_pens_02
    CARTEL: ESTUDIO CRANE · Calle Cable, 7¶Se restauran fotografías antiguas.¶Recuerdos que el tiempo borra. # id:j5_01_anuncio
    { inventario ? foto_ivy:
        PENSAMIENTO: Restaurar… Me da tiempo antes del Minipax si voy por el mercado. # id:j5_01_pens_03
    - else:
        PENSAMIENTO: Restaurar… La foto de Ivy sigue en el cajón. # id:j5_01_pens_04
    }
}
-> DONE

=== j5_salir_piso ===
{ not (inventario ? foto_ivy):
    -> sin_foto
}
* [Llevar la foto a Crane.] # decision:D-J5-FOTO
    ~ foto_a_crane = true
    CARTEL: Mercado de Watney Street. 07:45. # fx:negro # id:j5_01_cartel_foto # escena:mercado # pos:inicio
    -> DONE
* [No llevarla.]
    -> sin_foto
= sin_foto
CARTEL: AVENIDA DE LA VICTORIA CERRADA POR REFORMAS. # fx:negro # id:j5_01_reformas
CARTEL: Mercado de Watney Street. 07:45. # id:j5_01_cartel # escena:mercado # pos:inicio
-> DONE

// ==================================================================== J5.02 — Mercado de Watney Street
=== mercado ===

= entrar
{
- not mercado_visto:
    ~ mercado_visto = true
    PENSAMIENTO: Puestos de madera con toldos remendados. Patatas, retales, cacharros, cuchillas de afeitar usadas. Mucha gente. # id:j5_02_pens_00
    PENSAMIENTO: En un puesto, la mujer del pañuelo dobla telas y tararea una canción de amor vieja y pegadiza. # id:j5_02_pens_01
- estudio_visto and not cohete_caido:
    PENSAMIENTO: El mercado está más lleno. Sammy sigue en el bordillo. Dot canta. # id:j5_04_pens_00
}
-> DONE

= dot_mirar
PENSAMIENTO: Dobla telas y canta. La letra no se entiende; la melodía se queda pegada. # id:j5_02_dot_mirar
-> DONE

= dot
{
- not dot_hablado:
    DOT: ¿Retales, camarada? ¿No? Pues no estorbe. # id:j5_02_dot_00
- dot_confianza >= 1:
    DOT: ¡Mira quién vuelve! {El} de azul que dice «lo siento». # id:j5_02_dot_01
    DOT: ¿Retales? Tengo uno con flores. Ilegal no es, pero casi. # id:j5_02_dot_02
- else:
    DOT: ¿Otra verificación? # id:j5_02_dot_03
}
-> DONE

= sammy_mirar
PENSAMIENTO: Sentado en el bordillo, ordena su colección de metralla en filas. # id:j5_02_sammy_mirar
-> DONE

= sammy
SAMMY: ¡Ochenta y cuatro! Anoche cayó uno en el muelle y Billy Hogan llegó tarde. # id:j5_02_sammy_01
SAMMY: Este es el mejor. Parece plata. # id:j5_02_sammy_02
-> DONE

= cordones_mirar
PENSAMIENTO: Cordones de zapatos. Los vende un viejo con un solo ojo. # id:j5_02_cordones
-> DONE

= patatas_mirar
PENSAMIENTO: Patatas pequeñas, con tierra todavía. Más baratas que en el economato. # id:j5_02_patatas
-> DONE

= gente_mirar
PENSAMIENTO: Gente con prisa, con cestas, con niños. Nadie mira a nadie a los ojos, pero todos hablan. # id:j5_02_gente
-> DONE

= estudio_mirar
PENSAMIENTO: El escaparate del Estudio Crane. Fotos de bodas, de niños, de viejos. Ni un cartel. # id:j5_02_estudio_mirar
-> DONE

= ir_estudio
{ estudio_visto:
    PENSAMIENTO: Ya he estado. Llego tarde al Minipax. # id:j5_02_estudio_ya
    -> DONE
}
# escena:estudio # pos:puerta
-> DONE

= salir
{ not estudio_visto:
    PENSAMIENTO: El estudio de Crane está al fondo de la calle. # id:j5_02_salir_no
    -> DONE
}
-> DONE

// ==================================================================== J5.04 — El cohete
= cohete
~ cohete_caido = true
PENSAMIENTO: Un silbido. Lejano al principio. Agudo. Creciente. # id:j5_04_pens_01
PENSAMIENTO: El mismo silbido de la calle Stepney. # id:j5_04_pens_02
PENSAMIENTO: La gente se tira al suelo. Alguien grita: «¡Al suelo!». Dot levanta la cabeza buscando a Sammy. # id:j5_04_pens_03
PENSAMIENTO: Sammy, en mitad de la calzada, se ha agachado a recoger un trozo de metralla brillante. Está de espaldas. No oye nada. # id:j5_04_pens_04
// la etiqueta va en la línea que se muestra después de la secuencia (diseño técnico §4.5)
PENSAMIENTO: Silencio. Solo un pitido agudo. # minijuego:sammy,resultado=sammy_j5 # id:j5_04_pens_05
{ sammy_j5 == "correr":
    ~ sammy_intento = true
    ~ sube_duda(10)
    ~ sube_sospecha(8)
    PENSAMIENTO: Mis dedos rozaron su camisa. # id:j5_04_correr # escena:mercado_ruinas # pos:calzada
- else:
    ~ sube_duda(5)
    { sammy_j5 == "paralizado":
        PENSAMIENTO: No me he movido. No me he movido. # id:j5_04_paralizado # escena:mercado_ruinas # pos:puesto
    - else:
        PENSAMIENTO: Detrás del puesto de patatas. Las manos sobre la cabeza. # id:j5_04_cubierto # escena:mercado_ruinas # pos:puesto
    }
}
-> DONE

// ==================================================================== J5.03 — Estudio Crane
=== estudio ===

= entrar
{ jornada == 6:
    -> j6_estudio
}
{ jornada == 12:
    -> j12_estudio
}
{ estudio_visto:
    -> DONE
}
~ estudio_visto = true
CRANE: ¡Camarada! Qué alegría. Pase, pase. Aún no he encendido la estufa, perdone el frío. # id:j5_03_crane_01
{ foto_a_crane:
    ~ inventario -= foto_ivy
    PENSAMIENTO: Le doy la foto. La sujeta por los bordes, con mucha delicadeza, y la examina con una lupa. # id:j5_03_pens_00
    CRANE: Agua y fuego. Lo peor para una fotografía. # id:j5_03_crane_02
    CRANE: Pero la cara está ahí. Debajo de la mancha, la cara siempre sigue ahí. Deme tres días. # id:j5_03_crane_03
    PROTAGONISTA: ¿Por qué hace esto? # id:j5_03_prot_01
    CRANE: Porque en esta ciudad todo se olvida muy rápido, camarada. Alguien tiene que recordar. # id:j5_03_crane_04
    CRANE: ¿Cómo se llamaba? # id:j5_03_crane_05
    PROTAGONISTA: Ivy. # id:j5_03_prot_02
    CRANE: Ivy. Bonito nombre. # id:j5_03_crane_06
    PENSAMIENTO: Lo apunta en un sobre. Sin girarse, como de pasada: # id:j5_03_pens_01
    CRANE: ¿Y cómo era Ivy? Quiero decir… ¿qué le gustaba? # id:j5_03_crane_07
    -> prueba
}
CRANE: ¿No me trae la foto? Es una pena. Bueno, la oferta sigue en pie. Las caras esperan. # id:j5_03_crane_08
CRANE: Le invitaría a un té, pero llegará tarde a su ministerio. # id:j5_03_crane_09
-> DONE

= prueba
* [«Era una buena camarada. Leal.»] # decision:D-J5-CRANE
    CRANE: Claro, claro. # id:j5_03_crane_10
* [«Cantaba todo el tiempo. Canciones viejas.»]
    CRANE: ¿Ah, sí? ¿Cuáles? # id:j5_03_crane_11
    ** [«Naranjas y limones.»]
        ~ crane_info += 1
        ~ sube_sospecha(3)
        PENSAMIENTO: Anota algo, sonriendo. # id:j5_03_pens_02
        CRANE: La conozco. Las campanas de San Clemente. Ya no quedan campanas. # id:j5_03_crane_12
    ** [«No me acuerdo.»]
        CRANE: Las canciones se olvidan. Como todo. # id:j5_03_crane_13
* [«No quiero hablar de ella.»]
    CRANE: Por supuesto. Perdone. # id:j5_03_crane_14
- -> DONE

= crane
{ jornada == 12:
    -> j12_crane
}
{ jornada == 6:
    CRANE: Llévesela. Es suya. Las caras vuelven a quien las quiere. # id:j6_04_crane_despues
    -> DONE
}
{ foto_a_crane:
    CRANE: Tres días. La cara de Ivy, como nueva. # id:j5_03_crane_despues
- else:
    CRANE: Las caras esperan, camarada. # id:j5_03_crane_despues_2
}
-> DONE

= crane_mirar
PENSAMIENTO: En mangas de camisa. Manos de dedos finos, manchados de química. # id:j5_03_crane_mirar
-> DONE

= fotos_mirar
PENSAMIENTO: Bodas. Niños. Una anciana con un gato. Ningún cartel, ninguna consigna. Solo caras. # id:j5_03_fotos_01
PENSAMIENTO: En una, al fondo de una boda prole, una mujer joven… ¿Esa no es Brooke? # id:j5_03_fotos_02
PENSAMIENTO: No. No puede ser. # id:j5_03_fotos_03
-> DONE

= cuarto_mirar
{ bombilla_encendida:
    PENSAMIENTO: La bombilla roja de encima está encendida. Hay alguien trabajando ahí dentro. ¿O es una máquina? Se oye un zumbido. # id:j6_04_cuarto_mirar
    -> DONE
}
PENSAMIENTO: «Cuarto oscuro. No entrar.» Encima, una bombilla roja, apagada. # id:j5_03_cuarto_mirar
-> DONE

= cuarto
CRANE: Ahí no, camarada. La luz estropea el trabajo de semanas. # id:j5_03_cuarto
-> DONE

= camara_mirar
PENSAMIENTO: Una cámara antigua. De antes de la Revolución. ¿Cómo la conserva? # id:j5_03_camara
-> DONE

= fondos_mirar
PENSAMIENTO: Un jardín pintado. Una playa pintada. Para hacerse fotos en sitios donde nunca se ha estado. # id:j5_03_fondos
-> DONE

= salir
{ jornada == 6:
    CARTEL: Esa tarde. # fx:negro # id:j6_04_cartel # escena:piso_noche # pos:puerta
    -> DONE
}
# escena:mercado # pos:estudio
-> DONE

// ==================================================================== J5.05 — Después
=== ruinas ===

= entrar
{ ruinas_vistas:
    -> DONE
}
~ ruinas_vistas = true
PENSAMIENTO: Me levanto. Polvo. Toldos ardiendo. Gritos ahogados por el pitido. # sfx:pitido # id:j5_05_pens_00
PENSAMIENTO: El sonido vuelve poco a poco. # id:j5_05_pens_01
PENSAMIENTO: En mitad de la calzada, Dot, cubierta de polvo y con una brecha en la frente, de rodillas. Abraza algo pequeño. # id:j5_05_pens_02
DOT: Sammy. Sammy. Sammy. Sammy. # id:j5_05_dot_01
{ sammy_intento:
    ~ dot_confianza += 2
    PENSAMIENTO: Levanta la vista. Me ve: el mono roto en el brazo, sangre en la mano. Me mira largo. # id:j5_05_pens_03
    PENSAMIENTO: No dice nada. Asiente una vez. Casi nada. # id:j5_05_pens_04
- else:
    ~ dot_confianza = 0
    PENSAMIENTO: Levanta la vista. Me ve de pie, intact{o}, detrás del puesto de patatas. Me mira largo. # id:j5_05_pens_05
    PENSAMIENTO: Aparta la vista. # id:j5_05_pens_06
}
~ patrulla_llega = true
PENSAMIENTO: Llega una patrulla del Partido: hombres de uniforme negro y un oficial. # refrescar # id:j5_05_pens_07
OFICIAL: Despejen la zona. Circulen. # id:j5_05_oficial_01
PENSAMIENTO: Ve a Dot. Hace un gesto a sus hombres, sin mirar. # id:j5_05_pens_08
OFICIAL: Retiren eso. # id:j5_05_oficial_02
PROTAGONISTA: Es un niño. # id:j5_05_prot_01
OFICIAL: ¿Es usted del Partido, camarada? Entonces no tiene nada que hacer aquí. Circule. # id:j5_05_oficial_03
~ diario_sammy = true
PENSAMIENTO: A Ivy le hicieron un cartel. «Esta camarada es ahora una mártir del Partido.» # id:j5_05_pens_09
PENSAMIENTO: A Sammy le han dicho «eso». «Retiren eso.» # esperar:1.2 # id:j5_05_pens_10
-> DONE

= dot_mirar
PENSAMIENTO: No grita. Repite su nombre, muy bajo. # id:j5_05_dot_mirar
-> DONE

= dot
PENSAMIENTO: No me oye. No oye a nadie. # id:j5_05_dot_hablar
-> DONE

= oficial_mirar
PENSAMIENTO: Botas limpias. Ni una mota de polvo. # id:j5_05_oficial_mirar
-> DONE

= patrulla_mirar
PENSAMIENTO: Uniformes negros. Recogen sin mirar lo que recogen. # id:j5_05_patrulla_mirar
-> DONE

= metralla_mirar
PENSAMIENTO: Un trozo de metralla brillante. El que Sammy se agachó a recoger. # id:j5_05_metralla_mirar
-> DONE

= metralla
~ metralla_brillante_cogida = true
~ inventario += metralla_brillante
PENSAMIENTO: «Parece plata.» # objeto:metralla_brillante # refrescar # id:j5_05_metralla
-> DONE

= salir
CARTEL: 09:20. # fx:negro # id:j5_05_cartel # escena:departamento # pos:puerta
-> DONE

// ==================================================================== J5.06 — Departamento · Tarde
=== j5_entrar ===
{ depto_j5_visto:
    -> DONE
}
~ depto_j5_visto = true
~ voss_espera = true
PENSAMIENTO: Llego con la mano vendada con un pañuelo. Voss está de pie junto a mi mesa. # refrescar # id:j5_06_pens_00
VOSS: Una hora y veinte minutos, camarada {apellido}. # id:j5_06_voss_01
* [«Estaba en el mercado de Watney Street. Cuando cayó el cohete.»] # decision:D-J5-RETRASO
    VOSS: Qué… coincidencia. ¿Y qué hacía usted en Limehouse a las ocho de la mañana? # id:j5_06_voss_02
    ** [«Un atajo. La avenida está en obras.»]
        VOSS: Ya. # id:j5_06_voss_03
    ** [«Verificación para el Registro.»]
        VOSS: Qué celo. Entonces sabrá registrarlo bien. # id:j5_06_voss_04
    --
    ~ sube_sospecha(3)
* [«Me encontraba mal, Subdirector. El estómago.»]
    PENSAMIENTO: Mira el pañuelo ensangrentado de mi mano. # id:j5_06_pens_01
    VOSS: Ya veo. # id:j5_06_voss_05
    ~ sube_sospecha(6)
    { sammy_intento:
        VOSS: Curioso. La patrulla de Limehouse ha informado de un miembro del Partido que corría por el mercado. Corría hacia el impacto. # id:j5_06_voss_06
        ~ sube_sospecha(4)
    }
- VOSS: Tiene partes pendientes. Uno de ellos le resultará familiar. # id:j5_06_voss_07
~ voss_espera = false
PENSAMIENTO: Se aleja. # refrescar # id:j5_06_pens_02
-> DONE

// ==================================================================== J5.07 — El registro · El patrón
=== j5_libro ===
{ registro_j5_hecho:
    PENSAMIENTO: El libro está al día. # id:j5_07_libro_hecho
    -> DONE
}
PENSAMIENTO: En la mesa del Registro, varios cilindros. Uno de ellos: # sfx:tubo # id:j5_07_pens_00
CARTEL: def.civil · impacto · 19.4.84 · 08:12¶distrito: limehouse · mercado watney st · cuadr: J-8¶bajas: 7 (proles) # id:j5_07_parte
PENSAMIENTO: Siete. «Proles.» Entre paréntesis. # id:j5_07_pens_01
PENSAMIENTO: Sammy es un paréntesis. # esperar:1.2 # id:j5_07_pens_02
{ not (inventario ? zonificacion):
    PENSAMIENTO: «¿Por qué nunca en el centro?» Abro el cajón con rabia. El fieltro está despegado por una esquina. # id:j5_07_cajon
    ~ inventario += zonificacion
    ~ inventario += nota_amory
    ~ zonificacion_encontrada = true
    ~ fieltro_levantado = true
    ~ cajon_abierto = true
    ~ diario_amory = true
    PENSAMIENTO: Una lámina transparente. Y una nota con un pájaro. # objeto:zonificacion # id:j5_07_cajon_2
}
{ not (inventario ? compas):
    ~ inventario += compas
}
PENSAMIENTO: {ilegible_completado:Once|Diez} chinchetas. # minijuego:impactos,registro=j5,guiado=si,ilegible=J-8,vars=registro_j5 # id:j5_07_pens_03
~ registro_j5_hecho = true
-> j5_deduccion

// ◆ D-J5-PATRON · Tablero de deducción
=== j5_deduccion ===
PENSAMIENTO: Ninguno a menos de dos kilómetros de un ministerio. Ninguno en un distrito del Partido. ¿Con qué me quedo? # id:j5_07_pens_04
* [«Los cohetes solo caen sobre los proles.»] # decision:D-J5-PATRON
    ~ patron_conclusion = "proles"
    ~ sube_duda(10)
    ~ diario_cohetes = true
    PENSAMIENTO: {ilegible_completado:Once de once|Diez de diez}. Ninguno a menos de dos kilómetros de un ministerio. Ninguno en un distrito del Partido. # id:j5_07_proles_01
    PENSAMIENTO: Eurasia tiene cohetes que cruzan el mar… y nunca, ni una sola vez, se equivoca de barrio. # id:j5_07_proles_02
* [«Eurasia es cobarde: ataca a los débiles.»]
    ~ patron_conclusion = "cobardes"
    ~ sube_duda(3)
    ~ diario_cohetes = true
    PENSAMIENTO: Cobardes. Atacan donde no hay defensas. Donde más duele. Es lo que harían ellos. # id:j5_07_cobardes_01
    PENSAMIENTO: Es lo que harían… # esperar:1 # id:j5_07_cobardes_02
    { inventario ? nota_amory:
        PENSAMIENTO: Miro la nota de Amory. Es lo que harían. # id:j5_07_cobardes_03
    }
* [«Es casualidad. Once impactos no son nada.»]
    ~ patron_conclusion = "casualidad"
    ~ baja_sospecha(3)
    PENSAMIENTO: Casualidad. El azar. Las chinchetas no son una estadística. # id:j5_07_casualidad_01
    PENSAMIENTO: Amory diría que sí lo son. Amory no existe. # esperar:1 # id:j5_07_casualidad_02
- PENSAMIENTO: Stepney estaba al borde. Medio Partido, medio prole. # id:j5_07_stepney_01
PENSAMIENTO: Stepney fue la excepción. Eurasia apuntó a nosotros aquella vez. # id:j5_07_stepney_02
{ registro_j5_lamina_puesta == "si":
    ~ sube_sospecha(10)
    PENSAMIENTO: A las seis, Voss hace su ronda. Se detiene junto a la mesa del Registro. La lámina sigue sobre el mapa. # id:j5_07_ronda_01
    PENSAMIENTO: No dice nada. Apunta algo en su libreta. # id:j5_07_ronda_02
}
PENSAMIENTO: Fin de la jornada. # id:j5_07_fin
-> DONE

=== j5_salir ===
{ not registro_j5_hecho:
    PENSAMIENTO: Primero, el Registro. Uno de los partes me resultará familiar. # id:j5_06_salir_no
    -> DONE
}
CARTEL: Esa noche. # fx:negro # id:j5_07_cartel # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== J5.08 — El piso · Noche · El diario
=== j5_noche ===
{ noche_j5_vista:
    -> DONE
}
~ noche_j5_vista = true
PENSAMIENTO: Me quito el abrigo. Al colgarlo noto un peso extraño en el bolsillo interior. # id:j5_08_pens_00
-> DONE

=== j5_abrigo ===
{ diario_encontrado:
    PENSAMIENTO: El abrigo. Ya no pesa. # id:j5_08_abrigo_vacio
    -> DONE
}
~ diario_encontrado = true
~ inventario += diario
PENSAMIENTO: Un cuaderno pequeño de tapas negras. Papel crema, de antes de la Revolución. # objeto:diario # id:j5_08_diario_01
PENSAMIENTO: Las primeras páginas están arrancadas. En la cara interior de la tapa, un pájaro diminuto dibujado a lápiz. # id:j5_08_diario_02
{ dp_j3_amory == "recordar":
    PENSAMIENTO: Un pájaro. Es de Amory. Era su cuaderno. ¿Quién…? # id:j5_08_recordar_01
    PENSAMIENTO: La limpiadora. El carrito. Los dibujos. ¿Ella? # id:j5_08_recordar_02
- else:
    ~ sube_duda(5)
    PENSAMIENTO: Un pájaro. El pinchazo en la sien es ahora un dolor sordo. Alguien que dibujaba pájaros. # id:j5_08_aceptar_01
    PENSAMIENTO: Felix. Se llamaba Felix. # fx:temblor # id:j5_08_aceptar_02
    PENSAMIENTO: Me tapo la boca, como si lo hubiera dicho en voz alta. # id:j5_08_aceptar_03
}
PENSAMIENTO: Un cuaderno así no es ilegal. Nada es ilegal. Pero si me ven escribiendo en él… # id:j5_08_pens_01
PENSAMIENTO: La telepantalla lo ve todo. Todo salvo el hueco entre el armario y la pared del cartel de Ivy. # id:j5_08_pens_02
-> DONE

=== j5_diario_cono ===
{ not cono_avisado:
    ~ cono_avisado = true
    ~ sube_sospecha(5)
    TELEPANTALLA: …camaradas, recuerden la importancia del descanso… # id:j5_08_tp_01
}
PENSAMIENTO: Aquí no. Aquí me ve. # id:j5_08_cono
-> DONE

=== j5_hueco ===
{ jornada >= 6:
    -> j6_hueco
}
{ diario_escondite != "":
    PENSAMIENTO: El cuaderno está detrás del cartel de Ivy. Mañana. # id:j5_08_hueco_hecho
    -> DONE
}
PENSAMIENTO: El hueco entre el armario y la pared. Aquí no llega. # id:j5_08_hueco_01
PENSAMIENTO: Si escribo algo, ya lo habré hecho. No se puede deshacer. El crimental no se comete escribiendo. Escribir solo lo demuestra. # id:j5_08_hueco_02
* [Escribir.] # decision:D-J5-DIARIO
    ~ temp antes = diario_entradas
    PENSAMIENTO: Cierro el cuaderno. # minijuego:diario,fecha=19 de abril # id:j5_08_cerrar
    { diario_entradas > antes:
        ~ diario_iniciado = true
        ~ sube_duda(5)
        PENSAMIENTO: 1984. Creo. Nadie lo sabe con seguridad. # id:j5_08_anio
    }
* [Esconderlo sin escribir.]
    PENSAMIENTO: Todavía no. # id:j5_08_todavia
- PENSAMIENTO: Despego una esquina del cartel de Ivy, meto el cuaderno detrás y la vuelvo a pegar. Su cara queda un poco torcida. # id:j5_08_esconder_01
~ diario_escondite = "cartel"
PENSAMIENTO: Perdóname, Ivy. Eres el único sitio donde no miran. # id:j5_08_esconder_02
-> DONE

=== j5_hueco_mirar ===
{ inventario ? diario:
    PENSAMIENTO: El hueco entre el armario y la pared. La telepantalla no llega hasta aquí. # id:j5_08_hueco_mirar
- else:
    PENSAMIENTO: Un rincón entre el armario y la pared. Polvo. # id:piso_hueco_mirar
}
-> DONE

=== j5_dormir ===
~ jornada = 6
~ desayunado = false
CARTEL: JORNADA 6 # fx:negro # sfx:silbato # id:j5_08_jornada6
CARTEL: Jornada 6. # id:j5_08_fin # escena:piso # pos:cama
-> DONE
