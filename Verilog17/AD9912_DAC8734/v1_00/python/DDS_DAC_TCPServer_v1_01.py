#!/usr/bin/python3
## -*- coding: utf-8 -*-

# This script is stored in O:\Device Manuals and Data\?
# Revision history
# 1.00: initial version
# 1.01: changed to power_table_v2_00 and added protocol to set Power min/max
# TO-DO list
# - Introduce authentication mechanmism. Under the current situation, some malicious person can send a damaging command to the controller
# - Convert to a service by making a daemon process

import sys
import os

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
#new_path_list.append(dirname + '\\..') # To import xxx
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)

calibration_dir = os.path.join(dirname, 'calibration')
import time
import threading
import socketserver
import datetime
import getopt

import socket
import struct

#from AD9912_DAC8734_v1_00_dummy import *
from AD9912_DAC8734_v1_00 import *
from power_table_v2_00 import power_table

DDS1_DAC_CH = 1
DDS2_DAC_CH = 0


#COM_port = 'COM25' # IonTrap-laptop1 (white - 32bit)
#COM_port = 'COM38' # IonTrap8-광학실험실 테이블위 dummy terminal
COM_port = '/dev/ttyUSB1'

defaultTCPPort = 9912+8734
IDN = 'TCP Server for Dual DDS with trigger output v1.00'


def printUsage(programName):
    print('Usage:')
    print('%s [options]\tStarts a TCP daemon to control DAC remotely ' \
          % programName)
    print('\nOptions:')
    print('-p <port> \tspecifies the TCP port. The default port is %d.' % \
          defaultTCPPort)
    print('-h, --help \tshows this message')
    

output_voltage = 0
def set_DAC_output(dac, volt): # This is DAC value (0~10V)
    global output_voltage 
    if volt < 0:
        print('DAC error: negative voltage (%f) is not allowed.' % volt)
        return
    if volt > 10:
        print('DAC error: voltage (%f) larger than 10V is not allowed.' % volt)
        return
        
    #dac.voltage_register_update(0, 0, volt) # Set ch0 of DAC0 to 1.0 (V)
    #dac.load_dac()
    output_voltage = volt


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global dds, dac, instLock, activeClientSocket, DDS1_pt, DDS2_pt
        clientSocket = self.request
        clientAddress = clientSocket.getpeername()
        print("%s: Connection request from %s" % \
              (datetime.datetime.now().isoformat(), clientAddress))
        
        #print('Active count:', threading.activeCount())
        #if (threading.activeCount() > 8):
        if (threading.activeCount() > 8):
            activeClientAddress = activeClientSocket.getpeername()
            clientSocket.sendall(bytes('A:%s:%d\n' % activeClientAddress, 'latin-1'))
            clientSocket.close()
            print("%s: Refused connection from %s due to active connection with %s" % \
                  (datetime.datetime.now().isoformat(), 
                   clientAddress, activeClientAddress))
            return
        else:
            activeClientSocket = clientSocket
            clientSocket.sendall(bytes('C:\n', 'latin-1'))
            print('\nConnection from (%s,%d) became active connection\n' % clientAddress)

        try:
            data = clientSocket.recv(1024).decode('latin-1')
            if len(data) == 0:
                print('\nActive connection is closed. Waiting for a new active connection...\n')
                return
            if data[-1] != '\n':
                print('"'+data+'"')
                error_msg = 'Error: the received data is not finished with \\n'
                clientSocket.sendall(bytes(error_msg, 'latin-1'))
                print(error_msg)
                clientSocket.close()
                print('\nActive connection is closed. Waiting for a new active connection...\n')
                return
            data = data[:-1]
                
            #print('Received:', data)
            while True:
                print('"'+data+'"')
                if data[0:5] == '*IDN?':
                    clientSocket.sendall(bytes(IDN+'\n', 'latin-1'))

                elif data[0:6] == 'Q:DDS1':
                    item_string = data[7:] # can be 'RFOUT', 'FREQ', 'POWER'
                    clientSocket.sendall(bytes(str(DDS1[item_string])+'\n', 'latin-1'))

                elif data[0:10] == 'DDS1:RFOUT':
                    instLock.acquire()
                    if (data[11:] == 'True'):
                        dac.set_ch123(DDS1_DAC_CH, DDS1_pt.voltage_for_freq_power(DDS1['FREQ'], DDS1['POWER']))
                        DDS1['RFOUT'] = True
                    else:
                        dac.set_ch123(DDS1_DAC_CH, 0)
                        DDS1['RFOUT'] = False
                    instLock.release()

                elif data[0:9] == 'DDS1:FREQ':
                    instLock.acquire()
                    freq_in_MHz = float(data[10:])
                    DDS1['FREQ'] = freq_in_MHz
                    dds.set_frequency(freq_in_MHz, 1, 0)
                    if DDS1['RFOUT']:
                        dac.set_ch123(DDS1_DAC_CH, DDS1_pt.voltage_for_freq_power(DDS1['FREQ'], DDS1['POWER']))
                    instLock.release()

                elif data[0:10] == 'DDS1:POWER':
                    instLock.acquire()
                    power_in_dBm = float(data[11:])
                    DDS1['POWER'] = power_in_dBm
                    if DDS1['RFOUT']:
                        dac.set_ch123(DDS1_DAC_CH, DDS1_pt.voltage_for_freq_power(DDS1['FREQ'], DDS1['POWER']))
                    instLock.release()

                elif data[0:6] == 'Q:DDS2':
                    item_string = data[7:] # can be 'RFOUT', 'FREQ', 'POWER', 'TRIG'
                    clientSocket.sendall(bytes(str(DDS2[item_string])+'\n', 'latin-1'))

                elif data[0:10] == 'DDS2:RFOUT':
                    instLock.acquire()
                    if (data[11:] == 'True'):
                        dac.set_ch123(DDS2_DAC_CH, DDS2_pt.voltage_for_freq_power(DDS2['FREQ'], DDS2['POWER']))
                        DDS2['RFOUT'] = True
                    else:
                        dac.set_ch123(DDS2_DAC_CH, 0)
                        DDS2['RFOUT'] = False
                    instLock.release()

                elif data[0:9] == 'DDS2:FREQ':
                    instLock.acquire()
                    freq_in_MHz = float(data[10:])
                    DDS2['FREQ'] = freq_in_MHz
                    dds.set_frequency(freq_in_MHz, 0, 1)
                    if DDS2['RFOUT']:
                        dac.set_ch123(DDS2_DAC_CH, DDS2_pt.voltage_for_freq_power(DDS2['FREQ'], DDS2['POWER']))
                    instLock.release()

                elif data[0:10] == 'DDS2:POWER':
                    instLock.acquire()
                    power_in_dBm = float(data[11:])
                    DDS2['POWER'] = power_in_dBm
                    if DDS2['RFOUT']:
                        dac.set_ch123(DDS2_DAC_CH, DDS2_pt.voltage_for_freq_power(DDS2['FREQ'], DDS2['POWER']))
                    instLock.release()

                elif data[0:9] == 'DDS2:TRIG':
                    instLock.acquire()
                    DDS2['TRIG'] = (data[10:] == 'True')
                    dds.ch2_trigger_output(DDS2['TRIG'])
                    instLock.release()

                elif data[0:8] == 'DDS:FREQ':
                    instLock.acquire()
                    freq_in_MHz = float(data[9:])
                    DDS1['FREQ'] = freq_in_MHz
                    DDS2['FREQ'] = freq_in_MHz
                    dds.set_frequency(freq_in_MHz, 1, 1)
                    if DDS1['RFOUT']:
                        dac.set_ch123(DDS1_DAC_CH, DDS1_pt.voltage_for_freq_power(DDS1['FREQ'], DDS1['POWER']))
                    if DDS2['RFOUT']:
                        dac.set_ch123(DDS2_DAC_CH, DDS2_pt.voltage_for_freq_power(DDS2['FREQ'], DDS2['POWER']))
                    instLock.release()

                else:
                    print('Unknown request:', data)
                
                data = clientSocket.recv(1024).decode('latin-1')
                if len(data) == 0:
                    print('\nActive connection is closed. Waiting for a new active connection...\n')
                    return
                if data[-1] != '\n':
                    print('"'+data+'"')
                    error_msg = 'Error: the received data is not finished with \\n'
                    clientSocket.sendall(bytes(error_msg, 'latin-1'))
                    print(error_msg)
                    clientSocket.close()
                    print('\nActive connection is closed. Waiting for a new active connection...\n')
                    return
                data = data[:-1]
                #print('Received:', data)
                
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
        except IOError as e:
            print("%s: I/O error(%d): %s from %s" % (datetime.datetime.now().isoformat(), \
                                 e.errno, e.strerror, clientAddress))
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
            
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("%s: Connection closed from %s" % \
                  (datetime.datetime.now().isoformat(), clientAddress))
            print('\nActive connection is closed. Waiting for a new active connection...\n')
            raise
        print('\nActive connection is closed. Waiting for a new active connection...\n')
        

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


"""
import fcntl 
# This module is unique to Unix. To use this script on Windows machine, I 
# should remove get_ip_address() function and change the print statement in main()
# On raspberry pi, ip just shows up as 0.0.0.0 meaning all ethernet adapter.
# https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode('utf-8'))
    )[20:24])
"""


if __name__ == "__main__":
    global dds, dac, instLock, activeClientSocket, DDS1_pt, DDS2_pt

    argv = sys.argv
    try:
        opts, args = getopt.getopt(argv[1:],"p:h",['help'])
    except getopt.GetoptError:
        printUsage(argv[0])
        sys.exit(2)
    #print repr(opts)
    TCPPort = defaultTCPPort
    
    activeClientSocket = None

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            printUsage(argv[0])
            sys.exit()
        elif opt == '-p':
            TCPPort = int(arg)

    if 'fpga' in vars(): # To close the previously opened device when re-running the script with "F5"
        fpga.close()
    fpga = FPGA(COM_port)
    fpga.print_idn()


    dac = DAC8734(fpga)
    dds = AD9912(fpga, 10, 100)


    DDS1={}
    DDS2={}

    dds.set_frequency(30.0, 1, 1)
    DDS1['FREQ'] = 30.0
    DDS2['FREQ'] = 30.0

    dds.set_current(0x3ff, 1, 1)
    dac.set_ch123(DDS1_DAC_CH, 0)
    DDS1['RFOUT'] = False
    DDS1['POWER'] = -60
    
    dac.set_ch123(DDS2_DAC_CH, 0)
    DDS2['RFOUT'] = False
    DDS2['POWER'] = -60
    
    dds.ch2_trigger_output(False)
    DDS2['TRIG'] = False
    
    DDS1_pt = power_table(os.path.join(calibration_dir, 'calibration_DDS1_DAC1_DDS_full_current_ZX73-2500-S+_180522.csv'))
    DDS2_pt = power_table(os.path.join(calibration_dir, 'calibration_DDS2_DAC0_HSTL_FB_connected_DDS_full_current_ZX73-2500-S+_180522.csv'))

    DDS1['MAX_POWER'] = DDS1_pt.common_max_power
    DDS1['MIN_POWER'] = DDS1_pt.common_min_power
    
    DDS2['MAX_POWER'] = DDS2_pt.common_max_power
    DDS2['MIN_POWER'] = DDS2_pt.common_min_power
    
    
    
    # Create a lock for multiple threads
    instLock = threading.Lock()
    
    # Port 0 means to select an arbitrary unused port
    #HOST, PORT = "localhost", 11232
    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = TCPPort

    ThreadedTCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    

    print("Host IP:", ip, "Port:", port, "Serial port:", COM_port)
    #print("Host IP:", get_ip_address('eth0'), "Port:", port, "Serial port:", COM_port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

    fpga.close()



