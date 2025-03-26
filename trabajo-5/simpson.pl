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
    hombre(Z), member(X,Z),
    padre_de(X,Hijos),member(Padres,Hijos),
    padre_de(Padres,Nietos),member(Y,Nietos).


abuela_de(X, Y) :- 
    mujer(Z), member(X,Z),
    madre_de(X,Hijos),member(Padres,Hijos),
    (madre_de(Padres,Nietos);padre_de(Padres,Nietos)),member(Y,Nietos).

hermana_de(X, Y) :- 
    mujer(F),member(X,F),
    padre_de(_,H),member(X,H),member(Y,H);
    madre_de(_,H1),member(X,H1),member(Y,H1). 

hermano_de(X,Y) :- 
    hombre(L),member(X,L),
    padre_de(_,H),member(X,H),member(Y,H);
    madre_de(_,H1),member(X,H1),member(Y,H1).
	

tio_de(X, Y) :- hombre(X), hermano_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).
tia_de(X, Y) :- mujer(X), hermana_de(X, Z), (padre_de(Z, Y) ; madre_de(Z, Y)).

