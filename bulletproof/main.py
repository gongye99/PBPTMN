"""Various tests"""
import json
import time

from fastecdsa.curve import secp256k1
import os
from bulletproof.utils.utils import mod_hash, inner_product, ModP
from bulletproof.utils.commitments import vector_commitment, commitment
from bulletproof.utils.elliptic_curve_hash import elliptic_hash

# from .rangeproofs.rangeproof_prover import NIRangeProver
# from .rangeproofs.rangeproof_verifier import RangeVerifier
from bulletproof.rangeproofs.rangeproof_aggreg_prover import AggregNIRangeProver
from bulletproof.rangeproofs.rangeproof_aggreg_verifier import AggregRangeVerifier

CURVE = secp256k1
p = CURVE.q

def closest_power_of_two(m):
    n = 0
    while 2 ** n < m:
        n += 1
    return n - 1
# def singletry(vm, nm, m):
# v = 2 ** (2 ** vm)
# v是否在2的n次方-1的范围内。
def maskParameters(v,pv):
    ntemp =  closest_power_of_two(v)
    ntemp = closest_power_of_two(ntemp)
    vtemp = 2**ntemp-1
    np = closest_power_of_two(pv)
    np = closest_power_of_two(np)
    return vtemp , np

def gunverify(vtemp,np):
    m = 4
    V = vtemp
    n = np
    vs  =  [ModP(V, p) for _ in range(m)]
    # m=len(vs)
    # print("需要证明的数：", vm)
    # n = 2 ** nm
    # print("需要证明的范围为0到", nm)
    # 这行代码生成了一个包含7个随机字节串的列表，每个字节串的长度为10。
    seeds = [os.urandom(10) for _ in range(7)]
    # 这行代码定义了两个变量vs和n。vs是一个包含m个ModP(15, p)对象的列表，ModP(15, p)表示一个模p的整数。n被赋值为16。
    # 根据循环迭代的次数生成一个列表。在每次迭代中，都会创建一个ModP(15, p)对象，并将其添加到列表中。
    # range(m)：这是一个内置函数range()的调用，它返回一个包含从0到m-1的整数的可迭代对象。在这里，它用于控制循环的迭代次数。

    # 这行代码将vs列表的最后一个元素修改为ModP(2 ** 16 - 1, p)，其中**表示指数运算
    vs[-1] = ModP(2 ** n - 1, p)
    # 这行代码使用循环生成了一个包含n * m个元素的列表gs。
    # 每个元素是通过将i转换为字节串并与seeds[0]拼接，然后使用elliptic_hash函数对其进行哈希计算得到的结果。
    gs = [elliptic_hash(str(i).encode() + seeds[0], CURVE) for i in range(n * m)]
    # 这行代码与上一行类似，生成了一个包含n * m个元素的列表hs，
    # 每个元素通过将i转换为字节串并与seeds[1]拼接，然后使用elliptic_hash函数对其进行哈希计算得到。
    hs = [elliptic_hash(str(i).encode() + seeds[1], CURVE) for i in range(n * m)]
    # 这行代码使用seeds[2]作为输入，通过elliptic_hash函数计算得到一个哈希值，并将其赋值给变量g。
    g = elliptic_hash(seeds[2], CURVE)
    h = elliptic_hash(seeds[3], CURVE)
    u = elliptic_hash(seeds[4], CURVE)
    # 这行代码使用循环生成了一个包含m个元素的列表gammas。
    # 每个元素是通过将seeds[5]作为输入，通过mod_hash函数计算得到的模p的哈希值。
    gammas = [mod_hash(seeds[5], p) for _ in range(m)]
    Vs = [commitment(g, h, vs[i], gammas[i]) for i in range(m)]
    Prov = AggregNIRangeProver(vs, n, g, h, gs, hs, gammas, u, CURVE, seeds[6])
    proof = Prov.prove()  # 得到了gp hp ap 和 bp
    Verif = AggregRangeVerifier(Vs, g, h, gs, hs, u, proof)
    return Verif

start_time = time.time()
# 生成范围证明
vtemp,np = maskParameters(133,144)
np = 2**np
vtemp = 2**vtemp
# print(vtemp,"111111",np)
Verif = gunverify(vtemp,np)
# end_time = time.time()
# run_time = end_time - start_time
# print(f"程序运行时间：{run_time} 秒")
Verif_dict = Verif.to_dict()
print(Verif_dict)
# 代理需要做的
# start_time = time.time()
Verif.verify()
end_time = time.time()
run_time = end_time - start_time
print(f"程序运行时间：{run_time} 秒")

