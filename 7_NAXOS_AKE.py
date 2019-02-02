from charm.toolbox.integergroup import IntegerGroupQ


class Alice:

    def __init__(self, ak, pk):
        self.pk = pk
        self.g = pk['g']
        self.a = ak['a']

    def sendX(self):
        self.x = group.random()
        h = group.hash(self.x, self.a)
        X = self.g ** h
        return X

    def calculateSessionKey(self, Y):
        arg1 = Y ** self.a
        arg2 = self.pk['B'] ** (group.hash(self.x, self.a))
        arg3 = Y ** group.hash(self.x, self.a)
        Ka = group.hash(arg1, arg2, arg3)
        return Ka


class Bob:

    def __init__(self, bk, pk):
        self.pk = pk
        self.g = pk['g']
        self.b = bk['b']

    def sendY(self):
        self.y = group.random()
        h = group.hash(self.y, self.b)
        Y = self.g ** h
        return Y

    def calculateSessionKey(self, X):
        arg1 = self.pk['A'] ** (group.hash(self.y, self.b))
        arg2 = X ** self.b
        arg3 = X ** group.hash(self.y, self.b)
        Kb = group.hash(arg1, arg2, arg3)
        return Kb


def keygen():
    g = group.randomGen()
    a = group.random()
    b = group.random()
    p_k = {'A': g ** a, 'B': g ** b, 'g': g}
    a_k = {'a': a, 'g': g}
    b_k = {'b': b, 'g': g}
    return a_k, b_k, p_k


group = IntegerGroupQ(1024)
group.paramgen(1024)
(a_k, b_k, p_k) = keygen()

alice = Alice(a_k, p_k)
bob = Bob(b_k, p_k)

X = alice.sendX()
Y = bob.sendY()

K1 = alice.calculateSessionKey(Y)
K2 = bob.calculateSessionKey(X)

print(K1 == K2)
