from threading import Thread
import threading
import time
import numpy as np
import Queue
import Tkinter as tk
import sys

global mBarber
mBarber=0
global nChair
nChair=0
global Clientp
Clientp=0

class popupWindow(object):
    def __init__(self,master):
	global mBarber
        global nChair
        global Clientp
        
	top=self.top=tk.Toplevel(master)
        self.l1=tk.Label(top, text="Input the number of Barber: ")
        self.l1.grid(row=0)
        self.e1=tk.Entry(top)
        self.e1.grid(row=0, column=1)
        self.l2=tk.Label(top, text="Input the number of Chair: ")
        self.l2.grid(row=1)
        self.e2=tk.Entry(top)
        self.e2.grid(row=1, column=1)
        self.l3=tk.Label(top, text="Input Client Parameter: ")
        self.l3.grid(row=2)
        self.e3=tk.Entry(top)
        self.e3.grid(row=2, column=1)
        self.b=tk.Button(top,text='Ok',command=self.cleanup)
        self.b.grid(row=3, column=0, pady=4)
    def cleanup(self):
        #self.value=self.e1.get()
	mBarber = self.e1.get()
	
	nChair = self.e2.get()
	Clientp = self.e3.get()
	print mBarber
        print nChair
        print Clientp
        self.top.destroy()

class mainWindow(object):
    def __init__(self,master):
	
	self.master=master
        self.b=tk.Button(master,text="Enter Value!",command=self.popup)
        self.b.pack()
        #self.b2=tk.Button(master,text="Start",command=lambda: sys.stdout.write(self.entryValue()+'\n'))
	#self.b2=tk.Button(master, text="Start", command=main())
	self.b2=tk.Button(master, text="Start", command=quit)
        self.b2.pack()
    def popup(self):
        self.w=popupWindow(self.master)
        self.b["state"] = "disabled" 
        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"
    def entryValue(self):
        return self.w.value

#tk.Button(win, text='Begin', command=begin).pack()

#win.mainloop()

global onChair          #onChair is record how many clients in waitting room
onChair = 0

class endStore():         #endStore contain value wheather we end the program
    def __init__(self):
        self.end = "N"

global endS
endS = endStore()

class end( threading.Thread ):              #end function try to get the input if user want to terminate the program or not
    def run(self):
        global endS

        while endS.end != "Y":
            endS.end = input("Do you want to close the store?(Y or N)")

            if endS.end != "Y" or end != "N" :
                print("please type Y or N")

class Barber( threading.Thread ):
    def __init__(self, threadID, barberName, callB, callC, enter, q_Lock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.barberName = barberName
        self.callB = callB
        self.callC = callC
        self.enter = enter

    def run( self ):
        global mBarber
        global nChair
        global Clientp

        global ClientQueue

        global endS

        while getattr(endS, "end") != "Y":
            self.callB.acquire()
            self.callB.wait()
            self.callB.release()

            if getattr(endS, "end") == "Y":
                break

            self.enter.acquire()
            C = ClientQueue.get()
            self.enter.release()

            self.callC.acquire()
            self.callC.notify()
            self.callC.release()

            time.sleep(3)

            print (C.clientName, " out")

            self.enter.acquire()
            while ClientQueue.empty() != True:
                C = ClientQueue.get()
                self.enter.release()
                self.callC.acquire()
                self.callC.notify()
                self.callC.release()

                time.sleep(3)

                print (C.clientName, " out")

                self.enter.acquire()

            self.enter.release()

class Client( threading.Thread ) :
    def __init__( self, threadID, clientName, condbar, cond, enter ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.clientName = clientName
        self.cond = cond 
        self.condbar = condbar
        self.enter = enter


    def run( self ):
        global mBarber
        global nChair
        global Clientp

        global ClientQueue
        global endS


            #enter shop

        self.cond.acquire()
        self.condbar.acquire()
        self.condbar.notify() 
        self.condbar.release()
        self.cond.wait()
        self.cond.release()



def main():             #main function of  barber-client problem
    global mBarber      #mBarber record "m" barber is working
    #mBarber = input("input barber: ")
    #mBarber = int(mBarber)
    global nChair       #nChair record "n" chair in waiting room
    #nChair = input("input the number of chair: ")
    global Clientp      #Clientp record the frequent parameter of clients come
    #Clientp = input("input client paramater: ")
        

    wakeUpbarber = threading.Condition()    #Wheather the client can wake up barbers  
    enter = threading.Condition()           #Wheather the client can enter the waiting room

    callClient = threading.Condition()      #Wheather the barber can call next client
    q_Lock = threading.Condition()

    threadID1 = 1                           #threadID1 record the number of barbers
    threadID2 = 1                           #threadID2 record the number of clients
    BarberThreads = []                      #BarberThreads cantain all barbers who are working
    global ClientQueue
    ClientQueue = Queue.Queue(nChair)       #ClientQueue contain all clients in the store

    endprogram = end()
    endprogram.start()

    for threadID1 in range(1, mBarber):     #Create thread of barbers
        thread = Barber(threadID1, "barber" + str(threadID1), wakeUpbarber, callClient, enter, q_Lock)
        thread.start()
        BarberThreads.append(thread)

    while getattr(endS, "end") != "Y":  #If user input "Y" terminate creating client
        time.sleep(np.random.poisson(float(Clientp), 1))    #randomly create client

        thread = Client(threadID2, "client"+str(threadID2), wakeUpbarber, callClient, enter)

        print "client in", threadID2

        q_Lock.acquire()
        if ClientQueue.full() != True:
            ClientQueue.put(thread)
        else:
            print "============out", thread.clientName
        q_Lock.release()

        thread.start()

        threadID2 += 1

    wakeUpbarber.acquire()
    wakeUpbarber.notifyAll()
    wakeUpbarber.release()
    ClientQueue.join()

if __name__ == "__main__":
    win=tk.Tk()
    win.title("The Sleeping Barber Problem")
    C = tk.Canvas(win, bg="white", height=500, width=500)
    background_image = tk.PhotoImage(file="2.png")
    background_label = tk.Label(win, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    tk.Label(win, text="Welcome to the Barber Shop!", pady=20)
    C.pack()
    m=mainWindow(win)   
 
    #main()
    win.mainloop()
