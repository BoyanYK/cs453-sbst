# class State(object):
#     def __init__(self, arg_count):
#         self.
import itertools

def get_neighbours(state, step):
    """[summary]
    Get neighbouring values of input vector
    Essentially the cross products of all neighbouring values of each individual element
    Arguments:
        state {list} -- Input vector
        step {int} -- Iterations without change (of fitness)

    Returns:
        [list] -- All possible neighbours
    """
    neighbs = {}
    for i, value in enumerate(state):
        neighbs[i] = [value + step, value, value - step]

    inputs = []
    for neighb in neighbs.values():
        inputs.append(neighb)
        
    # print(list(itertools.product(*inputs)))
    # print("STATE ", state)
    return list(itertools.product(*inputs))