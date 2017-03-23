#!/usr/bin/sage
# coding=utf-8

from sage.all import *
from struct import *
f = open('s16384','rb')
ff = f.read()
f.close()
pos1 = 0x12080
pos2 = 0x2080
result = unpack('16384i',ff[pos1:pos1+16384*4])
base = list(unpack('16384i',ff[pos2:pos2+16384*4]))
G = SymmetricGroup(16384)
x = G([i+1 for i in base])
y = G([i+1 for i in result])

cyclex = x.cycles()
cycley = y.cycles()
assert len(cyclex) == len(cycley)

exp = []
order = []
for i in range(len(cyclex)):
    xi = cyclex[i]
    yi = cycley[i]
    tmp = xi
    order.append(xi.order())
    expi = 1
    while tmp != yi:
        expi += 1
        tmp *= xi
    exp.append(expi)

print CRT_list(exp,order)
