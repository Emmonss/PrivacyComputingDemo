import numpy as np
import random
from pprint import pprint
from algorithm.ot.base import BaseSender,BaseReceiver
from algorithm.ot.ot_demo_ecc import Sender as EccOtSender
from algorithm.ot.ot_demo_ecc import Receiver as EccOtReceiver
from utils.conversion import *
from algorithm.simple.shake_encode import encrypt, decrypt

class Sender(BaseSender):
    def __init__(self, k=12):
        super().__init__()
        self._k = k

        self._s = None

        self._q = None

        self._n = 0

        self._m = 0

        self.base_ot_rec = EccOtReceiver()

    @property
    def max_count(self)->int:
        if self._q is None:
            return 0
        else:
            return self._m

    def prepare1(self, rec_spk_list, rec_m):
        self._m = rec_m
        self._s = np.random.randint(2, size=self._k)
        # print(f"sender 选择列{self._s}")
        sender_rpk_list, self.sender_rsk_list= sender.base_ot_rec.rec1(rec_spk_list, self._s)
        return sender_rpk_list

    def prepare2(self, cipher_list):
        out, _ = self.base_ot_rec.rec2(cipher_list,self._s, self.sender_rsk_list)
        self._q = np.vstack([bytes_to_bit_arr(col) for col in out]).T
        return self._q

    def send(self, msg):
        assert len(msg) == self._m, ValueError("unequal size")

        packed_cipher = [
            (encrypt(int_to_bytes(i) + bit_arr_to_bytes(self._q[i,:]), msg[i][0]),
             encrypt(int_to_bytes(i) + bit_arr_to_bytes(self._q[i, :] ^ self._s), msg[i][1]))
            for i in range(self._m)
        ]
        self._n = self._m
        return packed_cipher

class Receiver(BaseReceiver):
    def __init__(self, k=128):
        super().__init__()

        self.rec_ssk_list = None
        self._r = None
        self._t = None
        self._k = k
        self._n:int = 0
        self._m:int = 0

        self.base_ot_sender = EccOtSender()

    @property
    def max_count(self) -> int:
        if self._r is None:
            return 0
        else:
            return self._m

    def prepare1(self,b_list):
        self._r = np.array(b_list)
        self._m = self._r.size

        # matrix m*k
        self._t = np.random.randint(2,size=(self._m, self._k))
        # print(f"rec t\n{self._t}")

        # u = (k*m ^ k).T = m * k
        '''
            b = r = [0,1]
            t = [[1 0 0],
                 [1 1 1]]
            u = [[1 0 0][0 0 0]]
        '''
        u = (self._t.T ^ self._r).T
        # print(f"rec u\n{u}")
        self.msg_list = [(bit_arr_to_bytes(self._t[:,i]), bit_arr_to_bytes(u[:,i])) for i in range(self._k)]
        self.rec_spk_list, self.rec_ssk_list = self.base_ot_sender.send1(self.msg_list)
        return self.rec_spk_list, self._m

    def prepare2(self, sender_rpk_list):
        cipher_list = self.base_ot_sender.send2(sender_rpk_list, self.rec_ssk_list, self.rec_spk_list, self.msg_list)
        # print(f"rec cipher_list:\n{cipher_list}")
        return cipher_list

    def remote(self,sender_packd_cipher):
        key_list = [int_to_bytes(i) + bit_arr_to_bytes(self._t[i,:]) for i in range(self._m)]

        res = [decrypt(key_list[i],sender_packd_cipher[i][self._r[i]]) for i in range(self._m)]

        return res





if __name__ == '__main__':
    def get_rnd_num():
        return np.round(random.uniform(0, 100), 2)


    import time

    st = time.time()

    msg_len = 100000
    print(f"测试数据量：{msg_len}")
    k = 128
    sender = Sender(k=k )
    receiver = Receiver(k=k )
    print("sender 生成测试数据".center(100, "="))
    msg1 = [(get_rnd_num(), get_rnd_num()) for _ in range(msg_len)]
    msg = [(item[0].tobytes(), item[1].tobytes()) for item in msg1]
    # pprint(msg1)
    # pprint(msg)

    print("receiver 生成选择列b".center(100, "="))
    b_list = [random.randint(0,1) for _ in range(msg_len)]
    # print(f"receiver 选择列:{b_list}")

    print("receiver prepare1".center(100, "="))
    rec_spk_list, rec_m = receiver.prepare1(b_list)

    print("sender prepare1".center(100, "="))
    sender_rpk_list = sender.prepare1(rec_spk_list, rec_m)

    print("receiver prepare2".center(100, "="))
    rec_cipher_list = receiver.prepare2(sender_rpk_list)

    print("sender prepare2".center(100, "="))
    sender_chose = sender.prepare2(rec_cipher_list)
    # print(sender_chose)

    print("sender send msg".center(100, "="))
    sender_packd_cipher = sender.send(msg)
    # print(sender_packd_cipher)

    print("receiver decode msg".center(100, "="))
    res = receiver.remote(sender_packd_cipher)
    out = [np.frombuffer(item)[0] for item in res]
    # print(out)

    ed = time.time()

    print(f"原始数据\n{msg1[:10]}")
    print(f"选择列b:{b_list[:10]}")
    print(f"选择结果{out[:10]}")
    print(f"耗时：{ed-st}s")
    # r = np.array(b_list)
    # m = r.size
    # k = 8
    # t = np.random.randint(2,size=(m,k))
    # u = (t.T ^ r).T
    # print(t)
    # print(u)
    # msg_list = [(bit_arr_to_bytes(t[:,i]), bit_arr_to_bytes(u[:,i])) for i in range(k)]
    # print(msg_list)
    # print(np.array(msg_list).shape)
    # print(t[:,0])
    # s = bit_arr_to_bytes(t[:,0])
    # print(s)
    # print(bytes_to_bit_arr(s))




