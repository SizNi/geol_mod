import numpy as np
from math import cos, sin, radians
from params import *


def mod():
    # создали массив случайных значений
    u = np.random.random((nrand, npar))
    # print(u)
    for irand in range(nrand):
        # вычисляем случайное значение igrad в интервал min-max через массив u
        igrad = imin + u[irand, 0] * (imax - imin)
        # аналогично для всего нижеидущего
        alfa = alfamin + u[irand, 1] * (alfamax - alfamin)
        m = mmin + u[irand, 2] * (mmax - mmin)
        kf = kmin + u[irand, 3] * (kmax - kmin)
        por = pormin + u[irand, 4] * (pormax - pormin)
        # не совсем понятная штука: массив нулей заменям массивом -10 разделенных на параметр
        for i in range(nskv):
            a1[i] = -a[i] / (m * por)
        print(alfa)
        for i in range(nx):
            for k in range(ny):
                vx[i, k] = kf * cos(radians(alfa)) * igrad / por





if __name__ == "__main__":
    mod()