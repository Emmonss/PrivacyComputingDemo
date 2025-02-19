
import random
from Crypto.PublicKey import ECC
import pandas as pd
from algorithm.ecc.ecc_utils import generate_key,key_2_bytes,point_2_bytes,point_2_bytes2
from algorithm.simple.gmpy_math import mpz
from pprint import pprint


ran_seed = 12
curve="ed25519"

sin = None
class PartyC:
    def __init__(self):
        self.sk_blue,self.pk_blue = generate_key()
        self.sk_black,self.pk_black = generate_key()


    def partyC_step1(self,data,key='key'):
        #shuffle
        shuffle_data = data.sample(frac=1, random_state=ran_seed).reset_index(drop=True)
        encode_data = []
        for item in shuffle_data[key]:
            encode_data.append(mpz(item)*self.pk_blue.pointQ)
        return list(shuffle_data[key]),encode_data

    def partyC_step2(self,data):
        encode_data = []
        encode_data_black = []
        for item in data:
            encode_data.append(item*self.sk_blue.d)

        for item in encode_data:
            encode_data_black.append(item*self.sk_black.d)
        return encode_data,encode_data_black

    def partyC_step_4_5(self, pc_data, pp_data,key='key'):
        pc_data_dict = {}
        for item in pc_data:
            pc_data_dict[point_2_bytes(item)] = item

        pp_data_dict = {}
        for item in pp_data:
            pp_data_dict[point_2_bytes(item)] = item
        pc_noinsec_bt = set(pc_data_dict.keys()) - set(pp_data_dict.keys())
        pp_noinsec_bt = set(pp_data_dict.keys()) - set(pc_data_dict.keys())

        pc_noinsec_data = []
        for item in pc_noinsec_bt:
            pc_noinsec_data.append(pc_data_dict[item] * self.sk_black.d)

        pp_noinsec_data = []
        for item in pp_noinsec_bt:
            pp_noinsec_data.append(pp_data_dict[item] * self.sk_black.d)


        return pc_noinsec_data,pp_noinsec_data

    def partyC_step8(self, data):
        return [point_2_bytes(item * self.sk_black.d).hex() for item in data]


    def merge_final(self,init_shuf_data, self_enc_data, insec_data):
        for _ in insec_data:
            init_shuf_data.append(None)
        # init_shuf_data = []
        self_enc_data.extend(insec_data)
        res = pd.DataFrame({
            'enc_key':self_enc_data,
            'key':init_shuf_data
        })

        res = res.astype({'enc_key': 'str', 'key': 'Int64'})
        return res

class PartyP:
    def __init__(self,n=32):
        self.sk_red,self.pk_red = generate_key()
        self.sk_gray,self.pk_gray = generate_key()


    def partyP_step1(self,data,key='key'):
        #shuffle
        shuffle_data = data.sample(frac=1, random_state=ran_seed).reset_index(drop=True)
        encode_data = []
        for index,item in enumerate(shuffle_data[key]):
            encode_data.append(mpz(item)*self.pk_red.pointQ)
        return list(shuffle_data[key]),encode_data

    def partyP_step2(self,data):
        encode_data = []
        encode_data_black = []
        for item in data:
            encode_data.append(item*self.sk_red.d)

        for item in encode_data:
            encode_data_black.append(item*self.sk_gray.d)
        return encode_data,encode_data_black

    def partyP_step3(self, data):
        random.seed(ran_seed)
        shuffled_list = data[:]
        random.shuffle(shuffled_list)
        return shuffled_list

    def partyP_step6_7(self, pc_noinsec_data, pp_noinsec_data):
        return [point_2_bytes(item * self.sk_gray.d).hex() for item in pc_noinsec_data], \
               [point_2_bytes(item * self.sk_gray.d).hex() for item in pp_noinsec_data]

    def partyP_step8(self, data):
        return [point_2_bytes(item * self.sk_gray.d).hex() for item in data]


    def merge_final(self,init_shuf_data, self_enc_data, insec_data):
        for _ in insec_data:
            init_shuf_data.append(None)
        self_enc_data.extend(insec_data)
        res = pd.DataFrame({
            'enc_key':self_enc_data,
            'key':init_shuf_data
        })
        res = res.astype({'enc_key': 'str', 'key': 'Int64'})
        return res

def main_private_protocol(pc_data,pp_data):
    pass
if __name__ == '__main__':
    n = 16
    print('party C step1'.center(50,'='))
    pc = PartyC()
    pc_data = {'key':[2,3,7,10]}
    pc_data = pd.DataFrame(pc_data)
    pc_shuffle_data, pc_data_step1 = pc.partyC_step1(pc_data)
    print(f"pc_shuffle_data:{pc_shuffle_data}")
    # print(pc_data_step1)

    print('party P step1'.center(50, '='))
    pp = PartyP()
    pp_data = {'key':[3,7,5,2]}
    pp_data = pd.DataFrame(pp_data)
    pp_shuffle_data,pp_data_step1 = pp.partyP_step1(pp_data)
    print(f"pp_shuffle_data:{pp_shuffle_data}")
    # print(pp_data_step1)

    print('party C step2'.center(50, '='))
    # pp_data_step1 send to pc
    pc_data_step2,pc_data_step2_black = pc.partyC_step2(pp_data_step1)
    # print(pc_data_step2)
    # print(pc_data_step2_black)

    #
    print('partyP step2'.center(50, '='))
    # pp_data_step1 send to pc
    pp_data_step2, pp_data_step2_gray = pp.partyP_step2(pc_data_step1)
    # print(pp_data_step2)
    # print(pp_data_step2_gray)
    #
    print('partyP step3'.center(50, '='))
    # pp_data_step1 send to pc
    pp_data_step2_shuffle = pp.partyP_step3(pp_data_step2)
    # print(pp_data_step2_shuffle)
    #
    # print('partyC step4 step5'.center(50, '='))
    pc_noinsec_data,pp_noinsec_data = pc.partyC_step_4_5(pc_data=pc_data_step2, pp_data=pp_data_step2_shuffle)
    # print(pc_noinsec_data)
    # print(pp_noinsec_data)
    # print(point_2_bytes2(pc_noinsec_data[0]))
    # print(point_2_bytes2(pp_noinsec_data[0]))
    #
    print('partyP step6 step7'.center(50, '='))
    pc_noinsec_data_final, pp_noinsec_data_final = pp.partyP_step6_7(pc_noinsec_data, pp_noinsec_data)
    # print(pc_noinsec_data_final)
    # print(pp_noinsec_data_final)

    print('partyC step8'.center(50, '='))
    #shuffle again
    pc_data_final = pc.partyC_step8(pp_data_step2_gray)
    # print(pc_data_final)
    # print(pc_shuffle_data)
    print('partP step8'.center(50, '='))
    pp_data_final = pp.partyP_step8(pc_data_step2_black)
    # print(pp_data_final)
    # print(pp_shuffle_data)
    # print(pp_data_final)

    print('partC merge self and insec data'.center(50, '='))
    pc_data_final_df = pc.merge_final(pc_shuffle_data,pc_data_final,pc_noinsec_data_final)
    # print(pc_data_final_df)
    pc_data_final_df.to_csv('./data/pc_data_test.csv',index=False)

    print('partP merge self and insec data'.center(50, '='))
    pp_data_final_df = pp.merge_final(pp_shuffle_data, pp_data_final, pp_noinsec_data_final)
    # print(pp_data_final)
    pp_data_final_df.to_csv('./data/pp_data_test.csv',index=False)

    #
