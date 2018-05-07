'''https://link.springer.com/chapter/10.1007/11506157_5'''
def pgcd(f, g, n):
    gp = Gp(stacksize=1024*1024*512)
    gp.set('g','gcd(Mod({},{}),Mod({},{}))'.format(pols[0],n,pols[1],n))
    print gp.get('g')
    res = gp('liftall(-Vec(g / Vec(g)[1])[2])')
    return int(res)

from gen import init_test

# mm, aa, bb, _, test = init_test()
import pickle
with open('lcg_stats') as f:
    test = pickle.load(f)


cnt = len(test)
x = []
y = []
for i in range(cnt-1):
    y.append(test[i+1]-test[i])
    # x.append(state[i+1]-state[i])
# for i in range(cnt-2):
#     assert (x[i+1] - a * x[i]) % m == 0

t = 6
# n = ceil(8*sqrt(t))
n = 40 - t
bb = float(32 + log(n, 2) + 1) * t / (n - t)

ys = []
xs = []
ym = []
for i in range(n):
    tmp = [0] * n
    tmp[i] = 1
    ys.append(y[i:i+t])
    # xs.append(x[i:i+t])
    # ym.append([j*K for j in y[i:i+t]]+tmp)

# xs = matrix(xs)
ys = matrix(ys)
lam = ys.left_kernel().matrix().LLL()
kk = lam.nrows()
# print n, kk, bb
# print lam

pols = []
P.<z> = ZZ[]
for sol in lam:
    pol = 0
    for i, k in enumerate(sol):
        pol += k * (z**(i))
    # print pol
    pols.append(pol)
    # print sol * xs
    # print sol * ys
    # print '---------'

rs = []
for i in range(12):
    rs.append(pols[i].resultant(pols[i+1]))
m0 = gcd(rs)
print 'm', m0
# assert mm == m0
m = m0

# pols = map(lambda i: i.change_ring(Zmod(m0)), pols)
f = pols[0]
g = pols[1]
ms = []
other_m = 1
tmp = m
while 1:
    flag = 1
    for i in f.coeffs():
        i = abs(i)
        if i in (0, 1):
            continue
        gcd_res = gcd(i, tmp)
        # print 'i', i, gcd_res
        if gcd_res == i:
            print 'gg', i
            ms.append(gcd_res)
            other_m *= gcd_res
            tmp //= gcd_res
            flag = 0
    for i in g.coeffs():
        i = abs(i)
        if i in (0, 1):
            continue
        gcd_res = gcd(i, tmp)
        # print 'i', i, gcd_res
        if gcd_res == i:
            print 'gg', i
            ms.append(gcd_res)
            other_m *= gcd_res
            tmp //= gcd_res
            flag = 0
    # print 'again', flag, tmp
    if flag:
        break
ms.append(tmp)

am = []
for i in ms:
    tmpf = f.change_ring(Zmod(i))
    tmpg = g.change_ring(Zmod(i))
    am.append(pgcd(f, g, i))
print ms
print am
a0 = CRT_list(am, ms)
# assert a0 == aa
print 'a', a0
a = a0


num = 39
Y = [i * (2^96) for i in y]

row = [m] + [0]*(num-1)
mat=[row]
for i in range(1,num):
    row = [(a^i)%m] + [0]*(num-1)
    row[i] = -1
    mat.append(row)

print len(mat), len(mat[0])
L = matrix(mat)

B = L.LLL()

W1 = B * vector(Y)
W2 = vector([ round(RR(w) / m) * m - w for w in W1 ])

Z_ = list(B.solve_right(W2))
print 'Y', Y[0]
print 'Z', Z_[0]
X_ = list([0]*num)
for i in range(num):
    X_[i] = Y[i]+Z_[i]
print 'X', X_[0]
# print 'true', x[0]

new_test = [i*(2^96) for i in test]

l = new_test[39]
h = new_test[39] + (1<<96) - 1
for i in range(38, -1, -1):
    l -= X_[i]
    h -= X_[i]
    if l < new_test[i]:
        l = new_test[i] 
    if h > new_test[i] + (1<<96) - 1:
        h = new_test[i] + (2^96) - 1
print l, h
for i in X_:
    l += i
    h += i
s0 = (l + h) / 2
with open('output', 'w') as f:
    pickle.dump((int(m), int(a), map(int, X_), int(s0)), f)
