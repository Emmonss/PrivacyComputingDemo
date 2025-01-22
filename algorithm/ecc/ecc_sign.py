from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

# 生成ECC密钥对
key = ECC.generate(curve='P-256')

# 待签名内容(发送的文本内容)
message = 'I am MKing Hello Everyone'

# 签名
signer = DSS.new(key, 'fips-186-3')
hasher = SHA256.new(message.encode())  # Hash对象，取内容摘要
# hasher.update(message.encode()) # 换种方式使用也可以
sign_obj = signer.sign(hasher)  # 用私钥对消息签名

print('签名内容：', sign_obj)

# 将签名写入文件，模拟发送（同时还发送了文本内容，为了方便，不写文件，后面直接引用）
with open('sign.bin', 'wb') as f:
    f.write(sign_obj)

# 读取签名内容，模拟接收
with open('sign.bin', 'rb') as f:
    sign_new = bytearray(f.read())  # 签名内容(二进制)，并转成bytearray，以便修改

# sign_new.append(0x32)  # 模拟错误的签名
print('收到签名：', sign_new)

# 验证签名
verifer = DSS.new(key.public_key(), 'fips-186-3')  # 使用公钥创建校验对象
hasher = SHA256.new(message.encode())  # 对收到的消息文本提取摘要

try:
    verifer.verify(hasher, sign_new)  # 校验摘要（本来的样子）和收到并解密的签名是否一致
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")