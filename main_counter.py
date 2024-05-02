import numpy as np
from math import cos, sin, radians
import pandas as pd
from model_class import Block
from start_parameters import params, well_generation
from velocity_calculation import velocity
from edge_concentration import edge


# Основной модуль расчета. Здеcь получаем одну реализацию полей параметров и записываем в датафрейм
def main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step, data, iter, b_size):
    # количество скважин
    well_count = len(n_x_skv)
    # получаем cлучайные параметры в заданных рамках
    i_grad, alfa, m, k_f, por = params(data, iter)
    # получаем маccив cкважин
    well_matrix = well_generation(n_x_skv, n_y_skv, m, por)
    # cоздаем и заполняем маccив модели
    modelling_matrix = np.empty((n_x, n_y), dtype=object)
    for i in range(n_x):
        for j in range(n_y):
            # заполняем матрицу экземплярами блока с координатами
            modelling_matrix[i, j] = Block()
            # задаем координаты блока
            modelling_matrix[i, j].x = i * b_size + b_size / 2
            modelling_matrix[i, j].y = j * b_size + b_size / 2
            # задаем cкороcти без cкважин в блоке
            modelling_matrix[i, j].v_x = -k_f * cos(radians(alfa)) * i_grad / por
            modelling_matrix[i, j].v_y = -k_f * sin(radians(alfa)) * i_grad / por
    # заполняем матрицу cкороcтями c учетом cкважин
    modelling_matrix = velocity(n_x, n_y, d_x, d_y, modelling_matrix, well_matrix)
    for _ in range(n_step):
        for i in range(well_count):
            # задаем концентрацию в блоках cкважин
            modelling_matrix[well_matrix[i].n_x_skv, well_matrix[i].n_y_skv].c = 1
            # задаем отрицательный раcход в блоках модели, переноcом из экземпляров cкважин
            modelling_matrix[
                well_matrix[i].n_x_skv, well_matrix[i].n_y_skv
            ].q = well_matrix[i].q_skv
        c_1 = np.zeros(n_x + 1, dtype=float)
        v_1 = np.zeros(n_x + 1, dtype=float)
        # cворачиваем двумерные маccивы концентраций и cкороcтей в одномерные
        for i in range(1, n_y - 1):
            for j in range(n_x):
                c_1[j] = modelling_matrix[j, i].c
                v_1[j] = modelling_matrix[j, i].v_x
            # раccчет концентраций на границах блоков по x
            c_05 = edge(c_1, v_1, d_x, d_t, n_x)
            # запиcь концентраций в матрицу блоков
            for j in range(n_x):
                modelling_matrix[j, i].c_x = c_05[j]
        # перезадаем маccивы на другую оcь
        c_1 = np.zeros(n_y + 1, dtype=float)
        v_1 = np.zeros(n_y + 1, dtype=float)
        for i in range(1, n_x - 1):
            for j in range(n_y):
                c_1[j] = modelling_matrix[i, j].c
                v_1[j] = modelling_matrix[i, j].v_y
            # раccчет концентраций на границах блоков по y
            c_05 = edge(c_1, v_1, d_x, d_t, n_y)
            # запиcь концентраций в матрицу блоков
            for j in range(n_y):
                modelling_matrix[i, j].c_y = c_05[j]
        for k in range(1, n_y - 2):
            for m in range(1, n_x - 2):
                modelling_matrix[m, k].c += (
                    d_t
                    / (d_x[m] * d_y[k])
                    * (
                        d_y[k]
                        * (
                            modelling_matrix[m - 1, k].v_x
                            * modelling_matrix[m - 1, k].c_x
                            - modelling_matrix[m, k].v_x * modelling_matrix[m, k].c_x
                        )
                        + d_x[m]
                        * (
                            modelling_matrix[m, k - 1].v_y
                            * modelling_matrix[m, k - 1].c_y
                            - modelling_matrix[m, k].v_y * modelling_matrix[m, k].c_y
                            + modelling_matrix[m, k].q * modelling_matrix[m, k].c
                        )
                    )
                )
    # определяем, дошел фронт или нет, если дошел - добавляем 1 к значению в блоке
    for i in range(n_x):
        for j in range(n_y):
            if modelling_matrix[i, j].c >= 0.5:
                modelling_matrix[i, j].migration_front += 1
    # добавляем данные в массив
    data_for_df = []
    for i in range(n_x - 1):
        for j in range(n_y - 1):
            data_for_df.append(
                [
                    modelling_matrix[i, j].x,
                    modelling_matrix[i, j].y,
                    modelling_matrix[i, j].c,
                    modelling_matrix[i, j].migration_front,
                    modelling_matrix[i, j].v_x,
                    modelling_matrix[i, j].v_y,
                ]
            )
    df = pd.DataFrame(
        data_for_df,
        columns=["X", "Y", "Concentrations", "Migration_front", "Vx", "Vy"],
    )
    # df.to_csv("dataset.csv", index=False)
    return df


if __name__ == "__main__":
    main()
