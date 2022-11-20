if __name__ == '__main__':
    import function_def.function_def as function_definisions
else:
    import src.function_def.function_def as function_definisions
    from src.LUT import LUT
    from src.nothing_is_here.criterial_function import Criterial_Funct_Counter

import threading
import queue
import time
def handle_conn(conn, buffor : queue.Queue):
    while True:
        print(" ewjqeiqw0oewq98ue9w8quwe98yqe98y")
        msg = conn.recv()
        if msg == function_definisions.DISCONNECT_MSG:
            break
        buffor.put(msg)
        time.sleep(0.1)


def slave_process(conn,buffor,architecture,N,nr_of_samplings_in_row=100, process_id = 0):
    print(f"process {process_id} starting")
    funcs = function_definisions.get_funct()
    approx_func = function_definisions.get_approx_funct()
    lut = LUT()
    for i in funcs:
        lut.add_funct(*i)
    counter = Criterial_Funct_Counter(architecture,N,lut,nr_of_samplings_in_row=nr_of_samplings_in_row)
    #conn_thr = threading.Thread(target=handle_conn,args=[conn,buffor])
    #conn_thr.start()
    print(f"process {process_id} finished starting")
    while True:#:conn_thr.is_alive()
        if buffor.empty():
            # do poprawienia
            time.sleep(0.01)
        else:
            # msg = conn.recv()
            # if msg == function_definisions.DISCONNECT_MSG:
            #     break
            # buffor.put(msg)
            func_vect, id = buffor.get()
            if type(func_vect) == str:
                break
            t = counter.count_criterial_funct(func_vect, approx_func)
            print("finished")
            conn.send([t,id])

    pass