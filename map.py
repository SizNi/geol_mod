import numpy as np
import pandas as pd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def front_map(type, n_x_skv, n_y_skv, b_size, n_x, n_y, data):
    # Извлечение координат и значений migration_front
    x = data["X"]
    y = data["Y"]
    migration_front = data["Migration_front"]

    # Создание сетки для интерполяции
    xi = np.arange(min(x), max(x) + 1, b_size / 2)
    yi = np.arange(min(y), max(y) + 1, b_size / 2)
    xi, yi = np.meshgrid(xi, yi)

    # Интерполяция значений migration_front на сетке
    zi = griddata((x, y), migration_front, (xi, yi), method="linear")
    # Установка размера рисунка в дюймах
    plt.figure(figsize=(10, 10))
    # построение контурной карты
    levels = np.arange(0, 101, 20)  # Значения для основных контуров
    intermediate_levels = np.arange(0, 101, 5)  # Значения для промежуточных контуров
    plt.contourf(xi, yi, zi, levels=intermediate_levels, cmap="Blues")
    colorbar = plt.colorbar()
    colorbar.set_label("Probability, %")
    # Добавление контуров основных
    contours = plt.contour(
        xi, yi, zi, levels=levels, colors="black", linewidths=0.5, alpha=0.5
    )
    # Добавление вспомогательных контуров
    plt.contour(
        xi, yi, zi, levels=intermediate_levels, colors="gray", linewidths=0.5, alpha=0.5
    )
    plt.contour(xi, yi, zi, levels=1, colors="gray", linewidths=0.5, alpha=0.5)
    # 0 - в белый цвет
    plt.contourf(xi, yi, zi, levels=[-1e-9, 0], colors="white")
    # Добавление подписей к контурам
    plt.clabel(contours, inline=True, fontsize=6)

    # Добавление скважин
    plt.scatter(
        [((x) * b_size - b_size / 2) for x in n_x_skv],
        [((y) * b_size - b_size / 2) for y in n_y_skv],
        c="red",
        label="Well",
        s=2000 / n_x,
    )
    # Добавление сетки с шагом b_size
    x_ticks = np.arange(0, n_x * b_size + 1, b_size)
    y_ticks = np.arange(0, n_y * b_size + 1, b_size)
    for x_tick in x_ticks:
        plt.axvline(x=x_tick, color="gray", linestyle=":", linewidth=0.5)
    for y_tick in y_ticks:
        plt.axhline(y=y_tick, color="gray", linestyle=":", linewidth=0.5)

    # Отображение осей и меток
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Migration Front Contourmap, {type} distribution.")
    plt.legend()
    # Сохранение графика в файл
    plt.savefig("result.png", dpi=600)


if __name__ == "__main__":
    front_map()
