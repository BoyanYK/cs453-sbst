import ast

def fitness_pred(pred):
    # print(pred)
    # TODO Need to handle if predicate is compared to another value or to another variable
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