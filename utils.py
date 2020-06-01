# import ast
# from fitness import fitness_pred
import os, sys

# * Code from https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def min_n(r, l):
    n = 0
    while fib(n) < r - l + 2:
        n += 1
    return n

# * Code from https://stackoverflow.com/a/23462371
def fib(n):
    v1, v2, v3 = 1, 1, 0    # initialise a matrix [[1,1],[1,0]]
    for rec in bin(n)[3:]:  # perform fast exponentiation of the matrix (quickly raise it to the nth power)
        calc = v2*v2
        v1, v2, v3 = v1*v1+calc, (v1+v3)*v2, calc+v3*v3
        if rec=='1':    v1, v2, v3 = v1+v2, v1, v2
    return v2