import numpy as np
from math import cos, sin, radians
from params import *
from Vel import vel
from Shock_1 import shock_1


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
        #print(alfa)
        for i in range(nx):
            for k in range(ny):
                vx[i, k] = kf * cos(radians(alfa)) * igrad / por
                vy[i, k] = kf * cos(radians(alfa)) * igrad / por

    vx_new, vy_new = vel(nx, ny, dx, dy, vx, vy, a1, nxskv, nyskv, nskv)
    print(np.array_equal(vx_new, vx))
    # переносим расходы скважин на сетку
    for nsk in range(nskv):
        q[nxskv[nsk], nyskv[nsk]] = -a1[nsk]
    # print(q)
    # print(a1)
    print(np.array_equal(etalon, q))
    for step in range(nstep):
        # задаем массивы для сворачивания двумерного в одномерный
        c1 = np.zeros(nx + 1)
        v1 = np.zeros(nx + 1)
        c05 = np.zeros(nx, dtype=float)
        for k in range(1, ny-1):
            for i in range(nx):
                c1[i] = c[i, k]
                v1[i] = vx_new[i, k]
            c05 = shock_1(c05, c1, v1, dx, dt, nx)
            # собираем массив обратно в двумерный (между блоками по x)
            for i in range(nx):
                cx[i, k] = c05[i]
        # задаем массивы для сворачивания двумерного в одномерный
        c1 = np.zeros(nx + 1)
        v1 = np.zeros(nx + 1)
        c05 = np.zeros(nx, dtype=float)
        for i in range(1, nx-1):
            for k in range(ny):
                c1[k] = c[i, k]
                v1[k] = vy_new[i, k]
            c05 = shock_1(c05, c1, v1, dx, dt, nx)
            # собираем массив обратно в двумерный (между блоками по y)
            for k in range(ny):
                cy[i, k] = c05[k]
        for k in range(1, ny - 2):
            for i in range(1, nx - 2):
                c[i, k] = c[i, k] + dt / (dx[i] * dy[k]) * (dy[k] * (vx_new[i - 1, k] * cx[i - 1, k] - vx_new[i, k] * cx[i, k]) + dx[i] * (vy_new[i, k - 1] * cy[i, k - 1] - vy_new[i, k] * cy[i, k] + q[i, k] * c[i, k]))
        # print(np.array_equal(etalon, c))
        # запись в 3 файла
        with open("output_2.txt", "a") as file2, open("output_3.txt", "a") as file3, open("output_4.txt", "a") as file4:
            for nsk in range(nskv):
                if nsk == 0:
                    file = file2
                elif nsk == 1:
                    file = file3
                else:
                    file = file4
                print(step * dt, c[nxskv[nsk], nyskv[nsk]], nxskv[nsk], nyskv[nsk], file=file)
    for i in range(nx):
        for k in range(ny):
            if c[i, k] >= 0.5:
                crez[i, k] += 1.0
    with open("output_1.txt", "w") as file:
        for i in range(1, nx):
            for k in range(1, ny):
                x = i * 10. - 5.
                y = k * 10. - 5.
                line = f"{x:12.5f} {y:12.5f} {c[i, k]:12.5f} {crez[i, k]:12.5f} {vx[i, k]:12.5f} {vy[i, k]:12.5f}\n"
                file.write(line)







if __name__ == "__main__":
    mod()
