import threading
from main import endStore

global endS

global mBarber
global nChair
global Clientp

global onChair

class Barber( threading.Thread ):
    def __init__(self, threadID, barberName, callB, callC, enter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.barberName = barberName
        self.callB = callB
        self.callC = callC
        self.enter = enter

    def run( self ):
        while gatattr(endS, "end") != "Y":
            self.callB.acquire()
            self.callB.wait()
            self.callB.release()
            
            if gatattr(endS, "end") == "Y":
                break

            self.callC.acquire()
            self.callC.notify()
            self.callC.release()

            sleep(3)

            ClientQueue.push()

            self.enter.acquire() 
            while onchair != 0:
                self.enter.release()
                self.callC.acquire()
                self.callC.notify()
                self.callC.release()

                sleep(3)
                
                self.enter.acquire()

            self.enter.release()
