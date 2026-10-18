#!/usr/bin/env python3
from math import gcd

from Crypto.Util.number import getPrime, bytes_to_long, inverse

E = 65537
BITS = 1024
UNKNOWN_BITS = 235


def keygen():
    while True:
        p, q = getPrime(BITS // 2), getPrime(BITS // 2)
        if p != q and gcd(E, (p - 1) * (q - 1)) == 1 and (p * q).bit_length() == BITS:
            return p, q


def encrypt(m, n):
    return pow(m, E, n)


def decrypt_crt(c, p, q, dp, dq):
    mp = pow(c, dp, p)
    mq = pow(c, dq, q)
    h = (inverse(q, p) * (mp - mq)) % p
    return mq + h * q



flag = open("flag.txt", "rb").read().strip()
p, q = keygen()
n = p * q
d = inverse(E, (p - 1) * (q - 1))
dp, dq = d % (p - 1), d % (q - 1)
m = bytes_to_long(flag)
assert m < n
c = encrypt(m, n)
assert decrypt_crt(c, p, q, dp, dq) == m
# what survived the cold boot: everything except the low UNKNOWN_BITS bits
dp_high = dp >> UNKNOWN_BITS
dq_high = dq >> UNKNOWN_BITS
with open("output.txt", "w") as f:
    f.write(f"N = {n}\n")
    f.write(f"e = {E}\n")
    f.write(f"c = {c}\n")
    f.write(f"dp_high = {dp_high}\n")
    f.write(f"dq_high = {dq_high}\n")