from threading import Thread
import time
import numpy as np
import Queue
import barber
import client

class endStore:
    def __init__():
        self.end = "N"

def end():
    while end != Y:
        endStore.end = input("Do you want to close the store?(Y or N)")

        if(end != Y or end != N)
            print("please type Y or N")

def main:
    global mBarber = input("input barber: ")
    global nChair = input("input the number of chire: ")
    global Clientp = input("input cient: ")
    
    threadID1 = 1
    threadID2 = 1
    BarberThreads = []
    ClientQueue = Queue.Queue(nChair)

    for threadID1 in range(1, mBarber, ClientQueue):
        thread = barber.Barber(threadID1, "barber" + str(threadID1))
        thread.start()
        BarberThreads.append(thread)

    while gatattr(endStore, "end") != "Y":
        sleep(np.random.poisson(Clientp, 1))
        thread = client.Client(threadID2, "client"+str(threadID2))
        thread.start()
        ClientQueue.put(thread)
        threadID2 += threadID2

    ClientQueue.join()
