import ast
import astor
import fitness as ft

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstLister(ast.NodeTransformer):
    # def visit_FunctionDef(self, node: ast.FunctionDef):
    #     # * FunctionDef(identifier name, arguments args,
    #     # *        stmt* body, expr* decorator_list, expr? returns,
    #     # *        string? type_comment)
    #     # print(node.name)
    #     self.generic_visit(node)

    # def visit_If(self, node: ast.If):
    #     # * If(expr test, stmt* body, stmt* orelse)
    #     # print(node.test)
    #     self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        # * Compare(expr left, cmpop* ops, expr* comparators)
        # print(node.left)
        # print(node.ops)
        # * Each Compare node has:
        # * left -> left value
        # * ops -> operators
        # * comparators -> list of values after the first 
        a = node.left
        b = node.comparators[0]
        for op in node.ops:
            fit = ft.fitness_pred(op)
            print(fit(1, 2, 1), " line_no ", node.lineno)
        # print(node.comparators)
        # self.generic_visit(node)
        ret_node = ast.Compare()
        ret_node.left = node.comparators[0]
        ret_node.ops = node.ops
        ret_node.comparators = [node.left]
        # print(node.left, ret_node.left)
        # print(node.comparators, ret_node.comparators)
        # self.generic_visit(node)
        # return ast.copy_location(ret_node, node)
        # print(ast.dump(ret_node))
        return ret_node

    # def visit_While(self, node: ast.While):
        
    #     # print(node.test)
    #     # print(node.body)
    #     # print(node.orelse)
    #     self.generic_visit(node)

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