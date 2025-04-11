from algorithm.simple.gmpy_math import mpz,get_random_big_num
import random,numpy as np
from algorithm.pailler.crt_paillier import PaillierKeyPair


def scale(num,old_min,old_max,min,max):
    res = []
    for item in num:
        res.append(((item-old_min) / (old_max-old_min)) * (max-min) + min)
    return res

def unscale(num,old_min,old_max,min,max):
    res = []
    for item in num:
        res.append(mpz((item-min) * (old_max - old_min) / (max - min) + old_min))
    return res


if __name__ == '__main__':
    min = 0
    max = 1000000000000000000
    big = 5
    pk, sk = PaillierKeyPair.generate_keypair(n_length=1024)

    init_data = [np.round(random.uniform(0,1.0) ,2)for _ in range(big)]
    print(f"加密前的数据:{init_data}")
    enc_data = [pk.encrypt(item) for item in init_data]
    enc_cipher = [item.ciphertext(False) for item in enc_data]
    # enc_cipher = [random.randint(1000,10000) for i in range(big)]
    enc_exp = [item.exponent for item in enc_data]
    print(f"加密后的的数据:{enc_cipher}")
    old_min = np.min(enc_cipher)
    old_max = np.max(enc_cipher)
    enc_cipher_scale = scale(enc_cipher,old_min,old_max,min,max)
    print(f"加密后的的数据缩放到({min},{max}):{enc_cipher_scale}")
    enc_cipher_back = unscale(enc_cipher_scale,old_min,old_max,min,max)
    print(f"还原数据:{enc_cipher_back}")


