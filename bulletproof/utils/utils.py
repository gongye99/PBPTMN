"""Contains various utilities"""

from hashlib import sha256
from typing import List
import base64

from fastecdsa.point import Point
from fastecdsa.curve import secp256k1
from fastecdsa.util import mod_sqrt

CURVE = secp256k1
BYTE_LENGTH = CURVE.q.bit_length() // 8


def egcd(a, b):
    """Extended euclid algorithm"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


class ModP:
    """Class representing an integer mod p"""

    def __init__(self, x, p):
        self.x = x
        self.p = p

    def __add__(self, y):
        if isinstance(y, int):
            return ModP(self.x + y, self.p)
        assert self.p == y.p
        return ModP((self.x + y.x) % self.p, self.p)

    def __radd__(self, y):
        return self + y

    def __mul__(self, y):
        if isinstance(y, int):
            return ModP(self.x * y, self.p)
        if isinstance(y, Point):
            return self.x * y
        assert self.p == y.p
        return ModP((self.x * y.x) % self.p, self.p)

    def __sub__(self, y):
        if isinstance(y, int):
            return ModP((self.x - y) % self.p, self.p)
        assert self.p == y.p
        return ModP((self.x - y.x) % self.p, self.p)

    def __rsub__(self, y):
        return -(self - y)

    def __pow__(self, n):
        return ModP(pow(self.x, n, self.p), self.p)

    def __mod__(self, other):
        return self.x % other

    def __neg__(self):
        return ModP(self.p - self.x, self.p)

    def inv(self):
        """Returns the modular inverse"""
        g, a, _ = egcd(self.x, self.p)
        if g != 1:
            raise Exception("modular inverse does not exist")
        else:
            return ModP(a % self.p, self.p)

    def __eq__(self, y):
        return (self.p == y.p) and (self.x % self.p == y.x % self.p)

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return str(self.x)


def mod_hash(msg: bytes, p: int, non_zero: bool = True) -> ModP:
    """Takes a message and a prime and returns a hash in ModP
    进行哈希变换且规定哈希变换后的值的范围"""
    i = 0
    while True:
        i += 1
        prefixed_msg = str(i).encode() + msg
        h = sha256(prefixed_msg).hexdigest()
        # 将哈希值h转换为一个整数x，使用16进制表示。利用随机数来生成一个x
        # 并将其限制在0到2 ** p.bit_length()之间。
        """% 2 ** p.bit_length()：这部分代码对转换后的整数进行取模运算。
        p.bit_length()返回了变量p的二进制表示的位数。
        2 ** p.bit_length()表示2的p的位数次方。
        通过对转换后的整数进行取模运算，可以确保x的值在0到2 ** p.bit_length()之间。
        int(h,16)将16进制转换为10进制"""
        x = int(h, 16) % 2 ** p.bit_length()
        if x >= p:
            continue
        elif non_zero and x == 0:
            continue
        else:
            return ModP(x, p)


def point_to_bytes(g: Point) -> bytes:
    """Takes an EC point and returns the compressed bytes representation"""
    # 检查输入的点g是否等于椭圆曲线的单位元素（即无穷远点）。如果是，则返回字节串b"\x00"，表示压缩表示为0。
    if g == Point.IDENTITY_ELEMENT:
        return b"\x00"
    # 这行代码将点g的x坐标转换为字节串表示,to_bytes()方法将整数转换为指定字节长度的字节串。
    # BYTE_LENGTH是一个常量，表示字节长度。
    x_enc = g.x.to_bytes(BYTE_LENGTH, "big")
    # 根据点g的y坐标的奇偶性选择一个前缀字节。如果g.y是奇数，则前缀字节为b"\x03"，否则为b"\x02"
    prefix = b"\x03" if g.y % 2 else b"\x02"
    return prefix + x_enc


def point_to_b64(g: Point) -> bytes:
    """Takes an EC point and returns the base64 compressed bytes representation"""
    return base64.b64encode(point_to_bytes(g))


def b64_to_point(s: bytes) -> Point:
    """Takes a base64 compressed bytes representation and returns the corresponding point"""
    return bytes_to_point(base64.b64decode(s))


def bytes_to_point(b: bytes) -> Point:
    """Takes a compressed bytes representation and returns the corresponding point"""
    # 如果是0，则表示对应的点是椭圆曲线的单位元素（无穷远点），因此返回Point.IDENTITY_ELEMENT，即椭圆曲线的单位元素。
    if b == 0:
        return Point.IDENTITY_ELEMENT
    # 这行代码将椭圆曲线的素数模数赋值给变量p。
    p = CURVE.p
    # 将压缩字节表示b的第一个字节赋值给变量yp，将剩余的字节赋值给变量x_enc。
    yp, x_enc = b[0], b[1:]
    # 根据yp的值来确定y坐标的奇偶性。如果yp等于2，则表示y坐标是偶数，因此将yp赋值为0；
    # 否则，表示y坐标是奇数，将yp赋值为1。
    yp = 0 if yp == 2 else 1
    # 将字节串x_enc转换为一个整数x。from_bytes()方法将字节串转换为整数，参数"big"表示使用大端字节序。
    x = int.from_bytes(x_enc, "big")
    # 计算椭圆曲线上的y坐标
    y = mod_sqrt((x ** 3 + CURVE.a * x + CURVE.b) % p, p)[0]
    # 检查计算得到的y坐标的奇偶性是否与之前确定的yp相同。
    # 如果相同，则表示y坐标是偶数，返回点(x, y)；
    # 否则，表示y坐标是奇数，返回点(x, p - y)，其中p - y表示模p下的负值
    if y % 2 == yp:
        return Point(x, y, CURVE)
    else:
        return Point(x, p - y, CURVE)


def inner_product(a: List[ModP], b: List[ModP]) -> ModP:
    """Inner-product of vectors in Z_p"""
    assert len(a) == len(b)
    # 计算a和b的内积
    return sum([ai * bi for ai, bi in zip(a, b)], ModP(0, a[0].p))
