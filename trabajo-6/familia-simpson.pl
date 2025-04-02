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
madre_de(selma, [ling]).