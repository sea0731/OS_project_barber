global mBarber
global nChair
global Clientp



class client( threading.Thread ) :
    def __init__( self, threadID, clientName, cond, enter ):
        threading.Thread.__init__( self )
        self.threadID = threadID
        self.clientName = clientName
        self.cond = cond 
        self.enter = enter '''main宣告兩個鎖cond , enter傳入'''


    def run( self ):
        self.enter.acquire()

        if Clientp < nChair :
            self.enter.release()
            '''enter shop'''
            Clientp+=1
            self.cond.acquire()
            barber.cond.notify()'''barber中的鎖先給個名字cond'''
            self.cond.wait()
            self.cond.release()
            print "release cond ".format( self.clientName )

        else :
            print "leave shop ".format( self.clientName )
            self.enter.release()
