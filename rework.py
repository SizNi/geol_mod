import numpy as np
from math import cos, sin, radians
from progress.bar import IncrementalBar
import pandas as pd
from filtration_rates import rates
from model_class import Block
from start_parameters import params, well_generation
from velocity_calculation import velocity


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
    # test = modelling_matrix[39,39].v_x
    # заполняем матрицу скоростями с учетом скважин
    modelling_matrix = velocity(n_x, n_y, d_x, d_y, modelling_matrix, well_matrix)
    # test_2 = modelling_matrix[39,39].v_x
    # print(test, test_2)


if __name__ == "__main__":
    main()
