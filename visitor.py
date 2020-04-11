import ast
import astor
import fitness as ft

tree = astor.parse_file("cs453-SBST-master/inputs/sample3.py")

class AstLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # * FunctionDef(identifier name, arguments args,
        # *        stmt* body, expr* decorator_list, expr? returns,
        # *        string? type_comment)
        # print(node.name)
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        # * If(expr test, stmt* body, stmt* orelse)
        # print(node.test)
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        # * Compare(expr left, cmpop* ops, expr* comparators)
        # print(node.left)
        # print(node.ops)
        for op in node.ops:
            fit = ft.fitness_pred(op)
            # print(fit(1,2))
        # print(node.comparators)
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        
        # print(node.test)
        # print(node.body)
        # print(node.orelse)
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        # print(node.target)
        # print(node.iter)
        # print(node.body)
        # print(n)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        print(node.func)
        print(node.args)
        print(node.keywords)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        print(node.id)
        print(node.ctx)

AstLister().visit(tree)