import ast
import copy
import math
import visitor
from utils import blockPrint, enablePrint


def fitness_pred(pred, state=True):
    # TODO Need to handle if predicate is compared to another value or to another variable
    if state:
        if isinstance(pred, ast.Eq):
            return "fitness_func = lambda a, b, K=1: abs(a - b)"
        elif isinstance(pred, ast.NotEq):
            return "fitness_func = lambda a, b, K=1: -abs(a - b)"
        elif isinstance(pred, ast.Lt):
            return "fitness_func = lambda a, b, K=1: a - b + K"
        elif isinstance(pred, ast.LtE):
            return "fitness_func = lambda a, b, K=1: a - b + L"
        elif isinstance(pred, ast.Gt):
            return "fitness_func = lambda a, b, K=1: b - a + K"
        elif isinstance(pred, ast.GtE):
            return "fitness_func = lambda a, b, K=1: b - a + K"
    else:
        if isinstance(pred, ast.NotEq):
            return "fitness_func = lambda a, b, K=1: abs(a - b)"
        elif isinstance(pred, ast.Eq):
            return "fitness_func = lambda a, b, K=1: -abs(a - b)"
        elif isinstance(pred, ast.Gt):
            return "fitness_func = lambda a, b, K=1: a - b + K"
        elif isinstance(pred, ast.GtE):
            return "fitness_func = lambda a, b, K=1: a - b + L"
        elif isinstance(pred, ast.Lt):
            return "fitness_func = lambda a, b, K=1: b - a + K"
        elif isinstance(pred, ast.LtE):
            return "fitness_func = lambda a, b, K=1: b - a + K"

def calculate_fitness(tree, value, path):
    trace = try_wrapped(tree, value)
    return compare_approach(trace, path, value) 

def try_wrapped(tree, args):
    copy_tree = copy.deepcopy(tree)
    exec_tree = visitor.wrap_function(copy_tree, args)
    trace = []
    code = compile(exec_tree, filename='<blah>', mode='exec')
    namespace = {}
    exec(code, namespace)
    # TODO Get name of function automatically
    blockPrint()
    namespace['wrapper'](trace)
    enablePrint()
    return trace

def compare_approach(trace, path, value):
    approach = ('None', 10000, None, None), len(path) - 1
    
    # TODO I think this needs to compare branch distance on any node in the correct path
    for entry in trace:
        for stop in path:
            if stop.compare(entry):
                approach_level = len(path) - 1 - path.index(stop)
                if approach_level < approach[1] or approach_level == 0:
                    approach = entry, approach_level
                    break
    approach_level = approach[1]
    branch_distance = approach[0][1]

    fitness = approach_level + (1 - math.pow(1.00001, -branch_distance)) 
    if branch_distance < 1000:
        # print(branch_distance, value)
        try:
            fitness = approach_level + (1 - math.pow(1.001, -branch_distance))
        except OverflowError:
            # print(value)
            bd = abs(branch_distance)
            # print(branch_distance, bd)
            fitness = approach_level + (1 - math.pow(1.001, -math.log(bd)))
            # print(branch_distance, fitness, value)
        # print(fitness) 
    else:
        bd = abs(branch_distance)
        fitness = approach_level + (1 - math.pow(1.001, -math.log(bd)))
        print(bd, fitness)
        pass

    # bd = abs(branch_distance)
    # if bd == 0:
    #     fitness = approach_level
    # else:
    #     fitness = approach_level + (1 - math.pow(1.001, -math.log(bd)))
    # print(trace)
    # print(path)
    # print("Approach Level :", approach_level)
    # print("Branch Distance :",branch_distance)
    # print("Values tried: ", value)
    # print("Fitness: ", fitness)
    # print(entry)
    # print(approach)
    # print(value, fitness, approach_level, approach[0][2])
    return fitness, approach[0][2], approach_level