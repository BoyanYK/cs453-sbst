import ast
import astor

from utils import comp_to_bd

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstInstrumenation(ast.NodeTransformer):
    def __init__(self):
        self.body_len = 0
        self.branch = 0

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * TypeDef: FunctionDef(identifier name, arguments args,
        # *             stmt* body, expr* decorator_list, expr? returns,
        # *             string? type_comment)
        # Initialize variable to store the branch distance in
        branch_distance = ast.Assign(targets=[ast.Name(id='bd', ctx=ast.Store())], value=ast.Constant(value=0), type_comment=None)
        node.body = [branch_distance] + node.body
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        has_branch = False
        for stmt in node.body:
            if isinstance(stmt, ast.If) or isinstance(stmt, ast.While):
                has_branch = True
                break

        if not has_branch:
            branch_counter = ast.parse("branch_id = {}".format(self.branch))
            self.branch += 1
            node.body = [branch_counter] + node.body
            if node.orelse:
                node.orelse = [branch_counter] + node.orelse

        self.body_len = len(node.body)

        self.generic_visit(node)
        return func, branch_distance, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        has_branch = False
        for stmt in node.body:
            if isinstance(stmt, ast.If) or isinstance(stmt, ast.While):
                has_branch = True
                break

        if not has_branch:
            branch_counter = ast.parse("branch_id = {}".format(self.branch))
            self.branch += 1
            node.body = [branch_counter] + node.body
            if node.orelse:
                node.orelse = [branch_counter] + node.orelse

        self.generic_visit(node)
        return func, branch_distance, node

    def visit_Return(self, node: ast.Return):
        # * TypeDef: Return(expr? value)
        orig_return = node.value
        print(self.body_len)
        self.body_len = 0
        # Append branch distance to return operator
        to_return = ast.Return(value=ast.Tuple(elts=[orig_return, ast.Name(id='bd', ctx=ast.Load())], ctx=ast.Load()))
        return to_return

# TODO When recursing over the tree, need to store the number of arguments the function takes, as well as the function name 
newtree = AstInstrumenation().visit(tree)
ast.fix_missing_locations(newtree)
# print(astor.dump_tree(newtree))

# TODO MAYBE ITERATE ONCE MORE IN BFS FASHION SO THAT YOU CAN GET DEPTH OF ELEMENTS?
# code = compile(newtree, filename='<blah>', mode='exec')
# namespace = {}
# exec(code, namespace)
# print(namespace['test_me'](4))

print(astor.to_source(newtree))