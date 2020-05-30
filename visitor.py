import ast
import astor
from utils import comp_to_bd, enumerate_branch


class TargetInstrumentation(ast.NodeTransformer):
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
        trace = ast.arg(arg="trace", annotation=None, type_comment=None)
        node.args.args.append(trace)
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * TypeDef: If(expr test, stmt* body, stmt* orelse)
        func, branch_distance = comp_to_bd(node.test)

        tracing = ast.parse("trace.append((\"{}\", bd, {}, {}))".format(node.__class__.__name__, astor.to_source(node.test), node.lineno)).body[0]
        self.generic_visit(node)
        return func, branch_distance, tracing, node
        
    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
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

# def wrap_function(tree, args):
#     wrapper = ast.FunctionDef(name='wrapper', 
#     args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='args', annotation=None, type_comment=None), ast.arg(arg='trace', annotation=None, type_comment=None)], vararg=None,
#                 kwonlyargs=[],
#                 kw_defaults=[],
#                 kwarg=None,
#                 defaults=[]), decorator_list=[], returns=None, type_comment=None)
#     # wrapper.body = [tree]
#     target_call = tree.name + '('
#     for arg in args:
#         target_call += str(arg) + ', '
#     target_call += 'trace)'
#     call = ast.parse(target_call)
#     wrapper.body = [tree, call]
#     # print(astor.dump_tree(ast.parse("def wrapper(args, trace):\n  a = 1")))
#     print(astor.to_source(wrapper))
#     # print(astor.dump_tree(wrapper))
#     return wrapper