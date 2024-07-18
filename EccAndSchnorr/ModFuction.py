def gcd(x, y):
    """ 使用欧几里德算法计算最大公约数 """

    # 如果其中一个数是 0，则最大公约数是另一个数
    if x == 0:
        return y
    if y == 0:
        return x

    # 欧几里德算法
    while x > 0:
        x, y = y % x, x

    return y


def extendGcd(a, b):
    """
    这段代码实现了扩展欧几里德算法（Extended Euclidean Algorithm），
    用于求解两个整数a和b的最大公约数（gcd）
    以及满足同余式a*x + b*y = gcd(a, b)平方的整数解(x, y)。
    同余式是数论的基本概念之一，设m是给定的一个正整数，a、b是整数，
    若满足m|(a-b)，则称a与b对模m同余，记为a≡b(mod m)，或记为a≡b(m)。
    这个式子称为模m的同余式,a与b对于模m，有同一个余数r
    """
    #  判断b是否为0。如果是，说明a和b的最大公约数为a
    if b == 0:
        return a, b
    #  如果b不为0，则递归调用extendGcd函数，传入参数b和a % b，以求解更小规模的问题。
    else:
        x, y = extendGcd(b, a % b)
        x, y = y, x - (a // b) * y
        return x, y


def isQuadricReside(a, p):
    """ 判断 a 是否为 素数p 的`平方剩余`
        ---------------------------
        * return 0 : a 被 p 整除
        * return 1 : a 是模 p 的平方剩余
        * return-1 : a 不是模 p 的平方剩余
    """
    legendre = (a ** int((p - 1) / 2)) % p
    if legendre > 1:
        legendre -= p

    return legendre

def calcResideRoot(a, p):
    """ 求模 p 的平方剩余 a 的两个平方根
        ---------------------------
        即方程 x^2 = a mod p 的解
        * retrun : 元组解(x1, x2)⛄
    """
    print(a,p)
    for i in range(1, p):
        if (i ** 2) % p == a:
            return (i, p - i)


def calcCongruence(n, p):
    """ 计算 a mod p 的同余正整数
        ----------------------
        * n : 分数、负数等
        * p : 素数
        * retrun : 同余的正整数
    """
    if isinstance(n, int):
        # 若a为整数, 则直接得到正整数同余式
        return n % p
        # 若n为分数b/a, 则计算得到正整数同余式
        # 即求不定 a*x + p*y = b 的解 x
    a, b = n.denominator, n.numerator
    coef = b // gcd(a, p)
    x, _ = extendGcd(a, p)
    return (coef * x) % p

def get_inverse_element(value, max_value):
    """
    计算value在1-max_value之间的逆元
    """
    for i in range(1, max_value):
        if (i * value) % max_value == 1:
            return i
    return -1