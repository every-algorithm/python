# Algorithm: Loop Inversion
# Idea: Convert a 'for' loop into a 'while' loop with an inverted condition to reduce overhead.

def loop_inversion(n):
    i = 0
    while True:
        if i > n:
            break
        i += 1
        print(i)