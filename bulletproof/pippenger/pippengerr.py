from sympy import integer_nthroot
from math import log2, floor
from itertools import combinations

"""" range(1, len(l)+1)生成了一个从1到len(l)的整数序列，表示子集的大小。
lambda r: list(combinations(l, r))是一个匿名函数，接受一个参数r，并返回l列表中长度为r的所有组合的列表。
combinations(l, r)函数返回l列表中长度为r的所有组合
map(lambda r: list(combinations(l, r)), range(1, len(l)+1))将上述匿名函数应用于整数序列，生成一个包含所有子集的列表的列表。"""
def subset_of(l):
    return sum(map(lambda r: list(combinations(l, r)), range(1, len(l)+1)), [])
#  l="abc",[('a',), ('b',), ('c',), ('a', 'b'), ('a', 'c'), ('b', 'c'), ('a', 'b', 'c')]

class Pippenger:
    # 得到椭圆曲线的生成元、阶数、阶数对应的二进制
    def __init__(self, group):
        self.G = group
        self.order = group.order
        self.lamb = group.order.bit_length()
    
    # Returns g^(2*j)
    def _pow2powof2(self, g, j):

        tmp = g
        for _ in range(j):
            tmp = self.G.square(tmp)
        return tmp

    # Returns Prod g_i ^ e_i
    def multiexp(self, gs, es):
        # 判断长度是否相等
        if len(gs) != len(es):
            raise Exception('Different number of group elements and exponents')

        # 将es列表中的每个元素取模self.G.order，并将结果存储在新的列表es中
        es = [ei % self.G.order for ei in es]

        if len(gs) == 0:
            return self.G.unit

        # self.lamb是Pippenger类的实例变量，它表示群的阶数的比特长度。
        lamb = self.lamb
        N = len(gs) # gs的长度
        # integer_nthroot是sympy库中的一个函数，用于计算一个整数的平方根。
        # 它接受两个参数，第一个参数是要计算平方根的整数，第二个参数是指定平方根的次数。
        # 使用integer_nthroot(lamb//N, 2)来计算lamb//N的平方根。
        s = integer_nthroot(lamb//N, 2)[0]+1
        t = integer_nthroot(lamb*N,2)[0]+1
        """"对于每个索引i，在gs_bin列表中创建一个临时列表tmp，并将gs[i]添加到tmp中。
        然后，使用一个嵌套的循环，从1到s-1，将self.G.square(tmp[-1])的结果追加到tmp中。
        最后，将tmp添加到gs_bin列表中。这样，gs_bin列表将包含N个子列表，每个子列表包含gs[i]及其幂的连续值。"""
        gs_bin = []
        for i in range(N):
            tmp = [gs[i]]
            for j in range(1,s):
                tmp.append(self.G.square(tmp[-1]))
            gs_bin.append(tmp)
        """"对于每个索引i，在es_bin列表中创建一个临时列表tmp1。
        然后，使用两个嵌套的循环，从0到s-1和0到t-1，分别创建临时列表tmp2，
        并将bin(es[i])[2:].zfill(s*t)[-(j+s*k+1)]的结果转换为整数后追加到tmp2中。
        最后，将tmp1添加到es_bin列表中。这样，es_bin列表将包含N个子列表，每个子列表包含es[i]的二进制表示的位数为s*t的连续值。"""
        es_bin = []
        for i in range(N):
            tmp1 = []
            for j in range(s):
                tmp2 = []
                for k in range(t):
                    # 先使用bin()将十进制数10转换为二进制数的字符串形式，并使用字符串的切片操作将“0b”头部去掉，
                    # 然后使用zfill()方法将二进制数补全到s*t位字符串。
                    tmp2.append(int(bin(es[i])[2:].zfill(s*t)[-(j+s*k+1)]))
                tmp1.append(tmp2)
            es_bin.append(tmp1)
        Gs = self._multiexp_bin(
                [gs_bin[i][j] for i in range(N) for j in range(s)],
                [es_bin[i][j] for i in range(N) for j in range(s)]
                )
        ans2 = Gs[-1]

        for k in range(len(Gs)-2,-1,-1):
            ans2 = self._pow2powof2(ans2, s)
            ans2 = self.G.mult(ans2, Gs[k])

        return ans2

    # 用于执行二进制分解的多项式乘法计算。
    # 它通过将元素列表和指数列表进行二进制分解，并使用字典来存储中间结果，最终得到多项式乘法的结果列表。
    def _multiexp_bin(self, gs, es):
        assert len(gs) == len(es)
        M = len(gs)  # gs的长度
        b = floor(log2(M) - log2(log2(M)))  # 下舍整数，小于或等于 x
        b = b if b else 1  # b被赋值为b本身，如果b的值为真（非零），否则赋值为1
        """" 代码使用列表推导式生成一个名为subsets的列表，
        其中每个元素是一个子集。子集的生成是通过使用range函数和min函数来确定子集的起始索引和结束索引，步长为b。
        这样，subsets列表将包含多个子集，每个子集是一个索引范围。"""
        subsets = [list(range(i,min(i+b,M))) for i in range(0,M,b)]  # range(初值, 终值, 步长)

        # Ts是一个列表推导式，它使用了嵌套的字典推导式。它的作用是创建一个包含多个字典的列表，
        # 其中每个字典都有一个键值对，键是subset_of(S)函数生成的子集，值是None。

        # 具体来说，subsets是一个包含多个子集的列表，每个子集由range函数生成。
        # 对于每个子集S，subset_of(S)函数生成一个包含S的所有子集的列表。
        # 然后，使用字典推导式{sub: None for sub in subset_of(S)}，
        # 将每个子集作为键，将None作为值，创建一个字典。最后，将这些字典组成的列表添加到Ts列表中。
        Ts = [{sub: None for sub in subset_of(S)} for S in subsets]

        """"代码使用zip函数将Ts列表和subsets列表进行迭代，并在每次迭代中执行以下操作：
        - 对于每个子集S中的索引i，将gs[i]作为键(i,)的值，添加到对应的字典T中。
        - 定义一个名为set_sub的内部函数，用于递归地设置字典T中的子乘积。
        - 对于字典T中的每个键sub，调用set_sub函数进行设置。
        """
        for T,S in zip(Ts, subsets):
            # zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象
            # codelist1 = [1, 2, 3] list2 = ['a', 'b', 'c'] zipped = zip(list1, list2) print(list(zipped))
            # 输出：[(1, 'a'), (2, 'b'), (3, 'c')]
            for i in S:
                T[(i,)] = gs[i]
            # Recursively set the subproducts in T
            def set_sub(sub):
                if T[sub] is None:
                    if T[sub[:-1]] is None:
                        set_sub(sub[:-1])
                    T[sub] = self.G.mult(T[sub[:-1]], gs[sub[-1]])
            for sub in T:
                set_sub(sub)
        """代码使用range函数迭代指数列表es[0]的长度，并在每次迭代中执行以下操作：
        - 创建一个临时变量tmp，并将其初始化为群的单位元素。
        - 使用zip函数将Ts列表和subsets列表进行迭代，并在每次迭代中执行以下操作：
        - 从子集S中选择满足条件es[j][k]的索引j，并将其存储在sub_es列表中。
        - 将sub_es转换为元组，并将其作为键从字典T中获取对应的值，并与tmp进行乘法运算。
        - 将乘积结果tmp添加到列表Gs中。"""
        Gs = []
        for k in range(len(es[0])):
            tmp = self.G.unit
            for T,S in zip(Ts, subsets):
                # 在循环中，对于S中的每个索引j，如果es[j][k]的值为真（非零），则将索引j添加到sub_es列表中。
                sub_es = [j for j in S if es[j][k]]
                # 使用 tuple() 函数创建元组
                sub_es = tuple(sub_es)
                # 检查sub_es是否为空。
                # 如果sub_es为空，表示没有满足条件的索引值，那么代码会跳过当前循环迭代，继续下一次迭代。
                # 如果sub_es不为空，则继续执行循环内的计算和操作。首先，将变量tmp与T[sub_es]进行乘法运算，
                # 并将结果赋值给tmp。这里的T[sub_es]表示字典T中键为sub_es的值。
                if not sub_es:
                    continue
                tmp = self.G.mult(tmp, T[sub_es])
            Gs.append(tmp)
            
        return Gs

            

