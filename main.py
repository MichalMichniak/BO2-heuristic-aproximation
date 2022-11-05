import src.main as s



if __name__ == '__main__':
    lut = s.LUT()
    f = lambda x: x**2
    lut.add_funct(f,10)
    pass