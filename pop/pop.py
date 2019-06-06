import functools
from poly import Polynomial
from utils import ID, product, LI_EXP
from charm.toolbox.integergroup import IntegerGroupQ, integer
import random
import pdb


def setup(security_parameter):
    G = IntegerGroupQ()
    G.paramgen(security_parameter)
    g = G.randomG()
    sk = G.random()
    return G, g, sk


def generate_f(G, n, z):
    return [integer(random.randrange(2 ** n), G.q) for _ in range(z)]

def create_polynomial(G, fid, sk, z):
    random.seed(str(sk) + fid)
    coefficients = [integer(random.randrange(G.q), G.q) for _ in range(z + 1)]

    for coeff in coefficients:
        while coeff == 0:
            coeff = integer(random.randrange(G.q), G.q)

    return Polynomial(coefficients)


def generate_tag_block(polynomial, f):
    return [(m, polynomial(m)) for m in f]


def generate_challenge(G, g, sk, fid, z):
    poly = create_polynomial(G, fid, sk, z)
    r = G.random()
    x_c = G.random()  # x_c != m_i

    K_f = g ** (r * poly(x_c))
    H = (g ** r, x_c, g ** (r * poly[0]))
    return K_f, H


def generate_proof(G, Tf, H):
    g_r, x_c, g_r_Lf0 = H
    phi = generate_phi_set(G, g_r_Lf0, Tf, g_r)
    P_f = LI_EXP(x_c, phi)
    return P_f


def generate_phi_set(G, g_r_Lf0, Tf, g_r):
    phi_set = [(integer(0, G.q), g_r_Lf0)]

    for m, t in Tf:
        element = (m, g_r ** t)
        phi_set.append(element)
    return phi_set


def main():
    n = 256
    z = 16
    G, g, sk = setup(1024)
    f = generate_f(G, n, z)
    polynomial = create_polynomial(G, ID(f), sk, z)
    tags = generate_tag_block(polynomial, f)
    K_f, H = generate_challenge(G, g, sk, ID(f), z)
    P_f = generate_proof(G, tags, H)
    assert K_f == P_f



if __name__ == '__main__':
    main()
