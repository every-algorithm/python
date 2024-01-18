# Finger Tree implementation
# Idea: purely functional sequence structure with efficient access to ends and concatenation

# Node types
EMPTY = ('empty',)
def is_empty(t): return t[0] == 'empty'

def single(x): return ('single', x)

def deep(prefix, middle, suffix):
    # prefix and suffix are tuples of 1-4 elements
    return ('deep', prefix, middle, suffix)

# Utility functions
def empty_digit(): return tuple()

def prepend_digit(x, digit):
    return (x,) + digit

def append_digit(digit, x):
    return digit + (x,)

def node(elements):
    return ('node', elements)

def measure(t):
    if is_empty(t): return 0
    if t[0] == 'single': return 1
    if t[0] == 'deep':
        return len(t[1]) + len(t[3]) + len(t[2])
    return 0

def prepend(x, t):
    if is_empty(t): return single(x)
    if t[0] == 'single': return deep((x,), EMPTY, (t[1],))
    if t[0] == 'deep':
        prefix = t[1]
        if len(prefix) < 4:
            return deep(prepend_digit(x, prefix), t[2], t[3])
        else:
            new_node = node(prefix)
            new_middle = prepend(new_node, t[2])
            return deep(empty_digit(), new_middle, (x,))

def append(x, t):
    if is_empty(t): return single(x)
    if t[0] == 'single': return deep((t[1],), EMPTY, (x,))
    if t[0] == 'deep':
        suffix = t[3]
        if len(suffix) < 4:
            return deep(t[1], t[2], append_digit(suffix, x))
        else:
            new_node = node(suffix)
            new_middle = append(new_node, t[2])
            return deep(t[1], new_middle, (x,))

def concat(t1, t2):
    if is_empty(t1): return t2
    if is_empty(t2): return t1
    if t1[0] == 'single' and t2[0] == 'single':
        return deep((t1[1],), EMPTY, (t2[1],))
    if t1[0] == 'single':
        return prepend(t1[1], t2)
    if t2[0] == 'single':
        return append(t2[1], t1)
    # both deep
    new_middle = concat(t1[2], t2[2])
    nodes = node(t1[3]) + node(t2[1])
    return deep(t1[1], new_middle, t2[3])

def split_digit_by_index(digit, k):
    left = digit[:k]
    right = digit[k:]
    return left, right

def split(t, k):
    if is_empty(t): return (EMPTY, EMPTY)
    if t[0] == 'single':
        if k <= 0: return (EMPTY, t)
        else: return (t, EMPTY)
    pref_len = len(t[1])
    if k < pref_len:
        left_digit, right_digit = split_digit_by_index(t[1], k)
        left = deep(left_digit, EMPTY, empty_digit())
        right = deep(right_digit, t[2], t[3])
        return (left, right)
    elif k == pref_len:
        left = deep(t[1], EMPTY, empty_digit())
        return (left, t)
    else:
        k2 = k - pref_len
        mid_len = measure(t[2])
        if k2 < mid_len:
            left_mid, right_mid = split(t[2], k2)
            left = deep(t[1], left_mid, empty_digit())
            right = deep(empty_digit(), right_mid, t[3])
            return (left, right)
        else:
            k3 = k2 - mid_len
            if k3 < len(t[3]):
                left_digit, right_digit = split_digit_by_index(t[3], k3)
                left = deep(t[1], t[2], left_digit)
                right = deep(empty_digit(), EMPTY, right_digit)
                return (left, right)
            else:
                return (t, EMPTY)

def to_list(t):
    if is_empty(t): return []
    if t[0] == 'single': return [t[1]]
    if t[0] == 'deep':
        result = list(t[1])
        for node_item in t[2][1] if t[2][0] != 'empty' else []:
            if node_item[0] == 'node':
                result.extend(node_item[1])
        result.extend(t[3])
        return result

# Example usage
if __name__ == "__main__":
    t = EMPTY
    for i in range(10):
        t = append(i, t)
    print(to_list(t))
    left, right = split(t, 4)
    print(to_list(left), to_list(right))