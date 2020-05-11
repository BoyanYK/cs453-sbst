import ast
import astor

from utils import comp_to_bd

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstInstrumenation(ast.NodeTransformer):

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
        self.generic_visit(node)
        return func, branch_distance, node
        

    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)
        self.generic_visit(node)
        return func, branch_distance, node

    def visit_Return(self, node: ast.Return):
        # * TypeDef: Return(expr? value)
        orig_return = node.value
        # Append branch distance to return operator
        to_return = ast.Return(value=ast.Tuple(elts=[orig_return, ast.Name(id='bd', ctx=ast.Load())], ctx=ast.Load()))
        return to_return

# TODO When recursing over the tree, need to store the number of arguments the function takes, as well as the function name 
newtree = AstInstrumenation().visit(tree)
ast.fix_missing_locations(newtree)

code = compile(newtree, filename='<blah>', mode='exec')
namespace = {}
exec(code, namespace)
# print(namespace['test_me'](4))

print(astor.to_source(newtree))