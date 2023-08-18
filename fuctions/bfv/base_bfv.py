from tenseal import context,SCHEME_TYPE,bfv_vector
from tenseal.tensors.bfvvector import BFVVector
from tenseal.enc_context import Context
from tenseal.enc_context import SecretKey
import numpy as np


def get_pair_key(poly_modulus_degree=4096,
                 plain_modulus=1032193,
                 gen_galois_keys=True):
    pk = context(SCHEME_TYPE.BFV,
                    poly_modulus_degree=poly_modulus_degree,
                    plain_modulus=plain_modulus)
    sk = pk.secret_key()
    pk.make_context_public(generate_galois_keys=gen_galois_keys)
    return sk, pk

def encrypt(pk:Context,s):
    return bfv_vector(pk, s)

def decrypt(sk:SecretKey,m:BFVVector):
    return m.decrypt(sk)

def mul(m1,m2):
    if not (isinstance(m1,BFVVector) or isinstance(m2,BFVVector)):
        return np.array(list(m1))*np.array(list(m2))
    return m1 * m2

def add(m1,m2):
    if not (isinstance(m1,BFVVector) or isinstance(m2,BFVVector)):
        return np.array(list(m1)) + np.array(list(m2))
    return m1+m2

def sub(m1,m2):
    if not (isinstance(m1,BFVVector) or isinstance(m2,BFVVector)):
        return np.array(list(m1)) - np.array(list(m2))
    return m1-m2

def dot(m1:BFVVector,m2,pk:Context):
    assert pk.has_galois_keys(),ValueError("pub key need galois key to do dot opration")
    return m1.dot(m2)

def sum(m1:BFVVector,pk:Context,axis=0):
    assert pk.has_galois_keys(), ValueError("pub key need galois key to do dot opration")
    return m1.sum(axis)



def bfv_vector_serialize(m1:BFVVector):
    return m1.serialize()

def from_serialize_bfv_vector(m1:bytes,pk:Context):
    return BFVVector.load(pk,m1)

def pubkey_serialize(pk:Context,save_galois_keys=True):
    return pk.serialize(save_galois_keys=save_galois_keys)

def from_serialize_pubkey(pks1:bytes):
    return Context.load(data=pks1)


if __name__ == '__main__':
    gen_galois_keys = True
    poly_modulus_degree = 4096
    plain_modulus = 1032193

    sk1, pk1 = get_pair_key(poly_modulus_degree,plain_modulus,gen_galois_keys)
    sk2, pk2 = get_pair_key(poly_modulus_degree,plain_modulus,gen_galois_keys)
    m1 = [1, 2, 3, 4, 5]
    m2 = [6, 7, 8, 9, 10]
    m3 = [1]*len(m1)
    # print(m3)



    pks1 = pubkey_serialize(pk1)
    print(type(pks1))
    pk1 = from_serialize_pubkey(pks1)
    print(pk1)
    print(type(pk1))

    c1 = encrypt(pk1, m1)
    c2 = encrypt(pk1, m2)
    c3 = encrypt(pk1, m3)

    c1 = c1.serialize()
    print(type(c1))
    c1 = from_serialize_bfv_vector(c1,pk1)
    print(c1)
    c1 = mul(c1,2)
    print(c1.decrypt(sk1))