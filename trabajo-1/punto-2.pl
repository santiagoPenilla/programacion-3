% Hechos
americano(colonel_west).
enemigo(corea_sur, eeuu).

misil(m1).

posee(corea_sur, m1).

vendio(colonel_west, m1, corea_sur).

% Reglas
arma(X) :- misil(X).

hostil(X) :- enemigo(X, eeuu).

criminal(X) :-
    americano(X),
    vendio(X, W, C),
    arma(W),
    hostil(C).
