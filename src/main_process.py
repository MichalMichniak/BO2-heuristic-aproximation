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

def print_conn(conn,global_queue : queue.Queue):
    while True:
        t = conn.recv()
        global_queue.put(t)
        print(f"{t}")

class Process_Package:
    def __init__(self,global_queue : queue.Queue,architecture,N):
        self.conn1,self.conn2 = m.Pipe()
        self.thrr = threading.Thread(target=print_conn, args=[self.conn2,global_queue])
        self.buffor = m.Queue()
        self.p = m.Process(target=slave_process, args=(self.conn1,self.buffor,architecture,N),kwargs={"nr_of_samplings_in_row":20,"process_id":1})
        pass

    def run(self):
        self.thrr.start()
        self.p.start()
        pass

    def put(self, instance):
        self.buffor.put(instance)



def main_process(process_number = 3, instance_count = 100):
    funcs = function_definisions.get_funct()
    approx_func = function_definisions.get_approx_funct()
    lut = LUT()
    for i in funcs:
        lut.add_funct(*i)
    asc = ASC(lut,140,2,[16,16,16,16,8,4,2,1])
    global_queue = queue.Queue()
    proc_lst = []
    maping_dict = {}
    ista = asc.generate_instance()
    for i in range(process_number):
        proc_lst.append(Process_Package(global_queue, asc.architecture,asc.N))
    for i in range(process_number):
        proc_lst[i].run()
    index = (i for i in range(100000))
    for j in range(100):
        if instance_count == 0:
                break
        for i in range(process_number):
            if instance_count == 0:
                break
            instance_count -=1
            ista = asc.generate_instance()
            temp_index = next(index)
            maping_dict[temp_index] = temp_index
            print(temp_index)
            proc_lst[i].put([ista.get_funct_vect(),temp_index])
            
    # for i in range(100):
    #     print(i)
    #     buffor.put([ista.get_funct_vect(),i])
    #     buffor.put([ista.get_funct_vect(),i])
    #     buffor.put([ista.get_funct_vect(),i])
    # print("bbb")
    
    # time.sleep(100)
    # buffor.put([function_definisions.DISCONNECT_MSG, 0])
    pass

