import src.main as s
import nothing_is_here.criterial_function as c
import src.Objective_Function as l
from copy import deepcopy

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
    asc = s.ASC(lut,30,4,[4,4,4,4,2,1])
    
    counter = c.Criterial_Funct_Counter(asc.architecture,asc.N,lut)
    ista = asc.generate_instance()
    metric = lambda x,y: (x-y)**2
    of = l.Objective_Function(s.prune(deepcopy(ista.get_funct_vect())),lut,metric)
    try:
        print(of.calculate_for_all(asc.N,10,lambda x,y,z,w: 0))
        print(counter.count_criterial_funct(ista.get_funct_vect(), lambda x,y,z,w: 0))
    except:
        print(ista.get_funct_vect())