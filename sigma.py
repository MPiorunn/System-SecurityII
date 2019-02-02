from charm.toolbox.integergroup import IntegerGroupQ


class Alice:

    def __init__(self, ak):
        self.ID_a = group.random()
        self.g = ak['g']
        self.a = ak['a']

    def sendX(self):
        self.x = group.random()
        self.X = self.g ** self.x
        return self.X

    # def sendData(self, bob_data):
    #     self.K = bob_data['Y'] ** self.x
    #     self.K_0 = group.hash(self.K, 0)
    #     self.K_1 = group.hash(self.K, 1)
    #     self.mac = group.hash(self.ID_a, self.K_0)
    #     if self.checkMac(bob_data):  # and self.verifySig(bob_data):
    #         self.sig = self.sign(bob_data, self.g ** self.x)
    # self.Ks = self.K_1
    # return {'X': self.g ** self.x, 'ID_a': self.ID_a, 'sig': "XD", 'mac': self.mac}

    # def sign(self, g_x, g_y):
    #     X = self.g ** self.x
    #     c = group.hash(g_x, g_y, X)
    #     s = self.x + self.a * c
    #     return {'s': s, 'X': X}

    # def checkMac(self, bob_data):
    #     mac = group.hash(bob_data['ID_b'], self.K_0)
    #     return self.mac == mac

    # def verifySig(self, bob_data):
    #     sig = bob_data['sig']
    #     X = sig['X']
    #     s = sig['s']
    #     c = group.hash(self.g ** self.x, bob_data['Y'])
    #     return self.g ** s == X * (self.g ** self.a) ** c


class Bob:

    def __init__(self, bk):
        self.ID_b = group.random()
        self.g = bk['g']
        self.b = bk['b']

    def sendData(self, X):
        self.y = group.random()
        self.K = X ** self.y
        self.K_0 = group.hash(self.K, 0)
        self.K_1 = group.hash(self.K, 1)
        self.mac = group.hash(self.ID_b, self.K_0)
        # sig = self.sign(X, self.g ** self.y)
        return {'Y': self.g ** self.y, 'ID_b': self.ID_b, 'sig': "xD", 'mac': self.mac}

    # def sign(self, g_x, g_y):
    #     X = self.g ** self.y
    #     c = group.hash(g_x, g_y, X)
    #     s = self.y + self.b * c
    #     return {'s': s, 'X': X}

    # def calculateKey(self, alice_data):
    #     self.K = alice_data['X'] ** self.y
    #     self.K_0 = group.hash(self.K, 0)
    #     self.K_1 = group.hash(self.K, 1)
    # if self.checkMac(alice_data):#and self.verifySig(alice_data):
    # self.Ks = self.K1

    # def checkMac(self, alice_data):
    #     mac = group.hash(alice_data['ID_b'], self.K_0)
    #     return self.mac == mac


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

alice = Alice(a_k)
bob = Bob(b_k)

X = alice.sendX()
bob_data = bob.sendData(X)
# alice_data = alice.sendData(bob_data)
#
# bob.calculateKey(alice_data)
