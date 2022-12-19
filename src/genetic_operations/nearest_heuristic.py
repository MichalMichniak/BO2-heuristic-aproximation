from src.Instance import Instance
from src.LUT import LUT
from src.Acceptable_Solution_Generator import check_if_acceptable
"""
heuristic of nearest acceptable instance to unacceptable function (propagation time criterium)
"""

def heuristic_(instance : Instance, lut : LUT):
    t_max = instance.t_max
    func_vect = instance.funct_vect.copy()
    time = [[0 for j in range(len(func_vect[i]))] for i in range(len(func_vect))]
    for i in list(range(1,len(time)))[::-1]:
        for j in range(len(time[i])):
            if time[i][j] + lut.lut_[func_vect[i][j][0]].get_time() > t_max:
                func_vect[i][j] = (0,func_vect[i][j][1])
            time[i][j] += lut.lut_[func_vect[i][j][0]].get_time()
            for k in func_vect[i][j][1:]:
                time[i-1][k] = max(time[i][j],time[i-1][k])
    for j in range(len(time[0])):
        if time[0][j] + lut.lut_[func_vect[0][j][0]].get_time() > t_max: 
            func_vect[0][j] = [0,func_vect[0][j][1]]
        time[0][j] += lut.lut_[func_vect[0][j][0]].get_time()
    instance.set_funct_vect(func_vect)
    # print(check_if_acceptable(instance))
    return instance
