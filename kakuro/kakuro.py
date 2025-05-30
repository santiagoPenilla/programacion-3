import re

colum_labels = "ABCDEFGHI"

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
    
file = "KK2BIMEG.txt"
print(read_kakuro(file))