import numpy as np


# преоборазование shock2com с фортрана в питон
# PARAMETER (nx=40,ny=40,nskv=3)
# задание переменных
nx, ny, nskv = 40, 40, 3
# real a(nskv)/nskv*-10./, a1(nskv)
# задаем 2 массива (массив a - все -10, массив a1 - все нули)
a = np.zeros(nskv) - 10.0
a1 = np.zeros(nskv)
# integer nxskv(nskv)/20,30,25/ ,nyskv(nskv)/20,15,20/,nxs/20/,nys/27/
# задаем два массива из трех элементов и два скаляра
nxskv = np.array([20, 30, 25])  # массив с тремя элементами
nyskv = np.array([20, 15, 20])  # массив с тремя элементами
nxs = 20  # скаляр
nys = 27  # скаляр
# real dt,dx(nx),dy(ny)
dt = np.float64(0.01)  # задаем скаляр dt
dx = np.zeros(nx, dtype=np.float64)  # объявляем массив dx размерности nx
dy = np.zeros(ny, dtype=np.float64)  # объявляем массив dy размерности ny
# integer nstep
# просто объявление переменной
nstep = 0
# DATA dx /nx*10./ ,dy/ny*10./
# два массива размерами nx и ny со значениями 10
dx = np.full(nx, 10.0)
dy = np.full(ny, 10.0)
# DATA dt /2/
# data nstep/400/
# просто задаем переменную
dt = 2
nstep = 400
