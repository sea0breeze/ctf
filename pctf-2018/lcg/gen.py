#!/usr/bin/env python
# coding=utf-8

import binascii
import os

N = 128
assert N % 8 == 0
OUTPUT = 32
HIDDEN = N-OUTPUT

def gcd(u, v):
    while v:
        u, v = v, u % v
    return abs(u)

def nextstate(state, mult, inc, modulus):
    return (state*mult + inc) % modulus

def init_test():
    while 1:
        m = int(binascii.hexlify(os.urandom(N // 8)), 16)
        a = 0
        b = 0
        s = 0
        while not (1 <= a < m and gcd(a, m) == 1):
            a = int(binascii.hexlify(os.urandom(N // 8)), 16)
        while not (1 <= b < m and gcd(b, m) == 1):
            b = int(binascii.hexlify(os.urandom(N // 8)), 16)
        while not (1 <= s < m):
            s = int(binascii.hexlify(os.urandom(N // 8)), 16)

        x = []
        y = []
        for i in xrange(40):
            y.append(s>>HIDDEN)
            x.append(s)
            s = nextstate(s, a, b, m)
        if gcd(x[1]-x[0], m) == 1:
            break
        else:
            print "Fail init"
    return m, a, b, x, y
