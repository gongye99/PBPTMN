"""Contains classes for the prover of an inner-product argument"""

from typing import Optional

from bulletproof.innerproduct.inner_product_verifier import Proof1, Proof2
from bulletproof.utils.commitments import vector_commitment
from bulletproof.utils.utils import inner_product
from bulletproof.utils.transcript import Transcript


class NIProver:
    """Class simulating a NI prover for the inner-product argument (Protocol 1)
    模拟内积参数的 NI 证明器的类（协议 1）"""
    def __init__(self, g, h, u, P, c, a, b, group, seed=b""):
        assert len(g) == len(h) == len(a) == len(b)
        self.g = g
        self.h = h
        self.u = u
        self.P = P
        self.c = c
        self.a = a
        self.b = b
        self.group = group
        self.transcript = Transcript(seed)

    def prove(self) -> Proof1:
        """
        Proves the inner-product argument following Protocol 1 in the paper
        Returns a Proof1 object.
        """
        # x = mod_hash(self.transcript.digest, self.group.order)，
        # 确保x的值在0到2 **self.group.order.bit_length()之间
        # 生成随机的x
        x = self.transcript.get_modp(self.group.q)
        self.transcript.add_number(x)
        P_new = self.P + (x * self.c) * self.u
        u_new = x * self.u
        Prov2 = FastNIProver2(
            self.g,
            self.h,
            u_new,
            P_new,
            self.a,
            self.b,
            self.group,
            self.transcript.digest,
        )
        return Proof1(u_new, P_new, Prov2.prove(), self.transcript.digest)


class FastNIProver2:
    """Class simulating a NI prover for the inner-product argument (Protocol 2)"""
    def __init__(self, g, h, u, P, a, b, group, transcript: Optional[bytes]=None):
        assert len(g) == len(h) == len(a) == len(b)
        # 用于验证向量a的长度是否是2的幂
        assert len(a) & (len(a) - 1) == 0
        self.log_n = len(a).bit_length() - 1
        self.n = len(a)
        self.g = g
        self.h = h
        self.u = u
        self.P = P
        self.a = a
        self.b = b
        self.group = group
        self.transcript = Transcript()
        if transcript:   # 副本存在
            self.transcript.digest += transcript  # 副本摘要的哈希值更新
            self.init_transcript_length = len(transcript.split(b"&"))    # 用"&"分割
        else:
            self.init_transcript_length = 1


    def prove(self):
        """
        Proves the inner-product argument following Protocol 2 in the paper
        Returns a Proof2 object.
        """
        gp = self.g
        hp = self.h
        ap = self.a
        bp = self.b

        xs = []
        Ls = []
        Rs = []
        # 代码检查ap、bp、gp、hp这几个向量的长度是否都为1。
        # 如果是，则表示已经达到了循环的终止条件，将生成一个Proof2对象并返回。
        while True:
            if len(ap) == len(bp) == len(gp) == len(hp) == 1:
                return Proof2(
                    ap[0],
                    bp[0],
                    xs,   # 副本摘要的哈希值列表
                    Ls,   # 承诺列表1
                    Rs,   # 承诺列表2
                    self.transcript.digest,   # 副本摘要的哈希值
                    self.init_transcript_length,
                )
            #  如果长度不为1，则继续执行循环内的计算和操作。首先，根据当前向量的长度，计算出切片的长度np，用于将向量分割成两部分。
            nq = np = len(ap) // 2
            # ap[:np]和bp[np:]分别表示ap和bp向量的切片，从索引0到np（不包括np）的元素，从索引np到末尾的元素
            # 证明者计算
            cl = inner_product(ap[:nq], bp[np:])
            cr = inner_product(ap[np:], bp[:nq])
            # g**a * h**b * u**cL
            L = vector_commitment(gp[np:], hp[:nq], ap[:nq], bp[np:]) + cl * self.u
            R = vector_commitment(gp[:nq], hp[np:], ap[np:], bp[:nq]) + cr * self.u
            #  list[ModP | Point] = []
            Ls.append(L)
            Rs.append(R)
            self.transcript.add_list_points([L, R])
            # x = mod_hash(self.transcript.digest, self.group.order)
            # 验证者生成一个随机数字。发送给证明者
            x = self.transcript.get_modp(self.group.q)
            # 副本摘要的哈希值列表
            xs.append(x)
            self.transcript.add_number(x)
            # inv Returns the modular inverse
            # a = ['a', 'b', 'c', 'd']
            # b = ['1', '2', '3', '4']
            # print(list(zip(a, b)))
            # [('a', '1'), ('b', '2'), ('c', '3'), ('d', '4')]
            # x、x的模逆、gp的0-np，gp的np到末尾互为组合
            # 证明者和验证者均计算
            gp = [x.inv() * gi_fh + x * gi_sh for gi_fh, gi_sh in zip(gp[:nq], gp[np:])]
            hp = [x * hi_fh + x.inv() * hi_sh for hi_fh, hi_sh in zip(hp[:nq], hp[np:])]
            # 证明者计算
            ap = [x * ai_fh + x.inv() * ai_sh for ai_fh, ai_sh in zip(ap[:nq], ap[np:])]
            bp = [x.inv() * bi_fh + x * bi_sh for bi_fh, bi_sh in zip(bp[:nq], bp[np:])]
