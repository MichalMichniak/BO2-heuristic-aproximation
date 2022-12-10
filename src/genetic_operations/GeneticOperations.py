
from src.Instance import Instance
from src.Acceptable_Solution_Generator import ASC
from random import randint
from  copy import deepcopy
import math
from typing import List
import numpy as np
class GeneticOperations:
    def __init__(self,asc : ASC) -> None:
        self.asc_ = asc
        pass

    def cross(self,parent1 : Instance,parent2 : Instance):
        func_vect = deepcopy(parent1.get_funct_vect())
        for n,i in enumerate(self.asc_.architecture):
            for j in range(i):
                rand = randint(0,1)
                if rand:
                    func_vect[n][j] = deepcopy(parent2.funct_vect[n][j])
        
        ins = Instance(self.asc_.t_max,self.asc_.N,self.asc_.architecture,self.asc_.lut)
        ins.set_funct_vect(func_vect)
        return ins

    def gen_oper_over_lst(self,lst,*args):
        new_population : List[Instance] = []
        scale = 100
        crosing = 0.85
        mutation = 0.05
        total_population = len(lst)
        crosing_population = math.ceil(total_population*crosing)
        rest = total_population - crosing_population
        for i in range(crosing_population):
            idx1 = int(min(math.floor(abs(np.random.normal(scale = scale))),len(lst)-1))
            idx2 = int(min(math.floor(abs(np.random.normal(scale = scale))),len(lst)-1))
            j = 0
            while idx1 == idx2:
                j+=1
                idx2 = int(min(math.floor(abs(np.random.normal(j,scale = scale))),len(lst)-1))
            new_population.append(self.cross(lst[idx1],lst[idx2]))
        new_population.extend(lst[:rest])
        for i in range(len(new_population)):
            if np.random.uniform()<mutation:
                row = randint(1,len(self.asc_.architecture)-1)
                col = randint(0,self.asc_.architecture[row]-1)
                new_fun_id = list(self.asc_.lut.lut_.keys())[randint(0, len(self.asc_.lut.lut_.keys())-1)]
                if self.asc_.lut.lut_[new_fun_id].n_param == 1:
                    new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1)]
                else:
                    new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1),randint(0,self.asc_.architecture[row-1]-1)]
        return new_population
