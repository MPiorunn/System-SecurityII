from charm.toolbox.integergroup import IntegerGroupQ


class Signer:

    def __init__(self, sk):
        self.x = group.random()
        self.g = sk['g']
        self.a = sk['a']

    def sign(self, m):
        X = self.g ** self.x
        c = group.hash(m, X)
        s = self.x + self.a * c
        return {'s': s, 'X': X}


class Verifier:

    def __init__(self, pk):
        self.g = pk['g']
        self.A = pk['A']

    def verify(self, sigma, m):
        X = sigma['X']
        s = sigma['s']
        c = group.hash(m, X)
        return self.g ** s == X * self.A ** c


def keygen():
    g = group.randomGen()
    a = group.random()
    sk = {'g': g, 'a': a}
    pk = {'g': g, 'A': g ** a}
    return pk, sk


group = IntegerGroupQ(1024)
group.paramgen(1024)
(pk, sk) = keygen()

message = "Message"
signer = Signer(sk)
verifier = Verifier(pk)

sigma = signer.sign(message)

verified = verifier.verify(sigma, message)
print(verified)
