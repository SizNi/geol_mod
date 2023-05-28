import numpy as np
from math import cos, sin, radians
from progress.bar import IncrementalBar
import pandas as pd
from filtration_rates import rates
from model_class import Block
from start_parameters import params


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
dx = np.full(n_x, 10.0)
dy = np.full(n_y, 10.0)
# здесь получаем одну реализацию полей параметров
def main():
    # задаем абстрактный параметр
    a_1 = np.zeros(well_count)
    # получаем случайные параметры в заданных рамках
    i_grad, alfa, m, k_f, por = params()
    # создаем и заполняем матрицу
    modelling_matrix = np.empty((n_x, n_y), dtype=object)
    for i in range(n_x):
        for j in range(n_y):
            # заполняем матрицу пустыми значениями
            modelling_matrix[i, j] = Block
            # 
            modelling_matrix[i, j].v_x = -k_f * cos(radians(alfa)) * i_grad / por
            modelling_matrix[i, j].v_y = -k_f * sin(radians(alfa)) * i_grad / por

if __name__ == "__main__":
    main()