from charm.toolbox.integergroup import IntegerGroupQ


class Signer:

    def __init__(self, sk):
        self.g = sk['g']
        self.a = sk['a']

    def sign(self, m):
        r = group.random()
        h = group.hash(m, r)
        H = h ** self.a
        x = group.random()
        X = h ** x
        R = self.g ** x
        A = self.g ** self.a
        c = group.hash(m, r, X, A, H, R)
        s = x + self.a * c
        return {'R': r, 'X': X, 'H': H, 's': s, 'r': r}


class Verifier:

    def __init__(self, pk):
        self.g = pk['g']
        self.A = pk['A']

    def verify(self, sig, m):
        h = group.hash(m, sig['r'])
        c = group.hash(m, sig['r'], sig['X'], self.A, sig['H'], sig['R'])
        left = self.g ** sig['s'] == sig['R'] * sig['H'] ** c  # wyjatek tutaj leci :(
        right = h ** sig['s'] == sig['X'] * sig['H'] ** c
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
signer = Signer(sk)
verifier = Verifier(pk)
message = "Mama tata"
sigma = signer.sign(message)
result = verifier.verify(sigma, message)
print(result)

'''
pseudokod
sk = a <-$Zq, pk = A <- g^a


Signer (m,a)
r<-$ {0,1}^ml
h<- H1(m,r)
H = h^a
x <-$ Zq*
R = g^x , X = h^x
c <- H2(m,r,x,A,H,R)
s = x + ac
sigma(R,X,H,s,r)

Verifier (sigma, m,A)
h <- H1(m,r)
c <- H2(m,R,X,A,H,r)
verification : g^s == RH^c && H^s  == XH^c

'''
