#!/usr/bin/env sage
# coding=utf-8

from hashlib import sha1

'''
The paper about this attack is attached in git.
It seems that the attack works whether it is ECDSA or DSA.
'''

q = 0x100000000000000000001f4c8f927aed3ca752257
d = 80
l = 5
bound = q / (2 ** (l+1))
# h = int(sha1('1').hexdigest(), 16)
h = 304942582444936629325699363757435820077590259883
t = []
u = []

for line in open('datas'):
    r, s, a = map(Zmod(q), line.strip().split(', '))
    tt = (r / s) / (2**l)
    tt = tt.lift()
    uu = (a - h / s) / (2**l)
    uu = uu.lift() + bound
    if uu >= q:
        uu -= q
    t.append(tt)
    u.append(uu)

m = []
for i in range(d):
    tmp = [0] * (d+2)
    tmp[i] = q
    m.append(tmp)
m.append(t+[1/(2**(l+1)), 0])
m.append(u+[0, bound])

ma = matrix(QQ, m)
print 'Ready to LLL...'
mb = ma.LLL()

flag_num = -mb[1][-2] * (2**(l+1))
print hex(int(flag_num))[2:].rstrip('L').decode('hex')
