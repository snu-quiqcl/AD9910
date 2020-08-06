# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:08:40 2020

@author: JeonghyunPark
"""

from Arty_S7_v1_01 import ArtyS7
#This ArtyS7 is in the AD9912 folder

"""
register address of AD9910 is defined here
"""
CFR1_ADDR               = 0x00
CFR2_ADDR               = 0x01
CFR3_ADDR               = 0x02
AUX_DAC_ADRR            = 0x03
IO_UPDATE_RATE_ADDR     = 0x04
FTW_ADDR                = 0x07
POW_ADDR                = 0x08
ASF_ADDR                = 0x09
SYNC_REG_ADDR           = 0x0A
DRG_LIMIT_ADDR          = 0x0B
DRG_RAMP_STEP_SIZE_ADDR = 0x0C
DRG_RAMP_RATE_ADDR      = 0x0D
PROFILE0_ADDR           = 0x0E
PROFILE1_ADDR           = 0x0F
PROFILE2_ADDR           = 0x10
PROFILE3_ADDR           = 0x11
PROFILE4_ADDR           = 0x12
PROFILE5_ADDR           = 0x13
PROFILE6_ADDR           = 0x14
PROFILE7_ADDR           = 0x15
RAM_ADDR                = 0x16

class AD9910:
    def __init__(self, fpga, min_freq = 10, max_freq = 400, sys_clk = 1000, 
                 unit = 'MHz'):                        
        #default min_freq, max_freq should be checked.
        """
        fpga        : ArtyS7
        max_freq    : maximum output frequency of DDS
        min_freq    : minimum output frequency of DDS
        sys_clk     : REF_CLK of DDS
        
        in this version we assum not using PLL in DDS. after this version 
        parameter about PLL will be added
        """
        self.fpga = fpga
        if(unit == 'Hz' or unit == 'hz'):
            self.max_freq = max_freq
            self.min_freq = min_freq
            self.sys_clk = sys_clk
            
        elif(unit == 'kHz' or unit == 'KHz' or unit == 'Khz' or unit == 'khz'):
            self.max_freq = max_freq * (10**3)
            self.min_freq = min_freq * (10**3)
            self.sys_clk = sys_clk * (10**3)
            
        elif(unit == 'mHz' or unit == 'MHz' or unit == 'Mhz' or unit == 'mhz'):
            self.max_freq = max_freq * (10**6)
            self.min_freq = min_freq * (10**6)
            self.sys_clk = sys_clk * (10**6)
            
        elif(unit == 'gHz' or unit == 'GHz' or unit == 'Ghz' or unit == 'ghz'):
            self.max_freq = max_freq * (10**9)
            self.min_freq = min_freq * (10**9)
            self.sys_clk = sys_clk * (10**9)
        else:
            print('Error in AD9912 constructor: not suitable unit (%s).'\
                  % unit, 'unit should be \'Hz\', \'kHz\', \'MHz\', \'GHz\'')
        
    def make_header_string(self, register_address, direction = 'W'):
        #AD9910 has fixed transfer length, so 'bytes_length' was deleted
        if direction == 'W':
            MSB = 0
        elif direction == 'R':
            MSB = 1
        else:
            print('Error ion make_header: unknown direction (%s).'%direction,\
                  'direction should be either \'W\' or \'R\'.')
            raise ValueError()
        
        if type(register_address) == str:
            address = int(register_address, 16)
        elif type(register_address) == int:
            address = register_address
        else:
            print('Error in make_header: unknown register address type (%s).' \
                  % type(register_address),'register_address should be either'\
                  ,'hexadecimal string or integer')
            raise ValueError()
        
        DONTCARE = 0
        
        print(MSB, DONTCARE, address)
        header_value = (MSB << 7) + (DONTCARE << 5) + address
        return ('%02X' % header_value)
    
    def frequency_to_FTW(self, freq, unit = 'MHz'):
        """
        makes frequency to FTW of DDS. Not need to consider sys_clk.
        Note that FTW is 32 bits in AD9910
        """
        if(unit == 'Hz' or unit == 'hz'):
            FTW = int((2**32)*(freq/(self.sys_clk*(10**0))))
        elif(unit == 'kHz' or unit == 'KHz' or unit == 'Khz' or unit == 'khz'):
            FTW = int((2**32)*(freq/(self.sys_clk*(10**3))))
        elif(unit == 'mHz' or unit == 'MHz' or unit == 'Mhz' or unit == 'mhz'):
            FTW = int((2**32)*(freq/(self.sys_clk*(10**6))))
        elif(unit == 'gHz' or unit == 'GHz' or unit == 'Ghz' or unit == 'ghz'):
            FTW = int((2**32)*(freq/(self.sys_clk*(10**9))))
        else:
            print('Error in frequency_to_FTW: not suitable unit (%s).'\
                  % unit, 'unit should be \'Hz\', \'kHz\', \'MHz\', \'GHz\'')
        return FTW
    
    def write64(self, register_addr, register_data):
        self.fpga.send_mod_BTF_int_list()
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list()
        self.fpga.send_command('WRITE DDS REG')
        
    def set_frequency(self, freq, unit = 'MHz'):
        """
        freq        : frequency user want to set
        unit        : unit of frequency. default is MHz
        """
        if (unit == 'Hz' or unit == 'hz'):
            freq_in_Hz = freq
            
        elif(unit == 'kHz' or unit == 'KHz' or unit == 'Khz' or unit == 'khz'):
            freq_in_Hz = freq * (10**3)
            
        elif(unit == 'mHz' or unit == 'MHz' or unit == 'Mhz' or unit == 'mhz'):
            freq_in_Hz = freq * (10**6)
            
        elif(unit == 'gHz' or unit == 'GHz' or unit == 'Ghz' or unit == 'ghz'):
            freq_in_Hz = freq * (10**9) 
            
        else:
            print('Error in set_frequency: not suitable unit (%s).'\
                  % unit, 'unit should be \'Hz\', \'kHz\', \'MHz\', \'GHz\'')
                
        if( freq_in_Hz < self.min_freq or freq_in_Hz > self.max_freq ):
            print('Error in set_frequency: frequency should be between %d'\
                  'and %d' % (self.min_freq, self.max_freq))
            raise ValueError(freq_in_Hz)
        self.write64(FTW_ADDR, self.frequency_to_FTW)

if __name__ == "__main__":
    dds = AD9910(None)
    print(dds.make_header_string(0x11, direction = 'R'))