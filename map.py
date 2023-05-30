import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

def front_map(data = pd.read_csv("main_dataset.csv")):
    # Извлечение координат и значений migration_front
    x = data['X']
    y = data['Y']
    migration_front = data['Migration_front']


    # Создание сетки для интерполяции
    xi = np.linspace(min(x), max(x), 400)
    yi = np.linspace(min(y), max(y), 400)
    xi, yi = np.meshgrid(xi, yi)

    # Интерполяция значений migration_front на сетке
    zi = griddata((x, y), migration_front, (xi, yi), method='linear')
    # Установка размера рисунка в дюймах
    plt.figure(figsize=(10, 10))
    # построение контурной карты
    levels = np.linspace(0, 100, num=5)  # Значения для контуров
    plt.contourf(xi, yi, zi, levels=levels, cmap='viridis')
    # Построение тепловой карты
    # plt.imshow(zi, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap='Pastel1')
    plt.colorbar()
    # Добавление контуров
    contours = plt.contour(xi, yi, zi, levels=levels, colors='black', linewidths=0.5, alpha=0.5)  # Построение контуров

    # Добавление подписей к контурам
    plt.clabel(contours, inline=True, fontsize=6)

    # Отображение осей и меток
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Migration Front Contourmap')
    # Сохранение графика в файл
    plt.savefig("res.png")


if __name__ == "__main__":
    front_map()