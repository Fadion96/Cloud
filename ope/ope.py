import random
from charm.toolbox.integergroup import IntegerGroupQ, integer
from charm.core.math.integer import reduce as reduce_mod
from utils import Polynomial, LI

G = IntegerGroupQ()
G.paramgen(1024)
g = G.randomG()

def gen_coeffs(degree):
    return [G.random() for _ in range(degree + 1)]

def main():
    m = 2
    d_p = 5
    k = 4
    d = k * d_p

    P = Polynomial(gen_coeffs(d_p))
    P_x = Polynomial(gen_coeffs(d))
    P_x[0] = integer(0, G.q)
    Q = lambda x, y: reduce_mod(P_x(x) + P(y))

    alpha = G.random()
    S = Polynomial(gen_coeffs(k))
    S[0] = alpha

    n = k * d_p + 1
    N = n * m
    X = [G.random() for _ in range(N)]

    # The receiver chooses a random set T of n indices 1 ≤ i1, i2, . . . , in ≤ N.
    T = list(range(N))
    random.shuffle(T)
    T = T[:n]

    # Receiver defines N values yi, for 1 ≤ i ≤ N. The value yi is defined as
    # S(xi) if i is in T, and is a random value if F otherwise.
    # The receiver sends the N points (Y) to the sender
    Y = [(x, S(x) if i in T else G.random()) for i, x in enumerate(X)]
    Qs = [(x, Q(x, y)) for x, y in Y]

    # Receiver calculates values.
    R_values = [v for i, v in enumerate(Qs) if i in T]
    R_0 = LI(integer(0, G.q), R_values)
    P_alpha = P(alpha)

    assert R_0 == P_alpha

if __name__ == '__main__':
    main()
