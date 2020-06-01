import ast

class Node(object):
    def __init__(self, node, parent=None):
        self.name = node.__class__.__name__
        self.parent = parent
        self.depth = 0 if not self.parent else self.parent.depth +  1
        self.lineno = node.lineno
        self.node = node
        
        self.children = []

    def __str__(self):
        # return "Node {}, depth {}, line {}".format(self.name, self.depth, self.lineno)
        return "{} @ {}".format(self.name, self.lineno)

    def get_body(self):
        try:
            return self.node.body
        except Exception:
            return []

    def get_else(self):
        try:
            return self.node.orelse
        except Exception:
            return []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return self.__str__()

    def compare(self, target):
        return self.name == target[0] and self.lineno == target[3]

def get_custom_tree(tree, func_name="test_me"):
    arg_count = 0
    for stmt in tree.body:
        if isinstance(stmt, ast.FunctionDef) and stmt.name == 'test_me':
            function = Node(stmt, 0)
            arg_count = len(stmt.args.args)
            break
    queue = []
    queue.append(function)
    flow_change = []
    while queue:
        node = queue.pop(0)
        for child in node.get_body():
            child_node = Node(child, parent=node)
            queue.append(child_node)
            node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While) or isinstance(node.node, ast.For):
            for child in node.get_else():
                child_node = Node(child, parent=node)
                queue.append(child_node)
                node.add_child(child_node)

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While):# Can't deal with For for now or isinstance(node.node, ast.For):
            flow_change.append(node)
    return function, flow_change, arg_count

def get_targets(tree, func_name="test_me"):
    root, flow_change, arg_count  = get_custom_tree(tree, func_name)
    # print(flow_change)
    targets = {}
    for node in flow_change:
        node_tree = [node]
        iter_node = node
        while not isinstance(iter_node.node, ast.FunctionDef):
            parent = iter_node.parent
            node_tree.append(parent)
            iter_node = parent
        targets[node] = node_tree
    return targets, arg_count
    