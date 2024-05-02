from main_counter import main
from map import front_map
from tqdm import tqdm
from start_parameters import distribution_array
from parameters import iteration_count, n_x, n_y, n_x_skv, n_y_skv, b_size, d_x, d_y, d_t, n_step, type


def app_start():
    bar_main = tqdm(total=iteration_count, desc="Iteration")
    # формирование массива случайных коэффициентов для задачи параметров
    data = distribution_array(iteration_count, 5, type)
    # первый вызов функции и получение основного датасета
    main_df = main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step, data, 0, b_size)
    bar_main.update(1)
    for iter in range(1, iteration_count):
        new_df = main(n_x_skv, n_y_skv, n_x, n_y, d_x, d_y, d_t, n_step, data, iter, b_size)
        # приращение вероятностей
        main_df.Migration_front += new_df.Migration_front
        bar_main.update(1)
    bar_main.close()
    # переводим вероятности из единиц в проценты (округление до единицы)
    main_df.Migration_front = main_df.Migration_front * (100 / iteration_count)
    # сохраняем датасет на всякий
    main_df.to_csv("main_dataset.csv", index=False)
    # функция-визуализатор
    front_map(
        type,
        n_x_skv,
        n_y_skv,
        b_size,
        n_x,
        n_y,
        main_df)


if __name__ == "__main__":
    app_start()
