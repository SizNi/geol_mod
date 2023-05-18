import numpy as np


def shock_1(c05, c1, v1, dx, dt, nx):
    r = [1.0] * (nx + 1)  # Инициализируем массив r значениями 1.0
    f = [0.0] * (nx + 1)  # Инициализируем массив f значениями 0.0
    c05[0] = c1[0]
    iapr = 2
    for j in range(1, nx - 1):
        sig = (
            1 if v1[j] >= 0 else -1
        )  # Определяем знак sig в зависимости от значения v[j]
        if iapr > 1:
            r1 = c1[j + 1 - sig] - c1[j - sig]
            r2 = c1[j + 1] - c1[j]
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
            0.5 * (c1[j] + c1[j + 1])
            - 0.5 * sig * (c1[j + 1] - c1[j])
            + 0.5
            * f[j]
            * (sig - dt * v1[j] * 2.0 / (dx[j] + dx[j + 1]))
            * (c1[j + 1] - c1[j])
        )
        # print(c05)
    # c.pop(0)  # Удаляем фиктивное значение, чтобы сделать массивы совместимыми с оригинальным кодом
    # c05.pop(0)  # Удаляем фиктивное значение, чтобы сделать массивы совместимыми с оригинальным кодом

    return c05