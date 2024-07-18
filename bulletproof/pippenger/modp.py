# 给定点的x和阶数
class ModP:

    num_of_mult=0
    @classmethod
    def reset(cls):
        cls.num_of_mult = 0

    def __init__(self, x, p):
        self.x = x
        self.p = p

# 加法重写
    def __add__(self, y):
        if isinstance(y, int):
            return ModP(self.x+y, self.p)
        assert self.p == y.p
        return ModP((self.x + y.x) % self.p, self.p)

# 乘法重写
    def __mul__(self, y):
        type(self).num_of_mult += 1
        if isinstance(y, int):
            return ModP(self.x*y, self.p)
        assert self.p == y.p
        return ModP((self.x * y.x) % self.p, self.p)

# 减法重写
    def __sub__(self, y):
        if isinstance(y, int):
            return ModP(self.x-y, self.p)
        assert self.p == y.p
        return ModP((self.x - y.x) % self.p, self.p)

# 指数重写
    def __pow__(self, n):
        # return ModP(pow(self.x, n, self.p), self.p)
        exp = bin(n)
        value = ModP(self.x, self.p)
    
        for i in range(3, len(exp)):
            value = value * value
            if(exp[i:i+1]=='1'):
                value = value*self
        return value
    
    
    def __neg__(self):
        return ModP(self.p - self.x, self.p)

# 重写相等
    def __eq__(self, y):
        return (self.x == y.x) and (self.p == y.p)

# 输出字符串
    def __str__(self):
        return str(self.x)

# 输出字符串
    # 实现 “自我描述” 功能——当直接打印类的实例化对象时,系统将会自动调用该方法,输出对象的自我描述信息,用来告诉外界对象具有的状态信息。
    def __repr__(self):
        return str(self.x)

