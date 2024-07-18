import random

from EccAndSchnorr.ECCnetwork import load_model_and_generate_curves
from EccAndSchnorr.ModFuction import get_inverse_element, gcd
from EccAndSchnorr.SetEcc import ECC

def genGN():
   # ellip = ECC(generate_ECC()[0],generate_ECC()[1],generate_ECC()[2])
   generated_curves = load_model_and_generate_curves('elliptic_curve_model.h5', 1)
   ellip = ECC(generated_curves(0),generated_curves(1),generated_curves(2))
   G = ellip.genG()
   (x, y) = G.point
   n = get_order(x, y, list[0],list[2])
   return G,n
def CalculateR(x1, y1, x2, y2, a, p):    #  椭圆同态加密算法
    """
        计算p+q
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
    计算椭圆曲线的阶
    """
    # 计算-p
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    while True:
        n += 1
        p_value = CalculateR(temp_x, temp_y, x0, y0, a, p)
        if p_value[0] == x1 and p_value[1] == y1:
            print("==========该椭圆曲线的阶为%d=========" % (n + 1))
            return n + 1

        temp_x = p_value[0]
        temp_y = p_value[1]
