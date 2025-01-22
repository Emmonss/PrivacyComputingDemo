import math

from algorithm.simple.gmpy_math import mpz,mod





if __name__ == '__main__':
    p = 4177
    m = 2174
    k = 30

    j = 15
    x = mpz(k * m + j)
    print(x)
    y_2 = mod((x*x*x + 3*x),p)
    print(y_2)
    print(math.sqrt(y_2))
    print(x/k)
    pass