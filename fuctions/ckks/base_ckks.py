from tenseal import context,SCHEME_TYPE
from tenseal import ckks_vector
from tenseal.enc_context import Context
from tenseal.enc_context import SecretKey
from tenseal.tensors.ckksvector import CKKSVector
import numpy as np

def get_pair_key(poly_modulus_degree=8192,
                 coeff_mod_bit_sizes=[60, 40, 40, 60],
                 gen_galois_keys=True,
                 global_scale=40):
    pk = context(SCHEME_TYPE.CKKS,
                    poly_modulus_degree=poly_modulus_degree,
                    coeff_mod_bit_sizes=coeff_mod_bit_sizes)
    pk.global_scale = 2 ** global_scale

    sk = pk.secret_key()
    pk.make_context_public(generate_galois_keys=gen_galois_keys)
    return sk, pk


def encrypt(pk:Context,s):
    return ckks_vector(pk, s)

def decrypt(sk:SecretKey,m:CKKSVector):
    return m.decrypt(sk)

def mul(m1,m2):
    if not (isinstance(m1,CKKSVector) or isinstance(m2,CKKSVector)):
        return np.array(list(m1))*np.array(list(m2))
    return m1 * m2

def add(m1,m2):
    if not (isinstance(m1,CKKSVector) or isinstance(m2,CKKSVector)):
        return np.array(list(m1)) + np.array(list(m2))
    return m1+m2

def sub(m1,m2):
    if not (isinstance(m1,CKKSVector) or isinstance(m2,CKKSVector)):
        return np.array(list(m1)) - np.array(list(m2))
    return m1-m2

def matmul(m1:CKKSVector,m2,pk:Context):
    assert pk.has_galois_keys(),ValueError("pub key need galois key to do dot opration")
    return m1.matmul(m2)

def sum(m1:CKKSVector,pk:Context,axis=0):
    assert pk.has_galois_keys(), ValueError("pub key need galois key to do dot opration")
    return m1.sum(axis)

def dot(m1:CKKSVector,m2,pk:Context):
    assert pk.has_galois_keys(),ValueError("pub key need galois key to do dot opration")
    return m1.dot(m2)

def pow(m1:CKKSVector,m2:int):
    return m1.pow(m2)

def ckks_vector_serialize(m1:CKKSVector):
    return m1.serialize()

def from_serialize_ckks_vector(m1:bytes,pk:Context):
    return CKKSVector.load(pk,m1)

def pubkey_serialize(pk:Context,save_galois_keys=True):
    return pk.serialize(save_galois_keys=save_galois_keys)

def from_serialize_pubkey(pks1:bytes):
    return Context.load(data=pks1)


if __name__ == '__main__':
    from pprint import pprint

    poly_modulus_degree = 8192
    coeff_mod_bit_sizes = [60, 40, 40, 60]
    gen_galois_keys = False
    global_scale = 40

    sk, pk = get_pair_key(poly_modulus_degree = poly_modulus_degree,
                            coeff_mod_bit_sizes = coeff_mod_bit_sizes,
                            gen_galois_keys = gen_galois_keys,
                            global_scale = 40)


    pks = pubkey_serialize(pk)
    print("{}:{}".format(type(pks),len(pks)))
    pk = from_serialize_pubkey(pks)
    print(type(pk))


    m1 = [1, 2, 3, 4, 5]
    m2 = [6, 7, 8, 9, 10]
    m3 = [1] * len(m1)


    c1 = encrypt(pk, m1)
    c2 = encrypt(pk, m2)
    c3 = encrypt(pk, m3)

    c1 = ckks_vector_serialize(c1)
    print("{}:{}".format(type(c1), len(c1)))
    c1 = from_serialize_ckks_vector(c1,pk)
    print(c1.decrypt(sk))

    print((c1*c2).decrypt(sk))





