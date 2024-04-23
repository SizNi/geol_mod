import numpy as np

# number of iteratons
iteration_count = 100
# model size in blocks
n_x = 40
n_y = 40
# wells coordinates (in blocks, X-Y)
n_x_skv = np.array([20, 30, 25])
n_y_skv = np.array([20, 15, 20])
# wells flow rate
q_main = np.array([62.1, 20.0, 24.3])
# block size
b_size = 10.0
# increment
d_x = np.full(n_x, b_size)
d_y = np.full(n_y, b_size)
# time step (days)
d_t = 1
# number of time steps
n_step = 200
# type of parameter distribution
type = "random"  # uniform/normal/lognormal/random
# filtration coefficient
k_f_min = 5.0
k_f_max = 20.0
# flow gradient
i_min = 0.001
i_max = 0.01
# flow direction
alfa_min = 270.0
alfa_max = 330.0
# sediment thickness
m_min = 5.0
m_max = 10.0
# porosity
por_min = 0.2
por_max = 0.4
