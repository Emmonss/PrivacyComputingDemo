import random
import gmpy2

class SecureComparator:
    def __init__(self):
        # 使用经过验证的64位素数
        self.p = 18446744073709551557  # 2^64 - 59
        self.triples = self._generate_valid_triples(4)

    def share(self, value):
        """加法秘密分享函数"""
        share_p0 = random.randint(0, self.p - 1)
        share_p1 = (value - share_p0) % self.p
        return [share_p0, share_p1]

    def add(self, shares_x, shares_y):
        """加法同态操作"""
        return [(x + y) % self.p for x, y in zip(shares_x, shares_y)]

    def _generate_valid_triples(self, count):
        """生成乘法三元组"""
        triples = []
        for _ in range(count):
            a = random.randint(0, self.p - 1)
            b = random.randint(0, self.p - 1)
            c = (a * b) % self.p
            triples.append((
                self.share(a),
                self.share(b),
                self.share(c)
            ))
        return triples

    def _validate_non_zero(self, d):
        """基于费马小定理的零值验证"""
        return pow(d, self.p - 1, self.p) == 0

    def compare(self, shares_x, shares_y):
        """完整的安全比较协议"""
        # 计算差值 d = x - y
        shares_neg_y = [(-y) % self.p for y in shares_y]
        shares_d = self.add(shares_x, shares_neg_y)

        # 重构差值（模拟安全计算）
        d = (shares_d[0] + shares_d[1]) % self.p

        # 判断差值是否为0
        is_zero = self._validate_non_zero(d)
        return self.share(1) if is_zero else self.share(0)


def demo():
    print("===== 完整协议演示 =====")
    sc = SecureComparator()
    res_list = []

    # 测试相等情况
    x = y = 18446744073709551556  # p-1
    shares_x = sc.share(x)
    print(shares_x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    res_list.append(result)
    print(f"result:{result}")
    print(f"相等测试: {sum(result) % sc.p} (预期1)")

    # 测试不等情况
    x, y = 123456789, 987654321
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    res_list.append(result)
    print(f"result:{result}")
    print(f"不等测试: {sum(result) % sc.p} (预期0)")

    # 测试3
    x, y = 123, 123
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    res_list.append(result)
    print(f"result:{result}")
    print(f"测试3: {sum(result) % sc.p} (预期1)")


    # 测试4
    x, y = 123456, 123456
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    res_list.append(result)
    print(f"result:{result}")
    print(f"测试4: {sum(result) % sc.p} (预期1)")

    # 测试5
    x, y = 123456, 654321
    shares_x = sc.share(x)
    shares_y = sc.share(y)
    result = sc.compare(shares_x, shares_y)
    res_list.append(result)
    print(f"result:{result}")
    print(f"测试5: {sum(result) % sc.p} (预期0)")

    print('=' * 100)

    r1 = 0
    r2 = 0
    for item in res_list:
        r1 += item[0]
        r2 += item[1]
    print(f"r1:{r1},r2:{r2},r1+r2:{r1 + r2}")
    print(f"num of euqal:{gmpy2.mod(r1 + r2, sc.p)}")


if __name__ == "__main__":
    demo()
