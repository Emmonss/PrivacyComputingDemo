

from tenseal import context,SCHEME_TYPE,bfv_vector
from tenseal.tensors.bfvvector import BFVVector
from tenseal.enc_context import Context
from tenseal.enc_context import SecretKey


if __name__ == '__main__':

    ctx = context(SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)
    if ctx.is_private():
        print("This context is private!")
    if ctx.is_public():
        print("This context is public!")

    sk = ctx.secret_key()

    ctx.make_context_public()
    if ctx.is_private():
        print("This context is private!")
    if ctx.is_public():
        print("This context is public!")
    print(type(sk))
    m1 = [1, 2, 3, 4, 5]
    m2 = [5, 4, 3, 2, 1]

    c1 = bfv_vector(ctx, m1)
    c2 = bfv_vector(ctx, m2)
    print(isinstance(c1,BFVVector))
    #
    # print("c1 is ", c1.serialize())
    # print("c2 is ", c2.serialize())
    # print(type(sk))
    print("m1 is ", c1.decrypt(sk))
    print("m2 is ", c2.decrypt(sk))

    # homomorphic addition
    c3 = c1 + c2
    print("The sum is ", c3.decrypt(sk))

    # homomorphic scale
    c4 = 2 * c1
    print("2 times of m1 is ", c4.decrypt(sk))

    # homomorphic multiplication
    c5 = c1 * c2
    print("The product is ", c5.decrypt(sk))
