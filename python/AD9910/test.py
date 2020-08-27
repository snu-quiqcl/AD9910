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
    dds = AD9910(ArtyS7('COM12'))
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
        
def real_exp1(port):
    dds = AD9910(ArtyS7(port))
    dds.reset_driver()
    dds.auto_mode()
    
    dds.initialize(1,1)
    dds.delay_cycle(100000)
    dds.io_update(1,1)
    dds.delay_cycle(50)
    
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

def real_exp2():
    dds = AD9910(ArtyS7(port))
    
    dds.reset_driver()
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
    dds.set_frequency(300 * MHz)
    dds.io_update(1,0)
    
    dds.set_CFR2(1, 0, amp_en_single_tone = 0, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 1, FM_gain = 15)
    dds.io_update(1,0)
    
    dds.set_parallel_amplitude(0.5)
    time.sleep(15)
    dds.set_parallel_amplitude(0.7)
    time.sleep(15)
    set_parallel_frequency(200*MHz)
    time.sleep(15)
    set_parallel_frequency(100*MHz)
    
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

if __name__ == '__main__':
    while True:
        print('[1] exp1')
        print('[2] exp2')
        print('[3] exp3')
        print('[4] exp4')
        print('[5] exp5')
        print('[6] exp6')
        print('[r1] real_exp1')
        print('[r2] real_exp2')
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
        elif( order_in == 'r1'):
            port = input('PORT : ')
            real_exp1(port)
        elif( order_in == 'r2'):
            port = input('PORT : ')
            real_exp2(port)
        elif( order_in == 'c'):
            convertor_chain()
        elif( order_in == 'q'):
            print('exit')
            break
