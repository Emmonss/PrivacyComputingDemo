

import random
from decimal import Decimal
from algorithm.simple.gmpy_math import *




def coeff(t, secret):
    """
    生成最高次为t - 1次的多项式，其中常数项是secret
    """
    # 保证第一项不为0
    coeff = [random.randrange(1, FIELD_SIZE)]
    # 后面t - 2系数项可为0
    if t > 3:
        coeff += [random.randrange(0, FIELD_SIZE) for _ in range(t - 2)]
    # 加入常数项
    coeff.append(secret)
    return coeff


def polynom(x, coefficients):
    """
    获取f(x)的值
    """
    point = 0
    # coeff从左到右是高次到低次的(使用enumerate表示指数)
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def generate_shares(n, m, secret, x):
    """
    将秘密分成n份，只需要m份就可以复原（也就是阈值，函数的最高次数 + 1）
    """
    coefficient = coeff(m, secret)
    shares = []
    for i in range(1, n + 1):
        xx = x[i - 1]
        shares.append((xx, polynom(xx, coefficient)))

    return shares


def reconstruct_secret(shares):
    """
    利用拉格朗日插值法（已知m个秘密)还原并得到secret(f(0))
    """
    sums = mpz(0)

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = mpz(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod = mul(prod, div(xi, sub(xi,xj)))
        prod = mul(prod,yj)
        sums = add(sums,prod)

    return int(round(sums, 0))


def multiply_shares(shares1, shares2):
    """
    将两组秘密份额相乘，得到新的秘密份额
    """
    multiplied_shares = []
    for (x1, y1), (x2, y2) in zip(shares1, shares2):
        if x1 != x2:
            raise ValueError("Shares must have the same x value.")
        multiplied_shares.append((x1, mod(mul(y1,y2) ,MOD)))
    return multiplied_shares


def ss_shamir_mul(host_data_share,guest_data_share):
    host_data_share_0, host_data_share_1 = host_data_share[:t // 2], host_data_share[t //2: t]
    guest_data_0, guest_data_1 = guest_data_share[:t // 2], guest_data_share[t // 2: t]

    print("host_data_share_0", host_data_share_0)
    print("host_data_share_1", host_data_share_1)

    print("guest_data_0", guest_data_0)
    print("guest_data_1", guest_data_1)


if __name__ == '__main__':
    FIELD_SIZE = 20
    import gmpy2

    # MOD = 9999999987
    MOD = get_safe_prime(512)
    print(f"mod{MOD}")

    #
    p_len = 64
    d_len = 13
    t = 8
    n = 16

    # FIELD_SIZE = 10 ** 2


    host_data = get_random_big_num(d_len)
    guest_data = get_random_big_num(d_len)

    # host_data = 10
    # guest_data = 111
    print("host_data:{}".format(host_data))
    print("guest_data:{}".format(guest_data))
    print("host_data+guest_data:{}".format(add(host_data, guest_data)))
    print("host_data*guest_data:{}".format(mul(host_data, guest_data)))

    # x 是共享的
    x = random.sample(range(0, FIELD_SIZE), n)
    print("x:{}".format(x))


    print("make share".center(100, '='))
    # 秘密共享
    host_data_share = generate_shares(n, t, host_data, x)
    guest_data_share = generate_shares(n, t, guest_data, x)
    print("host_data_share:{}".format(host_data_share))
    print("guest_data_share:{}".format(guest_data_share))

    host1 = reconstruct_secret(host_data_share)
    print("host_data_share all:", host1)
    guest1 = reconstruct_secret(guest_data_share)
    print("host_data_share all :", guest1)

    host1 = reconstruct_secret(host_data_share[:t])
    print("host_data_share t:", host1)
    guest1 = reconstruct_secret(guest_data_share[:t])
    print("host_data_share t:", guest1)

    host1 = reconstruct_secret(host_data_share[:t-2])
    print("host_data_share t-1:", host1)
    guest1 = reconstruct_secret(guest_data_share[:t-2])
    print("host_data_share t-1:", guest1)
    #
    # print("mul".center(100, '='))
    # ss_shamir_mul(host_data_share, guest_data_share)

    #
    # # print("Shares for Secret1:", host_data_share)
    # # print("Shares for Secret2:", guest_data_share)
    # # #
    # # # 秘密份额相乘
    multiplied_shares = multiply_shares(host_data_share, guest_data_share)
    print("Multiplied Shares:", multiplied_shares)

    # # 秘密份额相乘实现秘密相乘
    reconstructed_secret = reconstruct_secret(multiplied_shares)
    print("Reconstructed Secret:", reconstructed_secret)
    reconstructed_secret = reconstruct_secret(multiplied_shares[:t])
    print("Reconstructed Secret:", reconstructed_secret)
    reconstructed_secret = reconstruct_secret(multiplied_shares[:t//2])
    print("Reconstructed Secret:", reconstructed_secret)

