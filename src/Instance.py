from typing import List,Tuple
from src.LUT import LUT
class Instance:
    def __init__(self, t_max : float, N : int, architecture : List[int], lut : LUT):
        self.funct_vect : List[List[Tuple(int)]] = [[]]
        self.lut : LUT = lut
        self.architecture = architecture
        self.t_max = t_max
        self.N = N