from threading import Thread
import time
import numpy as np
import queue
import barber
import client

global onChair          #onChair is record how many clients in waitting room
onChair = 0

class endStore:         #endStore contain value wheather we end the program
    def __init__():
        self.end = "N"

global endS
endS = endStore()

def end():              #end function try to get the input if user want to terminate the program or not
    while end != "Y":
        endStore.end = input("Do you want to close the store?(Y or N)")

        if end != "Y" or end != "N" :
            print("please type Y or N")

def main():             #main function of  barber-client problem
    global mBarber      #mBarber record "m" barber is working
    mBarber = input("input barber: ")
    global nChair       #nChair record "n" chair in waiting room
    nChair = input("input the number of chire: ")
    global Clientp      #Clientp record the frequent parameter of clients come
    Clientp = input("input cient: ")
    
    wakeUpbarber = threading.Condition()    #Wheather the client can wake up barbers  
    enter = threading.Condition()           #Wheather the client can enter the waiting room

    callClient = threading.Condition()      #Wheather the barber can call next client
    
    threadID1 = 1                           #threadID1 record the number of barbers
    threadID2 = 1                           #threadID2 record the number of clients
    BarberThreads = []                      #BarberThreads cantain all barbers who are working
    ClientQueue = Queue.Queue(nChair)       #ClientQueue contain all clients in the store

    for threadID1 in range(1, mBarber):     #Create thread of barbers
        thread = barber.Barber(threadID1, "barber" + str(threadID1), wakeUpbarber, callClient, enter)
        thread.start()
        BarberThreads.append(thread)

    while gatattr(endS, "end") != "Y":  #If user input "Y" terminate creating client
        sleep(np.random.poisson(Clientp, 1))    #randomly create client
        thread = client.Client(threadID2, "client"+str(threadID2), wakeUpbarber, callClient, enter)
        thread.start()
        ClientQueue.put(thread)
        threadID2 += 1
    
    wakeUpbarber.acquire()
    wakeUpbarber.notifyAll()
    wakeUpbarber.release()
    ClientQueue.join()

main()
