

import hashlib
# import libsm3py


from utils.constant_utils import HASH_NONE,HASH_SHA224,HASH_SHA256,HASH_SHA384,HASH_SHA512,HASH_SHA1,HASH_MD5


def compute_md5(value):
    return hashlib.md5(bytes(value, encoding='utf-8')).hexdigest()

def compute_sha256(value):
    return hashlib.sha256(bytes(value, encoding='utf-8')).hexdigest()

def compute_sha1(value):
    return hashlib.sha1(bytes(value, encoding='utf-8')).hexdigest()

def compute_sha224(value):
    return hashlib.sha224(bytes(value, encoding='utf-8')).hexdigest()

def compute_sha512(value):
    return hashlib.sha512(bytes(value, encoding='utf-8')).hexdigest()

def compute_sha384(value):
    return hashlib.md5(bytes(value, encoding='utf-8')).hexdigest()

HASH_CLASS = {
    'none': lambda x = '':str(x),
    HASH_MD5:hashlib.md5,
    HASH_SHA1:hashlib.sha1,
    HASH_SHA512:hashlib.sha512,
    HASH_SHA384:hashlib.sha384,
    HASH_SHA256:hashlib.sha256,
    HASH_SHA224:hashlib.sha224,
}

def get_bits_of_hash_method(method):
    if method == HASH_SHA256:
        return 32*8
    elif method == HASH_MD5:
        return 16*8
    elif method == HASH_SHA1:
        return 20*8
    elif method == HASH_SHA224:
        return 28*8
    elif method == HASH_SHA384:
        return 48*8
    elif method == HASH_SHA512:
        return 64*8
    elif method == 'none':
        return 0

    else:
        return -1

class Hash:
    def __init__(self,method):
        self.method = method
        if self.method not in HASH_CLASS:
            raise ValueError("Hash does not support method:{}".format(method))

        self.bits = get_bits_of_hash_method(method)
        self.hash_op = HASH_CLASS[self.method]

        self._data = HASH_CLASS[self.method]()

    def compute_with_salt(self,value,suffix_salt=None, decode=True):
        if suffix_salt is None:
            return self.compute(value)

        if isinstance(value,(bytes,bytearray)):
            raise ValueError("if need add salt, value should not be bytes")

        value = str(value)
        value = value+suffix_salt
        return self.compute(value,decode=True)
        pass

    def compute(self,value,decode=True):
        if isinstance(value, str):
            value = bytes(value, encoding='utf-8')

        if not isinstance(value,(bytes,bytearray)):
            raise TypeError("value must be str or bytes")

        value = self.hash_op(value)

        if not decode:
            if self.method == "none":
                return value
            else:
                return value.digest()

        if self.method == "none":
            return value

        return value.hexdigest()


    def update(self,value):
        if isinstance(value, str):
            value = bytes(value, encoding='utf-8')

        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("value must be str or bytes")

        self._data.update(value)
        pass

    def get_hash_code(self):
        if self.method == "none":
            return self._data
        return self._data.hexdigest()
        pass

if __name__ == '__main__':
    pass