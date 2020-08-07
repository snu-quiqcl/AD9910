# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:04:01 2020

@author: JeonghyunPark
"""

from Arty_S7_v1_01 import *
from AD9910_eval import *

if __name__ == '__main__':
    fpga = ArtyS7('COM4')
    dds = AD9910(fpga)
    
    while(1):
        print('[1] set_frequency(self, freq, ch1, ch2, unit = \'MHz\')')
        print('[2] set_phase(self, phase, ch1, ch2, unit = \'FRAC\')')
        print('[3] set_amplitude(self, amplitude_frac, ch1, ch2)')
        print('set_profile(self, freq, phase, amplitude, ch1, ch2, profile = ' 
              '0, unit_freq = \'MHz\', unit_phase = \'FRAC\'')
        print('[8] exit')
        order = input('select funct you want to implement')
        
        if( order == 1 ):
            freq_in_MHz = input('freq_in_MHz : ')
            ch1 = input('ch1 : ')
            ch2 = input('ch2 : ')
            dds.set_frequency(freq_in_MHz, ch1, ch2)
            
        elif( order == 2 ):
            phase = input('freq_in_MHz : ')
            ch1 = input('ch1 : ')
            ch2 = input('ch2 : ')
            dds.set_phase(phase, ch1, ch2, unit = 'FRAC')
        
        elif( order == 3 ):
            amplitude_frac = input('freq_in_MHz : ')
            ch1 = input('ch1 : ')
            ch2 = input('ch2 : ')
            dds.set_amplitude(amplitude_frac, ch1, ch2)
            
        elif( order == 8 ):
            break
        
        else:
            print('error')

        
        