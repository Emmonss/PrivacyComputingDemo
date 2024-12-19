
import algorithm.simple.gmpy_math as gm_fuc
from rsa import PublicKey
from algorithm.base.hash import compute_sha256
from pprint import pprint
import gmpy2

import rsa
from rsa import PublicKey

random_num_len = 128
rsa_len = 256

def make_rsa(len= 512):
    (pubkey, privkey) = rsa.newkeys(512)
    return pubkey, privkey

class RSATransEntity:
    def __init__(self,e,d,n):
        self.e = e
        self.d = d
        self.n = n

    def __str__(self):
        return f"e:{self.e},d:{self.d},n:{self.n}"

class Guest:
    def __init__(self):
        self.rsa_set = RSATransEntity(None,None,None)
        self.r = gm_fuc.get_random_big_num(random_num_len)


    def hash_data(self,data:list[str]):
        data_result = [compute_sha256(item) for item in data]
        data_result = [gm_fuc.mpz(int(item,16)) for item in data_result]
        return data_result
    def get_host_pubkey(self,pubkey:PublicKey):
        self.rsa_set = RSATransEntity(pubkey.e,None,pubkey.n)

    def calculate_enc_g(self, data: list[str]):
        data = self.hash_data(data)
        #refresh radom data
        self.r = gm_fuc.get_random_big_num(random_num_len)
        # print(f'guest currrent random data:{self.r}')
        if self.rsa_set.e is None:
            raise ValueError("should init pubkey from host party")
        res = []
        for item in data:
            enc_r = gm_fuc.powmod(self.r, self.rsa_set.e, self.rsa_set.n)
            result = gm_fuc.mul(enc_r, item)
            res.append(result)
        return res

    def calculate_enc_g_from_host(self,enc_g:list[gmpy2.mpz]):
        if self.rsa_set.e is None:
            raise ValueError("should init pubkey from host party")
        # print(f'guest currrent random data:{self.r}')
        res = []
        for item in enc_g:
            enc_g2 = gm_fuc.divm(item, self.r, self.rsa_set.n).digits()
            enc_g2 = compute_sha256(enc_g2)
            res.append(enc_g2)
        return res

    def clear(self):
        self.rsa_set = RSATransEntity(None, None, None)
        self.r = gm_fuc.get_random_big_num(random_num_len)
class Host:
    def __init__(self):
        self.pubkey, self.privkey  = None,None
        self.rsa_set = RSATransEntity(None,None,None)
        self.flat_dict = dict()

    def hash_data(self,data:list[str]):
        data_result = [compute_sha256(item) for item in data]
        data_result = [gm_fuc.mpz(int(item,16)) for item in data_result]
        return data_result

    def init_rsa_params(self):
        self.pubkey, self.privkey = make_rsa(rsa_len)
        self.rsa_set = RSATransEntity(self.privkey.e,self.privkey.d,self.privkey.n)

        pass

    def calculate_enc_h(self,data:list[str]):
        data_hash = self.hash_data(data)
        if self.rsa_set.e is None:
            raise ValueError("should init pubkey from host party")
        res = []
        res_dict = dict()
        for index,item in enumerate(data_hash):
            enc_h = gm_fuc.powmod(item, self.rsa_set.d, self.rsa_set.n).digits()
            enc_h = compute_sha256(enc_h)
            res.append(enc_h)
            res_dict[enc_h] = data[index]
        self.flat_dict = res_dict
        pprint(self.flat_dict)
        return res

    def calculate_enc_g(self,enc_g:list[gmpy2.mpz]):
        if self.rsa_set.e is None:
            raise ValueError("should init pubkey from host party")

        res = []
        for item in enc_g:
            enc_g2 = gm_fuc.powmod(item, self.rsa_set.d, self.rsa_set.n)
            res.append(enc_g2)

        return res

    def calculate_intersecttion(self, enc_g:list[str], enc_h:list[str]):
        result = []
        if len(self.flat_dict) == 0:
            raise ValueError("enc_h is not compute pre")
        ins = list(set(enc_g).intersection(set(enc_h)))
        for item in ins:
            if item in self.flat_dict.keys():
                result.append(self.flat_dict.get(item))
        return result

    def clear(self):
        self.pubkey, self.privkey = None, None
        self.rsa_set = RSATransEntity(None, None, None)
        self.flat_dict = dict()





if __name__ == '__main__':
    guest_data = [str(i) for i in range(2)]+['qweasd',"qwe"]
    pprint(f"guest_data:{guest_data}")

    host_data = [str(i) for i in range(5)]+["qwe","asd"]
    pprint(f"host_data:{host_data}")

    host = Host()
    guest = Guest()

    #1
    print("init host rsa params:".center(60,'+'))
    host.init_rsa_params()
    print(f"host rsa params:{host.rsa_set}")
    #2
    print("send rsa pub key to guest:".center(60, '='))
    guest.get_host_pubkey(host.pubkey)
    print(f"guest rsa params:{guest.rsa_set}")

    #3
    print("guest compute enc_g".center(60, '='))
    enc_g = guest.calculate_enc_g(guest_data)
    # pprint(enc_g)
    print(f"enc_g size:{len(enc_g)}")

    print("host compute enc_h".center(60, '+'))
    enc_h = host.calculate_enc_h(host_data)
    print(f"enc_h size:{len(enc_h)}")
    pprint(enc_h)

    print("host compute enc_g from guest".center(60, '+'))
    enc_g = host.calculate_enc_g(enc_g)
    print(f"enc_g size:{len(enc_g)}")
    # pprint(enc_g)

    print("guest compute enc_g from host".center(60, '='))
    enc_g2 = guest.calculate_enc_g_from_host(enc_g)
    print(f"enc_g size:{len(enc_g2)}")
    pprint(enc_g2)

    # print("host get intersection by eng_g and enc_h".center(60, '+'))
    # psi_result = host.calculate_intersecttion(enc_g2, enc_h)
    # print(f"psi_result size:{len(psi_result)}")
    # pprint(psi_result)

    host.clear()
    guest.clear()

    pass