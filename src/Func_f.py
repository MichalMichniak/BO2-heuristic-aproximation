from src.Func import Func
from typing import Callable,List

class Func_f(Func):
    """
    unitary function class
    """
    def __init__(self,f : Callable[[float],float], time : float) -> None:
        """
        args:
            f : Callable[[float],float] - unitary function
            t : float - propagation time
        """
        super().__init__(time,1)
        f_ : Callable[[float,float],float] = f