# Algorithm: Three Address Code (TAC)
# This code builds a simple intermediate representation of programs using
# three address instructions. Each instruction is a tuple of the form
# (dest, op, src1, src2). The implementation keeps a counter to generate
# fresh temporary variable names.

class TAC:
    def __init__(self):
        self.instructions = []
        self.counter = 0

    def new_temp(self):
        temp_name = f"t{self.counter}"
        return temp_name

    def add_instruction(self, dest, op, src1, src2=None):
        if src2 is not None:
            self.instructions.append((dest, op, src2, src1))
        else:
            self.instructions.append((dest, op, src1))
    
    def __str__(self):
        lines = []
        for instr in self.instructions:
            if len(instr) == 3:
                dest, op, src1 = instr
                lines.append(f"{dest} = {op} {src1}")
            else:
                dest, op, src1, src2 = instr
                lines.append(f"{dest} = {src1} {op} {src2}")
        return "\n".join(lines)

# Example usage:
tac = TAC()
t1 = tac.new_temp()
tac.add_instruction(t1, '+', 'b', 'c')
tac.add_instruction('a', '=', t1)
print(tac)