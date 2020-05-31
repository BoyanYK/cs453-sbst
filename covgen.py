import ast
import astor
import visitor
import control_flow
import sys, os
import math
import random
import copy
from state import get_neighbours
from fitness import calculate_fitness

def main():
    target_path = sys.argv[1]
    try:
        iterations = int(sys.argv[2])
    except IndexError:
        iterations = 1000
    target_tree = astor.parse_file(target_path)
    # TODO Custom target function name
    targets, arg_count = control_flow.get_targets(target_tree)

    # hill_climb(target_tree, targets, arg_count, iterations)
    do_avm(target_tree, targets, arg_count, 10)


def do_avm(tree, targets, arg_count, retry_count):
    import avm
    for target, path in targets.items():
        path = list(reversed(path))[1:]
        print(target)
        instrumented = visitor.TargetInstrumentation(target, True)
        instrumented = instrumented.visit(copy.deepcopy(tree))
        search = avm.AVM(instrumented, path, arg_count, retry_count)
        # value = search.avm_ips()
        value = search.avm()
        print(value)




def hill_climb(tree, targets, arg_count, iterations):
    import numpy as np
    for target, path in targets.items():
        instrumented = visitor.TargetInstrumentation(target, True)
        instrumented = instrumented.visit(copy.deepcopy(tree))
        # ast.fix_missing_locations(instrumented)

        path = list(reversed(path))[1:] # Removes function_def node
        curr_fitness = 10000
        # value = random.randint(0, 100)
        value = [random.randint(0, 100) for i in range(arg_count)]
        visited_states = {}
        local_minima_iter = 1
        # n = 0
        for n in range(iterations):
            # print(type(value))
            n += 1
            # trace = try_wrapped(instrumented, value)
            new_fitness, predicate_value, approach_level = calculate_fitness(instrumented, value, path)
            visited_states[str(value)] = new_fitness
            # print(value)
            if new_fitness <= 0 and predicate_value == True and approach_level == 0:
                break
            else:
                neighbours = get_neighbours(value, local_minima_iter)
                results = {}
                results[str(value)] = new_fitness
                for neighbour in neighbours:
                    neighbour = list(neighbour)
                    # print(neighbour)
                    if str(neighbour) in visited_states:
                        results[str(neighbour)] = visited_states[str(neighbour)]
                    else:
                        # trace = try_wrapped(instrumented, neighbour)
                        neighb_fitness, neighb_predicate_value, approach_level = calculate_fitness(instrumented, neighbour, path)
                        results[str(neighbour)] = neighb_fitness
                        visited_states[str(neighbour)] = neighb_fitness
                    # break
                # print(results)
                index = np.argmin(list(results.values()))
                old_value = value
                value = list(results.keys())[index]
                value = ast.literal_eval(value) # ? Converting string back to list
                local_minima_iter = 1 if value != old_value else local_minima_iter * 2
                # break
        if n > iterations:
            print(target, " -")
        else:
            print(target, value, new_fitness, predicate_value)
        # print(n)
        # break


if __name__ == "__main__":
    main()