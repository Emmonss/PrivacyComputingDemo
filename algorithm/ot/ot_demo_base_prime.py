import numpy as np

from algorithm.simple.gmpy_math import *
from algorithm.base.hash import compute_sha256
from algorithm.ecc.ecc_utils import generate_key
from algorithm.ot.base import BaseSender,BaseReceiver
from algorithm.simple.shake_encode import encrypt,decrypt
from pprint import pprint

#naor pinkas ot base prime



class Sender(BaseSender):
    def __init__(self, bit_len =128):
        super().__init__()
        self.bit_len = bit_len
        self.a_list = []

    def _make_rnd_C(self,p,g):
        while 1:
            c = get_generation_for_safe_prime(p)
            if sign(sub(c,g)) !=0:
                return c


    def _make_rnd_a(self,p):
        while 1:
            rs = get_rand_state(p)
            a = mpz_rrandomb(rs,self.bit_len)
            if sign(sub(a,0))>0:
                return a


    def send1(self,msg):
        '''
            生成 p,g,C a
            保存a
            发送 p C g 给receiver
        '''
        p_list = []
        c_list = []
        g_list = []
        for i in range(len(msg)):
            p = get_safe_prime(self.bit_len)
            g = get_generation_for_safe_prime(p)
            c = self._make_rnd_a(p)
            a = self._make_rnd_a(p)

            p_list.append(p)
            c_list.append(c)
            g_list.append(g)
            self.a_list.append(a)

        return {
            'c_list':c_list,
            'g_list':g_list,
            'p_list':p_list
        }

    def send2(self,self_send1_result, rec_pk0_list, msg):
        '''
            自我生成的 p g C a
            receiver 生成的pk0
            ga = g^a mod p
            ca = c^a mod p
            ca^-1 * ca = 1 mod p

            当pk0 = g^k mod p 时
            sender_pk0 = pk0 ^ a mod p = (g^k mod p ) ^ a mod p  = g ^ ka mod p
            sender_pk1 = ((g^k mod p)^a mod p) * ca^-1 mod p = (g^ka * ca^-1) mod p

            当pk0 = c * gk mod p
            sender_pk0 = ((c * gk) mod p) ^ a mod p  = (c^a * g^ka) mod p
            sender_pk1 = (((c * gk) mod p)^a mod p) * ca^-1 mod p  = (c^a * g^ka * ca^-1) mod p = g^a mod p

            receiver不知道a的值 求不出 c^a mod p 只能得到一个密钥

            cipher0 = sender_pk0^msg0
            cipher1 = sender_pk1^msg1

            return [g^a, cipher0, cipher1]
        '''
        assert len(rec_pk0_list) == len(msg), ValueError("pk0 should be the same len as msg")
        assert len(self.a_list)!=0, ValueError("you should run send1 first")

        res_list = []
        for index, pk0 in enumerate(rec_pk0_list):
            a = self.a_list[index]
            g = self_send1_result['g_list'][index]
            c = self_send1_result['c_list'][index]
            p = self_send1_result['p_list'][index]
            g_a = powmod(g,a,p)
            c_a = powmod(c,a,p)
            c_a_1 = invert(c_a,p)

            sender_pk0 = powmod(pk0,a,p)
            sender_pk1 = mod(mul(powmod(pk0,a,p),c_a_1),p)


            sender_pk0 = sender_pk0.to_bytes(sender_pk0.bit_length(),'big')
            sender_pk1 = sender_pk1.to_bytes(sender_pk1.bit_length(), 'big')


            m0 = encrypt(sender_pk0, msg[index][0])
            m1 = encrypt(sender_pk1, msg[index][1])
            res_list.append([g_a,m0,m1])
        self.a_list.clear()
        return res_list

class Receiver(BaseReceiver):
    def __init__(self):
        super().__init__()
        self.p_list = []
        self.k_list = []

    def _get_rnd_k(self,p,g):
        while 1:
            rs = get_rand_state(p)
            k = mpz_random(rs,g)
            if sign(sub(k,0))>0:
                return k

    def rec1(self,send_result1,b_list):
        '''
            从sender获得p g C
            入参自我生成选择列b->(0,1)
            生成随机数k
            gk = g^k mod p

            b==0时
            pk0 = gk
            pk1 = c * gk mod p

            b==1时
            pk0 = c * gk mod p
            pk1 = gk

            发送pk0 给sender
        '''
        assert set(b_list).issubset({0, 1}), ValueError("the chose data should be 0 or 1")
        self.p_list = send_result1['p_list']
        send_glist = send_result1['g_list']
        send_clist = send_result1['c_list']

        pk0_list = []
        pk1_list = []
        for i,b in enumerate(b_list):

            c = send_clist[i]
            g = send_glist[i]
            p = self.p_list[i]
            k = self._get_rnd_k(p, g)

            self.k_list.append(k)
            g_k = powmod(g,k,p)
            if(b==0):
                pk0_list.append(g_k)
                pk1_list.append(mod(mul(c,g_k),p))
            else:
                pk1_list.append(g_k)
                pk0_list.append(mod(mul(c,g_k),p))

        return pk0_list

    def rec2(self,sender_cipher_list, b_list):

        '''
            sender入参 [g^a, cipher0, cipher1]
            自我选择列：b_list -> {0,1}, 随机数列k

            计算解密密钥key = (g^a mod p )^k mod p = g^ka mod p

            b==0 时
            plaintext = key^cipher0
            faker = key^cipher1
            b==1 时
            plaintext = key^cipher1
            faker = key^cipher0

        '''
        assert len(sender_cipher_list) == len(b_list), ValueError("the length choice list must be as same as the cipher list")


        res_list = []
        faker_list = []

        for index,b in enumerate(b_list):
            k = self.k_list[index]
            p = self.p_list[index]
            g_a = sender_cipher_list[index][0]
            cipher = sender_cipher_list[index][2 if b==1 else 1]
            faker_cipher = sender_cipher_list[index][1 if b==1 else 2]

            key = powmod(g_a,k,p)
            key = key.to_bytes(key.bit_length(),'big')
            res = decrypt(key, cipher)
            faker = decrypt(key,faker_cipher)
            res_list.append(res)
            faker_list.append(faker)

        self.k_list.clear()
        self.p_list.clear()
        return res_list, faker_list



if __name__ == '__main__':
    def get_rnd_num():
        return np.round(random.uniform(0,100),2)
    import time

    st = time.time()

    msg_len = 1000
    print(f"测试数据量：{msg_len}")
    sender = Sender()
    receiver = Receiver()
    print("sender 生成测试数据".center(100,"="))
    msg1 = [(get_rnd_num(),get_rnd_num()) for _ in range(msg_len)]
    msg = [(item[0].tobytes(), item[1].tobytes()) for item in msg1]
    # pprint(msg1)
    # pprint(msg)

    print("sender 根据msg 生成sender_result1 并发送到receiver".center(100, "="))
    sender_result1 = sender.send1(msg)
    # pprint(sender_result1)

    print("receiver 生成选择列b".center(100, "="))
    b_list = [random.randint(0,1) for _ in range(msg_len)]
    # print(f"b_list:{b_list}")


    print("receiver 根据sender_result1 生成receiver 的pubkey".center(100, "="))
    receiver_pk0_list = receiver.rec1(sender_result1, b_list)
    # pprint(receiver_pk0_list)


    print("sender 根据pk0加密数据".center(100, "="))
    cipher_list = sender.send2(sender_result1, receiver_pk0_list, msg)
    # pprint(cipher_list)

    print("receiver 恢复数据".center(100, "="))
    res_list, faker_list = receiver.rec2(cipher_list,b_list)
    # print(f"res_list:{res_list}")
    # print(f"faker_list:{faker_list}")

    plaintext = [np.frombuffer(item)[0] for item in res_list]
    faker_plaintext = [np.frombuffer(item)[0] for item in faker_list]
    # print(f"res_list:{plaintext}")
    # print(f"faker_list:{faker_plaintext}")

    print('='*100)
    print(f"原始数据:{msg1}")
    print(f"选择列:{b_list}")
    print(f"OT结果:{plaintext}")
    print(f"假结果：{faker_plaintext}")

    ed = time.time()
    print(f"耗时：{ed-st}s")
