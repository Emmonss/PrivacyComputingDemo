import random
import gmpy2


'''
    basic fuctions
'''
def mpz(a):
    return gmpy2.mpz(a)

def mul(a,b):
    return gmpy2.mul(a,b)

def div(a,b):
    return gmpy2.div(a,b)

def add(a,b):
    return gmpy2.add(a,b)

def sub(a,b):
    return gmpy2.sub(a,b)

def mod(a,n):
    return gmpy2.mod(a,n)

def powmod(a,b,n):
    return gmpy2.powmod(a,b,n)

def gcd(a,b):
    return int(gmpy2.gcd(a,b))


'''
    prime fuctions
'''


def invert(a,b):
    '''
        return int x where a*x ==1 mod b
    '''
    x = int(gmpy2.invert(a,b))
    assert x != 0, ZeroDivisionError('invert not inverse exists')

    return x

def crt_coefficient(p,q):
    tq = gmpy2.invert(p,q)
    tp = gmpy2.invert(q,p)
    return tp*q, tq*p

def powmod_crt(x,d,n,p,q,cp,cq):
    rp = gmpy2.powmod(x, d % (p - 1), p)
    rq = gmpy2.powmod(x, d % (q - 1), q)
    res = mod(add(mul(rp, cp), mul(rq, cq)), n)
    return int(res)

def get_random_big_num(n):
    return gmpy2.mpz(random.SystemRandom().getrandbits(n))

def ger_prime_over(n):
    r = get_random_big_num(n)
    r = gmpy2.bit_set(r,n-1)
    return next_prime(r)

def next_prime(n):
    return int(gmpy2.next_prime(n))

def get_safe_prime(n):
    while 1:
        p = ger_prime_over(n)
        p = 2*p+1
        if is_prime(p):
            return p


def get_generation_for_safe_prime(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p-1)//p
    while 1:
        g = random.randint(2,p-1)
        if powmod(g,(p-1)//p1,p) !=1 and powmod(g,(p-1)//p2,p) !=1:
            return g
'''
    bool fuctions
'''
def is_prime(p):
    return gmpy2.is_prime(p)

def is_qrt(n):
    return int(gmpy2.isqrt(n))

def legendre(a,p):
    return powmod(a,(p-1)//2,p)

def get_rand_state(p):
    return gmpy2.random_state(hash(p))
