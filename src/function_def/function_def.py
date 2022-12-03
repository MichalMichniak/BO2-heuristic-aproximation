import numpy as np
DISCONNECT_MSG = "DISCONECT"
from typing import List

def bound_decorator(func, X : List[float] = [-5,5]):
    def bounded_func(*args,**kwargs):
        x = func(*args,**kwargs)
        if x > X[1]:
            x = X[1]
        elif x<X[0]:
            x = X[0]
        return x
    return bounded_func


def get_funct():
    func_lst = [(lambda x,y: max(min(x+y,5),-5),12),
    (lambda x,y: max(min(max(x,y),5),-5),13),
    (lambda x,y: max(min(x/y if y !=0 else 5,5),-5),4),
    (lambda x,y: max(min(min(x,y),5),-5),5),
    (lambda x: max(min(0.3*x,5),-5),10),
    (lambda x: max(min(np.exp(x) if x<10 else 5,5),-5),5),
    (lambda x: max(min(np.log(np.abs(x)+0.00001),5),-5),8),
    (lambda x: max(min(np.abs(x),5),-5),2),
    (lambda x: 1,2),
    (lambda x: 2,2),
    (lambda x: 3,2),
    (lambda x: 4,2),
    (lambda x: 5,2),
    (lambda x: max(min(-float(x),5),-5),3)
    ]
    return func_lst

def get_metric():
    return lambda x,y: (x-y)**2

def get_approx_funct():
    return lambda x,y: 5*np.sin(0.1*x)*np.cos(0.1*y)