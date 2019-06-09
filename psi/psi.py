from charm.toolbox.integergroup import IntegerGroupQ, integer

G = IntegerGroupQ()
G.paramgen(1024)


def generate_sets(number_of_mutual, number_of_x, number_of_y):

    mutual_elements = generate_elements(number_of_mutual)

    X = generate_elements(number_of_y) + mutual_elements
    Y = [e for e in generate_elements(number_of_y) if e not in X] + mutual_elements

    return X, Y, mutual_elements


def generate_elements(number_of_elements):
    return [G.random() for _ in range(number_of_elements)]

def hash_elements(elements):
    return [G.hash(element) for element in elements]

def generate_Gs(X):

    # hash each element of the set
    gs = hash_elements(X)

    # pick a random a
    a = G.random()

    # generate big G = g ** a
    Gs = [g ** a for g in gs]

    return Gs, a


def generate_Hs_and_Bs(Y, Gs):

    # hash each element of the set
    hs = hash_elements(Y)

    # pick a random b
    b = G.random()

    # generate big H = h ** b
    Hs = [h ** b for h in hs]

    # generate Bs
    Bs = [G ** b for G in Gs]

    return Hs, Bs


def generate_As(Hs, a):
    As = [H ** a for H in Hs]
    return As


def main():

    # generate sets
    X, Y, mutual = generate_sets(4,10,12)

    # generate Gs
    Gs, a = generate_Gs(X)

    # generate Hs and Bs
    Hs, Bs = generate_Hs_and_Bs(Y, Gs)

    # generate As
    As = generate_As(Hs, a)

    # A side compares
    a_mutual = [el1 for el1, el2 in zip(X, Bs) if el2 in As]

    # B side compares
    b_mutual = [el1 for el1, el2 in zip(Y, As) if el2 in Bs]

    assert a_mutual == b_mutual == mutual


if __name__ == "__main__":
    main()
