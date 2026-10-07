// ACTO II · JORNADA 4 — El registro de impactos (guion: docs/guion-detallado/02-acto-2.md)
// Los knots de los escenarios compartidos desvían aquí cuando jornada == 4.
// Monólogo según la Duda: [D0] < 20 · [D1] 20–49 (convenciones del guion).

// ==================================================================== J4.01 — El piso · 07:15
=== j4_piso ===
{ gimnasia_j4:
    -> DONE
}
~ gimnasia_j4 = true
~ cajon_disponible = true
TELEPANTALLA: ¡Arriba, camaradas! ¡Uno, dos! ¡Uno, dos! # sfx:silbato # id:j4_01_tp_01
TELEPANTALLA: ¡Alto! ¡Descanso! # cf:id=CF-J4-GIMNASIA,expr=entusiasmo,dif=facil,golpes=6,coro=¡Uno!/¡Dos! # id:j4_01_tp_02
{ cf_j4_gimnasia == "fallo":
    ~ sube_sospecha(3)
}
TELEPANTALLA: …anoche, un cobarde cohete euroasiático alcanzó una zona residencial del distrito de Limehouse. # id:j4_01_tp_03
TELEPANTALLA: El Partido lamenta las víctimas y promete una respuesta implacable. ¡Muerte a Eurasia! # cf:id=CF-J4-NOTICIA,expr=duelo,dif=facil,golpes=8,coro=¡Muerte!/¡A Eurasia! # id:j4_01_tp_04
{ cf_j4_noticia == "fallo":
    ~ sube_sospecha(3)
}
{ duda < 20:
    PENSAMIENTO: El silbido de anoche. Lo oí. Otro más. Otro como el de Ivy. # id:j4_01_pens_d0
- else:
    PENSAMIENTO: El silbido de anoche. Lo oí desde la cama. Ni siquiera me levanté. ¿Desde cuándo no me levanto? # id:j4_01_pens_d1
}
-> DONE

=== j4_cartel_mirar ===
{ jornada >= 8:
    -> j8_cartel_manana
}
{ jornada >= 6 and diario_escondite == "cartel":
    PENSAMIENTO: Sigue un poco torcido. Lo enderezo. Ya está. # id:j6_01_cartel
    -> DONE
}
PENSAMIENTO: Buenos días, Ivy. # id:j4_01_cartel_01
{ duda >= 20:
    PENSAMIENTO: Te han cambiado la nariz. # id:j4_01_cartel_02
}
-> DONE

=== j4_cajon_piso ===
{ foto_cogida:
    PENSAMIENTO: Ya no queda nada en el cajón. # id:j4_01_cajon_vacio
    -> DONE
}
~ foto_cogida = true
~ inventario += foto_ivy
{ genero == "f":
    PENSAMIENTO: Una fotografía quemada por un borde, arrugada y desvaída. Dos niños en un parque. # objeto:foto_ivy # vineta:vineta-foto_ivy_m # id:j4_01_foto_01m
- else:
    PENSAMIENTO: Una fotografía quemada por un borde, arrugada y desvaída. Dos niños en un parque. # objeto:foto_ivy # vineta:vineta-foto_ivy_h # id:j4_01_foto_01
}
PENSAMIENTO: Ivy, con unos diez años. Y yo, algo mayor. La cara de Ivy está casi borrada por una mancha de agua. # id:j4_01_foto_02
PENSAMIENTO: Ya casi no se le ve la cara. En el cartel se le ve mejor. # id:j4_01_foto_03
PENSAMIENTO: No es la misma cara. # esperar:0.8 # vineta:fin # id:j4_01_foto_04
-> DONE

// ==================================================================== J4.02 — Departamento · Una tarea nueva
=== j4_entrar ===
{ cantina_j4_vista and not ilegible_visto:
    -> j4_ilegible
}
{ depto_j4_visto:
    -> DONE
}
~ depto_j4_visto = true
~ voss_presente = true
PENSAMIENTO: Pell teclea con dos dedos en la mesa de al lado. Voss sale de su despacho con una carpeta. # refrescar # id:j4_02_pens_00
VOSS: Camarada {apellido}. A partir de hoy llevará también el Registro de Impactos. # id:j4_02_voss_01
PROTAGONISTA: ¿El registro, Subdirector? ¿Quién lo llevaba hasta ahora? # id:j4_02_prot_01
VOSS: Estaba vacante. # esperar:1 # id:j4_02_voss_02
VOSS: Cada parte de Defensa Civil se anota en el mapa y en el libro. Exactitud, camarada. El Partido necesita saber dónde golpea el enemigo para golpearle a él. # id:j4_02_voss_03
{ amory_reaccion == "denuncia":
    VOSS: Usted ha demostrado tener buen ojo. Úselo. # id:j4_02_voss_04
}
~ registro_asignado = true
~ voss_presente = false
{ dp_j3_amory == "recordar":
    PENSAMIENTO: Vacante. Era de Amory. Amory llevaba el registro los jueves. Lo sé. Lo sé. # refrescar # id:j4_02_pens_recordar
- else:
    PENSAMIENTO: Vacante. Una mesa vacante. Un pinchazo en la sien. Mejor así. # refrescar # id:j4_02_pens_aceptar
}
-> DONE

// ==================================================================== J4.03 — La mesa del Registro
=== j4_registro_mirar ===
{
- jornada >= 5 and registro_j5_hecho:
    PENSAMIENTO: Las chinchetas negras, todas al este y al sur. El centro, limpio. # id:j5_07_mapa_despues
- registro_j4_hecho:
    PENSAMIENTO: Seis chinchetas negras clavadas en el mapa. # id:j4_03_mapa_despues
- else:
    PENSAMIENTO: Toda la ciudad. Sin una sola chincheta. Alguien la ha limpiado. # id:j4_03_mapa_mirar
}
-> DONE

=== j4_libro_mirar ===
PENSAMIENTO: El Libro de Registro. Tapas de tela gris. # id:j4_03_libro_mirar
-> DONE

=== j4_libro ===
{ jornada == 5:
    -> j5_libro
}
{ jornada == 8:
    -> j8_libro
}
{ registro_j4_hecho:
    PENSAMIENTO: El libro está al día. # id:j4_03_libro_hecho
    -> DONE
}
PENSAMIENTO: Se abre por la página del día. Las anteriores están arrancadas: quedan restos de papel en el lomo. # id:j4_03_libro_01
PENSAMIENTO: Faltan todas las páginas anteriores. Empiezo de cero. # id:j4_03_libro_02
{ duda >= 20:
    PENSAMIENTO: ¿Por qué arrancarlas? Un registro arrancado no es un registro. # id:j4_03_libro_d1
}
PENSAMIENTO: El tubo neumático escupe varios cilindros seguidos. # sfx:tubo # id:j4_03_tubo
// la etiqueta va en la línea que se muestra después del minijuego (diseño técnico §4.5)
PENSAMIENTO: Al día. # minijuego:impactos,registro=j4,vars=registro_j4 # id:j4_03_hecho
~ registro_j4_hecho = true
{ duda < 20:
    PENSAMIENTO: Seis. Seis en una noche. Eurasia no descansa. Nosotros tampoco. # id:j4_03_seis_d0
- else:
    PENSAMIENTO: Seis en una noche. # id:j4_03_seis_d1
}
{ registro_j4_lamina == "si":
    ~ sube_duda(3)
    { duda < 20:
        PENSAMIENTO: Todas en zona prole. Lógico: allí las casas son de ladrillo viejo y los proles no se refugian a tiempo. Eurasia busca hacer daño. # id:j4_03_lamina_d0
    - else:
        PENSAMIENTO: Todas en zona prole. # id:j4_03_lamina_d1
        { inventario ? nota_amory:
            PENSAMIENTO: «¿Por qué nunca en el centro?» # id:j4_03_lamina_nota
        }
    }
}
PENSAMIENTO: Es la hora de comer. # id:j4_03_comer
-> DONE

=== j4_cajon_mirar ===
PENSAMIENTO: Un cajón con tirador de latón. # id:j4_03_cajon_mirar
-> DONE

=== j4_cajon ===
{
- not cajon_abierto:
    ~ cajon_abierto = true
    ~ inventario += compas
    PENSAMIENTO: Dentro: un compás de latón, gomas, un lápiz roto. # objeto:compas # id:j4_03_cajon_01
    PENSAMIENTO: El fieltro del fondo está despegado por una esquina. # id:j4_03_cajon_02
- not fieltro_levantado:
    ~ fieltro_levantado = true
    ~ zonificacion_encontrada = true
    ~ inventario += zonificacion
    ~ inventario += nota_amory
    ~ diario_amory = true
    ~ sube_duda(5)
    PENSAMIENTO: Debajo del fieltro, una lámina transparente con un sello oficial: «Zonificación urbana. Distritos del Partido. Distritos proletarios.» # objeto:zonificacion # id:j4_03_lamina_01
    PENSAMIENTO: Y un papel doblado. Una sola línea, con letra apretada: «¿Por qué nunca en el centro?» En la esquina, un pájaro diminuto. # objeto:nota_amory # id:j4_03_nota_01
    { dp_j3_amory == "recordar":
        PENSAMIENTO: Un pájaro. Es su letra. Es Amory. «¿Por qué nunca en el centro?» ¿Qué centro? # id:j4_03_nota_recordar
    - else:
        PENSAMIENTO: Un pájaro. Alguien dibujaba pájaros. El pinchazo otra vez, más fuerte. No sé qué significa. # fx:temblor # id:j4_03_nota_aceptar
    }
- else:
    PENSAMIENTO: Ya no queda nada debajo del fieltro. # id:j4_03_cajon_vacio
}
-> DONE

=== j4_salir ===
{ not registro_j4_hecho:
    PENSAMIENTO: Primero, el Registro. # id:j4_02_salir_no
    -> DONE
}
{ cantina_j4_vista:
    PENSAMIENTO: Todavía queda el último cilindro del día. # id:j4_05_salir_no
    -> DONE
}
CARTEL: Mediodía. # fx:negro # id:j4_04_cartel # escena:cantina # pos:puerta
-> DONE

// ==================================================================== J4.04 — Cantina · Mediodía
=== j4_cantina ===
{ cantina_j4_vista:
    -> DONE
}
~ cantina_j4_vista = true
PENSAMIENTO: Como solo. La silla de enfrente está vacía. # id:j4_04_pens_00
-> DONE

=== j4_silla_mirar ===
{ dp_j3_amory == "recordar":
    PENSAMIENTO: «Si no hay palabra, no hay retirada.» Lo dijo aquí. Brindó con la ginebra. # id:j4_04_silla_recordar
- else:
    PENSAMIENTO: Una silla vacía. Las sillas vacías no significan nada. # id:j4_04_silla_aceptar
}
-> DONE

=== j4_pell_mirar ===
PENSAMIENTO: Pell come mecánicamente. Cuchara, boca, cuchara. # id:j4_04_pell_mirar
-> DONE

=== j4_brooke ===
{ brooke_j4:
    PENSAMIENTO: Brooke ya no está para hablar. # id:j4_04_brooke_otra
    -> DONE
}
~ brooke_j4 = true
BROOKE: Le han dado el registro. # id:j4_04_brooke_01
PROTAGONISTA: ¿Cómo lo sabe? # id:j4_04_prot_01
BROOKE: Esa mesa da mala suerte, camarada. # id:j4_04_brooke_02
PENSAMIENTO: Se levanta con la bandeja. # id:j4_04_pens_01
BROOKE: Coma algo. Se le nota en la cara cuando no come. # id:j4_04_brooke_03
-> DONE

=== j4_cantina_salir ===
{ not cantina_j4_vista:
    -> DONE
}
CARTEL: La tarde. # fx:negro # id:j4_04_cartel_tarde # escena:departamento # pos:mesa
-> DONE

// ==================================================================== J4.05 — Fin de la jornada · El parte ilegible
=== j4_ilegible ===
~ ilegible_visto = true
PENSAMIENTO: Último cilindro del día. # sfx:tubo # id:j4_05_pens_00
CARTEL: def.civil · impacto · 18.4.84 · 17:52¶distrito: limehouse · cuadr: ?-8 (ilegible)¶bajas: pendiente # id:j4_05_parte
PENSAMIENTO: Ilegible. No puedo registrar un impacto ilegible. # id:j4_05_pens_01
PENSAMIENTO: Limehouse está a veinte minutos andando. Si voy yo mism{o}… # id:j4_05_pens_02
* [«Un registro debe ser exacto. Ivy merece un registro exacto.»] # decision:D-J4-VERIFICAR
    ~ visita_prole_j4 = true
    CARTEL: Limehouse. Atardecer. # fx:negro # id:j4_05_cartel_ir # escena:limehouse # pos:entrada
* [«Lo completará Defensa Civil mañana.»]
    PENSAMIENTO: La casilla se queda en blanco. # id:j4_05_blanco
    CARTEL: Esa noche. # fx:negro # id:j4_05_cartel_casa # escena:piso_noche # pos:puerta
- -> DONE

// ==================================================================== J4.06 — Limehouse · Atardecer
=== limehouse ===

= entrar
{ final_en_curso == "D":
    -> fd_limehouse.entrar
}
{ limehouse_visto:
    -> DONE
}
~ limehouse_visto = true
~ sube_sospecha(3)
PENSAMIENTO: La música del Partido se queda atrás. Alguien tararea una canción de taberna. # id:j4_06_pens_00
{ duda < 20:
    PENSAMIENTO: Proles. Cuánto ruido. Cuánta suciedad. Y ni una sola telepantalla. ¿Cómo saben qué tienen que pensar? # id:j4_06_pens_d0
- else:
    PENSAMIENTO: Proles. Cuánto ruido. Hace mucho que no oía a nadie reír tan alto. # id:j4_06_pens_d1
}
-> DONE

= altavoz_mirar
PENSAMIENTO: Aquí el Partido habla desde lejos. Como si no hiciera falta acercarse. # id:j4_06_altavoz
-> DONE

= ropa_mirar
PENSAMIENTO: Sábanas, camisas… y vestidos de colores. Colores que no se ven en las Mansiones Victoria. # id:j4_06_ropa
-> DONE

= pub_mirar
PENSAMIENTO: «La Campana». Una taberna prole. Por las ventanas sale luz amarilla y humo. # id:j4_06_pub_mirar
-> DONE

= entrar_pub
# escena:pub # pos:puerta
-> DONE

= casa_mirar
{ casa_vista:
    PENSAMIENTO: Una cama colgando sobre la calle. Papel pintado de flores. Alguien eligió esas flores. # id:j4_07_casa_mirar
- else:
    PENSAMIENTO: Una columna de humo, al fondo de la calle. # id:j4_06_humo
}
-> DONE

// ==================================================================== J4.07 — Limehouse · La casa alcanzada
= casa
{ casa_vista:
    -> casa_mirar
}
~ casa_vista = true
PENSAMIENTO: Una casa partida por la mitad. Se ve el interior, como una casa de muñecas: una cama colgando, un papel pintado de flores. # musica:ruinas # id:j4_07_pens_00
PENSAMIENTO: Proles apartando escombros. Una mujer de brazos fuertes dirige a los demás a gritos. # id:j4_07_pens_01
PENSAMIENTO: Y el niño que rebusca entre los cascotes con una lata… Es el de la avenida. El del cigarrillo. Lleva un trozo de metralla colgado al cuello. # musica:prole # id:j4_07_pens_02
-> DONE

= sammy_mirar
PENSAMIENTO: El niño de la avenida. El del cigarrillo. # id:j4_07_sammy_mirar
-> DONE

= dot_mirar
PENSAMIENTO: Robusta, con un pañuelo en la cabeza. Nadie aparta un ladrillo sin que ella lo diga. # id:j4_07_dot_mirar
-> DONE

= proles_mirar
PENSAMIENTO: Apartan ladrillos con las manos. Nadie de Defensa Civil. # id:j4_07_proles_mirar
-> DONE

= dot
{ dot_hablado:
    DOT: Vuelva a su barrio, camarada. Aquí ya está todo apuntado. # id:j4_07_dot_despues
    -> DONE
}
-> sammy

= sammy
{ dot_hablado:
    SAMMY: ¡Ochenta y tres! Bueno, ochenta y dos, si se lo ha quedado. # id:j4_07_sammy_despues
    -> DONE
}
~ dot_hablado = true
SAMMY: ¡Mire! Este es de cohete grande. Este de uno pequeño. Este no sé. Tengo ochenta y tres. ¡El Billy Hogan solo tiene cuarenta! # id:j4_07_sammy_01
PROTAGONISTA: Eso es peligroso. Puede quedar alguno sin explotar. # id:j4_07_prot_01
SAMMY: ¡Qué va! Los cohetes explotan siempre. Mi madre dice que es lo único que funciona bien en Londres. # id:j4_07_sammy_02
DOT: ¡Sammy! ¡Deja en paz a {el} camarada! # id:j4_07_dot_01
PENSAMIENTO: Se acerca, se limpia las manos en el delantal y me mira el mono azul de arriba abajo. # id:j4_07_pens_03
DOT: ¿Viene del Partido? ¿A contar muertos? # id:j4_07_dot_02
PROTAGONISTA: Vengo a registrar el impacto. Mi parte era ilegible. # id:j4_07_prot_02
DOT: Ilegible. # id:j4_07_dot_03
DOT: Mire, apúntelo: calle Narrow, número once. Los Hennessy. La abuela y los dos pequeños. El padre estaba en el turno de noche del muelle. # id:j4_07_dot_04
DOT: Eso es lo que hay que apuntar. # id:j4_07_dot_05
~ ilegible_completado = true
PENSAMIENTO: J-8. El parte ya no es ilegible. # id:j4_07_pens_04
* [«Eurasia pagará por esto.»]
    DOT: Será. Aquí caen cada semana, ¿sabe? Cada semana. # id:j4_07_dot_06
    PENSAMIENTO: Señala con la barbilla hacia el oeste, donde brillan las pirámides blancas de los ministerios. # id:j4_07_pens_05
    DOT: Allí arriba nunca. Los euroasiáticos deben de tenernos mucho cariño. # id:j4_07_dot_07
    ~ sube_duda(3)
    { duda < 20:
        PENSAMIENTO: Habla así porque es prole. No entiende de estrategia. # id:j4_07_pens_d0
    - else:
        PENSAMIENTO: Allí arriba nunca. # id:j4_07_pens_d1
    }
* [«Lo siento por los Hennessy.»]
    DOT: …Gracias. No suelen decir eso los de azul. # id:j4_07_dot_08
    ~ dot_confianza += 1
* [«¿Por qué no se refugian?»]
    DOT: ¿Dónde? ¿En el metro? Lo cerraron hace dos años. «Por reformas.» # id:j4_07_dot_09
    DOT: Reforman muy despacio. # id:j4_07_dot_10
- SAMMY: ¿Quiere uno? Para que le dé suerte. Nunca te cae un cohete donde ya tienes uno. # id:j4_07_sammy_03
* [Aceptar la metralla.] # decision:D-J4-METRALLA
    ~ inventario += metralla_sammy
    ~ dot_confianza += 1
    SAMMY: ¡Ochenta y dos, entonces! # objeto:metralla_sammy # id:j4_07_sammy_04
* [Rechazarla.]
    SAMMY: Usted se lo pierde. # id:j4_07_sammy_05
-
~ crane_aparece = true
PENSAMIENTO: Al girarme para irme veo a un hombre con una cámara de fuelle, fotografiando las ruinas. # refrescar # id:j4_07_pens_06
-> DONE

// ==================================================================== J4.07b — Crane
= crane_mirar
PENSAMIENTO: Unos cincuenta años, bien afeitado, chaleco de lana y sombrero. Una cámara antigua sobre un trípode. # id:j4_07b_crane_mirar
-> DONE

= crane
{ crane_visto:
    CRANE: Calle Cable, junto al mercado. Cuando quiera. # id:j4_07b_crane_despues
    -> DONE
}
~ crane_visto = true
CRANE: No se mueva, camarada. Usted, con el mono azul delante de la casa rota… Es una imagen. # sfx:obturador # musica:crane # id:j4_07b_crane_01
CRANE: Perdone. Deformación profesional. Abel Crane. Tengo el estudio en la calle Cable, junto al mercado. # id:j4_07b_crane_02
PROTAGONISTA: ¿Para qué fotografía esto? # id:j4_07b_prot_01
CRANE: Para el recuerdo. Aquí nadie tiene fotos de nada. Si no las hago yo, dentro de un año nadie sabrá que aquí vivían los Hennessy. # id:j4_07b_crane_03
CRANE: Usted… perdone el atrevimiento… ¿no se parece a la chica del cartel nuevo? El de los mártires. La de primera fila. # id:j4_07b_crane_04
PROTAGONISTA: Era mi hermana. # id:j4_07b_prot_02
PENSAMIENTO: Se quita el sombrero. # id:j4_07b_pens_00
CRANE: Lo siento mucho. De verdad. # id:j4_07b_crane_05
CRANE: ¿Tiene fotos de ella? Fotos de verdad, digo, no carteles. # id:j4_07b_crane_06
{ inventario ? foto_ivy:
    PROTAGONISTA: Una. Muy estropeada. # id:j4_07b_prot_03
    CRANE: Tráigamela. Restauro fotografías antiguas, es mi especialidad. Hago maravillas con el agua y el fuego. # id:j4_07b_crane_07
    CRANE: Le devolveré la cara de su hermana. Sin compromiso. Para mí sería un honor. # id:j4_07b_crane_08
    ~ inventario += tarjeta_crane
    PENSAMIENTO: Me tiende una tarjeta. # objeto:tarjeta_crane # id:j4_07b_pens_01
- else:
    PROTAGONISTA: No. Solo el cartel. # id:j4_07b_prot_04
    CRANE: Qué pena. Si alguna vez encuentra una, venga a verme. # id:j4_07b_crane_09
}
{ duda < 20:
    PENSAMIENTO: Un prole amable. Existen. # musica:taberna_calle # id:j4_07b_pens_d0
- else:
    PENSAMIENTO: Un prole amable. Con una cámara. Es buena persona. Se le ve. # musica:taberna_calle # id:j4_07b_pens_d1
}
-> DONE

= volver
{ not dot_hablado:
    PENSAMIENTO: Todavía no. El impacto. # id:j4_06_volver_no
    -> DONE
}
CARTEL: Mansiones Victoria. Las once pasadas. # fx:negro # id:j4_10_cartel # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== J4.08 — Pub «La Campana» (opcional)
=== pub ===

= entrar
{ pub_visto:
    -> DONE
}
~ pub_visto = true
PENSAMIENTO: El ambiente se apaga cuando entro con el mono azul. Silencio. # id:j4_08_pens_00
PENSAMIENTO: Después, poco a poco, vuelven las conversaciones. # id:j4_08_pens_01
-> DONE

= campana_mirar
PENSAMIENTO: Una campana de barco. Vieja. Tiene algo grabado: «S. Clem…». El resto está borrado. # id:j4_08_campana
-> DONE

= diana_mirar
PENSAMIENTO: Una diana de dardos, acribillada. Aquí juegan por gusto. # id:j4_08_diana
-> DONE

= proles_mirar
PENSAMIENTO: Juegan a la lotería. Apuntan números en papelitos con una seriedad que no he visto nunca en el Ministerio. # id:j4_08_proles
-> DONE

= tabernero_mirar
PENSAMIENTO: Seca una jarra sin dejar de mirarme. # id:j4_08_tabernero_mirar
-> DONE

= tabernero
TABERNERO: Aquí no servimos ginebra de la Victoria, camarada. Solo cerveza. Si quiere ginebra, vuelva a su barrio. # id:j4_08_tabernero
-> DONE

= viejo_mirar
PENSAMIENTO: Un viejo, solo, con una pinta. Habla con ella más que con nadie. # id:j4_08_viejo_mirar
-> DONE

= viejo
{ viejo_hablado:
    VIEJO: Medio litro. Y dicen que es más. # id:j4_08_viejo_despues
    -> DONE
}
~ viejo_hablado = true
VIEJO: ¿Sabe lo que era una pinta? Antes. Una pinta de verdad. Ahora te ponen esto, medio litro, y te dicen que es más. # id:j4_08_viejo_01
VIEJO: Y es menos. Yo lo sé porque me acuerdo. Los jóvenes no se acuerdan de nada. # id:j4_08_viejo_02
PROTAGONISTA: Antes de la Revolución los capitalistas les mataban de hambre. # id:j4_08_prot_01
PENSAMIENTO: Me mira por fin, divertido. # id:j4_08_pens_02
VIEJO: ¿Ah, sí? Pues yo me acuerdo de que estaba gordo. # id:j4_08_viejo_03
~ sube_duda(2)
PENSAMIENTO: Se ríe hasta toser. # sfx:tos # id:j4_08_pens_03
-> DONE

= salir
# escena:limehouse # pos:pub
-> DONE

// ==================================================================== J4.10 — El piso · Noche
=== j4_noche ===
{ noche_j4_vista:
    -> DONE
}
~ noche_j4_vista = true
{ visita_prole_j4 and hilda_aprecio < 2:
    PENSAMIENTO: Al subir por la escalera, una puerta se entreabre. # id:j4_10_pens_00
    HILDA: Qué tarde, {nombre}. Las once pasadas. ¿Mucho trabajo? # id:j4_10_hilda_01
    PROTAGONISTA: Verificación de un impacto. Para el Registro. # id:j4_10_prot_01
    HILDA: Ah. Qué celo. # id:j4_10_hilda_02
    ~ sube_sospecha(3)
    PENSAMIENTO: Cierra la puerta despacio. # id:j4_10_pens_01
}
PENSAMIENTO: Mi piso. La telepantalla, en voz baja. # id:j4_10_pens_02
-> DONE

=== j4_dormir ===
~ nueva_jornada(5)
~ desayunado = false
CARTEL: JORNADA 5 # fx:negro # sfx:silbato # id:j4_10_jornada5
CARTEL: Jornada 5. Antes del silbato. # id:j4_10_fin # escena:piso # pos:cama
-> DONE
