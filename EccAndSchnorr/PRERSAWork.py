
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
import base64
import time

# 1) 系统初始化
# 2) 请求公私钥对
def generate_rsa_keypair():
    key = RSA.generate(2048)
    return key, key.publickey()

# KGC生成Alice和Bob的公私钥对
alice_key, alice_pub_key = generate_rsa_keypair()
bob_key, bob_pub_key = generate_rsa_keypair()
aes_key = get_random_bytes(16)
# 3) Alice生成密文文件
def encrypt_data(data, rsa_public_key):
    # 使用AES加密数据
    cipher_aes = AES.new(aes_key, AES.MODE_EAX)
    nonce = cipher_aes.nonce  # 保存nonce值用于解密
    print(aes_key)
    print(nonce)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode())

    # 使用Alice的公钥加密AES密钥
    cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
    encrypted_nonce = cipher_rsa.encrypt(nonce)

    return base64.b64encode(ciphertext).decode(), base64.b64encode(encrypted_nonce).decode()


# 4) 构建重加密密钥
def generate_re_encryption_key(sender_private_key, receiver_public_key):
    # 生成重加密密钥
    return sender_private_key, receiver_public_key



# 5) 代理重加密
def re_encrypt(c2, re_encryption_key):
    # 解密得到AES密钥
    cipher_rsa = PKCS1_OAEP.new(re_encryption_key[0])
    aes_key = cipher_rsa.decrypt(base64.b64decode(c2))

    # 使用Bob的公钥重新加密AES密钥
    cipher_rsa = PKCS1_OAEP.new(re_encryption_key[1])
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)

    return base64.b64encode(encrypted_aes_key).decode()



# 6) Bob请求数据
def decrypt_data(c1, c3, rsa_private_key):
    # 使用Bob的私钥解密得到AES密钥
    cipher_rsa = PKCS1_OAEP.new(rsa_private_key)
    nonce = cipher_rsa.decrypt(base64.b64decode(c3))
    print(nonce)

    # 使用AES密钥和nonce解密数据
    cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
    decrypted_data = cipher_aes.decrypt(base64.b64decode(c1))
    return decrypted_data.decode()

if __name__ == '__main__':
    # 加密和生成重加密的密钥
    # start_time = time.time()
    data = "0,0,{123,address:to the moon,name: luv,id:3125190099072}"
    c1, c2 = encrypt_data(data, alice_pub_key)
    print("加密的密文：",c1)
    print("加密的nonce：",c2)
    re_encryption_key = generate_re_encryption_key(alice_key, bob_pub_key)
    print("重加密的密钥：",re_encryption_key)
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")
    # 代理重加密
    # start_time = time.time()
    c3 = re_encrypt(c2, re_encryption_key)
    print("重新加密的nonce：",c3)
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")
    # 解密
    start_time = time.time()
    decrypted_data = decrypt_data(c1, c3, bob_key)
    print("解密后的数据:", decrypted_data)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time} 秒")

