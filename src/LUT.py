from typing import Callable,List,Dict,Union
from src.Func_f import Func_f
from src.Func_g import Func_g

class LUT:
    def __init__(self, lut : Dict[int, Union[Callable[[float,float],float],Callable[[float],float]]]= {}):
        self.lut_ = lut
        self.index = max(lut.keys())+1
    
    def add_funct(self,f : Callable[[float,float],float], time):
        try:
            f(0,0)
        except TypeError:
            self.lut_[self.index] = Func_f(f,time)
            return
        self.lut_[self.index] = Func_g(f,time)