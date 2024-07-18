import math
import time
from SetEcc import *
import sys
import hmac, hashlib
from ECCMainWork import *
import random

def sign(r): # 随机数加上公钥
    # 公钥和随机数序列化相加，取哈希值
    cbytes = hashlib.sha256(pubbytes+Rbytes).digest()
    # bytes类型转换为十进制
    ct = int.from_bytes(cbytes, 'big')
    l = math.floor(math.log10(ct)) + 1
    c=0
    while ct > 0:
        c = c + ct % 10
        ct //= 10  # 去掉数字的个位

    z = r+c*sk
    Z=z*G
    x=Z.point[0]
    y=Z.point[1]
    X=int(sha256(str(x).encode()).hexdigest(), 16)
    Y=int(sha256(str(y).encode()).hexdigest(), 16)
    zplus=(X,Y)

    return zplus


def Genverify(R):
    cbytes = hashlib.sha256(pubbytes + Rbytes).digest()
    ct = int.from_bytes(cbytes, 'big')
    c = 0
    while ct > 0:
        c = c + ct % 10
        ct //= 10  # 去掉数字的个位
    vp=R + c * pk
    vx=vp.point[0]
    vy=vp.point[1]
    vxplus=int(sha256(str(vx).encode()).hexdigest(), 16)
    vyplus=int(sha256(str(vy).encode()).hexdigest(), 16)
    verify = (vxplus,vyplus)
  #  print("z:", z)
  #  print("c:", c)
    return verify
def verify(V1,V2):
    if V1[0] == V2[0] and V1[1] == V2[1]:
        return 1
    else:
        return 0



if __name__ == '__main__':
    a = 162
    b = 365
    p = 823
    # 162, 365, 823
    ellip = ECC(a, b, p)
    G,n = genGN(ellip)
    sk = ElgamlPrivkeyA(n)  # 私钥
    pk = ElgamalPubkey(G, sk)  # 公钥 代理使用
    start_time = time.time()
    r = random.randint(1, 1000)
    print("随机数:", r)
    R = r * G
    # 公钥序列化
    pubbytes = point_to_ser(pk, False)
    # 随机数序列化
    Rbytes = point_to_ser(R, False)
    print("生成元:",G)
    print("椭圆阶数:",n)
   #  print("sk:",sk)
   #  print("pk:",pk)
    V1=sign(r)
    print("身份证明：", V1)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time} 秒")
    # start_time = time.time()
    V2=Genverify(R)
    result = verify(V1,V2)
    print("验证：",V2)
    print("验证结果：",result)
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")