
from algorithm.ecc.ecc_utils import generate_key
from algorithm.base.hash import compute_sha256
from algorithm.simple.gmpy_math import mpz,get_random_big_num


# def


if __name__ == '__main__':
    y = 'fucker test'
    s = mpz(int(compute_sha256(y), 16))
    print(f"y:{s}")
    r_len = 64
    #host
    sk, pk = generate_key()
    print(f"key:{sk.d}")

    # print(sk.pointQ.xy)
    # print(pk.pointQ.xy)
    y_point = s * pk.pointQ
    print(f"f(y)=:{y_point.x + y_point.y}")

    pass