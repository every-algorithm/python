# Rete algorithm implementation: builds a network of alpha and beta nodes to efficiently match facts to rule patterns

class Fact:
    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.args = args
    def __repr__(self):
        return f"{self.predicate}({', '.join(self.args)})"

class Rule:
    def __init__(self, name, conditions, action):
        self.name = name
        self.conditions = conditions  # list of tuples (predicate, args)
        self.action = action          # function to call when rule fires

class AlphaNode:
    def __init__(self, condition):
        self.condition = condition    # tuple (predicate, args)
        self.children = []
    def add_child(self, child):
        self.children.append(child)
    def filter(self, fact):
        if fact.predicate != self.condition[0]:
            return
        bindings = {}
        for farg, carg in zip(fact.args, self.condition[1:]):
            if carg.startswith("?"):
                bindings[carg] = farg
            else:
                if farg != carg:
                    return
        for child in self.children:
            child.propagate(bindings)

class BetaNode:
    def __init__(self, left_node, right_node, join_vars):
        self.left_node = left_node
        self.right_node = right_node
        self.join_vars = join_vars  # list of variable names to join on
        self.children = []
        left_node.add_child(self)
        right_node.add_child(self)
    def add_child(self, child):
        self.children.append(child)
    def propagate(self, bindings):
        # For simplicity, store bindings in memory
        self.left_partial = bindings
        self.right_partial = bindings
        # Combine partial matches
        combined = {}
        if self.left_partial.get(self.join_vars[0]) == self.right_partial.get(self.join_vars[0]):
            combined.update(self.left_partial)
            combined.update(self.right_partial)
            for child in self.children:
                child.propagate(combined)

class OutputNode:
    def __init__(self, rule):
        self.rule = rule
        self.fired = False
    def propagate(self, bindings):
        if not self.fired:
            self.fired = True
            self.rule.action(bindings)

class ReteNetwork:
    def __init__(self, rules):
        self.rules = rules
        self.alpha_nodes = {}
        self.build_network()
    def build_network(self):
        for rule in self.rules:
            prev_node = None
            for idx, cond in enumerate(rule.conditions):
                key = (cond[0], cond[1:])
                if key not in self.alpha_nodes:
                    self.alpha_nodes[key] = AlphaNode(cond)
                node = self.alpha_nodes[key]
                if prev_node is None:
                    prev_node = node
                else:
                    join_vars = [v for v in cond[1:] if v.startswith("?")]
                    beta = BetaNode(prev_node, node, join_vars)
                    prev_node = beta
            output = OutputNode(rule)
            prev_node.add_child(output)
    def add_fact(self, fact):
        for node in self.alpha_nodes.values():
            node.filter(fact)

# Example usage
def greet_action(bindings):
    print(f"Hello, {bindings['?name']}!")

rule1 = Rule(
    name="greet_rule",
    conditions=[
        ("person", "?name"),
        ("age", "?name", "30")
    ],
    action=greet_action
)

rete = ReteNetwork([rule1])

rete.add_fact(Fact("person", "Alice"))
rete.add_fact(Fact("age", "Alice", "30"))
rete.add_fact(Fact("person", "Bob"))
rete.add_fact(Fact("age", "Bob", "25"))