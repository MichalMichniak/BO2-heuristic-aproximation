from src.LUT import LUT
from src.Instance import Instance
from typing import List

class ASC:
    def __init__(self,lut : LUT, t_max : float, N : int, architecture : List[int])->None:
        self.lut = lut
        self.t_max = t_max
        
        pass
