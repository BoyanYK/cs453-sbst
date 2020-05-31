import ast
import astor
# from utils import comp_to_bd
from fitness import fitness_pred


class TargetInstrumentation(ast.NodeTransformer):
    def __init__(self, target, state):
        self.target = target
        self.state = state
        
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * TypeDef: FunctionDef(identifier name, arguments args,
        # *             stmt* body, expr* decorator_list, expr? returns,
        # *             string? type_comment)
        trace = ast.arg(arg="trace", annotation=None, type_comment=None)
        node.args.args.append(trace)
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        if node.lineno == self.target.lineno and node.__class__.__name__ == self.target.name:
            func, branch_distance = comp_to_bd(node.test, self.state)
        else:
            func, branch_distance = comp_to_bd(node.test)

        tracing = ast.parse("trace.append((\"{}\", bd, {}, {}))".format(node.__class__.__name__, astor.to_source(node.test), node.lineno)).body[0]
        self.generic_visit(node)
        return func, branch_distance, tracing, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        if node.lineno == self.target.lineno and node.__class__.__name__ == self.target.name:
            func, branch_distance = comp_to_bd(node.test, self.state)
        else:
            func, branch_distance = comp_to_bd(node.test)

        tracing = ast.parse("trace.append((\"{}\", bd, {}, {}))".format(node.__class__.__name__, astor.to_source(node.test), node.lineno)).body[0]
        return func, branch_distance, tracing, node


    # TODO Try to tackle 'for' branching?
    # def visit_For(self, node: ast.For):
    #     self.generic_visit(node)
    #     return node
def wrap_function(tree, args):
    wrapper = ast.FunctionDef(name='wrapper', 
    args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='trace', annotation=None, type_comment=None)], vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]), decorator_list=[], returns=None, type_comment=None)
    target_call = tree.body[0].name + '('
    for arg in args:
        target_call += str(arg) + ', '
    target_call += 'trace)'
    call = ast.parse(target_call)
    wrapper.body = [tree.body[0], call.body[0]]
    tree.body = [wrapper]
    ast.fix_missing_locations(tree)
    return tree

def comp_to_bd(comp: ast.Compare, state=True):
    """[summary]
    Given a comparator operator, returns an assignment to branch distance variable
    
    Arguments:
        comp {ast.Compare} -- Comparator operator, part of {ast.If} or {ast.While}

    Returns:
        func {ast.Lambda} - Function to calculate branch distance
        branch_distance {ast.expr} - Assigning the relevant branch distance calculation function return value to the branch distance variable
    """
    fit = fitness_pred(comp.ops[0], state)
    func = ast.parse(fit).body[0]
    left = comp.left
    right = comp.comparators[0]
    branch_distance = ast.Assign(targets=[ast.Name(id='bd', ctx=ast.Store())], type_comment=None)
    branch_distance.value = ast.Call(func=ast.Name(id='fitness_func', ctx=ast.Load()), args=[left, right], keywords=[])
    return func, branch_distance