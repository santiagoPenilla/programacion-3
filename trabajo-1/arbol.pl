mujer(marge).
mujer(patty).
mujer(selma).
mujer(lisa).
mujer(jacqueline).
mujer(ling).
mujer(mona).
mujer(maggie).

hombre(homero).
hombre(herbert).
hombre(abraham).
hombre(clancy).
hombre(bart).

padre_de(abraham, homero).
padre_de(abraham, herbert).
padre_de(clancy, marge).
padre_de(clancy, patty).
padre_de(clancy, selma).
padre_de(homero, bart).
padre_de(homero, lisa).
padre_de(homero, maggie).
madre_de(mona, homero).
madre_de(mona, herbert).
madre_de(jacqueline, marge).
madre_de(jacqueline, selma).
madre_de(jacqueline, patty).
madre_de(marge, lisa).
madre_de(marge, bart).
madre_de(marge, maggie).
madre_de(selma, ling).

abuelo_de(X, Y) :- 
    hombre(X), 
    (padre_de(X, Z) ; madre_de(X, Z)), 
    (padre_de(Z, Y) ; madre_de(Z, Y)).

abuela_de(X, Y) :- 
    mujer(X), 
    madre_de(X, Z), 
    (padre_de(Z, Y) ; madre_de(Z, Y)).

hermana_de(X, Y) :- 
    mujer(X), 
    ((padre_de(P, X), padre_de(P, Y)) ; 
    (madre_de(M, X), madre_de(M, Y))).

hermano_de(X, Y) :- 
    hombre(X),  
    ((padre_de(P, X), padre_de(P, Y)) ; 
    (madre_de(M, X), madre_de(M, Y))).

tio_de(X, Y) :- hombre(X), hermano_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).
tia_de(X, Y) :- mujer(X), hermana_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).

