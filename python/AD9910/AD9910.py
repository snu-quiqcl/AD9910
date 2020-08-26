# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:08:40 2020

@author: JeonghyunPark
"""

from Arty_S7_v1_01 import ArtyS7
#This ArtyS7 is in the AD9912 folder
from unit_set import *

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

DEFAULT_CFR1            = (1 << 16) 
DEFAULT_CFR2            = ( ( 1 << 24 ) 
                        | ( 1 << 16 ) 
                        | ( 1 << 5 ) )
DEFAULT_CFR3            = ( ( 1 << 27)
                        | ( 7 << 16 )
                        | ( 1 << 15 )
                        | ( 1 << 14 ) )

DEST_SPI_DATA           = 0x00
DEST_SPI_CONFIG         = 0x01
DEST_DDS_IO_UPDATE      = 0x02
DEST_DDS_PROFILE        = 0x03
DEST_DDS_PARALLEL       = 0x04

CHANNEL_LENGTH          = 12

SPI_CONFIG_WRITE        = ( ( 0 << 31 ) \
                        | ( 0 << 30 ) \
                        | ( 0 << 29 ) \
                        | ( 0b00000000 << 16 ) \
                        | ( 16 << 0 ) )
SPI_CONFIG_READ         = ( ( 0 << 31 ) \
                        | ( 1 << 30 ) \
                        | ( 0 << 29 ) \
                        | ( 0b00000000 << 16 ) \
                        | ( 16 << 0 ) )
                        
"""
SPI CONFIG
31      lsb_first
30      slave_en
29      end_spi
28:24   dummy
23:16   cs
15:11   length
10      cspol
9       cpol
8       cpha
7:0     clk_div

GENERAL INST
127:112 dummy
111:108 dest (functionality)
107:96  dest (channel value)
95:32   timestamp
31:0    data
"""

class AD9910:
    def __init__(self, fpga, min_freq = 10 * MHz, max_freq = 400 * MHz, sys_clk = 1000 * MHz, 
                 dest_val = 1, auto_en = False):                        
        #default min_freq, max_freq should be checked.
        """
        fpga            : ArtyS7
        max_freq        : maximum output frequency of DDS
        min_freq        : minimum output frequency of DDS
        sys_clk         : REF_CLK of DDS
        
        in this version we assum not using PLL in DDS. after this version 
        parameter about PLL will be added
        """
        self.fpga = fpga
        self.auto_en = auto_en
        self.dest_val = dest_val
        self.code_list = []
        self.time = 0
        self.fm_gain = 0
        self.spi_config = 0
        self.spi_config_int_list = self.set_config()
        self.cfr1 = [DEFAULT_CFR1, DEFAULT_CFR1]
        self.cfr2 = [DEFAULT_CFR2, DEFAULT_CFR2]
        self.cfr3 = [DEFAULT_CFR3, DEFAULT_CFR3]
        self.max_freq = max_freq
        self.min_freq = min_freq
        self.sys_clk = sys_clk
        self.write_32_duration = 1000
        self.write_64_duration = 4000
        self.read_32_duration  = 1000
        self.read_64_duration  = 4000
        
        
    def make_8_int_list(self, data):
        int_list = []
        int_list.append( ( data >> 56 ) & 0xff )
        int_list.append( ( data >> 48 ) & 0xff )
        int_list.append( ( data >> 40 ) & 0xff )
        int_list.append( ( data >> 32 ) & 0xff )
        int_list.append( ( data >> 24 ) & 0xff )
        int_list.append( ( data >> 16 ) & 0xff )
        int_list.append( ( data >> 8  ) & 0xff )
        int_list.append( ( data >> 0  ) & 0xff )
        
        return int_list
    
    def convert_to_16_int_list(self, data_list):
        if( len(data_list) != 8 ):
            print('Error in covert_to_17_int_list : length of data_list'\
                  ' should be 8')
            raise ValueError(data_list)
        
        int_list = []
        int_list.append(data_list[0])
        int_list.append(data_list[1])
        int_list.append(data_list[2])
        int_list.append(data_list[3])
        
        int_list.append( ( self.time >> 56 ) & 0xff )
        int_list.append( ( self.time >> 48 ) & 0xff )
        int_list.append( ( self.time >> 40 ) & 0xff )
        int_list.append( ( self.time >> 32 ) & 0xff )
        int_list.append( ( self.time >> 24 ) & 0xff )
        int_list.append( ( self.time >> 16 ) & 0xff )
        int_list.append( ( self.time >> 8  ) & 0xff )
        int_list.append( ( self.time >> 0  ) & 0xff )
        
        int_list.append(data_list[4])
        int_list.append(data_list[5])
        int_list.append(data_list[6])
        int_list.append(data_list[7])
        
        print(int_list)
        
        return int_list
    
    def read_int_list(self, length = 65):
        int_list = []
        next_val = 0
        for i in range(length):
            next_val = self.fpga.read_next()
            int_list.append(int.from_bytes(next_val.encode('latin-1'),'little'))
        
        return int_list
    
    def read_17_int_list(self):
        int_list = []
        next_val = 0
        for i in range(17):
            next_val = self.fpga.read_next()
            int_list.append(int.from_bytes(next_val.encode('latin-1'),'little'))
        
        return int_list
        
    def delay_cycle(self, shift_cycle):
        if(str(type(shift_cycle)) != '<class \'int\'>'):
            print('Error in delay_cycle : shift_cycle unit should be \'int\'')
            raise TypeError(shift_cycle)
            
        self.time = self.time + shift_cycle
    
    def delay(self, shift_second):
        self.time = self.time + int( shift_second * ( 100000000 ) )
    
    def set_config(self, cs = 0, length = 8, end_spi = 0, slave_en = 0, 
                   lsb_first = 0, dummy = 0, cspol = 0, cpol = 0, cpha = 0, 
                   clk_div = 16):
        config = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | ( lsb_first << 31 ) \
                        | ( slave_en << 30 ) \
                        | ( end_spi << 29 ) \
                        | ( dummy << 24 ) \
                        | ( cs << 16 ) \
                        | ( ( length - 1 ) << 11 ) \
                        | ( cspol << 10 ) \
                        | ( cpol << 9 ) \
                        | ( cpha << 8 ) \
                        | ( clk_div << 0 ) )
            
        config_int_list = self.make_8_int_list(config)
        self.spi_config = config
        self.spi_config_int_list = config_int_list
        return config_int_list
    
    def make_write_list(self, data, length = 8):
        data_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | ( data & 0xffffffff ) )
        data_int_list = self.make_8_int_list(data_to_send)
        return data_int_list
    
    def write(self, ch1, ch2, register_addr, register_data_list, last_length):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 16.
        """
        delayed_cycle = 0
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        
        addr_int_list = self.make_write_list(register_addr << 24)
        
        if( self.auto_en ):
            fifo_config_int_list1 = self.convert_to_16_int_list(config_int_list1)
            self.delay_cycle(1)
            
            fifo_addr_int_list = self.convert_to_16_int_list(addr_int_list)
            self.delay_cycle(self.write_32_duration)
            
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_addr_int_list)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += ( 1 + self.write_32_duration )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
        
        for i in range(len(register_data_list) - 1):
            if ( i == 0 ):
                config_int_list2 = self.set_config( cs =((ch2 << 1)|(ch1 << 0)), 
                                                   length = 32)
                if( self.auto_en ):
                    fifo_config_int_list2 = self.convert_to_16_int_list(config_int_list2)
                    self.delay_cycle(1)
                    
                    self.fpga.send_mod_BTF_int_list(fifo_config_int_list2)
                    self.fpga.send_command('WRITE FIFO')
                    
                    delayed_cycle += 1
                else:
                    self.fpga.send_mod_BTF_int_list(config_int_list2)
                    self.fpga.send_command('WRITE FIFO')
                
            data_int_list = self.make_write_list(register_data_list[i])
            if( self.auto_en ):
                fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
                self.delay_cycle(self.write_32_duration)
                
                self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
                self.fpga.send_command('WRITE FIFO')
                
                delayed_cycle += self.write_32_duration
            else:
                self.fpga.send_mod_BTF_int_list(data_int_list)
                self.fpga.send_command('WRITE DDS REG')
        
        config_int_list3 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = last_length,
                                           end_spi = 1 )
        
        last_int_list = self.make_write_list(register_data_list[-1] << ( 32 - last_length ) )
        
        if( self.auto_en ):
            fifo_config_int_list3 = self.convert_to_16_int_list(config_int_list3)
            self.delay_cycle(1)
            
            fifo_last_int_list = self.convert_to_16_int_list(last_int_list)
            self.delay_cycle(self.write_32_duration)
            
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list3)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_last_int_list)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += ( 1 + self.write_32_duration )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list3)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(last_int_list)
            self.fpga.send_command('WRITE DDS REG')
        
        self.delay_cycle(-delayed_cycle)
        
    def write32(self, ch1, ch2, register_addr, register_data):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        delayed_cycle = 0
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1 )
        data_int_list = self.make_write_list(register_data)
        
        if( self.auto_en ):
            fifo_config_int_list1 = self.convert_to_16_int_list(config_int_list1)
            self.delay_cycle(1)
            
            fifo_addr_int_list = self.convert_to_16_int_list(addr_int_list)
            self.delay_cycle(self.write_32_duration)
            
            fifo_config_int_list2 = self.convert_to_16_int_list(config_int_list2)
            self.delay_cycle(1)
            
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.delay_cycle(self.write_32_duration)
            
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_addr_int_list)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list2)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += 2 * ( self.write_32_duration + 1 )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
        
        self.delay_cycle(-delayed_cycle)
    
    def write64(self, ch1, ch2, register_addr, register_data):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        delayed_cycle = 0
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32 )
        data_int_list1 = self.make_write_list(register_data >> 32)
        config_int_list3 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1 )
        data_int_list2 = self.make_write_list(register_data)
        
        if( self.auto_en ):
            fifo_config_int_list1 = self.convert_to_16_int_list(config_int_list1)
            self.delay_cycle(1)
            
            fifo_addr_int_list = self.convert_to_16_int_list(addr_int_list)
            self.delay_cycle(self.write_32_duration)
            
            fifo_config_int_list2 = self.convert_to_16_int_list(config_int_list2)
            self.delay_cycle(1)
            
            fifo_data_int_list1 = self.convert_to_16_int_list(data_int_list1)
            self.delay_cycle(self.write_32_duration)
            
            fifo_config_int_list3 = self.convert_to_16_int_list(config_int_list3)
            self.delay_cycle(1)
            
            fifo_data_int_list2 = self.convert_to_16_int_list(data_int_list2)
            self.delay_cycle(self.write_32_duration)
            
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_addr_int_list)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list2)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list3)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list2)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += 3*( self.write_32_duration + 1 )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list3)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            
        self.delay_cycle(-delayed_cycle)
        
    def read32(self, ch1, ch2, register_addr):
        """
        register_addr   : address of register in DDS. this is int type.
        """
        delayed_cycle = 0
        if( ch1 == ch2 ):
            print('Error in read32 : only one channel should be selected or'\
                  'not selected')
            raise ValueError( bin( ch2 << 1 | ch1 ) )
        
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8, end_spi = 0, 
                                           slave_en = 0 )
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1,
                                           slave_en = 1 )
        data_int_list = self.make_write_list(0)
        
        if( self.auto_en ):
            fifo_config_int_list1 = self.convert_to_16_int_list(config_int_list1)
            self.delay_cycle(1)
            fifo_addr_int_list = self.convert_to_16_int_list(addr_int_list)
            self.delay_cycle(self.read_32_duration)
            fifo_config_int_list2 = self.convert_to_16_int_list(config_int_list2)
            self.delay_cycle(1)
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.delay_cycle(self.read_32_duration)
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_addr_int_list)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list2)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += 2 * ( self.read_32_duration + 1 )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
            
        self.delay_cycle(-delayed_cycle)
        
    def read64(self, ch1, ch2, register_addr, end_spi = 1):
        """
        register_addr   : address of register in DDS. this is int type.
        """
        delayed_cycle = 0
        if( ch1 == ch2 ):
            print('Error in read32 : only one channel should be selected or'\
                  'not selected')
            raise ValueError( bin( ch2 << 1 | ch1 ) )
        
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 0, 
                                           slave_en = 1 )
        data_int_list = self.make_write_list(0)
        config_int_list3 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1,
                                           slave_en = 1 )
        data_int_list = self.make_write_list(0)
        
        if( self.auto_en ):
            fifo_config_int_list1 = self.convert_to_16_int_list(config_int_list1)
            self.delay_cycle(1)
            fifo_addr_int_list = self.convert_to_16_int_list(addr_int_list)
            self.delay_cycle(self.read_32_duration)
            fifo_config_int_list2 = self.convert_to_16_int_list(config_int_list2)
            self.delay_cycle(1)
            fifo_data_int_list1 = self.convert_to_16_int_list(data_int_list)
            self.delay_cycle(self.read_32_duration)
            fifo_config_int_list3 = self.convert_to_16_int_list(config_int_list3)
            self.delay_cycle(1)
            fifo_data_int_list2 = self.convert_to_16_int_list(data_int_list)
            self.delay_cycle(self.read_32_duration)
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_addr_int_list)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list2)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list1)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_config_int_list3)
            self.fpga.send_command('WRITE FIFO')
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list2)
            self.fpga.send_command('WRITE FIFO')
            
            delayed_cycle += 3 * ( self.read_32_duration + 1 )
        else:
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list3)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
            
        self.delay_cycle(-delayed_cycle)
    
    def frequency_to_FTW(self, freq):
        """
        makes frequency to FTW of DDS. Not need to consider sys_clk.
        Note that FTW is 32 bits in AD9910
        """
        FTW = int((2**32)*(freq*(10**0)/(self.sys_clk))) & 0xffffffff
        
        return FTW
    
    def phase_to_POW(self, phase):
        """
        notice that defulat unit is radian
        """
        POW = int( phase * (2**16) / (2*PI) ) & 0xffff
        
        return POW
    
    def amplitude_to_ASF(self, amplitude_frac):
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
                
        ASF = int( amplitude_frac * ( 0x3fff ) ) & 0x3fff
        
        return ASF
        
    def set_frequency(self, ch1, ch2, freq):
        """
        freq            : frequency user want to set
        unit            : unit of frequency. default is MHz
        """
        freq_in_Hz = freq  
        
        self.write32(FTW_ADDR, self.frequency_to_FTW(freq_in_Hz, unit = 'Hz'), 
                     ch1, ch2)
        
    def set_phase(self, ch1, ch2, phase):
        """
        phase           : phase user want to set
        unit            : unit of phase. defualt is fraction of 2 pi
        """
        self.write16(POW_ADDR, self.phase_to_POW(phase),ch1, ch2)
        
    def set_amplitude(self, ch1, ch2, amplitude_frac):
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
                
        self.write32(ASF_ADDR, ( self.amplitude_to_ASF(amplitude_frac) << 2 ), 
                     ch1, ch2)
        
    def initialize(self, ch1, ch2):
        delayed_cycle = 0
        self.set_CFR1(ch1,ch2)
        if self.auto_en == True: 
            self.delay_cycle(self.write_64_duration)
            delayed_cycle += self.write_64_duration
        self.set_CFR2(ch1,ch2)
        if self.auto_en == True: 
            self.delay_cycle(self.write_64_duration)
            delayed_cycle += self.write_64_duration
        self.set_CFR3(ch1,ch2)
        if self.auto_en == True: 
            self.delay_cycle(self.write_64_duration)
            delayed_cycle += self.write_64_duration
        self.delay_cycle(-delayed_cycle)
        
    def set_CFR1(self, ch1, ch2, ram_en = 0, ram_playback = 0, manual_OSK = 0, 
                 inverse_sinc_filter = 0, internal_porfile = 0, sine = 1,
                 load_LRR = 0, autoclear_DRG = 0, autoclear_phase = 0, 
                 clear_DRG = 0, clear_phase = 0, load_ARR = 0, OSK_en = 0,
                 auto_OSK = 0, digital_power_down = 0, DAC_power_down = 0, 
                 REFCLK_powerdown = 0, aux_DAC_powerdown = 0, 
                 external_power_down_ctrl = 0, SDIO_in_only = 0, 
                 LSB_first = 0):
        CFR1_setting = ( 
            ( ram_en << 31 ) 
            | (ram_playback << 29)  
            | (manual_OSK << 23 ) 
            | (inverse_sinc_filter << 22) 
            | (internal_porfile << 17) 
            | (sine << 16) 
            | (load_LRR << 15) 
            | (autoclear_DRG << 14) 
            | (autoclear_phase << 13) 
            | (clear_DRG << 12) 
            | (clear_phase << 11) 
            | (load_ARR << 10) 
            | (OSK_en << 9) 
            | (auto_OSK << 8) 
            | (digital_power_down << 7) 
            | (DAC_power_down << 6) 
            | (REFCLK_powerdown << 5) 
            | (aux_DAC_powerdown << 4) 
            | (external_power_down_ctrl << 3) 
            | (SDIO_in_only << 1) 
            | (LSB_first << 0) )
        if( ch1 == 1 ):
            self.cfr1[0] = CFR1_setting
        if( ch2 == 1 ):
            self.cfr1[1] = CFR1_setting
        self.write32(ch1, ch2, CFR1_ADDR, CFR1_setting)
        
    def set_CFR2(self, ch1, ch2, amp_en_single_tone = 1, internal_IO_update = 0, 
                 SYNC_CLK_en = 0, DRG_dest = 0, DRG_en = 0, 
                 DRG_no_dwell_high = 0, DRG_no_dwell_low = 0, read_eff_FTW = 1, 
                 IO_update_rate = 0, PDCLK_en = 0, PDCLK_inv = 0, Tx_inv = 0, 
                 matched_latency_en = 0, data_ass_hold = 0, sync_val_dis = 1, 
                 parallel_port = 0, FM_gain = 0):
        CFR2_setting = ( 
            ( amp_en_single_tone << 24 ) 
            | ( internal_IO_update << 23 ) 
            | ( SYNC_CLK_en << 22 ) 
            | ( DRG_dest << 20 ) 
            | ( DRG_en << 19 ) 
            | ( DRG_no_dwell_high << 18 ) 
            | ( DRG_no_dwell_low << 17 ) 
            | ( read_eff_FTW << 16 ) 
            | ( IO_update_rate << 14 ) 
            | ( PDCLK_en << 11 ) 
            | ( PDCLK_inv << 10 ) 
            | ( Tx_inv << 9 ) 
            | ( matched_latency_en << 7 ) 
            | ( data_ass_hold << 6 ) 
            | ( sync_val_dis << 5 ) 
            | ( parallel_port << 4 ) 
            | ( FM_gain << 0 ) )
        
        if( ch1 == 1 ):
            self.cfr2[0] = CFR2_setting
        if( ch2 == 1 ):
            self.cfr2[1] = CFR2_setting
        self.write32(ch1, ch2, CFR2_ADDR, CFR2_setting)
        
    def set_CFR3(self, ch1, ch2, DRV0 = 0, PLL_VCO = 0, I_CP = 0, 
                 REFCLK_div_bypass = 1, REFCLK_input_div_reset = 1, 
                 PFD_reset = 0, PLL_en = 0, N = 0):
        CFR3_setting = (
            ( DRV0 << 28 )
            | ( 1 << 27)
            | ( PLL_VCO << 24 )
            | ( I_CP << 19 )
            | ( 7 << 16 )
            | ( REFCLK_div_bypass << 15 )
            | ( REFCLK_input_div_reset << 14 )
            | ( PFD_reset << 10 )
            | ( PLL_en << 8 )
            | ( N << 1 ) )
        
        if( ch1 == 1 ):
            self.cfr3[0] = CFR3_setting
        if( ch2 == 1 ):
            self.cfr3[1] = CFR3_setting
        self.write32(ch1, ch2, CFR3_ADDR, CFR3_setting)
    
    def set_profile_register(self, ch1, ch2, freq, phase, amplitude, 
                             profile = 0 ):
        freq_in_Hz = freq
                
        if( freq_in_Hz < self.min_freq or freq_in_Hz > self.max_freq ):
            print('Error in set_frequency: frequency should be between %d'\
                  'and %d' % (self.min_freq, self.max_freq))
                
        phase_in_rad = phase
            
        FTW = self.frequency_to_FTW(freq_in_Hz)
        POW = self.phase_to_POW(phase_in_rad)
        ASF = self.amplitude_to_ASF(amplitude)
        data = ( ASF << 48 ) | ( POW << 32 ) | ( FTW << 0 )
        self.write64(ch1, ch2, PROFILE0_ADDR + profile, data)
        
    def set_profile_pin(self, profile1, profile2):
        data_to_send = 0
        data_to_send = ( ( DEST_DDS_PROFILE << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( profile1 & 0b111  ) \
                        | ( ( profile2 << 3 ) & 0b111000 ) )
        data_int_list = self.make_8_int_list(data_to_send)
        
        if( self.auto_en ):
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('SET DDS PIN')
            
    def bits_to_represent(self, num):
        val = num
        count = 0
        while(val > 0):
            count = count + 1
            val = val >> 1
            
        return count
    
    def set_fm_gain(self, fm_gain):
        self.fm_gain = fm_gain & 0xf
        self.cfr1[0] = self.cfr1[0] - ( self.cfr1[0] & 0xf )
        self.cfr1[0] = self.cfr1[0] + fm_gain & 0xf
        self.write32(1, 0, CFR1_ADDR, self.cfr1[0])
    
    def minimum_fm_gain(self, frequency):
        return max(min(self.bits_to_represent(\
                        self.frequency_to_FTW(frequency)) - 16, 15),0)
    
    def set_parallel_frequency(self, frequency, set_fm_gain = True, \
                               parallel_en = 1):
        """
        frequency : frequency to set
        set_fm_gain : whether to set fm_gain dynamically 
        parallel_en : whether to set TxEnable high
        """
        
        data_to_send = 0
        delayed_cycle = 0
        
        fm_gain = self.minimum_fm_gain(frequency)
        
        FTW_16bit = int(self.frequency_to_FTW(frequency) // \
                        ( 2 ** fm_gain ))
        
        if( fm_gain != self.fm_gain and set_fm_gain == True ):
            self.set_fm_gain(fm_gain)
            self.delay_cycle(self.write_32_duration)
            delayed_cycle += self.write_32_duration
        
        data_to_send = ( ( DEST_DDS_PARALLEL << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( parallel_en << 18  ) \
                        | ( 0b10 << 16 ) \
                        | ( FTW_16bit & 0xffff ))
        data_int_list = self.make_8_int_list(data_to_send)
        
        if( self.auto_en ):
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('SET DDS PIN')
            
        self.delay_cycle(-delayed_cycle)
        
    def set_parallel_amplitude(self, amplitude, parallel_en = 1):
        """
        amplitude : frequency to set
        parallel_en : whether to set TxEnable high
        """
        
        data_to_send = 0
        
        ASF_14bit = self.amplitude_to_ASF(amplitude)
            
        data_to_send = ( ( DEST_DDS_PARALLEL << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( parallel_en << 18  ) \
                        | ( 0b00 << 16 ) \
                        | ( ( ASF_14bit & 0x3fff ) << 2 ) )
        data_int_list = self.make_8_int_list(data_to_send)
        
        if( self.auto_en ):
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('SET DDS PIN')
    
    def set_parallel_phase(self, phase, parallel_en = 1):
        """
        phase : phase to set
        parallel_en : whether to set TxEnable high
        """
        
        data_to_send = 0
        
        POW_16bit = self.phase_to_POW(phase)
            
        data_to_send = ( ( DEST_DDS_PARALLEL << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( parallel_en << 18  ) \
                        | ( 0b01 << 16 ) \
                        | ( POW_16bit & 0xffff ))
        data_int_list = self.make_8_int_list(data_to_send)
        
        if( self.auto_en ):
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('SET DDS PIN')
    
    def set_parallel_phasor(self, amplitude, phase, set_amplitude_lsb = False,\
                            set_phase_lsb = False, parallel_en = 1):
        """
        amplitude : amplitude to set
        phase : phase to set
        set_amplitude_lsb : whether to set amplitude lsb using ASF register
        set_phase_lsb : whether to set phase lsb using POW register
        parallel_en : whether to set TxEnable high
        """
        
        data_to_send = 0
        delayed_cycle = 0
        
        ASF = self.amplitude_to_ASF(amplitude)
        ASF_8bit = ( ASF >> 6 ) & 0xff
        
        POW = self.phase_to_POW(phase)
        POW_8bit = ( POW >> 8 ) & 0xff
        
        if( set_amplitude_lsb == True ):
            self.set_amplitude(1, 0, amplitude)
            self.delay_cycle(2000)
            delayed_cycle += 2000
        if( set_phase_lsb == True):
            self.set_phase(1, 0, phase)
            self.delay_cycle(2000)
            delayed_cycle += 2000
            
        data_to_send = ( ( DEST_DDS_PARALLEL << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( parallel_en << 18  ) \
                        | ( 0b11 << 16 ) \
                        | ( ASF_8bit << 8 ) \
                        | ( POW_8bit ) )
        data_int_list = self.make_8_int_list(data_to_send)
        
        if( self.auto_en ):
            fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('SET DDS PIN')
            
        self.delay_cycle(-delayed_cycle)
    
    def io_update(self, ch1, ch2):
        delayed_cycle = 0
        data_to_send1 = 0
        data_to_send1 = ( ( DEST_DDS_IO_UPDATE << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( ( ch2 & 0b1 ) << 1 ) \
                        | ( ch1 & 0b1 ) )
        data_int_list1 = self.make_8_int_list(data_to_send1)
        
        data_to_send2 = 0
        data_to_send2 = ( ( DEST_DDS_IO_UPDATE << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( ( 0 ) << 1 ) \
                        | ( 0 ) )
        data_int_list2 = self.make_8_int_list(data_to_send2)
        
        if( self.auto_en ):
            fifo_data_int_list1 = self.convert_to_16_int_list(data_int_list1)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list1)
            self.fpga.send_command('WRITE FIFO')
            
            self.delay_cycle(5)
            delayed_cycle += 5
            
            fifo_data_int_list2 = self.convert_to_16_int_list(data_int_list2)
            self.fpga.send_mod_BTF_int_list(fifo_data_int_list2)
            self.fpga.send_command('WRITE FIFO')
        else:
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('DDS IO UPDATE')
        
        self.delay_cycle(-delayed_cycle)
    
    def auto_mode(self):
        self.auto_en = True
        
    def auto_mode_disable(self):
        self.auto_en = False
    
    def auto_start(self):
        self.fpga.send_command('AUTO START')
        
    def auto_stop(self):
        self.fpga.send_command('AUTO STOP')
        
    def write_fifo(self, data):
        data_to_send = ( data & 0xffffffffffffffff )
        data_int_list = self.make_8_int_list(data_to_send)
        fifo_data_int_list = self.convert_to_16_int_list(data_int_list)
        self.fpga.send_mod_BTF_int_list(fifo_data_int_list)
        self.fpga.send_command('WRITE FIFO')
    
    def read_rti_fifo(self):
        self.fpga.send_command('READ RTI FIFO')
        
    def set_counter(self, counter_offset):
        data_to_send = ( counter_offset & 0xffffffffffffffff )
        data_int_list = self.make_8_int_list(data_to_send)
        self.fpga.send_mod_BTF_int_list(data_int_list)
        self.fpga.send_command('SET COUNTER')
    
    def override_enable(self):
        self.fpga.send_command('OVERRIDE EN')
        
    def override_disable(self):
        self.fpga.send_command('OVERRIDE DIS')
        
    def now(self):
        return self.time
    
    def set_now_cycle(self, time):
        self.time = time
    
    def reset_driver(self):
        self.fpga.send_command('RESET DRIVER')
    
    def read_exception_log(self):
        self.fpga.send_command('EXCEPTION LOG')
        
    def ram_write(self, ch1, ch2, data_list):
        self.write(ch1, ch2, RAM_ADDR, data_list, 32)
    
    def set_ram_profile_register(self,ch1, ch2, addr_step_rate, end_addr, 
                                 start_addr, no_dwell_high, zero_crossing, 
                                 ram_mode_ctrl, profile):
        data_to_send = ( ( ( addr_step_rate & 0xffff ) << 40 ) \
                        | ( ( end_addr & 0x3ff ) << 30 ) \
                        | ( ( start_addr & 0x3ff ) << 14 ) \
                        | ( ( no_dwell_high & 0x1 ) << 5 ) \
                        | ( ( zero_crossing & 0x1 ) << 3 ) \
                        | ( ( ram_mode_ctrl & 0x7 ) << 0 ) )
        self.write64(ch1, ch2, PROFILE0_ADDR + profile, data_to_send)
        

if __name__ == "__main__":
    dds = AD9910(ArtyS7(None))
    #dds.io_update(1,1)
    dds.auto_en = True
    dds.io_update(1,1)
    dds.set_profile_pin(1,1)
    dds.set_profile_register(1,1,100*MHz,0*RAD,1.0,0)
    dds.fpga.close()