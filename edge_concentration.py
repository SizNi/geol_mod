import numpy as np


def edge(c_1, v_1, d_x, d_t, n_axis):
    c_05 = np.zeros(n_axis + 1, dtype=float)
    r = np.ones(n_axis + 1)  # Инициализируем массив r значениями 1.0
    f = np.zeros(n_axis + 1)  # Инициализируем массив f значениями 0.0
    c_05[0] = c_1[0]
    iapr = 2
    for i in range(1, n_axis - 1):
        # Определяем знак sig в зависимости от значения v[i]
        sig = 1 if v_1[i] >= 0 else -1
        if iapr > 1:
            r1 = c_1[i + 1 - sig] - c_1[i - sig]
            r2 = c_1[i + 1] - c_1[i]
            if r2 * r1 <= 0.0:
                r[i] = 0.0
            else:
                r[i] = r1 / r2
            if r[i] <= 0.0:
                f[i] = 0.0
            else:
                if r[i] <= 1.0:
                    f[i] = min(2.0 * r[i], 1.0)
                else:
                    f[i] = min(2.0, r[i])
        c_05[i] = (
            0.5 * (c_1[i] + c_1[i + 1])
            - 0.5 * sig * (c_1[i + 1] - c_1[i])
            + 0.5
            * f[i]
            * (sig - d_t * v_1[i] * 2.0 / (d_x[i] + d_x[i + 1]))
            * (c_1[i + 1] - c_1[i])
        )
    return c_05
