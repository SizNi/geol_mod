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

c1 = np.zeros((nxskv, nyskv), dtype=float)
cx = np.zeros((nxskv, nyskv), dtype=float)
vx = np.zeros((nxskv, nyskv), dtype=float)
cy = np.zeros((nxskv, nyskv), dtype=float)
vy = np.zeros((nxskv, nyskv), dtype=float)
c1 = np.zeros(nxskv, dtype=float)
v1 = np.zeros(nxskv, dtype=float)
c05 = np.array([], dtype=float)
crez = np.zeros((nxskv, nyskv), dtype=float)
q = np.zeros((nxskv, nyskv), dtype=float)
# рандомно заполняем массив u
u = rands_1(nrand, npar)
for irand in range(nrand):
    igrad = imin + u[irand, 0] * (imax - imin)
    alfa = alfamin + u[irand, 1] * (alfamax - alfamin)
    m = mmin + u[irand, 2] * (mmax - mmin)
    kf = kmin + u[irand, 3] * (kmax - kmin)
    por = pormin + u[irand, 4] * (pormax - pormin)

    for i in range(nskv):
        a1[i] = -a1[i] / (m * por)

    for i in range(nxskv):
        for k in range(nyskv):
            vx[i, k] = kf * cos(radians(alfa)) * igrad / por
            vy[i, k] = kf * sin(radians(alfa)) * igrad / por
# вызываем расчетный модуль
vx, vy = vel(nyskv, nxskv, dx, dy, vx, vy, a1, nxskv, nyskv, nskv)
c1[nxs, nys] = 100.0

for nsk in range(nskv):
    q[nxskv[nsk], nyskv[nsk]] = -a1[nsk]
    # print(q)
np.savetxt("test.txt", q)
np.savetxt("test_a.txt", a1)
# охватываем loop_1

for step in range(nstep):
    for k in range(nyskv):
        for i in range(nxskv):
            c1[i] = c1[i, k]
            v1[i] = vx[i, k]
        # вынес в отдельный файл рассчет массива c05
        c05 = shock_1(c05, c1, v1, dx, dt, nxskv)

        for i in range(nxskv):
            cx[i, k] = c05[i]
    for i in range(1, nxskv - 1):
        for k in range(nyskv):
            c1[k] = c1[i, k]
            v1[k] = vy[i, k]

        c05 = shock_1(c05, c1, v1, dy, dt, nyskv)

        for k in range(nyskv):
            cy[i, k] = c05[k]

    for k in range(1, nyskv - 1):
        for i in range(1, nxskv - 1):
            c1[i, k] = c1[i, k] + dt / (dx[i] * dy[k]) * (
                dy[k] * (vx[i - 1, k] * cx[i - 1, k] - vx[i, k] * cx[i, k])
                + dx[i]
                * (
                    vy[i, k - 1] * cy[i, k - 1]
                    - vy[i, k] * cy[i, k]
                    + q[i, k] * c1[i, k]
                )
            )

    # записываем в файлы
    for nsk in range(nskv):
        if nsk == 0:
            with open("output_2.txt", "w") as file:
                file.write(
                    f"{step * dt} {c1[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
        elif nsk == 1:
            with open("output_3.txt", "w") as file:
                file.write(
                    f"{step * dt} {c1[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
        elif nsk == 2:
            with open("output_4.txt", "w") as file:
                file.write(
                    f"{step * dt} {c1[nxskv[nsk], nyskv[nsk]]} {nxskv[nsk]} {nyskv[nsk]}\n"
                )
    for i in range(nxskv):
        for k in range(nyskv):
            if c1[i, k] >= 0.5:
                crez[i, k] += 1.0

    with open("output_1.txt", "w") as file:
        for i in range(nxskv - 1):
            for k in range(nyskv - 1):
                line = f"{i * 10. - 5. :12.5g} {k * 10. - 5. :12.5g} {c1[i, k] :12.5g} {crez[i, k] :12.5g} {vx[i, k] :12.5g} {vy[i, k] :12.5g}\n"
                file.write(line)
