import ast
import astor
import visitor
import control_flow
import sys, os
import math
import random
import copy
from state import get_neighbours
from utils import blockPrint, enablePrint

def main():
    target_path = sys.argv[1]
    try:
        iterations = int(sys.argv[2])
    except IndexError:
        iterations = 1000
    target_tree = astor.parse_file(target_path)
    instrumented = visitor.TargetInstrumentation().visit(copy.deepcopy(target_tree))
    # TODO Add Wrapper around function, so that you can call that wrapper with a list of arguments and then call the function With the correct number of arguments
    args_number = len(target_tree.body[0].args.args)
    # print(args_number)
    # to_call = visitor.wrap_function(instrumented.body[0], [1,2,3])
    # print(get_neighbours([10,15,20], 1))
    ast.fix_missing_locations(instrumented)

    targets = control_flow.get_targets(target_tree)

    hill_climb(instrumented, targets, args_number, iterations)


def hill_climb(tree, targets, arg_count, iterations):
    import numpy as np
    for target, path in targets.items():
        path = list(reversed(path))[1:] # Removes function_def node
        curr_fitness = 10000
        # value = random.randint(0, 100)
        value = [random.randint(0, 100) for i in range(arg_count)]
        visited_states = {}
        local_minima_iter = 1
        n = 0
        while n < iterations:
            # print(type(value))
            n += 1
            trace = try_wrapped(tree, value)
            new_fitness, predicate_value = calculate_fitness(trace, path)
            visited_states[str(value)] = new_fitness
            if new_fitness == 0 or predicate_value:
                break
            else:
                # print(value)
                neighbours = get_neighbours(value, local_minima_iter)#[value - local_minima_iter, value + local_minima_iter]
                results = {}
                results[str(value)] = new_fitness
                # print(neighbours)
                for neighbour in neighbours:
                    neighbour = list(neighbour)
                    # print(neighbour)
                    if str(neighbour) in visited_states:
                        results[str(neighbour)] = visited_states[str(neighbour)]
                    else:
                        # print(neighbour)
                        # print(type(neighbour))
                        trace = try_wrapped(tree, neighbour)
                        neighb_fitness, neighb_predicate_value = calculate_fitness(trace, path)
                        results[str(neighbour)] = neighb_fitness
                        visited_states[str(neighbour)] = neighb_fitness
                    # break
                # break
                index = np.argmin(list(results.values()))
                old_value = value
                value = list(results.keys())[index]
                value = ast.literal_eval(value) # ? Converting string back to list
                local_minima_iter = 1 if value != old_value else local_minima_iter + 1
        if n == iterations:
            print(target, " -")
        else:
            print(target, value, new_fitness, predicate_value)


def try_wrapped(tree, args):
    # print(tree)
    copy_tree = copy.deepcopy(tree)
    exec_tree = visitor.wrap_function(copy_tree, args)
    # print(astor.to_source(exec_tree))
    trace = []
    code = compile(exec_tree, filename='<blah>', mode='exec')
    namespace = {}
    exec(code, namespace)
    # TODO Get name of function automatically
    blockPrint()
    namespace['wrapper'](trace)
    enablePrint()
    return trace

# def try_input(tree, input):
#     trace = []
#     code = compile(tree, filename='<blah>', mode='exec')
#     namespace = {}
#     exec(code, namespace)
#     # TODO Get name of function automatically
#     blockPrint()
#     namespace['test_me'](input, trace)
#     enablePrint()
#     return trace

def calculate_fitness(trace, path):
    approach = ('None', 10000, None, None), len(path) - 1
    # print(trace)
    # print(path)
    for entry in trace:
        for stop in path:
            if stop.compare(entry):
                approach_level = len(path) - 1 - path.index(stop)
                if approach_level < approach[1] or approach_level == 0:
                    approach = entry, approach_level
                break
    approach_level = approach[1]
    branch_distance = approach[0][1]
    # print(branch_distance)
    fitness = approach_level + (1 - math.pow(1.001, -branch_distance)) 
    return fitness, approach[0][2] 


if __name__ == "__main__":
    main()