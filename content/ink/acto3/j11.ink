// ACTO III · JORNADA 11 — El Ministerio del Amor (guion: docs/guion-detallado/03-acto-3.md)
// El expediente de Ivy, el doblepensar extremo, la lista de Len Pike y el anticuario de uniforme negro.

// ==================================================================== El piso · Mañana
=== j11_piso ===
{ depto_j11_visto:
    -> DONE
}
TELEPANTALLA: Mañana, en el Parque de la Victoria, los prisioneros estasiáticos recibirán su justo castigo. Asistencia obligatoria para el personal de los ministerios. # id:j11_00_tp_01
PENSAMIENTO: Mañana. # id:j11_00_pens_00
-> DONE

// ==================================================================== J11.01 — Departamento · Mañana
=== j11_entrar ===
{ depto_j11_visto:
    -> DONE
}
~ depto_j11_visto = true
~ voss_presente = true
PENSAMIENTO: Voss me espera junto a mi mesa con una carpeta gris sellada con lacre rojo. # refrescar # id:j11_01_pens_00
VOSS: Camarada {apellido}. La lista de prisioneros estasiáticos para la ejecución pública de mañana en el parque. # id:j11_01_voss_01
VOSS: Llévela al Ministerio del Amor. Recepción de la planta baja. # esperar:0.8 # id:j11_01_voss_02
VOSS: Personalmente. # id:j11_01_voss_03
PROTAGONISTA: ¿Al Minimor, Subdirector? # id:j11_01_prot_01
VOSS: ¿Le supone algún problema, camarada? # id:j11_01_voss_04
PROTAGONISTA: Ninguno, Subdirector. # cf:id=CF-J11-VOSS,expr=neutral,dif=dificil,golpes=10 # id:j11_01_prot_02
{ cf_j11_voss == "fallo":
    ~ sube_sospecha(10)
}
PENSAMIENTO: Me mira un segundo de más. # id:j11_01_pens_01
VOSS: Es un edificio muy interesante. Todo el mundo debería visitarlo al menos una vez. # id:j11_01_voss_05
~ voss_presente = false
PENSAMIENTO: Me está enseñando dónde voy a acabar. # refrescar # id:j11_01_pens_02
PENSAMIENTO: En el pasillo, Brooke se cruza conmigo. Sin detenerse, me pone algo en la mano: una chapa metálica con un número. # id:j11_01_pens_03
~ inventario += chapa
~ brooke_revelada = true
BROOKE: Archivo B, pasillo cuatro. Tres minutos mientras sellan la lista. # objeto:chapa # id:j11_01_brooke_01
BROOKE: Mi hermano está en esa lista. # id:j11_01_brooke_02
PENSAMIENTO: ¿Su hermano? # id:j11_01_pens_04
CARTEL: Ministerio del Amor. # fx:negro # id:j11_02_cartel # escena:minimor # pos:entrada
-> DONE

// ==================================================================== J11.02 — Ministerio del Amor · Recepción
=== minimor ===

= entrar
{ expediente_visto and len_decision == "":
    -> j11_lista
}
{ minimor_visto:
    -> DONE
}
~ minimor_visto = true
PENSAMIENTO: Sin ventanas. Alambradas, nidos de ametralladoras, guardias con porras articuladas. # fx:aclarar # id:j11_02_pens_00
PENSAMIENTO: Dentro, todo es blanco. Una luz sin sombras que no parpadea. Un zumbido constante. # id:j11_02_pens_01
PENSAMIENTO: Y, muy de vez en cuando, algo que podría ser un grito lejano. O una tubería. # id:j11_02_pens_02
FUNCIONARIA: Carpeta. # id:j11_02_func_01
PENSAMIENTO: La abre, la sella, empieza a cotejar nombres con un fichero. # sfx:sello # id:j11_02_pens_03
FUNCIONARIA: Siéntese. Tardaré unos minutos. # id:j11_02_func_02
-> DONE

= banco
{ lista_proles_vista:
    PENSAMIENTO: El banco blanco. Espero. # id:j11_02_banco_ya
    -> DONE
}
PENSAMIENTO: Me siento en el banco. A mi lado, una copia de la lista. # id:j11_02_banco_01
PENSAMIENTO: Pike. # documento:lista_prisioneros # id:j11_02_pike_00
PENSAMIENTO: Pike. Como Dot. # esperar:1 # id:j11_02_pike_01
PENSAMIENTO: Junto a cada nombre, una foto de ficha. La de Pike, L.: un hombre fornido, de unos treinta y cinco. Un ancla tatuada en el cuello, como los estibadores de Limehouse. # id:j11_02_pike_02
{ dot_confianza >= 1:
    PENSAMIENTO: Dot dijo que su marido trabajaba en el muelle. Turno de noche. # esperar:0.8 # id:j11_02_pike_dot_01
    PENSAMIENTO: Len. Le llamaba Len. # id:j11_02_pike_dot_02
- else:
    PENSAMIENTO: Un estibador. «Capturado en el frente de Manchuria.» Con un ancla de Limehouse en el cuello. # id:j11_02_pike_no
}
PENSAMIENTO: Hogan. Sammy decía que Billy Hogan tenía cuarenta trozos de metralla. # esperar:0.8 # id:j11_02_hogan_01
PENSAMIENTO: ¿El padre de Billy? # id:j11_02_hogan_02
~ sube_duda(10)
~ lista_proles_vista = true
PENSAMIENTO: «Prisioneros estasiáticos.» Hace tres días eran euroasiáticos. Hace un mes eran estibadores. # id:j11_02_pens_04
~ funcionaria_fuera = true
FUNCIONARIA: Espere aquí. # refrescar # id:j11_03_func_01
PENSAMIENTO: Se lleva la carpeta a una oficina interior. Tres minutos, dijo Brooke. # id:j11_03_pens_00
-> DONE

= servicio
{ expediente_visto:
    PENSAMIENTO: No. Otra vez no. # id:j11_03_servicio_ya
    -> DONE
}
{ not funcionaria_fuera:
    PENSAMIENTO: Una puerta lateral, pequeña, gris. Con la funcionaria delante, ni mirarla. # id:j11_03_servicio_no
    -> DONE
}
{ not (inventario ? chapa):
    PENSAMIENTO: Cerrada. # id:j11_03_servicio_cerrada
    -> DONE
}
PENSAMIENTO: La chapa de Brooke encaja en la ranura. Un acceso de servicio, el de los proles de la limpieza. # sfx:cerrojo # reloj:inicio=10:20:00,limite=180,agotar=minimor_archivo.agotado # id:j11_03_servicio_01
PENSAMIENTO: Archivo B, pasillo cuatro. # fx:negro # id:j11_03_servicio_02 # escena:minimor_archivo # pos:servicio
-> DONE

= funcionaria_mirar
PENSAMIENTO: Una mujer sin edad. Voz de enfermera. # id:j11_02_func_mirar
-> DONE

= mostrador_mirar
PENSAMIENTO: Un fichero, un teléfono negro y una máquina de escribir. # id:j11_02_mostrador
-> DONE

= oficina_mirar
PENSAMIENTO: La puerta de la oficina interior. Blanca. Sin picaporte por este lado. # id:j11_02_oficina
-> DONE

= salir
PENSAMIENTO: No puedo irme sin la lista sellada. # id:j11_02_salir
-> DONE

// ==================================================================== J11.03 — Archivo B · Pasillo cuatro
=== minimor_archivo ===

= entrar
{ archivo_b_visto:
    -> DONE
}
~ archivo_b_visto = true
PENSAMIENTO: Pasillos blancos idénticos. Puertas numeradas. Ninguna telepantalla a la vista. # id:j11_03_pens_01
PENSAMIENTO: Las del Minimor están empotradas en la pared. Dicen que se las oye zumbar. # id:j11_03_pens_02
-> DONE

= visto
PENSAMIENTO: Una voz, desde ninguna parte. # id:j11_03_visto_00
TELEPANTALLA: Camarada. Vuelva a la sala de espera. # id:j11_03_visto_01
~ sube_sospecha_sigilo(10)
PENSAMIENTO: Vuelvo. Espero. Nadie viene. Lo intento otra vez. # id:j11_03_visto_02
-> DONE

= agotado
PENSAMIENTO: Pasos en algún pasillo. Tengo que darme prisa. # sfx:botas # id:j11_03_agotado_01
~ sube_sospecha(5)
PENSAMIENTO: Un minuto. Quizá menos. # reloj:mas=60 # id:j11_03_agotado_02
-> DONE

= puerta_mirar
PENSAMIENTO: Una puerta blanca con una placa. No es la cuatro. # id:j11_03_puerta
-> DONE

= b4_mirar
PENSAMIENTO: «B-4.» # id:j11_03_b4_mirar
-> DONE

= b4
{ expediente_visto:
    PENSAMIENTO: Ya he visto lo que había que ver. # id:j11_03_b4_ya
    -> DONE
}
-> j11_expediente

= servicio
{ expediente_visto:
    PENSAMIENTO: Al banco. Rápido. # id:j11_03_volver # escena:minimor # pos:banco
    -> DONE
}
PENSAMIENTO: Volver ahora sería volver para nada. # id:j11_03_servicio_nada
-> DONE

// ==================================================================== J11.04 — El expediente de Ivy
=== j11_expediente ===
PENSAMIENTO: Un fichero de expedientes por apellido. El cajón de mi propio apellido. # sfx:papel # id:j11_04_pens_00
PENSAMIENTO: Dentro, entre otras fichas, una carpeta: {apellido}, Ivy. # documento:expediente_ivy # id:j11_04_pens_01
PENSAMIENTO: «Evitar martirio de signo subversivo.» # esperar:5 # id:j11_04_pens_02
PENSAMIENTO: La mataron para que la Hermandad no tuviera una mártir. # esperar:1 # id:j11_04_pens_03
PENSAMIENTO: Y la convirtieron en la suya. # esperar:1.4 # id:j11_04_pens_04
PENSAMIENTO: «Familiar directo. Sin implicación. Alta capacidad de odio canalizable.» # esperar:1 # id:j11_04_pens_05
PENSAMIENTO: Eso soy yo. # id:j11_04_pens_06
PENSAMIENTO: «Recomendación: destino Minipax.» Mi trabajo. Mi mesa. Mis partes. Mi odio. # esperar:1.4 # id:j11_04_pens_07
PENSAMIENTO: Todo esto lo firmó el mismo hombre. «H. Voss.» # esperar:1.8 # id:j11_04_pens_08
PENSAMIENTO: El abrigo. Los guantes. «Esta camarada es ahora una mártir del Partido.» # esperar:1 # id:j11_04_pens_09
PENSAMIENTO: Era él. # esperar:1.4 # id:j11_04_pens_10
PENSAMIENTO: «No les creas.» No hablaba de Eurasia, Ivy. Hablaba de ellos. # id:j11_04_pens_11
~ sube_duda(25)
~ ivy_revelada = true
~ expediente_visto = true
~ diario_ivy_verdad = true
// DP-J11-IVY · Doblepensar extremo: la voz que habla es la de Voss
PENSAMIENTO: El expediente tiembla. Las palabras empiezan a moverse. # sfx:pitido # dp:id=DP-J11-IVY # id:j11_04_dp_00
{ dp_j11_ivy == "aceptar":
    ~ baja_duda(20)
    ~ baja_sospecha(10)
    PENSAMIENTO: El expediente vuelve a ser legible. # documento:expediente_ivy # id:j11_04_aceptar_01
    PENSAMIENTO: Me protegió. Me protegió. # id:j11_04_aceptar_02
    PENSAMIENTO: Las manos no paran de temblar. # id:j11_04_aceptar_03
- else:
    ~ sube_duda(10)
    PENSAMIENTO: La estática se rompe como un cristal. # id:j11_04_recordar_01
    PENSAMIENTO: Ivy cantaba. Ivy me dijo: «No les creas». # id:j11_04_recordar_02
}
PENSAMIENTO: Al fondo de la carpeta, la foto. Ivy, con Nell y el tabernero, en un sótano. # id:j11_04_foto_00
* [Llevarme la foto del sótano.] # decision:D-J11-EXPEDIENTE
    ~ inventario += foto_sotano
    ~ foto_sotano_cogida = true
    ~ sube_sospecha(5)
    PENSAMIENTO: Dentro del mono. Mañana notarán que falta. # objeto:foto_sotano # id:j11_04_foto_coger
* [Dejarlo todo como estaba.]
    PENSAMIENTO: Cierro la carpeta. Cierro el cajón. # id:j11_04_foto_dejar
- PENSAMIENTO: Pasos en el pasillo. # sfx:botas # id:j11_04_pasos
PENSAMIENTO: Vuelvo al banco justo a tiempo. # fx:negro # reloj:parar # id:j11_04_volver # escena:minimor # pos:banco
-> DONE

// ==================================================================== J11.05 — La lista · Len Pike
=== j11_lista ===
PENSAMIENTO: La funcionaria vuelve con la carpeta sellada y una hoja más. # id:j11_05_pens_00
FUNCIONARIA: Falta un dato. El Subdirector Voss debe firmar la lista definitiva en el Minipax. Llévesela. # id:j11_05_func_01
FUNCIONARIA: Y esta es la lista de reserva, por si alguno de los prisioneros… no estuviera en condiciones para mañana. # id:j11_05_func_02
PENSAMIENTO: Suena el teléfono. Se gira para atenderlo. # sfx:pitido # id:j11_05_pens_01
PENSAMIENTO: Pike, L. Mañana. En el parque. La lista de reserva. Si cambio un nombre… otro ocupará su lugar. # id:j11_05_pens_02
PENSAMIENTO: La funcionaria cuelga. # minijuego:lista,resultado=len_decision,vars=len # id:j11_05_pens_03
~ diario_len = true
{ len_decision:
- "cambio":
    ~ len_salvado = true
    ~ sube_duda(5)
    ~ sube_sospecha(10)
    PENSAMIENTO: He salvado a un hombre. He matado a otro. Los dos con la misma máquina de escribir. # esperar:1 # id:j11_05_cambio_01
    PENSAMIENTO: Ya soy uno de ellos. # id:j11_05_cambio_02
    { len_chico:
        PENSAMIENTO: Era el más joven. Lo elegí porque no tenía cara de nada. # esperar:1 # id:j11_05_chico_01
        PENSAMIENTO: Lo elegí porque no tenía cara de nada. # id:j11_05_chico_02
    }
- "rabia":
    PENSAMIENTO: La funcionaria se gira. Mira los dos trozos. # id:j11_05_rabia_01
    FUNCIONARIA: …Tenemos copias, camarada. Siempre tenemos copias. # id:j11_05_rabia_02
    PENSAMIENTO: Descuelga el teléfono. # id:j11_05_rabia_03
    ~ sube_sospecha(30)
- "tachado":
    PENSAMIENTO: La funcionaria mira el tachón. Me mira. Saca otra copia del fichero. # id:j11_05_tachado_01
    ~ sube_sospecha(10)
- else:
    PENSAMIENTO: Diez segundos. No he hecho nada. # id:j11_05_nada_01
}
PENSAMIENTO: Salgo con la carpeta bajo el brazo. # id:j11_05_salir
CARTEL: De regreso. Las Mansiones Victoria. # fx:negro # id:j11_06_cartel # escena:avenida # pos:calle
-> DONE

// ==================================================================== J11.06 — Las Mansiones Victoria · Winston
=== j11_avenida ===
{ charrington_visto:
    -> DONE
}
~ charrington_visto = true
PENSAMIENTO: Delante del portal, una furgoneta negra. Vecinos asomados a las ventanas. # id:j11_06_pens_00
PENSAMIENTO: Hombres de uniforme negro bajan cajas. Les da órdenes un anciano de pelo blanco y espalda perfectamente recta. Voz seca. Joven. # id:j11_06_pens_01
HILDA: ¡{nombre}! ¡Smith! ¡El del séptimo! ¡Lo han cogido! ¡Con una chica! # id:j11_06_hilda_01
HILDA: En un cuarto encima de una tienda de antigüedades, en el barrio prole. ¡Llevaban meses! ¡Meses! # id:j11_06_hilda_02
HILDA: ¡Yo lo sabía! ¡Lo apunté! ¡Tercera ausencia del mes! # id:j11_06_hilda_03
-> DONE

=== j11_charrington_mirar ===
PENSAMIENTO: Ese hombre… parece un anticuario. Un viejo amable de barrio. Pero da órdenes como Voss. # id:j11_06_charr_01
PENSAMIENTO: ¿Cuántos hay como él? ¿Cuántos viejos amables? # id:j11_06_charr_02
{ crane_info >= 2 and not crane_sospechado:
    ~ crane_sospechado = true
    PENSAMIENTO: Un viejo amable con una tienda en el barrio prole. # esperar:1 # id:j11_06_charr_crane_01
    PENSAMIENTO: Una tienda. Un estudio. # esperar:1.2 # id:j11_06_charr_crane_02
    PENSAMIENTO: No. No puede ser. # id:j11_06_charr_crane_03
}
-> DONE

=== j11_hilda_otra ===
HILDA: ¡Tercera ausencia del mes! ¡Yo lo apunté! # id:j11_06_hilda_otra
-> DONE

=== j11_portal ===
PENSAMIENTO: El anciano pasa a mi lado al subir a la furgoneta. Me mira un instante, sin ningún interés. # id:j11_06_pens_02
PENSAMIENTO: Sube. La furgoneta arranca. # sfx:furgoneta # id:j11_06_pens_03
HILDA: Dicen que la chica era de la Liga Anti-Sex. ¡Anti-Sex! # id:j11_06_hilda_04
HILDA: Ya no se puede fiar una de nadie. # id:j11_06_hilda_05
CARTEL: Esa noche. # fx:negro # id:j11_07_cartel # escena:piso_noche # pos:puerta
-> DONE

// ==================================================================== J11.07 — El piso · Noche
=== j11_noche ===
{ noche_j11_vista:
    -> DONE
}
~ noche_j11_vista = true
PENSAMIENTO: Me quedo de pie frente al cartel de Ivy. # id:j11_07_pens_00
-> DONE

=== j11_cartel_mirar ===
{ cartel_arrancado:
    PENSAMIENTO: La pared desnuda. Una mancha más clara con su forma. # id:j11_07_mancha
    -> DONE
}
{ dp_j11_ivy == "aceptar":
    PENSAMIENTO: Traidora. # esperar:1 # id:j11_07_aceptar_01
    PENSAMIENTO: Traidora. La palabra suena hueca. # esperar:1 # id:j11_07_aceptar_02
    PENSAMIENTO: El Partido me protegió. # id:j11_07_aceptar_03
- else:
    PENSAMIENTO: Te pusieron en la pared para que yo te odiara a ti también sin saberlo. Para que gritara contra Goldstein con tu cara. # id:j11_07_recordar_01
    PENSAMIENTO: Y yo grité. Cinco años. # esperar:1 # id:j11_07_recordar_02
    PENSAMIENTO: No eras su mártir. Eras de los nuestros. Eras de los suyos. # esperar:1 # id:j11_07_recordar_03
    PENSAMIENTO: Eras tuya. # id:j11_07_recordar_04
}
-> DONE

// ◆ D-J11-CARTEL
=== j11_cartel_usar ===
{ cartel_arrancado or dp_j11_ivy != "recordar":
    -> j11_cartel_mirar
}
PENSAMIENTO: Su cara. Su cara de cartel. # id:j11_07_cartel_00
* [Arrancar el cartel.] # decision:D-J11-CARTEL
    ~ cartel_arrancado = true
    PENSAMIENTO: Lo arranco de un tirón. # sfx:papel # id:j11_07_arrancar_01
    { diario_escondite == "cartel":
        PENSAMIENTO: El cuaderno cae al suelo. # id:j11_07_arrancar_diario
        ~ diario_escondite = "hornillo"
    }
    PENSAMIENTO: Detrás, la pared desnuda tiene una mancha más clara con su forma. # id:j11_07_arrancar_02
    TELEPANTALLA: {num} {apellido}. Los símbolos del Partido no se destruyen. # id:j11_07_arrancar_tp
    ~ sube_sospecha(15)
    { diario_escondite == "hornillo":
        PENSAMIENTO: El cuaderno, al hornillo. Ya no tengo otro sitio. # id:j11_07_arrancar_hornillo
    }
* [Dejarlo.]
    PENSAMIENTO: No. Sigue siendo su cara. Aunque no lo sea. # id:j11_07_dejar
- -> DONE

// J11.08 — Fragmento IV: alguien ha dejado unas hojas entre las páginas del diario
=== j11_fragmento ===
~ fragmento_4 = true
PENSAMIENTO: Entre las páginas del cuaderno, unas hojas mecanografiadas que no estaban ahí. # id:j11_08_pens_00
PENSAMIENTO: ¿Quién…? ¿Cuándo…? # esperar:1 # id:j11_08_pens_01
PENSAMIENTO: Los proles también limpian. # esperar:1 # id:j11_08_pens_02
PENSAMIENTO: No. Aquí no limpia nadie. Alguien que sabe cuándo no mira. # id:j11_08_pens_03
PENSAMIENTO: «Un reloj parado es un acto de rebeldía.» # minijuego:libro,fragmento=4 # id:j11_08_pens_04
~ libro_fragmentos = 4
~ diario_libro_pasado = true
{ not (inventario ? libro):
    ~ inventario += libro
}
{ inventario ? reloj_ivy:
    PENSAMIENTO: Saco el reloj de Ivy. Nunca le di cuerda. Pensé que era por pena. # esperar:1 # id:j11_08_reloj_01
    PENSAMIENTO: Era otra cosa. # id:j11_08_reloj_02
- else:
    PENSAMIENTO: Nunca le di cuerda al reloj de Ivy. Pensé que era por pena. Era otra cosa. # id:j11_08_reloj_03
}
->->

=== j11_dormir ===
~ nueva_jornada(12)
~ desayunado = false
CARTEL: JORNADA 12 # fx:negro # sfx:silbato # id:j11_08_jornada12
CARTEL: La oferta. # id:j11_08_fin # escena:piso # pos:cama
-> DONE
