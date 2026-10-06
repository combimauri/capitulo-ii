=== function fijar_genero(gen) ===
~ genero = gen
{ gen == "f":
    ~ o = "a"
    ~ a_ = "a"
    ~ el = "la"
    ~ El = "La"
    ~ un = "una"
    ~ del_ = "de la"
    ~ lo_ = "la"
- else:
    ~ o = "o"
    ~ a_ = ""
    ~ el = "el"
    ~ El = "El"
    ~ un = "un"
    ~ del_ = "del"
    ~ lo_ = "lo"
}

// Para casos raros: {g("varón", "mujer")}
=== function g(m, f) ===
{ genero == "f":
    ~ return f
}
~ return m

=== function limitar(x) ===
{ x < 0:
    ~ return 0
}
{ x > 100:
    ~ return 100
}
~ return x

=== function sube_duda(n) ===
~ duda = limitar(duda + n)

=== function baja_duda(n) ===
~ duda = limitar(duda - n)

=== function sube_sospecha(n) ===
~ sospecha = limitar(sospecha + n)

// Al ser visto en una misión de sigilo. Con la penalización reducida (opciones), sube la mitad.
=== function sube_sospecha_sigilo(n) ===
{ opc_sigilo_reducido:
    ~ sube_sospecha(n / 2)
- else:
    ~ sube_sospecha(n)
}

=== function baja_sospecha(n) ===
~ sospecha = limitar(sospecha - n)
// si el Comité leyó el diario, la Sospecha ya no baja de 40 (guion J6.05), aunque Nell lo recupere
{ comite_leyo and sospecha < 40:
    ~ sospecha = 40
}

// Un día nuevo (equilibrio, M7): desde el Acto II, el Partido mira un poco menos a quien no ha hecho nada.
// La Sospecha baja ALIVIO_JORNADA al empezar cada jornada (respeta el suelo de 40 si el Comité leyó el diario).
CONST ALIVIO_JORNADA = 5
=== function nueva_jornada(n) ===
~ jornada = n
{ n >= 5:
    ~ baja_sospecha(ALIVIO_JORNADA)
}
