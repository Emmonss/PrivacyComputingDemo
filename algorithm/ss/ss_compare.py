import random

# 设置随机种子以便复现结果
random.seed(42)

def generate_triple(p):
    """生成Beaver乘法三元组"""
    a = random.randint(0, p-1)
    b = random.randint(0, p-1)
    c = (a * b) % p
    a1 = random.randint(0, p-1)
    a2 = (a - a1) % p
    b1 = random.randint(0, p-1)
    b2 = (b - b1) % p
    c1 = random.randint(0, p-1)
    c2 = (c - c1) % p
    return ((a1, a2), (b1, b2), (c1, c2))

def beaver_multiply(a_shares, b_shares, triple_a, triple_b, triple_c, p):
    """使用Beaver三元组进行安全乘法"""
    a1, a2 = a_shares
    b1, b2 = b_shares
    a_t1, a_t2 = triple_a
    b_t1, b_t2 = triple_b
    c1, c2 = triple_c

    # 计算本地差值
    e1 = (a1 - a_t1) % p
    e2 = (a2 - a_t2) % p
    e = (e1 + e2) % p

    f1 = (b1 - b_t1) % p
    f2 = (b2 - b_t2) % p
    f = (f1 + f2) % p

    # 计算新份额
    z1 = (c1 + e * b_t1 + f * a_t1 + e * f) % p
    z2 = (c2 + e * b_t2 + f * a_t2) % p
    return (z1, z2)


if __name__ == '__main__':

    # 参数配置
    p = 37  # 选用素數17作为模数
    triples = [generate_triple(p) for _ in range(4)]  # 预生成四个三元组

    # 输入数值的秘密分享（示例：x=5, y=5）
    # x1, x2 = 14, 2   # x = 3 + 2 = 5 mod 17
    # y1, y2 = 13, 3  # y = 4 + 1 = 5 mod 17

    x1, x2 = 1, 2   # x = 3 + 2 = 5 mod 17
    y1, y2 = 2, 1 # y = 4 + 1 = 5 mod 17

    # 计算差值d = x - y的分享
    d1 = (x1 - y1) % p
    d2 = (x2 - y2) % p

    # 四步平方计算d^16
    # 1. 计算d^2
    d_squared = beaver_multiply((d1, d2), (d1, d2), *triples[0], p)
    # 2. 计算d^4
    d_4th = beaver_multiply(d_squared, d_squared, *triples[1], p)
    # 3. 计算d^8
    d_8th = beaver_multiply(d_4th, d_4th, *triples[2], p)
    # 4. 计算d^16
    d_16th = beaver_multiply(d_8th, d_8th, *triples[3], p)

    # 计算c = 1 - d^16 (1的分享为(1, 0))
    c1 = (1 - d_16th[0]) % p
    c2 = (0 - d_16th[1]) % p

    # 验证结果
    result = (c1 + c2) % p
    print(f"比较结果分享: c1={c1}, c2={c2}")
    print(f"最终结果（1表示相等，0不等）: {result}")
