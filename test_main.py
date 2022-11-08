import src.main as s
import src.nothing_is_here.criterial_function as c
import src.Objective_Function as l
from copy import deepcopy
import timeit
if __name__ == '__main__':
    lut = s.LUT()
    f = lambda x,y: x+y
    lut.add_funct(f,10)
    lut.add_funct(f,2)
    lut.add_funct(f,12)
    lut.add_funct(f,13)
    lut.add_funct(f,20)
    f = lambda x: x+2
    lut.add_funct(f,2)
    lut.add_funct(f,5)
    lut.add_funct(f,1)
    asc = s.ASC(lut,30,3,[4,4,4,4,2,1])
    
    counter = c.Criterial_Funct_Counter(asc.architecture,asc.N,lut,nr_of_samplings_in_row=100)
    ista = asc.generate_instance()
    metric = lambda x,y: (x-y)**2
    of = l.Objective_Function(deepcopy(ista.get_funct_vect()),lut,metric)
    try:
        print("start")
        for i in range(1):
            counter.count_criterial_funct(ista.get_funct_vect(), lambda x,y,z: 0)
        print("end1")
        for i in range(1):
            of.calculate_for_all(asc.N,100,lambda x,y,z: 0)
        print("end2")
        
        
        
    except:
        print(ista.get_funct_vect())