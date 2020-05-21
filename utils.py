import ast
import fitness as ft

def comp_to_bd(comp: ast.Compare):
    """[summary]
    Given a comparator operator, returns an assignment to branch distance variable
    
    Arguments:
        comp {ast.Compare} -- Comparator operator, part of {ast.If} or {ast.While}

    Returns:
        func {ast.Lambda} - Function to calculate branch distance
        branch_distance {ast.expr} - Assigning the relevant branch distance calculation function return value to the branch distance variable
    """
    fit = ft.fitness_pred(comp.ops[0])
    func = ast.parse(fit).body[0]
    left = comp.left
    right = comp.comparators[0]
    branch_distance = ast.Assign(targets=[ast.Name(id='bd', ctx=ast.Store())], type_comment=None)
    branch_distance.value = ast.Call(func=ast.Name(id='fitness_func', ctx=ast.Load()), args=[left, right], keywords=[])
    return func, branch_distance

def enumerate_branch(node, branch):
    """ 
    Given an AST node, checks if the node has branching and if not, marks its body and/or else 
    statements as branches
    Arguments:
        node {ast element} -- AST node to verify
        branch {int} -- Current branch number

    Returns:
        ({ast element}, {int}) -- returns the same structure as input in order to continue iteration
    """
    has_branch = False
    for stmt in node.body:
        if isinstance(stmt, ast.If) or isinstance(stmt, ast.While):
            has_branch = True
            break

    if not has_branch:
        branch_counter = ast.parse("branch_ids_visited.add({})".format(branch)).body[0]
        branch += 1
        node.body = [branch_counter] + node.body
        if node.orelse:
            branch_counter = ast.parse("branch_ids_visited.add({})".format(branch)).body[0]
            # print(ast.dump(branch_counter))
            branch += 1
            node.orelse = [branch_counter] + node.orelse
        
    return node, branch