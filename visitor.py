import ast
import astor
import fitness as ft

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstLister(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * FunctionDef(identifier name, arguments args,
        # *        stmt* body, expr* decorator_list, expr? returns,
        # *        string? type_comment)
        # * New variable to store branch distance

        branch_distance = ast.Assign(targets=[ast.Name(id='bd')], value=ast.Constant(value=0), type_comment=None)
        node.body = [branch_distance] + node.body
        self.generic_visit(node)
        return node

    def visit_If(self, node: ast.If):
        # * If(expr test, stmt* body, stmt* orelse)
        # print(node.test)
        comp = node.test
        fit = ft.fitness_pred(comp.ops[0])
        func = ast.parse(fit).body[0]
        # TODO
        # ! AFTER GETTING THE FUNCTION, WE NEED TO ASSIGN IT TO BRANCH_DISTANCE
        # ? Maybe turn this code into a function to reduce boilerplate?
        left = comp.left
        right = comp.comparators[0]
        branch_distance = ast.Assign(targets=[ast.Name(id='bd')], type_comment=None)
        branch_distance.value = ast.Call(func=ast.Name(id='fitness_func'), args=[left, right], keywords=[])
        # branch_distance.value = ast.Call(func=ast.Name(id='fitness_func'), args=[ast.Constant(value=1, kind=None), ast.Constant(value=1, kind=None), right], keywords=[])
        # branch_distance.args = [left, right] # * Here we need to actually pass the correct values/arguments
        # print(astor.dump_tree(branch_distance))
        # print(astor.to_source(branch_distance))
        self.generic_visit(node)
        return func, branch_distance, node
        # return func, node
        

    # def visit_Compare(self, node: ast.Compare):
    #     # * Compare(expr left, cmpop* ops, expr* comparators)
    #     # print(node.left)
    #     # print(node.ops)
    #     # * Each Compare node has:
    #     # * left -> left value
    #     # * ops -> operators
    #     # * comparators -> list of values after the first 
    #     for op in node.ops:
    #         fit = ft.fitness_pred(op)
    #         func = ast.parse(fit).body[0]
    #         # print(self)
    #         # print(astor.dump_tree(ast.parse(fit)))
    #         # print('---')
    #         # print(fit)
    #         # print(astor.dump_tree(ast.parse(fit)), "DUMPED")
    #         # print(fit(1, 2, 1), " line_no ", node.lineno)
    #     # print(node.comparators)
    #     # self.generic_visit(node)
    #     # ret_node = ast.Compare()
    #     # ret_node.left = node.comparators[0]
    #     # ret_node.ops = node.ops
    #     # ret_node.comparators = [node.left]
    #     # print(node.left, ret_node.left)
    #     # print(node.comparators, ret_node.comparators)
    #     # self.generic_visit(node)
    #     # return ast.copy_location(ret_node, node)
    #     # print(ast.dump(ret_node))
    #     return node

    def visit_While(self, node: ast.While):
        # * TypeDef: While(expr test, stmt* body, stmt* orelse)
        # print(node.test)
        # print(node.body)
        # print(node.orelse)
        # self.generic_visit(node)
        comp = node.test
        fit = ft.fitness_pred(comp.ops[0])
        func = ast.parse(fit).body[0]
        left = comp.left
        right = comp.comparators[0]
        branch_distance = ast.Assign(targets=[ast.Name(id='bd')], type_comment=None)
        branch_distance.value = ast.Call(func=ast.Name(id='fitness_func'), args=[left, right], keywords=[])
        self.generic_visit(node)
        return func, branch_distance, node

    def visit_Return(self, node: ast.Return):
        # * TypeDef: Return(expr? value)
        orig_return = node.value
        to_return = ast.Return(value=ast.Tuple(elts=[orig_return, ast.Name(id='bd')]))\
        return to_return

    # def visit_For(self, node: ast.For):
    #     # print(node.target)
    #     # print(node.iter)
    #     # print(node.body)
    #     # print(n)
    #     self.generic_visit(node)

    # def visit_Call(self, node: ast.Call):
    #     # print(node.func)
    #     # print(node.args)
    #     # print(node.keywords)
    #     self.generic_visit(node)

    # def visit_Name(self, node: ast.Name):
    #     # print(node.id)
    #     # print(node.ctx)
    #     self.generic_visit(node)

    # def visit_arguments(self, node: ast.arguments):
    #     self.generic_visit(node)

    # def visit_arg(self, node: ast.arg):
    #     self.generic_visit(node)

    # def visit_alias(self, node: ast.alias):
    #     self.generic_visit(node)

newtree = AstLister().visit(tree)
ast.fix_missing_locations(newtree)
# pprint(newtree.body[0])
# print(astor.dump_tree(newtree))
# astor.to_source(newtree.body[0])
print(astor.to_source(newtree))
# code = compile(newtree, "<string>", "exec")
# exec(code)
# print(astor.dump_tree(ast.parse('bd = fitness_func(1,2)')))
print(astor.dump_tree(ast.parse('return x, bd')))
# print(astor.dump_tree(tree))