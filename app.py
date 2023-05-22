import numpy as np
from math import cos, radians
from params import *
from Vel import vel
from Shock_1 import shock_1
from progress.bar import IncrementalBar
import pandas as pd
from vizualize import viz


def mod():
    bar = IncrementalBar("irand", max=nrand)
    # массив скоростей по x, y
    vx = vy = np.zeros((nx, ny), dtype=float)
    u = np.random.random((nrand, npar))
    for irand in range(nrand):
        # вычисляем случайное значение igrad в интервал min-max через массив u
        igrad = imin + u[irand, 0] * (imax - imin)
        # аналогично для всего нижеидущего
        alfa = alfamin + u[irand, 1] * (alfamax - alfamin)
        m = mmin + u[irand, 2] * (mmax - mmin)
        kf = kmin + u[irand, 3] * (kmax - kmin)
        por = pormin + u[irand, 4] * (pormax - pormin)
        # абстрактный параметр, основанный на дебите скважин
        for i in range(nskv):
            a1[i] = -a[i] / (m * por)
        # вычисляем поле скоростей без скважин
        vx[:, :] = kf * cos(radians(alfa)) * igrad / por
        vy[:, :] = kf * cos(radians(alfa)) * igrad / por
        bar.next()
    bar.finish()
    # вычисляем поле скоростей со скважинами
    vx, vy = vel(nx, ny, dx, dy, vx, vy, a1, nxskv, nyskv, nskv)
    #  точка старта для концентраций
    c[nxs, nys] = 2
    # переносим расходы скважин на сетку
    for nsk in range(nskv):
        q[nxskv[nsk], nyskv[nsk]] = -a1[nsk]
    bar = IncrementalBar("step", max=nstep)
    # задаем массивы для сворачивания двумерного в одномерный
    c1 = v1 = np.zeros(nx + 1)
    # c05 - концентрация на границе блока (половина длинны от центра блока)
    c05_x = np.zeros(nx, dtype=float)
    c05_y = np.zeros(ny, dtype=float)
    for step in range(nstep):
        for k in range(1, ny - 1):
            c1[:nx] = c[:nx, k]
            v1[:nx] = vx[:nx, k]
            c05_x = shock_1(c05_x, c1, v1, dx, dt, nx)
            # собираем массив обратно в двумерный (между блоками по x)
            cx[:nx, k] = c05_x[:]
        for i in range(1, nx - 1):
            c1[:ny] = c[i, :ny]
            v1[:ny] = vy[i, :ny]
            # собираем массив обратно в двумерный (между блоками по y)
            c05_y = shock_1(c05_y, c1, v1, dy, dt, ny)
            cy[i, :ny] = c05_y[:]
            # print(np.array_equal(etalon, cx))
        for k in range(1, ny - 2):
            for i in range(1, nx - 2):
                c[i, k] = c[i, k] + dt / (dx[i] * dy[k]) * (
                    dy[k] * (vx[i - 1, k] * cx[i - 1, k] - vx[i, k] * cx[i, k])
                    + dx[i]
                    * (
                        vy[i, k - 1] * cy[i, k - 1]
                        - vy[i, k] * cy[i, k]
                        + q[i, k] * c[i, k]
                    )
                )
        old = False
        # на фортране было создание этих 3 файлов, сейчас они вроде бы не нужны, вынес в цикл
        if old:
            with open("output_2.txt", "a") as file2, open(
                "output_3.txt", "a"
            ) as file3, open("output_4.txt", "a") as file4:
                for nsk in range(nskv):
                    file = file2 if nsk == 0 else file3 if nsk == 1 else file4
                    print(
                        step * dt,
                        c[nxskv[nsk], nyskv[nsk]],
                        nxskv[nsk],
                        nyskv[nsk],
                        file=file,
                    )
        bar.next()
    bar.finish()
    # прибавляем 1, если фронт дошел до скважины
    crez[np.where(c >= 0.5)] += 1.0
    # запись результирующего файла (на фортране был output_1.txt)
    data_for_df = []
    for i in range(1, nx):
        for k in range(1, ny):
            x = i * 10.0 - 5.0
            y = k * 10.0 - 5.0
            data_for_df.append([x, y, c[i, k], crez[i, k], vx[i, k], vy[i, k]])
    df = pd.DataFrame(
        data_for_df, columns=["X", "Y", "Concentrations", "Crez", "Vx", "Vy"]
    )
    # сохранение файла в целом не нужно, если нужна картинка, можно на визуализацию передавать датасет
    df.to_csv("dataset.csv", index=False)
    # визуализация
    viz(df)


if __name__ == "__main__":
    mod()
