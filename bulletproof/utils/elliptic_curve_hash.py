from fastecdsa.point import Point
from fastecdsa.curve import Curve
from fastecdsa.util import mod_sqrt
from hashlib import sha256, md5

# 根据输入的msg和椭圆曲线参数CURVE，通过不断增加i的值，计算满足特定条件的椭圆曲线上的点，并返回该点
def elliptic_hash(msg: bytes, CURVE: Curve):
    p = CURVE.p
    i = 0
    while True:
        # 无限循环，控制循环可以进行的条件是x>=p
        i += 1
        # 将整数i转换为字节串，并与msg拼接，得到一个新的字节串prefixed_msg
        # str.encode用于将 str 类型转换成 bytes 类型
        prefixed_msg = str(i).encode() + msg
        # 使用SHA-256哈希算法对prefixed_msg进行哈希计算，得到一个哈希值h
        h = sha256(prefixed_msg).hexdigest()
        # 将哈希值h转换为一个整数x，将16进制转换为10进制表示。利用随机数来生成一个x
        x = int(h, 16)
        if x >= p:
            continue
        # 计算椭圆曲线上的y坐标的平方，其中CURVE.a和CURVE.b是椭圆曲线的参数。
        y_sq = (x ** 3 + CURVE.a * x + CURVE.b) % p
        # 计算y_sq的模p的平方根，返回一个列表，取第一个元素作为y的值。
        y = mod_sqrt(y_sq, p)[0]
        # 检查点(x, y)是否在椭圆曲线上。
        if CURVE.is_point_on_curve((x, y)):
            # 对prefixed_msg进行MD5哈希计算，得到一个哈希值，将其转换为整数，并对2取模，得到一个二进制值b
            b = int(md5(prefixed_msg).hexdigest(), 16) % 2
            # 如果b为真，则返回点(x, y)，否则返回点(x, p - y)。这里使用Point类创建一个椭圆曲线上的点对象，并将其返回。
            return Point(x, y, CURVE) if b else Point(x, p - y, CURVE)

