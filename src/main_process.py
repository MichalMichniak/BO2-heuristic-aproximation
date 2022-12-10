import src.gui

if __name__ == '__main__':
    import function_def.function_def as function_definisions
else:
    import src.function_def.function_def as function_definisions
    from src.LUT import LUT
    from src.nothing_is_here.criterial_function import Criterial_Funct_Counter
    from src.Acceptable_Solution_Generator import ASC
    from src.slave_process import slave_process
    from src.genetic_operations.GeneticOperations import GeneticOperations
import threading
import queue
import time
import multiprocessing as m
import numpy as np
import itertools
from typing import List
from src.gui import global_y, global_progress, global_rdy_flag, global_arg, global_exit
class Count:
    """
    glogal counter of finished processes
    """
    def __init__(self,initial_value = 0) -> None:
        self.initial_value =initial_value
        

def print_conn(conn,global_queue : queue.Queue,count_lock : threading.Lock,global_count:Count):
    """
    function counter process interface
    every result is saved in global_queue as [criterial function value , index of instance]
    """
    while True:
        t = conn.recv()
        if type(t) == str:
            if t == "DISCONECT":
                conn.close()
                print(f"disconected processes : {t}")
                break
            else:
                with count_lock:
                    global_count.initial_value +=1
                    #print(f"finished processes : {global_count.initial_value}")
        else:
            global_queue.put(t)
        #print(f"{t}")

class Process_Package:
    """
    class managing one process of criterial function count
    """
    def __init__(self,global_queue : queue.Queue,architecture,N,count_lock : threading.Lock,global_count:Count):
        self.conn1,self.conn2 = m.Pipe()
        self.thrr = threading.Thread(target=print_conn, args=[self.conn2,global_queue,count_lock,global_count])
        self.buffor = m.Queue()
        self.p = m.Process(target=slave_process, args=(self.conn1,self.buffor,architecture,N),kwargs={"nr_of_samplings_in_row":10,"process_id":1})
        pass

    def run(self):
        """
        start of the process
        """
        self.thrr.start()
        self.p.start()
        pass

    def put(self, instance):
        """
        add instance to compute criterial function
        every instance consist of [encoded function, index of instance]
        """
        self.buffor.put(instance)

def split_counting(lst_instance : List,proc_lst : List[Process_Package]):
    """
    function that splits counting to different processes
    argv:
        lst_instance : List[Instance] - list of instances to count
        proc_lst : List[Process_Package] - list of counting proceses
    """
    index = (i for i in itertools.count(start=0))
    for j in range(len(lst_instance)):
        temp_index = next(index)
        proc_lst[j%len(proc_lst)].put([lst_instance[j].get_funct_vect(),temp_index])
    for i in range(len(proc_lst)):
        proc_lst[i].put(["end",0])

def get_lst_from_queue_sort(global_queue : queue.Queue,lst_instance : List):
    """
    return the multithreading queue content in sorted list
    """
    crit_idx_lst = []
    while not global_queue.empty():
        crit_idx_lst.append(global_queue.get())
    crit_idx_lst.sort(key=lambda x:x[0])
    print(crit_idx_lst[:1])
    last = crit_idx_lst[:1]
    lst = [lst_instance[j] for _,j in crit_idx_lst]
    return lst, last



def main_process(process_number = 3, instance_count = 100, max_iteration = 4):
    """
    main function that control subprocesses and contain main program loop
    """
    funcs = function_definisions.get_funct()
    lut = LUT()
    
    for i in funcs:
        lut.add_funct(*i)
    asc = ASC(lut,140,2,[8,6,4,2,1])
    global_queue = queue.Queue()
    #gui = src.gui.GUI([[i for i in range(instance_count)],[0 for i in range(instance_count)]])
    #gui.run()
    global_arg[:] = [process_number, instance_count, max_iteration]
    gui_process = threading.Thread(target=src.gui.start)
    gui_process.start()
    while 1:
        while not global_rdy_flag[0]:
            process_number = global_arg[0]
            instance_count = global_arg[1]
            max_iteration = global_arg[2]
            time.sleep(0.100)
            pass
        global_y[:] = []
        proc_lst = []
        # maping_dict = {}
        # ista = asc.generate_instance()
        g = GeneticOperations(asc)
        count_lock = threading.Lock()
        global_count = Count()
        for i in range(process_number):
            proc_lst.append(Process_Package(global_queue, asc.architecture,asc.N,count_lock,global_count))
        for i in range(process_number):
            proc_lst[i].run()
        lst_instance = [asc.generate_instance() for i in range(instance_count)]
        split_counting(lst_instance,proc_lst)

        for i in range(max_iteration):
            print(f"iteration : {i}")
            while global_count.initial_value != process_number:
                time.sleep(0.1)
            else:
                global_count.initial_value = 0
            lst_instance, last = get_lst_from_queue_sort(global_queue, lst_instance)
            global_y.append(last[0][0])
            global_progress[0] = int(i/max_iteration*100 + 1)
            #gui.plot_data.data_y[i] = last[0][0];
            # print(lst_instance)
            if i < max_iteration - 1:
                ##################################################
                """
                operacje genetyczne na populacji lst_instance
                TU PISAĆ KOD
    
                """
                lst_instance = g.gen_oper_over_lst(lst_instance)


                ##################################################
                split_counting(lst_instance, proc_lst)

        # for i in range(100):
        #     print(i)
        #     buffor.put([ista.get_funct_vect(),i])
        #     buffor.put([ista.get_funct_vect(),i])
        #     buffor.put([ista.get_funct_vect(),i])
        # print("bbb")

        # time.sleep(100)
        # buffor.put([function_definisions.DISCONNECT_MSG, 0])
        print("######DISCONECTING AND JOINING STAGE##############")
        for i in proc_lst:
            i.put(["DISCONECT",0])
            i.p.join()
        global_rdy_flag[0] = 0

    pass

