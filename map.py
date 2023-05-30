import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import griddata
from archive.params import *

def с_map():
    df = pd.read_csv('main_dataset.csv')
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    concentration = df.iloc[:, 3]

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
    plt.savefig("с.png")

def c_2_map():
    df = pd.read_csv('main_dataset.csv')
    # Определение координат и значения для интерполяции
    x = df['X']
    y = df['Y']
    values = df['Migration_front']

    # Создание сетки
    a = 10  # размер сетки по оси X
    b = 10  # размер сетки по оси Y
    xi = np.linspace(min(x), max(x), a)
    yi = np.linspace(min(y), max(y), b)
    xi, yi = np.meshgrid(xi, yi)

    # Интерполяция данных на сетку
    zi = griddata((x, y), values, (xi, yi), method='linear')

    # Set up the figure
    f, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")

    # Draw a contour plot to represent the bivariate density
    sns.kdeplot(
        data=df,
        x="X",
        y="Y",
        hue="Migration_front",
        thresh=.1,
        levels=5,
        alpha=0.8,
    )

    # Добавление интерполированных изолиний
    plt.contour(xi, yi, zi, levels=5, colors='k', linestyles='dashed')

    # Сохранение картинки
    plt.savefig('my_plot.png')
    
if __name__ == "__main__":
    c_2_map()