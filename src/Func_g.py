from src.Func import Func
from typing import Callable,List

class Func_g(Func):
    def __init__(self,g : Callable[[float,float],float], time : float):
        super().__init__(time)
        g_ : Callable[[float,float],float] = g