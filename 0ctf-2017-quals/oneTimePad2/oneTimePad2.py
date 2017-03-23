#!/usr/bin/env python
# coding=utf-8

from os import urandom

def process1(m, k):
    res = 0
    for i in bin(k)[2:]:
        res = res << 1;
        if (int(i)):
            res = res ^ m
        if (res >> 128):
            res = res ^ P
    return res

def process2(a, b):
    res = []
    res.append(process1(a[0], b[0]) ^ process1(a[1], b[2]))
    res.append(process1(a[0], b[1]) ^ process1(a[1], b[3]))
    res.append(process1(a[2], b[0]) ^ process1(a[3], b[2]))
    res.append(process1(a[2], b[1]) ^ process1(a[3], b[3]))
    return res

def nextrand(rand):
    global N, A, B
    tmp1 = [1, 0, 0, 1]
    tmp2 = [A, B, 0, 1]
    s = N
    N = process1(N, N)
    while s:
        if s % 2:
            tmp1 = process2(tmp2, tmp1)
        tmp2 = process2(tmp2, tmp2)
        s = s / 2
    return process1(rand, tmp1[0]) ^ tmp1[1]


def keygen():
    key = str2num(urandom(16))
    while True:
        yield key
        key = nextrand(key)

def encrypt(message):
    length = len(message)
    pad = '\x00' + urandom(15 - (length % 16))
    to_encrypt = message + pad
    res = ''
    generator = keygen()
    f = open('key.txt', 'w') # This is used to decrypt and of course you won't get it.
    for i, key in zip(range(0, length, 16), generator):
        f.write(hex(key)+'\n')
        res += num2str(str2num(to_encrypt[i:i+16]) ^ key)
    f.close()
    return res

def decrypt(ciphertxt):
    # TODO
    pass

def str2num(s):
    return int(s.encode('hex'), 16)

def num2str(n, block=16):
    s = hex(n)[2:].strip('L')
    s = '0' * ((32-len(s)) % 32) + s
    return s.decode('hex')

P = 0x100000000000000000000000000000087
A = 0xc6a5777f4dc639d7d1a50d6521e79bfd
B = 0x2e18716441db24baf79ff92393735345
N = str2num(urandom(16))
assert N != 0

if __name__ == '__main__':
    with open('top_secret') as f:
        top_secret = f.read().strip()
    assert len(top_secret) == 16
    plain = "One-Time Pad is used here. You won't know that the flag is flag{%s}." % top_secret

    with open('ciphertxt', 'w') as f:
        f.write(encrypt(plain).encode('hex')+'\n')
