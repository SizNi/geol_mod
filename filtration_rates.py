import numpy as np
from math import cos, sin, radians


def rates(nx, ny, dx, dy, a1, nxskv, nyskv, nskv, kf, alfa, igrad, por):
    vx = vy = np.zeros((nx, ny), dtype=float)
    x1 = y1 = np.zeros(nskv)
    vx[:, :] = -kf * cos(radians(alfa)) * igrad / por
    vy[:, :] = -kf * sin(radians(alfa)) * igrad / por
