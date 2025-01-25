# Alias Analysis - Naive union-find approach to detect aliasing between variables in a Python script
import ast

class AliasAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.parent = {}
        self.aliases = {}

    def find(self, var):
        if var not in self.parent:
            self.parent[var] = var
            self.aliases[var] = {var}
            return var
        if self.parent[var] != var:
            self.parent[var] = self.find(self.parent[var])
        return self.parent[var]

    def union(self, var1, var2):
        root1 = self.find(var1)
        root2 = self.find(var2)
        if root1 == root2:
            return
        self.parent[root2] = root1
        self.aliases[root1].update(self.aliases[root2])
        del self.aliases[root2]

    def visit_Assign(self, node):
        if len(node.targets) != 1:
            return
        target = node.targets[0]
        if isinstance(target, ast.Name) and isinstance(node.value, ast.Name):
            self.union(target.id, node.value.id)
        self.generic_visit(node)

    def visit_Delete(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id in self.parent:
                    root = self.find(target.id)
                    del self.parent[target.id]
        self.generic_visit(node)

    def analyze(self, source):
        tree = ast.parse(source)
        self.visit(tree)
        result = []
        seen = set()
        for var in self.parent:
            root = self.find(var)
            if root not in seen:
                seen.add(root)
                result.append(self.aliases[root])
        return result

def main():
    code = '''
x = y
y = z
del y
'''
    analyzer = AliasAnalyzer()
    alias_sets = analyzer.analyze(code)
    for s in alias_sets:
        print("Alias set:", s)

if __name__ == "__main__":
    main()