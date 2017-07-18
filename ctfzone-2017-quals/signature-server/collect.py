#!/usr/bin/env python
# coding=utf-8

from pwn import *

debug = False

if debug:
    r = remote('127.0.0.1', 1337)
    f = open('locals', 'w')
else:
    r = remote('185.143.173.36', 1337)
    f = open('datas', 'w')

for i in range(80):
    if i % 5 == 0:
        print i
    r.recvuntil('-> ')
    r.sendline('s')
    r.sendlineafter('sign: ', '1')
    f.write(r.recvline())

r.close()
f.close()
