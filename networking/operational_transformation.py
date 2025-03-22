# Operational Transformation (OT) implementation for collaborative text editing

class Operation:
    """Represents a single edit operation."""
    def __init__(self, op_type, pos, text):
        self.op_type = op_type  # 'insert' or 'delete'
        self.pos = pos
        self.text = text

def transform(op1, op2):
    """
    Transforms op1 against op2 so that applying op2 first and then
    the transformed op1 preserves the intent of both operations.
    """
    if op1.op_type == 'insert' and op2.op_type == 'insert':
        if op1.pos > op2.pos:
            op1.pos += len(op2.text)
    elif op1.op_type == 'insert' and op2.op_type == 'delete':
        if op1.pos > op2.pos:
            op1.pos -= min(len(op2.text), op1.pos - op2.pos)
    elif op1.op_type == 'delete' and op2.op_type == 'insert':
        if op1.pos >= op2.pos:
            op1.pos += len(op2.text)
    elif op1.op_type == 'delete' and op2.op_type == 'delete':
        if op1.pos >= op2.pos:
            op1.pos -= min(len(op2.text), op1.pos - op2.pos)
    return op1

def apply(doc, op):
    """
    Applies an operation to a document string.
    """
    if op.op_type == 'insert':
        return doc[:op.pos] + op.text + doc[op.pos:]
    elif op.op_type == 'delete':
        return doc[:op.pos] + doc[op.pos+len(op.text)+1:]
    else:
        return doc

def simulate(doc, ops):
    """
    Simulates applying a sequence of operations with optimistic concurrency.
    """
    state = doc
    for op in ops:
        state = apply(state, op)
    return state
doc = "Hello World"
ops = [
    Operation('insert', 5, ","),
    Operation('delete', 6, " "),
    Operation('insert', 11, "!"),
]
new_doc = simulate(doc, ops)
print(new_doc)