import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow

def front_map(data = pd.read_csv('main_dataset.csv'), n_x_skv = np.array([20, 30, 25]), n_y_skv = np.array([20, 15, 20])):
    # Извлечение координат и значений migration_front
    x = data['X']
    y = data['Y']
    migration_front = data['Migration_front']


    # Создание сетки для интерполяции
    xi = np.linspace(min(x), max(x), 20)
    yi = np.linspace(min(y), max(y), 20)
    xi, yi = np.meshgrid(xi, yi)

    # Интерполяция значений migration_front на сетке
    zi = griddata((x, y), migration_front, (xi, yi), method='linear')
    # Установка размера рисунка в дюймах
    plt.figure(figsize=(10, 10))
    # построение контурной карты
    levels = np.linspace(0, 100, num=20)  # Значения для контуров
    plt.contourf(xi, yi, zi, levels=levels, cmap='viridis')
    # Построение тепловой карты
    # plt.imshow(zi, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap='Pastel1')
    plt.colorbar()
    # Добавление контуров
    contours = plt.contour(xi, yi, zi, levels=levels, colors='black', linewidths=0.5, alpha=0.5)  # Построение контуров

    # Добавление подписей к контурам
    plt.clabel(contours, inline=True, fontsize=6)

    # Добавление скважин
    plt.scatter([((x) * 10 + 5) for x in n_x_skv], [((y) * 10 + 5) for y in n_y_skv], c='red', label='Скважина')
    # print([((x+1) * 10)-5 for x in n_x_skv], [((y+1) * 10)-5 for y in n_y_skv])
    # Добавление сетки с шагом 10
    x_ticks = np.arange(0, 401, 10)
    y_ticks = np.arange(0, 401, 10)
    for x_tick in x_ticks:
        plt.axvline(x=x_tick, color='gray', linestyle=':', linewidth=0.5)
    for y_tick in y_ticks:
        plt.axhline(y=y_tick, color='gray', linestyle=':', linewidth=0.5)

    # Отображение осей и меток
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Migration Front Contourmap')
    # Сохранение графика в файл
    plt.savefig("res.png", dpi=600)


if __name__ == "__main__":
    front_map()