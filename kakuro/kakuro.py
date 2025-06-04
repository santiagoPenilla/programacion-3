import re
from table import BY_SUM

colum_labels = "ABCDEFGHI"
initial_domain = { i for i in range(1, 10) } 

def get_doms(kakuro):
    domains = {}
    for constraints in kakuro['constraints'].values():
        for cells, _ in constraints:
            for cell in cells:
                if cell not in domains:
                    domains[cell] = initial_domain.copy()
    return domains

def cels_range(start, end):
    cels = []
    if start[0] != end[0]:
        current_col = colum_labels.index(start[0])
        end_col = colum_labels.index(end[0])
        for i in range(current_col, end_col + 1):
            cels.append(colum_labels[i] + start[1:])
    else:
        current_row = int(start[1])
        end_row = int(end[1])
        for i in range(current_row, end_row + 1):
            cels.append(start[0] + str(i))
    return cels

def read_kakuro(file):
    constraints = {}
    pat =  re.compile(r'^([A-Z]\d+):([x\d]+)\\([x\d]+)\((\d+)(?:,(\d+))?\)$')

    with open(file) as f:
        for line in f:
            if not line: continue
            line = line.strip().replace(' ', '')
            m = pat.match(line)
            
            cell, down_sum, right_sum, first_cnt, second_cnt = m.groups()
            constraint = []
            if right_sum == "x":
                start = cell[0] + str(int(cell[1]) + 1)
                end = cell[0] + str(int(cell[1]) + int(first_cnt))
                constraint.append((cels_range(start, end), int(down_sum)))
            elif down_sum == "x":
                index = colum_labels.index(cell[0])
                start = colum_labels[index + 1] + cell[1]
                end = colum_labels[index + int(first_cnt)] + cell[1]
                constraint.append((cels_range(start, end), int(right_sum)))
            else:
                start = cell[0] + str(int(cell[1]) + 1)
                end = cell[0] + str(int(cell[1]) + int(first_cnt))
                constraint.append((cels_range(start, end), int(down_sum)))
                index = colum_labels.index(cell[0])
                start = colum_labels[index + 1] + cell[1]
                end = colum_labels[index + int(second_cnt)] + cell[1]
                constraint.append((cels_range(start, end), int(right_sum)))
            constraints[cell] = constraint
    return constraints

def doms_rule(kakuro):
    for key, constraint in kakuro["constraints"].items():
        for cells, total in constraint:
            combinations = BY_SUM[total][len(cells)]
            dominio = set()
            if len(combinations) == 1:
                unique = combinations[0]
                dominio = {int(d) for d in unique}
            else:
                for combination in combinations:
                    dominio |= {int(d) for d in combination}
            for cell in cells:
                kakuro["domains"][cell] &= dominio

def propagate_uniques(kakuro):
    changed = False
    singles = {}
    for cell, domain in kakuro["domains"].items():
        if len(domain) == 1:
            singles[cell] = next(iter(domain))

    for clue_cell, constraint in kakuro["constraints"].items():
        for cells, _ in constraint:
            for cell,val in singles.items():
                if cell in cells:
                    for other in cells:
                        if other!=cell and val in kakuro["domains"][other]:
                            kakuro["domains"][other].remove(val)
                            changed = True
    return changed


def remaind_value(kakuro):
    changed = False
    for n, constraints in kakuro["constraints"].items():
        for cells, total in constraints:
            singletons = [c for c in cells if len(kakuro["domains"][c]) == 1]
            others = [c for c in cells if len(kakuro["domains"][c]) > 1]

            if len(others) == 1 and len(singletons) == len(cells) - 1:
                rem_cell = others[0]
                assigned_sum = sum(next(iter(kakuro["domains"][c])) for c in singletons)
                missing = total - assigned_sum

                if missing in kakuro["domains"][rem_cell] and kakuro["domains"][rem_cell] != {missing}:
                    kakuro["domains"][rem_cell] = {missing}
                    changed = True

    return changed

def reduce_by_Sum(kakuro):
    changed = False
    for key, constraint in kakuro["constraints"].items():
        for cells, total in constraint:
            combinations = BY_SUM[total][len(cells)]
            parsed = [{int(d) for d in combo} for combo in combinations]

            valid = [comb for comb in parsed
                     if all(any(v in kakuro["domains"][cell] for cell in cells) for v in comb)]

            if len(valid) < len(parsed):
                for cell in cells:
                    old_dom = kakuro["domains"][cell]
                    new_dom = set()
                    for comb in valid:
                        new_dom |= comb & old_dom
                    if new_dom != old_dom:
                        kakuro["domains"][cell] = new_dom
                        changed = True
    return changed

from itertools import combinations

def reduce_naked_tuples(kakuro):
    changed = False
    doms = kakuro["domains"]

    for constraint in kakuro["constraints"].values():
        for cells, n in constraint:
            n_cells = len(cells)
            for k in range(2, n_cells):
                cand = [c for c in cells if 2 <= len(doms[c]) <= k]
                for combo in combinations(cand, k):
                    union_vals = set()
                    for c in combo:
                        union_vals.update(doms[c])
                    if len(union_vals) == k:
                        for other in cells:
                            if other not in combo:
                                if doms[other] & union_vals:
                                    doms[other] -= union_vals
                                    changed = True
    return changed

def propagate_all(kakuro):
    changed = True
    while changed:
        changed = False
        changed |= propagate_uniques(kakuro)
        changed |= remaind_value(kakuro)
        changed |= reduce_by_Sum(kakuro)
        changed |= reduce_naked_tuples(kakuro)

def make_kakuro(file):
    kakuro = {}
    kakuro["constraints"] = read_kakuro(file)
    kakuro["domains"] = get_doms(kakuro)
    return kakuro

def is_solved(kakuro):
    return all(len(dom) == 1 for dom in kakuro["domains"].values())


def select_unassigned_cell(kakuro):
    min_size = 10
    chosen = None
    for cell, dom in kakuro["domains"].items():
        if 1 < len(dom) < min_size:
            min_size = len(dom)
            chosen = cell
    return chosen


def backtrack(kakuro):
    if is_solved(kakuro):
        return True

    cell = select_unassigned_cell(kakuro)
    if cell is None:
        return False

    domain_snapshot = kakuro["domains"][cell].copy()

    for val in list(domain_snapshot):
        domains_backup = { cell: dom.copy() 
                   for cell, dom in kakuro["domains"].items() }

        kakuro["domains"][cell] = {val}

        propagate_all(kakuro)

        contradiction = any(len(dom) == 0 for dom in kakuro["domains"].values())
        if not contradiction:
            if backtrack(kakuro):
                return True

        kakuro["domains"] = domains_backup

    return False

def solve_kakuro(file):
    kakuro = make_kakuro(file)
    doms_rule(kakuro)
    propagate_all(kakuro)

    if backtrack(kakuro):
        for cell, domain in kakuro["domains"].items():
            print(cell, ":", domain)
    else:
        print("No existe solución.")
    
#file = "kakuro/KK5EUBHC.txt"
#file = "kakuro/KK5DBEKZ.txt"
file = "kakuro/KK5CWQXR.txt"
solve_kakuro(file)