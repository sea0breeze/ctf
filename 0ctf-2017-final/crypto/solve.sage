from sage.all import *

'''
Reference:
https://github.com/mimoo/RSA-and-LLL-attacks
https://gist.github.com/elliptic-shiho/ea5047587ee4e6d4b256a0b10750a8b3
https://gist.github.com/hellman/4b2897a857a5ec91d9ea965d87b795c8
'''

def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += ' ' if BB[ii,jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print a

with open('private.key') as f:
    e, d, p1, q1, p2, q2, k1, y1 = eval(f.read())

n1 = p1 * q1
n2 = p2 * q2
s1 = p1 + q1 - 1
s2 = p2 + q2 - 1

assert int(pow(pow(0xdeadbeef, e, n1), d)) == 0xdeadbeef
assert int(pow(pow(0xdeadbeef, e, n2), d)) == 0xdeadbeef

ne = e.bit_length()
nd = d.bit_length()
n = max(n1.bit_length(), n2.bit_length())
print '[+]bit length of n: %d\n[+]bit length of e: %d\n[+]bit length of d: %d' % (n, ne, nd)
print '[+]e:', e
print '[+]N1:', n1
print '[+]N2:', n2
# assert 0

assert k1 < 2^nd and y1 < 2^nd

a = 2^(n//2)
l1 = matrix([[a, e], [0, n1]])
l1 = l1.LLL()
print '[+]bit length of l:', map(lambda x: int(x).bit_length(), list(l1[0])+list(l1[1])), "(They should be around %d)" % floor(n*(3/4))

v = vector([a*d, 1-k1*s1])
v_a = l1.solve_left(v)
print '[+]bit length of a:', map(lambda x: int(x).bit_length(), v_a), "(They should be no more than %d)" % ceil(nd-n/4)

l11 = l1[0][0]
l21 = l1[1][0]
assert l11 % a == 0 and l21 % a == 0
l11 //= a
l21 //= a

modulus = e * l21
P.<x, y, z> = PolynomialRing(ZZ)
pol = x * (n2-y) - e*l11*z + 1

# Here comes the important part!
mm = 4
tt = 1
XX = 2^nd
YY = 2^((n+1)//2+1)
ZZ_ = 2^ceil(nd-n/4)
assert y1 < XX 
assert s2 < YY
assert v_a[0] < ZZ_
assert (pol(x=y1, y=s2, z=v_a[0])) % modulus == 0
print '[+]roots:', (y1, s2, v_a[0])
print '[+]modulus:', modulus

PR.<u, x, y, z> = PolynomialRing(ZZ)
Q = PR.quotient(x*y - 1 - u)
polz = Q(pol).lift()
print '[+]target poly:', polz

UU = XX*YY - 1

gg = []
for kk in range(mm+1):
    for ii in range(mm+1-kk):
        for jj in range(mm+1-kk-ii):
            poly = x^ii * z^jj * polz^kk * modulus^(mm-kk)
            gg.append(poly)

hh = []
for jj in range(1, tt+1):
    for kk in range(floor(mm/tt)*jj, mm+1):
        for ll in range(kk+1):
            poly = y^jj * z^(kk-ll) * polz^ll * modulus^(mm-ll)
            poly = Q(poly).lift()
            hh.append(poly)

monomials = []
polys = sorted(gg+hh)
for poly in polys:
    monomials += poly.monomials()
monomials = sorted(set(monomials))
print '[+]list of monomials:', monomials
print len(monomials), len(polys)
assert len(monomials) == len(polys)
dim = len(polys)
M = matrix(ZZ, dim)
for ii in xrange(dim):
    M[ii, 0] = polys[ii](0, 0, 0, 0)
    for jj in xrange(dim):
        if monomials[jj] in polys[ii].monomials():
            M[ii, jj] = polys[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU, XX, YY, ZZ_)
matrix_overview(M, dim)
print ''
print '=' * 128
print ''

B = M.LLL()
matrix_overview(B, dim)

PS.<xs, ys, zs> = PolynomialRing(QQ)
xs, ys, zs = PS.gens()
hs = []
for ii in range(dim):
    pol = 0
    for jj in range(dim):
        pol += monomials[jj](xs*ys-1, xs, ys, zs) * B[ii, jj] / monomials[jj](UU, XX, YY, ZZ_)
    assert pol(xs=y1, ys=s2, zs=v_a[0]) % modulus == 0
    if pol(xs=y1, ys=s2, zs=v_a[0])  == 0:
        print "Got poly with good root over ZZ. (Vector %d)" % ii
        hs.append(pol)

pset = PS.ideal(hs)
assert pset.dimension() == 0
print "[+]Well done! It's solvable!"
proot = pset.variety()[0]
print "[+]Got root:", proot
print "[+]d should be:", d
dd = (proot['xs'] * (n2 - proot['ys']) + 1) // e
print "[+]what we compute is:", dd
