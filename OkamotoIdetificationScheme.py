from charm.toolbox.integergroup import IntegerGroupQ


class Prover:

    def __init__(self, sk) -> None:
        self.x1 = group.random()
        self.x2 = group.random()
        self.a1 = sk['a1']
        self.a2 = sk['a2']
        self.g1 = sk['g1']
        self.g2 = sk['g2']

    def sendX(self):
        X = self.g1 ** self.x1 * self.g2 ** self.x2
        return X

    def sendS(self, c):
        s1 = self.x1 + self.a1 * c
        s2 = self.x2 + self.a2 * c
        return s1, s2


class Verifier:

    def __init__(self, pk):
        self.c = group.random()
        self.A = pk['A']
        self.g1 = pk['g1']
        self.g2 = pk['g2']

    def sendC(self, X):
        self.X = X
        return self.c

    def verify(self, s1, s2):
        left = (self.g1 ** s1) * (self.g2 ** s2)
        right = X * (self.A ** c)
        return left == right


def keygen():
    g1 = group.randomGen()
    g2 = group.randomGen()
    a1 = group.random()
    a2 = group.random()
    sk = {'g1': g1, 'g2': g2, 'a1': a1, 'a2': a2}
    pk = {'g1': g1, 'g2': g2, 'A': (g1 ** a1) * (g2 ** a2)}
    return pk, sk


group = IntegerGroupQ(1024)
group.paramgen(1024)
(pk, sk) = keygen()
prover = Prover(sk)
verifier = Verifier(pk)

X = prover.sendX()
c = verifier.sendC(X)
(s1, s2) = prover.sendS(c)

print(verifier.verify(s1, s2))
