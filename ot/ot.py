import secrets
from charm.schemes.pkenc.pkenc_rsa import RSA
from charm.core.math.integer import random

class A:
    def __init__(self, N, d):
        self.N = N
        self.d = d

    def generate_messages(self, nr_of_messages):
        self.messages = [random(self.N) for _ in range(nr_of_messages)]

    def generate_random(self, nr_of_messages):
        self.xs = [random(self.N) for _ in range(nr_of_messages)]
        return self.xs

    def mask_messages(self,v):
        self.ks = [(v - x) ** self.d for x in self.xs]
        self.masked = [message + k for message, k in zip(self.messages, self.ks)]
        return self.masked


class B:
    def __init__(self, N, e):
        self.N = N
        self.e = e

    def choose(self, xs, nr_of_messages):
        self.xs = xs
        self.b = secrets.randbelow(nr_of_messages)
        self.k = random(self.N)
        self.v = self.xs[self.b] + (self.k ** self.e)
        return self.v

    def decrypt(self, masked):
        self.message = masked[self.b] - self.k

def generate_RSA(key_size):
    pk, sk = RSA().keygen(key_size)
    return sk['d'], pk['N'], pk['e']

def main():
    nr_of_messages = 15
    d, N, e = generate_RSA(2048)
    a = A(N,d)
    b = B(N,e)
    a.generate_messages(nr_of_messages)
    xs = a.generate_random(nr_of_messages)
    v = b.choose(xs, nr_of_messages)
    masked = a.mask_messages(v)
    b.decrypt(masked)

    assert a.messages[b.b] == b.message

if __name__ == "__main__":
    main()
