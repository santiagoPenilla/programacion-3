%nota(X, suspenso) :- X < 5.
%nota(X, aprobado) :- X >= 5, X < 7.
%nota(X, notable) :- X >= 7, X < 9.
%nota(X, sobresaliente) :- X >= 9.

nota(X, suspenso) :- X < 5, !.
nota(X, aprobado) :- X < 7, !.
nota(X, notable) :- X < 9, !.
nota(_, sobresaliente).