#!/usr/bin/env sage
# coding=utf-8

proof.arithmetic(False)

threshold = 21 << 1018 # just chosen arbitrarily:)

def genKey(n, nd):
    '''
    Designed with the awesome idea that generating two RSA key pairs
    that have the same public and private exponents to reduce the
    storage requirements!
    '''

    assert n/2 > nd
    tmp = n/2 - nd
    
    while True:
        while True:
            x1 = randrange(2^(nd-1), 2^nd)
            x2 = randrange(2^(tmp-1), 2^tmp)
            p1 = x1*x2 + 1
            if p1.is_prime():
                print '[+]bit length of p1:', int(p1).bit_length()
                break

        while True:
            y2 = randrange(2^(tmp-1), 2^tmp)
            p2 = x1*y2 + 1
            if p2.is_prime():
                print '[+]bit length of p2:', int(p2).bit_length()
                break

        while True:
            y1 = randrange(2^(nd-1), 2^nd)
            q1 = y1*y2 + 1
            if q1.is_prime():
                print '[+]bit length of q1:', int(q1).bit_length()
                break

        count = 0
        while True:
            d = randrange(2^(nd-1), 2^nd)
            if gcd(x1*x2*y1*y2, d) != 1:
                continue
            e = int(1/Mod(d, (p1-1)*(q1-1)))
            k1 = (e*d - 1) // ((p1-1)*(q1-1))
            assert e*d == (p1-1)*(q1-1)*k1 + 1
            q2 = k1*x2 + 1
            if q2.is_prime():
                print '[+]bit length of q2:', int(q2).bit_length()
                break
        n1 = p1 * q1
        n2 = p2 * q2
        n1, n2 = max([n1, n2]), min([n1, n2])
        if n1 <= threshold:
            print '[+]N for encryptions is too small!'
            continue
        if n2 >= threshold:
            print '[+]N for signatures is too large!'
            continue
        break

    assert int(pow(pow(0xdeadbeef, e, n1), d)) == 0xdeadbeef
    assert int(pow(pow(0xdeadbeef, e, n2), d)) == 0xdeadbeef
    return (e, d, n1, n2)

if __name__ == '__main__':
    print genKey(1024, 342)
