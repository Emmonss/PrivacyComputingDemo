


import math,sys
import numpy as np
from gmpy2 import gmpy2

from algorithm.base._DTable import TableABC

class FixedPointNumber(object):

    BASE = 16
    LOG2_BASE = math.log(BASE,2)

    FLOAT_MANTISSA_BITS = sys.float_info.mant_dig

    #max prime of 127 bit
    Q = 293973345475167247070445277780365744413 ** 2

    def __init__(self,encoding,exponent,n=None,max_int = None):
        if n is None:
            self.n = FixedPointNumber.Q
            self.max_int = self.n //2
        else:
            self.n = n
            if max_int is None:
                self.max_int = self.n // 2
            else:
                self.max_int = max_int

        self.encoding = encoding
        self.exponent = exponent


    @classmethod
    def calculate_exponent_from_precision(cls,precision):
        exponent = math.floor(math.log(precision,cls.BASE))
        return exponent

    @classmethod
    def encode(cls,scalar,n=None,max_int=None,precision=None,max_exponent=None):

        exponent = None

        if np.abs(scalar)<1e-200:
            scalar=0

        if n is None:
            n = cls.Q
            max_int = n //2

        if precision is None:
            if isinstance(scalar,int) or isinstance(scalar,np.int16) or \
                isinstance(scalar,np.int32) or isinstance(scalar,np.int64) or isinstance(scalar, gmpy2.mpz):
                exponent=0
            elif isinstance(scalar,float) or isinstance(scalar,np.float16) or \
                isinstance(scalar,np.float32) or isinstance(scalar,np.float64):
                flt_exponent = math.frexp(scalar)[1]
                lsb_exponent = cls.FLOAT_MANTISSA_BITS - flt_exponent

                exponent = math.floor(lsb_exponent / cls.LOG2_BASE)
            else:
                raise TypeError("what the fuck of the type of scalar:{}".format(type(scalar)))

        else:
            exponent = cls.calculate_exponent_from_precision(precision)

        if max_exponent is not None:
            exponent = max(max_exponent,exponent)

        int_fixpoint = int(round(scalar * pow(cls.BASE,exponent)))

        if abs(int_fixpoint) > max_int:
            raise ValueError(" too big int_fixpoint")

        return cls(int_fixpoint%n,exponent,n,max_int)

    def decode(self):
        if self.encoding>self.n:
            raise ValueError('attempt to decode corrupted number')
        elif self.encoding <=self.max_int:
            mantissa = self.encoding
        elif self.encoding >= self.n - self.max_int:
            mantissa = self.encoding - self.n
        else :
            raise OverflowError('overflow detected in decode number')

        return mantissa * pow(self.BASE, -self.exponent)

    def increase_exponent_to(self,new_exponent):
        if new_exponent <self.exponent:
            raise ValueError("new exponent should be big than old one")
        factor  = pow(self.BASE,new_exponent-self.exponent)
        new_encode = self.encoding * factor % self.n

        return FixedPointNumber(new_encode,new_exponent,self.n,self.max_int)

    def __align_exponent(self,x,y):
        if x.exponent<y.exponent:
            x = x.increase_exponent_to(y.exponent)
        else:
            y = y.increase_exponent_to(x.exponent)

        return x,y


    def __trncate(self,a):
        scalar = a.decode()
        return FixedPointNumber(scalar,n=self.n,max_int=self.max_int)

    def __add_fixedpointnumber(self,other):
        if self.n != other.n:
            other = self.encode(other.decode(),n=self.n,max_int=self.max_int)
        x,y = self.__align_exponent(self,other)
        encoding = (x.encoding + y.encoding) % self.n
        return FixedPointNumber(encoding, x.exponent, n=self.n, max_int=self.max_int)

    def __add_scalar(self,scalar):
        encode = self.encode(scalar,n=self.n, max_int=self.max_int)
        return self.__add_fixedpointnumber(encode)

    def __sub_fixedpointnumber(self,other):
        if self.n != other.n:
            other = self.encode(other.decode(),n=self.n,max_int=self.max_int)
        x,y = self.__align_exponent(self,other)
        encoding = (x.encoding - y.encoding) % self.n
        return FixedPointNumber(encoding, x.exponent, n=self.n, max_int=self.max_int)

    def __sub_scalar(self,scalar):
        scalar = -1 * scalar
        return self.__add_scalar(scalar)

    def __mul_fixedpointnumber(self, other):
        pass

    def __mul_scalar(self,scalar):
        val = self.decode()
        z = val *scalar
        z_encode = FixedPointNumber.encode(z, n=self.n, max_int=self.max_int)
        return z_encode




    def __add__(self, other):
        if isinstance(other,FixedPointNumber):
            return self.__add_fixedpointnumber(other)
        elif type(other).__name__ =="PaillierEncryptNumber":
            return other + self.decode()
        else:
            return self.__add_scalar(other)

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, FixedPointNumber):
            return self.__sub_fixedpointnumber(other)
        elif type(other).__name__ == "PaillierEncryptNumber":
            return (other - self.decode()) * -1
        else:
            return self.__sub_scalar(other)

    def __rsub__(self, other):
        if type(other).__name__ == "PaillierEncryptNumber":
            return other - self.decode()
        x = self.__sub__(other)
        x = -1 * x.decode()
        return self.encode(x, n=self.n, max_int=self.max_int)

    def __mul__(self, other):
        if isinstance(other, FixedPointNumber):
            return self.__mul_fixedpointnumber(other)
        elif type(other).__name__ == "PaillierEncryptNumber":
            return other * self.decode()
        else:
            return self.__mul_scalar(other)

    def __rmul__(self, other):
        return self.__mul__()

    def __truediv__(self, other):
        if isinstance(other, FixedPointNumber):
            scalar = other.decode()
        else:
            scalar = other
        return self.__mul__(1/scalar)

    def __rtruediv__(self, other):
        res = 1.0 / self.__truediv__(other).decode()
        return FixedPointNumber.encode(res, n=self.n, max_int=self.max_int)

    def __lt__(self, other):
        x = self.decode()
        if isinstance(other, FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x<y:
            return True
        else:
            return False

    def __gt__(self, other):
        x = self.decode()
        if isinstance(other,FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x>y:
            return True
        else:
            return False

    def __le__(self, other):
        x = self.decode()
        if isinstance(other, FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x <= y:
            return True
        else:
            return False


    def __ge__(self, other):
        x = self.decode()
        if isinstance(other, FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x >= y:
            return True
        else:
            return False

    def __eq__(self, other):
        x = self.decode()
        if isinstance(other, FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x == y:
            return True
        else:
            return False

    def __ne__(self, other):
        x = self.decode()
        if isinstance(other, FixedPointNumber):
            y = other.decode()
        else:
            y = other
        if x != y:
            return True
        else:
            return False

    def __abs__(self):
        if self.encoding <= self.max_int:
            return self
        elif self.encoding >= self.n - self.max_int:
            return self * -1

    def __mod__(self, other):
        return FixedPointNumber(self.encoding % other, self.exponent, n=self.n, max_int=self.max_int)


class FixPointEndec(object):
    def __init__(self,
                 n=None,
                 max_int=None,
                 precision=None,*args,**kwargs):
        if n is None:
            self.n = FixedPointNumber.Q
            self.max_int = self.n //2
        else:
            self.n = n
            if max_int is None:
                self.max_int = self.n//2
            else:
                self.max_int = max_int

        self.precision = precision


    @classmethod
    def _transform_op(cls, tensor, op):
        def _is_table(x):
            return isinstance(x,TableABC)
        def _transform(x):
            arr = np.zeros(shape=x.shape,dtype=object)
            view = arr.view().reshape(-1)
            x_array = x.view().reshape(-1)
            for i in range(arr.size):
                view[i] - op(x_array[i])
            return arr




