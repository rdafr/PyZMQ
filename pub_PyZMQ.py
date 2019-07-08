import zmq
import random
import sys
import time
import json

port = "8000"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    #topic = random.randrange(9999,10005)
    #topic = 10001
    #messagedata = random.randrange(1,215) - 80
    VRMS = random.randrange(100.00,135.00)
    #FP = random.uniform(0.75,1)
    IRMS = random.randrange(50.00,100.00)
    FP = random.randrange(75.00,100.00)
    FREQ = random.randrange(59.00,61.00)
    data = {"VRMS": VRMS,"IRMS": IRMS,"FP": FP,"FREQ":FREQ}
    socket.send(json.dumps(data))
    print ("Voltage: %d Current: %d Pwr. Factor: %d Freq: %d" % (VRMS, IRMS, FP, FREQ))
    #socket.send("%d %d %d %d %d" % (VRMS, IRMS, FP, FREQ))
    time.sleep(5)
