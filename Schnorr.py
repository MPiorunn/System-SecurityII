from charm.toolbox.integergroup import IntegerGroupQ


class Schnorr():

    def __init__(self, groupObj, bitsize):
        global group
        group = groupObj
        group.paramgen(bitsize)

    def keyGeneration(self):
        g = group.randomGen()
        a = group.random()
        pk = {'g': g, 'A': g ** a}
        sk = a
        return pk, sk

    def generateX(self, pk):
        x = group.random()
        X = pk['g'] ** x
        return X, x

    def challenge(self):
        c = group.random()
        return c

    def response(self, x, c, sk):
        s = (x + c * sk)
        return s

    def verify(self, s, X, pk, c):
        return (pk['g'] ** s) == (X * pk['A'] ** c)




group1 = IntegerGroupQ()
scheme = Schnorr(group1, 256)
(pk, sk) = scheme.keyGeneration()
(X, x) = scheme.generateX(pk)
c = scheme.challenge()
s = scheme.response(x, c, sk)
decision = scheme.verify(s, X, pk, c)
if (decision):
    print("GOod")
else:
    print("Bad")