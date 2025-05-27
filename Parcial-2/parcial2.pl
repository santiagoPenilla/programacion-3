personas([
    miembro(
        nombre(homero),
        [nombre(bart), nombre(lisa), nombre(maggie)],
        [
            evento(tipo(nacimiento), año(1956)),
            evento(tipo(graduacion), año(1974)),
            evento(tipo(boda), año(1980)),
            evento(tipo(trabajo_planta), año(1980)),
            evento(tipo(torneo_bolos), año(1990)),
            evento(tipo(gira_rock), año(1993)),
            evento(tipo(astronauta), año(1994)),
            evento(tipo(despido), año(1995))
        ]
    ),
           
    miembro(
        nombre(marge),
        [nombre(bart), nombre(lisa), nombre(maggie)],
        [
            evento(tipo(nacimiento), año(1958)),
            evento(tipo(graduacion), año(1976)),
            evento(tipo(boda), año(1980)),
            evento(tipo(hobby), año(1992)),
            evento(tipo(arresto), año(1993)),
            evento(tipo(hospitalizacion), año(1997)),
            evento(tipo(protagonista), año(2001))
        ]
    ),
           
    miembro(
        nombre(lisa),
        [],
        [
            evento(tipo(nacimiento), año(1982)),
            evento(tipo(saxofon), año(1988)),
            evento(tipo(honores), año(1993)),
            evento(tipo(mentor), año(1994)),
            evento(tipo(vegetariana), año(1995)),
            evento(tipo(premio_ensayo), año(1997)),
            evento(tipo(presidenta), año(2010))
        ]
    ),

    miembro(
        nombre(bart),
        [],
        [
            evento(tipo(nacimiento), año(1980)),
            evento(tipo(castigo), año(1990)),
            evento(tipo(revolucion), año(1991)),
            evento(tipo(estrella_tv), año(1993)),
            evento(tipo(heroico), año(1995)),
            evento(tipo(deporte), año(1999)),
            evento(tipo(expulsion), año(2000))
        ]
    ),

    miembro(
        nombre(maggie),
        [],
        []
    )
]).

linea_de_descendencia(Nombre, Descendientes):-  
    personas(Familia),
    member(miembro(nombre(Nombre), Descendientes, _), Familia), !.

evento_mas_reciente(Persona, EventoReciente):-  
    personas(Familia),
    member(miembro(nombre(Persona), _, Eventos), Familia),
    max_evento(Eventos, EventoReciente), !.

historia_familiar(Nombre, EventosOrdenados) :-  
    personas(Familia),
    member(miembro(nombre(Nombre), Hijos, EventosPersonales), Familia),
    eventos_de_hijos(Hijos, Familia, EventosHijos),
    append(EventosPersonales, EventosHijos, TodosEventos),
    ordenar_eventos(TodosEventos, EventosOrdenados), !.

max_evento([Ultimo], Ultimo).
max_evento([evento(Tipo1, año(Año1)) | Resto], EventoMaximo) :-  
    max_evento(Resto, evento(Tipo2, año(Año2))),
    comparar_eventos(evento(Tipo1, año(Año1)), evento(Tipo2, año(Año2)), EventoMaximo).

comparar_eventos(evento(Tipo1, año(Año1)), evento(_, año(Año2)), evento(Tipo1, año(Año1))) :-  
    Año1 >= Año2.

comparar_eventos(evento(_, año(Año1)), evento(Tipo2, año(Año2)), evento(Tipo2, año(Año2))) :-  
    Año1 < Año2.

eventos_de_hijos([], _, []).

eventos_de_hijos([nombre(Hijo)|RestoHijos], Familia, EventosTotales) :-  
    member(miembro(nombre(Hijo), _, Eventos), Familia),
    eventos_de_hijos(RestoHijos, Familia, EventosRestantes),
    append(Eventos, EventosRestantes, EventosTotales).

ordenar_eventos(Eventos, Ordenados) :-  
    predsort(comparar_anos, Eventos, Ordenados).

comparar_anos(Orden, evento(_, año(Año1)), evento(_, año(Año2))) :-  
    compare(Orden, Año1, Año2).
