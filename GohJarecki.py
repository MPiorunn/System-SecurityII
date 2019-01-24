from charm.toolbox.integergroup import IntegerGroupQ


class Prover:

    def __init__(self, g, a) -> None:
        self.x = group.random()
        self.g = g
        self.a = a

    def sendX(self):
        X = g ** self.x
        return X

    def sendS(self, c):
        s = self.x + a * c
        return s


class Verifier:

    def __init__(self, g, A):
        self.c = group.random()
        self.g = g
        self.A = A

    def sendC(self, X):
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
prover = Prover(g, a)
verifier = Verifier(g, g ** a)

X = prover.sendX()
c = verifier.sendC(X)
s = prover.sendS(c)

print(verifier.verify(s))


'''
pseudokod
sk = a <-$Zq, pk = A <- g^a
H1 - wyrzuca element z grupy g
H2 = losuje esponent 

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