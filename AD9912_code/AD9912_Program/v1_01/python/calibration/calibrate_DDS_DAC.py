# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:01:58 2018

@author: iontrap
Set "Res BW" to manual 100 kHz
"""

import time
import sys

from AD9912_DAC8734_v1_00 import FPGA, DAC8734, AD9912
from N9918A_v1_00 import N9918A

def measure(f, freq, voltage):
    time.sleep(1)            
    sa.write('CALC:MARK1:FUNC:MAX')
    measured_freq=float(sa.query('CALC:MARK1:X?'))
    measured_power_dBm = float(sa.query('CALC:MARK1:Y?'))
    
    print('%.0f MHz, %.2f (V), Freq: %.0f MHz, %.2f dBm' % \
          (freq, voltage, measured_freq/1e6, measured_power_dBm))
    f.write('%f, %f , %f, %f\n' % \
          (freq, voltage, measured_freq/1e6, measured_power_dBm))
    

if __name__ == '__main__':
    if 'fpga' in vars(): # To close the previously opened device when re-running the script with "F5"
        fpga.close()
    fpga = FPGA('COM16') # IonTrap-laptop1 (white - 32bit)
    #fpga = FPGA('COM38') # IonTrap8-광학실험실 테이블위 dummy terminal
    #fpga = FPGA('/dev/ttyUSB1')
    fpga.print_idn()

    dac = DAC8734(fpga)
    dds = AD9912(fpga, 10, 105)

    if 'sa' in vars(): # To close the previously opened device when re-running the script with "F5"
        sa.close()
    sa = N9918A('10.1.1.144')
    print(sa.query('*IDN?'))

    dds.set_current(0x03ff, 1, 1)

    f = open('calibration_test.csv', 'w')
    
    dac_ch = 0
    try:
        for freq in range(10, 101, 5):
            dds.set_frequency(freq, 1, 1)
    
            for voltage in range(0, 200, 1):
                voltage = voltage / 100
                dac.set_ch123(dac_ch, voltage)
                measure(f, freq, voltage)
            f.flush()
            
            for voltage in range(20, 50, 1):
                voltage = voltage / 10
                dac.set_ch123(dac_ch, voltage)
                measure(f, freq, voltage)
    
            for voltage in range(5, 16, 1):
                dac.set_ch123(dac_ch, voltage)
                measure(f, freq, voltage)
    
            f.flush()
    finally:
        f.close()
        

    f.close()

"""
dac.set_ch0_a1_a2_a3(1)
sa.write('CALC:MARK1:FUNC:MAX')
measured_freq=float(sa.query('CALC:MARK1:X?'))
measured_power_dBm = float(sa.query('CALC:MARK1:Y?'))

print('%.0f MHz, %.1f (V), Freq: %.0f MHz, %.2f dBm' % \
      (freq, voltage, measured_freq/1e6, measured_power_dBm))

"""