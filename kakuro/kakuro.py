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
    
def make_kakuro(file):
    kakuro = {}
    kakuro["constraints"] = read_kakuro(file)
    kakuro["domains"] = get_doms(kakuro)
    return kakuro

file = "kakuro/KK2BIMEG.txt"
kakuro = make_kakuro(file)
doms_rule(kakuro)

for cell, domain in kakuro["domains"].items():
    print(cell, domain)