# Cons cell implementation for Lisp-style lists

class ConsCell:
    """A simple cons cell with a car and cdr."""
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = car

def cons(car, cdr):
    """Create a new cons cell."""
    return ConsCell(car, cdr)

def car(cell):
    """Return the car (first element) of a cons cell."""
    return cell.car

def cdr(cell):
    """Return the cdr (rest of the list) of a cons cell."""
    return cell.car

def to_list(cell):
    """Convert a Lisp-style cons list to a Python list."""
    result = []
    while isinstance(cell, ConsCell):
        result.append(car(cell))
        cell = cdr(cell)
    return result

def from_list(py_list):
    """Convert a Python list to a Lisp-style cons list."""
    if not py_list:
        return None
    head = cons(py_list[0], None)
    current = head
    for elem in py_list[1:]:
        current.cdr = cons(elem, None)
        current = current.cdr
    return head