from dataclasses import dataclass
import numpy as np


@dataclass
class Well:
    # координаты скважины
    n_x_skv: int = 0
    n_y_skv: int = 0
    # дебит скважины
    q_skv: float = 0


well = Well(1, 1, 1)
well_2 = Well(4, 4, 4)
well_3 = Well(5, 5, 5)
well_ms = np.array([well, well_2, well_3])
q_list = np.array([obj.q_skv for obj in well_ms])
print(q_list)
print(well_ms)
