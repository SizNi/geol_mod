import numpy as np
from math import cos, sin, radians
from params import *
from Vel import vel
from Shock_1 import shock_1
from progress.bar import IncrementalBar
import pandas as pd
from vizualize import final_viz


def mod():
    # для концентраций (доведение до 1 если надо)
    crez = np.zeros((nx, ny), dtype=float)
    # расход скважин
    q = np.zeros((nx, ny), dtype=float)
    # параметр от скорости
    a1 = np.zeros(nskv)
    # массив случайного распределения
    u = np.random.random((nrand, npar))
    # датафрейм на вероятности
    df_crez = pd.DataFrame(columns=["X", "Y", "Crez"])
    bar = IncrementalBar("irand", max=nrand)
    for irand in range(nrand):
        # массив скоростей по x, y
        vx = vy = np.zeros((nx, ny), dtype=float)
        # концентрации
        c = np.zeros((nx, ny), dtype=float)
        # концентраии на разделениях блоков
        cx = np.zeros((nx, ny), dtype=float)
        cy = np.zeros((nx, ny), dtype=float)
        # вычисляем случайное значение igrad в интервал min-max через массив u
        igrad = imin + u[irand, 0] * (imax - imin)
        # аналогично для всего нижеидущего
        alfa = alfamin + u[irand, 1] * (alfamax - alfamin)
        m = mmin + u[irand, 2] * (mmax - mmin)
        kf = kmin + u[irand, 3] * (kmax - kmin)
        por = pormin + u[irand, 4] * (pormax - pormin)
        # абстрактный параметр, основанный на дебите скважин
        # цикл заменен на поэлементное деление
        a1 = a / (m * por)
        # вычисляем поле скоростей без скважин
        vx[:, :] = -kf * cos(radians(alfa)) * igrad / por
        vy[:, :] = -kf * sin(radians(alfa)) * igrad / por
        # вычисляем поле скоростей со скважинами
        vx, vy = vel(nx, ny, dx, dy, vx, vy, a1, nxskv, nyskv, nskv)
        # переносим расходы скважин на сетку
        # цикл также заменен поэлементным обращением
        q[nxskv, nyskv] = -a1
        # задаем массивы для сворачивания двумерного в одномерный
        c1 = v1 = np.zeros(nx + 1)
        # c05 - концентрация на границе блока (половина длинны от центра блока)
        c05_x = np.zeros(nx, dtype=float)
        c05_y = np.zeros(ny, dtype=float)
        for step in range(nstep):
            # дополнительные правки
            for nsk in range(nskv):
                c[nxskv[nsk], nyskv[nsk]] = 1
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

        # Рассчитываем вероятности
        for i in range(nx):
            for k in range(ny):
                if c[i, k] >= 0.5:
                    crez[i, k] += 1.0
        # запись результирующего файла (на фортране был output_1.txt)
        data_for_df = []
        data_for_final_df = []
        for i in range(1, nx):
            for k in range(1, ny):
                x = i * 10.0 - 5.0
                y = k * 10.0 - 5.0
                data_for_df.append([x, y, c[i, k], crez[i, k], vx[i, k], vy[i, k]])
                data_for_final_df.append(crez[i, k])
        df = pd.DataFrame(
            data_for_df, columns=["X", "Y", "Concentrations", "Crez", "Vx", "Vy"]
        )
        # Разобраться!!!!!!!!!!!!!!!!!
        df_crez["X"] = df["X"]
        df_crez["Y"] = df["Y"]

        df_crez["Crez"] = data_for_final_df
        # сохранение файла в целом не нужно, если нужна картинка, можно на визуализацию передавать датасет
        df.to_csv("dataset.csv", index=False)
        # визуализация
        bar.next()
    bar.finish()
    df_crez.to_csv("dataset_crez.csv", index=False)
    final_viz(df_crez, nrand)
    return df


if __name__ == "__main__":
    mod()
