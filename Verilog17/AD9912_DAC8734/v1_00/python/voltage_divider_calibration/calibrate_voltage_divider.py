# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 17:01:58 2018

@author: iontrap
Set "Res BW" to manual 100 kHz
"""

import time
import sys

from DDS_DAC_TCPClient_Class_v1_03 import DDS_DAC
from N9918A_v1_00 import N9918A

def measure(f, freq, dBm):
    sa.write('CALC:MARK1:FUNC:MAX')
    measured_freq=float(sa.query('CALC:MARK1:X?'))
    measured_power_dBm = float(sa.query('CALC:MARK1:Y?'))
    
    print('%.0f MHz, %.2f dBm, Freq: %.0f MHz, %.2f dBm' % \
          (freq, dBm, measured_freq/1e6, measured_power_dBm))
    f.write('%f, %f , %f, %f\n' % \
          (freq, dBm, measured_freq/1e6, measured_power_dBm))



if __name__ == '__main__':
    if 'sa' in vars(): # To close the previously opened device when re-running the script with "F5"
        sa.close()
    sa = N9918A('10.1.1.149')
    print(sa.query('*IDN?')) # Agilent Technologies,N9918A,MY53103462,A.07.50,2014-05-14.13:27
    
    if 'dds_dac' in globals():
        dds_dac.disconnect()

    dds_dac = DDS_DAC()
    dds_dac.connect() # TCP Server for Dual DDS with trigger output v1.00
    dds_dac.DDS1_output_on_off(True)

    f = open('calibration_divider_18-3.csv', 'w')
    
    dBm = 0
    time.sleep(0.5)
    dds_dac.DDS1_apply_power(dBm)
    time.sleep(0.5)
    try:
        #for freq_in_MHz in range(10, 101, 1):
        for freq_in_MHz in range(10, 101, 1):
            dds_dac.DDS1_apply_freq(freq_in_MHz)
            time.sleep(4)
            measure(f, freq_in_MHz, dBm)
            
    except KeyboardInterrupt:
        pass
        

    f.close()
    dds_dac.disconnect()
    sa.close()



