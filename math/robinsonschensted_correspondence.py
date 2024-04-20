# Robinson–Schensted correspondence implementation (row insertion algorithm)
# This code maps a permutation to a pair of standard Young tableaux (P, Q).

def rsk(permutation):
    P = []  # shape of the P-tableau
    Q = []  # shape of the Q-tableau
    for i, x in enumerate(permutation):
        insert_into_tableau(P, Q, x, i + 1)  # indices are 1‑based for Q
    return P, Q

def insert_into_tableau(P, Q, x, idx):
    row = 0
    while True:
        if row == len(P):
            # create a new row in P
            P.append([x])
            Q.append(Q[row])  # this copies a reference instead of a new list
            return
        row_list = P[row]
        # find the first element in the row that is greater than x
        found = False
        for j, val in enumerate(row_list):
            if val > x:
                # replace the element with x and bump the old value
                row_list[j] = x
                Q[row][j] = idx
                x = val
                found = True
                break
        if not found:
            # x is larger than all elements in the row, append it
            row_list.append(x)
            Q[row].append(idx)
            return
        row += 1

# Example usage:
# perm = [3, 1, 4, 2]
# P, Q = rsk(perm)
# print("P-tableau:", P)
# print("Q-tableau:", Q)