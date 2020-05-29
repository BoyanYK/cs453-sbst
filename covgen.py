import ast
import astor
import visitor
import control_flow
import sys
import math

def main():
    target_path = sys.argv[1]
    target_tree = astor.parse_file(target_path)
    instrumented = visitor.TargetInstrumentation().visit(target_tree)
    ast.fix_missing_locations(instrumented)

    targets = control_flow.get_targets(target_tree)

    search(instrumented, targets)

def search(tree, targets):
    # TODO Loop for all targets ..
    # for target, path in targets.items():
    path = list(targets.values())[2]
    print(path)
    path = list(reversed(path))[1:] # Removes function_def node
    # TODO Loop until fitness function ... 
    trace = try_input(tree, [])
    fitness, predicate_value = calculate_fitness(trace, path)
    print(fitness, predicate_value)
    # TODO New inputs based on fitness.. 

def try_input(tree, inputs):
    trace = []
    code = compile(tree, filename='<blah>', mode='exec')
    namespace = {}
    exec(code, namespace)
    # TODO Get name of function automatically
    # TODO Pass correct number of arguments
    namespace['test_me'](0, trace)
    return trace

def calculate_fitness(trace, path):
    approach = None, len(path) - 1
    for entry in trace:
        for stop in path:
            if stop.compare(entry):
                approach_level = len(path) - 1 - path.index(stop)
                if approach_level < approach[1]:
                    approach = entry, approach_level
                break
    approach_level = approach[1]
    branch_distance = approach[0][1]
    fitness = approach_level + (1 - math.pow(1.001, -branch_distance)) 
    # print("Approach ", approach)
    return fitness, approach[0][2]


if __name__ == "__main__":
    main()