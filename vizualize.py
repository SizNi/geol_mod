import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata
from params import *


def viz(df):
    # Загрузка данных из файла в DataFrame
    # df = pd.read_csv('dataset.csv')
    # Извлечение координат и концентраций из датафрейма
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    concentration = df.iloc[:, 2]

    # Создание сетки для интерполяции
    xi = np.arange(0, 401, nx)
    yi = np.arange(0, 401, ny)
    xi, yi = np.meshgrid(xi, yi)

    # Интерполяция концентраций
    zi = griddata((x, y), concentration, (xi, yi), method="cubic")

    # Создание графика
    plt.contourf(xi, yi, zi, levels=20, cmap="viridis")
    plt.colorbar()

    # Добавление осей и заголовка
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Interpolated Visualization of Dataset")

    # Добавление сетки
    plt.grid(True, linestyle="--", linewidth=0.5, color="black")

    # Установка пределов на осях
    plt.xlim(0, 400)
    plt.ylim(0, 400)

    # Добавление делений на осях X и Y
    plt.xticks(xi[0])
    plt.yticks(yi[:, 0])

    # Сохранение графика в файл
    plt.savefig("res.png")


if __name__ == "__main__":
    viz()
