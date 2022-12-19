import src.main as s
import src.genetic_operations.nearest_heuristic as n
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
    asc = s.ASC(lut,4,2,[8,6,4,2,1])
    ista2 = asc.generate_instance()
    ista2.set_funct_vect(ista1.get_funct_vect())
    print(n.heuristic_(ista2,lut))

    print(g.cross(ista1,ista2))