from main_counter import main
from map import front_map
from tqdm import tqdm


iteration_count = 100


def app_start():
    bar_main = tqdm(total=iteration_count, desc='iteration')
    main_df = main()
    bar_main.update(1)
    for i in range(iteration_count-1):
        new_df = main()
        main_df.Migration_front += new_df.Migration_front
        bar_main.update(1)
    bar_main.close()
    front_map(main_df)
    main_df.to_csv("main_dataset.csv", index=False)


if __name__ == "__main__":
    app_start()
