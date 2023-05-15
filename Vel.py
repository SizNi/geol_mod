import math


def vel(n1, n2, x, y, vx, vy, a, nx, ny, nskv):
    x1 = [0] * 100
    y1 = [0] * nskv

    for i in range(nskv):
        nxx = nx[i]
        for ix in range(2, nxx):
            x1[i] += (x[ix - 1] + x[ix]) / 2

        xc = x1[nskv]

        nyy = ny[i]
        for iy in range(2, nyy):
            y1[i] += (y[iy - 1] + y[iy]) / 2

        yc = y1[nskv]

    x2 = x[0] / 2
    y2 = y[0] / 2

    for k in range(2, n1):
        x2 = x[0] / 2
        for i in range(n2):
            y3 = y2 + y[k]
            for ns in range(nskv):
                yb = y3 - y1[ns]
                yh = y2 - y1[ns]
                xx = x2 - x1[ns]
                vx[i][k] = (-1) * a[ns] * (math.atan(yb / xx) - math.atan(yh / xx)) / y[
                    k
                ] + vx[i][k]

    x2 = x[0] / 2
    y2 = y[0] / 2

    for i in range(2, n2):
        y2 = y[0] / 2
        for k in range(1, n1):
            x3 = x2 + x[i]
            for ns in range(nskv):
                xp = x3 - x1[ns]
                xl = x2 - x1[ns]
                yy = y2 - y1[ns]
                vy[i][k] = (-1) * a[ns] * (math.atan(xp / yy) - math.atan(xl / yy)) / x[
                    i
                ] + vy[i][k]

    return vx, vy
