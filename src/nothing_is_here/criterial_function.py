from typing import Callable, List, Tuple, Dict
from src.LUT import LUT
import numpy as np

class Criterial_Funct_Counter:
    """
    count criterial function for given architecture
    """
    def __init__(self,architecture : List[int],N : int, lut : LUT, X_space : List[int]= [-5,5], nr_of_samplings_in_row = 10, metric : Callable[[float,float],float]= None):
        """
        init

        args:
            architecture : List[int] - given architecture
            N : int - number of inputs
        """
        if metric==None:
            self.metric = lambda x,y: (x-y)**2
        else:
            self.metric = metric
        self.architecture = architecture
        self.N = N
        self.lut = lut
        self.initial_sol = [[[] for i in range(j)] for j in self.architecture]
        self.v_map = [[] for i in range(self.N)]
        self.initial_sampling = np.linspace(X_space[0],X_space[1],nr_of_samplings_in_row)
        self.func_temp = [[0 for i in range(j)] for j in self.architecture]

    def count_single(self, v : List[float], func : List[List[Tuple[int]]]):
        # works when given architecture is corect
        if len(v) != self.N:
            raise ValueError("bad dimensionality of given input")
        self.func_temp = [[0 for i in range(j)] for j in self.architecture]
        for j in range(self.architecture[0]):
            if self.lut[func[0][j][0]].n_param == 1:
                self.func_temp[0][j] = self.lut[func[0][j][0]].f_(v[func[0][j][1]])
            else:
                self.func_temp[0][j] = self.lut[func[0][j][0]].g_(v[func[0][j][1]],v[func[0][j][2]])
        for i in range(1,len(self.architecture)):
            for j in range(self.architecture[i]):
                if self.lut[func[i][j][0]].n_param == 1:
                    self.func_temp[i][j] = self.lut[func[i][j][0]].f_(self.func_temp[i-1][func[i][j][1]])
                else:
                    self.func_temp[i][j] = self.lut[func[i][j][0]].g_(self.func_temp[i-1][func[i][j][1]],self.func_temp[i-1][func[i][j][2]])
        return self.func_temp[-1][0]
    
    def count_next(self,forward_way : List[bool], index : List[int]):
        i = 0
        
        index[i] += 1 if forward_way[i] else -1
        while index[i] == len(self.initial_sampling) or index[i] == -1:
            forward_way[i] = not forward_way[i]
            index[i] += 1 if forward_way[i] else -1
            i+=1
            if i > self.N:
                raise IndexError()
            index[i] += 1 if forward_way[i] else -1
        return forward_way,index,i

    def revers_func(self,func:List[List[Tuple[int]]]):
        tab = []
        for i in func[-1][0][1:]:
            tab.append([i,len(func)-2])
            if 0 not in self.initial_sol[-2][i]:
                self.initial_sol[-2][i].append(0)
        while len(tab) != 0:
            temp = tab[0]
            tab.pop(0)
            for i in func[temp[1]][temp[0]][1:]:
                if temp[1] > 0:
                    tab.append([i,temp[1]-1])
                    if temp[0] not in self.initial_sol[temp[1]-1][i]:
                        self.initial_sol[temp[1]-1][i].append(temp[0])
                else:
                    if temp[0] not in self.v_map[i]:
                        self.v_map[i].append(temp[0])

    def count_one_change(self,func:List[List[Tuple[int]]],change : int, v : float):

        tab = []
        for i in self.v_map[change]:
            tab.append([i,0])
        if len(tab) == 0:
            return self.func_temp[-1][0]
        while tab[0][1] == 0:
            temp = tab[0]
            tab.pop(0)
            if self.lut[func[temp[1]][temp[0]][0]].n_param == 1:
                self.func_temp[temp[1]][temp[0]] = self.lut[func[temp[1]][temp[0]][0]].f_(v[func[temp[1]][temp[0]][1]])
            else:
                self.func_temp[temp[1]][temp[0]] = self.lut[func[temp[1]][temp[0]][0]].g_(v[func[temp[1]][temp[0]][1]],v[func[temp[1]][temp[0]][2]])
            for i in self.initial_sol[temp[1]][temp[0]]:
                tab.append([i,temp[1]+1])
            pass
        while len(tab) != 0:
            temp = tab[0]
            tab.pop(0)
            if self.lut[func[temp[1]][temp[0]][0]].n_param == 1:
                self.func_temp[temp[1]][temp[0]] = self.lut[func[temp[1]][temp[0]][0]].f_(self.func_temp[temp[1]-1][func[temp[1]][temp[0]][1]])
            else:
                self.func_temp[temp[1]][temp[0]] = self.lut[func[temp[1]][temp[0]][0]].g_(self.func_temp[temp[1]-1][func[temp[1]][temp[0]][1]],self.func_temp[temp[1]-1][func[temp[1]][temp[0]][2]])
            for i in self.initial_sol[temp[1]][temp[0]]:
                tab.append([i,temp[1]+1])
        return self.func_temp[-1][0]

    def count_criterial_funct(self, func : List[List[Tuple[int]]], y : Callable):
        index = [0 for i in range(self.N)]
        param = [self.initial_sampling[0] for i in range(self.N)]
        f_c = self.metric(self.count_single(param,func),y(*param))
        forward_way = [True for i in range(self.N)]
        self.revers_func(func)
        run = True
        while run:
            try:
                forward_way,index,change = self.count_next(forward_way,index)
            except IndexError:
                run = False
                continue
            param[change] = self.initial_sampling[index[change]]
            f_c += self.metric(self.count_one_change(func,change,param),y(*param))
        return f_c


