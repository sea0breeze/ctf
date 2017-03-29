#!/usr/bin/env python
# coding=utf-8

table1 = [2519479749, 882775218, 1423990682, 588921374, 1832875373, 2787014706, 1644446493, 4145957705, 4003550880, 1201359790, 52328806, 3815793521, 3746052287, 2776562778, 2165735275, 2970579843, 1125563752, 376534782, 2526561353, 918384088, 500007583, 3341944108, 2096269325, 1043419796, 3554651348, 3970926008, 2290989021, 48486030, 499483490, 3867123687, 2689685039, 858422008, 2864756522, 1986642315]

table2 = [657800374, 909907066, 3699292052, 4095130001, 1424314379, 2589740212, 838473182, 2659734325, 2489071715, 2536617442, 726959802, 3382419106, 2547873521, 3083836440, 811431237, 1676056497, 2189369980, 543636498, 3306810483, 3679982497, 816452217, 823515817, 928870791, 1328426388, 410290954, 1225528300, 386220600, 13164700, 1340483833, 3423913261, 535908089, 423076688, 2072682706, 3395541267]

def encrypt(t1, iv, tid):
    left = (t1[0] + iv) & 0xffffffff
    right = (t1[1] + tid) & 0xffffffff

    for i in range(1, 0x11):
        j = 2 * i
        tmp = left ^ right
        rol = right & 0x1f
        v11 = ((tmp << rol) | (tmp >> (32 - rol))) & 0xffffffff
        left = (t1[j] + v11) & 0xffffffff
        tmp = left ^ right
        rol = left & 0x1f
        v12 = ((tmp << rol) | (tmp >> (32 - rol))) & 0xffffffff
        right = (t1[j|1] + v12) & 0xffffffff

    return (right << 32) | left

def decrypt(t, block):
    left, right = unpack('2I', block)
    for i in range(16, 0, -1):
        j = i << 1
        v12 = (right + (1 << 32) - t[j|1]) & 0xffffffff
        rol = left & 0x1f
        tmp = ((v12 >> rol) | (v12 << (32 - rol))) & 0xffffffff
        right = tmp ^ left
        v11 = (left + (1 << 32) - t[j]) & 0xffffffff
        rol = right & 0x1f
        tmp = ((v11 >> rol) | (v11 << (32 - rol))) & 0xffffffff
        left = tmp ^ right
    left = (left + (1 << 32) - t[0]) & 0xffffffff
    right = (right + (1 << 32) - t[1]) & 0xffffffff

    return (right << 32) | left

from struct import unpack, pack

def enc(name, iv):
    with open(name, 'rb') as f:
        plain = f.read()
    plain = plain + '\x80'
    plain = plain + (8 - len(plain) & 7) * '\x00'
    plen = len(plain) / 8
    res = ''
    for i in xrange(plen):
        if (i & 3) == 3:
            res += plain[i<<3:(i<<3)+8]
            continue
        key = encrypt(table1, iv, i)
        a, b = unpack('2I', plain[i<<3:(i<<3)+8])
        tmp = encrypt(table2, a, b)
        # print hex(key), hex(tmp)
        res += pack('Q', key ^ tmp)
    return res

def dec(name):
    with open(name, 'rb') as f:
        iv = unpack('I', f.read(4))[0]
        c = f.read()
    clen = len(c) / 8
    res = ''
    for i in range(clen):
        if (i & 3) == 3:
            res += c[i<<3:(i<<3)+8]
            continue
        key = encrypt(table1, iv, i)
        m = unpack('Q', c[i<<3:(i<<3)+8])[0] ^ key
        m = decrypt(table2, pack('Q', m))
        res += pack('Q', m)
    return res.rstrip('\x00')[:-1]

with open('./ciphertext.zip', 'wb+') as f:
    f.write(dec('ciphertext.zip.enc'))
