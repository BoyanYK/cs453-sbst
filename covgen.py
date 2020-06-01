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
from utils import TimeExceeded

def main():
    target_path = sys.argv[1]
    method = "avm_ips"
    target_function = "test_me"
    iterations = 1000
    try:
        method = sys.argv[2]
        iterations = int(sys.argv[3])
    except IndexError:
        # iterations = 1000
        pass
    target_tree = astor.parse_file(target_path)
    # print(astor.dump_tree(target_tree))
    # TODO Custom target function name
    targets, arg_count = control_flow.get_targets(target_tree, target_function)
    if "avm" in method:
        perform_avm(target_tree, targets, arg_count, 10, method, iterations, target_function)
    elif "hill_climb" in method:
        hill_climb(target_tree, targets, arg_count, iterations, target_function)



def perform_avm(tree, targets, arg_count, retry_count, method, iterations, target_function="test_me"):
    import avm
    results_true = {}
    results_false = {}
    for target, path in targets.items():
        path = list(reversed(path))[1:]
        print("\nStarting :", target)
        # print(results_true)
        # print(results_false)
        for state in [True, False]:
            start_value = None
            # if state:
            for prev_target, (inputs, _) in results_true.items():
                # inputs, _ = value
                # print('-----\n',prev,'-----')
                # print(prev_target, prev_state)
                # if prev_target in path and prev_target.lineno != target.lineno:
                    # start_value = inputs
                start_value = copy.deepcopy(inputs) if type(inputs) == list else None
                    # print('----- ',prev_target, target, start_value, ' -----')
            # print(results_true)
            instrumented = visitor.TargetInstrumentation(target, state)
            instrumented = instrumented.visit(copy.deepcopy(tree))
            search = avm.AVM(instrumented, path, arg_count, retry_count, state, iterations, target_function)
            # value = search.avm_ips()
            value = search.search(method, start_value)
            print(target," Value: ", value)
            # print(target, state)
            if state:
                results_true[target] = value
            else:
                results_false[target] = value
                # print(results_false)
            # results[(target, state)] = value


def hill_climb(tree, targets, arg_count, iterations, target_function="test_me"):
    import numpy as np
    for target, path in targets.items():
        path = list(reversed(path))[1:] # Removes function_def node
        for state in [True, False]:
            instrumented = visitor.TargetInstrumentation(target, state)
            instrumented = instrumented.visit(copy.deepcopy(tree))
            # ast.fix_missing_locations(instrumented)

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
                try:
                    new_fitness, predicate_value, approach_level = calculate_fitness(instrumented, value, path, target_function)
                    visited_states[str(value)] = new_fitness
                    # print(value, new_fitness, predicate_value)
                    if new_fitness <= 0 and predicate_value == state and approach_level == 0:
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
                                neighb_fitness, neighb_predicate_value, approach_level = calculate_fitness(instrumented, neighbour, path, target_function)
                                results[str(neighbour)] = neighb_fitness
                                visited_states[str(neighbour)] = neighb_fitness
                            # break
                        # print(results)
                        index = np.argmin(list(results.values()))
                        old_value = value
                        value = list(results.keys())[index]
                        value = ast.literal_eval(value) # ? Converting string back to list
                        local_minima_iter = 1 if value != old_value else local_minima_iter * 2
                except TimeExceeded:
                    n = iterations + 1
                    break
                    # break
            if n > iterations:
                print(target, " -")
            else:
                print(target, value, new_fitness, predicate_value)
        # print(n)
        # break


if __name__ == "__main__":
    main()