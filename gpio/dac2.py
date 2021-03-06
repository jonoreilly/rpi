import time
import math
import RPi.GPIO as GPIO
import threading

#set GPIO
GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#pins [0] is the highest resistance(lowest significance) bit. pinstatus states pin values
datapin = [21, 20, 16, 26, 19, 13]
pinstatus = []
for i in range(0, len(datapin)):
    pinstatus.append(0)
    GPIO.setup(datapin[i], GPIO.OUT)

freq = 440 #set Do to play



class player (threading.Thread):
    
    def __init__(self, threadID):  #ID == 1 -> write to pins, 0 -> buffer pin data
        self.ID = threadID
        global pinstatus
        self.laststatus = list(pinstatus)
        threading.Thread.__init__(self)
        
    def writearray(self):  #write data from pinstatus to GPIO
        global pinstatus
        global datapin
        for i in range(0, len(datapin)):
            if pinstatus[i] and not self.laststatus[i]:
                GPIO.output(datapin[i], GPIO.HIGH)
                self.laststatus[i] = int(pinstatus[i])
            elif self.laststatus[i] and not pinstatus[i]:
                GPIO.output(datapin[i], GPIO.LOW)
                self.laststatus[i] = int(pinstatus[i])

    def writenumber(self):  #calculate GPIO from a frequency
        global freq
        global pinstatus
        number = (math.sin((time.time()-self.start)*freq)+1)*(63/2)

        listholder = list(str(bin(int(number))))
        listholder.pop(0), listholder.pop(0)
        finalist = []
        for i in range(0, len(listholder)):
            finalist.append(listholder[len(listholder)-(i+1)])
        while len(pinstatus) > len(finalist):
            finalist.append(0)
        pinstatus = list(finalist)


        self.writearray()
    

    def run(self):
        global datapin
        if self.ID:
            while True:
                self.writearray()
        else:
            self.start = time.time()
            while True:
                self.writenumber()
            
        



#reproducer = player(1)
calculator = player(0)

#reproducer.start()
calculator.start()


while True:
    try:
        freq = int(input("440Hz is Do\n>>"))
    except KeyError:
        print("EMPTY")
