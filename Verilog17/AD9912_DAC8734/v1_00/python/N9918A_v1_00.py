# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:29:34 2018

@author: iontrap
"""

import socket
import time

class N9918A():
    def __init__(self, TCP_address):
        self.TCP_IP = TCP_address
        self.TCP_PORT = 5025
        self.BUFFER_SIZE = 1024
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.TCP_IP, self.TCP_PORT))
        self.s.settimeout(10) # unit in second?
        
    def close(self):
        self.s.close()
        
    def write(self, msg):
        self.s.send(bytes(msg+'\n', 'latin-1'))

    def read(self, length=100):
        return (self.s.recv(length)[:-1]).decode('latin-1')

    def query(self, msg, length=100):
        self.write(msg)
        return self.read(length)
    
    def peak(self, pause=2):
        time.sleep(pause)
        self.write('CALC:MARK1:FUNC:MAX')
        measured_freq=float(self.query('CALC:MARK1:X?'))
        measured_power_dBm = float(self.query('CALC:MARK1:Y?'))
        return (measured_freq, measured_power_dBm)


if __name__ == '__main__':
    if 'sa' in vars(): # To close the previously opened device when re-running the script with "F5"
        sa.close()
    sa = N9918A('10.1.1.138')
    sa.query('*IDN?')
    
    (freq, power_dBm) = sa.peak(0)
    print('Freq: %.0f MHz, %.2f dBm' % (freq/1e6, power_dBm))
