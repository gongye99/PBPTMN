import random
from fractions import Fraction

from ModFuction import *

class ECC():
    """ 椭圆曲线密码体制
        实现椭圆曲线点的运算, 消息的加密等
        可应用于 Elgamal 加密
        ------------------------------
        此 ECC类 用到运算符重载, 代码较复杂
        可以参看简化版:`ecc2.py`中的 ECC类
        曲线方程: y^2 = x^3 + ax - b
        * a : Ep(a, b) 中的 a
        * b : Ep(a, b) 中的 b
        * p : GF(p), y^2 mod p 中的 p
    """
    def __init__(self, a, b, p):
        if 4 * a ** 3 + 27 * b ** 2 == 0:
            print("非法椭圆曲线，请重新输入")
        self.__class__.a = a  # __class__表示设为类成员属性
        self.__class__.b = b  # 以便内部类point访问
        self.__class__.p = p

    def genEset(self):
        """ 生成椭圆曲线的坐标点集 Ep(a, b)
            * return : 坐标点集 [(x1,y1), (x2,y2), ··· ]
        """
        a, b, p = self.a, self.b, self.p
        Eset = [EO.point]  # 定义一个`点集Ep(a,b)`的加法幺元
        for x in range(0, p):
            sqr = (x ** 3 + a * x + b) % p  # 计算待开方的值
            # y是不是p的平方剩余，若y是，则求出y的值，有一对
            if isQuadricReside(sqr, p) == 1:
                # 若 sqr 是 p 的平方剩余, 则求 sqr 的根
                solution = calcResideRoot(sqr, p)
                Eset.append((x, solution[0]))
                Eset.append((x, solution[1]))
        return Eset

    def genG(self):
        a, b, p = self.a, self.b, self.p
        for x in range(0, p):
            sqr = (x ** 3 + a * x + b) % p  # 计算待开方的值
            # y是不是p的平方剩余，若y是，则求出y的值，有一对
            if isQuadricReside(sqr, p) == 1:
                # 若 sqr 是 p 的平方剩余, 则求 sqr 的根
                solution = calcResideRoot(sqr, p)
                break
        G = self.point(x, solution[0])
        return G


    class point():
        """ Ep(a,b)中`坐标点(x, y)`实例化为`point对象`
            --------------------------------------
            实例化后的point对象可做 + - * 等运算
        """

        def __init__(self, *point):
            """ 获取实例对象ECC()中的 a, p, `坐标点point`
                * a, p : Ep(a, b) 中的 a, p
                * point : 椭圆曲线上的坐标点(x, y)
            """
            # 继承外部类成员属性 ECC.a, ECC.p
            self.a, self.p, self.point = ECC.a, ECC.p, point


        def __add__(self, other):
            """ 重载运算符`+`: 定义椭圆上点的加法
                * self  : point对象 P:(x1, y1)
                * other : point对象 Q:(x2, y2)
                * retrun: point对象 P+Q:(x3,y3)
            """
            a, p, P, Q = self.a, self.p, self, other
            (x1, y1), (x2, y2) = self.point, other.point

            if P.point == EO.point: return Q  # EO+Q=Q 和加法元相加返回本身
            if Q.point == EO.point: return P  # P+EO=P
            if x1 == x2 and y1 != y2: return EO  # P+Q=EO 同一条直线上的和为加法元

            # 求k
            if x1 != x2: lamb = Fraction(y2 - y1, x2 - x1)  # 使用斜率公式lamb = (y2 - y1) / (x2 - x1)计算斜率
            if x1 == x2: lamb = Fraction(3 * x1 * x1 + a, 2 * y1)  # 使用斜率公式lamb = (3 * x1 * x1 + a) / (2 * y1)计算斜率
            lamb = calcCongruence(lamb, p)  # 计算 lamb mod p 的同余正整数

            # 求R(x3,y3)
            x3 = lamb ** 2 - x1 - x2
            x3 = calcCongruence(x3, p)
            y3 = lamb * (x1 - x3) - y1
            y3 = calcCongruence(y3, p)

            return ECC.point(x3, y3)

        def __mul__(self, coef):
            """ 重载运算符`*`: 椭圆上点的数乘 例如Point*3 """
            sums = self
            """代码中的for循环用于进行点的数乘操作。循环从1到coef（数乘的系数）进行迭代，
            每次迭代都将当前点self与自身相加，然后将结果赋值给变量sums。
            这个数乘操作的目的是将一个点在椭圆曲线上重复相加多次，从而得到一个新的点。"""
            for _ in range(1, coef): sums += self
            return sums

        def __rmul__(self, other):
            """ 重载运算符`*`: 椭圆上点的数乘 例如3*Point """
            return self * other

        def __neg__(self):
            """ 重载运算符`-`: 椭圆上点的加法逆元
             根据椭圆曲线上点的加法逆元的定义，计算出一个新的点，
             使得将该点与原始点相加后得到椭圆曲线上的加法幺元（零元素）。
             在椭圆曲线上，点的加法逆元是一个特殊的点，
             表示在曲线上进行加法运算时，与原始点相加后得到加法幺元的点。"""
            x, y = (self.point[0], ECC.p - self.point[1])
            # 判断y是否等于椭圆曲线的模数ECC.p，如果是，则将y的值设为0，否则保持不变。
            y = 0 if y == ECC.p else y
            return ECC.point(x, y)

        def __sub__(self, other):
            """ 重载运算符`-`: 椭圆上点的减法 """
            other = - other  # 返回加法逆元 则 P-Q = P+(-Q)
            return self + other

        def __repr__(self):
            """ 重载函数`print`: 打印对象point的点(x,y) """
            # 获取point对象的坐标点point (0,0)打印字母O
            disp = self.point
            disp = 'O' if disp == EO.point else disp
            return str(disp)

        def __str__(self):
            x, y = (self.point[0], self.point[1])
            """ 将椭圆曲线上的点转换为字符串格式 """
            return f"({x}, {y})"

        def export(self):
            x=self.point[0]
            y=self.point[1]
            x_bytes = x.to_bytes((x.bit_length() + 7) // 8, 'big')
            y_bytes = y.to_bytes((y.bit_length() + 7) // 8, 'big')
            point_bytes = x_bytes + y_bytes
            return point_bytes


def point_to_ser(P, comp=True):
     """ Convert Point to serialized format """
     #  WEAKNESS - to_bytes not constant time (this is used in ECDH)
     if comp:
        return bytes((2 + (P.point[1] & 1),)) + P.point[0].to_bytes(32, 'big')
     else:
        return b'\x04' + P.point[0].to_bytes(32, 'big') + P.point[1].to_bytes(32, 'big')

def ser_to_point(self,Aser,p):
    assert Aser[0] == 0x04
    x = int.from_bytes(Aser[1:33], 'big')
    assert x < p
    y = int.from_bytes(Aser[33:], 'big')
    assert y < p
    return self.point(x,y)


EO = ECC(1, 1, 1).point('O', 'O')

if __name__ == '__main__':
    ellip = ECC(1, 1, 23)  # 实例化一个 Ep(a,b) 对象
    G1=ellip.genG()
    print(G1);
    P = ellip.point(3, 10)  # 实例化Ep(a,b)上的point对象
    Q = ellip.point(9, 7)  # 实例化Ep(a,b)上的point对象
    print("P=",P)
    print("P-Q:", P - Q)
    print("p+G=",P + G1)
    (x,y)=P.point
    print(x)