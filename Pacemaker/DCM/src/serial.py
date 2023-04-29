import serial
import serial.tools.list_ports
import struct

SerialPort = ''
NamePort = ''
for i in comports():
    if i.serial_number == '000000123456':
        SerialPort = i.serial_number #Tells me which device is being used 
        NamePort = i.device #Tells me if connected (return these values and output to front end)


# upperRate = request.form['upper_rate']
# lowerRate = request.form['low_rate']
# amplitude = request.form['amplitude']
# pulseWidth = request.form['pulse_width']
# sensitivity = request.form['sensitivity']
# hysteresis = request.form['hysteresis']
# smoothing = request.form['smoothing']
# ARP = request.form['RP']
# PVARP = request.form['PVARP']

def send():    
    PMode_byte = struct.pack('B', amplitude)
    URL_byte = struct.pack('B', upperRate)
    LRL_byte = struct.pack('B', lowerRate)
    amp_byte = struct.pack('f', amplitude)
    pulseW_byte = struct.pack('f', pulseWidth)
    sensitivity_byte = struct.pack('f', sensitivity)
    #hysteresis_byte = struct.pack('B', hysteresis)
    smoothing_byte = struct.pack('B', smoothing)
    ARP_byte = struct.pack('B', ARP)
    VRP_byte = struct.pack('B', VRP)

    #Send all int together all float together





def receive():
    #Receive voltages and plot against time
    #Receive
    voltage = struct.unpack('D', VRP) #VRP is the placeholder for the variable being received
    