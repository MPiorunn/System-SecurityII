from charm.toolbox.integergroup import IntegerGroupQ


class Alice:

    def __init__(self, ak, pk):
        self.pk = pk
        self.ID_a = group.random()
        self.g = pk['g']
        self.a = ak['a']

    def sendX(self):
        self.x = group.random()
        self.X = self.g ** self.x
        return self.X

    def sendData(self, bob_data):
        self.K = bob_data['Y'] ** self.x
        self.K_0 = group.hash(self.K, 0)
        self.K_1 = group.hash(self.K, 1)
        self.mac = group.hash(self.ID_a, self.K_0)
        if self.checkMac(bob_data) and self.verifySig(bob_data):
            self.sig = self.sign(self.g ** self.x, bob_data['Y'])
            self.Ks = self.K_1
            return {'X': self.g ** self.x, 'ID_a': self.ID_a, 'sig': self.sig, 'mac': self.mac}

    def checkMac(self, bob_data):
        mac = group.hash(bob_data['ID_b'], self.K_0)
        return bob_data['mac'] == mac

    def verifySig(self, bob_data):
        sig = bob_data['sig']
        X = sig['X']
        s = sig['s']
        c = group.hash(self.g ** self.x, bob_data['Y'], X)
        return self.g ** s == X * self.pk['B'] ** c

    def sign(self, g_x, g_y):
        x = group.random()
        X = self.g ** x
        c = group.hash(g_x, g_y, X)
        s = x + self.a * c
        return {'s': s, 'X': X}

    def getSessionKey(self):
        return self.Ks


class Bob:

    def __init__(self, bk, pk):
        self.pk = pk
        self.g = pk['g']
        self.b = bk['b']
        self.ID_b = group.random()

    def sendData(self, X):
        self.y = group.random()
        self.K = X ** self.y
        self.K_0 = group.hash(self.K, 0)
        self.K_1 = group.hash(self.K, 1)
        self.mac = group.hash(self.ID_b, self.K_0)
        sig = self.sign(X, self.g ** self.y)
        return {'Y': self.g ** self.y, 'ID_b': self.ID_b, 'sig': sig, 'mac': self.mac}

    def sign(self, g_x, g_y):
        x = group.random()
        X = self.g ** x
        c = group.hash(g_x, g_y, X)
        s = x + self.b * c
        return {'s': s, 'X': X}

    def calculateKey(self, alice_data):
        self.K = alice_data['X'] ** self.y
        self.K_0 = group.hash(self.K, 0)
        self.K_1 = group.hash(self.K, 1)
        if self.checkMac(alice_data) and self.verifySig(alice_data):
            self.Ks = self.K_1

    def checkMac(self, alice_data):
        mac = group.hash(alice_data['ID_a'], self.K_0)
        return alice_data['mac'] == mac

    def verifySig(self, alice_data):
        sig = alice_data['sig']
        X = sig['X']
        s = sig['s']
        c = group.hash(alice_data['X'], self.g ** self.y, X)
        return self.g ** s == X * self.pk['A'] ** c

    def getSessionKey(self):
        return self.Ks


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
bob_data = bob.sendData(X)
alice_data = alice.sendData(bob_data)

bob.calculateKey(alice_data)

print(alice.getSessionKey() == bob.getSessionKey())
