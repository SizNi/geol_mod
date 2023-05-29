from dataclasses import dataclass
import numpy as np


@dataclass
class Block:
    # координаты блока
    x = 0.0
    y = 0.0
    # коэффициент фильтрации
    k_f: float = 0.0
    # скорости по двум направлениям
    v_x: float = 0.0
    v_y: float = 0.0
    # концентрации по двум направлениям
    c_x: float = 0.0
    c_y: float = 0.0
    # общее значение концентраций
    c: float = 0.0
    # расходы скважин
    q: float = 0.0
    # факт дохода фронта до блока
    migration_front: int = 0


@dataclass
class Well:
    # координаты скважины
    n_x_skv: int = 0
    n_y_skv: int = 0
    # дебит скважины
    q_skv: float = 0
