from hashlib import sha1
from functools import reduce

def ID(x):
    return sha1(str(x).encode('utf-8')).hexdigest()


def product(l):
    return reduce(lambda x, y: x * y, l)


def LI_EXP(x, phi):
    return product(
        grLx ** product((x - mj) / (m - mj) for mj, _ in phi if mj != m)
        for m, grLx in phi
    )
