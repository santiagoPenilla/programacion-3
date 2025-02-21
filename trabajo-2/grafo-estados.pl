% Hechos
viajar_a(vancouver, edmonton, 16).
viajar_a(vancouver, calgary, 13).
viajar_a(edmonton, saskatoon, 12).
viajar_a(calgary, edmonton, 14).
viajar_a(calgary, regina, 14).
viajar_a(saskatoon, calgary, 20).
viajar_a(saskatoon, winnipeg, 9).
viajar_a(regina, winnipeg, 7).
viajar_a(regina, saskatoon, 7).

% Reglas
conexion(X, Y, C) :- viajar_a(X, Y, C).
conexion(X, Y, C) :- viajar_a(Y, X, C).

tiene_aristas(Sitio) :- viajar_a(Sitio, _, _); viajar_a(_, Sitio, _).