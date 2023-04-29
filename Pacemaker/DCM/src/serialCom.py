import serial
import serial.tools.list_ports
import struct
from time import sleep
import json



class SerialCom:

    def __init__(self):
        self.filename='src/data_base.json'
        self.SerialPort = ''
        self.NamePort = ''

        f = open(self.filename)
        self.data = json.load(f)
        f.close()

    

    def updateParams(self,mode,username):


        if mode == 'AOO':
            self.pacingMode = 1
            self.upperRate = self.data[username]["pacemakerSettings"][mode]['upperRate']
            self.lowerRate = self.data[username]["pacemakerSettings"][mode]['lowerRate']
            self.ApulseWidth = self.data[username]["pacemakerSettings"][mode]['atrialPulseWidth']
            self.amplitude = self.data[username]["pacemakerSettings"][mode]['atrialAmplitude']
            self.smoothing = 0
            self.ARP = 0
            self.VRP = 0
            self.sensitivity = 0
            self.reactionTime = 0
            self.recoveryTime = 0
            self.responseFactor = 0
            self.MSR = 0
            self.VpulseWidth = 0

            

        elif mode == 'VOO':
            self.pacingMode = 2
            self.upperRate = self.data[username]["pacemakerSettings"][mode]['upperRate']
            self.lowerRate = self.data[username]["pacemakerSettings"][mode]['lowerRate']
            self.VpulseWidth = self.data[username]["pacemakerSettings"][mode]['ventricularPulseWidth']
            self.amplitude = self.data[username]["pacemakerSettings"][mode]['ventricularAmplitude']
            self.smoothing = 0
            self.ARP = 0
            self.VRP = 0
            self.sensitivity = 0
            self.reactionTime = 0
            self.recoveryTime = 0
            self.responseFactor = 0
            self.MSR = 0
            self.ApulseWidth = 0
            print("got VOO values")

        elif mode == 'AAI':
            self.pacingMode = 3
            self.upperRate = self.data[username]["pacemakerSettings"][mode]['upperRate']
            self.lowerRate = self.data[username]["pacemakerSettings"][mode]['lowerRate']
            self.ApulseWidth = self.data[username]["pacemakerSettings"][mode]['atrialPulseWidth']
            self.amplitude = self.data[username]["pacemakerSettings"][mode]['atrialAmplitude']
            self.ARP = self.data[username]["pacemakerSettings"][mode]['RP']
            self.sensitivity = self.data[username]["pacemakerSettings"][mode]['atrialSensitivity']
            self.smoothing = self.data[username]["pacemakerSettings"][mode]['rateSmoothing']
            VpulseWidth = 0 #this mode's gonna break
            VRP = 0
            self.reactionTime = 0
            self.recoveryTime = 0
            self.responseFactor = 0
            self.MSR = 0

        elif mode == 'VVI':
            self.pacingMode = 4
            self.upperRate = self.data[username]["pacemakerSettings"][mode]['upperRate']
            self.lowerRate = self.data[username]["pacemakerSettings"][mode]['lowerRate']
            self.VpulseWidth = self.data[username]["pacemakerSettings"][mode]['ventricularPulseWidth']
            self.amplitude = self.data[username]["pacemakerSettings"][mode]['ventricularAmplitude']
            self.VRP = self.data[username]["pacemakerSettings"][mode]['RP']
            self.sensitivity = self.data[username]["pacemakerSettings"][mode]['ventricularSensitivity']
            self.smoothing = self.data[username]["pacemakerSettings"][mode]['rateSmoothing']
            self.ApulseWidth = 0
            self.ARP = 0
            self.reactionTime = 0
            self.recoveryTime = 0
            self.responseFactor = 0
            self.MSR = 0

    def openCOM(self):
        for p in serial.tools.list_ports.comports():
            if p.serial_number == '000000123456':
                self.SerialPort = p.serial_number #Tells me which device is being used 
                self.CompPort = p.device #Tells me if connected (return these values and output to front end)
                self.SerialPort = self.SerialPort

                return (self.SerialPort,self.CompPort)
        raise Exception("Connection failed")

    def send(self):     #Send all int together all float together
            #Pack all integers together

        PMode_byte = struct.pack('B', int(self.pacingMode))
        URL_byte = struct.pack('B', int(self.upperRate))
        LRL_byte = struct.pack('B', int(self.lowerRate))
        ARP_word = struct.pack('H', int(self.ARP))
        VRP_word = struct.pack('H', int(self.VRP))
        #hysteresis_byte = struct.pack('B', hysteresis)
        #Packing all floats together
        amp_byte = struct.pack('f', self.amplitude)
        #
        VpulseW_byte = struct.pack('B',  self.VpulseWidth)
        ApulseW_byte = struct.pack('B', self.ApulseWidth)

        S_set = b'\x16' + b'\x55' + PMode_byte + URL_byte + LRL_byte  + ARP_word + VRP_word + amp_byte + VpulseW_byte + ApulseW_byte 
        S_echo = b'\x16' + b'\x22' + PMode_byte + URL_byte + LRL_byte  + ARP_word + VRP_word + amp_byte + VpulseW_byte + ApulseW_byte 

    


        with serial.Serial(self.CompPort, 115200) as pacemaker:
            pacemaker.write(S_set)
        
        #It seems like sending and receiving occur after one another
        #Check if i need to add heartbeat to S_echo
        # =>
        #Receive voltages and plot against time
        sleep(1)
        with serial.Serial(self.CompPort, 115200) as pacemaker:
            print("Recieving information")
            pacemaker.write(S_echo)
            print("Echoing")

            data = pacemaker.read(13) #read(number of by sending/receiving).
            print("Read done")

            #testSen=struct.unpack('B', data) 
            #ModeRec = struct.unpack('B', data) 


    
            MODE_ECHO = data[0]   #0th output 
            URL_ECHO = data[1]   #1st output
            LRL_ECHO = data[2]   # 2nd output
            ARP_ECHO = struct.unpack('H', data[3:5])[0]
            VRP_ECHO = struct.unpack('H', data[5:7])[0]
            amp_ECHO = struct.unpack('f', data[7:11])[0]

            VpulseW_ECHO = data[11]  
            ApulseW_ECHO = data[12]


            print("MODE:", MODE_ECHO)
            print("URL_byte", URL_ECHO)
            print("LRL_byte",LRL_ECHO)
            print("ARP_byte", ARP_ECHO)
            print("VRP_byte", VRP_ECHO)
            print("amp_byte", amp_ECHO)
            print("VpulseW_byte", VpulseW_ECHO)
            print("ApulseW_byte", ApulseW_ECHO)


"""
serialcom = SerialCom()
serialcom.openCOM()
serialcom.updateParams("AOO","h")
serialcom.send()    """

##################################################










































































"""


filename='data_base.json'
SerialPort = ''
NamePort = ''

  
# Opening JSON file
f = open(filename)
  
# returns JSON object as 
# a dictionary

data = json.load(f)
  
# Iterating through the json
# list
#print(data)
  
# Closing file
f.close()

username="h"


mode = data[username]["pacemakerSettings"]["currentMode"]

print(mode)

if mode == 'AOO':
    pacingMode = 1
    upperRate = data[username]["pacemakerSettings"][mode]['upperRate']
    lowerRate = data[username]["pacemakerSettings"][mode]['lowerRate']
    ApulseWidth = data[username]["pacemakerSettings"][mode]['atrialPulseWidth']
    amplitude = data[username]["pacemakerSettings"][mode]['atrialAmplitude']
    smoothing = 0
    ARP = 0
    VRP = 0
    sensitivity = 0
    reactionTime = 0
    recoveryTime = 0
    responseFactor = 0
    MSR = 0
    VpulseWidth = 0

elif mode == 'VOO':
    pacingMode = 2
    upperRate = data[username]["pacemakerSettings"][mode]['upperRate']
    lowerRate = data[username]["pacemakerSettings"][mode]['lowerRate']
    VpulseWidth = data[username]["pacemakerSettings"][mode]['ventricularPulseWidth']
    amplitude = data[username]["pacemakerSettings"][mode]['ventricularAmplitude']
    smoothing = 0
    ARP = 0
    VRP = 0
    sensitivity = 0
    reactionTime = 0
    recoveryTime = 0
    responseFactor = 0
    MSR = 0
    ApulseWidth = 0

elif mode == 'AAI':
    pacingMode = 3
    upperRate = data[username]["pacemakerSettings"][mode]['upperRate']
    lowerRate = data[username]["pacemakerSettings"][mode]['lowerRate']
    ApulseWidth = data[username]["pacemakerSettings"][mode]['atrialPulseWidth']
    amplitude = data[username]["pacemakerSettings"][mode]['atrialAmplitude']
    ARP = data[username]["pacemakerSettings"][mode]['RP']
    sensitivity = data[username]["pacemakerSettings"][mode]['atrialSensitivity']
    smoothing = data[username]["pacemakerSettings"][mode]['rateSmoothing']
    VpulseWidth = 0
    VRP = 0
    reactionTime = 0
    recoveryTime = 0
    responseFactor = 0
    MSR = 0

elif mode == 'VVI':
    pacingMode = 4
    upperRate = data[username]["pacemakerSettings"][mode]['upperRate']
    lowerRate = data[username]["pacemakerSettings"][mode]['lowerRate']
    VpulseWidth = data[username]["pacemakerSettings"][mode]['ventricularPulseWidth']
    amplitude = data[username]["pacemakerSettings"][mode]['ventricularAmplitude']
    VRP = data[username]["pacemakerSettings"][mode]['RP']
    sensitivity = data[username]["pacemakerSettings"][mode]['ventricularSensitivity']
    smoothing = data[username]["pacemakerSettings"][mode]['rateSmoothing']
    ApulseWidth = 0
    ARP = 0
    reactionTime = 0
    recoveryTime = 0
    responseFactor = 0
    MSR = 0



SerialPort = ''
NamePort = ''

for p in serial.tools.list_ports.comports():
    if p.serial_number == '000000123456':
        SerialPort = p.serial_number #Tells me which device is being used 
        NamePort = p.device #Tells me if connected (return these values and output to front end)
CompPort = 'COM4'


def send():     #Send all int together all float together
    #Pack all integers together

    PMode_byte = struct.pack('B', 1)
    URL_byte = struct.pack('B', 2)
    LRL_byte = struct.pack('B', 3)
    ARP_word = struct.pack('H', 260)
    VRP_word = struct.pack('H', 6)
    #hysteresis_byte = struct.pack('B', hysteresis)
    #Packing all floats together
    amp_byte = struct.pack('f', 7.5)
    #
    VpulseW_byte = struct.pack('B', 8)
    ApulseW_byte = struct.pack('B', 9)




    #sensitivity_byte = struct.pack('f', sensitivity)
    #ReacTime_byte = struct.pack('f', reactionTime)
    #RecTime_byte = struct.pack('f', recoveryTime)
    #RespFactor_byte = struct.pack('f', responseFactor)
    #MSR_byte = struct.pack('f', MSR)


#    S_set = b'\x16' + b'\x55' + PMode_byte + URL_byte + LRL_byte + smoothing_byte + ARP_byte + VRP_byte + amp_byte + VpulseW_byte + ApulseW_byte + sensitivity_byte + ReacTime_byte + RecTime_byte + RespFactor_byte + MSR_byte
#    S_echo = b'\x16' + b'\x22' + PMode_byte + URL_byte + LRL_byte + smoothing_byte + ARP_byte + VRP_byte + amp_byte + VpulseW_byte + ApulseW_byte + sensitivity_byte + ReacTime_byte + RecTime_byte + RespFactor_byte + MSR_byte

    S_set = b'\x16' + b'\x55' + PMode_byte + URL_byte + LRL_byte  + ARP_word + VRP_word + amp_byte + VpulseW_byte + ApulseW_byte 
    S_echo = b'\x16' + b'\x22' + PMode_byte + URL_byte + LRL_byte  + ARP_word + VRP_word + amp_byte + VpulseW_byte + ApulseW_byte 

  


    with serial.Serial(CompPort, 115200) as pacemaker:
        pacemaker.write(S_set)
    
    #It seems like sending and receiving occur after one another
    #Check if i need to add heartbeat to S_echo
    # =>
    #Receive voltages and plot against time
    sleep(1)
    with serial.Serial(CompPort, 115200) as pacemaker:
        print("Recieving information")
        pacemaker.write(S_echo)
        print("Echoing")

        data = pacemaker.read(13) #read(number of by sending/receiving).
        print("Read done")

        #testSen=struct.unpack('B', data) 
        #ModeRec = struct.unpack('B', data) 


 
        MODE_ECHO = data[0]   #0th output 
        URL_ECHO = data[1]   #1st output
        LRL_ECHO = data[2]   # 2nd output
        ARP_ECHO = struct.unpack('H', data[3:5])[0]
        VRP_ECHO = struct.unpack('H', data[5:7])[0]
       # ARP_ECHO = data[4]  #4th and 5th
        #VRP_ECHO = data[5]  #6th and 7th
        amp_ECHO = struct.unpack('f', data[7:11])[0]

        VpulseW_ECHO = data[11]  
        ApulseW_ECHO = data[12]

        #sensitivity_ECHO = data[9]
        #reacTime_ECHO = data[10]
        #RespFactor_ECHO = data[11]
        #MSR_ECHO = data[12]



        print("MODE:", MODE_ECHO)
        print("URL_byte", URL_ECHO)
        print("LRL_byte",LRL_ECHO)
        print("ARP_byte", ARP_ECHO)
        print("VRP_byte", VRP_ECHO)
        print("amp_byte", amp_ECHO)
        print("VpulseW_byte", VpulseW_ECHO)
        print("ApulseW_byte", ApulseW_ECHO)

        #print("ReacTime_byte", reacTime_ECHO)
        #print("sensitivity_byte", sensitivity_ECHO)
        #print("RespFactor_byte", RespFactor_ECHO)
        #print("MSR_byte", MSR_ECHO)

        
        #print("data:" , URLRec)
        # LRLRec = struct.unpack('B', data[2])
        # smoothingRec = struct.unpack('B', data[3])
        # ARPRec = struct.unpack('B', data[4])
        # VRPRec = struct.unpack('B', data[5])
        # ampRec = struct.unpack('f', data[6])
        # VpulseRec = struct.unpack('f', data[7])
        # ApulseRec = struct.unpack('f', data[8])
        # sensitivityRec = struct.unpack('f', data[9])
        # ReacTimeRec = struct.unpack('f', data[10])
        # RecTimeRec = struct.unpack('f', data[11])
        # RespFactorRec = struct.unpack('f', data[12])
        # MSRRec = struct.unpack('f', data[13])
        # HeartRate = struct.unpack('f', data[14])
        #store all values and double check w stored values (REQUIREMENT IN ASSIGNMENT)
        #and on top of that you need to receive HeartRate and that is the y-value to ECG
    print("Send complete")

#ser = serial.Serial()
# ser.write writes to the port
# ser.read reads it g  


send()"""