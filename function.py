from scipy.integrate import quad
import math as m

class RF:
    def __init__(self, f):
        self.f = f

    def __call__(self, x):
        return self.f(x)

    def __neg__(self):
        return RF(lambda x: -self.f(x))

    def __pow__(self, a):
        return RF(lambda x: self.f(x)**a)

    def __add__(self, other):
        if isinstance(other, RF):
            return RF(lambda x: self.f(x) + other.f(x))
        else:
            return RF(lambda x: self.f(x) + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self - other

    def __mul__(self, other):
        if isinstance(other, RF):
            return RF(lambda x: self.f(x) * other.f(x))
        else:
            return RF(lambda x: self.f(x) * other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return RF(lambda x: self.f(x) / other.f(x))

    def __rtruediv__(self, other):
        return self / other

    def __abs__(self):
        return RF(lambda x: abs(self.f(x)))

    def __matmul__(self, other):
        return RF(lambda x: self.f(other.f(x)))

    def integrate(self, a, b):
        return quad(self, a, b)[0]

    def linComb(cs, fs):
        if len(fs) < len(cs):
            raise ValueError('not enough functions')
        curf = RF.const(0)
        for i in range(len(cs)):
            curf = curf + (cs[i] * fs[i])
        return curf

    def scalar(f, g):
        return (f*g).integrate(0,1)

    def norm(f):
        #print(RF.scalar(f,f))
        return m.sqrt(RF.scalar(f,f))

    # standard functions
    def id():
        return RF(lambda x: x)

    def const(a):
        return RF(lambda x: a)

    def log(a):
        return RF(lambda x: m.log(x,a))

    def pow(a):
        return RF(lambda x: x**a)

    def sin():
        return RF(m.sin)

    def cos():
        return RF(m.cos)

    def exp():
        return RF(m.exp)

    def sqrt():
        return RF(m.sqrt)

    def ln():
        return RF(m.log)

    def tg():
        return RF(m.tan)

    def gamma():
        return RF(m.gamma)

'''
# standard polynomials
standard = [lambda x: 1, lambda x: x**1, lambda x: x**2, lambda x: x**3, lambda x: x**4, lambda x: x**5,
            lambda x: x**6, lambda x: x**7, lambda x: x**8, lambda x: x**9, lambda x: x**10]
standard = list(map(RF, standard))

d_standard = [lambda x: 0, lambda x: 1, lambda x: 2*x, lambda x: 3*x**2, lambda x: 4*x**3, lambda x: 5*x**4,
            lambda x: 6*x**5, lambda x: 7*x**6, lambda x: 8*x**7, lambda x: 9*x**8, lambda x: 10*x**9]
d_standard = list(map(RF, d_standard))


# Chebyshev polynomials
cheb = [lambda x: 1, lambda x: x, lambda x: 2*x**2-1, lambda x: 4*x**3-3*x, lambda x: 8*x**4-8*x**2+1, lambda x: 16*x**5-20*x**3+5*x,
        lambda x: 32*x**6-48*x**4+18*x**2-1, lambda x: 64*x**7-112*x**5+56*x**3-7*x, lambda x: 128*x**8-256*x**6+160*x**4-32*x**2+1]
cheb = list(map(RF, cheb))

d_cheb = [lambda x: 0, lambda x: 1, lambda x: 4*x, lambda x: 12*x**2-3, lambda x: 32*x**3-16*x, lambda x: 80*x**4-60*x**2+5,
          lambda x: 32*6*x**5-48*4*x**3+36*x, lambda x: 64*7*x**6-112*5*x**3+56*3*x**2-7, lambda x: 128*8*x**7-256*6*x**5+160*4*x**3-64*x]
d_cheb = list(map(RF, d_cheb))

cheb1 = [lambda x: 1, lambda x: x, lambda x: 2*x**2, lambda x: 4*x**3-3*x, lambda x: 8*x**4-8*x**2, lambda x: 16*x**5-20*x**3+5*x,
        lambda x: 32*x**6-48*x**4+18*x**2, lambda x: 64*x**7-112*x**5+56*x**3-7*x, lambda x: 128*x**8-256*x**6+160*x**4-32*x**2]
cheb1 = list(map(RF, cheb1))

d_cheb1 = [lambda x: 0, lambda x: 1, lambda x: 4*x, lambda x: 12*x**2-3, lambda x: 32*x**3-16*x, lambda x: 80*x**4-60*x**2+5,
          lambda x: 32*6*x**5-48*4*x**3+36*x, lambda x: 64*7*x**6-112*5*x**3+56*3*x**2-7, lambda x: 128*8*x**7-256*6*x**5+160*4*x**3-64*x]
d_cheb1 = list(map(RF, d_cheb1))

cheb2 = [lambda x: 1, lambda x: x, lambda x: 4*x**3-3*x, lambda x: 16*x**5-20*x**3+5*x,
        lambda x: 64*x**7-112*x**5+56*x**3-7*x]
cheb2 = list(map(RF, cheb2))

d_cheb2 = [lambda x: 0, lambda x: 1, lambda x: 12*x**2-3, lambda x: 80*x**4-60*x**2+5,
          lambda x: 64*7*x**6-112*5*x**3+56*3*x**2-7]
d_cheb2 = list(map(RF, d_cheb2))

# Legendre polynomials

leg = [lambda x: 1, lambda x: x, lambda x: (3*x**2-1)/2, lambda x: (5*x**3-3*x)/2, lambda x: (35*x**4-30*x**2+3)/8, lambda x: (63*x**5-70*x**3+15*x)/8,
       lambda x: (231*x**6-315*x**4+105*x**2-5)/16]
leg = list(map(RF, leg))

d_leg = [lambda x: 0, lambda x: 1, lambda x: 3*x, lambda x: (15*x**2-3)/2, lambda x: (35*4*x**3-60*x)/8, lambda x: (63*5*x**4-70*3*x**2+15)/8,
         lambda x: (231*6*x**5-315*4*x**3+105*x)/16]
d_leg = list(map(RF, d_leg))

leg1 = [lambda x: 1, lambda x: x, lambda x: (3*x**2)/2, lambda x: (5*x**3-3*x)/2, lambda x: (35*x**4-30*x**2)/8, lambda x: (63*x**5-70*x**3+15*x)/8,
       lambda x: (231*x**6-315*x**4+105*x**2)/16]
leg1 = list(map(RF, leg1))

d_leg1 = [lambda x: 0, lambda x: 1, lambda x: 3*x, lambda x: (15*x**2-3)/2, lambda x: (35*4*x**3-60*x)/8, lambda x: (63*5*x**4-70*3*x**2+15)/8,
         lambda x: (231*6*x**5-315*4*x**3+105*x)/16]
d_leg1 = list(map(RF, d_leg1))
'''