from random import shuffle
import secrets
from charm.schemes.pkenc.pkenc_rsa import RSA
from charm.core.math.integer import random, integer

from charm.toolbox.symcrypto import SymmetricCryptoAbstraction


def generate_RSA(key_size):
    pk, sk = RSA().keygen(key_size)
    return sk['d'], pk['N'], pk['e']

def generate_keys(bytes):
    return [secrets.randbits(bytes * 8) for _ in range(2)]

def generate_random(value):
    xs = [random(value) for _ in range(2)]
    return xs

def choose(b, k, xs, e):
    v = xs[b] + (k ** e)
    return v

def mask_messages(v, xs, N, d, messages):
    ks = [(v - x) ** d for x in xs]
    masked = [integer(message, N) + k for message, k in zip(messages, ks)]
    return masked

def enc(k1, k2, msg):
    a1 = SymmetricCryptoAbstraction(k1.to_bytes(16,byteorder='big'))
    a2 = SymmetricCryptoAbstraction(k2.to_bytes(16,byteorder='big'))
    c0 = a1.encrypt(msg.to_bytes(16,byteorder='big'))
    c1 = a2.encrypt(c0)
    return c1
#
def dec(k1, k2, ct):
    a1 = SymmetricCryptoAbstraction(k1.to_bytes(16,byteorder='big'))
    a2 = SymmetricCryptoAbstraction(k2.to_bytes(16,byteorder='big'))
    m0 = a2.decrypt(ct)
    m1 = a1.decrypt(m0)
    return m1
#
# A_0, A_1 = [os.urandom(128) for _ in range(2)]
# B_0, B_1 = [os.urandom(128) for _ in range(2)]
# C_0, C_1 = [os.urandom(128) for _ in range(2)]
#

# # random.shuffle(Table)
#
#
# Alice_A = A_1
# Bob_b   = B_1
#
# for i, t in enumerate(Table):
#     try:
#         print(i)
#         a = dec(Alice_A, Bob_b, t)
#         print(a == C_1)
#         print(a == C_0)
#     except:
#         pass

def main():
    d, N, e = generate_RSA(256)
    k_a = generate_keys(16)
    k_b = generate_keys(16)
    k_c = generate_keys(16)
    table = [
        enc(k_a[0], k_b[0], k_c[0]),
        enc(k_a[0], k_b[1], k_c[0]),
        enc(k_a[1], k_b[0], k_c[0]),
        enc(k_a[1], k_b[1], k_c[1])
    ]
    shuffle(table)
    key_a = secrets.choice(k_a)
    # OT
    xs = generate_random(N)
    bit = secrets.randbelow(2)
    k = random(N)
    v = choose(bit, k, xs, e)
    ks = mask_messages(v, xs, N, d, k_b)
    key_b = int(ks[bit] - k)
    #Bob has k_b_bit
    print(k_c)
    for ct in table:
        try:
            key_c = int.from_bytes(dec(key_a, key_b, ct), byteorder='big')
            for key in k_c:
                if key_c == key:
                    print(key_c)
                    break
        except:
            pass

if __name__ == '__main__':
    main()
