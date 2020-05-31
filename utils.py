import ast
import fitness as ft
import os, sys

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

# * Code from https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__