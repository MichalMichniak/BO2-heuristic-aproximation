from src.LUT import LUT
from src.Instance import Instance
from typing import List
import random

class ASC:
    def __init__(self,lut : LUT, t_max : float, N : int, architecture : List[int])->None:
        if min(architecture) <=0:
            raise ValueError("number of functions in layer can't be negative or zero")
        self.lut = lut
        self.t_max = t_max
        self.id_func_idx = lut.id_func_idx
        self.N = N
        self.architecture = architecture
        self.dict_idx_t = [(i,self.lut.lut_[i].get_time(),self.lut.lut_[i].n_param) for i in self.lut.lut_.keys()]
        # TODO: filtering function t>t_max
        self.dict_idx_t = sorted(self.dict_idx_t,key= lambda x: x[1])
        self.dict_idx_len = len(self.dict_idx_t) - 1
        pass

    def binary_search(self,t,a=0,b=None):
        if b == None:
            b = self.dict_idx_len
        if b-a == 2:
            if self.dict_idx_t[b][1]<=t:
                return b
            elif self.dict_idx_t[b-1][1]<=t:
                return b-1
            else:
                return a 
        elif b-a == 1:
            if self.dict_idx_t[b][1]<=t:
                return b
            else:
                return a 
        elif b-a == 0:
            return a
        if self.dict_idx_t[(a+b)//2][1]>t:
            return self.binary_search(t,a,(a+b)//2-1)
        else:
            return self.binary_search(t,(a+b)//2,b)

    def generate_instance(self)->Instance:
        funct_vect = [[None for j in range(i)] for i in self.architecture]
        funct_vect_temp = [[[] for j in range(i)] for i in self.architecture]
        for i in list(range(len(self.architecture)))[::-1]:
            if i == len(self.architecture)-1:
                for j in range(self.architecture[i]):
                    r = random.randint(0,self.dict_idx_len-1)
                    if self.dict_idx_t[r][2] == 1:
                        first_arg = random.randint(0,self.architecture[i-1]-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg)
                        funct_vect_temp[i][j] = self.dict_idx_t[r][1]
                        funct_vect_temp[i-1][first_arg].append(j)
                    elif self.dict_idx_t[r][2] == 2:
                        first_arg = random.randint(0,self.architecture[i-1]-1)
                        second_arg = random.randint(0,self.architecture[i-1]-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg,second_arg)
                        funct_vect_temp[i][j] = self.dict_idx_t[r][1]
                        funct_vect_temp[i-1][first_arg].append(j)
                        funct_vect_temp[i-1][second_arg].append(j)
                    else:
                        raise ValueError("bad function n_param value. Too many parameters in func")
            elif i == 0:
                for j in range(self.architecture[i]):
                    t = 0
                    for k in funct_vect_temp[i][j]:
                        if funct_vect_temp[i+1][k] >= t:
                            t = funct_vect_temp[i+1][k]
                    n = self.binary_search(self.t_max - t)
                    r = random.randint(0,n)
                    if self.dict_idx_t[r][2] == 1:
                        first_arg = random.randint(0,self.architecture[i-1]-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg)
                    elif self.dict_idx_t[r][2] == 2:
                        first_arg = random.randint(0,self.N-1)
                        second_arg = random.randint(0,self.N-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg,second_arg)
            else:
                for j in range(self.architecture[i]):
                    t = 0
                    for k in funct_vect_temp[i][j]:
                        if funct_vect_temp[i+1][k] >= t:
                            t = funct_vect_temp[i+1][k]
                    n = self.binary_search(self.t_max - t)
                    r = random.randint(0,n)
                    if self.dict_idx_t[r][2] == 1:
                        first_arg = random.randint(0,self.architecture[i-1]-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg)
                        funct_vect_temp[i][j] = self.dict_idx_t[r][1]+t
                        funct_vect_temp[i-1][first_arg].append(j)
                    elif self.dict_idx_t[r][2] == 2:
                        first_arg = random.randint(0,self.architecture[i-1]-1)
                        second_arg = random.randint(0,self.architecture[i-1]-1)
                        funct_vect[i][j]=(self.dict_idx_t[r][0],first_arg,second_arg)
                        funct_vect_temp[i][j] = self.dict_idx_t[r][1]+t
                        funct_vect_temp[i-1][first_arg].append(j)
                        funct_vect_temp[i-1][second_arg].append(j)
        new_instance = Instance(self.t_max,self.N,self.architecture,self.lut)
        new_instance.set_funct_vect(funct_vect)
        return new_instance

def check_if_acceptable(inst : Instance)->bool:
    inst_vect = inst.get_funct_vect()
    inst_vect_t = [[None for j in i] for i in inst_vect]
    for j in range(len(inst_vect[0])):
        temp = inst_vect[0][j]
        inst_vect_t[0][j] = inst.lut.lut_[temp[0]].get_time()
    for i in range(1,len(inst_vect)):
        for j in range(len(inst_vect[i])):
            temp = inst_vect[i][j]
            t_func = inst.lut.lut_[temp[0]].get_time()
            t_prev_max = 0
            for k in temp[1:]:
                if t_prev_max<inst_vect_t[i-1][k]:
                    t_prev_max = inst_vect_t[i-1][k]
            inst_vect_t[i][j] = t_prev_max + t_func
    return inst_vect_t[-1][0] <= inst.t_max
