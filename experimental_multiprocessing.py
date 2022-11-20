import multiprocessing
import threading
import os
import time
from src.main import *
MSGCLOSE = "CLOSE"

def proc(conn,lut):
    time.sleep(10)
    while True:
        msg = conn.recv()
        if msg == MSGCLOSE:
            break
        print(f"hello world {msg[0]}")
    conn.close()

if __name__ == '__main__':
    lut = LUT()
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
    conn1, conn2 = multiprocessing.Pipe(duplex=True)
    conn12, conn22 = multiprocessing.Pipe(duplex=True)
    child = multiprocessing.Process(target=proc,args=[conn1,lut])
    child1 = multiprocessing.Process(target=proc,args=[conn12,lut])
    child.start()
    child1.start()
    conn2.send("hello world")
    print("1")
    conn2.send([[2,2,3],[12,3,4]])
    print("2")
    conn2.send(MSGCLOSE)
    conn22.send("hello world")
    print("1")
    conn22.send([[2,2,3],[12,3,4]])
    print("2")
    conn22.send(MSGCLOSE)
    child.join()
    child1.join()