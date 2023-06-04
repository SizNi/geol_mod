from main_counter import main
from map import front_map
from tqdm import tqdm
import numpy as np

# количество итераций
iteration_count = 100
# размеры модели в блоках
n_x = n_y = 40
# координаты скважин
n_x_skv = np.array([20, 30, 25])
n_y_skv = np.array([20, 15, 20])
# приращение
d_x = np.full(n_x, 10.0)
d_y = np.full(n_y, 10.0)
# временной шаг
d_t = 1
# количество временных шагов
n_step = 200
# размер блока
b_size = 10


def app_start():
    bar_main = tqdm(total=iteration_count, desc="Iteration")
    # первый вызов функции и получение основного датасета
    main_df = main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step)
    bar_main.update(1)
    for _ in range(iteration_count - 1):
        new_df = main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step)
        # приращение вероятностей
        main_df.Migration_front += new_df.Migration_front
        bar_main.update(1)
    bar_main.close()
    # переводим вероятности из единиц в проценты (округление до единицы)
    main_df.Migration_front = main_df.Migration_front * (100 / iteration_count)
    # сохраняем датасет на всякий
    main_df.to_csv("main_dataset.csv", index=False)
    # функция-визуализатор
    front_map(main_df, n_x_skv, n_y_skv, b_size, n_x, n_y)


if __name__ == "__main__":
    app_start()
