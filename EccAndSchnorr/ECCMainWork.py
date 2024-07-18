import ast
from hashlib import sha256
import time
import numpy as np

# from ECCnetwork import load_model_and_generate_curves
from EccAndSchnorr.AESmainwork import *
from SetEcc import ECC
from ModFuction import *
import random


def CalculateR(x1, y1, x2, y2, a, p):
    """
        计算p+q   计算两点相加的结果，并返回新点的坐标
        """
    flag = 1  # 定义符号位
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 计算分子
        denominator = 2 * y1  # 计算分母
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value =gcd(member, denominator)
    member = int(member / gcd_value)
    denominator = int(denominator / gcd_value)
    # 求分母的逆元
    inverse_value = get_inverse_element(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # 计算x3,y3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    # print("%d<=====>%d" % (x3, y3))
    return [x3, y3]

def get_order(x0, y0, a, p):
    """
    计算椭圆曲线的阶  阶是椭圆曲线上点的数量
    """
    # 计算-p
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    p_value_tmp = None
    while True:
        n += 1
        if n % 2 == 1:
            p_value_tmp = p_value
        p_value = CalculateR(temp_x, temp_y, x0, y0, a, p)

        if p_value == p_value_tmp:
            return 0

        if p_value[0] == x1 and p_value[1] == y1:
            print("==========该椭圆曲线的阶为%d=========" % (n + 1))
            return n + 1

        temp_x = p_value[0]
        temp_y = p_value[1]

def genGN(ellip):
    G = ellip.genG()
    # print(G)
    (x, y) = G.point
    n = get_order(x, y, ellip.a, ellip.p)
    if n == 0:
        return genGN()
    else:
        return G,n

def ElgamlPrivkeyA(n):
    # A的私钥
    k = random.randint(1, int(n))
    return k

def ElgamalPubkey(G,k):
    PA = k*G
    return PA

def encrypt(PM,G,PA):
    # Bob 选择随机数 k, 对消息 PM 进行加密得到密文
    # Bob 发送密文 C = [(676, 558), (385, 328)]
    r = random.randint(1, 1000)
    C = [r * G, PM + r * PA]
    return (C)

def decrypt(C,k):
    c1=C[0]
    c2=C[1]
    mk=c2-k*c1
    print("解密后的信息为：",mk)
    return mk

def HidenMessage(msg,curve):
    adjustment = 0  # 调整次数
    p = curve.p
    x = msg % p
    circle = msg // p
    while True:
        rhs = x ** 3 + curve.a * x + curve.b
        # y是不是p的平方剩余，若y是，则求出y的值，有一对
        y = mod_sqrt(rhs, p)
        if y is not None:
            m=curve.point(x,y)
            return m, adjustment,circle
        x += 1
        adjustment += 1
def legendre_symbol(a, p):
    """ 计算勒让德符号 (a/p) """
    return pow(a, (p - 1) // 2, p)

def mod_sqrt(a, p):
    """ 计算模 p 下的平方根，假设 p 是素数 """
    if legendre_symbol(a, p) != 1:
        return None  # 如果 a 不是平方剩余，则不存在平方根

    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Tonelli-Shanks 算法
    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
            if i == m:
                return None
        b = pow(c, 2 ** (m - i - 1), p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = pow(b, 2, p)
        m = i
    return r
# def ActualMessage(m,G,n):
#     i=0
#     while True:
#         i=i+1
#         if double_and_add(G, i, n, G).point == m.point:
#             return i
def ActualMessage(m,adjustment,circle):
    (x,y)=m.point
    original_integer = x - adjustment + p * circle
    return original_integer

if __name__ == '__main__':
    # generated_curves = load_model_and_generate_curves('elliptic_curve_model.keras', 1)
    # print(generated_curves)
    # a, b, p = generated_curves[0]
    a = 162
    b = 365
    p = 823
    # 162, 365, 823
    ellip = ECC(a, b, p)
    G,n=genGN(ellip)
    print("存款：519")
    # start_time = time.time()
    PM1,adjustment,circle=HidenMessage(519,ellip)
    print("存取信息嵌入椭圆曲线表示为：存款",PM1)
    print("辅助数字为：",adjustment,circle)
    # ASE加密
    keyASE = gunASEkey()
    KA = ElgamlPrivkeyA(n)
    PubK = ElgamalPubkey(G, KA)
    C1 = encrypt(PM1, G, PubK)
    print("存款：",C1)
    # C1Str = str(C1)+","+str(adjustment)+","+str(circle)
    # print(C1Str)
    C1Str = str(C1)
    ciphertext, tag, nonce = encryptASE(C1Str, keyASE)
    # end_time = time.time()
    # run_time = end_time - start_time
    # print(f"程序运行时间：{run_time} 秒")
    start_time = time.time()
    C1repStr = decryptASE(ciphertext,tag,nonce,keyASE)
    print(C1repStr)
    # 将字节串转换为字符串
    C1repStrr = C1repStr.decode('utf-8')
    # 将字符串安全地转换为Python表达式（在这种情况下是列表）
    points_tuples = ast.literal_eval(str(C1repStrr))
    # points = [ellip.point(p) for p in points_tuples]
    point1 = ellip.point(points_tuples[0][0],points_tuples[0][1])
    point2 = ellip.point(points_tuples[1][0],points_tuples[1][1])
    points = [point1,point2]
    print(points)
    DM = decrypt(points, KA)
    message = ActualMessage(DM, adjustment,circle)
    print("存款信息的明文为：",message)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"程序运行时间：{run_time} 秒")



