

import os


PICKLE_VERSION=3
ABS_PROJECT_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



HASH_MD5 = 'md5'
HASH_SHA1 = 'sha1'
HASH_SHA224 = 'sha224'
HASH_SHA256 = 'sha256'
HASH_SHA384 = 'sha384'
HASH_SHA512 = 'sha512'
HASH_SM3 = 'sm3'
HASH_NONE = 'none'

if __name__ == '__main__':
    pass
    print(ABS_PROJECT_PATH)