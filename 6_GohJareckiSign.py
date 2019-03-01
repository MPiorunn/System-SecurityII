from charm.toolbox.integergroup import IntegerGroupQ


class Signer:

    def __init__(self, sk):
        self.g = sk['g']
        self.a = sk['a']

    def sign(self, m):
        A = self.g ** self.a
        r = group.random()
        h = group.hash(m, r)
        x = group.random()
        H = h ** self.a
        X = h ** x
        R = self.g ** x
        c = group.hash(m, r, X, A, H, R)
        s = x + self.a * c
        return {'R': r, 'X': X, 'H': H, 's': s, 'r': r}


#

class Verifier:

    def __init__(self, pk):
        self.g = pk['g']
        self.A = pk['A']

    def verify(self, sig, m):
        h = group.hash(m, sig['r'])
        c = group.hash(m, sig['r'], sig['X'], self.A, sig['H'], sig['R'])
        left = (self.g ** sig['s']) == sig['R'] * (self.A ** c)  # wyjatek tutaj leci :(
        right = h ** sig['s'] == sig['X'] * sig['H'] ** c
        return left == right


def keygen():
    g = group.randomGen()
    a = group.random()
    sk = {'g': g, 'a': a}
    pk = {'g': g, 'A': g ** a}
    return pk, sk


group = IntegerGroupQ()
group.paramgen(1024)
(pk, sk) = keygen()
signer = Signer(sk)
verifier = Verifier(pk)
message = "Mama tata"
sigma = signer.sign(message)
result = verifier.verify(sigma, message)
print(result)
