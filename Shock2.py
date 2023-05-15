import numpy as np
from Shock2com import *
import math
from Vel import vel


# преоборазование shock2 с фортрана в питон
def Shock2():
    nrand = 100
    npar = 5
    u = np.zeros((nrand, npar), dtype=np.float32)
    mmin=5
    mmax=10
    pormin=0.2
    pormax=0.4
    imin=0.001
    imax=0.01
    alfamin=270
    alfamax=330.0
    kmin=5
    kmax=20
    # задаем массивы
    vx = np.zeros((nx, ny), dtype=np.float)
    c = np.zeros((nx, ny), dtype=np.float)
    vy = np.zeros((nx, ny), dtype=np.float)
    cx = np.zeros((nx, ny), dtype=np.float)
    cy = np.zeros((nx, ny), dtype=np.float)
    q = np.zeros((nx, ny), dtype=np.float)
    for irand in range(1, nrand+1):
        igrad = imin + u[irand-1,0]*(imax - imin)
        alfa = alfamin + u[irand-1,1]*(alfamax - alfamin)
        m = mmin + u[irand-1,2]*(mmax - mmin)
        kf = kmin + u[irand-1,3]*(kmax - kmin)
        por = pormin + u[irand-1,4]*(pormax - pormin)
        for i in range(nskv):
            a1[i] = -a[i]/(m*por)
        # заполняем массивы
        for i in range(1, nx+1):
            for k in range(1, ny+1):
                vx[i,k] = kf*math.cos(math.radians(alfa))*igrad/por
                c[i,k] = 0.0
                vy[i,k] = kf*math.sin(math.radians(alfa))*igrad/por
                cx[i,k] = 0.0
                cy[i,k] = 0.0
        # вызываем модуль расчета
        vel(ny,nx,dx,dy,vx,vy,a1,nxskv,nyskv,nskv)
        for nsk in range(nskv):
            q[nxskv[nsk], nyskv[nsk]] = -a1[nsk]

