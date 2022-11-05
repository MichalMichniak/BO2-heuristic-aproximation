from src.Func import Func
from typing import Callable,List

class Func_g(Func):
    """
    binary function class
    """
    def __init__(self,g : Callable[[float,float],float], time : float) -> None:
        """
        args:
            f : Callable[[float],float] - binary function
            t : float - propagation time
        """
        super().__init__(time,2)
        g_ : Callable[[float,float],float] = g