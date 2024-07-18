#   Base64是一种用64个字符来表示任意二进制数据的方法。
import base64

from bulletproof.utils.utils import mod_hash, point_to_b64


class Transcript:
    """
    Transcript class.
    Contains all parameters used to generate randomness using Fiat-Shamir
    Separate every entity by a '&'.
    转录类。包含用于使用 Fiat-Shamir 生成随机性的所有参数，用“&”分隔每个实体。
    """

    def __init__(self, seed=b""):
        # 将seed参数进行Base64编码，并将编码结果与字节串b"&"拼接起来，
        # 然后将拼接后的结果赋值给实例变量self.digest。
        # 这个self.digest变量用于存储生成随机性的参数，它是一个以Base64编码表示的字节串。
        self.digest = base64.b64encode(seed) + b"&"

    def add_point(self, g):
        """Add an elliptic curve point to the transcript
        添加一个椭圆曲线以64位二进制添加"""
        self.digest += point_to_b64(g)
        self.digest += b"&"

    def add_list_points(self, gs):
        """Add a list of elliptic curve point to the transcript
        添加一组"""
        for g in gs:
            self.add_point(g)

    def add_number(self, x):
        """Add a number to the transcript"""
        self.digest += str(x).encode()
        self.digest += b"&"

    def get_modp(self, p):
        """Generate a number as the hash of the digest摘要"""
        return mod_hash(self.digest, p)
