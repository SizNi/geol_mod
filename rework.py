import numpy as np
from math import cos, sin, radians
from progress.bar import IncrementalBar
import pandas as pd
from filtration_rates import rates
from model_class import Block
from start_parameters import params, well_generation
from velocity_calculation import velocity
from edge_concentration import edge


# размеры модели в блоках
n_x = n_y = 40
# количество скважин
well_count = 3
# координаты скважин
n_x_skv = np.array([20, 30, 25])
n_y_skv = np.array([20, 15, 20])
# до сих пор непонял откуда это взялось
a = np.full(well_count, -10.0)
# приращение
d_x = np.full(n_x, 10.0)
d_y = np.full(n_y, 10.0)
d_t = 1.0
n_step = 200


# здесь получаем одну реализацию полей параметров
def main():
    # задаем абстрактный параметр
    a_1 = np.zeros(well_count)
    # получаем случайные параметры в заданных рамках
    i_grad, alfa, m, k_f, por = params()
    # получаем массив скважин
    well_matrix = well_generation(well_count, n_x_skv, n_y_skv, m, por)
    # создаем и заполняем массив модели
    modelling_matrix = np.empty((n_x, n_y), dtype=object)
    for i in range(n_x):
        for j in range(n_y):
            # заполняем матрицу пустыми значениями
            modelling_matrix[i, j] = Block
            modelling_matrix[i, j].v_x = -k_f * cos(radians(alfa)) * i_grad / por
            modelling_matrix[i, j].v_y = -k_f * sin(radians(alfa)) * i_grad / por
    # по факту первоначальное вычисление скоростей дальше не используется,
    # потом можно будет убрать. Пока можно сравнить до включения скважин и после,
    # различие на 1-2 порядка при параметрах по умолчанию
    # заполняем матрицу скоростями с учетом скважин
    modelling_matrix = velocity(n_x, n_y, d_x, d_y, modelling_matrix, well_matrix)

    for step in range(n_step):
        for i in range(well_count):
            # задаем концентрацию в блоках скважин
            modelling_matrix[well_matrix[i].n_x_skv, well_matrix[i].n_y_skv].c = 1
            # задаем отрицательный расход в блоках модели, переносом из экземпляров скважин
            modelling_matrix[
                well_matrix[i].n_x_skv, well_matrix[i].n_y_skv
            ].q = -well_matrix[i].q_skv

        c_1 = np.zeros(n_x + 1, dtype=float)
        v_1 = np.zeros(n_x + 1, dtype=float)
        # сворачиваем двумерные массивы концентраций и скоростей в одномерные
        for i in range(1, n_y - 1):
            for j in range(n_x):
                c_1[j] = modelling_matrix[j, i].c
                v_1[j] = modelling_matrix[j, i].v_x
            # рассчет концентраций на границах блоков по x
            c_05 = edge(c_1, v_1, d_x, d_t, n_x)
            # запись концентраций в матрицу блоков
            for i in range(n_x):
                modelling_matrix[j, i].c_x = c_05[i]

        # перезадаем массивы на другую ось
        c_1 = np.zeros(n_y + 1, dtype=float)
        v_1 = np.zeros(n_y + 1, dtype=float)
        for i in range(1, n_x - 1):
            for j in range(n_y):
                c_1[j] = modelling_matrix[j, i].c
                v_1[j] = modelling_matrix[j, i].v_y
            # рассчет концентраций на границах блоков по y
            c_05 = edge(c_1, v_1, d_x, d_t, n_y)
            # запись концентраций в матрицу блоков
            for i in range(n_x):
                modelling_matrix[j, i].c_y = c_05[i]
        for i in range(1, n_y - 1):
            for j in range(1, n_x - 1):
                modelling_matrix[j, i].c = modelling_matrix[j, i].c + d_t / (
                    d_x[j] * d_y[i]
                ) * (
                    d_y[i]
                    * (
                        modelling_matrix[j - 1, i].v_x * modelling_matrix[j - 1, i].c_x
                        - modelling_matrix[j, i].v_x * modelling_matrix[j, i].c_x
                    )
                    + d_x[j]
                    * (
                        modelling_matrix[j, i - 1].v_y * modelling_matrix[j, i - 1].c_y
                        - modelling_matrix[j, i].v_y * modelling_matrix[j, i].c_y
                        + modelling_matrix[j, i].q * modelling_matrix[j, i].c
                    )
                )


if __name__ == "__main__":
    main()