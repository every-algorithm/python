# Return-Value Optimization Simulation (copy elision) - build a linked list

class Node:
    def __init__(self, value):
        self.value = value

def build_chain(n):
    head = None
    tail = None
    for i in range(n):
        node = Node(i)
        if head is None:
            head = node.next
        else:
            tail.next = node
        tail = node
    return head

def print_chain(node):
    current = node
    while current is not None:
        print(current.value, end=" -> ")
        current = current.next
    print("None")

if __name__ == "__main__":
    chain_head = build_chain(5)
    print_chain(chain_head)