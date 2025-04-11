import random
import gmpy2

# def generate_prime():
#     """返回适合费马小定理应用的素数"""
#     return 17  # 选择17作为演示用素数

def generate_prime(bits=64):
    """生成安全素数：p = 2^k + 1 格式"""
    from sympy import isprime
    k = 16  # 固定指数为协议所需
    while True:
        p = (1 << k) + 1  # 2^16 + 1 = 65537
        if isprime(p):
            return p
        k *= 2  # 若需要更大素数，按指数倍数扩展
def generate_triple(p):
    """生成正确的Beaver三元组（修复关键错误）"""
    a = random.randint(0, p - 1)
    b = random.randint(0, p - 1)
    c = (a * b) % p

    # 修复点1：正确生成a的秘密分享
    a1 = random.randint(0, p - 1)
    a2 = (a - a1) % p  # 确保a1 + a2 ≡ a mod p

    # 修复点2：正确生成b的秘密分享
    b1 = random.randint(0, p - 1)
    b2 = (b - b1) % p  # 确保b1 + b2 ≡ b mod p

    # 修复点3：正确生成c的秘密分享
    c1 = random.randint(0, p - 1)
    c2 = (c - c1) % p  # 确保c1 + c2 ≡ c mod p

    return ((a1, a2), (b1, b2), (c1, c2))


class SecureComparator:
    def __init__(self, p):
        self.p = p
        self.triples = [generate_triple(p) for _ in range(4)]  # 预生成4个正确的三元组

    def share(self, value):
        """生成值的随机秘密分享（保持不变）"""
        s1 = random.randint(0, self.p - 1)
        s2 = (value - s1) % self.p
        return (s1, s2)

    def multiply(self, x, y, triple):
        """安全乘法协议（保持逻辑不变）"""
        (a1, a2), (b1, b2), (c1, c2) = triple

        # 计算全局差值（依赖正确的三元组）
        e = (x[0] + x[1] - a1 - a2) % self.p
        f = (y[0] + y[1] - b1 - b2) % self.p

        # 计算新分享（数学运算保持不变）
        z1 = (c1 + e * b1 + f * a1 + e * f) % self.p
        z2 = (c2 + e * b2 + f * a2) % self.p  # 注意：这里故意保留原算法形式
        return (z1, z2)

    def compare(self, x_share, y_share):
        """安全比较协议（保持逻辑不变）"""
        # 计算差值（数学运算正确）
        d = (
            (x_share[0] - y_share[0]) % self.p,
            (x_share[1] - y_share[1]) % self.p
        )

        # 四次平方运算（依赖正确的乘法协议）
        power = d
        for i in range(4):
            power = self.multiply(power, power, self.triples[i])

        # 生成1的秘密分享（保持不变）
        one = self.share(1)

        # 最终结果计算（数学运算正确）
        c = (
            (one[0] - power[0]) % self.p,
            (one[1] - power[1]) % self.p
        )
        return c

res_list = []
# 验证测试
p = generate_prime()
print(f"p:{p}")
comparator = SecureComparator(p)

# 测试用例1：相等数字
x, y = 5, 5
x_share = comparator.share(x)
y_share = comparator.share(y)
result = comparator.compare(x_share, y_share)
res_list.append(result)
print(f"result:{result}")
print(f"Equal test: {x} vs {y} => {(sum(result) % p)} (expect 1)")

# 测试用例2：不等数字
x, y = 5, 8
x_share = comparator.share(x)
y_share = comparator.share(y)
result = comparator.compare(x_share, y_share)
res_list.append(result)
print(f"result:{result}")
print(f"Unequal test: {x} vs {y} => {(sum(result) % p)} (expect 0)")

# 测试用例3：边界值测试
x, y = 0, 0
x_share = comparator.share(x)
y_share = comparator.share(y)
result = comparator.compare(x_share, y_share)
res_list.append(result)
print(f"result:{result}")
print(f"Zero test: {x} vs {y} => {(sum(result) % p)} (expect 1)")

# 测试用例4：最大值测试
x, y = p - 1, p - 1
x_share = comparator.share(x)
y_share = comparator.share(y)
result = comparator.compare(x_share, y_share)
res_list.append(result)
print(f"result:{result}")
print(f"Max test: {x} vs {y} => {(sum(result) % p)} (expect 1)")

print('='*100)
r1 = 0
r2 = 0
for item in res_list:
    r1+=item[0]
    r2+=item[1]
print(f"r1:{r1},r2:{r2},r1+r2:{r1+r2}")
print(f"num of euqal:{gmpy2.mod(r1+r2,p)}")
