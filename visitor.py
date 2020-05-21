import ast
import astor

from utils import comp_to_bd, enumerate_branch

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstInstrumenation(ast.NodeTransformer):
    def __init__(self):
        # self.body_len = 0
        self.branch = 0

    def get_max_branch(self):
        """Helper to get the maximum branch number for a function

        Returns:
            {int} -- Maximum branch
        """
        return self.branch 

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * TypeDef: FunctionDef(identifier name, arguments args,
        # *             stmt* body, expr* decorator_list, expr? returns,
        # *             string? type_comment)
        # Initialize variable to store the branch distance in
        branch_distance = ast.Assign(targets=[ast.Name(id='bd', ctx=ast.Store())], value=ast.Constant(value=0), type_comment=None)
        branch_id = ast.parse("branch_ids_visited = set()").body[0]
        node.body = [branch_distance, branch_id] + node.body
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        node, self.branch = enumerate_branch(node, self.branch)

        self.body_len = len(node.body)

        self.generic_visit(node)
        return func, branch_distance, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        node, self.branch = enumerate_branch(node, self.branch)

        self.generic_visit(node)
        return func, branch_distance, node

    def visit_For(self, node: ast.For):
        node, self.branch = enumerate_branch(node, self.branch)
        
        self.generic_visit(node)
        return node

    def visit_Return(self, node: ast.Return):
        # * TypeDef: Return(expr? value)
        orig_return = node.value
        # print(self.body_len)
        # self.body_len = 0
        # Append branch distance to return operator
        to_return = ast.Return(value=ast.Tuple(elts=[orig_return, ast.Name(id='bd', ctx=ast.Load()), ast.Name(id='branch_ids_visited', ctx=ast.Load())], ctx=ast.Load()))
        return to_return

# TODO When recursing over the tree, need to store the number of arguments the function takes, as well as the function name 
newtree = AstInstrumenation().visit(tree)
ast.fix_missing_locations(newtree)
# print(astor.dump_tree(newtree))

# TODO MAYBE ITERATE ONCE MORE IN BFS FASHION SO THAT YOU CAN GET DEPTH OF ELEMENTS?
code = compile(newtree, filename='<blah>', mode='exec')
namespace = {}
exec(code, namespace)
print(namespace['test_me'](4))

# print(astor.to_source(newtree))