Dom=set(range(1,10)) # Dominio de valores

Idcols="ABCDEFGHI" # Identificadores de columnas

import itertools as it
Varkeys = list(it.product(Dom,Idcols)) # Generamos todas las combinaciones de valores y columnas

strVarkeys=[f"{key[1]}{key[0]}" for key in Varkeys] # Convertimos las combinaciones a un formato de string para las variables

VarDoms={key:Dom.copy() for key in strVarkeys} # Creamos un diccionario donde cada variable tiene como dominio el conjunto de valores del sudoku

boardname="SD2MFXKY-facil" # Directorio del tablero a resolver

with open(boardname, "r") as archivo:
    for clave in VarDoms:
        linea = archivo.readline().strip()
        if linea.isdigit() and len(linea)==1:
          linea = {int(linea)}
          VarDoms[clave] = linea

"""Añadimos Restricciones"""

# Restricciones de columnas
def defColsConstraints(IdCols,Dom):
  Constraints=[]
  for id in IdCols:
    ConstraintVars=[f"{id}{i}" for i in Dom]
    Constraints.append(ConstraintVars)
  return Constraints

# Restricciones de filas
def defRowsConstraints(IdCols,Dom):
  Constraints=[]
  for i in Dom:
    ConstraintVars=[f"{id}{i}" for id in IdCols]
    Constraints.append(ConstraintVars)
  return Constraints

# Restricciones de cajas
def defBoxesContraints(IdCols,Dom):
    allBoxes = []
    for row_start in range(1, 10, 3):
        for col_start in range(0, 9, 3):
            varsBox = []
            for i in range(3):
                for j in range(3):
                    row = row_start + i
                    col = IdCols.index(IdCols[col_start]) + j
                    varsBox.append(f"{IdCols[col]}{row}")
            allBoxes.append(varsBox)
    return allBoxes

# Definimos las restricciones
Constraints= defColsConstraints(Idcols,Dom) + defRowsConstraints(Idcols,Dom) + defBoxesContraints(Idcols,Dom)

# Definimos las restricciones de consistencia
def ConsistenceDifference(Constraints,VarDoms):
  anyChange = False
  for constraint in Constraints:
    for var in constraint:
      if len(VarDoms[var])==1:
        for othervar in constraint:
          if othervar!=var:
            oldDom=VarDoms[othervar].copy()
            VarDoms[othervar].difference_update(VarDoms[var])
            if oldDom!=VarDoms[othervar]:
              anyChange=True
  return anyChange

def ConsistenceDomsEqual2(Constraints,VarDoms):
  anyChange=False
  for Constraint in Constraints:
    for var1 in Constraint:
      if len(VarDoms[var1])==2:
        for var2 in Constraint:
          if not(var1==var2):
            if VarDoms[var1]==VarDoms[var2]:
              for var3 in Constraint:
                if not(var1==var3) and not(var2==var3):
                  oldValue=VarDoms[var3].copy()
                  VarDoms[var3].discard(list(VarDoms[var1])[0])
                  VarDoms[var3].discard(list(VarDoms[var1])[1])
                  if not(oldValue==VarDoms[var3]):
                    anyChange=True
  return anyChange

def DomsEqual(Vars,constraint):
  anyChange=False
  varsEquals={}
  for var1 in constraint:
    if len(Vars[var1])>1:
      for var2 in constraint:
        if not(var1==var2):
          if (Vars[var1]==Vars[var2]):
            if tuple(Vars[var1]) in varsEquals:
              Set_aux=set(varsEquals[tuple(Vars[var1])].copy())
              Set_aux.add(var1)
              Set_aux.add(var2)
              varsEquals[tuple(Vars[var1])]=list(Set_aux)
            else:
              varsEquals[tuple(Vars[var1])]=[var1,var2]
  for domVar in varsEquals:
    if len(domVar)==len(varsEquals[domVar]):
      for var in constraint:
        if not(var in varsEquals[domVar]):
          for value in domVar:
            oldValue=Vars[var].copy()
            Vars[var].discard(value)
            if not(oldValue==Vars[var]):
              anyChange=True
  return anyChange

anyChange = True
iteration = 1
while anyChange:
  iteration += 1
  anyChange = ConsistenceDifference(Constraints,VarDoms)
  anyChange |= ConsistenceDomsEqual2(Constraints,VarDoms)

for var in VarDoms:
  print(f"{var}: {VarDoms[var]}")