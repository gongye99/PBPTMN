from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii
import time
def gunASEkey():
    # 随机生成密钥
    key = get_random_bytes(16)  # AES-128位密钥
    return key

# 初始化加密器
def encryptASE(data,key,nonce=None):
    cipher_encrypt = AES.new(key, AES.MODE_EAX,nonce=nonce)
    nonce = cipher_encrypt.nonce

    # 加密数据
    # data = "[(18, 34), (59, 390)]"
    ciphertext, tag = cipher_encrypt.encrypt_and_digest(data.encode())

    # 打印加密后的数据
    print("Ciphertext:", binascii.hexlify(ciphertext))
    return ciphertext,tag,nonce

def decryptASE(ciphertext,tag,nonce,key):
    # 初始化解密器
    cipher_decrypt = AES.new(key, AES.MODE_EAX, nonce=nonce)

    # 解密数据
    decrypted_data = cipher_decrypt.decrypt_and_verify(ciphertext, tag)

    # 打印解密后的数据
    print("Decrypted Data:", decrypted_data.decode())
    return decrypted_data

if __name__ == '__main__':
    start_time = time.time()
    key = gunASEkey()
    data = '123,address:to the moon,name: luv,id:3125190099072,1'
    ciphertext1,tag1,nonce1 = encryptASE(data,key)
    nonce1_hex = nonce1.hex()
    print(nonce1.hex())
    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time} 秒")
    # start_time = time.time()
    nonce1_origin = bytes.fromhex(nonce1_hex)
    ciphertext2,tag2,nonce2 = encryptASE(data,key,nonce1_origin)
    if ciphertext1 == ciphertext2 :
        print("pass")
    else:
        print("fail")
    # decryptASE(ciphertext1,tag,nonce,key)
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")