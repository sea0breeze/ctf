#!/usr/bin/env sage
# coding=utf-8

from sage.all import *

p.<x> = GF(2^128)

print 'Start'
c = file("./ciphertxt").read().strip()
m = "One-Time Pad is used here. You won't know that the flag is flag{".encode('hex')

x = []
for i in range(0, len(m), 32):
    ci = int(c[i:i+32], 16)
    print ci
    mi = int(m[i:i+32], 16)
    x.append(p.fetch_int(ci^^mi))

a = p.fetch_int(264046295839861049478585915471640894461L)
k = p.fetch_int(139842438333098917680069068063480255258L)

n = []
for i in range(len(x)-1):
    n.append((x[i+1]+k)/(x[i]+k))

print "Log start."
e = []
for i in n:
    print 'try...'
    e.append(i.log(a))

print [i for i in e]
e0 = e[-1]
e1 = (p.fetch_int(e0)**2).integer_representation()
xx = (x[-1]+k)*(a**e1)+k
xx = xx.integer_representation()

print xx
print hex(xx^^int(c[-64:-32], 16))[2:-1].decode('hex')
