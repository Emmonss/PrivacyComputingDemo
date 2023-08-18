import tenseal as ts


if __name__ == '__main__':

    import tenseal as ts
    ctx=ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    ctx.global_scale=2**40

    sk = ctx.secret_key()
    ctx.make_context_public()


    m1 = [1, 2, 3, 4, 5]
    m2 = [6, 7, 8, 9, 10]
    print("m1 is ", m1)
    print("m2 is ", m2)

    c1 = ts.ckks_vector(ctx, m1)
    c2 = ts.ckks_vector(ctx, m2)

    c3 = c1 + c2
    sum = c3.decrypt(sk)
    print("The sum of m1 and m2 is ", sum)

    c4 = c1 * c2
    prod = c4.decrypt(sk)
    print("The product of m1 and m2 is ", prod)