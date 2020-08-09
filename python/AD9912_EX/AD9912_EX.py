# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:03:46 2020

@author: JeonghyunPark
"""

from Arty_S7_v1_01 import *
from AD9912_DAC8734_v1_01 import *

TEST = 1

if __name__ == '__main__':
    if TEST:
        fpga = ArtyS7(None)
    else:
        fpga = ArtyS7('COM1')
    dds = AD9912(fpga)
    
    while(1):
        print('[1] set_frequency(self, freq_in_MHz, ch1, ch2)')
        print('[2] set_current(self, current, ch1, ch2)')
        print('[8] exit')
        order = input('select funct you want to implement')
        
        if( order == '1' ):
            freq_in_MHz = float(input('freq_in_MHz : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_frequency(freq_in_MHz, ch1, ch2)
            
        elif( order == '2' ):
            current = float(input('current : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_current(current, ch1, ch2)
            
        elif( order == '8' ):
            fpga.close()
            break
        
        else:
            print('error')

        
        