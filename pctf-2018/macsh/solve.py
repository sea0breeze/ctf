#!/usr/bin/env python
# coding=utf-8

from pwn import log, process, context, remote

# context.log_level = 'debug'
N = 16

def to_block(b):
    return '{:0{width}x}'.format(b, width=N*2).decode('hex')

def to_blocks(m):
    m += to_block(len(m))
    padb = N - len(m) % N
    m += chr(padb) * padb
    blocks = [m[N*i : N*(i+1)] for i in range(len(m) // N)]
    return blocks

# r = process('./macsh.py')
r = remote('macsh.chal.pwning.xxx', 64791)

def e(m, mac = '0'):
    global r
    r.sendlineafter('> ', mac+'<|>'+m)
    return r.recvline()


def test(cmd):
    global r

    echo = 'echo ' + '3' * (len(cmd)-5)
    p = 'tag ' + echo
    p1 = echo + '\x00' * (16-len(echo))
    p2 = cmd + '\x00' * (16-len(cmd))

    gg = 'tag ' + p1+'s'*(16*8-1)*16+p2+'s'*(16*8-1)*16
    res1 = e(gg)
    log.info(res1)
    res1 = int(res1, 16)

    gg = 'tag ' + p1+'s'*(16*8-1)*16+p1+'s'*(16*8-1)*16
    res2 = e(gg)
    log.info(res2)
    res2 = int(res2, 16)
    
    res3 = e(p)
    log.info(res3)
    res3 = int(res3, 16)
    log.info(e(cmd,mac = format(res1^res2^res3, 'x')))

test('cat flag.txt')
r.interactive()
