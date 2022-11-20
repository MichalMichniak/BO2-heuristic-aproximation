import multiprocessing
import threading
import os
import time

MSGCLOSE = "CLOSE"

def proc(conn):
    time.sleep(10)
    while True:
        msg = conn.recv()
        if msg == MSGCLOSE:
            break
        print(f"hello world {msg[0]}")
    conn.close()

if __name__ == '__main__':
    conn1, conn2 = multiprocessing.Pipe(duplex=True)
    conn12, conn22 = multiprocessing.Pipe(duplex=True)
    child = multiprocessing.Process(target=proc,args=[conn1])
    child1 = multiprocessing.Process(target=proc,args=[conn12])
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