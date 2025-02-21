import random

import numpy
from Crypto.PublicKey import ECC
import pandas as pd
from algorithm.ecc.ecc_utils import generate_key,key_2_bytes,point_2_bytes,point_2_bytes2
from algorithm.pailler.crt_paillier import PaillierKeyPair,PaillierPublicKey
from algorithm.simple.gmpy_math import mpz
from algorithm.base.hash import compute_sha256
from utils.shuffle_utils import *
ran_seed = 123
ran_seed2 = 234



class PartyC:
    def __init__(self,key_len = 16):
        self.sk_blue,self.pk_blue = generate_key()
        self.pk_black,self.sk_black = PaillierKeyPair.generate_keypair(key_len)

    def get_self_pk_black(self):
        return self.pk_black

    def partyC_step2(self,data,key = 'key',value = 'value'):
        shuffle_data = data.sample(frac=1, random_state=ran_seed).reset_index(drop=True)
        enc_key = []
        enc_value = []
        for item in shuffle_data[key]:
            item = mpz(int(compute_sha256(item), 16))
            enc_key.append(mpz(item) * self.pk_blue.pointQ)
        for item in shuffle_data[value]:
            enc_value.append(self.pk_black.encrypt(item))
        return pd.DataFrame({
            key: enc_key,
            value: enc_value
        })


    def partyC_step3(self,data,key = 'key',value = 'value'):
        enc_data = []
        for item in data[key]:
            enc_data.append(item*self.sk_blue.d)
        # data[key] = enc_data
        return pd.DataFrame({
            key:enc_data,
            value:data[value]
        })

    def partyC_step7(self,pc_data, pp_data,key = 'key',value = 'value'):
        pc_data_key = [point_2_bytes(item).hex() for item in pc_data[key]]
        pp_data_key = [point_2_bytes(item).hex() for item in pp_data[key]]
        pc_data_value = list(pc_data[value])
        pp_data_value = list(pp_data[value])
        # print(pc_data_key)
        # print(pp_data_key)
        insec_data = list(set(pc_data_key).intersection(set(pp_data_key)))
        # print(insec_data)
        pc_index = []
        pp_index = []
        pc_select_value = []
        pp_select_value = []
        for item in insec_data:
            pc_i = find_index(pc_data_key,item)
            if pc_i!=-1:
                pc_index.append(pc_i)
                pc_select_value.append(pc_data_value[pc_i])
            pp_i = find_index(pp_data_key,item)
            if pp_i!=-1:
                pp_index.append(pp_i)
                pp_select_value.append(pp_data_value[pp_i])
        pc_data_pc_share = [self.sk_black.decrypt(item) - bound for item in pp_select_value]
        return insec_data,pc_select_value,pp_index,pc_data_pc_share
        # print(pc_index)
        # print(pp_index)
        # print([pp_pk.decrypt(item) for item in pc_select_value])
        #
        # print([-(self.sk_black.decrypt(item) - bound) for item in pp_select_value])

    def partyC_step8_9(self, data, pp_pk_gray:PaillierPublicKey):
        pp_rand = [0 - random.randint(1, 10) for _ in range(len(data))]
        enc_rand = [pp_pk_gray.encrypt(item+bound) for item in pp_rand]
        enc_data = []
        for index, item in enumerate(data):
            enc_div = item + enc_rand[index]
            enc_data.append(enc_div)
        return [-item for item in pp_rand], enc_data
        pass



class PartyP:
    def __init__(self, key_len=16):
        self.sk_red, self.pk_red = generate_key()
        self.pk_gray, self.sk_gray = PaillierKeyPair.generate_keypair(key_len)

    def get_self_pk_gray(self):
        return self.pk_gray

    def partyP_step2(self,data,key = 'key',value = 'value'):
        shuffle_data = data.sample(frac=1, random_state=ran_seed).reset_index(drop=True)
        enc_key = []
        enc_value = []
        for item in shuffle_data[key]:
            item = mpz(int(compute_sha256(item), 16))
            enc_key.append(item * self.pk_red.pointQ)
        for item in shuffle_data[value]:
            enc_value.append(self.pk_gray.encrypt(item))
        return pd.DataFrame({
            key: enc_key,
            value: enc_value
        })

    def partyP_step3_4(self,data,key = 'key',value = 'value'):
        enc_data = []
        for item in data[key]:
            enc_data.append(item*self.sk_red.d)
        res = pd.DataFrame({
            key: enc_data,
            value: data[value]
        })

        return res.sample(frac=1, random_state=ran_seed2).reset_index(drop=True)

    def partyP_step5(self,data, pc_pk_black:PaillierPublicKey):
        pp_rand = [0 - random.randint(1, 10) for _ in range(data.shape[0])]
        shuffled_list, _ = shuffle_with_seed(pp_rand,ran_seed)
        shuffle_dict = {}
        for item in shuffled_list:
            enc_item = pc_pk_black.encrypt(item + bound)
            shuffle_dict[enc_item] = -item
        return shuffle_dict

    def partyP_step6_7(self,data,rand_data,key = 'key',value = 'value'):
        enc_data = []
        # print(rand_data)
        for index,item in enumerate(data[value]):
            enc = item + rand_data[index]
            enc_data.append(enc)
        # data[value] = enc_data
        return pd.DataFrame({
            key:data[key],
            value:enc_data
        })

    def partyP_step10(self, data):
        return [self.sk_gray.decrypt(item)- bound for item in data]
        pass

    def partyP_step11(self, pp_index_step7, pp_rand_step5, pp_rand_dict5):
        pc_data_pp_share = []
        for index in pp_index_step7:
            pp_rand_index = pp_rand_step5[index]
            pc_data_pp_share.append(pp_rand_dict5[pp_rand_index])
        # print(pc_data_pp_share)
        return pc_data_pp_share



if __name__ == '__main__':
    key_len = 128
    bound = random.randint(100,1000)


    print('party C step1'.center(50,'='))
    pc = PartyC(key_len=key_len)
    pc_pk_black = pc.get_self_pk_black()

    print('party C step2'.center(50,'='))
    pc_data = {
        'key': ['a', 'c', 'd', 'f'],
        'value':[5,3,1,10]
    }
    pc_data = pd.DataFrame(pc_data)
    pc_df_step2 = pc.partyC_step2(pc_data)

    print('party P step1'.center(50, '='))
    pp = PartyP(key_len=key_len)
    pp_pk_gray = pp.get_self_pk_gray()


    print('party P step2'.center(50, '='))
    pp_data = {
        'key': ['b', 'd', 'c', 'g'],
        'value': [4, 2, 6, 9]
    }
    pp_data = pd.DataFrame(pp_data)
    pp_df_step2 = pp.partyP_step2(pp_data)
    # print([point_2_bytes(item).hex() for item in pp_df_step2['key']])
    # print(pp_df_step1)
    # print(point_2_bytes(pp_df_step2['key'][0]).hex())

    print('party C step3'.center(50, '='))
    # print(point_2_bytes(pp_df_step2['key'][0]).hex())
    pc_df_step3 = pc.partyC_step3(pp_df_step2)
    # print([point_2_bytes(item).hex() for item in pc_df_step3['key']])
    # print(point_2_bytes(pc_df_step3['key'][0]).hex())


    print('party P step3 step4'.center(50, '='))
    # print(point_2_bytes(pc_df_step2['key'][0]).hex())
    pp_df_step3 = pp.partyP_step3_4(pc_df_step2)
    # print([point_2_bytes(item).hex() for item in pp_df_step3['key']])
    # print(point_2_bytes(pp_df_step3['key'][0]).hex())

    print('party P step5'.center(50, '='))
    # pc_pk_black PaillierPublicKey

    # print(pp_rand)
    pp_rand_dict5 = pp.partyP_step5(pp_df_step3,pc_pk_black)
    pp_rand_step5 = list(pp_rand_dict5.keys())
    # print([-(pc.sk_black.decrypt(item) - bound) for item in pp_rand_step5])
    # print(ppd)
    # ppds = restore_with_indices(ppd,pp_rand_index)
    # print(ppds)

    print('party P step6 step7'.center(50, '='))
    # print([pc.sk_black.decrypt(item) for item in pp_df_step3['value']])
    pp_df_step6 = pp.partyP_step6_7(pp_df_step3, pp_rand_step5)
    # print([pc.sk_black.decrypt(item) - bound for item in pp_df_step6['value']])
    pp_df_key_hash = [point_2_bytes(item).hex()for item in pp_df_step6['key']]
    pc_df_key_hash = [point_2_bytes(item).hex()for item in pc_df_step3['key']]
    # for item in pp_df_key_hash:
    #     if item in pc_df_key_hash:
    #         print(f"fuck:{item}")
    # print(pp_df_key_hash)
    # print(pc_df_key_hash)


    print('party C step7'.center(50, '='))
    pp_pc_insec_key,pc_select_step7,pp_index_step7,pc_data_pc_share = pc.partyC_step7(pc_data=pc_df_step3, pp_data=pp_df_step6)
    # print(pc_select_step7)
    # print(pp_index_step7)
    # print(pc_data_pc_share)

    print('party C step8 9'.center(50, '='))
    pp_data_pc_share, pp_data_pp_share_enc = pc.partyC_step8_9(pc_select_step7,pp_pk_gray)
    # print(pp_data_pc_share)
    # print(pp_data_pp_share_enc)
    pp_data_pp_share = pp.partyP_step10(pp_data_pp_share_enc)
    # print(pp_data_pp_share)

    print('party P step11'.center(50, '='))
    pc_data_pp_share = pp.partyP_step11(pp_index_step7, pp_rand_step5, pp_rand_dict5)
    # print(pc_data_pp_share)


    print('result merge'.center(50, '='))
    print("intersection encode key:")
    print(pp_pc_insec_key)
    print("party C share:")
    print(f"pc_data_pc_share:{pc_data_pc_share}")
    print(f"pp_data_pc_share:{pp_data_pc_share}")
    print("party P share:")
    print(f"pp_data_pc_share:{pp_data_pc_share}")
    print(f"pp_data_pp_share:{pp_data_pp_share}")
    print("insec merge")
    print(f"pc insec data:{numpy.array(pc_data_pc_share)+numpy.array(pc_data_pp_share)}")
    print(f"pp indec data:{numpy.array(pp_data_pc_share) + numpy.array(pp_data_pp_share)}")


    pc_final_df = pd.DataFrame({
        'key': pp_pc_insec_key,
        'pc_data_pc_share':pc_data_pc_share,
        'pp_data_pc_share':pp_data_pc_share
    })
    pc_final_df.to_csv('./data/ps3i_partyC_result.csv', index=False)

    pp_final_df = pd.DataFrame({
        'key': pp_pc_insec_key,
        'pc_data_pp_share': pc_data_pp_share,
        'pp_data_pp_share': pp_data_pp_share
    })
    pp_final_df.to_csv('./data/ps3i_partyP_result.csv', index=False)








