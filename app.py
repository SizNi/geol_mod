from main_counter import main
from map import front_map
from tqdm import tqdm
import numpy as np

# количество итераций
iteration_count = 50
# координаты скважин
n_x_skv = np.array([20, 30, 25])
n_y_skv = np.array([20, 15, 20])

def app_start():
    bar_main = tqdm(total=iteration_count, desc='iteration')
    main_df = main(n_x_skv, n_y_skv)
    bar_main.update(1)
    for _ in range(iteration_count-1):
        new_df = main(n_x_skv, n_y_skv)
        # будем считать в процентах
        main_df.Migration_front += new_df.Migration_front / iteration_count * 100
        bar_main.update(1)
    bar_main.close()
    main_df.to_csv("main_dataset.csv", index=False)
    front_map(main_df, n_x_skv, n_y_skv)


if __name__ == "__main__":
    app_start()
