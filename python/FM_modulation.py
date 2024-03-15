# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:30:26 2023

@author: alexi
"""
from unit_set import *
from AD9910 import AD9910
from Arty_S7_v1_01 import ArtyS7
from uart_convertor import convertor_chain
import time
import math

gray_code = [0b000, 0b001, 0b011, 0b010, 0b110, 0b111, 0b101, 0b100]

class Experiment:
    def __init__(self, port):
        self.dds = AD9910(ArtyS7(port))
        
    def ram_write_frequency_list(self, freq_list,addr_step_rate):
        """
        RAM Data Write
        """
        #should reset driver before using override enable!!!!
        self.dds.auto_stop()
        self.dds.reset_driver()
        #For Ram input, set ram_en = 0, and set auto mode disable & override enabled
        self.dds.auto_mode_disable()
        self.dds.override_enable()
        last_addr = 0
        
        self.dds.set_now_cycle(0)
        
        self.dds.set_profile_pin(profile1 = 0, profile2 = 0)
        
        #set frequency register
        self.dds.set_frequency(ch1 = 1, ch2 = 0, freq = 10 * MHz)
        
        #set phase register
        self.dds.set_phase(ch1 = 1, ch2 = 0, phase = 0)
        
        #set amplitude register
        self.dds.set_amplitude(ch1 = 1, ch2 = 0, amplitude_frac = 0.8)
        
        self.dds.set_CFR1(ch1=1,ch2=0, ram_en = 0, ram_playback = 0, manual_OSK = 0, 
                      inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                      load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                      clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                      auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                      REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                      external_power_down_ctrl = 0, SDIO_in_only = 0, 
                      LSB_first = 0)
        
        self.dds.set_CFR2(ch1=1,ch2=0, amp_en_single_tone = 0, internal_IO_update = 0, 
                      SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                      DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                      IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                      matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                      parallel_port = 0, FM_gain = 0)
        
        self.dds.set_CFR3(ch1=1,ch2=0)
        
        self.dds.io_update(1,0)
        
        #set profile pin
        self.dds.set_profile_pin(profile1 = 0, profile2 = 0)
        
        #set ram profile to bidirectional ram mode with start address 0 to 
        #end address 16 with step rate 20
        for i in range(8):
            self.dds.set_ram_profile_register(ch1 = 1, ch2 = 0, addr_step_rate =addr_step_rate[i], 
                                      end_addr= last_addr + len(freq_list[i]) - 1, 
                                      start_addr = last_addr, no_dwell_high=0, zero_crossing=0, 
                                      ram_mode_ctrl=1, profile=i)
            last_addr = last_addr + len(freq_list[i])
            print('last addr : ' + str(last_addr))
            
        #send ram data
        #dds.ram_write_frequency(ch1=1,ch2=0,data_list = freq_list)
        for i in range(8):
            self.dds.set_profile_pin(profile1 = i, profile2 = 0)
            self.dds.io_update(1,0)
            self.dds.ram_write_frequency(ch1 = 1, ch2 = 0, data_list = freq_list[i])
            self.dds.io_update(1,0)
            print(f'freq {i}')
            print(freq_list[i])
        
        ###########################################################################
        #set ram_en = 1
        ###########################################################################
        self.dds.set_CFR1(ch1=1,ch2=0, ram_en = 1, ram_playback = 0, manual_OSK = 0, 
                      inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                      load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                      clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                      auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                      REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                      external_power_down_ctrl = 0, SDIO_in_only = 0, 
                      LSB_first = 0)
        
        
        
        ###########################################################################
        #setting auto mode
        ###########################################################################
        
        
        # For simulation, fpga should be closed at last code
        # self.dds.fpga.close()
    
    def do_experiment(self):
        """
        Exectue Experiment Code
        """
        self.dds.override_disable()
        self.dds.auto_stop()
        self.dds.reset_driver()
        self.dds.set_now_cycle(0)
        
        #Write Experiment code here
        # one cycle = 10 ns
        self.dds.auto_mode()
        
        self.dds.delay_cycle(1000)
                
        self.dds.io_update(1,0)
        self.dds.delay_cycle(10)
        self.dds.set_profile_pin(profile1 = 2, profile2 = 0)
        self.dds.delay_cycle(10)
        self.dds.io_update(1,0)
        self.dds.delay_cycle(1000000000)
        self.dds.set_profile_pin(profile1 = 0, profile2 = 0)

        self.dds.delay_cycle(int(len(freq_list[0])*4*addr_step_rate[0]/10))
        self.dds.set_profile_pin(profile1 = 1, profile2 = 0)

        self.dds.delay_cycle(int(len(freq_list[1])*4*addr_step_rate[1]/10))
        self.dds.set_profile_pin(profile1 = 0, profile2 = 0)

        self.dds.delay_cycle(int(len(freq_list[0])*4*addr_step_rate[0]/10))
        self.dds.set_profile_pin(profile1 = 2, profile2 = 0)
        
        self.dds.auto_start()
        
if __name__ == '__main__':
    port = input()
    exp = Experiment(port)
    
    freq_list = [[],[],[],[],[],[],[],[]]
    addr_step_rate = [1,1,1,1,1,1,1,1]
    
    freq_list[0] = [ 8*MHz, 16*MHz, 32*MHz, 48*MHz, 64*MHz, 80*MHz ]
    addr_step_rate[0] =200
    
    freq_list[1] = [ 1*MHz, 2*MHz, 3*MHz, 4*MHz, 5*MHz, 6*MHz, 7*MHz, 8*MHz, 9*MHz, 10*MHz ]
    addr_step_rate[1] =300
    
    freq_list[2] = [ 0*MHz ]
    addr_step_rate[2] =2000
    
    freq_list[3] = [ 130*MHz ]
    addr_step_rate[3] =2000
    
    freq_list[4] = [ 140*MHz ]
    addr_step_rate[4] =2000
    
    freq_list[5] = [ 150*MHz ]
    addr_step_rate[5] =2000
    
    freq_list[6] = [ 160*MHz ]
    addr_step_rate[6] =2000
    
    freq_list[7] = [ 190*MHz ]
    addr_step_rate[7] =2000
    
    while True:
        print('[1] Frequency RAM write')
        print('[2] Experiment')
        print('[m] manual mode')
        print('[c] convert')
        print('[q] exit')
        order_in = input()
        if( order_in == '1' ):
            exp.ram_write_frequency_list(freq_list,addr_step_rate)
        elif(order_in == '2'):
            exp.do_experiment()
        elif( order_in == 'c'):
            convertor_chain()
        elif( order_in == 'q'):
            print('exit')
            break
