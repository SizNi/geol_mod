import numpy as np


def vel(nx, ny, dx, dy, vx, vy, a1, nxskv, nyskv, nskv):
    x1 = np.zeros(nskv)
    y1 = np.zeros(nskv)

    for i in range(nskv):
        x1[i] = np.sum((dx[: nxskv[i] - 1] + dx[1 : nxskv[i]]) / 2)
        y1[i] = np.sum((dy[: nyskv[i] - 1] + dy[1 : nyskv[i]]) / 2)

    x2 = dx[0] / 2
    y2 = dy[0] / 2

    for k in range(1, ny):
        y3 = y2 + dy[k]
        for i in range(nx):
            for ns in range(nskv):
                yb = y3 - y1[ns]
                yh = y2 - y1[ns]
                xx = x2 - x1[ns]
                vx[i, k] -= a1[ns] * (np.arctan(yb / xx) - np.arctan(yh / xx)) / dy[k]
            if i < nx - 1:
                x2 += dx[i + 1]
        y2 = y3

    x2 = dx[0] / 2
    y2 = dy[0] / 2

    for i in range(1, nx):
        x3 = x2 + dx[i]
        for k in range(ny):
            for ns in range(nskv):
                xp = x3 - x1[ns]
                xl = x2 - x1[ns]
                yy = y2 - y1[ns]
                vy[i, k] -= a1[ns] * (np.arctan(xp / yy) - np.arctan(xl / yy)) / dx[i]
            if k < ny - 1:
                y2 += dy[k + 1]
        x2 = x3
    return vx, vy
