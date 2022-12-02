if __name__ == '__main__':
    import function_def.function_def as function_definisions
else:
    import src.function_def.function_def as function_definisions
    from src.LUT import LUT
    from src.nothing_is_here.criterial_function import Criterial_Funct_Counter
    from src.Acceptable_Solution_Generator import ASC
    from src.slave_process import slave_process

import threading
import queue
import time
import multiprocessing as m
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
                    print(f"finished processes : {global_count.initial_value}")
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

def split_counting(lst_instance,proc_lst):
    index = (i for i in range(100000))
    for j in range(len(lst_instance)):
        temp_index = next(index)
        #print(temp_index)
        proc_lst[j%len(proc_lst)].put([lst_instance[j].get_funct_vect(),temp_index])
    for i in range(len(proc_lst)):
        proc_lst[i].put(["end",0])

def get_lst_from_queue_sort(global_queue : queue.Queue,lst_instance):
    crit_idx_lst = []
    while not global_queue.empty():
        crit_idx_lst.append(global_queue.get())
    crit_idx_lst.sort(key=lambda x:x[0])
    lst = [lst_instance[j] for _,j in crit_idx_lst]
    return lst



def main_process(process_number = 3, instance_count = 100 , epoch = 3):
    funcs = function_definisions.get_funct()
    # approx_func = function_definisions.get_approx_funct()
    lut = LUT()
    
    for i in funcs:
        lut.add_funct(*i)
    asc = ASC(lut,140,2,[16,16,16,16,8,4,2,1])
    global_queue = queue.Queue()
    proc_lst = []
    maping_dict = {}
    ista = asc.generate_instance()
    count_lock = threading.Lock()
    global_count = Count()
    for i in range(process_number):
        proc_lst.append(Process_Package(global_queue, asc.architecture,asc.N,count_lock,global_count))
    for i in range(process_number):
        proc_lst[i].run()
    lst_instance = [asc.generate_instance() for i in range(instance_count)]
    split_counting(lst_instance,proc_lst)

    for i in range(epoch):
        print(f"Epoch : {i}")
        while global_count.initial_value != process_number:
            time.sleep(0.1)
        else:
            global_count.initial_value = 0
        lst_instance = get_lst_from_queue_sort(global_queue,lst_instance)
        # print(lst_instance)
        if i < epoch - 1:
            ##################################################
            """
            operacje genetyczne na populacji lst_instance
            TU PISAĆ KOD

            """
            lst_instance = lst_instance


            ##################################################
            split_counting(lst_instance,proc_lst)
        
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
    
    pass
