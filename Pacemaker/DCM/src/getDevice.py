import sys
import glob
import serial


import serial.tools.list_ports

if __name__ == '__main__':

    all_comports = serial.tools.list_ports.comports()

    for comport in all_comports:
        print(comport.device, comport.name, comport.description, comport.interface)



def getDevice():

    pass