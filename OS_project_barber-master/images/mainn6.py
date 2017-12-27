from threading import Thread
import threading
import time
import numpy as np
import Queue
import Tkinter as tk
import sys
from Tkinter import END

global enter
enter = threading.Condition()           #Wheather the client can enter the waiting room

global ClientQueue
ClientQueue = Queue.Queue()       #ClientQueue contain all clients in the store

global workingBarber
workingBarber = []

global onChair          #onChair is record how many clients in waitting room
onChair = 0

global mBarber
mBarber = 0

global nChair
nChair = 0

global BarberThreads

global whetherFull
whetherFull = 0
global whetherIn
whetherIn = 0

class end( threading.Thread ):              #end function try to get the input if user want to terminate the program or not
    def __init__(self, mainrun):
        self.mainrun = mainrun

    def run(self):
        global ClientQueue
        global BarberThreads

     
        while ClientQueue.empty() != true:
       	    ClientQueue.get().exit()
       	for barber in BarberThreads:
            barber.exit()
        mainrun.exit()
                

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

        while 1:
            self.callB.acquire()
            self.callB.wait()	//進入休息等待client喚醒
            self.callB.release()

            self.enter.acquire()	//鎖住enter不讓barber同時取用client資訊
            C = ClientQueue.get()	//取得client資訊
            workingBarber[self.threadID] = 1
            #print workingBarber[self.threadID - 1]
            self.enter.release()	//釋放enter

            self.callC.acquire()	//鎖住callC不讓複數barber同時喚醒client
            self.callC.notify()		//喚醒client
            self.callC.release()	//釋放callC

            time.sleep(10)		//工作時間

	    print "thread",self.threadID,workingBarber[ self.threadID]
            self.enter.acquire()
            workingBarber[self.threadID] = 0
            #print workingBarber[self.threadID - 1]
            self.enter.release()

            print C.clientName, " out"

            self.enter.acquire()	//鎖住enter不讓barber同時取用client資訊
            while ClientQueue.empty() != True:	//若有等待中的client則繼續工作
                C = ClientQueue.get()
                workingBarber[self.threadID] = 1
            	#print workingBarber[self.threadID - 1]
                self.enter.release()
                self.callC.acquire()
                self.callC.notify()
                self.callC.release()

                time.sleep(10)
		print "thread",self.threadID,workingBarber[ self.threadID]
                self.enter.acquire()
                workingBarber[self.threadID] = 0
            	#print workingBarber[self.threadID - 1]
                self.enter.release()

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

            #enter shop

        self.cond.acquire()	//鎖住cond不許同時去喚醒barber
        self.condbar.acquire()
        self.condbar.notify() 	//喚醒一個barber 
        self.condbar.release()
        self.cond.wait()	//進入等待barber喚醒
        self.cond.release()	//釋放cond



class mainObject( threading.Thread ):             #main function of  barber-client problem
    def __init__ ( self ):
        threading.Thread.__init__( self )
        global mBarber      #mBarber record "m" barber is working
        #mBarber = input("input barber: ")
	mBarber = int(mBarber)
        global workingBarber
        for i in range (0, mBarber):
            workingBarber.append(0)

        global nChair       #nChair record "n" chair in waiting room
        #nChair = input("input the number of chair: ")
        nChair = int(nChair)
	#print "inmain: ", nChair
        global Clientp      #Clientp record the frequent parameter of clients come
        #Clientp = input("input client paramater: ")

        global BarberThreads

    def run( self ):
        wakeUpbarber = threading.Condition()    #Wheather the client can wake up barbers  
        global enter

        callClient = threading.Condition()      #Wheather the barber can call next client
        q_Lock = threading.Condition()

        threadID1 = 1                           #threadID1 record the number of barbers
        threadID2 = 1                           #threadID2 record the number of clients
        BarberThreads = []                      #BarberThreads cantain all barbers who are working
        global ClientQueue
        ClientQueue = Queue.Queue(nChair)       #ClientQueue contain all clients in the store

        global whetherFull
	global whetherIn

        for threadID1 in range(0, mBarber):     #Create thread of barbers
            thread = Barber(threadID1, "barber" + str(threadID1), wakeUpbarber, callClient, enter, q_Lock)
            thread.start()
            BarberThreads.append(thread)

        while 1:  #If user input "Y" terminate creating client
            time.sleep(np.random.poisson(float(Clientp), 1))    #randomly create client

            thread = Client(threadID2, "client"+str(threadID2), wakeUpbarber, callClient, enter)
	    whetherIn = 1

            print "client in", threadID2
	    
	    time.sleep(2)

            q_Lock.acquire()

            print ClientQueue.full()
            #print "zxrdtfcygvhbijnkmpl,: " , ClientQueue.qsize()

            if ClientQueue.full() != True:
                ClientQueue.put(thread)
            else:
                print "============out", thread.clientName
                whetherFull = 1
                #print "full 1", whetherFull
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
        global mBarber
        global nChair
        global Clientp


	
        mBarber = self.e1.get()
	nChair = self.e2.get()
	Clientp = self.e3.get()

        self.top.destroy()

    	mainrun = mainObject()

   	mainrun.start()


class mainwindow(tk.Frame):
    def __init__(self, master):
        self.master=master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)

        self.canvas=tk.Canvas(self, width=1000, height=800, bg='white', highlightthickness=0)
        self.store = create(self.canvas, "2.png", 500, 362)
        self.canvas.pack(fill="both", expand=True)

        self.button1 = tk.Button(self.canvas, text = "Enter Value!", command = self.popup)
	self.button1.configure(width = 10, activebackground = "#33B5E5")
	self.button1_window = self.canvas.create_window(500, 600, window=self.button1)
	self.canvas.pack()

    def popup(self):
	popupWindow(self)
	self.button1.destroy()
	self.run()

    def close(self):
        print("Application-shutdown")
        self.master.destroy()

    def run(self):
        global ClientQueue
	# ClientQueue here has to be syncronized
        enter.acquire()
	
        global mBarber
	mBarber = int(mBarber)
        enter.release()

        global nChair
        nChair = int(nChair)

        global whetherFull
	global whetherIn
        global workingBarber
	# WorkingBarber here has to be syncronized
        enter.acquire()
        for i in range (0, mBarber):
            workingBarber.append(0)
        enter.release()

        while True:
            self.canvas.delete("all")
            self.store = create(self.canvas, "2.png", 500, 362)

	    if whetherIn == 1:
		whetherIn = 0
		self.peopleIn = create(self.canvas, "p1.png", 900, 300)
                time.sleep(1)
                self.canvas.delete(self.peopleIn)

            if nChair == 1:
                self.image1 = create(self.canvas, "c.png", 500, 590)
		if ClientQueue.qsize() == 1:
		    self.canvas.delete(self.image1)
                    self.image1 = create(self.canvas, "p1.png", 500, 500)
            elif nChair == 2:
                self.image1 = create(self.canvas, "c.png", 375, 590)
                self.image2 = create(self.canvas, "c.png", 625, 590)
		if ClientQueue.qsize() == 1:
		    self.canvas.delete(self.image1)
                    self.image1 = create(self.canvas, "p1.png", 375, 590)
            	elif ClientQueue.qsize() == 2:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
               	    self.image1 = create(self.canvas, "p1.png", 375, 590)
                    self.image2 = create(self.canvas, "p1.png", 625, 590)
            elif nChair == 3:
                self.image1 = create(self.canvas, "c.png", 250, 590)
                self.image2 = create(self.canvas, "c.png", 500, 590)
                self.image3 = create(self.canvas, "c.png", 750, 590)
		if ClientQueue.qsize() == 1:
		    self.canvas.delete(self.image1)
                    self.image1 = create(self.canvas, "p1.png", 250, 590)
            	elif ClientQueue.qsize() == 2:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
                    self.image1 = create(self.canvas, "p1.png", 250, 590)
                    self.image2 = create(self.canvas, "p1.png", 500, 590)
            	elif ClientQueue.qsize() == 3:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
                    self.image1 = create(self.canvas, "p1.png", 250, 590)
                    self.image2 = create(self.canvas, "p1.png", 500, 590)
                    self.image3 = create(self.canvas, "p1.png", 750, 590)
            elif nChair == 4:
                self.image1 = create(self.canvas, "c.png", 125, 590)
                self.image2 = create(self.canvas, "c.png", 375, 590)
                self.image3 = create(self.canvas, "c.png", 625, 590)
                self.image4 = create(self.canvas, "c.png", 875, 590)
		if ClientQueue.qsize() == 1:
		    self.canvas.delete(self.image1)
                    self.image1 = create(self.canvas, "p1.png", 125, 590)
            	elif ClientQueue.qsize() == 2:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
                    self.image1 = create(self.canvas, "p1.png", 125, 590)
                    self.image2 = create(self.canvas, "p1.png", 375, 590)
            	elif ClientQueue.qsize() == 3:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
                    self.image1 = create(self.canvas, "p1.png", 125, 590)
                    self.image2 = create(self.canvas, "p1.png", 375, 590)
                    self.image3 = create(self.canvas, "p1.png", 625, 590)
            	elif ClientQueue.qsize() == 4:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
		    self.canvas.delete(self.image4)
                    self.image1 = create(self.canvas, "p1.png", 125, 590)
                    self.image2 = create(self.canvas, "p1.png", 375, 590)
                    self.image3 = create(self.canvas, "p1.png", 625, 590)
                    self.image4 = create(self.canvas, "p1.png", 875, 590)
            elif nChair == 5:
                self.image1 = create(self.canvas, "c.png", 100, 590)
                self.image2 = create(self.canvas, "c.png", 300, 590)
                self.image3 = create(self.canvas, "c.png", 500, 590)
                self.image4 = create(self.canvas, "c.png", 700, 590)
                self.image5 = create(self.canvas, "c.png", 900, 590)
		if ClientQueue.qsize() == 1:
		    self.canvas.delete(self.image1)
                    self.image1 = create(self.canvas, "p1.png", 100, 590)
            	elif ClientQueue.qsize() == 2:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
                    self.image1 = create(self.canvas, "p1.png", 100, 590)
                    self.image2 = create(self.canvas, "p1.png", 300, 590)
            	elif ClientQueue.qsize() == 3:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
                    self.image1 = create(self.canvas, "p1.png", 100, 590)
                    self.image2 = create(self.canvas, "p1.png", 300, 590)
                    self.image3 = create(self.canvas, "p1.png", 500, 590)
            	elif ClientQueue.qsize() == 4:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
		    self.canvas.delete(self.image4)
                    self.image1 = create(self.canvas, "p1.png", 100, 590)
                    self.image2 = create(self.canvas, "p1.png", 300, 590)
                    self.image3 = create(self.canvas, "p1.png", 500, 590)
                    self.image4 = create(self.canvas, "p1.png", 700, 590)
            	elif ClientQueue.qsize() == 5:
              	    self.canvas.delete(self.image1)
		    self.canvas.delete(self.image2)
		    self.canvas.delete(self.image3)
		    self.canvas.delete(self.image4)
		    self.canvas.delete(self.image5)
                    self.image1 = create(self.canvas, "p1.png", 100, 590)
                    self.image2 = create(self.canvas, "p1.png", 300, 590)
                    self.image3 = create(self.canvas, "p1.png", 500, 590)
                    self.image4 = create(self.canvas, "p1.png", 700, 590)
                    self.image5 = create(self.canvas, "p1.png", 900, 590)

	    '''
            if ClientQueue.qsize() == 1:
                self.image1 = create(self.canvas, "p1.png", 500, 590)
            elif ClientQueue.qsize() == 2:
                self.image1 = create(self.canvas, "p1.png", 375, 590)
                self.image2 = create(self.canvas, "p1.png", 625, 590)
            elif ClientQueue.qsize() == 3:
                self.image1 = create(self.canvas, "p1.png", 250, 590)
                self.image2 = create(self.canvas, "p1.png", 500, 590)
                self.image3 = create(self.canvas, "p1.png", 750, 590)
            elif ClientQueue.qsize() == 4:
                self.image1 = create(self.canvas, "p1.png", 125, 590)
                self.image2 = create(self.canvas, "p1.png", 375, 590)
                self.image3 = create(self.canvas, "p1.png", 625, 590)
                self.image4 = create(self.canvas, "p1.png", 875, 590)
            elif ClientQueue.qsize() == 5:
                self.image1 = create(self.canvas, "p1.png", 100, 590)
                self.image2 = create(self.canvas, "p1.png", 300, 590)
                self.image3 = create(self.canvas, "p1.png", 500, 590)
                self.image4 = create(self.canvas, "p1.png", 700, 590)
                self.image5 = create(self.canvas, "p1.png", 900, 590)
	    '''
            #if the shop is full
            if whetherFull == 1:
                whetherFull = 0
                self.fullpic = create(self.canvas, "full.png", 500, 315)
                time.sleep(1)
                self.canvas.delete(self.fullpic)

	    if mBarber == 1:
                self.b1 = create(self.canvas, "s.png", 500, 120)
		for i in range (0, mBarber):
            	    if i==0 and workingBarber[i] == 1:
            	    	self.b11 = create(self.canvas, "light.png", 500, 240)
	    elif mBarber == 2:
                self.b1 = create(self.canvas, "s.png", 375, 120)
                self.b2 = create(self.canvas, "s.png", 625, 120)
		for i in range (0, mBarber):
            	    if i==0 and workingBarber[i] == 1:
            	        self.b11 = create(self.canvas, "light.png", 375, 240)
            	    if i==1 and workingBarber[i] == 1:
            	        self.b21 = create(self.canvas, "light.png", 625, 240)
	    elif mBarber == 3:
                self.b1 = create(self.canvas, "s.png", 250, 120)
                self.b2 = create(self.canvas, "s.png", 500, 120)
                self.b3 = create(self.canvas, "s.png", 750, 120)
		for i in range (0, mBarber):
            	    if i==0 and workingBarber[i] == 1:
            	        self.b11 = create(self.canvas, "light.png", 250, 240)
            	    if i==1 and workingBarber[i] == 1:
            	        self.b21 = create(self.canvas, "light.png", 500, 240)
            	    if i==2 and workingBarber[i] == 1:
                        self.b31 = create(self.canvas, "light.png", 750, 240)
	    '''
	    for i in range (0, mBarber):
            	if i==0 and workingBarber[i] == 1:
            	    self.b1 = create(self.canvas, "light.png", 250, 240)
            	if i==1 and workingBarber[i] == 1:
            	    self.b1 = create(self.canvas, "light.png", 250, 240)
            	if i==2 and workingBarber[i] == 1:
                    self.b2 = create(self.canvas, "light.png", 500, 240)
            	if i==3 and workingBarber[i] == 1:
                    self.b3 = create(self.canvas, "light.png", 750, 240)
            '''
            self.canvas.update_idletasks()
            self.after(100, self.run)

            break

def main():
    win=tk.Tk()
    win.title("The Sleeping Barber Problem")
    m=mainwindow(win).pack(fill='both', expand=True)

    win.mainloop()


if __name__ == "__main__":
    main()

