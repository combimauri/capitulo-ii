// ACTO III · Lo que se repite cada día: el cartel de Ivy, por la mañana y por la noche.

=== j8_cartel_manana ===
{ cartel_arrancado:
    PENSAMIENTO: La pared desnuda. La mancha más clara tiene su forma. # id:j12_00_cartel_mancha
    -> DONE
}
{ jornada:
- 8:
    PENSAMIENTO: Esta noche, Ivy. # id:j8_01_cartel
- 9:
    PENSAMIENTO: «Kent está en Oceanía.» Tú lo sabías, ¿verdad? # id:j9_01_cartel
- 10:
    PENSAMIENTO: Hoy te pondrán en todas las paredes. # id:j10_01_cartel
- 11:
    PENSAMIENTO: Buenos días, Ivy. # id:j11_00_cartel
- else:
    PENSAMIENTO: Hoy no te miro. # id:j12_00_cartel
}
-> DONE

=== j8_cartel_noche ===
{ jornada == 11:
    -> j11_cartel_mirar
}
{ jornada:
- 8:
    PENSAMIENTO: «¿Estás dispuest{o} a que tu hermana deje de ser una mártir?» # esperar:1 # id:j8_10_cartel_01
    PENSAMIENTO: Ya no lo es. Ahora es otra cosa. No sé qué. # esperar:1 # id:j8_10_cartel_02
    PENSAMIENTO: Ya no sé quién eras. # id:j8_10_cartel_03
- 9:
    PENSAMIENTO: ¿Qué documentos, Ivy? ¿Qué escribías? # id:j9_08_cartel
- else:
    PENSAMIENTO: Ivy murió por Eurasia. Ahora Ivy murió por Estasia. # id:j10_06_cartel
}
-> DONE
