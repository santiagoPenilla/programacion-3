Dom=set(range(1,10)) # Dominio de valores

Idcols="ABCDEFGHI" # Identificadores de columnas

import itertools as it
Varkeys = list(it.product(Dom,Idcols)) # Generamos todas las combinaciones de valores y columnas

strVarkeys=[f"{key[1]}{key[0]}" for key in Varkeys] # Convertimos las combinaciones a un formato de string para las variables

VarDoms={key:Dom.copy() for key in strVarkeys} # Creamos un diccionario donde cada variable tiene como dominio el conjunto de valores del sudoku

# Directorio del tablero a resolver
#boardname="SD2MFXKY-facil"
#boardname = "SD3CJFOG-moderado" 
#boardname= "SD8RXDKO-extremo"
boardname = "SD9LHPLL-imposible"

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

# Nuevas restricciones
def hidden_single(units, VarDoms):
    changed = False
    for unit in units:
        for val in Dom:
            possibles = [v for v in unit if val in VarDoms[v]]
            if len(possibles) == 1:
                var = possibles[0]
                if VarDoms[var] != {val}:
                    VarDoms[var] = {val}
                    changed = True
    return changed

def naked_subsets(units, VarDoms, size):
    changed = False
    for unit in units:
        candidates = [v for v in unit if 1 < len(VarDoms[v]) <= size]
        for subset in it.combinations(candidates, size):
            values = set()
            for var in subset:
                values |= VarDoms[var]
            if len(values) == size:
                for var in unit:
                    if var not in subset:
                        before = VarDoms[var].copy()
                        VarDoms[var] -= values
                        if VarDoms[var] != before:
                            changed = True
    return changed

def hidden_subsets(units, VarDoms, size):
    changed = False
    for unit in units:
        for values in it.combinations(Dom, size):
            values = set(values)
            related = [v for v in unit if VarDoms[v] <= values]
            if len(related) == size:
                for var in related:
                    before = VarDoms[var].copy()
                    VarDoms[var] &= values
                    if VarDoms[var] != before:
                        changed = True
    return changed

def pointing(VarDoms, rows, cols, boxes):
    changed = False
    for box in boxes:
        for val in Dom:
            vars_with_val = [v for v in box if val in VarDoms[v]]
            if 1 < len(vars_with_val) <= 3:
                row_ids = {v[1] for v in vars_with_val}
                col_ids = {v[0] for v in vars_with_val}

                if len(row_ids) == 1:
                    row = int(row_ids.pop()) - 1
                    for v in rows[row]:
                        if v not in box and val in VarDoms[v]:
                            VarDoms[v].discard(val)
                            changed = True

                if len(col_ids) == 1:
                    col = Idcols.index(col_ids.pop())
                    for v in cols[col]:
                        if v not in box and val in VarDoms[v]:
                            VarDoms[v].discard(val)
                            changed = True
    return changed

def x_wing(VarDoms, rows):
    changed = False
    for val in Dom:
        row_map = {}
        for r in range(9):
            row_map[r] = [v for v in rows[r] if val in VarDoms[v]]
        valid = [(r, vs) for r, vs in row_map.items() if len(vs) == 2]

        for (r1, pair1), (r2, pair2) in it.combinations(valid, 2):
            if pair1 == pair2:
                c1 = Idcols.index(pair1[0][0])
                c2 = Idcols.index(pair1[1][0])
                for r in set(range(9)) - {r1, r2}:
                    for c in [c1, c2]:
                        v = f"{Idcols[c]}{r+1}"
                        if val in VarDoms[v]:
                            VarDoms[v].discard(val)
                            changed = True
    return changed

def swordfish(VarDoms, rows):
    changed = False
    for val in Dom:
        row_map = {}
        for r in range(9):
            vars_with_val = [v for v in rows[r] if val in VarDoms[v]]
            if 2 <= len(vars_with_val) <= 3:
                row_map[r] = vars_with_val

        for triple in it.combinations(row_map.items(), 3):
            cols_in_triple = [set(Idcols.index(v[0]) for v in vs) for _, vs in triple]
            common = set.intersection(cols_in_triple[0], cols_in_triple[1], cols_in_triple[2])

            if len(common) == 3:
                rows_used = {r for r, _ in triple}
                for r in set(range(9)) - rows_used:
                    for c in common:
                        v = f"{Idcols[c]}{r+1}"
                        if val in VarDoms[v]:
                            VarDoms[v].discard(val)
                            changed = True
    return changed

# Implementación de forward checking
def forward_checking_search(VarDoms, Constraints):
    vars_list = list(VarDoms.keys())

    def recursive_fc_solver(i):
        if i == len(vars_list):
            return True

        xi = vars_list[i]
        for ai in list(VarDoms[xi]):
            saved_domains = {v: VarDoms[v].copy() for v in VarDoms}
            VarDoms[xi] = {ai}

            failed = False
            for constraint in Constraints:
                if xi in constraint:
                    for xj in constraint:
                        if xj != xi:
                            VarDoms[xj].discard(ai)
                            if not VarDoms[xj]:
                                failed = True
                                break
                    if failed:
                        break

            if not failed:
                if recursive_fc_solver(i + 1):
                    return True

            for v in saved_domains:
                VarDoms[v] = saved_domains[v]

        return False

    return recursive_fc_solver(0)

cols = defColsConstraints(Idcols, Dom)
rows = defRowsConstraints(Idcols, Dom)
boxes = defBoxesContraints(Idcols, Dom)

# bucle de propagación
anyChange = True
while anyChange:
    anyChange = False
    anyChange |= ConsistenceDifference(Constraints, VarDoms)
    anyChange |= ConsistenceDomsEqual2(Constraints, VarDoms)
    anyChange |= hidden_single(Constraints, VarDoms)
    anyChange |= naked_subsets(Constraints, VarDoms, 2)
    anyChange |= naked_subsets(Constraints, VarDoms, 3)
    anyChange |= hidden_subsets(Constraints, VarDoms, 2)
    anyChange |= hidden_subsets(Constraints, VarDoms, 3)
    anyChange |= pointing(VarDoms, rows, cols, boxes)
    anyChange |= x_wing(VarDoms, rows)
    anyChange |= swordfish(VarDoms, rows)

# Imprimir el tablero con formato
def print_sudoku(VarDoms):
    for i in range(1, 10):
        fila = ""
        for j in "ABCDEFGHI":
            var = f"{j}{i}"
            val = VarDoms[var]
            if len(val) == 1:
                fila += str(next(iter(val))) + " "
            else:
                fila += ". "
            if j in "C" or j == "F":
                fila += "| "
        print(fila.strip())
        if i in [3, 6]:
            print("-" * 21)

if forward_checking_search(VarDoms, Constraints):
    print_sudoku(VarDoms)
else:
    print("No existe ninguna solución para este tablero.")