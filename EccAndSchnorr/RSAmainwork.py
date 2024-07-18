import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import time

def hash_data(data):
    # 创建一个sha256哈希对象
    hash_object = hashlib.sha256()
    # 提供要哈希的数据，必须是字节串
    hash_object.update(data.encode())
    # 获取哈希值的十六进制表示
    hash_hex = hash_object.hexdigest()
    return hash_hex
# 生成RSA密钥对
def genkey():
    key = RSA.generate(2048)
    return key, key.publickey()

# 加密
def encrypt(public_key, message):
    # 需要从公钥字节串转换为RSA对象
    cipher_rsa_encrypt = PKCS1_OAEP.new(public_key)
    encrypted_message = cipher_rsa_encrypt.encrypt(message.encode())
    print("加密后的消息:", binascii.hexlify(encrypted_message))
    return encrypted_message

# 解密
def decrypt(private_key, encrypted_message):
    # 需要从私钥字节串转换为RSA对象
    cipher_rsa_decrypt = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa_decrypt.decrypt(encrypted_message)
    print("解密后的消息:", decrypted_message.decode())
    return decrypted_message.decode()

if __name__ == '__main__':
    message = '123,address:to the moon,name: luv,id:3125190099072,1'
    key_C, pub_key_C = genkey()
    # A用自己的公钥加密
    start_time = time.time()
    message_hash = hash_data(message)
    encrypted_message1 = encrypt(pub_key_C, message_hash)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time} 秒")
    # B用自己的公钥加密
    message_hash = hash_data(message)
    encrypted_message2 = encrypt(pub_key_C, message_hash)
    # C尝试用私钥解密
    # start_time = time.time()
    decrypted_message1 = decrypt(key_C, encrypted_message1)
    decrypted_message2 = decrypt(key_C, encrypted_message2)
    # 将解密后的字符串再次加密（应该用B的公钥加密，但直接比较加密后的结果可能不等因为加密操作包含随机性）
    # 因此，我们验证A是否能成功解密自己加密的消息
    if decrypted_message1 == decrypted_message2:
        print("pass")
    else:
        print("fail")
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")