from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair


class Prover:

    def __init__(self, sk):
        self.x = group.random()
        self.g = sk['g']
        self.a = sk['a']

    def sendX(self):
        self.X = self.g ** self.x
        return self.X

    def sendS(self, c):
        b = self.X * c
        g2 = group.hash(b, G1)
        S = g2 ** (self.x + self.a * c)
        return S


class Verifier:

    def __init__(self, pk):
        self.g = pk['g']
        self.A = pk['A']

    def sendC(self, X):
        self.X = X
        return self.c

    def verify(self, S):
        self.c = group.random()
        left = pair(S, self.g)
        h = group.hash((self.X * self.c), G1)
        right = pair(h, self.X * self.A ** c)

        return left == right


def keygen():
    g = group.random(G2)
    a = group.random()
    sk = {'g': g, 'a': a}
    pk = {'g': g, 'A': g ** a}
    return pk, sk


group = PairingGroup('MNT224')
(pk, sk) = keygen()
prover = Prover(sk)
verifier = Verifier(pk)

X = prover.sendX()
c = verifier.sendC(X)
S = prover.sendS(c)

verified = verifier.verify(S)
print(verified)
