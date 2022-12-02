import src.main as s
import multiprocessing as m
import time
import threading
import queue
import src.main_process as m
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    m.main_process(4,20)
    
    """ Pawel jak nie wierzysz w multiprocesing to to pod spodem robi to samo co na gorze"""
    # funcs = s.get_funct()
    # approx_func = s.get_approx_funct()
    # lut = s.LUT()
    # for i in funcs:
    #     lut.add_funct(*i)
    # asc = s.ASC(lut,140,2,[16,16,16,16,8,4,2,1])
    # counter = s.Criterial_Funct_Counter(asc.architecture,asc.N,lut,nr_of_samplings_in_row=20)
    # for i in range(200):
    #     ista = asc.generate_instance()
    #     print(counter.count_criterial_funct(ista.get_funct_vect(), approx_func))
    pass