from typing import List,Tuple
from src.LUT import LUT
class Instance:
    """
    One instance of solution class
    """
    def __init__(self, t_max : float, N : int, architecture : List[int], lut : LUT) -> None:
        """
        args:
            t_max : float - maximum propagation time of whole net
            N : int - number of inputs in net
            architecture : List[int] - list of numbers of functions in each layer
            lut : LUT - look up table, dictionary which is mapping indexes -> functions
        """
        self.funct_vect : List[List[Tuple(int)]] = [[]]
        self.lut : LUT = lut
        self.architecture = architecture
        self.t_max = t_max
        self.N = N

    def 