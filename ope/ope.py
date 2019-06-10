from random import shuffle
from charm.toolbox.integergroup import IntegerGroupQ, integer
from charm.core.math.integer import reduce as reduce_mod
from utils import Polynomial, LI

G = IntegerGroupQ()
G.paramgen(1024)
g = G.randomG()

def gen_coeffs(degree):
    return [G.random() for _ in range(degree + 1)]

def main():
    d_p = 5 # degree of polynomial P
    k = 4 # Security parameter and degree of polynomial s
    d = k * d_p # degree of polynomials P_x and Q
    m = 2

    # Sender has polynomial P of degree d_p
    P = Polynomial(gen_coeffs(d_p))
    # Sender generates random masking polynomial P_x of degree d
    P_x = Polynomial(gen_coeffs(d))
    # P_x(0) = 0
    P_x[0] = integer(0, G.q)
    # Sender defines bivariate polynomial Q which holds Q(0,y) = P(y)
    Q = lambda x, y: reduce_mod(P_x(x) + P(y))

    # Receiver generates alpha
    alpha = G.random()
    # Receiver chooses random polynomial S of degree k
    S = Polynomial(gen_coeffs(k))
    # S(0) = alpha
    S[0] = alpha

    # The receiver wants use univariate polynomial R(x) = Q(x,S(x))
    # R(0) = Q(0,S(0)) = P(alpha)
    # So if receiver is able to interpolate R, then can learn R(0) = P(alpha)
    # Degree of R is d_r = d = k * d_p

    # Receiver want to learn n values of R to interpolate the polynomial.
    # To achieve that, receiver uses n-of-N OT
    n = k * d_p + 1 # number of values of R required to interpolate R.
    N = n * m # number of distinct random values x, all different from 0.
    xs = [G.random() for _ in range(N)]

    for x in xs:
        while x == integer(0, G.q):
            x = G.random()

    # The receiver chooses a random set T of n indices between 1 and N.
    T = list(range(N))
    shuffle(T)
    T = T[:n]

    # Receiver defines N values y. The value yi is defined as
    # S(xi) if i is in T, and is a random value if F otherwise.
    # The receiver sends the N points (x,y) to the sender
    Y = [(x, S(x) if i in T else G.random()) for i, x in enumerate(xs)]

    # Sender evaluates Q(x,y) for each pair x,y in Y
    Qs = [(x, Q(x, y)) for x, y in Y]

    # Receiver chooses to learn R(x_i) values for i in T.
    R_values = [v for i, v in enumerate(Qs) if i in T]
    # Receiver interpolates R in order to learn R(0) = P(alpha)
    R_0 = LI(integer(0, G.q), R_values)
    P_alpha = P(alpha)

    assert R_0 == P_alpha

if __name__ == '__main__':
    main()
