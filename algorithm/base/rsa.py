import rsa
from rsa import PublicKey
import gmpy2

def make_rsa(len= 512):
    (pubkey, privkey) = rsa.newkeys(512)
    return pubkey, privkey



if __name__ == '__main__':
    pass