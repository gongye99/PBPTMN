from fastecdsa.curve import secp256k1
from pippenger.pippengerr import Pippenger
from pippenger.group import EC

PipSECP256k1 = Pippenger(EC(secp256k1))

__all__ = ["Pippenger", "EC", "PipSECP256k1"]
# 用于定义模块中可以被导入的公共接口。
# 在这个例子中，__all__列表中包含了三个字符串元素："Pippenger", "EC", 和 "PipSECP256k1"。
# 这意味着当其他模块导入pippenger模块时，只有这三个变量会被导入，其他变量将不可见。


