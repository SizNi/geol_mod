import random
from model_class import Well
import numpy as np


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


# генератор стартовых параметров
def params():
    i_grad = random.uniform(i_min, i_max)
    alfa = random.uniform(alfa_min, alfa_max)
    m = random.uniform(m_min, m_max)
    k_f = random.uniform(k_f_min, k_f_max)
    por = random.uniform(por_min, por_max)
    return i_grad, alfa, m, k_f, por


# генератор массива объектов скважин
def well_generation(well_count, n_x_skv, n_y_skv, m, por):
    # создаем массив скважин
    well_matrix = np.empty(well_count, dtype=object)
    q_skv = 10 / ((m * por) * well_count)
    for i in range(well_count):
        # уменьшаем на 1 из-за отсчета с нуля
        well_matrix[i] = Well(n_x_skv[i]-1, n_y_skv[i]-1, q_skv)
    return well_matrix


"""if __name__ == "__main__":
    well_count = 3
    # координаты скважин
    n_x_skv = np.array([20, 30, 25])
    n_y_skv = np.array([20, 15, 20])
    q_skv = 10.0
    m = 11
    por = 0.3
    well_generation(well_count, n_x_skv, n_y_skv, m, por)"""
