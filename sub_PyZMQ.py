import sys
import zmq
import math
import json

port = "8000"
context = zmq.Context()
socket = context.socket(zmq.SUB)
print ("Coletando os dados de consumo: ")
socket.connect ("tcp://localhost:%s" % port)

#topicfilter = "10001"
#socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
socket.setsockopt(zmq.SUBSCRIBE, '')
cont = 0
#tempo = time.time() ou int(time.time())
while (True):
    cont=0
    MED_VRMS=0
    MED_IRMS=0
    MED_FP=0
    MED_FREQ=0
    while (cont < 12):
        string = socket.recv()
        #VRMS, IRMS, FP, FREQ = string.split()
        medidas = json.loads(string)
        
        """VRMS = int(VRMS)
        IRMS = int(IRMS)
        FP = int(FP)
        FREQ = int(FREQ)"""
        
        VRMS = (medidas["VRMS"])
        IRMS = (medidas["IRMS"])
        FP = (medidas["FP"])
        FREQ = (medidas["FREQ"])

        print ("Tensao: %d Corrente: %d Fator de Pot.: %d Freq: %d" % (VRMS, IRMS,FP,FREQ))                   
        VA = VRMS*IRMS
        W = VA*FP/100
        VAR = math.sqrt(((VA)**2)-((W)**2))
        print ("Pot. Ativa: %d Pot. Reativa: %d Pot. Total: %d\n" % (W, VAR, VA))

        if (VRMS < 110):
            print ("Houve um evento de subtensao: %d \n" % (VRMS))
        elif (VRMS > 130):
            print ("Houve um evento de sobretensao: %d\n" % (VRMS))

        MED_VRMS = MED_VRMS + VRMS
        MED_IRMS = MED_IRMS + IRMS
        MED_FP = MED_FP + FP
        MED_FREQ = MED_FREQ + FREQ
        
        cont = cont + 1

    MED_VRMS = MED_VRMS/12
    MED_IRMS = MED_IRMS/12
    MED_FP = MED_FP/12
    MED_FREQ = MED_FREQ/12
    
    data={"tipo":"parametros","dados":{"VRMS":MED_VRMS,"IRMS":MED_IRMS,"FP":MED_FP,"FREQ":MED_FREQ}}
    
    with open('dados_periodicos.json','w') as outfile:
        json.dump(data, outfile)
      
