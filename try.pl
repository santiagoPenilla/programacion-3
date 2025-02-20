% Hechos
parent(juan, maria).
parent(juan, jose).
parent(maria, carla).

% Regla para encontrar abuelos
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).
