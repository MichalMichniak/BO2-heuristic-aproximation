import src.main as s
import timeit
if __name__ == '__main__':
    funcs = s.get_funct()
    lut = s.LUT()
    for i in funcs:
        lut.add_funct(*i)
    lut = s.LUT()
    asc = s.ASC(lut,140,2,[8,6,4,2,1])
    g = s.GeneticOperations(asc)
    ista1 = asc.generate_instance()
    ista2 = asc.generate_instance()
    print(ista1)
    print(ista2)
    print(g.cross(ista1,ista2))