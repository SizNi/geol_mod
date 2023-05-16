import numpy as np


def shock_1(c05, c, v, dx, dt, nx):
    # c = np.zeros(nx + 1, dtype=float)
    # print(c)
    c05 = np.zeros(nx, dtype=float)
    r = [1.0] * (nx + 1)  # Инициализируем массив r значениями 1.0
    f = [0.0] * (nx + 1)  # Инициализируем массив f значениями 0.0
    
    iapr = 2
    # iapr = 1
    # походу тут идет ошибочные ограничения счетчика
    for j in range(1, nx):
        sig = 1 if v[j] >= 0 else -1  # Определяем знак sig в зависимости от значения v[j]
        if iapr > 1:
            print(len(c))
            r1 = c[j + 1 - sig] - c[j - sig]  # Вычисляем r1
            r2 = c[j + 1] - c[j]  # Вычисляем r2
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
        c05[j] = 0.5 * (c[j] + c[j + 1]) - 0.5 * sig * (c[j + 1] - c[j]) + \
                0.5 * f[j] * (sig - dt * v[j] * 2.0 / (dx[j] + dx[j + 1])) * (c[j + 1] - c[j])
        # print(c05)
    # c.pop(0)  # Удаляем фиктивное значение, чтобы сделать массивы совместимыми с оригинальным кодом
    # c05.pop(0)  # Удаляем фиктивное значение, чтобы сделать массивы совместимыми с оригинальным кодом

    return c05
