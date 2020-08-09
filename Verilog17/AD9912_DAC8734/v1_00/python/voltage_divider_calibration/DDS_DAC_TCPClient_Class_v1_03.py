# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 00:10:48 2018

@author: 1109282

* Change log
v1_00: Initial working version with DDS1 olny
v1_01: Working with DDS1 & DDS2
v1_02: Adding oscilloscope
v1_03: Power limit

"""
# from http://wiki.python.org/moin/TcpCommunication
# About SCPI over TCP: page 12 from ftp://ftp.datx.com/Public/DataAcq/MeasurementInstruments/Manuals/SCPI_Measurement.pdf

from __future__ import unicode_literals
import os, sys
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
new_path_list.append(dirname + '\\..') # For ImportForSpyderAndQt5
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)




import math
import socket

class DDS_DAC():
    
    def __init__(self):
        
        self.connected = False
        

    def query(self, message):
        """ Send the message and read the reply.
        
        Args:
            query (unicode string): query
        
        Returns:
            unicode string: reply string
        """
        self.socket.send((message+'\n').encode('latin-1'))
        data = self.socket.recv(1024)
        data_decoded = data.decode('latin-1')
        if data_decoded[-1] != '\n':
            print(data_decoded)
            raise ValueError('Error in query: the returned message is not finished with \"\\n\"')
            
        return data_decoded[:-1] # Removing the trailing '\n'

    
    def write(self, message):
        """ Send the command.
        
        Args:
            message (unicode string): message to send
        
        Returns:
            None
        """
        self.socket.send((message + '\n').encode('latin-1'))


    def read(self):
        """ Reads data from the device.
        
        Args:
            None
        
        Returns:
            unicode string: received string
        """
        data = self.socket.recv(1024)
        data_decoded = data.decode('latin-1')
        if data_decoded[-1] != '\n':
            raise ValueError('Error in read: the returned message is not finished with \\n')
            
        return data_decoded[:-1] # Removing the trailing '\n'
        

    def disconnect(self):
        if self.connected:
            self.socket.close() 
        self.connected = False

    def connect(self):
        if self.connected:
            print('It is already connected.')
            return

        self.TCP_IP = '10.1.1.119' #'iontrap-RPI-2.sktsdc.com'
        self.TCP_PORT = 18646
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.TCP_IP, self.TCP_PORT))
        self.socket.settimeout(1) # unit in second?
        
        connection_status = self.read()
        if connection_status[:2] == 'A:':
            print('Connection to Dual DDS server failed', \
                ('There is another active connection. Please disconnect another connection from %s first.' % str(connection_status[2:])))
            return
        elif connection_status[:2] == 'C:':
            #print('This connection became active')
            pass

        print(self.query('*IDN?')) # 'TCP Server for Dual DDS with trigger output v1.00'
        self.connected = True
            
            

    
    def DDS1_apply_freq(self, freq_in_MHz):
        self.write('DDS1:FREQ %f' % freq_in_MHz)

    def DDS1_apply_power(self, dBm):
        self.write('DDS1:POWER %.2f' % dBm)

    def DDS1_output_on_off(self, status):
        if status:
            self.write('DDS1:RFOUT True')
        else:
            self.write('DDS1:RFOUT False')



    def DDS1_set_power_mW(self, mW):
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        
        self.DDS1_apply_power(dBm)
        
        



            
    

        
if __name__ == "__main__":
    if 'dds_dac' in globals():
        dds_dac.disconnect()
        
    dds_dac = DDS_DAC()
    #sys.exit(app.exec_())

