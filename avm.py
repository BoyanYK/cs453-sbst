from fitness import calculate_fitness
from math import floor, ceil
import random
import copy
from utils import fib, min_n

class AnswerFound(Exception):
    pass

class AVM():
    def __init__(self, tree, path, arg_count, attempts, state):
        self.results = {}
        self.tree = tree
        self.path = path
        self.arg_count = arg_count
        self.attempts = attempts
        self.state = state
        self.answer = None
        self.range = 10
    
    def get_f(self, inputs, index, value):
        inputs[index] = value
        if str(inputs) in self.results:
            return self.results[str(inputs)]
        else:
            fitness, branch_state, approach_level = calculate_fitness(self.tree, inputs, self.path)
            # if not self.state:
                # print(fitness, branch_state, inputs)
            if approach_level == 0 and branch_state == self.state:
                self.answer = inputs, (fitness, branch_state, approach_level)
                raise AnswerFound
            self.results[str(inputs)] = fitness
            return fitness

    def satisfied_condition(self, inputs):
        return calculate_fitness(self.tree, inputs, self.path)[1] == self.state

    def search(self, method="avm_ips", inputs=None):
        if "ips" in method:
            return self.avm(self.avm_ips, inputs)
        elif "gs" in method:
            return self.avm(self.avm_gs, inputs)
        elif "ls" in method:
            return self.avm(self.avm_ls, inputs)

    def avm(self, method, inputs=None):
        # for method in [self.avm_ips, self.avm_gs]:
        for j in range(self.attempts):
            # print("Starting inputs, iteration ", inputs, j)
            if not inputs:
                inputs = [random.randint(-self.range, self.range) for i in range(self.arg_count)]
            # start_inputs = copy.deepcopy(inputs)
            for i, value in enumerate(inputs):
                try:
                    value, fitness = method(inputs, i)
                except AnswerFound:
                    # print("Found Answer")
                    # print(self.answer)
                    return self.answer
                if fitness <= 0.0 and self.satisfied_condition(inputs):
                    # break
                    return inputs, calculate_fitness(self.tree, inputs, self.path)
                inputs[i] = value
            if self.satisfied_condition(inputs):
                return inputs, calculate_fitness(self.tree, inputs, self.path)
            inputs = None
            self.range *= 10
        # print(self.results)
        # print('---')
        # for res in self.results.items():
        #     print(res)
        # print('---')
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

    def avm_ls(self, inputs, index):
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
        n = min_n(r, l)
        while n > 3:
            if l + fib(n-1) - 1 <= r and self.get_f(inputs, index, l + fib(n-2) - 1) >= self.get_f(inputs, index, l + fib(n-1) - 1):
                l = l + fib(n-2)
            n -= 1
        x = l
        return x, fitness