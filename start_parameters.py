import random
from model_class import Well
import numpy as np
from math import pi


k_f_min = 5.0
k_f_max = 20.0
i_min = 0.001
i_max = 0.01
alfa_min = 270.0
alfa_max = 330.0
m_min = 5.0
m_max = 10.0
por_min = 0.2
por_max = 0.4
# расход м3/сут
q_main = 62.8


# массив распределния параметров (формируется до запуска повторяющихся циклов)
def distribution_array(iteration_count, n_par):
    d_array = np.empty((iteration_count, n_par), dtype=float)
    random.seed()
    d_array = np.random.random((iteration_count, n_par))
    return d_array


# генератор стартовых параметров
def params(d_array, iter):
    i_grad = i_min + d_array[iter, 0] * (i_max - i_min)
    alfa = alfa_min + d_array[iter, 1] * (alfa_max - alfa_min)
    m = m_min + d_array[iter, 2] * (m_max - m_min)
    k_f = k_f_min + d_array[iter, 3] * (k_f_max - k_f_min)
    por = por_min + d_array[iter, 4] * (por_max - por_min)
    return i_grad, alfa, m, k_f, por


# генератор массива объектов скважин
def well_generation(n_x_skv, n_y_skv, m, por):
    # создаем массив скважин
    q_skv = q_main / (m * por * 2 * pi)
    well_matrix = [Well(n_x - 1, n_y - 1, q_skv) for n_x, n_y in zip(n_x_skv, n_y_skv)]
    return np.array(well_matrix)
