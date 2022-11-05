from src.Func import Func
from typing import Callable,List

class Func_f(Func):
    def __init__(self,f : Callable[[float],float], time : float):
        super().__init__(time)
        f_ : Callable[[float,float],float] = f