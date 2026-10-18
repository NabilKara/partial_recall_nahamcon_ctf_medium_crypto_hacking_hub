# Partial Recall's Writeup

**Category:** crypto 
**Difficulty:** medium

## 1. What we are given

`chall.py` is plain textbook RSA with CRT:

```python
n  = p * q
d  = inverse(E, (p - 1) * (q - 1))
dp, dq = d % (p - 1), d % (q - 1)
c  = pow(m, E, n)              
dp_high = dp >> UNKNOWN_BITS
dq_high = dq >> UNKNOWN_BITS
```

The leak is a contiguous block of most-significant bits.



## 2. From `dp` to a polynomial

Since `e·dp ≡ 1 (mod p-1)`, there is an integer `kp` with

```
e·dp = 1 + kp·(p-1)        where 1 ≤ kp < e
```

so `e·dp - 1 + kp = kp·p`, which is `0 mod p`. Write `dp = a + x`, where `a = dp_high · 2^235` is known and
`0 ≤ x < 2^235` is the lost part. Multiplying by `e⁻¹ mod N` makes the polynomial monic:

```
f(x) = x + A       with  A = a + e⁻¹·(kp - 1)  (mod N)         f(x) ≡ 0 (mod p)
```

We don't know `p`, but it divides the known `N`. Finding a small root of a polynomial modulo an unknown divisor of
`N` is exactly what Coppersmith's method solves.

## 3. Finding the root

```python
roots = cuso.find_small_roots(
    relations=[x + A],
    bounds={x: (0, 2**235)},
    modulus="p",
    modulus_multiple=N,
    modulus_lower_bound=2**511,
    modulus_upper_bound=2**512,
)
p = int(roots[0]["p"])
```


## 4. The unknown `kp`

kp < 65537, so try every value.

A faster way would be to use both leaks :
`dq` obeys the same relation, `e·dq = 1 + kq·(q-1)`. Multiplying the two relations gives

```
(e·dp - 1)(e·dq - 1) = kp·kq·(p-1)(q-1)  ≈  kp·kq·N
```

we approximate `dp` and `dq` with the known
part plus the middle of the unknown range (`dp₀`, `dq₀`):

```
K = kp·kq = round( (e·dp₀ - 1)(e·dq₀ - 1) / (N - 2·√N + 1) )
```

`K` is a whole number below 2³², and the approximation error is around 10⁻⁷⁴, so the rounding gives exactly
`kp·kq`. Then:

1. Factor `K` and list the pairs `(kp, kq)` with `kp·kq = K` and both below `e`.
2. keep only the two pairs that satisfy the congruence :  `(kp - 1)(kq - 1) ≡ kp·kq·N (mod e)`.
3. the right pair gives `p`.

## 5. Finish

```python
q = N // p
d = pow(e, -1, (p - 1) * (q - 1))
m = pow(c, d, N)
print(m.to_bytes((m.bit_length() + 7) // 8, "big"))
```

```
flag{17d4a39935c3b205c8c846365327e4f7656f11}
```