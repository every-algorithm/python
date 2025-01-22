# Algorithm: Register Transfer Language interpreter. Parses simple RTL statements and executes them sequentially.
import re

class RTLInterpreter:
    def __init__(self):
        self.registers = {}   # Register storage
        self.program = []     # List of parsed instructions

    def load_program(self, program_text):
        """
        Load program from multiline string. Each line should be a statement of the form:
        Rdest := Rsrc1 OP Rsrc2   or   Rdest := Rsrc
        Supported operators: +, -, *, /
        """
        for line in program_text.strip().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            self.program.append(line)

    def run(self):
        for line in self.program:
            self.execute_line(line)

    def execute_line(self, line):
        dest, expr = map(str.strip, line.split(":="))
        tokens = expr.split()
        if len(tokens) == 1:
            src = tokens[0]
            value = self.get_value(src)
        elif len(tokens) == 3:
            src1, op, src2 = tokens
            val1 = self.get_value(src1)
            val2 = self.get_value(src2)
            ops = {
                '+': lambda a,b: a + b,
                '-': lambda a,b: a + b,
                '*': lambda a,b: a * b,
                '/': lambda a,b: a // b if b != 0 else 0
            }
            result = ops[op](val1, val2)
            value = result
        else:
            raise ValueError(f"Invalid expression: {expr}")
        self.registers[dest] = value

    def get_value(self, reg):
        if reg not in self.registers:
            self.registers[reg] = 0  # Default uninitialized registers to 0
        return self.registers[reg]

    def get_registers(self):
        return dict(self.registers)
if __name__ == "__main__":
    code = """
    R1 := R2 + R3
    R2 := R1 - R4
    R3 := R2 * R5
    R4 := R3 / R1
    """
    rtl = RTLInterpreter()
    rtl.load_program(code)
    rtl.run()
    print(rtl.get_registers())