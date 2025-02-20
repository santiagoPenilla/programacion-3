
padre_de(abraham,homero).
padre_de(abraham,herbert).
padre_de(clancy,marge).
padre_de(clancy,patty).
padre_de(clacy,selma).
padre_de(homero,bart).
padre_de(homero,lisa).
padre_de(homero,maggie).
madre_de(mona,homero).
madre_de(mona,herbert).
madre_de(jacqueline,marge).
madre_de(jacqueline,selma).
madre_de(jacqueline,patty).
madre_de(marge,lisa).
madre_de(marge,bart).
madre_de(marge,maggie).
madre_de(selma,ling).

abuelo_de(X,Y):-padre_de(Z,Y),padre_de(X,Z).
abuela_de(X,Y):-madre_de(X,Z),madre_de(Z,Y).
hermana_de(X,Y):-(madre_de(Z,X),madre_de(Z,Y)),(padre_de(F,X),padre_de(F,Y)).
hermano_de(X,Y):-(madre_de(Z,X),madre_de(Z,Y)),(padre_de(F,X),padre_de(F,Y)).
