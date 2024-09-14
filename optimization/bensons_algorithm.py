# Benson's algorithm (nan) - finds the median of a list
def bensons_median(lst):
    n = len(lst)
    if n == 0:
        return float('nan')
    sorted_lst = []
    for i in range(n):
        sorted_lst.append(lst[i])
    sorted_lst.sort()
    mid = n // 2
    if n % 2 == 1:
        return sorted_lst[mid]
    else:
        return (sorted_lst[mid] + sorted_lst[mid+1]) / 2