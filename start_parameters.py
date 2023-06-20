import random
from model_class import Well
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import pandas as pd


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
def distribution_array(iteration_count, n_par, type='random'):
    # случайное распределение, задается от 0 до 1 и потом участвует в виде коэффициента
    if type == 'random':
        data_igrad = np.random.random(iteration_count)
        data_igrad = i_min + (i_max - i_min) * data_igrad
        data_alfa = np.random.random(iteration_count)
        data_alfa = alfa_min + (alfa_max - alfa_min) * data_alfa
        data_m = np.random.random(iteration_count)
        data_m = m_min + (m_max - m_min) * data_m
        data_kf = np.random.random(iteration_count)
        data_kf = k_f_min + (k_f_max - k_f_min) * data_kf
        data_por = np.random.random(iteration_count)
        data_por = por_min + (por_max - por_min) * data_por
    # нормальное распределение. Задается среднее, отклонение как 1/6 интервала и обрезается по крайним значениями
    elif type == 'normal':
        data_igrad = np.random.normal(loc=(i_max + i_min) / 2, scale=(i_max - i_min)/6, size=(iteration_count))
        data_igrad = np.clip(data_igrad, i_min, i_max)
        data_alfa = np.random.normal(loc=(alfa_max + alfa_min) / 2, scale=(alfa_max - alfa_min)/6, size=(iteration_count))
        data_alfa = np.clip(data_alfa, alfa_min, alfa_max)
        data_m = np.random.normal(loc=(m_max + m_min) / 2, scale=(m_max - m_min)/6, size=(iteration_count))
        data_m = np.clip(data_m, m_min, m_max)
        data_kf = np.random.normal(loc=(k_f_max + k_f_min) / 2, scale=(k_f_max - k_f_min)/6, size=(iteration_count))
        data_kf = np.clip(data_kf, k_f_min, k_f_max)
        data_por = np.random.normal(loc=(por_max + por_min) / 2, scale=(por_max - por_min)/6, size=(iteration_count))
        data_por = np.clip(data_por, por_min, por_max)
    # логнормальное распределение. Задается среднее, сигма и обрезается по краям
    elif type == 'lognormal':
        data_igrad = np.random.lognormal(mean=np.log((i_max + i_min) / 2), sigma=np.sqrt(2 * np.log(i_max / i_min)), size=(iteration_count))
        data_igrad = np.clip(data_igrad, i_min, i_max)
        data_alfa = np.random.lognormal(mean=np.log((alfa_max + alfa_min) / 2), sigma=np.sqrt(2 * np.log(alfa_max / alfa_min)), size=(iteration_count))
        data_alfa = np.clip(data_alfa, alfa_min, alfa_max)
        data_m = np.random.lognormal(mean=np.log((m_max + m_min) / 2), sigma=np.sqrt(2 * np.log(m_max / m_min)), size=(iteration_count))
        data_m = np.clip(data_m, m_min, m_max)
        data_kf = np.random.lognormal(mean=np.log((k_f_max + k_f_min) / 2), sigma=np.sqrt(2 * np.log(k_f_max / k_f_min)), size=(iteration_count))
        data_kf = np.clip(data_kf, k_f_min, k_f_max)
        data_por = np.random.lognormal(mean=np.log((por_max + por_min) / 2), sigma=np.sqrt(2 * np.log(por_max / por_min)), size=(iteration_count))
        data_por = np.clip(data_por, por_min, por_max)
    # запись в датафрейм всех параметров для всех итераций
    data = pd.DataFrame({
        "i_grad":data_igrad,
        "alfa": data_alfa,
        "m":data_m,
        "k_f":data_kf,
        "por":data_por,
        })
    data.to_csv('stat.csv', index = False)
    return data


# генератор стартовых параметров
def params(data, iter):
    i_grad = data.loc[iter,"i_grad"]
    alfa = data.loc[iter,"alfa"]
    m = data.loc[iter,"m"]
    k_f = data.loc[iter,"k_f"]
    por = data.loc[iter,"por"]
    return i_grad, alfa, m, k_f, por


# генератор массива объектов скважин
def well_generation(n_x_skv, n_y_skv, m, por):
    # создаем массив скважин
    q_skv = q_main / (m * por * 2 * pi)
    well_matrix = [Well(n_x - 1, n_y - 1, q_skv) for n_x, n_y in zip(n_x_skv, n_y_skv)]
    return np.array(well_matrix)
