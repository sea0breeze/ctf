import string
import pickle
from pwn import *
from hashlib import sha256
from subprocess import check_output
import random

context.log_level='debug'

def dopow():
    tab=string.ascii_letters+string.digits
    c.recvuntil('with ')
    pre=c.recv(10)
    print pre
    i=0
    while True:
        cur=''.join(random.sample(tab,6))
        if sha256(pre+cur).hexdigest()[-6:] == ('ffffff'):
            return pre+cur
        i+=1

c = remote('lcg.chal.pwning.xxx',6051)
work=dopow()
c.sendline(work)
'''
c = remote('127.0.0.1', 6051)
'''
c.recvuntil('seconds.\n')
#oracle = c.recvline().strip()
#m,a,b,state = map(int,oracle.split(' ')[1:])
stat = c.recvline().strip()
stat = map(int,stat.split(' ')[1:])
assert len(stat)==40
f=open('lcg_stats','w')
pickle.dump(stat,f)
f.close()

import os
print 'Ready to sage'
raw_input()

with open('output') as f:
    m, a, diff, s0 = pickle.load(f)
d = diff[-1]

for i in range(200):
    d = d * a % m
    s0 = (s0 + d) % m
    output = s0 >> 96
    c.sendline(str(output))
    print c.recvline()

c.recv()
c.interactive()
