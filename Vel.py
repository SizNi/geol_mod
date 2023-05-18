import math


def vel(nx, ny, dx, dy, vx, vy, a1, nxskv, nyskv, nskv):
    x1 = [0] * 100
    y1 = [0] * (nskv)
    for i in range(nskv):
        nxx = nxskv[i]
        for ix in range(1, nxx):
           x1[i] = x1[i] + (dx[ix - 1] + dx[ix]) / 2      
        nyy = nyskv[i]
        for iy in range(1, nyy):
            y1[i] = y1[i] + (dy[iy - 1] + dy[iy]) / 2
    x2 = dx[0] / 2
    y2 = dy[0] / 2
    for k in range(1, ny):
        x2 = dx[0] / 2
        for i in range(nx):
            y3 = y2 + dy[k]
            for ns in range(nskv):
                yb = y3 - y1[ns]
                yh = y2 - y1[ns]
                xx = x2 - x1[ns]
                vx[i][k] = (-1) * a1[ns] * (math.atan(yb / xx) - math.atan(yh / xx)) / dy[k] + vx[i][k]
            if i < nx - 1:
                x2 = x2 + dx[i + 1]
        y2 = y3
    x2 = dx[0] / 2
    y2 = dy[0] / 2
    for i in range(1, nx):
        y2 = dy[0] / 2
        for k in range(ny):
            x3 = x2 + dx[i]
            for ns in range(nskv):
                xp = x3 - x1[ns]
                xl = x2 - x1[ns]
                yy = y2 - y1[ns]
                vy[i][k] = (-1) * a1[ns] * (math.atan(xp / yy) - math.atan(xl / yy)) / dx[i] + vy[i][k]
            if k < ny - 1:
                y2 = y2 + dy[k + 1]
        x2 = x3
    return vx, vy