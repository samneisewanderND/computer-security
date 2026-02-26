def rsa_enc(pt: list[int], n: int, e: int) -> list[int]:
    return [pow(m, e, n) for m in pt]


def rsa_dec(ct: list[int], n: int, d: int) -> list[int]:
    return [pow(x, d, n) for x in ct]


def main():
    bob_n = 77
    bob_e = 17
    bob_d = 53
    mary_n = 77
    mary_e = 37
    mary_d = 13

    pt_ord = [1, 17, 8, 6, 7, 19]
    print(pt_ord)
    c1 = rsa_enc(pt_ord, bob_n, bob_d)
    print(c1)
    c2 = rsa_enc(c1, mary_n, mary_e)
    print(c2)
    p1 = rsa_dec(c2, mary_n, mary_d)
    print(p1)
    p2 = rsa_dec(p1, bob_n, bob_e)
    print(p2)


main()
