from charm.toolbox.integergroup import IntegerGroupQ


class Signer:

    def __init__(self, g, a):
        self.x = group.random()
        self.g = g
        self.a = a

    def sign(self, m):
        X = g ** self.x
        c = group.hash(m, X)
        s = self.x + self.a * c
        return {'s': s, 'X': X}


class Verifier:

    def __init__(self, A):
        self.A = A

    def verify(self, sigma, m):
        X = sigma['X']
        s = sigma['s']
        c = group.hash(m, X)
        return g ** s == X * self.A ** c


group = IntegerGroupQ(1024)
group.paramgen(1024)
g = group.randomGen()
a = group.random()

message = "Message"
signer = Signer(g, a)
verifier = Verifier(g ** a)

sigma = signer.sign(message)

verified = verifier.verify(sigma, message)
print(verified)
