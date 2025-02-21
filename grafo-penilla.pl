viaja_a(edmonton,saskatoon,12).
viaja_a(saskatoon,winnipeg,20).
viaja_a(saskatoon,calgary,9).
viaja_a(vancouver,edmonton,16).
viaja_a(vancouver,calgary,13).
viaja_a(calgary,regina,14).
viaja_a(regina,winnipeg,4).
viaja_a(regina,saskatoon,7).

%reglas
conexion(X, Y, F) :- viaja_a(X, Y, F).
conexion(X, Y, F) :- viaja_a(Y, X, F).
tiene_aristas(X, Y) :- viaja_a(X, Y, _);viaja_a(Y, X, _).
viaje_x_a_z(X,Y,Z):- 