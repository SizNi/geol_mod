import numpy as np


def velocity(n_x, n_y, d_x, d_y, modelling_matrix, well_matrix):
    # вытаскиваем данные из массива экземпляров класса
    well_count = len(well_matrix)
    n_x_skv = np.array([obj.n_x_skv for obj in well_matrix])
    n_y_skv = np.array([obj.n_y_skv for obj in well_matrix])
    a_1 = np.array([-obj.q_skv for obj in well_matrix])
    x_1 = np.zeros(well_count)
    y_1 = np.zeros(well_count)
    # заполняем по обоим осям от 2(1) блока до скважины
    for i in range(well_count):
        x_1[i] = 0
        y_1[i] = 0
        # прибавление 1 нужно для захвата непосредственно блока со скважиной
        n_x_x = n_x_skv[i] + 1
        n_y_y = n_y_skv[i] + 1
        # заменяем цикл for на векторизацию
        x_1[i] = np.sum((d_x[1:n_x_x] + d_x[:n_x_x-1]) / 2)
        y_1[i] = np.sum((d_y[1:n_y_y] + d_y[:n_y_y-1]) / 2)

    x_2 = d_x[0] / 2
    y_2 = d_y[0] / 2
    for i in range(1, n_y):
        x_2 = d_x[0] / 2
        y_3 = y_2 + d_y[i]
        for j in range(n_x):
            for k in range(well_count):
                y_b = y_3 - y_1[k]
                y_h = y_2 - y_1[k]
                x_x = x_2 - x_1[k]
                modelling_matrix[j, i].v_x -= (
                    a_1[k] * (np.arctan(y_b / x_x) - np.arctan(y_h / x_x)) / d_y[i]
                )
            if j < n_x - 1:
                x_2 += d_x[j + 1]
        y_2 = y_3

    x_2 = d_x[0] / 2
    y_2 = d_y[0] / 2

    for i in range(1, n_x):
        y_2 = d_y[0] / 2
        x_3 = x_2 + d_x[i]
        for j in range(n_y):
            for k in range(well_count):
                x_p = x_3 - x_1[k]
                x_l = x_2 - x_1[k]
                y_y = y_2 - y_1[k]
                modelling_matrix[i, j].v_y -= (
                    a_1[k] * (np.arctan(x_p / y_y) - np.arctan(x_l / y_y)) / d_x[i]
                )
            if j < n_y - 1:
                y_2 += d_y[j + 1]
        x_2 = x_3
    return modelling_matrix
