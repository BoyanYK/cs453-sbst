import astor
import target
import ast

tree = astor.code_to_ast(target)

def visitFun(function):
    print("Name", function.name)
    print("Args", function.args)
    # get_args(function.args)
    print("Body", function.body)
    visitBody(function.body)
    print("decorator", function.decorator_list)
    print("Return", function.returns)
    print("Type", function.type_comment)
    print("---")

def visitBody(body):
    for stmt in body:
        # print(stmt)
        if isinstance(stmt, ast.If):
            visitIf(stmt)
        elif isinstance(stmt, ast.Return):
            print('return')

def visitIf(i):
    print(i.test)
    print(i.body)
    print(i.orelse)
    print(i)

def get_args(args):
    print("PosOnly", args.posonlyargs)
    print("Args", args.args[0].arg)
    print("---")

for function in tree.body:
    # print(function)
    visitFun(function)
    # break


# print(astor.dump_tree(a))
# print(a.body.pop()._attributes)
# print(astor.get_op_symbol(a.body.pop()))
# print(a)
# for ind, item in enumerate(a.body[0].body):
#     # print(ind, item)
#     # print(item.body)
#     # if isinstance(item, ast.Assign) and isinstance(item.value, ast.List):
#         # del tree.body[0].body[ind]
        
#     for a in astor.iter_node(item):
#         print(a)

# tree = ast.parse('target.py', filename='target.py')
# print(tree)
# print(tree.body)
# print(tree.body[0].value.attr)#.value.id)
# print(tree.body[0].value.value.ctx)
# for node in ast.iter_child_nodes(tree):
#     print(node)

def visitIf(item):
    print(item)
# print(ast.parse(target))
# def function_handler():
