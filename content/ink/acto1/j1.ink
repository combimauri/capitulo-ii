// ACTO I · JORNADA 1 — La rutina (guion: docs/guion-detallado/01-acto-1.md)

=== j1_01 ===
# escena:piso # pos:cama # jornada:1
TELEPANTALLA: ¡Buenos días, camaradas de entre treinta y cuarenta! ¡Arriba, arriba! ¡Tablas de gimnasia! # id:j1_01_tp_01
CARTEL: [Aquí irá el microjuego de crimen facial: la gimnasia matinal.] # id:j1_01_cartel_cf
TELEPANTALLA: ¡{num} {apellido}! ¡Eso es! ¡Así se mueve {un} camarada de verdad! ¡Mirad todos! # id:j1_01_tp_02
PENSAMIENTO: Me ha nombrado. Delante de todo el bloque. # id:j1_01_pens_01
-> DONE

// ------------------------------------------------------------------ puntos interactivos del piso
=== piso ===

= cartel_mirar
PENSAMIENTO: Ivy. Cada mañana te lo prometo. Cada mañana. Eurasia pagará cada piedra de la calle Stepney. # id:piso_cartel_mirar
-> DONE

= cartel_usar
PENSAMIENTO: Nunca la dibujaron sonriendo. Ella siempre sonreía. # id:piso_cartel_usar_01
PENSAMIENTO: Pero así está bien: una mártir no sonríe. # id:piso_cartel_usar_02
-> DONE

= reloj_mirar
PENSAMIENTO: Las nueve y cuarenta. Nunca le he dado cuerda. No quiero que vuelva a andar. # id:piso_reloj_mirar
-> DONE

= reloj_usar
PENSAMIENTO: No. Se queda así. # id:piso_reloj_usar
-> DONE

= tele_mirar
PENSAMIENTO: Se le puede bajar el volumen, pero no apagarla. Nadie querría apagarla. Sería como quedarse a oscuras. # id:piso_tele_mirar
-> DONE

= tele_usar
PENSAMIENTO: El volumen. # id:piso_tele_usar_01
* [Subirlo]
    ~ tele_volumen = 1
    TELEPANTALLA: …la producción de botas en el último trimestre ha superado el plan en un noventa y ocho por ciento… # id:piso_tele_usar_02
    PENSAMIENTO: Noventa y ocho por ciento. Algún día todos tendremos botas. # id:piso_tele_usar_03
* [Bajarlo]
    ~ tele_volumen = -1
    ~ sube_sospecha(2)
    PENSAMIENTO: Un poco. Solo un poco. Para oír el hervidor. # id:piso_tele_usar_04
    TELEPANTALLA: …camarada {apellido}, recuerde que el volumen recomendado favorece la concentración… # id:piso_tele_usar_05
* [Dejarlo como está]
    PENSAMIENTO: Está en el volumen justo. El Partido sabe cuál es el volumen justo. # id:piso_tele_usar_06
- -> DONE

= ventana_mirar
PENSAMIENTO: Los cuatro ministerios. El de la Verdad, el del Amor, el de la Abundancia. # id:piso_ventana_mirar_01
PENSAMIENTO: Y el mío: el de la Paz. Desde aquí parecen montañas. # id:piso_ventana_mirar_02
-> DONE

= hornillo_mirar
PENSAMIENTO: El hornillo. Una sola llama, como todos los hornillos del bloque. # id:piso_hornillo_mirar
-> DONE

= hornillo_usar
{ desayunado:
    PENSAMIENTO: Ya he desayunado. Repetir sería acaparar. # id:piso_hornillo_usar_01
- else:
    ~ desayunado = true
    PENSAMIENTO: Café de la Victoria. Sabe a tierra mojada. # id:piso_hornillo_usar_02
    PENSAMIENTO: Pero está caliente, y eso es más de lo que tienen en Eurasia. # id:piso_hornillo_usar_03
}
-> DONE

= cama_mirar
PENSAMIENTO: La cama está hecha. Una cama deshecha es una mente deshecha. # id:piso_cama_mirar
-> DONE

= abrigo_mirar
PENSAMIENTO: Mi abrigo. Gris, como todos los abrigos. Abriga lo justo. # id:piso_abrigo_mirar
-> DONE

= armario_mirar
PENSAMIENTO: Dos monos azules, una camisa, el abrigo de invierno. Todo lo que necesito. # id:piso_armario_mirar
-> DONE

= puerta_usar
{ not desayunado:
    PENSAMIENTO: Primero el desayuno. Un estómago vacío es un estómago desleal. # id:piso_puerta_usar_01
    -> DONE
}
CARTEL: Fin de la demo técnica. La escalera de las Mansiones Victoria llegará con el corte vertical. # id:piso_puerta_fin # escena:escalera
-> DONE
