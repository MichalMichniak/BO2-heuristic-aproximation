import src.main as s
import src.nothing_is_here.criterial_function as c
import src.Objective_Function as l
from copy import deepcopy
import timeit
if __name__ == '__main__':
    funcs = s.get_funct()
    lut = s.LUT()
    for i in funcs:
        lut.add_funct(*i)
    lut = s.LUT()
    asc = s.ASC(lut,140,2,[8,6,4,2,1])
    g = s.GeneticOperations(asc)
    ista = asc.generate_instance()