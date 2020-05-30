import ast
import astor
import visitor
import control_flow
import sys, os
import math
import random

def main():
    target_path = sys.argv[1]
    target_tree = astor.parse_file(target_path)
    instrumented = visitor.TargetInstrumentation().visit(target_tree)
    ast.fix_missing_locations(instrumented)

    targets = control_flow.get_targets(target_tree)

    hill_climb(instrumented, targets)

# * Code from https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def hill_climb(tree, targets):
    import numpy as np
    # TODO Loop for all targets ..
    for target, path in targets.items():
    # path = list(targets.values())[0]
    # print(path)
        path = list(reversed(path))[1:] # Removes function_def node
    # trace = try_input(tree, 1)
    # fitness, predicate_value = calculate_fitness(trace, path)
    
    # TODO Loop until fitness function ... 
        curr_fitness = 10000
        value = random.randint(0, 100)
        # value = 3
        visited_states = {}
        local_minima_iter = 1
        while True:
            trace = try_input(tree, value)
            new_fitness, predicate_value = calculate_fitness(trace, path)
            visited_states[value] = new_fitness
            if new_fitness == 0 or predicate_value:
                break
            else:
                neighbours = [value - local_minima_iter, value + local_minima_iter]
                results = {}
                results[value] = new_fitness
                for neighbour in neighbours:
                    if neighbour in visited_states:
                        results[neighbour] = visited_states[neighbour]
                    else:
                        trace = try_input(tree, neighbour)
                        neighb_fitness, neighb_predicate_value = calculate_fitness(trace, path)
                        results[neighbour] = neighb_fitness
                        visited_states[neighbour] = neighb_fitness
                # print(value)
                index = np.argmin(list(results.values()))
                old_value = value
                value = list(results.keys())[index]
                # if value == new_fitness:
                #     local_minima_iter += 1
                # else:
                #     local_minima_iter = 1
                local_minima_iter = 1 if value != old_value else local_minima_iter + 1
                # print(value)
            # print("Current value {}, fitness {}".format(value, results[value]))
            # break

        print(target, value, new_fitness, predicate_value)
    # TODO New inputs based on fitness.. 

def try_input(tree, input):
    trace = []
    code = compile(tree, filename='<blah>', mode='exec')
    namespace = {}
    exec(code, namespace)
    # TODO Get name of function automatically
    # TODO Pass correct number of arguments
    blockPrint()
    namespace['test_me'](input, trace)
    enablePrint()
    return trace

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