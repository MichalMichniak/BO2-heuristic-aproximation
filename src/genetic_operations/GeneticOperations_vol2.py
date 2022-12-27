
from src.Instance import Instance
from src.Acceptable_Solution_Generator import ASC
from random import randint
from  copy import deepcopy
import math
from typing import List
import numpy as np
from src.LUT import LUT
from src.genetic_operations.nearest_heuristic import heuristic_

class GeneticOperations:
    def __init__(self,asc : ASC, X = [-5,5]) -> None:
        self.X = X
        self.asc_ = asc
        self.cross_variance_col = 50
        self.similarity_matrix = count_similarity_matrix(asc,X)
        pass

    def cross(self,parent1 : Instance,parent2 : Instance):
        func_vect = deepcopy(parent2.get_funct_vect())
        layer = max(min(int(np.random.normal(len(func_vect)//2 + 1, self.cross_variance_col)),0),len(func_vect)-1)
        place = np.random.randint(0,len(func_vect[layer]))
        lst = []
        lst2 = [place]
        for l in range(0,layer,-1):
            for pl in lst2:
                for arg in parent1.funct_vect[l][pl][1:]:
                    lst.append(arg)
                    func_vect[l][pl] = parent1.funct_vect[l][pl].copy()
            lst2 = lst
            lst = []
        ins = Instance(self.asc_.t_max,self.asc_.N,self.asc_.architecture,self.asc_.lut)
        ins.set_funct_vect(func_vect)
        return ins

    def gen_oper_over_lst(self, lst, criterial:List[float], lut : LUT, crosing = 0.60, hard_mutation = 0.05, nearby_func_mutation = 0.20, arguments_mutation = 0.10, typeofsurviving = "roulette", restrictions = True):
        new_population : List[Instance] = []
        
        ### probability of roulette
        proportions = np.array(criterial,dtype = float) - criterial[-1]
        sum_of_proportions = np.sum(proportions)
        individual_probabilities = proportions/sum_of_proportions
        cumultative_distribute_func = individual_probabilities
        for i in range(1,len(cumultative_distribute_func)):
            cumultative_distribute_func[i] = cumultative_distribute_func[i] + cumultative_distribute_func[i-1]
        ###


        total_population = len(lst)
        crosing_population = math.ceil(total_population*crosing)
        rest = total_population - crosing_population


        for i in range(crosing_population):
            ### roulette generation
            idx1 = get_idx_binary_search(np.random.uniform(),cumultative_distribute_func)%len(criterial)
            idx2 = get_idx_binary_search(np.random.uniform(),cumultative_distribute_func)%len(criterial)
            j = 0
            while idx1 == idx2:
                j+=1
                idx2 += np.random.randint(j,2+j)%len(criterial)
            new_population.append(self.cross(lst[idx1],lst[idx2]))

        if typeofsurviving == "roulette":
            # roulette chosing:
            survivors = []
            for i in range(rest):
                ### roulette generation
                survivors.append(lst[get_idx_binary_search(np.random.uniform(),cumultative_distribute_func)%len(criterial)]) 
            new_population.extend(survivors)
        elif typeofsurviving == "tournament":
            survivors = []
            for i in range(rest):
                ### tournament generation for set of 5 instances
                indexes = [np.random.randint(0,len(lst)-1) for i in range(5)]
                index = min(indexes)
                survivors.append(lst[index]) 
            new_population.extend(survivors)
        else:
            # best chosing:
            new_population.extend(lst[:rest])

        #Mutation operators

        # Hard mutation
        for i in range(len(new_population)):
            if np.random.uniform()<hard_mutation:
                row = randint(0,len(self.asc_.architecture)-1)
                col = randint(0,self.asc_.architecture[row]-1)
                new_fun_id = list(self.asc_.lut.lut_.keys())[randint(0, len(self.asc_.lut.lut_.keys())-1)]
                if row == 0:
                    if self.asc_.lut.lut_[new_fun_id].n_param == 1:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.N-1)]
                    else:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.N-1),randint(0,self.asc_.N-1)]
                else:
                    if self.asc_.lut.lut_[new_fun_id].n_param == 1:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1)]
                    else:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1),randint(0,self.asc_.architecture[row-1]-1)]
        
        # mutation of arguments
        for i in range(len(new_population)):
            if np.random.uniform()<arguments_mutation:
                row = randint(0,len(self.asc_.architecture)-1)
                col = randint(0,self.asc_.architecture[row]-1)
                new_fun_id = new_population[i].funct_vect[row][col][0]
                if row == 0:
                    if self.asc_.lut.lut_[new_fun_id].n_param == 1:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.N-1)]
                    else:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.N-1),randint(0,self.asc_.N-1)]
                else:
                    if self.asc_.lut.lut_[new_fun_id].n_param == 1:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1)]
                    else:
                        new_population[i].funct_vect[row][col] = [new_fun_id, randint(0,self.asc_.architecture[row-1]-1),randint(0,self.asc_.architecture[row-1]-1)]
        
        # mutation of nearby function
        for i in range(len(new_population)):
            if np.random.uniform()<nearby_func_mutation:
                row = randint(0,len(self.asc_.architecture)-1)
                col = randint(0,self.asc_.architecture[row]-1)
                old_func = new_population[i].funct_vect[row][col][0]
                random_prob = np.random.uniform()
                new_fun_id = 0
                random_prob -= self.similarity_matrix[old_func,new_fun_id]
                while random_prob >=0 and new_fun_id<len(self.similarity_matrix)-1:
                    new_fun_id += 1
                    random_prob -= self.similarity_matrix[old_func,new_fun_id]
                new_param = [list(self.asc_.lut.lut_.keys())[new_fun_id]]
                if self.asc_.lut.lut_[new_param[0]].n_param == 1:
                    new_param.append(list(new_population[i].funct_vect[row][col])[1])
                else:   
                    new_param.extend(list(new_population[i].funct_vect[row][col])[1:])
                if self.asc_.lut.lut_[new_param[0]].n_param == 2 and len(new_param) == 2:
                    if row == 0:
                        new_argument = randint(0,self.asc_.N-1)
                    else:
                        new_argument = randint(0,self.asc_.architecture[row-1]-1)
                    new_param.append(new_argument)
                new_population[i].funct_vect[row][col] = new_param.copy()
        if restrictions:
            for i in range(len(new_population)):
                new_population[i] = heuristic_(new_population[i],lut)
        return new_population

def get_idx_binary_search(value,dystrybuanta,a=0,b=None):
    """
    binary search for place in distribuantt of the bigest index
    that is less or equal given probability value.

    args:
        value : float - upper boundary of searched value
        a : beggining search index
        b : end search index
    """
    if b == None:
        b = len(dystrybuanta)-1
    if b-a == 2:
        if dystrybuanta[b]<=value:
            return b
        elif dystrybuanta[b-1]<=value:
            return b-1
        else:
            return a 
    elif b-a == 1:
        if dystrybuanta[b]<=value:
            return b
        else:
            return a 
    elif b-a == 0:
        return a
    if dystrybuanta[(a+b)//2]>value:
        return get_idx_binary_search(value,dystrybuanta,a,(a+b)//2-1)
    else:
        return get_idx_binary_search(value,dystrybuanta,(a+b)//2,b)

def count_similarity_matrix(asc : ASC, X = [-5,5], sampling = 20, metric = None):
    if metric == None:
        metric = lambda x,y: abs(x-y)
    sample = np.linspace(X[0],X[1],sampling)
    sim_matrix = np.zeros([len(asc.lut.lut_),len(asc.lut.lut_)])
    for i in range(len(asc.lut.lut_)):
        for j in range(len(asc.lut.lut_)):
            func1 = asc.lut.lut_[list(asc.lut.lut_.keys())[i]]
            func2 = asc.lut.lut_[list(asc.lut.lut_.keys())[j]]
            if func1.n_param == 2 and func2.n_param == 2:
                nr_sampl = sampling**2
                suma = 0.0
                for arg1 in sample:
                    for arg2 in sample:
                        suma+= metric(func1.g_(arg1,arg2),func2.g_(arg1,arg2))
                sim_matrix[i,j] = suma/nr_sampl
            elif func1.n_param == 1 and func2.n_param == 1:
                nr_sampl = sampling
                suma = 0.0
                for arg1 in sample:
                    suma+= metric(func1.f_(arg1),func2.f_(arg1))
                sim_matrix[i,j] = suma/nr_sampl
            else:
                if func1.n_param == 1:
                    func1,func2 = func2,func1
                nr_sampl = 2*sampling**2
                suma = 0.0
                for arg1 in sample:
                    for arg2 in sample:
                        suma+= metric(func1.g_(arg1,arg2),func2.f_(arg1))
                for arg1 in sample:
                    for arg2 in sample:
                        suma+= metric(func1.g_(arg1,arg2),func2.f_(arg2))
                sim_matrix[i,j] = suma/nr_sampl
    for i in range(len(asc.lut.lut_)):
        sim_matrix[i,:] = (np.max(sim_matrix[i,:])-sim_matrix[i,:])
        sim_matrix[i,:] = sim_matrix[i,:]/np.sum(sim_matrix[i,:])
    for i in range(len(asc.lut.lut_)):
        sim_matrix[i,i] = 0
    print(sim_matrix)
    return sim_matrix
                
