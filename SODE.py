from function import *
import numpy as np

class SODE:
    def __init__(self, cs, bc):
        self.a, self.b, self.c = cs
        self.y0, self.y1 = bc

        uk = lambda k: RF.pow(k) - RF.pow(k+1)
        d_uk = lambda k: k*RF.pow(k-1) - (k+1)*RF.pow(k)
        d2_uk = lambda k: k*(k-1)*RF.pow(k-2) - (k+1)*k*RF.pow(k-1)
        self.polys = [uk(k) for k in range(101)]
        self.d_polys = [d_uk(k) for k in range(101)]
        self.d2_polys = [d2_uk(k) for k in range(101)]

        self.u0 = (self.y1 - self.y0)*RF.id() + self.y0
        self.d_u0 = RF.const(self.y1 - self.y0)
        self.d2_u0 = RF.const(0)


    def getA(self, n):
        M = []
        mk = lambda k: k*(k-1)*RF.pow(k-2) + \
                       (self.a - (k+1))*k*RF.pow(k-1) + \
                       (self.b - self.a*(k+1))*RF.pow(k) - \
                       self.b*RF.pow(k+1)
        d = self.a * self.d_u0 + \
            self.b * self.u0 - \
            self.c
        for i in range(1,n+1):
            m = []
            for j in range(1,n+1):
                m.append(RF.scalar(mk(j), self.polys[i]))
            M.append(m)
        D = [RF.scalar(-d, self.polys[i]) for i in range(1,n+1)]
        A = np.linalg.solve(M, D)

        return A

    def solve(self, n):
        ya = lambda cs: self.u0 + RF.linComb(cs, self.polys[1:])
        d_ya = lambda cs: self.d_u0 + RF.linComb(cs, self.d_polys[1:])
        d2_ya = lambda cs: self.d2_u0 + RF.linComb(cs, self.d2_polys[1:])

        A = self.getA(n)
        ya1 = ya(A)
        d_ya1 = d_ya(A)
        d2_ya1 = d2_ya(A)
        R = d2_ya1 + self.a*d_ya1 + self.b*ya1 - self.c
        try:
            R_norm = RF.norm(R)
            return ya1, R_norm, R
        except ValueError:
            return ya1, None, R