# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 14:04:01 2020

@author: JeonghyunPark
"""

from Arty_S7_v1_01 import *
from AD9910_eval import *

if __name__ == '__main__':
    fpga = ArtyS7('COM12')
    dds = AD9910(fpga)
    
    while(1):
        print('[1] set_frequency(self, freq, ch1, ch2, unit = \'MHz\')')
        print('[2] set_phase(self, phase, ch1, ch2, unit = \'FRAC\')')
        print('[3] set_amplitude(self, amplitude_frac, ch1, ch2)')
        print('[4] set_profile(self, freq, phase, amplitude, ch1, ch2, profile = ' 
              '0, unit_freq = \'MHz\', unit_phase = \'FRAC\'')
        print('[5] io_update(self)')
        print('[6] set CFR1')
        print('[7] set CFR1')
        print('[8] set CFR1')
        print('[111] exit')
        order = input('select funct you want to implement')
        
        if( order == '1' ):
            freq_in_MHz = float(input('freq_in_MHz : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_frequency(freq_in_MHz, ch1, ch2)
            
        elif( order == '2' ):
            phase = float(input('freq_in_MHz : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_phase(phase, ch1, ch2, unit = 'FRAC')
        
        elif( order == '3' ):
            amplitude_frac = float(input('freq_in_MHz : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_amplitude(amplitude_frac, ch1, ch2)
            
        elif( order == '4' ):
            freq = float(input('freq : '))
            phase = float(input('phase : '))
            amplitude = float(input('amplitude : '))
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            profile = int(input('profile : '))
            dds.set_profile(freq, phase, amplitude, ch1, ch2, profile 
                            = 0, unit_freq = 'MHz', unit_phase = 'FRAC')
        
        elif( order == '5'):
            dds.io_update()
            
        elif( order == '6'):
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_CFR1(ch1, ch2)
            
        elif( order == '7'):
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_CFR2(ch1, ch2)
            
        elif( order == '8'):
            ch1 = int(input('ch1 : '))
            ch2 = int(input('ch2 : '))
            dds.set_CFR3(ch1, ch2)
            
        elif( order == '111' ):
            break
        
        else:
            print('error')

        
        