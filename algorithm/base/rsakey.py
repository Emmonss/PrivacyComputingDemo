import rsa
from utils.conversion import int_to_bytes,bytes_to_int

def make_rsa(len= 512):
    (pubkey, privkey) = rsa.newkeys(512)
    return pubkey, privkey



if __name__ == '__main__':
    d = 12
    dd = int_to_bytes(d)
    print(dd)
    print(len(dd))
    # print(dd)
    # pubkey, privkey = make_rsa(8)
    #
    # pubkey2, privkey2 = make_rsa(128)
    # ci = rsa.encrypt(dd,pubkey)
    # print(ci)
    # print(bytes_to_int(ci))
    #
    # ci2 = rsa.encrypt(ci,pubkey2)
    # print(ci2)
    # print(bytes_to_int(ci2))
    #
    # pl = rsa.decrypt(ci,privkey)
    # print(pl)
    # ddd = bytes_to_int(pl)
    # print(ddd)
    #
