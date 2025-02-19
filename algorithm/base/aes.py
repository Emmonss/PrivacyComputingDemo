from Crypto.Cipher import AES
from utils.conversion import int_to_bytes,bytes_to_int
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import struct


def generate_aes_key(key_length=16):
    key = get_random_bytes(key_length)
    return key

def aes_encrypt_int(data, key):
    # 将整数转换为字节（8字节）
    data_bytes = struct.pack('>Q', data)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data_bytes, AES.block_size))
    return encrypted_data

def aes_decrypt_int(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # 将字节转换回整数
    return struct.unpack('>Q', decrypted_data)[0]

def aes_encrypt_bytes(data, key):
    # 使用随机生成的初始化向量（IV）
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    # 返回IV和加密数据
    return iv + encrypted_data

def aes_decrypt_bytes(encrypted_data, key):
    # 提取IV
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data


def aes_encrypt_str(data, key):
    # 将字符串编码为字节
    data_bytes = data.encode('utf-8')
    # 使用随机生成的初始化向量（IV）
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data_bytes, AES.block_size))
    # 返回IV和加密数据
    return iv + encrypted_data

def aes_decrypt_str(encrypted_data, key):
    # 提取IV
    iv = encrypted_data[:AES.block_size]
    encrypted_data = encrypted_data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    # 将字节解码为字符串
    return decrypted_data.decode('utf-8')


if __name__ == '__main__':
    # 密钥必须是16, 24, 或 32字节
    # key = b'16bytekey1234567'
    key = generate_aes_key(32)
    print(key)
    # # 示例整数
    data = 12345678
    #
    # # 加密
    # encrypted = encrypt_int(data, key)
    # print(f"Encrypted: {encrypted}")
    #
    # encrypted2 = encrypt_bytes(encrypted, key)
    # print(f"Encrypted: {encrypted2}")
    #
    # # 解密
    # decrypted2 = decrypt_bytes(encrypted2, key)
    # print(f"Decrypted: {encrypted2}")
    #
    # decrypted = decrypt_int(decrypted2, key)
    # print(f"Decrypted: {decrypted}")

    # data = "fuck you"

    # # 加密
    # encrypted = aes_encrypt_str(data, key)
    # print(f"Encrypted: {encrypted}")
    #
    # encrypted2 = aes_encrypt_bytes(encrypted, key)
    # print(f"Encrypted: {encrypted2}")
    #
    # # 解密
    # decrypted2 = aes_decrypt_bytes(encrypted2, key)
    # print(f"Decrypted: {encrypted2}")
    #
    # decrypted = aes_decrypt_str(decrypted2, key)
    # print(f"Decrypted: {decrypted}")
    #
    key1 = generate_aes_key(32)
    print(f"key1: {key1}")

    key2 = generate_aes_key(32)
    print(f"key2: {key2}")

    p11 = aes_encrypt_int(data,key1)
    print(f"p11: {p11}")
    p21 = aes_encrypt_int(data,key2)
    print(f"p21: {p21}")

    p12 = aes_encrypt_bytes(p11, key2)
    print(f"p12: {p12}")
    p22 = aes_encrypt_bytes(p21, key1)
    print(f"p21: {p22}")