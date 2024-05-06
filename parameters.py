import numpy as np

# number of iteratons
iteration_count = 100
# model size in blocks
n_x = 80
n_y = 80
# wells coordinates (in blocks, X-Y)
n_x_skv = np.array([20])
n_y_skv = np.array([20])
# wells flow rate
q_main = np.array([432])
# block size
b_size = 2
# increment
d_x = np.full(n_x, b_size)
d_y = np.full(n_y, b_size)
# time step (days)
d_t = 1
# number of time steps
n_step = 1
# type of parameter distribution
type = "random"  # uniform/normal/lognormal/random
# filtration coefficient
k_f_min = 1.73
k_f_max = 1.73
# flow gradient
i_min = 0.005
i_max = 0.005
# flow direction
alfa_min = 290
alfa_max = 290
# sediment thickness
m_min = 50
m_max = 50
# porosity
por_min = 0.3
por_max = 0.3
