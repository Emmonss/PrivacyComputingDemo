from pprint import pprint
from fuctions.ot.base import BaseSender,BaseReceiver
from algorithm.base.hash import Hash
from utils.constant_utils import HASH_SHA256
import random,gmpy2
import numpy as np
from algorithm.simple.gmpy_math import *

class Sender(BaseSender):
    def __init__(self,bit_len=128,n=2):
        super().__init__()
        self.bit_len = bit_len

        self.C_list = []
        self.g_list = []
        self.p_list = []
        self.a_list = []
        self.ga_list = []
        self.ca_list = []
        self.ca1_list = []
        self.sha256 = Hash(method=HASH_SHA256)

    def _get_rnd_c(self,p,g):
        while 1:
            c = get_generation_for_safe_prime(p)

            if gmpy2.sign(gmpy2.sub(c,g)) !=0:
                return c


    def _get_rnd_a(self,p):
        while 1:
            rs = get_rand_state(p)
            a = gmpy2.mpz_random(rs,self.bit_len)

            if gmpy2.sign(gmpy2.sub(a,0)) >0:
                return a

    def send(self,msg):
        pass


