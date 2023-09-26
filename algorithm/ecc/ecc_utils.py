from Crypto.PublicKey import ECC

__all__=[]


SUPPORT_CURVE = ["secp256r1","secp384r1"]
def generate_key(curve="secp256r1"):
    sk = ECC.generate(curve=curve)
    pk = sk.public_key()
    return sk,pk

def key_2_bytes(key:ECC.EccKey):
    if key.has_private():
        raise ValueError("only public key can be serialized to bytes")
    return key.export_key(format="DER",compress=True)

def bytes_2_key(data:bytes) -> ECC.EccKey:
    return ECC.import_key(data)

def point_2_bytes(point:ECC.EccPoint):
    xs = point.x.to_bytes()
    ys = bytes([2+point.y.is_odd()])
    return xs+ys


if __name__ == '__main__':
    s = "fuck".encode("utf-8")

    print('='*100)

    sk1,pk1 = generate_key()
    print(sk1)
    print(pk1)
    print('='*100)

    sk2,pk2 = generate_key()
    print(sk2)
    print(pk2)
    print('=' * 100)

    k1 = pk1.pointQ*sk2.d
    k2 = pk2.pointQ*sk1.d

    print(k1.x,k1.y)
    print(k2.x,k2.y)

    print('='*100)
    print(point_2_bytes(k1))
    print(point_2_bytes(k2))
