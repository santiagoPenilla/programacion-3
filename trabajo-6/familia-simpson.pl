es_mujer(X):- 
    member(X, [mujer(jacqueline), mujer(ling), mujer(lisa), mujer(maggie), mujer(marge), mujer(mona), mujer(patty), mujer(selma)]).

es_hombre(X):- 
    member(X, [hombre(abraham), hombre(bart), hombre(clancy), hombre(herbert), hombre(homero)]).

madre_de(X,Y):- 
    member((X,Y),
    [(mujer(marge), hombre(bart)), (mujer(marge), mujer(lisa)), (mujer(marge), mujer(maggie)), 
     (mujer(mona), hombre(herbert)), (mujer(mona), hombre(homero)), 
     (mujer(jacqueline), mujer(marge)), (mujer(jacqueline), mujer(patty)), (mujer(jacqueline), mujer(selma)), 
     (mujer(selma), mujer(ling))]).

padre_de(X,Y):- 
    member((X,Y),
    [(hombre(homero), hombre(bart)), (hombre(homero), mujer(lisa)), (hombre(homero), mujer(maggie)), 
     (hombre(abraham), hombre(herbert)), (hombre(abraham), hombre(homero)),
     (hombre(clancy), mujer(marge)), (hombre(clancy), mujer(patty)), (hombre(clancy), mujer(selma))]).

abuela_de(X, Z) :- madre_de(X, Y), (padre_de(Y, Z) ; madre_de(Y, Z)).
abuelo_de(X, Z) :- padre_de(X, Y), (padre_de(Y, Z) ; madre_de(Y, Z)).

dif(A, B):- A \== B.

hermano_de(X, Y) :- 
    es_hombre(X), dif(X,Y),
    (padre_de(Z, X), padre_de(Z, Y));
    (madre_de(Z, X), madre_de(Z, Y)), es_hombre(X), dif(X,Y).

hermana_de(X, Y) :- 
    es_mujer(X), dif(X,Y),
    (padre_de(Z, X), padre_de(Z, Y));
    (madre_de(Z, X), madre_de(Z, Y)), es_mujer(X), dif(X,Y).

tia_de(X, Z) :-  
    es_mujer(X), 
    hermana_de(X, Y), 
    (padre_de(Y, Z) ; madre_de(Y, Z)).

tio_de(X, Z) :-  
    es_hombre(X), 
    hermano_de(X, Y), 
    (padre_de(Y, Z) ; madre_de(Y, Z)).

prima_de(X, Z) :- 
    (tio_de(Y, Z) ; tia_de(Y, Z)),  
    (madre_de(Y, X) ; padre_de(Y, X)), 
    es_mujer(X).

primo_de(X, Z) :- 
    (tio_de(Y, Z) ; tia_de(Y, Z)),  
    (madre_de(Y, X) ; padre_de(Y, X)), 
    es_hombre(X).
