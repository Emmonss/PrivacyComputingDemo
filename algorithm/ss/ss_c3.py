import random


class SecureComparator:
    def __init__(self, prime=17):
        self.p = prime
        self.bit_length = 4
        self.triples = self._generate_valid_triples(4)  # 关键修复点

    def _generate_valid_triples(self, count):
        """正确生成满足c=ab的三元组"""
        triples = []
        for _ in range(count):
            # 生成随机明文a,b
            a = random.randint(0, self.p - 1)
            b = random.randint(0, self.p - 1)
            c = (a * b) % self.p

            # 生成a的加法分享
            a0 = random.randint(0, self.p - 1)
            a1 = (a - a0) % self.p

            # 生成b的加法分享
            b0 = random.randint(0, self.p - 1)
            b1 = (b - b0) % self.p

            # 生成c的加法分享
            c0 = random.randint(0, self.p - 1)
            c1 = (c - c0) % self.p

            triples.append(([a0, a1], [b0, b1], [c0, c1]))
        return triples

    def share(self, value):
        """生成正确的加法秘密分享"""
        share_p0 = random.randint(0, self.p - 1)
        share_p1 = (value - share_p0) % self.p
        return [share_p0, share_p1]

    def add(self, shares_x, shares_y):
        """保持模运算的加法"""
        return [(x + y) % self.p for x, y in zip(shares_x, shares_y)]

    def multiply(self, shares_x, shares_y, triple):
        """修复后的正确乘法协议"""
        a_shares, b_shares, c_shares = triple

        # 计算ε = x - a 和 δ = y - b 的本地部分
        epsilon_0 = (shares_x[0] - a_shares[0]) % self.p
        epsilon_1 = (shares_x[1] - a_shares[1]) % self.p
        delta_0 = (shares_y[0] - b_shares[0]) % self.p
        delta_1 = (shares_y[1] - b_shares[1]) % self.p

        # 公开值（模拟网络交换）
        epsilon = (epsilon_0 + epsilon_1) % self.p
        delta = (delta_0 + delta_1) % self.p

        # 正确计算结果分享
        z0 = (c_shares[0] + epsilon * b_shares[0] + delta * a_shares[0] + epsilon * delta) % self.p
        z1 = (c_shares[1] + epsilon * b_shares[1] + delta * a_shares[1]) % self.p
        return [z0, z1]

    def power_16(self, shares_d):
        """正确的幂次计算"""
        current = shares_d
        for i in range(4):
            current = self.multiply(current, current, self.triples[i])
        return current

    def compare(self, shares_x, shares_y):
        """修复后的比较协议"""
        # 计算安全差值
        shares_neg_y = [(-y) % self.p for y in shares_y]
        shares_d = self.add(shares_x, shares_neg_y)

        # 计算d^16
        shares_d_pow = self.power_16(shares_d)

        # 计算1 - d^16
        shares_one = self.share(1)
        shares_res = self.add(shares_one, [(-s) % self.p for s in shares_d_pow])
        return shares_res


def demo():
    print("===== 修复后的安全比较协议演示 =====")
    sc = SecureComparator()

    # 测试相等情况
    x, y = 7, 7
    print(f"\n案例1：{x} == {y}")
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    print(f"x分享（和={sum(shares_x) % sc.p}）: {shares_x}")
    print(f"y分享（和={sum(shares_y) % sc.p}）: {shares_y}")

    result = sc.compare(shares_x, shares_y)
    reconstructed = (result[0] + result[1]) % sc.p
    print(f"比较结果：{reconstructed}（1表示相等）")

    # 测试不等情况
    x, y = 5, 9
    print(f"\n案例2：{x} != {y}")
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    reconstructed = (result[0] + result[1]) % sc.p
    print(f"比较结果：{reconstructed}（0表示不等）")


if __name__ == "__main__":
    demo()
