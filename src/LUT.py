from typing import Callable,List,Dict,Union,Optional
from src.Func_f import Func_f
from src.Func_g import Func_g
from src.Func import Func
class LUT:
    """
    Look up table

    index -> function
    """
    def __init__(self, lut : Dict[int, Func]= {}):
        """
        args:
            lut : Dict[int, Func] - initial mapping
        """
        self.lut_ = lut
        if len(lut.keys()) != 0:
            self.index = max(lut.keys())+1
        else:
            self.index = 0
    
    def add_funct(self,f : Callable[[float,Optional[float]],float], time : float):
        """
        add function to look up table
        args:
            f : Callable[[float,Optional[float]],float] - function to add
            time : float - propagation time of that function
        """
        try:
            f(0,0)
        except TypeError:
            self.lut_[self.index] = Func_f(f,time)
            self.index +=1
            return
        self.lut_[self.index] = Func_g(f,time)
        self.index +=1
