persona(X) :- madre(X, Y), persona(Y).
persona(ana).
madre(eva, ana).