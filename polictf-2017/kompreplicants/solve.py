#!/usr/bin/env python
# coding=utf-8

from cStringIO import StringIO

def tob(c):
    res = bin(c)[2:]
    return res.rjust(8, '0')

with open('./flag.txt.short008', 'rb') as f:
    c = f.read()

tmp = map(ord, c)
raw = [tmp[0]]
# Every byte in the compressed file is actually a sum of previous bytes and the current byte of the true content!
for i in range(1, len(tmp)):
    raw.append((tmp[i]-tmp[i-1])%256)

# Get the conversion table of Huffman Coding
raw = ''.join(map(tob, raw))
raw = StringIO(raw)
table = {}
while True:
    size = int(raw.read(4), 2)
    if not size:
        break
    oldch = chr(int(raw.read(8), 2))
    newch = raw.read(size)
    table[newch] = oldch

print table

# Decode it and get the cute flag!
mes = ''
flag = 0
while True:
    bits = ''
    while True:
        bit = raw.read(1)
        if not bit:
            flag = 1
            break
        bits += bit
        if table.has_key(bits):
            mes += table[bits]
            break
    if flag:
        break
print mes
