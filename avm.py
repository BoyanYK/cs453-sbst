from fitness import calculate_fitness
from math import floor, ceil
import random

class AVM():
    def __init__(self, tree, path, arg_count, attempts, state):
        self.results = {}
        self.tree = tree
        self.path = path
        self.arg_count = arg_count
        self.attempts = attempts
        self.state = state
    
    def get_f(self, inputs, index, value):
        inputs[index] = value
        if str(inputs) in self.results:
            return self.results[str(inputs)]
        else:
            fitness = calculate_fitness(self.tree, inputs, self.path)[0]
            self.results[str(inputs)] = fitness
            return fitness

    def satisfied_condition(self, inputs):
        return calculate_fitness(self.tree, inputs, self.path)[1] == self.state

    def search(self, method="avm_ips", inputs=None):
        if "ips" in method:
            return self.avm(self.avm_ips, inputs)
        elif "gs" in method:
            return self.avm(self.avm_gs, inputs)

    def avm(self, method, inputs=None):
        import copy
        for j in range(self.attempts):
            if not inputs:
                inputs = [random.randint(0, 100) for i in range(self.arg_count)]
            # start_inputs = copy.deepcopy(inputs)
            for i, value in enumerate(inputs):
                value, fitness = method(inputs, i)
                if fitness < 0.0:
                    return inputs, calculate_fitness(self.tree, inputs, self.path)
                inputs[i] = value
            if self.satisfied_condition(inputs):
                return inputs, calculate_fitness(self.tree, inputs, self.path)
        return "Unable to find solution", inputs

    def avm_ips(self, inputs, index):
        x = inputs[index]
        fitness = self.get_f(inputs, index, x)
        while fitness > 0:
            # print(x)
            if self.get_f(inputs, index, x - 1) >= fitness and self.get_f(inputs, index, x + 1) >= fitness:
                # if self.satisfied_condition(x):
                return x, fitness
            k = -1 if self.get_f(inputs, index, x - 1) < self.get_f(inputs, index, x + 1) else 1
            while self.get_f(inputs, index, x + k) < self.get_f(inputs, index, x):
                if fitness < 0:
                    break
                fitness = self.get_f(inputs, index, x + k)
                x = x + k
                k = 2 * k
        return x, fitness

    def avm_gs(self, inputs, index):
        x = inputs[index]
        fitness = self.get_f(inputs, index, x)
            # print(x)
        if self.get_f(inputs, index, x - 1) >= fitness and self.get_f(inputs, index, x + 1) >= fitness:
            # if self.satisfied_condition(x):
            return x, fitness
        k = -1 if self.get_f(inputs, index, x - 1) < self.get_f(inputs, index, x + 1) else 1
        while self.get_f(inputs, index, x + k) < self.get_f(inputs, index, x):
            if fitness < 0:
                break
            fitness = self.get_f(inputs, index, x + k)
            x = x + k
            k = 2 * k
        l = min(x - k / 2, x + k)
        r = max(x - k / 2, x + k)
        while l < r:
            if self.get_f(inputs, index, floor((l + r) / 2)) < self.get_f(inputs, index, floor((l + r) / 2) + 1):
                r = floor((l + r) / 2)
            else:
                l = floor((l + r) / 2) + 1
        x = l
        return x, fitness

