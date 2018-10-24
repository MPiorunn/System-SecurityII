from charm.toolbox.integergroup import IntegerGroupQ


class Prover():

    def __init__(self, g, a, group) -> None:
        self.g = g
        self.a = a
        self.group = group

    def sendX(self):
        self.x = group.random()
        X = g ** self.x
        return X

    def sendS(self, c):
        s = self.x + a * c
        return s


class Verifier():

    def __init__(self, g, A, group):
        self.g = g
        self.A = A
        self.group = group

    def sendC(self, X):
        self.c = group.random()
        self.X = X
        return self.c

    def verify(self, s):
        left = self.g ** s
        right = self.X * (self.A ** self.c)
        return left == right


group = IntegerGroupQ(1024)
group.paramgen(1024)
g = group.randomGen()
a = group.random()
prover = Prover(g, a, group)
verifier = Verifier(g, g ** a, group)

X = prover.sendX()
c = verifier.sendC(X)
s = prover.sendS(c)

print(verifier.verify(s))
