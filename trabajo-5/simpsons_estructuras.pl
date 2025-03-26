mujer([marge,patty,selma,lisa,jacqueline,ling,mona,maggie]).

hombre([herbert,abraham,clancy,bart,homero]).

padre_de(abraham,[homero,herbert]).
padre_de(clancy,[marge,patty,selma]).
padre_de(homero,[bart,lisa,maggie]).

madre_de(mona,[homero,herbert]).
madre_de(jacqueline,[marge,selma,patty]).
madre_de(marge, [lisa,bart,maggie]).
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

hermano_de(X,Y) :- 
    hombre(L),member(X,L),
    padre_de(_,H),member(X,H),member(Y,H),
    madre_de(_,H1),member(X,H1),member(Y,H1).
	

tio_de(X, Y) :- hombre(X), hermano_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).
tia_de(X, Y) :- mujer(X), hermana_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).
