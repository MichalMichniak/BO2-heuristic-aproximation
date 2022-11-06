import src.main as s



if __name__ == '__main__':
    lut = s.LUT()
    f = lambda x,y: x**2+y
    lut.add_funct(f,10)
    lut.add_funct(f,2)
    lut.add_funct(f,12)
    lut.add_funct(f,13)
    lut.add_funct(f,20)
    f = lambda x: x**2
    lut.add_funct(f,2)
    lut.add_funct(f,5)
    lut.add_funct(f,1)
    asc = s.ASC(lut,30,2,[4,4,4,4,2,1])
    ista = asc.generate_instance()
    ista = s.prune(ista)
    for i in ista:
        print(i)
    pass