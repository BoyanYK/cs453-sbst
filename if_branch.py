import ast
import astor
import networkx as nx
from utils import comp_to_bd, enumerate_branch
import matplotlib.pyplot as plt
from typing import NamedTuple
from networkx.drawing.nx_agraph import graphviz_layout

tree = astor.parse_file("cs453-SBST-master/inputs/sample5.py")

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

def add_elems(depth_map, body, depth):
    for node in body:
        depth_map[node] = depth
    return depth_map
    

def get_custom_tree(tree):
    function = Node(tree.body[0], 0)
    queue = []
    queue.append(function)
    # for node in function.get_body():
    #     queue.append(Node(node, 0, tree.body[0]))
    # G = nx.DiGraph()
    # G.add_node(function)
    flow_change = []
    end = 0
    nodes = {}
    # nodes[]
    while queue:
        node = queue.pop(0)
        # G.add_node(node)
        # nodes.add(node)
        nodes[node] = None
        branches_off = False
        has_return = False

        prev = node

        for child in node.get_body():
            child_node = Node(child, parent=node)
            queue.append(child_node)
            node.add_child(child_node)
            # nodes.add(child_node)
            # nodes[child_node] = None
            #     # branches_off = 

        if isinstance(node.node, ast.If):
            for child in node.get_else():
                child_node = Node(child, parent=node)
                # print(child_node)
                queue.append(child_node)
                node.add_child(child_node)
                # nodes.add(child_node)
                # nodes[child_node] = None

        if isinstance(node.node, ast.If) or isinstance(node.node, ast.While) or isinstance(node.node, ast.For):
            flow_change.append(node)
    return nodes, function, flow_change

def get_targets(tree):
    node_dict, root, flow_change = get_custom_tree(tree)
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
    return targets
    
# print(nodes)    
# for node in nodes.keys():
#     if node.name == "If":
#         print(node)

# a = nx.nx_agraph.to_agraph(G)
# pos = graphviz_layout(G, prog='dot')
# nx.draw(G, pos=pos, with_labels=True, labels=nodes)
# plt.draw()
# plt.show()
