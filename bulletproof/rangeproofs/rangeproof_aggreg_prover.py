from typing import List
from bulletproof.utils.utils import Point, ModP, inner_product, mod_hash
from bulletproof.utils.transcript import Transcript
from bulletproof.utils.commitments import vector_commitment, commitment
from bulletproof.rangeproofs.rangeproof_verifier import Proof
from bulletproof.rangeproofs.rangeproof_aggreg_verifier import Proof
from bulletproof.innerproduct.inner_product_prover import NIProver
from bulletproof.pippenger import PipSECP256k1


# vs, n, g, h, gs, hs, gammas, u, CURVE, seeds[6]
class AggregNIRangeProver:
    def __init__(
        self,
        # 一组随机数x
        vs: List[ModP],
        n: int,
        # 椭圆上的点
        g: Point,
        h: Point,
        # 椭圆上的点集
        gs: List[Point],
        hs: List[Point],
        # 一组随机数x的集合
        gammas: List[ModP],
        # 椭圆上的点
        u: Point,
        group,
        # 字节表示的随机数
        seed: bytes = b"",
    ):
        self.vs = vs
        self.n = n
        self.g = g
        self.h = h
        self.gs = gs
        self.hs = hs
        self.gammas = gammas
        self.u = u   #椭圆曲线上的一个点
        self.group = group
        self.transcript = Transcript(seed)
        self.m = len(vs)

    def to_dict(self):
        return {
            "vs": [v.to_dict() for v in self.vs],
            "n": self.n,
            "g": self.g.to_dict(),
            "h": self.h.to_dict(),
            "gs": [g.to_dict() for g in self.gs],
            "hs": [h.to_dict() for h in self.hs],
            "gammas": [gamma.to_dict() for gamma in self.gammas],
            "u": self.u.to_dict(),
            # group可能是一个复杂的对象，需要特别处理。这里假设它是一个可以直接序列化的基本类型，或者提供了to_dict方法
            "group": self.group.to_dict() if hasattr(self.group, 'to_dict') else self.group,
            "seed": self.seed.hex(),  # bytes类型可以转换为十六进制字符串进行序列化
            "m": self.m,
            # transcript也是一个复杂对象，需要根据其结构进行相应的处理
            "transcript": self.transcript.to_dict() if hasattr(self.transcript, 'to_dict') else self.transcript,
        }

    def prove(self):
        vs = self.vs  # len=4
        n = self.n    # 16
        m = self.m    # 4
        gs = self.gs   # len=64
        hs = self.hs   # len=64
        h = self.h

        aL = []
        for v in vs:
            # 将v.x的二进制表示进行反转，并将二进制形式逐位转换为整数列表，然后将其添加到aL列表中。
            # reversed()函数是返回序列seq的反向访问的迭代器
            # 将v二进制数组化成整数数组,随机数v集合,每个v的二进制表示的每一位为一个单独的元素
            aL += list(map(int, reversed(bin(v.x)[2:].zfill(n))))[:n]
        # 对于aL列表中的每个元素x，计算(x - 1) % self.group.q的值，并将结果存储在aR列表中
        # 设置范围，在1到self.group.q之间   x, y = (self.point[0], ECC.p - self.point[1])
        # 位上数字为1的变为0，为0的变为阶数
        aR = [
            (x - 1) % self.group.q for x in aL
        ]  # TODO 实现椭圆曲线点的逆来计算 -1 * g 而不是乘以 p-1
        # 使用mod_hash()函数对字节串b"alpha" + self64位编码后进行哈希运算，并将结果赋值给变量alpha。
        # b作为前缀可以创建字节字符串
        # 此字节串则会被作为bytes（字节）类型而非string（字符串）类型进行处理，因而可以进一步编码进如ASCII乃至于Utf-8等二进制形式的数据流中
        alpha = mod_hash(b"alpha" + self.transcript.digest, self.group.q)
        # 调用vector_commitment()函数计算向量的承诺值，并将结果与alpha * h相加，得到变量A。
        # 关于aL的承诺
        A = vector_commitment(gs, hs, aL, aR) + alpha * h
        """ 致盲因子 """
        # 对于范围range(n * m)中的每个元素i，
        # 使用mod_hash()函数对字节串str(i).encode() + self64位编码后的进行哈希运算，并将结果存储在sL列表中,一组随机数
        sL = [
            mod_hash(str(i).encode() + self.transcript.digest, self.group.q)
            for i in range(n * m)    # 0--n*m
        ]
        # 对于范围range(n * m, 2 * n * m)中的每个元素i，
        # 使用mod_hash()函数对字节串str(i).encode() + self64位编码后的进行哈希运算，并将结果存储在sR列表中
        sR = [
            mod_hash(str(i).encode() + self.transcript.digest, self.group.q)
            for i in range(n * m, 2 * n * m)    # n*m--2*n*m
        ]
        # 使用mod_hash()函数对字节串str(2 * n).encode() + self64位编码后的进行哈希运算，并将结果赋值给变量
        rho = mod_hash(str(2 * n).encode() + self.transcript.digest, self.group.q)
        # 调用vector_commitment()函数计算向量的承诺值，并将结果与rho * h相加
        S = vector_commitment(gs, hs, sL, sR) + rho * h
        self.transcript.add_list_points([A, S])   # self添加一组椭圆曲线上的点
        """验证者向证明者发送随机的y"""
        y = self.transcript.get_modp(self.group.q)
        # 将y值添加到self.transcript中，用于记录证明过程中的交互
        self.transcript.add_number(y)
        # 从self.transcript中获取一个模self.group.q的值，并将结果赋值给变量z。这一步计算了z值
        z = self.transcript.get_modp(self.group.q)
        # 将z值添加到self.transcript中，用于记录证明过程中的交互。
        self.transcript.add_number(z)

        # 调用_get_polynomial_coeffs()函数计算多项式系数t1和t2，并将结果分配给变量t1和t2。这一步计算了多项式系数t1和t2，
        # 真的系数
        t1, t2 = self._get_polynomial_coeffs(aL, aR, sL, sR, y, z)
        # 使用mod_hash()函数对字节串b"tau1" + self.transcript.digest进行哈希运算，并将结果赋值给变量tau1。这一步计算了tau1值
        # 随机的系数，用于证明承诺的系数
        tau1 = mod_hash(b"tau1" + self.transcript.digest, self.group.q)
        tau2 = mod_hash(b"tau2" + self.transcript.digest, self.group.q)
        # 调用commitment()函数计算承诺值T1，其中使用self.g和h作为基点，t1作为系数，tau1作为附加参数。
        # 生成t1，t2的承诺
        T1 = commitment(self.g, h, t1, tau1)
        T2 = commitment(self.g, h, t2, tau2)
        # 将T1和T2两个点添加到self.transcript中，用于记录证明过程中的交互。
        self.transcript.add_list_points([T1, T2])
        # 从self.transcript中获取一个模self.group.q的值，并将结果赋值给变量x
        x = self.transcript.get_modp(self.group.q)
        self.transcript.add_number(x)
        taux, mu, t_hat, ls, rs = self._final_compute(
            aL, aR, sL, sR, y, z, x, tau1, tau2, alpha, rho
        )

        # return Proof(taux, mu, t_hat, ls, rs, T1, T2, A, S), x,y,z
        # h**y**(-n)
        hsp = [(y.inv() ** i) * hs[i] for i in range(n * m)]

        # 计算变量P的值，其中包括A、x S和一系列点的线性组合
        # 关于ls和rs的承诺，由验证者生成
        P = (
            A
            + x * S
            + PipSECP256k1.multiexp(
                gs + hsp,
                [-z for _ in range(n * m)]
                + [
                    (z * (y ** i)) + (z ** (2 + (i // self.n))) * (2 ** (i % self.n))
                    for i in range(n * m)
                ],
            )
        )
        # 创建一个NIProver类的实例InnerProv，并传递相应的参数。这一步用于创建内部证明器。
        # 承诺由g,h,r,v变成了gs,hsp,ls,rs
        InnerProv = NIProver(gs, hsp, self.u, P + (-mu) * h, t_hat, ls, rs, self.group)
        # 调用InnerProv实例的prove()方法，生成内部证明。这一步生成了内部证明，
        # gp,hp,bp,ap发生变化,也就是gs,hsp,ls,rs发生了变化
        innerProof = InnerProv.prove()

        ### DEBUG ###
        # 计算变量delta_yz的值，其中包括一系列数值的求和和乘法运算
        delta_yz = (z - z ** 2) * sum(
            [y ** i for i in range(n * m)], ModP(0, self.group.q)
        ) - sum(
            [(z ** (j + 2)) * ModP(2 ** n - 1, self.group.q) for j in range(1, m + 1)]
        )
        t0 = sum([vs[j] * (z ** (2 + j)) for j in range(m)]) + delta_yz
        ### DEBUG ###
        return Proof(taux, mu, t_hat, T1, T2, A, S, innerProof, self.transcript.digest)

    def _get_polynomial_coeffs(self, aL, aR, sL, sR, y, z):
        t1 = inner_product(
            sL,
            [
                (y ** i) * (aR[i] + z)
                + (z ** (2 + (i // self.n))) * (2 ** (i % self.n))
                for i in range(self.n * self.m)
            ],
        ) + inner_product(
            [aL[i] - z for i in range(self.n * self.m)],
            [(y ** i) * sR[i] for i in range(self.n * self.m)],
        )
        t2 = inner_product(sL, [(y ** i) * sR[i] for i in range(self.n * self.m)])
        return t1, t2

    def _final_compute(self, aL, aR, sL, sR, y, z, x, tau1, tau2, alpha, rho):
        # <aL-z*1**n,y**n o (aR+z*1**n)+z*2**n>
        ls = [aL[i] - z + sL[i] * x for i in range(self.n * self.m)]
        rs = [
            (y ** i) * (aR[i] + z + sR[i] * x)
            + (z ** (2 + (i // self.n))) * (2 ** (i % self.n))
            for i in range(self.n * self.m)
        ]
        # t0+t1*X+t2*X, to=v*z**2+(y,z)
        t_hat = inner_product(ls, rs)
        # 用于证明承诺的多项式
        taux = (
            tau2 * (x ** 2)
            + tau1 * x
            + sum([(z ** (2 + j)) * self.gammas[j] for j in range(self.m)])
        )
        mu = alpha + rho * x    # 致盲A和S
        return taux, mu, t_hat, ls, rs
