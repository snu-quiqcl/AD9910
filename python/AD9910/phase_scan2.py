from unit_set import *
from AD9910 import AD9910
from Arty_S7_v1_01 import ArtyS7
from uart_convertor import convertor_chain
import time
import math

gray_code = [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100]

        
dds = AD9910(ArtyS7('COM13'))

dds.auto_stop()
dds.reset_driver()
dds.auto_mode_disable()
dds.override_enable()

#set frequency register
dds.set_frequency(ch1 = 1, ch2 = 0, freq = 200 * MHz)
dds.io_update(1,0)

#set phase register
dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
dds.io_update(1,0)

#set amplitude register
dds.set_amplitude(ch1 = 1, ch2 = 0, amplitude_frac = 0.8)
dds.io_update(1,0)

dds.initialize(1,0)


dds.set_profile_pin(0,0)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,0)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,1)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,2)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,3)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,4)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,5)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,6)
dds.set_profile_register(1,0,190*MHz,0*deg,0.0,7)
while True:
    profile = input()
    
    if profile == '0':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,1)
    elif profile == '1':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,45*deg,1.0,1)
    elif profile == '2':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,90*deg,1.0,1)
    elif profile == '3':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,135*deg,1.0,1)
    elif profile == '4':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,180*deg,1.0,1)
    elif profile == '5':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,225*deg,1.0,1)
    elif profile == '6':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,270*deg,1.0,1)
    elif profile == '7':
        dds.set_profile_register(1,0,200*MHz,0*deg,1.0,0)
        dds.set_profile_register(1,0,200*MHz,315*deg,1.0,1)
    elif profile == 's':
        break    
    dds.io_update(1,0)