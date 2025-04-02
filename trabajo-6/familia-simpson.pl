mujer([marge, patty, selma, lisa, jacqueline, ling, mona, maggie]).
hombre([herbert, abraham, clancy, bart, homero]).

es_mujer(X) :- mujer(L), member(X, L).
es_hombre(X) :- hombre(L), member(X, L).

padre_de(abraham, [homero, herbert]).
padre_de(clancy, [marge, patty, selma]).
padre_de(homero, [bart, lisa, maggie]).

madre_de(mona, [homero, herbert]).
madre_de(jacqueline, [marge, selma, patty]).
madre_de(marge, [lisa, bart, maggie]).
madre_de(selma, [ling]).  % Se coloca ling entre corchetes para mantener la consistencia

abuelo_de(X, Y) :- 
    es_hombre(X), 
    (padre_de(X, Hijos) ; madre_de(X, Hijos)), 
    member(Z, Hijos),
    (padre_de(Z, Nietos) ; madre_de(Z, Nietos)),
    member(Y, Nietos).

abuela_de(X, Y) :- 
    es_mujer(X), 
    madre_de(X, Hijos), 
    member(Z, Hijos),
    (padre_de(Z, Nietos) ; madre_de(Z, Nietos)),
    member(Y, Nietos).

hermana_de(X, Y) :- 
    es_mujer(X), 
    ((padre_de(P, Hijos), member(X, Hijos), member(Y, Hijos));
     (madre_de(M, Hijos), member(X, Hijos), member(Y, Hijos))),
    X \= Y.

hermano_de(X, Y) :- 
    es_hombre(X), 
    ((padre_de(P, Hijos), member(X, Hijos), member(Y, Hijos));
     (madre_de(M, Hijos), member(X, Hijos), member(Y, Hijos))),
    X \= Y.

tio_de(X, Y) :- 
    es_hombre(X), 
    hermano_de(X, Z), 
    ((padre_de(Z, Hijos), member(Y, Hijos));
     (madre_de(Z, Hijos), member(Y, Hijos))).

tia_de(X, Y) :- 
    es_mujer(X), 
    hermana_de(X, Z), 
    ((padre_de(Z, Hijos), member(Y, Hijos));
     (madre_de(Z, Hijos), member(Y, Hijos))).