from charm.toolbox.integergroup import IntegerGroupQ


class Prover:

    def __init__(self, sk) -> None:
        self.x = group.random()
        self.g = sk['g']
        self.a = sk['a']

    def sendX(self):
        X = self.g ** self.x
        return X

    def sendS(self, c):
        s = self.x + self.a * c
        return s


class Verifier:

    def __init__(self, pk):
        self.g = pk['g']
        self.A = pk['A']

    def sendC(self, X):
        self.X = X
        self.c = group.random()
        return self.c

    def verify(self, s):
        left = self.g ** s
        right = self.X * (self.A ** self.c)
        return left == right


def keygen():
    g = group.randomGen()
    a = group.random()
    sk = {'g': g, 'a': a}
    pk = {'g': g, 'A': g ** a}
    return pk, sk


group = IntegerGroupQ(1024)
group.paramgen(1024)
(pk, sk) = keygen()
prover = Prover(sk)
verifier = Verifier(pk)

X = prover.sendX()
c = verifier.sendC(X)
s = prover.sendS(c)

print(verifier.verify(s))
