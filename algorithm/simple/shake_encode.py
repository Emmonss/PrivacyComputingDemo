from Crypto.Hash import SHAKE256



def encrypt(secret:bytes, plaintext:bytes):
    shake = SHAKE256.new(secret)
    key = shake.read(len(plaintext))

    int_key = int.from_bytes(key,'big')
    int_pt = int.from_bytes(plaintext, 'big')

    int_ct = int_key ^ int_pt
    return int_ct.to_bytes(len(plaintext), "big")


def decrypt(secret:bytes, ciphertext:bytes):
    shake = SHAKE256.new(secret)

    key = shake.read(len(ciphertext))
    int_key = int.from_bytes(key, 'big')
    int_pt = int.from_bytes(ciphertext, 'big')

    int_ct = int_key ^ int_pt
    return int_ct.to_bytes(len(ciphertext), "big")


if __name__ == '__main__':
    msg = "fuker msg"
    key = "fucker key"
    fkey = "faker key"
    msgb = msg.encode('utf-8')
    keyb = key.encode('utf-8')
    print(f"msg{msg}:bytes:{msgb}")
    print(f"msg{key}:bytes:{keyb}")

    cipher = encrypt(keyb,msgb)
    print(f"cipher{cipher}")

    decoder = decrypt(keyb, cipher)
    print(f"cipher{decoder};plain:{decoder.decode('utf-8')}")

    faker_decoder = decrypt(fkey.encode('utf-8'), cipher)
    print(f"cipher{faker_decoder};")

