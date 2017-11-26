import  threading
import  barber

global mBarber
global nChair
global Clientp

global onChair

class Client( threading.Thread ) :
    def __init__( self, threadID, clientName, condbar, cond, enter ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.clientName = clientName
        self.cond = cond 
        self.condbar = condbar
        self.enter = enter #main宣告兩個鎖cond , enter傳入


    def run( self ):

        self.enter.acquire()

        if onChair < nChair :
            onChair += 1
            self.enter.release()

            #enter shop
            
            self.cond.acquire()
            self.condbar.acquire()
            self.condbar.notify() 
            self.condbar.release()
            self.cond.wait()
            self.cond.release()
            print("{0} release cond".format( self.clientName ))

        else :
            print("{0} leave shop".format( self.clientName ))
            self.enter.release()
