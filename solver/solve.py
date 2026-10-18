#!/usr/bin/env python3
from math import isqrt

import cuso
from sage.all import Integer, var

N = 141070733942427662847364310169519836277853357721568389686723564833539278764856395540207547187135222725952716795407994343733822644248356085445895343929500319027494468537551593972483575556657574468334396459954917093116006080801699945317922195536482971392150710230766390234029623934605694599058166480175447472621
e = 65537
c = 89388024804412138464333182254996404487264779011278420087225246950512958910690642564995894006642903517029493626582160016284593473677375935793030944309660927606730450657387851383096379414913182703780149736063153178772256618478589851010396703726896743916492801857618352031604858273380647170501547638490539859279
dp_high = 130674939832039229147966903478926083144968760837300654872637835352220594986661183447
dq_high = 86921953141440313208777624921721208793819203385750442239818510262511909226302558963

UNKNOWN_BITS = 235

x = var("x")


def kp_candidates():
    
    dp = (dp_high << UNKNOWN_BITS) + (1 << (UNKNOWN_BITS - 1))   
    dq = (dq_high << UNKNOWN_BITS) + (1 << (UNKNOWN_BITS - 1))
    num = (e * dp - 1) * (e * dq - 1)
    den = N - 2 * isqrt(N) + 1
    K = (2 * num + den) // (2 * den)
    print(f"kp*kq = {K}")

    pairs = [(int(k), K // int(k)) for k in Integer(K).divisors()]
    return [kp for kp, kq in pairs
            if kp < e and kq < e and ((kp - 1) * (kq - 1) - kp * kq * N) % e == 0]


def find_p(kp):
    A = ((dp_high << UNKNOWN_BITS) + pow(e, -1, N) * (kp - 1)) % N
    roots = cuso.find_small_roots(
        relations=[x + A],
        bounds={x: (0, 1 << UNKNOWN_BITS)},
        modulus="p",
        modulus_multiple=N,
        modulus_lower_bound=1 << 511,
        modulus_upper_bound=1 << 512,
    )
    for r in roots:
        if N % int(r["p"]) == 0:
            return int(r["p"])


for kp in kp_candidates():
    p = find_p(kp)
    if p:
        break

q = N // p
d = pow(e, -1, (p - 1) * (q - 1))
m = pow(c, d, N)
print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())