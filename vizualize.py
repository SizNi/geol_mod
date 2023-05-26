import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.interpolate import griddata
from params import *


def viz(df):
    # Загрузка данных из файла в DataFrame
    # df = pd.read_csv('dataset.csv')
    # Извлечение координат и концентраций из датафрейма
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

    # Сохранение графика в файл
    plt.savefig("res.png")

def final_viz(df = pd.read_csv("dataset_crez.csv"), nrand = 100):
    sns.set_theme(style="darkgrid")
    # Интерполяция данных
    xi = np.linspace(df['X'].min(), df['X'].max(), 400)
    yi = np.linspace(df['Y'].min(), df['Y'].max(), 400)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((df['X'], df['Y']), df['Crez'], (xi, yi), method='linear')

    # Построение тепловой карты на основе интерполированных данных
    ax = sns.heatmap(zi, cmap='YlGnBu')
    
    # Добавление изолиний равных значений
    contour_levels = [nrand/10, nrand/4, nrand/2, nrand*3/4]
    contour = plt.contour(xi, yi, zi, levels=contour_levels, colors='k')
    plt.clabel(contour, inline=True, fontsize=8)
    
    # Настройка осей и заголовка
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Interpolated Heatmap')
    plt.savefig('final_res.png')
    
if __name__ == "__main__":
    final_viz()
