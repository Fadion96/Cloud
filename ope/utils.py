from functools import reduce
from charm.core.math.integer import reduce as reduce_mod

class Polynomial:

    def __init__(self, coefficients):
        self.coefficients = coefficients

    def __len__(self):
        return len(self.coefficients)

    def __call__(self, x):
        return reduce_mod(reduce(lambda prev, curr: curr * x + prev, self.coefficients))

    def __getitem__(self, i):
        return self.coefficients[i]

    def __setitem__(self, i, value):
        self.coefficients[i] = value

    def get_degree(self):
        return len(self.coefficients) - 1

def product(A):
    return reduce(lambda x, y: x * y, A)

def summ(A):
    return reduce(lambda x, y: x + y, A)

def LI(argument, interpolation_set):
    return reduce_mod(summ(
        yj * product((argument - xm) / (xj - xm)
                             for xm, _ in interpolation_set if xm != xj)
        for xj, yj in interpolation_set
    ))
