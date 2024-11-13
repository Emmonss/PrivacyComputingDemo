"""
@Time : 2024/4/21 18:19
@Auth ： yeqc
"""

import random
from decimal import Decimal

FIELD_SIZE = 10 ** 2
MOD = 9999999987


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
    sums = 0

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                # print(Decimal(Decimal(xi) / (xi - xj)))
                prod *= Decimal(Decimal(xi) / (xi - xj))
        # print(yj)
        prod *= yj
        sums += Decimal(prod)
    print(sums)

    return int(round(Decimal(sums), 0))


def multiply_shares(shares1, shares2):
    """
    将两组秘密份额相乘，得到新的秘密份额
    """
    multiplied_shares = []
    for (x1, y1), (x2, y2) in zip(shares1, shares2):
        if x1 != x2:
            raise ValueError("Shares must have the same x value.")
        multiplied_shares.append((x1, (y1 * y2) % MOD))
    return multiplied_shares


# Driver code
if __name__ == '__main__':
    # (3,5) sharing scheme
    t, n = 3, 5
    secret1 = 10
    secret2 = 111

    # 设置相同tuple(x,y)中的x
    x = random.sample(range(0, FIELD_SIZE), n)
    # 秘密共享
    shares1 = generate_shares(n, t, secret1, x)
    shares2 = generate_shares(n, t, secret2, x)

    print("Shares for Secret1:", shares1)
    print("Shares for Secret2:", shares2)

    # 秘密份额相乘
    multiplied_shares = multiply_shares(shares1, shares2)
    print("Multiplied Shares:", multiplied_shares)

    # 秘密份额相乘实现秘密相乘
    reconstructed_secret = reconstruct_secret(multiplied_shares)
    print("Reconstructed Secret:", reconstructed_secret)