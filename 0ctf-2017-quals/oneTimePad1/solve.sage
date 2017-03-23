#!/usr/bin/env sage
# coding=utf-8

from sage.all import *

def str2num(s):
    return int(s.encode('hex'), 16)

P.<x> = GF(2^256)

m = [None, "I_am_not_a_secret_so_you_know_me", "feeddeadbeefcafefeeddeadbeefcafe"]
c = []
f = open("./ciphertext")
for line in f:
    c.append(int(line.strip(),16))

k2 = P.fetch_int(c[2] ^^ str2num(m[2]))
k1 = P.fetch_int(c[1] ^^ str2num(m[1]))
k = k2 + (k1 * k1)
k0 = (k1 + k).sqrt()
print hex(k0.integer_representation() ^^ c[0])[2:].strip('L').decode('hex')
