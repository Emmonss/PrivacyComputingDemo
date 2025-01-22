

from algorithm.simple.gmpy_math import *
from algorithm.ecc.ecc_utils import generate_key,key_2_bytes,bytes_2_key,point_2_bytes,SUPPORT_CURVE
from algorithm.simple.shake_encode import encrypt, decrypt
from Crypto.PublicKey.ECC import EccKey

import numpy as np
import random
from pprint import pprint
from algorithm.ot.base import BaseSender,BaseReceiver
import time

class Sender(BaseSender):
    def __init__(self,curve='secp256r1'):
        super().__init__()
        self._curve = curve
        assert curve in SUPPORT_CURVE, ValueError(f"not support curve{curve}, should be one of{SUPPORT_CURVE}")


    def send1(self,msg):
        pk_list = []
        sk_list = []
        for i in range(len(msg)):
            sk,pk = generate_key(curve=self._curve)
            pk_list.append(key_2_bytes(pk))
            sk_list.append(sk)
        return pk_list,sk_list

    def send2(self,rec_pk_list,sender_sk_list,sender_pk_list,msg_list):
        '''
            rec_pk_list

            b==1时
            rec_pk = rec_pk + sender_pk
            ck0 = ( rec_pk + sender_pk )*sender_sk.d = rec_pk + sender_pk + 2sender_pk
            ck1 = ( rec_pk + sender_pk - sender_pk) )*sender_sk.d = rec_pk + sender_pk

            b==0时 rec_pk = rec_pk
            ck1 = rec_pk *sender_sk.d = rec_pk + sender_pk
            ck0 = ( rec_pk - sender_pk) )*sender_sk.d = rec_pk - sender_pk
        '''
        assert len(sender_sk_list)==len(rec_pk_list)==len(msg_list), ValueError("unequal len")
        cipher_list = []
        for index in range(len(msg_list)):
            msg = msg_list[index]
            m0,m1 = msg
            rec_pk = bytes_2_key(rec_pk_list[index])
            sender_pk = bytes_2_key(sender_pk_list[index])
            sender_sk = sender_sk_list[index]
            ck0 = rec_pk.pointQ * sender_sk.d
            ck1 = (-sender_pk.pointQ + rec_pk.pointQ) * sender_sk.d
            cipher0 = encrypt(point_2_bytes(ck0), m0)
            cipher1 = encrypt(point_2_bytes(ck1), m1)
            cipher_list.append((cipher0,cipher1))

        return cipher_list




class Receiver(BaseReceiver):
    def __init__(self):
        super().__init__()
        self.sender_pk_list = []
    def rec1(self,sender_pk_list,b_list):
        '''
            入参：sender_pk_list b_list
            生成曲线上的点sk和pk
            当b==1时 rec_pk = pk+sender_pk
            否则保持不变 rec_pk = pk
        '''
        assert set(b_list).issubset({0, 1}), ValueError("the chose data should be 0 or 1")
        assert len(b_list)==len(sender_pk_list),ValueError("choice list show as same len as pk list")
        curve = bytes_2_key(sender_pk_list[0]).curve
        rec_pk_list = []
        rec_sk_list = []
        for index,b in enumerate(b_list):
            sender_pk = bytes_2_key(sender_pk_list[index])
            self.sender_pk_list.append(sender_pk)
            sk,pk = generate_key(curve=curve)
            if b ==1:
                point = pk.pointQ + sender_pk.pointQ
                pk = EccKey(curve=curve, point=point)
            rec_pk_list.append(key_2_bytes(pk))
            rec_sk_list.append(sk)

        return rec_pk_list,rec_sk_list

    def rec2(self, cipher_list, b_list, rec_sk_list:list[EccKey]):
        assert set(b_list).issubset({0, 1}), ValueError("the chose data should be 0 or 1")
        assert len(cipher_list) == len(b_list), ValueError("the length choice list must be as same as the cipher list")
        plaintext_list = []
        fakertext_list = []
        for index,b in enumerate(b_list):
            ck = self.sender_pk_list[index].pointQ *rec_sk_list[index].d
            cipher_mi = cipher_list[index][b]
            faker_cipher_mi = cipher_list[index][abs(1-b)]
            plaintext_list.append(decrypt(point_2_bytes(ck), cipher_mi))
            fakertext_list.append(decrypt(point_2_bytes(ck), faker_cipher_mi))

        self.sender_pk_list.clear()
        return plaintext_list,fakertext_list





if __name__ == '__main__':
    def get_rnd_num():
        return np.round(random.uniform(0, 100), 2)
    st = time.time()

    curve = 'secp256r1'
    msg_len = 100000
    print(f"测试数据量：{msg_len}")
    sender = Sender(curve=curve)
    receiver = Receiver()
    print("sender 生成测试数据".center(100, "="))
    msg1 = [(get_rnd_num(), get_rnd_num()) for _ in range(msg_len)]
    msg = [(item[0].tobytes(), item[1].tobytes()) for item in msg1]
    # pprint(msg1)
    # pprint(msg)

    print("sender 生成sender sk pk并发送到receiver".center(100, "="))
    sender_pk_list, sender_sk_list = sender.send1(msg)
    # print(sender_sk_list)
    # pprint(sender_pk_list)

    print("receiver 生成选择列b".center(100, "="))
    b_list = [random.randint(0, 1) for _ in range(msg_len)]
    # print(f"b_list:{b_list}")

    print("receiver 根据sender_result1 生成receiver 的pk sk".center(100, "="))
    rec_pk_list,rec_sk_list = receiver.rec1(sender_pk_list, b_list)
    # pprint(rec_pk_list)
    # pprint(rec_sk_list)

    print("sender 根据pk0加密数据".center(100, "="))
    cipher_list = sender.send2(rec_pk_list, sender_sk_list, sender_pk_list, msg)
    # pprint(cipher_list)

    print("receiver 恢复数据".center(100, "="))
    res_list, faker_list = receiver.rec2(cipher_list,b_list,rec_sk_list)
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

