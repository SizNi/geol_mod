import numpy as np


nrand = 100
npar = 5
kf = 0.0
igrad = 0.0
kmin = 5.0
kmax = 20.0
imin = 0.001
imax = 0.01
alfamin = 270.0
alfamax = 330.0
mmin = 5.0
mmax = 10.0
m = 0.0
pormin = 0.2
pormax = 0.4
# преоборазование shock2com с фортрана в питон
nx, ny, nskv = 40, 40, 3
# задаем 2 массива (массив a - все -10, массив a1 - все нули)
a = np.zeros(nskv) - 10.0
a1 = np.zeros(nskv)
# задаем два массива из трех элементов и два скаляра
nxskv = np.array([20, 30, 25])  # массив с тремя элементами
nyskv = np.array([20, 15, 20])  # массив с тремя элементами
nxs = 20  # скаляр
nys = 27  # скаляр
# два массива размерами nx и ny со значениями 10
dx = np.full(nx, 10.0)
dy = np.full(ny, 10.0)
# просто задаем переменную
dt = 2.0
nstep = 400
# ----------------------------
etalon = np.zeros((nx, ny), dtype=float)
# расход скважин
q = np.zeros((nx, ny), dtype=float)
# концентрации
c = np.zeros((nx, ny), dtype=float)
# концентраии на разделениях блоков
cx = np.zeros((nx, ny), dtype=float)
cy = np.zeros((nx, ny), dtype=float)
# для концентраций (доведение до 1 если надо)
crez = np.zeros((nx, ny), dtype=float)
