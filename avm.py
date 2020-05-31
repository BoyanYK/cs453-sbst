from fitness import calculate_fitness
from math import floor, ceil
import random

class AVM():
    def __init__(self, tree, path):
        self.results = {}
        self.tree = tree
        self.path = path
    
    def get_f(self, value):
        value = [value]
        if str(value) in self.results:
            return self.results[str(value)]
        else:
            fitness = calculate_fitness(self.tree, value, self.path)[0]
            self.results[str(value)] = fitness
            return fitness

    def satisfied_condition(self, value):
        return calculate_fitness(self.tree, [value], self.path)[1]

    def avm_ips(self):
        x = random.randint(0,100)
        fitness = self.get_f(x)
        while fitness > 0:
            # print(x)
            if self.get_f(x - 1) >= fitness and self.get_f(x + 1) >= fitness:
                # if self.satisfied_condition(x):
                return x, fitness
            k = -1 if self.get_f(x - 1) < self.get_f(x + 1) else 1
            while self.get_f(x + k) < self.get_f(x):
                # print("Line 28 ",x, fitness)
                fitness = self.get_f(x + k)
                x = x + k
                k = 2 * k
        return x, fitness

    def avm_gs(self):
        x = 0
        print(self.get_f(x))
        print(self.get_f(x-1))
        print(self.get_f(x+1))
        if self.get_f(x - 1) >= self.get_f(x) and self.get_f(x + 1) >= self.get_f(x):
            return x
        k = -1 if self.get_f(x - 1) < self.get_f(x + 1) else 1
        while self.get_f(x + k) < self.get_f(x):
            x = x + k
            k = 2 * k
            if self.get_f(x + k) <= 0:
                return self.get_f(x + k)
        l = min(x - k / 2, x + k)
        r = max(x - k / 2, x + k)
        while l < r:
            if self.get_f(floor((l + r) / 2)) < self.get_f(floor((l + r) / 2) + 1):
                r = floor((l + r) / 2)
            else:
                l = floor((l + r) / 2) + 1
        return l

