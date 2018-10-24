from charm.toolbox.integergroup import IntegerGroupQ


class Okamoto():

    def __init__(self, groupObj, bitsize):
        global group
        group = groupObj
        group.paramgen(bitsize)

    def keyGeneration(self):
        g1 = group.randomGen()
        g2 = group.randomGen()
        a1 = group.random()
        a2 = group.random()
        A = (g1 ** a1) * (g2 ** a2)
        pk = {'g1': g1, 'g2': g2, 'A': A}
        sk = {'a1': a1, 'a2': a2}
        return pk, sk

    def generateX(self, pk):
        x1 = group.random()
        x2 = group.random()
        X = (pk['g1'] ** x1) * (pk['g2'] ** x2)
        return X, x1, x2

    def challenge(self):
        c = group.random()
        return c

    def response(self, x1, x2, c, sk):
        s1 = (x1 + c * sk['a1'])
        s2 = (x2 + c * sk['a2'])
        return s1, s2

    def verify(self, s1, s2, X, pk, c):
        return ((pk['g1'] ** s1) * (pk['g2'] ** s2)) == (X * pk['A'] ** c)

group1 = IntegerGroupQ()
scheme = Okamoto(group1, 256)
(pk, sk) = scheme.keyGeneration()
(X, x1, x2) = scheme.generateX(pk)
c = scheme.challenge()
(s1, s2) = scheme.response(x1, x2, c, sk)
decision = scheme.verify(s1, s2, X, pk, c)
if (decision):
    print("GOod")
else:
    print("Bad")
