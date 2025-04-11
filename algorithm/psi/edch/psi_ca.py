from algorithm.ecc.ecc_utils import generate_key,key_2_bytes,bytes_2_key,point_2_bytes,bytes_2_point
from algorithm.base.hash import compute_sha256
from algorithm.simple.gmpy_math import mpz
from pprint import pprint
from Crypto.PublicKey.ECC import EccKey,EccPoint
import numpy as np
import random,copy
curve="ed25519"



def ser_point(data:EccPoint):
    return point_2_bytes(data).hex()

def add_curve(data:str, pk:EccKey):
    hash_data = compute_sha256(data)
    res = mpz(int(hash_data,16)) * pk.pointQ
    return res
    # return point_2_bytes(res).hex()

def add_curve_sk(data:bytes, sk:EccKey):
    # p = bytes_2_point()
    res = data * sk.d
    return res

def add_curve_list(data:list[str], pk:EccKey):
    res = []
    for item in data:
        res.append(add_curve(item, pk))
    return res

if __name__ == '__main__':
    host_data = ['fuck1','fuck2','fuck3']
    guest_data = ['fuck2','fuck3','fuck4']

    print("生成双方的椭圆曲线密钥{host_sk, host_pk}和{guest_sk, guest_pk}")
    host_sk, host_pk = generate_key(curve=curve)
    guest_sk, guest_pk = generate_key(curve=curve)

    print("guest方将数据映射到椭圆曲线上并用guest_pk加密，结果如下".center(100,'='))
    guest_curve_result = add_curve_list(guest_data, guest_pk)
    pprint([ser_point(item) for item in guest_curve_result])
    #
    print("host方将数据映射到椭圆曲线上并用host_pk加密，结果如下".center(100,'='))
    host_curve_result = add_curve_list(host_data, host_pk)
    pprint([ser_point(item) for item in host_curve_result])

    print("guest方将加密数据发送给host方-->>>> 并打乱".center(100,'='))
    guest_curve_host_shuffle = copy.copy(guest_curve_result)
    random.shuffle(guest_curve_host_shuffle)
    pprint([ser_point(item) for item in guest_curve_host_shuffle])
    #
    print("host方将打乱后的数据用自身私钥加密".center(100, '='))
    guest_curve_host_shuffle_enc = [add_curve_sk(item, host_sk) for item in guest_curve_host_shuffle]
    pprint([ser_point(item) for item in guest_curve_host_shuffle_enc])

    print("host将打乱加密后的数据发送给guest方<<<----".center(100, '='))
    print("host方将自己的数据也发给guest方 guest方用guest_sk加密<<<---".center(100, '='))
    host_curve_result_enc = [add_curve_sk(item, guest_sk) for item in host_curve_result]
    pprint([ser_point(item) for item in host_curve_result_enc])


    print("分割线".center(100, '*'))
    print("现在guest方有自身加密且经过host方打乱的数据 和host方发来经过自身sk加密后的数据")
    print("现在guest方有自身加密且经过host方打乱的数据")
    guest_curve_host_shuffle_enchex = [ser_point(item) for item in guest_curve_host_shuffle_enc]
    pprint(guest_curve_host_shuffle_enchex)
    print("host方发来经过自身sk加密后的数据")
    host_curve_result_enc_hex = [ser_point(item) for item in host_curve_result_enc]
    pprint(host_curve_result_enc_hex)

    print("计数".center(50, '*'))
    count = 0
    for item in guest_curve_host_shuffle_enchex:
        if item in host_curve_result_enc_hex:
            count+=1
    print(f"交集个数：{count}")
    print("guest把交集个数发送给host方---->>>>>（不发也成 看场景） 算法交互结束")
    #
    # #
    # #intersection
    # print('host intersection'.center(100, '='))
    # print(f"guest_curve_list:{guest_curve_list}")
    # host_intersection = []
    # for item in guest_curve_list:
    #     if item in host_curve_result:
    #         host_intersection.append(host_curve_result[item])
    # print(f"host intersection result:{host_intersection}")
    # #
    # print('guest intersection'.center(100, '='))
    # print(f"host_curve_list:{host_curve_list}")
    # guest_intersection = []
    # for item in host_curve_list:
    #     if item in guest_curve_result:
    #         guest_intersection.append(guest_curve_result[item])
    # print(f"guest intersection result:{guest_intersection}")
    #




    pass