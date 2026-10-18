# Recall

**Category:** crypto
**Difficulty:** medium

Textbook CRT-RSA (1024-bit, e = 65537).

A "cold-boot dump" leaks the all but the low 235 bits of both `dp` and `dq`. Player must turn that into a factorisation of `N`
and decrypt the unpadded ciphertext.