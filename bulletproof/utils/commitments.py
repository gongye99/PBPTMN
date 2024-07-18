from fastecdsa.point import Point

from bulletproof.pippenger import PipSECP256k1


def commitment(g, h, x, r):
    return x * g + r * h


def vector_commitment(g, h, a, b):
    assert len(g) == len(h) == len(a) == len(b)
    # return sum([ai*gi for ai,gi in zip(a,g)], Point(None,None,None)) \
    #         + sum([bi*hi for bi,hi in zip(b,h)], Point(None,None,None))
    """PipSECP256k1是pippenger一个类，它提供了在椭圆曲线上进行多项式乘法的功能。multiexp方法接受两个参数，分别是g + h和a + b。
    g + h表示将列表g和h进行元素级别的相加操作。这意味着对应位置的元素将相加，并返回一个新的列表。
    a + b也表示将列表a和b进行元素级别的相加操作，返回一个新的列表。
    最后，multiexp方法将对这两个列表进行多项式乘法的计算，并返回结果。"""
    p = PipSECP256k1.multiexp(g + h, a + b)
    return p


def _mult(a: int, g: Point) -> Point:
    if a < 0 and abs(a) < 2 ** 32:
        return abs(a) * _inv(g)
    else:
        return a * g


def _inv(g: Point) -> Point:
    return Point(g.x, -g.y, g.curve)
