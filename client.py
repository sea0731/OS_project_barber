import  threading
import  barber

global mBarber
global nChair
global Clientp

global onChair

class Client( threading.Thread ) :
    def __init__( self, threadID, clientName, cond, enter ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.clientName = clientName
        self.cond = cond 
        self.enter = enter #main宣告兩個鎖cond , enter傳入


    def run( self ):
        self.enter.acquire()

        if onChair < nChair :
            self.enter.release()

            #enter shop
            onChair += 1
            self.cond.acquire()
            barber.Barber.cond.notify(1) #barber中的鎖先給個名字cond
            self.cond.wait()
            self.cond.release()
            print("{0} release cond".format( self.clientName ))

        else :
            print("{0} leave shop".format( self.clientName ))
            self.enter.release()
