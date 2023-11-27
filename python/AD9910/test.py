#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:43:56 2020

@author: parkjeonghyun
"""
from unit_set import *
from AD9910 import AD9910
from Arty_S7_v1_01 import ArtyS7
from uart_convertor import convertor_chain
import time

def exp1():
    dds = AD9910(ArtyS7('COM12'))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    #dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 100*MHz, phase = 0 * RAD, 
    #                         amplitude = 1.0, profile = 1)
    dds.delay_cycle(10000)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp1')
            dds.fpga.close()
            return

def exp2():
    dds = AD9910(ArtyS7('COM6'))
    dds.reset_driver()
    dds.auto_mode()
    dds.delay_cycle(500)
    #dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
    #                         amplitude = 1.0, profile = 0)
    dds.set_parallel_amplitude(amplitude = 1.0, parallel_en = 1)
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp2')
            dds.fpga.close()
            return

def exp3():
    dds = AD9910(ArtyS7('COM12'))
    dds.reset_driver()
    dds.override_enable()
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 100*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 1)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.set_parallel_amplitude(amplitude = 1.0, parallel_en = 1)
    dds.initialize(1,1)
    dds.read32(1,0,0x00)
    dds.read32(0,1,0x01)
    dds.read32(1,0,0x02)
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp3')
            dds.fpga.close()
            return
    
def exp4():
    dds = AD9910(ArtyS7('COM12'))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 100*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 1)
    dds.delay_cycle(10000)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.read32(1,0,0x00)
    dds.read32(0,1,0x01)
    dds.read32(1,0,0x02)
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    dds.read_rti_fifo()
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp4')
            dds.fpga.close()
            return

def exp5():
    dds = AD9910(ArtyS7(None))
    dds.reset_driver()
    dds.auto_mode()
    dds.initialize(1,1)
    dds.delay_cycle(30000)
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 30*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 60*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 1)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 90*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 2)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 120*MHz, phase = 0 * RAD, 
                             amplitude = 0.5, profile = 3)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 150*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 4)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 180*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 5)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 210*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 6)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 240*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 7)
    
    dds.delay_cycle(10000)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 2, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 4, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.delay_cycle(50)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.read_exception_log()
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
        elif( order_in == 'q'):
            print('exit exp5')
            dds.fpga.close()
            return
        
def exp6():
    dds = AD9910(ArtyS7(None))
    dds.reset_driver()
    dds.override_enable()
    
    dds.initialize(1,0)
    dds.io_update(1,0)
    
    dds.set_frequency(1, 0, 1 * MHz)
    dds.io_update(1,0)
    
    dds.set_amplitude(1,0,1.0)
    dds.io_update(1,0)
    
    dds.set_phase(1, 0, 0 * RAD)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 3, start_addr = 0,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 0)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 7, start_addr = 4,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 1)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 11, start_addr = 8,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 2)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 15, start_addr = 12,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 3)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 19, start_addr = 16,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 4)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 23, start_addr = 20,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 5)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 27, start_addr = 24,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 6)
    dds.io_update(1,0)
    
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate = 4,
                                 end_addr = 31, start_addr = 28,
                                 no_dwell_high = 0, zero_crossing = 0,
                                 ram_mode_ctrl = 0b001, profile = 7)
    dds.io_update(1,0)
    
    freq_list0 = [ 1*MHz, 2*MHz, 3*MHz, 4*MHz]
    freq_list1 = [ 10*MHz, 20*MHz, 30*MHz, 40*MHz]
    freq_list2 = [ 50*MHz, 60*MHz, 70*MHz, 80*MHz]
    freq_list3 = [ 90*MHz, 100*MHz, 110*MHz, 120*MHz]
    freq_list4 = [ 130*MHz, 140*MHz, 150*MHz, 160*MHz]
    freq_list5 = [ 170*MHz, 180*MHz, 190*MHz, 200*MHz]
    freq_list6 = [ 210*MHz, 220*MHz, 230*MHz, 240*MHz]
    freq_list7 = [ 250*MHz, 260*MHz, 270*MHz, 280*MHz]
    total_freq_list = freq_list0 + freq_list1 + freq_list2 + freq_list3 + \
        freq_list4 + freq_list5 + freq_list6 + freq_list7
    
    dds.ram_write_frequency(1,0,total_freq_list)
    dds.io_update(1,0)
    
    dds.set_CFR1(1, 0, ram_en = 1, ram_playback = 0b00, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0b0010, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    dds.io_update(1,0)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65))
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_17_int_list()
            if( received_int_list == 0xff ):
                print('EMPTY')
            else:
                print(dds.read_17_int_list())
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(dds.fpga.read_next())
        
        elif( order_in == 'q'):
            print('exit real_exp1')
            dds.fpga.close()
            return
        
def exp7():
    dds = AD9910(ArtyS7(None))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 50*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    dds.delay_cycle(100)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(100)
    dds.io_update(1,0)
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp1')
            dds.fpga.close()
            return
        
def exp8():
    dds = AD9910(ArtyS7(None))
    dds.auto_mode()
    
    dds.reset_driver()
    dds.set_CFR1(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    dds.set_CFR2(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    dds.set_CFR3(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    
    #dds.initialize(1,0)
    #dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 200*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    
    dds.delay_cycle(10000)
    
    dds.set_frequency(ch1=1,ch2=0,freq=200*MHz)   
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_amplitude(ch1 = 1, ch2 =0, amplitude_frac = 1.0)
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x09)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == 'q'):
            print('exit exp1')
            dds.fpga.close()
            return
        
def exp9():
    """
    For read function test
    read value
    '01100010',
    '01110110',
    '01100111',
    '00000110',
    '01110100',
    '01100111',
    '01000110',
    '01110000',
    '00000111',
    '00000000',
    '01110000',
    '00000111',
    '00000000',
    '01110100',
    '00000111',
    '00000000',
    '01110000',
    '00000111',
    '00000000',
    '01110000',
    '00000111',
    '00000000',
    '01110000',
    '00000111',
    '01001000',
    '01110011',
    '00111111',
    '00110110',
    '11110011',
    '01101111',
    '01011100',
    '11110010',
    '00110111',
    '00100111',
    '01110010',
    '10000111',
    '01100010',
    '01110110',
    '01100111',
    '00001100',
    '11101000',
    '11001110',
    '10001100',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11101000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00011010',
    '11100110',
    '00001110',
    '01101101',
    '11100110',
    '11011110',
    '10111001',
    '11100100',
    '01101110',
    '01001110',
    '11100101',
    '00001111'
    
    -->
    11000100
    11101100
    11001110
    00001100
    11101000
    11001110
    10001100
    11100000
    00001110
    00000000
    11100000
    00001110
    00000000
    11101000
    00001110
    00000000
    11100000
    00001110
    00000000
    11100000
    00001110
    00000000
    11100000
    00001110
    10010000
    11100110
    01111110
    01101101
    11100110
    11011110
    10111001
    11100100
    01101110
    01001110
    11100101
    00001110
    11000100
    11101100
    11001110
    00011001
    11010001
    10011101
    00011001
    11000000
    00011100
    00000001
    11000000
    00011100
    00000001
    11010000
    00011100
    00000001
    11000000
    00011100
    00000001
    11000000
    00011100
    00000001
    11000000
    00011100
    00110101
    11001100
    00011100
    11011011
    11001101
    10111101
    01110011
    11001000
    11011100
    10011101
    11001010
    00011111
    
    ->'11000100',
    '11101100',
    '11001110',
    '00001100',
    '11101000',
    '11001110',
    '10001100',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11101000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '00000000',
    '11100000',
    '00001110',
    '10010000',
    '11100110',
    '01111110',
    '01101101',
    '11100110',
    '11011110',
    '10111001',
    '11100100',
    '01101110',
    '01001110',
    '11100101',
    '00001110',
    '11000100',
    '11101100',
    '11001110',
    '00011001',
    '11010001',
    '10011101',
    '00011001',
    '11000000',
    '00011100',
    '00000001',
    '11000000',
    '00011100',
    '00000001',
    '11010000',
    '00011100',
    '00000001',
    '11000000',
    '00011100',
    '00000001',
    '11000000',
    '00011100',
    '00000001',
    '11000000',
    '00011100',
    '00110101',
    '11001100',
    '00011100',
    '11011011',
    '11001101',
    '10111101',
    '01110011',
    '11001000',
    '11011100',
    '10011101',
    '11001010',
    '00011111'
    
    dat2.append(int(''.join(reversed(a)),2))
                    
    [35,
     55,
     115,
     48,
     23,
     115,
     49,
     7,
     112,
     0,
     7,
     112,
     0,
     23,
     112,
     0,
     7,
     112,
     0,
     7,
     112,
     0,
     7,
     112,
     9,
     103,
     126,
     182,
     103,
     123,
     157,
     39,
     118,
     114,
     167,
     112,
     35,
     55,
     115,
     152,
     139,
     185,
     152,
     3,
     56,
     128,
     3,
     56,
     128,
     11,
     56,
     128,
     3,
     56,
     128,
     3,
     56,
     128,
     3,
     56,
     172,
     51,
     56,
     219,
     179,
     189,
     206,
     19,
     59,
     185,
     83,
     248]
    
    for i in range(length):
        next_val = self.fpga.read_next()
        int_list.append(int.from_bytes(next_val.encode('latin-1'),'little'))
    """
    dds = AD9910(ArtyS7(None))
    dds.reset_driver()
    dds.auto_mode()
    
    dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x09)
    dds.delay_cycle(20000)
    
    #dds.read64(ch1 = 1, ch2 = 0, register_addr = 0x11)
    #dds.delay_cycle(20000)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
            dds.read_rti_fifo()
            #dds.read_rti_fifo()
        elif( order_in == 'q'):
            print('exit exp9')
            dds.fpga.close()
            return
        
def exp10():
    """
    real_exp6 simulation

    """
    dds = AD9910(ArtyS7(None))
    dds.auto_mode()
    
    dds.reset_driver()
    dds.set_CFR1(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    dds.set_CFR2(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    dds.set_CFR3(ch1=1,ch2=0)
    dds.delay_cycle(10000)
    
    #dds.initialize(1,0)
    #dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 100*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    
    dds.delay_cycle(10000)
    
    dds.set_frequency(ch1=1,ch2=0,freq=200*MHz)   
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_amplitude(ch1 = 1, ch2 =0, amplitude_frac = 1.0)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
            dds.read_rti_fifo()
            #dds.read_rti_fifo()
        elif( order_in == 'q'):
            print('exit exp10')
            dds.fpga.close()
            return
        
def exp11():
    """
    RAM mode simulation
    """
    dds = AD9910(ArtyS7(None))
    #should reset driver before using override enable!!!!
    dds.reset_driver()
    #For Ram input, set ram_en = 0, and set auto mode disable & override enabled
    dds.auto_mode_disable()
    dds.override_enable()
    
    freq_list = [ 10*MHz, 12*MHz, 14*MHz, 16*MHz, 18*MHz, 20*MHz, 22*MHz, 24*MHz,
                 26*MHz, 28*MHz, 30*MHz, 32*MHz, 34*MHz, 36*MHz, 38*MHz, 40*MHz]
    
    
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 0, ram_playback = 0, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 1, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 0, FM_gain = 0)
    dds.set_CFR3(ch1=1,ch2=0)
    
    dds.io_update(1,0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =20, 
                                 end_addr= len(freq_list) - 1, 
                                 start_addr=0, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=0)
    
    #set profile pin
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #send ram data
    dds.ram_write_frequency(ch1=1,ch2=0,data_list = freq_list)
    
    dds.io_update(1,0)
    
    #set ram_en = 1
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 1, ram_playback = 0, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    
    dds.io_update(1,0)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
            dds.read_rti_fifo()
            #dds.read_rti_fifo()
        elif( order_in == 'q'):
            print('exit exp11')
            dds.fpga.close()
            return
        
def exp12():
    """
    parallel mode simulation
    """
    dds = AD9910(ArtyS7(None))
    dds.reset_driver()
    dds.auto_mode()
    
    dds.initialize(1,1)
    dds.delay_cycle(30000)
    dds.io_update(ch1=1, ch2=0)
    dds.delay_cycle(1000)
    
    dds.set_amplitude(1, 0, 1.0)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_phase(1, 0, 0 * RAD)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_frequency(1,0,180 * MHz)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 1, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 1, FM_gain = 15)
    
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    
    dds.delay_cycle(1000)
    
    dds.set_parallel_frequency(frequency = 20*MHz , set_fm_gain = False,
                               parallel_en = 1)
    dds.delay_cycle(1000)
    
    dds.set_parallel_frequency(frequency = 25*MHz , set_fm_gain = False,
                               parallel_en = 1)
    dds.delay_cycle(1000)
    
    dds.set_parallel_frequency(frequency = 30*MHz , set_fm_gain = False,
                               parallel_en = 1)
    dds.delay_cycle(1000)
    
    dds.set_parallel_frequency(frequency = 15*MHz , set_fm_gain = False,
                               parallel_en = 1)
    dds.delay_cycle(1000)
    
    
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
            dds.read_rti_fifo()
            #dds.read_rti_fifo()
        elif( order_in == 'q'):
            print('exit exp11')
            dds.fpga.close()
            return
    
        
def real_exp1(port):
    dds = AD9910(ArtyS7(port))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_now_cycle(0)
    
    dds.initialize(1,1)
    dds.delay_cycle(100000)
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 30*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 60*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 1)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 90*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 2)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 120*MHz, phase = 0 * RAD, 
                             amplitude = 0.5, profile = 3)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 150*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 4)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 180*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 5)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 210*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 6)
    dds.delay_cycle(10000)
    
    dds.io_update(1,1)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 240*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 7)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 2, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 4, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp1')
            dds.fpga.close()
            return

def real_exp2(port):
    dds = AD9910(ArtyS7(port))
    
    dds.reset_driver()
    dds.set_now_cycle(0)
    dds.auto_mode_disable()
    dds.override_enable()
    
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 30*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.io_update(1,0)
    
    dds.initialize(1,0)
    dds.io_update(1,0)
    
    dds.set_amplitude(1, 0, 1.0)
    dds.io_update(1,0)
    dds.set_phase(1, 0, 0 * RAD)
    dds.io_update(1,0)
    dds.set_frequency(1,0,300 * MHz)
    dds.io_update(1,0)
    
    dds.set_amplitude(ch1 =1 ,ch2 = 0, amplitude_frac = 1.0)
    
    dds.io_update(1,0)
    time.sleep(5)
    dds.set_frequency(ch1 =1 ,ch2 = 0, freq = 200*MHz)
    
    dds.io_update(1,0)
    time.sleep(5)
    dds.set_frequency(ch1 =1 ,ch2 = 0, freq = 100*MHz)
    
    dds.io_update(1,0)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65+7))
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp2')
            dds.fpga.close()
            return

def real_exp3(port):
    dds = AD9910(ArtyS7(port))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_now_cycle(0)
    dds.delay_cycle(500)
    #dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
    #                         amplitude = 1.0, profile = 0)
    dds.set_parallel_amplitude(amplitude = 1.0, parallel_en = 1)
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            print(received_int_list)
            
            #if( received_int_list[5] == 0xff ):
            #    print('EMPTY')
            #else:
            #    print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp3')
            dds.fpga.close()
            return
        
def real_exp4(port):
    """
    To check 000->011 glitch using PLL

    """
    dds = AD9910(ArtyS7(port))
    dds.auto_mode()
    dds.set_now_cycle(0)
    
    dds.reset_driver()
    dds.delay_cycle(100000)
    
    dds.initialize(1,0)
    dds.delay_cycle(100000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_CFR3(ch1 = 1, ch2 = 0, DRV0 = 0, PLL_VCO = 7, I_CP = 0, 
                 REFCLK_div_bypass = 1, REFCLK_input_div_reset = 1, 
                 PFD_reset = 0, PLL_en = 1, N = 25)
    # PLL is enabled with divider number N = 25. PLL_VCO is selected for proper VCO range.
    dds.delay_cycle(100000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 30*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 60*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 1)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 90*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 2)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 120*MHz, phase = 0 * RAD, 
                             amplitude = 0.5, profile = 3)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 150*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 4)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 180*MHz, phase = 0 * RAD, 
                             amplitude = 0.2, profile = 5)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 210*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 6)
    dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 240*MHz, phase = 0 * RAD, 
                             amplitude = 0.8, profile = 7)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 7, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    dds.delay(20*s)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(1000)
    dds.io_update(1,0)
    
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp4')
            dds.fpga.close()
            return

def real_exp5(port):
    dds = AD9910(ArtyS7(port))
    dds.auto_mode()
    dds.set_now_cycle(0)
    
    dds.reset_driver()
    
    dds.delay_cycle(20000)
    
    #dds.set_profile_pin(profile1 = 4, profile2 = 0)
    #dds.delay_cycle(200000)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(200000)
    
    dds.set_CFR1(ch1=1,ch2=0)
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_CFR2(ch1=1,ch2=0)
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_CFR3(ch1=1,ch2=0)
    dds.delay_cycle(20000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.delay_cycle(1000)
    
    #dds.initialize(1,0)
    #dds.delay_cycle(10000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_profile_register(ch1 = 1, ch2 = 0, freq = 100*MHz, phase = 0 * RAD, 
                             amplitude = 1, profile = 0)
    
    dds.delay_cycle(10000)
    
    dds.set_frequency(ch1=1,ch2=0,freq=100*MHz)   
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.set_amplitude(ch1 = 1, ch2 =0, amplitude_frac = 1)
    dds.delay_cycle(10000)
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(1000)
    
    dds.io_update(1,0)
    dds.delay_cycle(1000)
    
    dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x00)
    dds.delay_cycle(10000)
    #dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x01)
    dds.delay_cycle(10000)
    #dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x02)
    dds.delay_cycle(10000)
    #dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x07)
    dds.delay_cycle(10000)
    #dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x08)
    dds.delay_cycle(10000)
    #dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x09)
    dds.delay_cycle(10000)
    #dds.read64(ch1 = 1, ch2 = 0, register_addr = 0x0F)
    dds.delay_cycle(20000)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp5')
            dds.fpga.close()
            return
        
def real_exp6(port):
    dds = AD9910(ArtyS7(port))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_now_cycle(0)
    
    dds.read32(ch1 = 1, ch2 = 0, register_addr = 0x09)
    dds.delay_cycle(20000)
    
    #dds.read64(ch1 = 1, ch2 = 0, register_addr = 0x11)
    #dds.delay_cycle(20000)
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp5')
            dds.fpga.close()
            return
        
def real_exp7(port):
    """
    RAM mode simulation
    """
    dds = AD9910(ArtyS7(port))
    #should reset driver before using override enable!!!!
    dds.reset_driver()
    #For Ram input, set ram_en = 0, and set auto mode disable & override enabled
    dds.auto_mode_disable()
    dds.override_enable()
    dds.set_now_cycle(0)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set frequency register
    dds.set_frequency(ch1 = 1, ch2 = 0, freq = 100 * MHz)
    
    #set phase register
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    
    #set amplitude register
    dds.set_amplitude(ch1 = 1, ch2 = 0, amplitude_frac = 0.5)
    
    freq_list = [ 100*MHz, 120*MHz, 140*MHz, 160*MHz, 180*MHz, 200*MHz, 220*MHz, 240*MHz,
                 260*MHz, 280*MHz, 300*MHz]
    
    #amplitude_list = [0.5, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.0]
    
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 0, ram_playback = 0, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 0, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 0, FM_gain = 0)
    dds.set_CFR3(ch1=1,ch2=0)
    
    dds.io_update(1,0)
    
    #set profile pin
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 10, 
                                 start_addr=0, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 21, 
                                 start_addr=11, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=1)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 32, 
                                 start_addr=22, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=2)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 43, 
                                 start_addr=33, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=3)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 54, 
                                 start_addr=44, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=4)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 65, 
                                 start_addr=55, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=5)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 76, 
                                 start_addr=66, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=6)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 87, 
                                 start_addr=77, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=7)
        
    #send ram data
    #dds.ram_write_frequency(ch1=1,ch2=0,data_list = freq_list)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 2, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 4, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 7, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list)
    dds.io_update(1,0)
    
    ###########################################################################
    #set ram_en = 1
    ###########################################################################
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 1, ram_playback = 0, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    
    dds.io_update(1,0)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.override_disable()
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp5')
            dds.fpga.close()
            return
        
def real_exp8(port):
    """
    RAM mode simulation
    """
    dds = AD9910(ArtyS7(port))
    #should reset driver before using override enable!!!!
    dds.reset_driver()
    #For Ram input, set ram_en = 0, and set auto mode disable & override enabled
    dds.auto_mode_disable()
    dds.override_enable()
    dds.set_now_cycle(0)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set frequency register
    dds.set_frequency(ch1 = 1, ch2 = 0, freq = 100 * MHz)
    
    #set phase register
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    
    #set amplitude register
    dds.set_amplitude(ch1 = 1, ch2 = 0, amplitude_frac = 0.0)
    
    #freq_list = [ 100*MHz, 120*MHz, 140*MHz, 160*MHz, 180*MHz, 200*MHz, 220*MHz, 240*MHz,
    #             260*MHz, 280*MHz, 300*MHz]
    
    amplitude_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 0, ram_playback = 2, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 0, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 0, FM_gain = 0)
    dds.set_CFR3(ch1=1,ch2=0)
    
    dds.io_update(1,0)
    
    #set profile pin
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 10, 
                                 start_addr=0, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 21, 
                                 start_addr=11, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=1)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 32, 
                                 start_addr=22, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=2)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 43, 
                                 start_addr=33, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=3)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 54, 
                                 start_addr=44, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=4)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 65, 
                                 start_addr=55, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=5)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 76, 
                                 start_addr=66, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=6)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =100, 
                                 end_addr= 87, 
                                 start_addr=77, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=7)
        
    #send ram data
    #dds.ram_write_frequency(ch1=1,ch2=0,data_list = freq_list)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 2, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 4, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 7, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.io_update(1,0)
    
    ###########################################################################
    #set ram_en = 1
    ###########################################################################
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 1, ram_playback = 2, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    
    dds.io_update(1,0)
    
    dds.override_disable()
    
    ###########################################################################
    #setting auto mode
    ###########################################################################
    dds.auto_stop()
    dds.set_now_cycle(0)
    dds.reset_driver()
    dds.auto_mode()
    
    dds.delay_cycle(1000)
    dds.io_update(1,1)
    
    dds.delay_cycle(1000)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    
    dds.delay_cycle(2000)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    dds.delay_cycle(2000)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    
    dds.delay_cycle(2000)
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    ###########################################################################
    #start auto mode
    ###########################################################################
    dds.auto_start()
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp5')
            dds.fpga.close()
            return    
        
def real_exp9(port):
    """
    RAM mode simulation
    """
    dds = AD9910(ArtyS7(port))
    #should reset driver before using override enable!!!!
    dds.reset_driver()
    #For Ram input, set ram_en = 0, and set auto mode disable & override enabled
    dds.auto_mode_disable()
    dds.override_enable()
    dds.set_now_cycle(0)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set frequency register
    dds.set_frequency(ch1 = 1, ch2 = 0, freq = 100 * MHz)
    
    #set phase register
    dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
    
    #set amplitude register
    dds.set_amplitude(ch1 = 1, ch2 = 0, amplitude_frac = 0.5)
    
    #freq_list = [ 100*MHz, 120*MHz, 140*MHz, 160*MHz, 180*MHz, 200*MHz, 220*MHz, 240*MHz,
    #             260*MHz, 280*MHz, 300*MHz]
    
    amplitude_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 0, ram_playback = 2, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 0, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 0, FM_gain = 0)
    dds.set_CFR3(ch1=1,ch2=0)
    
    dds.io_update(1,0)
    
    #set profile pin
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 10, 
                                 start_addr=0, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=0)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 21, 
                                 start_addr=11, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=1)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 32, 
                                 start_addr=22, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=2)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 43, 
                                 start_addr=33, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=3)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 54, 
                                 start_addr=44, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=4)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 65, 
                                 start_addr=55, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=5)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 76, 
                                 start_addr=66, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=6)
    
    #set ram profile to bidirectional ram mode with start address 0 to 
    #end address 16 with step rate 20
    dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =2000, 
                                 end_addr= 87, 
                                 start_addr=77, no_dwell_high=0, zero_crossing=0, 
                                 ram_mode_ctrl=2, profile=7)
        
    #send ram data
    #dds.ram_write_frequency(ch1=1,ch2=0,data_list = freq_list)
    
    dds.set_profile_pin(profile1 = 0, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 2, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 3, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 4, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 5, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 6, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    dds.set_profile_pin(profile1 = 7, profile2 = 0)
    dds.io_update(1,0)
    dds.ram_write_amplitude(ch1 = 1, ch2 = 0, data_list = amplitude_list)
    dds.io_update(1,0)
    
    ###########################################################################
    #set ram_en = 1
    ###########################################################################
    dds.set_CFR1(ch1=1,ch2=0, ram_en = 1, ram_playback = 2, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0)
    
    
    dds.io_update(1,0)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.set_profile_pin(1,0)
    dds.io_update(1,0)
    print('set HIGH')
    time.sleep(5)
    
    
    dds.set_profile_pin(0,0)
    dds.io_update(1,0)
    print('set LOW')
    time.sleep(5)
    
    dds.override_disable()
    
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[3] exception log')
        print('[4] rti value')
        print('[r] read next')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            dds.auto_start()
        elif( order_in == '2'):
            dds.auto_stop()
        elif( order_in == '3'):
            dds.read_exception_log()
            print('EXCEPTION LOG : ',end = '')
            print(dds.read_int_list(65 + 7))
            # 7-> "#3 2 bit + length in 3 bit + \r\n 2bit"
        elif( order_in == '4'):
            dds.read_rti_fifo()
            print('RTI FIFO LIST : ',end = '')
            received_int_list = dds.read_int_list(17 + 7)
            if( received_int_list[5] == 0xff ):
                print('EMPTY')
            else:
                print(received_int_list)
        
        elif( order_in == 'r'):
            print('next_val : ',end = '')
            print(int.from_bytes(dds.fpga.read_next().encode('latin-1'),'little'))
        
        elif( order_in == 'q'):
            print('exit real_exp5')
            dds.fpga.close()
            return    
        
def manual_mode(port):
    """
    manual mode for real time control
    """
    dds = AD9910(ArtyS7(port))
    #should reset driver before using override enable!!!!
    dds.reset_driver()
    
    while True:
        cont_ch1 = 1
        cont_ch2 = 2
        print('[1] CFR1 setting')
        print('[2] CFR2 setting')
        print('[3] CFR3 setting')
        print('[pf]profile')
        print('[pp]profile pin')
        print('[a] Set amplitude')
        print('[f] Set frequency')
        print('[p] Set phase')
        print('[i] IO_UPDATE')
        print('[q] exit')
        
        cmd = input()
        
        if(cmd == 'f' or cmd == 'F'):
            print('frequency value(control channel 1,2) : ')
            freq = input()
            freq_unit = 1
            
            if ('K' in freq) or ('k' in freq):
                freq_unit = 1000
            
            if ('M' in freq) or ('m' in freq):
                freq_unit = 1000000
            
            if ('G' in freq) or ('g' in freq):
                freq_unit = 1000000000
                
            if ('T' in freq) or ('t' in freq):
                freq_unit = 1000000000000
            
            num_len = 0
            while num_len < len(freq):
                if freq[num_len] > '9' or freq[num_len] <'0':
                    break
                num_len += 1
            
            if num_len < 1:
                raise Exception('No number enetered')
                
            freq_num = int(freq[0:num_len])
            freq_num = freq_num * freq_unit
            print(str(freq_num) + 'Hz')
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_frequency(ch1=cont_ch1, ch2=cont_ch2, freq = freq_num)
            dds.delay_cycle(1500)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
            
        elif(cmd == 'a' or cmd == 'A'):
            print('amplitude_frac value(control channel 1,2) : ')
            amp = input()
            amp_frac_num = float(amp)
            if amp_frac_num < 0 or amp_frac_num > 1:
                raise Exception('wrong amplitude number')
            
            print(amp)
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_amplitude(ch1 = cont_ch1, ch2 = cont_ch2, amplitude_frac = amp_frac_num)
            dds.delay_cycle(1500)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
        
        elif(cmd == 'p' or cmd == 'P'):
            print('phase value(control channel 1,2) (unit is radian): ')
            phase = input()
            phase_unit = 1
            
            phase_num = float(phase) * phase_unit
            if phase_num < 0 or phase_num > 2*PI:
                raise Exception('wrong phase number')
                
            print(phase)
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_phase(ch1 = cont_ch1, ch2 = cont_ch2, phase = phase_num)
            dds.delay_cycle(1500)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
        
        elif(cmd == 'pf' or cmd == 'PF'):
            print('profile (0~7) : ')
            profile_num = int(input())
            if(profile_num < 0 or profile_num > 7):
                raise Exception('wrong profile number')
            
            print(str(profile_num))
            
            print('frequency value(control channel 1,2) : ')
            freq = input()
            freq_unit = 1
            
            if ('K' in freq) or ('k' in freq):
                freq_unit = 1000
            
            if ('M' in freq) or ('m' in freq):
                freq_unit = 1000000
            
            if ('G' in freq) or ('g' in freq):
                freq_unit = 1000000000
                
            if ('T' in freq) or ('t' in freq):
                freq_unit = 1000000000000
            
            num_len = 0
            while num_len < len(freq):
                if freq[num_len] > '9' or freq[num_len] <'0':
                    break
                num_len += 1
            
            if num_len < 1:
                raise Exception('No number enetered')
                
            freq_num = int(freq[0:num_len])
            freq_num = freq_num * freq_unit
            print(str(freq_num) + 'Hz')
            
            print('amplitude_frac value(control channel 1,2) : ')
            amp = input()
            amp_frac_num = float(amp)
            if amp_frac_num < 0 or amp_frac_num > 1:
                raise Exception('wrong amplitude number')
            
            print(amp)
            
            print('phase value(control channel 1,2) (unit is radian): ')
            phase = input()
            phase_unit = 1
            
            phase_num = float(phase) * phase_unit
            if phase_num < 0 or phase_num > 2*PI:
                raise Exception('wrong phase number')
                
            print(phase)
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_profile_register(ch1 = cont_ch1, ch2 = cont_ch2, freq = freq_num, phase = phase_num, 
                                     amplitude = amp_frac_num, profile = profile_num)
            dds.delay_cycle(3000)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
            
        elif( cmd == 'pp' or cmd == 'PP'):
            print('profile (change ch1, ch2 simultaneously )(0~7) : ')
            profile_num = int(input())
            if(profile_num < 0 or profile_num > 7):
                raise Exception('wrong profile number')
            
            print(str(profile_num))
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_profile_pin(profile1 = profile_num, profile2 = profile_num)
            dds.delay_cycle(3000)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
            
        elif( cmd == '1'):
            print('CFR1 setting')
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_CFR1(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.delay_cycle(3000)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
        
        elif( cmd == '2'):
            print('CFR2 setting')
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_CFR2(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.delay_cycle(3000)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
            
        elif( cmd == '3'):
            print('CFR3 setting')
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.auto_mode()
            dds.set_CFR3(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.delay_cycle(3000)
            dds.io_update(ch1 = cont_ch1, ch2 = cont_ch2)
            dds.auto_start()
            
        elif(cmd == 'q'):
            print('exit manual mode')
            dds.fpga.close()
            return
        
        if(cmd == 'i' or cmd == 'I'):
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.reset_driver()
            dds.delay_cycle(30)
            dds.auto_mode()
            dds.io_update(ch1 = 0, ch2 = 1)
            dds.delay_cycle(200)
            dds.io_update(ch1 = 1, ch2 = 0)
            dds.auto_start()
            
            
            dds.auto_stop()
            dds.set_now_cycle(0)
            dds.delay_cycle(30)
            dds.auto_mode()
            dds.io_update(ch1 = 0, ch2 = 1)
            dds.delay_cycle(200)
            dds.io_update(ch1 = 1, ch2 = 0)
            dds.auto_start()
            print('done')
        
        else:
            print('Wrong command')

if __name__ == '__main__':
    while True:
        print('[1] exp1')
        print('[2] exp2')
        print('[3] exp3')
        print('[4] exp4')
        print('[5] exp5')
        print('[6] exp6')
        print('[7] exp7')
        print('[8] exp8')
        print('[9] exp9')
        print('[10] exp10')
        print('[10] exp11')
        print('[10] exp12')
        print('[r1] real_exp1')
        print('[r2] real_exp2')
        print('[r3] real_exp3')
        print('[r4] real_exp4')
        print('[r5] real_exp5')
        print('[r6] real_exp6')
        print('[r7] real_exp7')
        print('[r8] real_exp7')
        print('[r9] real_exp7')
        print('[m] manual mode')
        print('[c] convert')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            exp1()
        elif( order_in == '2'):
            exp2()
        elif( order_in == '3'):
            exp3()
        elif( order_in == '4'):
            exp4()
        elif( order_in == '5'):
            exp5()
        elif( order_in == '6'):
            exp6()
        elif( order_in == '7'):
            exp7()
        elif( order_in == '8'):
            exp8()
        elif( order_in == '9'):
            exp9()
        elif( order_in == '10'):
            exp10()
        elif( order_in == '11'):
            exp11()
        elif( order_in == '12'):
            exp12()
        elif( order_in == 'r1'):
            port = input('PORT : ')
            real_exp1(port)
        elif( order_in == 'r2'):
            port = input('PORT : ')
            real_exp2(port)
        elif( order_in == 'r3'):
            port = input('PORT : ')
            real_exp3(port)
        elif( order_in == 'r4'):
            port = input('PORT : ')
            real_exp4(port)
        elif( order_in == 'r5'):
            port = input('PORT : ')
            real_exp5(port)
        elif( order_in == 'r6'):
            port = input('PORT : ')
        elif( order_in == 'r7'):
            port = input('PORT : ')
            real_exp7(port)
        elif( order_in == 'r8'):
            port = input('PORT : ')
            real_exp8(port)
        elif( order_in == 'r9'):
            port = input('PORT : ')
            real_exp9(port)
        elif( order_in == 'm'):
            port = input('PORT : ')
            manual_mode(port)
        elif( order_in == 'c'):
            convertor_chain()
        elif( order_in == 'q'):
            print('exit')
            break
