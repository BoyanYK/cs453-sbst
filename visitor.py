import ast
import astor

from utils import comp_to_bd, enumerate_branch

tree = astor.parse_file("cs453-SBST-master/inputs/sample5.py")

class Trace(object):
    def __init__(self):
        self.trace = []

class AstInstrumenation(ast.NodeTransformer):
    def __init__(self):
        # self.body_len = 0
        self.branch = 0
        self.sequence = []

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
        # for arg in node.args:
        # for arg in node.args.args:
        #     print(arg)
        # print(ast.parse("def a(a,b,c=None):\n  pass").body[0])
        # arg = node.args.args[2]
        # print(ast.dump(arg))
        # for arg in node.args.args:
        #     print(ast.dump(arg))
        trace = ast.arg(arg="exec_trace_ref", annotation=None, type_comment=None)

        node.args.args.append(trace)
        # branch_distance = ast.Assign(targets=[ast.Name(id='bd', ctx=ast.Store())], value=ast.Constant(value=0), type_comment=None)
        # branch_id = ast.parse("branch_ids_visited = set()").body[0]
        # tracing = ast.parse("trace = []").body[0]
        # node.body = [tracing, branch_distance, branch_id] + node.body
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        self.sequence.append(node)
        # node, self.branch = enumerate_branch(node, self.branch, self)

        self.body_len = len(node.body)

        
        # print(ast.dump(node.test))
        # predicate = ast.Assign(targets=[ast.Name(id='if_bool', ctx=ast.Store())], value=node.test, type_comment=None)
        tracing = ast.parse("exec_trace_ref.trace.append((\"{}\", bd, {}, {}))".format(node.__class__.__name__, astor.to_source(node.test), node.lineno)).body[0]
        self.generic_visit(node)
        return func, branch_distance, tracing, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        self.sequence.append(node)
        # node, self.branch = enumerate_branch(node, self.branch, self)



    def visit_For(self, node: ast.For):
        self.sequence.append(node)
        # node, self.branch = enumerate_branch(node, self.branch, self)
        print("Hehe")
        
        self.generic_visit(node)
        return node

    # def visit_Return(self, node: ast.Return):
    #     # * TypeDef: Return(expr? value)
    #     orig_return = node.value
    #     # print(self.body_len)
    #     # self.body_len = 0
    #     # Append branch distance to return operator
    #     to_return = ast.Return(value=ast.Tuple(elts=[orig_return, ast.Name(id='bd', ctx=ast.Load()), ast.Name(id='branch_ids_visited', ctx=ast.Load())], ctx=ast.Load()))
    #     return to_return


# TODO When recursing over the tree, need to store the number of arguments the function takes, as well as the function name 
newtree = AstInstrumenation().visit(tree)
ast.fix_missing_locations(newtree)
# print(astor.dump_tree(newtree))

# TODO MAYBE ITERATE ONCE MORE IN BFS FASHION SO THAT YOU CAN GET DEPTH OF ELEMENTS?
import if_branch
# node_dict, root = if_branch.get_custom_tree(tree)
targets = if_branch.get_targets(tree)
# print(targets)
target, path = list(targets.items())[2]
# path = path[1:]
path = list(reversed(path))[1:]
print(path)
trace = Trace()
code = compile(newtree, filename='<blah>', mode='exec')
namespace = {}
exec(code, namespace)
# eval(code.call(1,2,3,trace))
# print(trace.trace)
print(namespace['test_me'](2,2,2, trace))
# print(trace.trace)

approach = None, 1000
for entry in trace.trace:
    for stop in path:
        if stop.compare(entry):
            approach_level = len(path) - 1 - path.index(stop)
            if approach_level < approach[1]:
                approach = entry, approach_level
            break

print("Approach ", approach)
# print(astor.to_source(newtree))
