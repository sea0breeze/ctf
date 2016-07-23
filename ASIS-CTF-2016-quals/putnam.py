from hashlib import sha1

def check(flag): # These bignums are hard-coded and can be known using gdb, this function is at 0x402B26
    tmp = flag + 927000317028443242660218700625015177618729308292
    tmp1 = 58083098340436592572428949667026971680998552113001298964050042091817127554826077890574096402833663439016381224578837061641047295828109375 % tmp
    tmp4 = pow(flag, 3, tmp)
    v7 = (tmp4 + tmp1) % tmp
    return v7

# There are factors of a bignum, but it seems factoring is not needed...
f = '17 41 1277 201812749 5114084777490587 79446245382102257493817667075063441 10915057861749906024158514424195715948375317244103006997979908370684387984168819'.split()
f = map(int,f)
from itertools import combinations
for i in range(1, len(f)+1):
    for k in combinations(f, i):
        tmp = reduce(lambda x,y: x*y, k) - 927000317028443242660218700625015177618729308292
        assert check(tmp) == 0
        if tmp > 0:
            flag = hex(tmp)[2:].strip('L')
            if len(flag) % 2 != 0:
                flag = '0'+flag
            if 'f8502be39225bb1bcaf0d3591da722ca541162fc' == sha1(flag.decode('hex')).hexdigest():
                print flag.decode('hex')
