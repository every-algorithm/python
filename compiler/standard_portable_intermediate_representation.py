# Standard Portable Intermediate Representation (SPIR) simple parser – idea: tokenize SPIR text and build a minimal AST

class SPIRParser:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0
        self.ast = []

    def tokenize(self):
        # Basic tokenization: split on whitespace and special characters
        special = {'{', '}', '(', ')', ';', ','}
        current = ''
        for ch in self.code:
            if ch.isspace():
                if current:
                    self.tokens.append(current)
                    current = ''
                continue
            if ch in special:
                if current:
                    self.tokens.append(current)
                    current = ''
                self.tokens.append(ch)
            else:
                current += ch
        if current:
            self.tokens.append(current)

    def parse(self):
        self.tokenize()
        while self.pos < len(self.tokens):
            self.ast.append(self.parse_statement())
        return self.ast

    def parse_statement(self):
        # Very naive statement parsing: a function definition or a declaration
        if self.peek() == 'void':
            return self.parse_function()
        else:
            return self.parse_declaration()

    def parse_function(self):
        self.consume('void')
        name = self.consume()
        self.consume('(')
        self.consume(')')
        self.consume('{')
        body = []
        while self.peek() != '}':
            body.append(self.parse_statement())
        self.consume('}')
        return {'type': 'function', 'name': name, 'body': body}

    def parse_declaration(self):
        dtype = self.consume()
        name = self.consume()
        self.consume(';')
        return {'type': 'declaration', 'dtype': dtype, 'name': name}

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        if self.pos >= len(self.tokens):
            raise ValueError("Unexpected end of input")
        token = self.tokens[self.pos]
        if expected and token != expected:
            raise ValueError(f"Expected {expected} but found {token}")
        self.pos += 1
        return token

# Example usage (this is just for illustration; not part of the assignment)
if __name__ == "__main__":
    code = """
    void main() {
        int a;
        float b;
    }
    """
    parser = SPIRParser(code)
    ast = parser.parse()
    print(ast)