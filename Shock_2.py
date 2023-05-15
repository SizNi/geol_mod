import numpy as np
from Shock2com import *
from math import cos, sin, radians
from Vel import vel
from Rands_1 import rands_1
from Shock_1 import shock_1


# преоборазование shock2 с фортрана в питон
nrand = 100
npar = 5
u = np.zeros((nrand, npar), dtype=float)
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

c = np.zeros((nx, ny), dtype=float)
cx = np.zeros((nx, ny), dtype=float)
vx = np.zeros((nx, ny), dtype=float)
cy = np.zeros((nx, ny), dtype=float)
vy = np.zeros((nx, ny), dtype=float)
c1 = np.array([], dtype=float)
v1 = np.array([], dtype=float)
c05 = np.array([], dtype=float)
crez = np.zeros((nx, ny), dtype=float)
q = np.zeros((nx, ny), dtype=float)
crez = 0.0
q = 0.0
# рандомно заполняем массив u
u = rands_1(nrand, npar)
for irand in range(1, nrand + 1):
    igrad = imin + u[irand - 1, 0] * (imax - imin)
    alfa = alfamin + u[irand - 1, 1] * (alfamax - alfamin)
    m = mmin + u[irand - 1, 2] * (mmax - mmin)
    kf = kmin + u[irand - 1, 3] * (kmax - kmin)
    por = pormin + u[irand - 1, 4] * (pormax - pormin)

    for i in range(1, nskv + 1):
        a1[i - 1] = -a[i - 1] / (m * por)

    for i in range(1, nx + 1):
        for k in range(1, ny + 1):
            vx[i - 1, k - 1] = kf * cos(radians(alfa)) * igrad / por
            c[i - 1, k - 1] = 0.0
            vy[i - 1, k - 1] = kf * sin(radians(alfa)) * igrad / por
            cx[i - 1, k - 1] = 0.0
            cy[i - 1, k - 1] = 0.0
# вызываем расчетный модуль
vx, vy = vel(ny, nx, dx, dy, vx, vy, a1, nxskv, nyskv, nskv)
c[nxs, nys] = 100

for nsk in range(1, nskv + 1):
    q[nxskv[nsk - 1], nyskv[nsk - 1]] = -a1[nsk - 1]
# охватываем loop_1
for step in range(1, nstep + 1):
    cx = np.zeros((nx, ny))
    cy = np.zeros((nx, ny))

    for k in range(2, ny - 1):
        c1 = c[:, k].copy()
        v1 = vx[:, k].copy()
        # вынес в отдельный файл рассчет массива c05
        c05 = shock_1(c05, c1, v1, dx, dt, nx)

        cx[:, k] = c05

    for i in range(2, nx - 1):
        c1 = c[i, :].copy()
        v1 = vy[i, :].copy()

        c05 = shock_1(c05, c1, v1, dy, dt, ny)

        cy[i, :] = c05

    for k in range(2, ny - 2):
        for i in range(2, nx - 2):
            c[i, k] += (
                dt
                / (dx[i] * dy[k])
                * (
                    dy[k] * (vx[i - 1, k] * cx[i - 1, k] - vx[i, k] * cx[i, k])
                    + dx[i] * (vy[i, k - 1] * cy[i, k - 1] - vy[i, k] * cy[i, k])
                    + q[i, k] * c[i, k]
                )
            )
    # записываем в файлы
    for nsk in range(1, nskv + 1):
        if nsk == 1:
            with open("output_2.txt", "w") as file:
                file.write(
                    f"{step * dt} {c[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
        elif nsk == 2:
            with open("output_3.txt", "w") as file:
                file.write(
                    f"{step * dt} {c[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
        elif nsk == 3:
            with open("output_4.txt", "w") as file:
                file.write(
                    f"{step * dt} {c[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
    with open("output_1.txt", "w") as file:
        for i in range(1, nx):
            for k in range(1, ny):
                if c[i, k] >= 0.5:
                    crez[i, k] += 1

        for i in range(1, nx - 1):
            for k in range(1, ny - 1):
                x = i * 10.0 - 5.0
                y = k * 10.0 - 5.0
                output = [x, y, c[i, k], crez[i, k], vx[i, k], vy[i, k]]
                file.write(
                    "{:12.5g} {:12.5g} {:12.5g} {:12.5g} {:12.5g} {:12.5g}\n".format(
                        *output
                    )
                )
