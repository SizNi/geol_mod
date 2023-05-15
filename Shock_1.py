def shock_1(c05, c, v, dx, dt, nx):
    c05[0] = c[0]
    nstr = nx
    r = [1.0] * nx
    f = [0.0] * nx

    iapr = 2
    for j in range(1, nstr - 1):
        sig = 1.0 if v[j] >= 0 else -1.0
        if iapr > 1:
            r1 = c[j + 1 - sig] - c[j - sig]
            r2 = c[j + 1] - c[j]
            if r2 * r1 <= 0.0:
                r[j] = 0.0
            else:
                r[j] = r1 / r2
            if r[j] <= 0.0:
                f[j] = 0.0
            else:
                if r[j] <= 1.0:
                    f[j] = min(2.0 * r[j], 1.0)
                else:
                    f[j] = min(2.0, r[j])
        c05[j] = (
            0.5 * (c[j] + c[j + 1])
            - 0.5 * sig * (c[j + 1] - c[j])
            + 0.5
            * f[j]
            * (sig - dt * v[j] * 2.0 / (dx[j] + dx[j + 1]))
            * (c[j + 1] - c[j])
        )
    return c05
