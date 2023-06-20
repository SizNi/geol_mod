import numpy as np

iteration_count = 100
min_value = 5
max_value = 20

# Генерация случайных значений от 0 до 1
data_igrad = np.random.random(iteration_count)

# Масштабирование значений в заданный диапазон
data_igrad = min_value + (max_value - min_value) * data_igrad

# Вывод значений
print(data_igrad)