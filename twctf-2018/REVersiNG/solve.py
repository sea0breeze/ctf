#!/usr/bin/env python
# coding=utf-8

from pwn import *
from struct import unpack

def xor(a):
    a = bytearray(a)
    b = bytearray('KNOWN_PLAIN_TEXT'*8)
    return str(bytearray([i^j for i,j in zip(a,b)]))

def getkey(k):
    # r = process(['qemu-mips', '-L', '/usr/mips-linux-gnu', 'mips.elf'])
    r = remote('pwn1.chal.ctf.westerns.tokyo', 16625)
    r.send('\x00')
    r.send(p32(0x412320+k, endian='big'))
    rand = r.recvline().strip()
    # log.info(rand)
    rand = rand.decode('hex')
    c1 = r.recvline().strip()
    c2 = r.recvline().strip()
    # log.info(c1)
    # log.info(c2)
    c1 = xor(c1.decode('hex'))
    c2 = xor(c2.decode('hex'))
    i1 = unpack('>16I', c1[:64])
    i2 = unpack('>16I', c2[:64])
    res = [(i-j)&0xffffffff for i,j in zip(i1, i2)]
    res = [format(i, '08x') for i in res]
    res = ''.join(res).decode('hex')[k]
    log.info('%d: %s', k, repr(res))
    r.close()
    return res

if __name__ == '__main__':
    flag = ''
    for i in range(16, 48):
        flag += getkey(i)
    print flag.encode('hex')
