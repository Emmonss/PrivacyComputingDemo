from algorithm.simple.gmpy_math import *
import random
from algorithm.base.fixedpoint import FixedPointNumber



class PaillierKeyPair(object):
    def __init__(self):
        pass
    @staticmethod
    def generate_keypair(n_length=1024):

        p=q=n=None
        n_len = 0

        while n_len != n_length:
            p = ger_prime_over(n_length // 2)
            q = p
            while q == p:
                q = ger_prime_over(n_length // 2)
            n = p*q
            n_len = n.bit_length()
        public_key = PaillierPublicKey(n)
        private_key = PaillierPrivateKey(public_key,p,q)
        return public_key,private_key


class PaillierPublicKey(object):
    def __init__(self,n):
        self.g = n+1
        self.n = n
        self.nsquare = n*n
        self.max_int = n // 3 - 1

    def apply_obfuscator(self,ciphertext,random_value = None):
        r = random_value or random.SystemRandom().randrange(1,self.n)
        obfuscator = powmod(r,self.n,self.nsquare)
        return int((ciphertext * obfuscator) % self.nsquare)

    def raw_encrypt(self, plaintext, random_value=None):

        if not isinstance(plaintext,int):
            raise ValueError("plaintext should be int")

        if plaintext >= (self.n - self.max_int) and plaintext < self.n:
            neg_plaintext = self.n - plaintext
            neg_ciphertext = (self.n * neg_plaintext+1)% self.nsquare
            ciphertext = invert(neg_ciphertext,self.nsquare)
        else:
            ciphertext = (self.n * plaintext +1) % self.nsquare

        ciphertext = self.apply_obfuscator(ciphertext,random_value)
        return ciphertext

    def encrypt(self,value, precision=None, random_value = None):
        if isinstance(value,FixedPointNumber):
            value = value.decode()
        encoding = FixedPointNumber.encode(value,self.n, self.max_int,precision)
        obfuscator = random_value or 1
        ciphertext = self.raw_encrypt(encoding.encoding, random_value=obfuscator)
        encryptednumber = PaillierEncryptNumber(self,ciphertext,encoding.exponent)
        if random_value is None:
            encryptednumber.apply_obfuscator()
        return  encryptednumber


    def __repr__(self):
        hashcode = hex(hash(self))[2:]
        return "<Paillier Public Key".format(hashcode[:10])

    def __eq__(self, other):
        return self.n == other.n

    def __hash__(self):
        return hash(self.n)


class PaillierPrivateKey(object):
    def __init__(self,public_key,p,q):
        if not p*q == public_key.n:
            raise ValueError("pub key not equal")
        if p==q:
            raise ValueError("p and q have to be different")
        self.public_key = public_key
        self.p = q if q<p else p
        self.q = p if q<p else q
        self.p_square = pow(self.p, 2)
        self.q_square = pow(self.q, 2)
        self.q_inverse = invert(q,p)
        self.hp = self.h_fuc(self.p, self.p_square)
        self.hq = self.h_fuc(self.q,self.q_square)

    def h_fuc(self,x,xsquare):
        return invert(self.l_fuc(powmod(self.public_key.g,x-1,xsquare),x),x)

    def l_fuc(self,x,p):
        return (x-1)//p

    def crt(self,mp,mq):
        u = (mp - mq) * self.q_inverse % self.p
        x=(mq+(u*self.q)) % self.public_key.n
        return x

    def raw_decrypt(self,ciphertext):
        if not isinstance(ciphertext,int):
             raise TypeError("ciphertext should be int type")

        mp = self.l_fuc(powmod(ciphertext,self.p-1,self.p_square),self.p)* self.hp % self.p
        mq = self.l_fuc(powmod(ciphertext,self.q-1,self.q_square),self.q) * self.hq % self.q

        return self.crt(mp,mq)

    def decrypt(self,encrypt_number):
        if not isinstance(encrypt_number,PaillierEncryptNumber):
            raise TypeError("encrypt_number should be PaillierEncryptNumber type")

        if self.public_key != encrypt_number.public_key:
            raise ValueError(" the pb key is not equal")

        encoded = self.raw_decrypt(encrypt_number.ciphertext(be_secure=False))
        encoded = FixedPointNumber(encoded,encrypt_number.exponent,
                                   self.public_key.n,self.public_key.max_int)
        decrypt_value = encoded.decode()

        return decrypt_value

    def __eq__(self, other):
        return self.p ==other.p and self.q == other.q

    def __hash__(self):
        return hash((self.p,self.q))

    def __repr__(self):
        hashcode = hex(hash(self))[2:]
        return "<Paillier Private Key".format(hashcode[:10])


class PaillierEncryptNumber(object):
    def __init__(self,public_key,ciphertext,exponent=0):
        self.public_key = public_key
        self.__ciphertext=ciphertext
        self.exponent=exponent
        self.__is_obfuscator = False

        if not isinstance(self.__ciphertext,int):
            raise TypeError("ciphertext should be a int type")
        if not isinstance(self.public_key,PaillierPublicKey):
            raise TypeError("public_key should be a PaillierPublicKey type")

    def ciphertext(self,be_secure=True):

        if be_secure and not self.__is_obfuscator:
            self.apply_obfuscator()

        return self.__ciphertext

    def apply_obfuscator(self):
        self.__ciphertext = self.public_key.apply_obfuscator(self.__ciphertext)
        self.__is_obfuscator=True

    def increase_exponent_to(self,new_exponent):
        if new_exponent <self.exponent:
            raise ValueError("new exponent should be greater than old one")

        factor = pow(FixedPointNumber.BASE,new_exponent-self.exponent)
        new_encrypt_number = self.__mul__(factor)
        new_encrypt_number.exponent = new_exponent

        return new_encrypt_number

    def __align_exponent(self,x,y):
        if x.exponent < y.exponent:
            x = x.increase_exponent_to(y.exponent)
        elif x.exponent > y.exponent:
            y = y.increase_exponent_to(x.exponent)
        return x,y

    def __add_scalar(self,scalar):
        if isinstance(scalar,FixedPointNumber):
            scalar = scalar.decode()
        encode = FixedPointNumber.encode(scalar,
                                         self.public_key.n,
                                         self.public_key.max_int,
                                         max_exponent=self.exponent)
        print(encode.n)
        print(self.public_key.n)
        return self.__add_fixpointnumber(encode)


    def __add_fixpointnumber(self,encode):
        if self.public_key.n != encode.n:
            raise ValueError("the n of pub key and encode not equal")
        x,y = self.__align_exponent(self,encode)

        encrypt_scalar = x.public_key.raw_encrypt(y.encoding,1)
        encryptnumber = self.__raw_add(x.ciphertext(False),encrypt_scalar,x.exponent)

        return encryptnumber

    def __add_encryptnumber(self,other):
        if self.public_key !=other.public_key:
            raise ValueError("add two numbers has diff pub key")

        x, y = self.__align_exponent(self, other)

        encryptnumber = self.__raw_add(x.ciphertext(False), y.ciphertext(False), x.exponent)

        return encryptnumber

    def __raw_add(self,e_x,e_y,exponent):
        ciphertext = mpz(e_x) * mpz(e_y) % self.public_key.nsquare

        return PaillierEncryptNumber(self.public_key,int(ciphertext),exponent)

    def add_encryptnumber(self,other):
        return self.__add_encryptnumber(other)

    def add_scalar(self,scalar):
        return self.__add__(scalar)

    def mul_scalar(self,scalar):
        return self.__rmul__(scalar)

    def sub_scalar(self,scalar):
        return self.__sub__(scalar)

    def rsub_scalar(self,scalar):
        return self.__rsub__(scalar)

    def div_scalar(self,scalar):
        return self.__truediv__(scalar)



    def __add__(self, other):
        if isinstance(other,PaillierEncryptNumber):
            return self.__add_encryptnumber(other)
        else:
            return self.__add_scalar(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self +(other * -1)

    def __rsub__(self, other):
        return other + (self * -1)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return self.__mul__(1/scalar)

    def __mul__(self, scalar):
        if isinstance(scalar,FixedPointNumber):
            scalar = scalar.decode()
        encode = FixedPointNumber.encode(scalar,
                                         self.public_key.n,
                                         self.public_key.max_int)
        plaintext = encode.encoding

        if plaintext<0 or plaintext>=self.public_key.max_int:
            raise ValueError("scalar out of bounds")
        if plaintext >= self.public_key.n - self.public_key.max_int:
            neg_c = invert(self.ciphertext(False),self.public_key.nsquare)
            neg_scalar = self.public_key.n - plaintext
            ciphertext = powmod(neg_c,neg_scalar,self.public_key.nsquare)
        else:
            ciphertext = powmod(self.ciphertext(False),plaintext,self.public_key.nsquare)

        exponent = self.exponent + encode.exponent

        return PaillierEncryptNumber(self.public_key,int(ciphertext),exponent)



if __name__ == '__main__':
    pk,sk = PaillierKeyPair.generate_keypair(n_length=32)

    s1 = 3
    s2 = 6
    m1 = pk.encrypt(s1)
    m2 = pk.encrypt(s2)

    print(s1,s2)

    print(m1.ciphertext(False))
    print(m2.ciphertext(False))

    print("plus")
    m3 = m1.add_encryptnumber(m2)
    print(m3.ciphertext(False))
    s3 = sk.decrypt(m3)
    print(s3)

    print("add")
    m4 = m1.add_scalar(3)
    s4 = sk.decrypt(m4)
    print(s4)

    print("mul")
    m4 = m1.mul_scalar(4)
    s4 = sk.decrypt(m4)
    print(s4)


    pass
