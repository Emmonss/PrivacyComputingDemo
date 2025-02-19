import gmpy2
from Crypto.PublicKey import ECC
from algorithm.base.hash import compute_sha256
from algorithm.simple.gmpy_math import mpz,is_prime
__all__=[]


SUPPORT_CURVE = ["secp256r1","secp384r1","ed25519"]
def generate_key(curve="ed25519"):
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

def point_2_bytes2(point:ECC.EccPoint):
    # print(type(point.x))
    # print(mpz(point.x))
    xs = mpz(point.x).digits(16).encode('utf-8')
    ys = mpz(point.y).digits(16).encode('utf-8')
    return xs,ys

def bytes_2_point(x,y,curve="ed25519"):
    x = gmpy2.mpz(x, 16)
    y = gmpy2.mpz(y, 16)
    return ECC.EccPoint(x,y,curve=curve)


if __name__ == '__main__':
    s = "fuck"
    # print(compute_sha256(s))
    s = mpz(int(compute_sha256(s),16))
    # print(s)


    sk1, pk1 = generate_key()

    sk2, pk2 = generate_key()

    # print(pk1.pointQ.xy)
    # print(pk2.pointQ.xy)
    #
    # p3 = pk1.pointQ + pk2.pointQ
    # print(p3.xy)
    #
    # p4 = -pk2.pointQ
    # print(p4.xy)
    # p5 = p3+p4
    # print(p5.xy)

    k1 = s * pk1.pointQ*sk2.d
    k2 = s * pk2.pointQ*sk1.d

    print(k1.xy)
    xs,ys = point_2_bytes2(k1)
    print(xs,ys)
    k11 = bytes_2_point(xs,ys)
    print(k11.xy)

    # print(point_2_bytes(k2))
    # print(k1.x, k1.y)
    # print(k1.x.to_bytes(),k1.y.to_bytes())
    # print(k2.x.to_bytes(),k2.y.to_bytes())



