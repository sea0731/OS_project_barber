from threading import Thread
import threading
import time
import numpy as np
import Queue
import Tkinter as tk
import sys
from Tkinter import END


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

            print C.clientName, " out"

            self.enter.acquire()
            while ClientQueue.empty() != True:
                C = ClientQueue.get()
                self.enter.release()
                self.callC.acquire()
                self.callC.notify()
                self.callC.release()

                time.sleep(3)

                print C.clientName, " out"

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



def mainrun():             #main function of  barber-client problem
    global mBarber      #mBarber record "m" barber is working
    mBarber = input("input barber: ")
    mBarber = int(mBarber)
    global nChair       #nChair record "n" chair in waiting room
    nChair = input("input the number of chair: ")
    global Clientp      #Clientp record the frequent parameter of clients come
    Clientp = input("input client paramater: ")

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

        print ClientQueue.full()
        #print "zxrdtfcygvhbijnkmpl,: " , ClientQueue.qsize()

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

IMAGE_PATH = "images/"

class create(object):
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos
 
        self.tk_image = tk.PhotoImage(
            file="{}{}".format(IMAGE_PATH, image_name))
        self.image_obj= canvas.create_image(
            xpos, ypos, image=self.tk_image)

class mainwindow(tk.Frame):
    def __init__(self, master):
        self.master=master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)
        
        self.canvas=tk.Canvas(self, width=1000, height=700, bg='white', highlightthickness=0)
	self.store = create(self.canvas, "2.png", 500, 362)
        self.canvas.pack(fill="both", expand=True)
	
	for num in range(0,2):
	    global ClientQueue
	    ClientQueue=1
	    ClientQueue+=1
	    global BarberQueue
	    BarberQueue=1
	    BarberQueue+=1
            self.run()
	    #self.after(5000, self.run)
	
    def close(self):
        print("Application-shutdown")
        self.master.destroy()

    def run(self):
        global ClientQueue
	#ClientQueue=1
	global BarberQueue
	#BarberQueue=1
        
        while ClientQueue<=5:
            if ClientQueue == 1:
                self.image1 = create(self.canvas, "p1.png", 500, 590)
            elif ClientQueue == 2:
                self.image1 = create(self.canvas, "p1.png", 375, 590)
                self.image2 = create(self.canvas, "p1.png", 625, 590)
            elif ClientQueue == 3:
                self.image1 = create(self.canvas, "p1.png", 250, 590)
                self.image2 = create(self.canvas, "p1.png", 500, 590)
                self.image3 = create(self.canvas, "p1.png", 750, 590)
	    elif ClientQueue == 4:
                self.image1 = create(self.canvas, "p1.png", 125, 590)
                self.image2 = create(self.canvas, "p1.png", 375, 590)
                self.image3 = create(self.canvas, "p1.png", 625, 590)
                self.image4 = create(self.canvas, "p1.png", 875, 590)
	    elif ClientQueue == 5:
                self.image1 = create(self.canvas, "p1.png", 100, 590)
                self.image2 = create(self.canvas, "p1.png", 300, 590)
                self.image3 = create(self.canvas, "p1.png", 500, 590)
                self.image4 = create(self.canvas, "p1.png", 700, 590)
                self.image5 = create(self.canvas, "p1.png", 900, 590)
	    #if the shop is full
	    if ClientQueue == 5:
		global inn
		inn=0
		self.full()
	    ClientQueue += 1
	    
	    if BarberQueue == 1:
                self.b1 = create(self.canvas, "s.png", 500, 120)
	    elif BarberQueue == 2:
                self.b1 = create(self.canvas, "s.png", 375, 120)
                self.b2 = create(self.canvas, "s.png", 625, 120)
	    elif BarberQueue == 3:
                self.b1 = create(self.canvas, "s.png", 250, 120)
                self.b2 = create(self.canvas, "s.png", 500, 120)
                self.b3 = create(self.canvas, "s.png", 750, 120)
	    self.canvas.update_idletasks()
            self.after(3000, self.run)
	    
	    break
    def full(self):
	global ClientQueue
	global inn
	#inn=0
	if inn == 0:
	    self.fullpic = create(self.canvas, "full.png", 500, 415)
	    for x in range(50):
    	        x=500
	        y=415
    	        time.sleep(0.025)
    	        self.canvas.move(self.fullpic, x, -y)
    	        #canvas.move(rc2, x, y)
    	        self.canvas.update_idletasks()
	    self.after(1000, self.full)
	    inn=1
	else:
	    self.canvas.delete(self.fullpic)
	    inn=0
	    return

def main():
    win=tk.Tk()
    win.title("The Sleeping Barber Problem")
    m=mainwindow(win).pack(fill='both', expand=True)
        
    mainrun()

    win.mainloop()

if __name__ == "__main__":
    main()

