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

=== function baja_sospecha(n) ===
~ sospecha = limitar(sospecha - n)
