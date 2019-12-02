from more_itertools import take, collapse


class Node:
    def __init__(self, num_children, num_metadata):
        self.num_children = num_children
        self.num_metadata = num_metadata
        self.children = []
        self.metadata = []

    def value(self):
        if self.num_children == 0:
            return sum(self.metadata)
        else:
            value = 0
            for index in self.metadata:
                if 1 <= index <= self.num_children:
                    value += self.children[index - 1].value()
            return value


def load_node(data):
    node = Node(next(data), next(data))
    for i in range(node.num_children):
        node.children.append(load_node(data))
    node.metadata = take(node.num_metadata, data)
    return node


def process_data(data):
    data = map(int, data.split())
    root = load_node(data)
    return root


def recursive_iter(node: Node):
    yield node
    for node in node.children:
        yield from recursive_iter(node)


def solve_a(data):
    root = process_data(data)
    checksum = sum(collapse(map(lambda x: x.metadata, recursive_iter(root))))
    return checksum


def solve_b(data):
    root = process_data(data)
    return root.value()
