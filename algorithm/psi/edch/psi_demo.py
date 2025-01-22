from algorithm.ecc.ecc_utils import generate_key,key_2_bytes,bytes_2_key,point_2_bytes
from algorithm.base.hash import compute_sha256
from algorithm.simple.gmpy_math import mpz
from pprint import pprint
from gmpy2 import gmpy2
from Crypto.PublicKey.ECC import EccKey
curve="ed25519"



def add_curve(data:str, pk:EccKey, sk:EccKey):
    hash_data = compute_sha256(data)
    res = mpz(int(hash_data,16)) * pk.pointQ *sk.d
    return point_2_bytes(res).hex()


def add_curve_list(data:list[str], pk:EccKey, sk:EccKey):
    res = dict()
    for item in data:
        res[add_curve(item, pk, sk)] = item
    return res
    pass

if __name__ == '__main__':
    host_data = ['fuck1','fuck2','fuck3']
    guest_data = ['fuck2','fuck3','fuck4']

    host_sk, host_pk = generate_key(curve=curve)
    guest_sk, guest_pk = generate_key(curve=curve)

    print('guest compute'.center(100,'='))
    guest_curve_result = add_curve_list(guest_data, host_pk, guest_sk)
    guest_curve_list = guest_curve_result.keys()
    pprint(guest_curve_result)

    print('host compute'.center(100, '='))
    host_curve_result = add_curve_list(host_data, host_pk, guest_sk)
    host_curve_list = host_curve_result.keys()
    pprint(host_curve_result)


    #intersection
    print('host intersection'.center(100, '='))
    print(f"guest_curve_list:{guest_curve_list}")
    host_intersection = []
    for item in guest_curve_list:
        if item in host_curve_result:
            host_intersection.append(host_curve_result[item])
    print(f"host intersection result:{host_intersection}")

    print('guest intersection'.center(100, '='))
    print(f"host_curve_list:{host_curve_list}")
    guest_intersection = []
    for item in host_curve_list:
        if item in guest_curve_result:
            guest_intersection.append(guest_curve_result[item])
    print(f"guest intersection result:{guest_intersection}")





    pass