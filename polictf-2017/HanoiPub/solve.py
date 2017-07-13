#!/usr/bin/env python
# coding=utf-8

from struct import unpack

str = bytearray("To beer or not to beer, that is the question")
offset = 0xf85
tmp_array = bytearray()

f = open('./hanoipub.bin', 'rb')
f.seek(offset)
index = 1
while 1:
    tmp = unpack('H', f.read(2))[0]
    if tmp is 1:
        break
    tmp = tmp / index - 0x30
    tmp ^= str[index-1]
    tmp_array.append(tmp)
    index += 1

print tmp_array
