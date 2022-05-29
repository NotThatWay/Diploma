from function import *
from SODE import SODE
import matplotlib.pyplot as plt
import numpy as np

'''
a = RF.const(-0.5)
b = 0.5*RF.id()
c = 2*RF.id()
'''
a = RF.pow(-1/3)
b = RF.pow(4) + 2
c = RF.pow(-1)

y0 = 0
y1 = 0.1

n = 20

sode = SODE((a,b,c), (y0,y1))

f, r_norm, R = sode.solve(n)

print('Residue_norm: {0}'.format(r_norm))

N = 1000
x = np.arange(1/N, 1+1/N, 1/N)

plt.plot(x, list(map(f, x)))
plt.plot(x, list(map(R*R, x)))
plt.show()
