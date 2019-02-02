from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair
from charm.core.engine.util import objectToBytes
from charm.toolbox.IBSig import *


class BLS(IBSig):
    def __init__(self, groupObj):
        IBSig.__init__(self)
        global group
        group = groupObj

    def dump(self, obj):
        return objectToBytes(obj, group)

    def keygen(self):
        g, x = group.random(G2), group.random()
        g_x = g ** x
        pk = {'g^x': g_x, 'g': g, 'identity': str(g_x)}
        sk = {'x': x}
        return pk, sk

    def sign(self, x, message):
        m = self.dump(message)
        return group.hash(m, G1) ** x

    def verify(self, pk, sig, message):
        m = self.dump(message)
        h = group.hash(m, G1)
        return pair(sig, pk['g']) == pair(h, pk['g^x'])


group_obj = PairingGroup('MNT224')
m = "This is my secret message"
bls = BLS(group_obj)
(pk, sk) = bls.keygen()
sig = bls.sign(sk['x'], m)
ver = bls.verify(pk, sig, m)
if ver:
    print("Verified")
else:
    print("Not verified")
