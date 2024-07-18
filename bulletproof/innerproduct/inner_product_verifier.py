"""Contains classes for the prover of an inner-product argument"""

from fastecdsa.curve import secp256k1, Curve
from bulletproof.utils.utils import mod_hash, point_to_b64, ModP
from bulletproof.pippenger import PipSECP256k1

SUPERCURVE: Curve = secp256k1


class Proof1:
    """Proof class for Protocol 1"""

    def __init__(self, u_new, P_new, proof2, transcript):
        self.u_new = u_new
        self.P_new = P_new
        self.proof2 = proof2
        self.transcript = transcript

    def to_dict(self):
        """Convert the Proof1 instance to a dictionary."""
        return {
            "u_new": self.u_new,
            "P_new": self.P_new,
            "proof2": self.proof2.to_dict() if hasattr(self.proof2, "to_dict") else self.proof2,
            "transcript": self.transcript
        }

class Verifier1:
    """Verifier class for Protocol 1"""

    def __init__(self, g, h, u, P, c, proof1):
        self.g = g
        self.h = h
        self.u = u
        self.P = P
        self.c = c
        self.proof1 = proof1

    def to_dict(self):
        return {
            "g": self.g,
            "h": self.h,
            "u": self.u,
            "P": self.P,
            "c": self.c,
            "proof1": self.proof1,
        }
    def assertThat(self, expr: bool):
        """Assert that expr is truthy else raise exception"""
        if not expr:
            raise Exception("Proof invalid")
           # print("Proof invalid")
    def verify_transcript(self):
        """Verify a transcript to assure Fiat-Shamir was done properly"""
        lTranscript = self.proof1.transcript.split(b"&")
        self.assertThat(
            lTranscript[1]
            == str(mod_hash(b"&".join(lTranscript[:1]) + b"&", SUPERCURVE.q)).encode()
        )

    def verify(self):
        """Verifies the proof given by a prover. Raises an execption if it is invalid"""
        self.verify_transcript()

        lTranscript = self.proof1.transcript.split(b"&")
        x = lTranscript[1]
        x = ModP(int(x), SUPERCURVE.q)
        # P‘=P*u**(x*c)
        self.assertThat(self.proof1.P_new == self.P + (x * self.c) * self.u)
        # u=u**x
        self.assertThat(self.proof1.u_new == x * self.u)

        Verif2 = Verifier2(
            self.g, self.h, self.proof1.u_new, self.proof1.P_new, self.proof1.proof2
        )

        return Verif2.verify()


class Proof2:
    """Proof class for Protocol 2"""

    def __init__(self, a, b, xs, Ls, Rs, transcript, start_transcript: int = 0):
        self.a = a
        self.b = b
        self.xs = xs
        self.Ls = Ls
        self.Rs = Rs
        self.transcript = transcript
        self.start_transcript = (
            start_transcript
        )  # Start of transcript to be used if Protocol 2 is run in Protocol 1

    def to_dict(self):
        """Convert the Proof2 instance to a dictionary."""
        return {
            "a": self.a,
            "b": self.b,
            "xs": self.xs,
            "Ls": self.Ls,
            "Rs": self.Rs,
            "transcript": self.transcript,
            "start_transcript": self.start_transcript
        }

class Verifier2:
    """Verifier class for Protocol 2"""

    def __init__(self, g, h, u, P, proof: Proof2):
        self.g = g
        self.h = h
        self.u = u
        self.P = P
        self.proof = proof

    def to_dict(self):
        return {
            "g": self.g,
            "h": self.h,
            "u": self.u,
            "P": self.P,
            "proof": self.proof,
        }

    def assertThat(self, expr):
        """Assert that expr is truthy else raise exception"""
        if not expr:
            raise Exception("Proof invalid")
            # print("Proof invalid")

    def get_ss(self, xs):
        """See page 15 in paper"""
        n = len(self.g)
        log_n = n.bit_length() - 1  # g的长度的比特长度
        ss = []
        for i in range(1, n + 1):
            tmp = ModP(1, SUPERCURVE.q)
            for j in range(0, log_n):
                b = 1 if bin(i - 1)[2:].zfill(log_n)[j] == "1" else -1
                tmp *= xs[j] if b == 1 else xs[j].inv()
            ss.append(tmp)
        return ss

    def verify_transcript(self):
        """Verify a transcript to assure Fiat-Shamir was done properly"""
        init_len = self.proof.start_transcript
        n = len(self.g)
        log_n = n.bit_length() - 1  # g的比特长度
        Ls = self.proof.Ls
        Rs = self.proof.Rs
        xs = self.proof.xs  # innerproof中生成的随机数字
        lTranscript = self.proof.transcript.split(b"&")
        for i in range(log_n):
            self.assertThat(lTranscript[init_len + i * 3] == point_to_b64(Ls[i]))
            self.assertThat(lTranscript[init_len + i * 3 + 1] == point_to_b64(Rs[i]))
            self.assertThat(
                str(xs[i]).encode()
                == lTranscript[init_len + i * 3 + 2]
                == str(
                    mod_hash(
                        b"&".join(lTranscript[: init_len + i * 3 + 2]) + b"&",
                        SUPERCURVE.q,
                    )
                ).encode()
            )

    def verify(self):
        """Verifies the proof given by a prover. Raises an execption if it is invalid"""
        self.verify_transcript()

        proof = self.proof
        Pip = PipSECP256k1
        ss = self.get_ss(self.proof.xs)
        LHS = Pip.multiexp(
            self.g + self.h + [self.u],
            [proof.a * ssi for ssi in ss]
            + [proof.b * ssi.inv() for ssi in ss]
            + [proof.a * proof.b],
        )
        RHS = self.P + Pip.multiexp(
            proof.Ls + proof.Rs,
            [xi ** 2 for xi in proof.xs] + [xi.inv() ** 2 for xi in proof.xs],
        )

        self.assertThat(LHS == RHS)
        print("ok")
        return True
