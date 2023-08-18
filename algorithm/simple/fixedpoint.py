


import functools,math,sys
import numpy as np
from algorithm.simple._DTable import TableABC

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
            if self.max_int is None:
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
                isinstance(scalar,np.int32) or isinstance(scalar,np.int64):
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

        if abs(int_fixpoint)> max_int:
            raise ValueError(" too big int_fixpoint")

        return cls(int_fixpoint%n,exponent,max_int)

    def decode(self):
        pass