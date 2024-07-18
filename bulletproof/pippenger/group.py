#ABC库提供了抽象基类用于规范Python代码的接口
from abc import ABC, abstractmethod

# 用于快速椭圆曲线加密的Python库
from fastecdsa.curve import Curve

from bulletproof.pippenger.modp import ModP

"""定义了一个名为Group的抽象基类和两个具体的子类MultIntModP和EC"""
class Group(ABC):
    def __init__(self, unit, order):
        self.unit = unit
        self.order = order

    @abstractmethod
    def mult(self, x, y):
        pass

    def square(self, x):
        return self.mult(x, x)


class MultIntModP(Group):
    def __init__(self, p, order):
        Group.__init__(self, ModP(1, p), order)

    #  MultIntModP类的mult方法实现了整数模P的乘法运算
    def mult(self, x, y):
        return x * y


class EC(Group):
    def __init__(self, curve: Curve):
        # curve.G.IDENTITY_ELEMENT表示椭圆曲线对象curve的G属性的IDENTITY_ELEMENT属性。
        # 这个属性表示椭圆曲线上的单位元素。
        # curve.q表示椭圆曲线对象curve的q属性，它表示椭圆曲线的阶数。
        Group.__init__(self, curve.G.IDENTITY_ELEMENT, curve.q)

    # EC类的mult方法实现了椭圆曲线上的加法运算
    def mult(self, x, y):
        return x + y
