from typing import List,Tuple
from src.LUT import LUT
class Instance:
    def __init__(self, t_max : float, N : int, architecture : List[int], lut : LUT):
        self.funct_vect : List[List[Tuple(int)]] = [[]]