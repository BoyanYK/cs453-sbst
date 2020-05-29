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



# newtree = TargetInstrumenation().visit(tree)
# ast.fix_missing_locations(newtree)
# # print(astor.dump_tree(newtree))

# import control_flow
# # node_dict, root = if_branch.get_custom_tree(tree)
# targets = control_flow.get_targets(tree)
# # print(targets)
# target, path = list(targets.items())[2]
# # path = path[1:]
# print(target)
# path = list(reversed(path))[1:]
# print(path)
# trace = []
# code = compile(newtree, filename='<blah>', mode='exec')
# namespace = {}
# exec(code, namespace)
# # eval(code.call(1,2,3,trace))
# # print(trace.trace)
# print(namespace['test_me'](3, trace))
# # print(trace.trace)

# approach = None, len(path) - 1
# for entry in trace.trace:
#     for stop in path:
#         if stop.compare(entry):
#             approach_level = len(path) - 1 - path.index(stop)
#             if approach_level < approach[1]:
#                 approach = entry, approach_level
#             break

# print("Approach ", approach)
# # print(astor.to_source(newtree))