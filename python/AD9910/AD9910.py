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

PI                      = 3.1415926535897931

DEST_SPI_DATA           = 0x00
DEST_SPI_CONFIG         = 0x01
DEST_DDS_IO_UPDATE      = 0x02
DEST_DDS_PROFILE        = 0x03
DEST_DDS_PARALLEL       = 0x04

CHANNEL_LENGTH          = 12

TEST                    = 1

SPI_CONFIG_WRITE        = 0 << 31 \
                        | 0 << 30 \
                        | 0 << 29 \
                        | 0b00000000 << 16 \
                        | 16 << 0
SPI_CONFIG_READ         = 0 << 31 \
                        | 1 << 30 \
                        | 0 << 29 \
                        | 0b00000000 << 16 \
                        | 16 << 0
                        
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
    def __init__(self, fpga, min_freq = 10, max_freq = 400, sys_clk = 1000, 
                 unit = 'MHz', dest_val = 1, auto_en = False):                        
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
        self.spi_config_write = SPI_CONFIG_WRITE
        self.spi_config_read = SPI_CONFIG_READ
        
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
    def make_9_int_list(self, data):
        int_list = [ 8 ]
        int_list.append( ( data // (2 ** 56)) & 0xff )
        int_list.append( ( data // (2 ** 48)) & 0xff )
        int_list.append( ( data // (2 ** 40)) & 0xff )
        int_list.append( ( data // (2 ** 32)) & 0xff )
        int_list.append( ( data // (2 ** 24)) & 0xff )
        int_list.append( ( data // (2 ** 16)) & 0xff )
        int_list.append( ( data // (2 ** 8)) & 0xff )
        int_list.append( ( data // (2 ** 0)) & 0xff )
        
        return int_list
    
    def delay(self, shift_time, unit = 'ns'):
        if( unit == 'ns' ):
            self.time = self.time + (shift_time // 10)
        elif(unit == 'mu' or unit == 'Mu' or unit == 'mU' or unit == 'MU'):
            self.time = self.time + shift_time
        else:
            print('Error in delay: not suitable unit (%s). unit should be' \
                  '\'ns\',\'mu\'' % unit)
            raise ValueError(shift_time)
    
    def write16(self, register_addr, register_data, ch1, ch2, end_spi = 1):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 16.
        """
        config_to_send1 = 0
        config_to_send1 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | end_spi << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 7 << 11)
        addr_to_send = 0
        addr_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | register_addr )
        config_to_send2 = 0
        config_to_send2 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | end_spi << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 15 << 11)
        data_to_send = 0
        data_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | register_data )
        
        config_int_list1 = self.make_9_int_list(config_to_send1)
        addr_int_list = self.make_9_int_list(addr_to_send)
        config_int_list2 = self.make_9_int_list(config_to_send2)
        data_int_list = self.make_9_int_list(data_to_send)
        
        if(TEST != 1):
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
        else:
            print('config1 to send')
            for i in range(config_int_list1):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('addr to send')
            for i in range(addr_int_list):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('config2 to send')
            for i in range(config_int_list2):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('data to send')
            for i in range(data_int_list):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
            
            print('')
    
    def write32(self, register_addr, register_data, ch1, ch2, end_spi):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        config_to_send1 = 0
        config_to_send1 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | end_spi << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 7 << 11)
        addr_to_send = 0
        addr_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | register_addr )
        config_to_send2 = 0
        config_to_send2 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | end_spi << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 31 << 11)
        data_to_send = 0
        data_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | register_data )
        
        config_int_list1 = self.make_9_int_list(config_to_send1)
        addr_int_list = self.make_9_int_list(addr_to_send)
        config_int_list2 = self.make_9_int_list(config_to_send2)
        data_int_list = self.make_9_int_list(data_to_send)
        
        if(TEST != 1):
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
        else:
            print('config1 to send')
            for i in range(config_int_list1):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('addr to send')
            for i in range(addr_int_list):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('config2 to send')
            for i in range(config_int_list2):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('data to send')
            for i in range(data_int_list):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
            
            print('')
    
    def write64(self, register_addr, register_data, ch1, ch2, end_spi = 1):
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        config_to_send1 = 0
        config_to_send1 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | 0 << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 7 << 11)
        addr_to_send = 0
        addr_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | register_addr )
        config_to_send2 = 0
        config_to_send2 = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | self.config_write \
                        | end_spi << 29 \
                        | ( ch1 << 16 ) \
                        | ( ch2 << 17 ) \
                        | 15 << 11)
        data_to_send1 = 0
        data_to_send1 = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | ( ( register_data // ( 2 ** 32 )) & 0xff  ) )
        data_to_send2 = 0
        data_to_send2 = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( register_data & 0xff  ) )
        
        config_int_list1 = self.make_9_int_list(config_to_send1)
        addr_int_list = self.make_9_int_list(addr_to_send)
        config_int_list2 = self.make_9_int_list(config_to_send2)
        data_int_list1 = self.make_9_int_list(data_to_send1)
        data_int_list2 = self.make_9_int_list(data_to_send2)
        
        if(TEST != 1):
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(addr_int_list)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(config_int_list2)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list1)
            self.fpga.send_command('WRITE DDS REG')
            self.fpga.send_mod_BTF_int_list(data_int_list2)
            self.fpga.send_command('WRITE DDS REG')
        else:
            print('config1 to send')
            for i in range(config_int_list1):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('addr to send')
            for i in range(addr_int_list):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('config2 to send')
            for i in range(config_int_list2):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
            
            print('data to send')
            for i in range(data_int_list1):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
            
            print('')
            
            print('data to send')
            for i in range(data_int_list2):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
            
            print('')
        
    
    def frequency_to_FTW(self, freq, unit = 'MHz'):
        """
        makes frequency to FTW of DDS. Not need to consider sys_clk.
        Note that FTW is 32 bits in AD9910
        """
        if(unit == 'Hz' or unit == 'hz'):
            FTW = int((2**32)*(freq*(10**0)/(self.sys_clk)))
        elif(unit == 'kHz' or unit == 'KHz' or unit == 'Khz' or unit == 'khz'):
            FTW = int((2**32)*(freq*(10**3)/(self.sys_clk)))
        elif(unit == 'mHz' or unit == 'MHz' or unit == 'Mhz' or unit == 'mhz'):
            FTW = int((2**32)*(freq*(10**6)/(self.sys_clk)))
        elif(unit == 'gHz' or unit == 'GHz' or unit == 'Ghz' or unit == 'ghz'):
            FTW = int((2**32)*(freq*(10**9)/(self.sys_clk)))
        else:
            print('Error in frequency_to_FTW: not suitable unit (%s).'\
                  % unit, 'unit should be \'Hz\', \'kHz\', \'MHz\', \'GHz\'')
        return FTW
    
    def phase_to_POW(self, phase, unit = 'FRAC'):
        if (unit == 'FRAC' or unit == 'frac'):
            phase_in_frac = phase
            
        elif(unit == 'RAD' or unit == 'rad' ):
            phase_in_frac = phase/(2*PI)
            
        elif(unit == 'DEG' or unit == 'deg'):
            phase_in_frac = phase/(360)
            
        else:
            print('Error in set_phase: not suitable unit (%s).'\
                  % unit, 'unit should be \'FRAC\', \'RAD\', \'DEG\'')
        POW = int( phase_in_frac * (2**16) )
        return POW
    
    def amplitude_to_ASF(self, amplitude_frac):
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
        ASF = int( amplitude_frac * ( 0x3fff ) )
        return ASF
        
    def set_frequency(self, freq, ch1, ch2, unit = 'MHz'):
        """
        freq            : frequency user want to set
        unit            : unit of frequency. default is MHz
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
        
        self.write32(FTW_ADDR, self.frequency_to_FTW(freq_in_Hz, unit = 'Hz'), 
                     ch1, ch2)
        
    def set_phase(self, phase, ch1, ch2, unit = 'FRAC'):
        """
        phase           : phase user want to set
        unit            : unit of phase. defualt is fraction of 2 pi
        """
        if (unit == 'FRAC' or unit == 'frac'):
            phase_in_frac = phase
            
        elif(unit == 'RAD' or unit == 'rad' ):
            phase_in_frac = phase/(2*PI)
            
        elif(unit == 'DEG' or unit == 'deg'):
            phase_in_frac = phase/(360)
            
        else:
            print('Error in set_phase: not suitable unit (%s).'\
                  % unit, 'unit should be \'FRAC\', \'RAD\', \'DEG\'')
        self.write16(POW_ADDR, self.phase_to_POW(phase_in_frac, unit = 'FRAC'),
                     ch1, ch2)
        
    def set_amplitude(self, amplitude_frac, ch1, ch2):
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
        self.write32(ASF_ADDR, ( self.amplitude_to_ASF(amplitude_frac) << 2 ), 
                     ch1, ch2)
        
    def initialize(self):
        self.set_CFR1()
        self.set_CFR2()
        self.set_CFR3()
        
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
        self.write32(CFR1_ADDR, CFR1_setting, ch1, ch2)
        
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
        self.write32(CFR2_ADDR, CFR2_setting, ch1, ch2)
        
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
        self.write32(CFR3_ADDR, CFR3_setting, ch1, ch2)
    
    def set_profile_register(self, freq, phase, amplitude, ch1, ch2, profile = 0, 
                    unit_freq = 'MHz', unit_phase = 'FRAC'):
        if (unit_freq == 'Hz' or unit_freq == 'hz'):
            freq_in_Hz = freq
            
        elif(unit_freq == 'kHz' or unit_freq == 'KHz' or 
             unit_freq == 'Khz' or unit_freq == 'khz'):
            freq_in_Hz = freq * (10**3)
            
        elif(unit_freq == 'mHz' or unit_freq == 'MHz' or 
             unit_freq == 'Mhz' or unit_freq == 'mhz'):
            freq_in_Hz = freq * (10**6)
            
        elif(unit_freq == 'gHz' or unit_freq == 'GHz' or 
             unit_freq == 'Ghz' or unit_freq == 'ghz'):
            freq_in_Hz = freq * (10**9) 
            
        else:
            print('Error in set_frequency: not suitable unit (%s).'\
                  % unit_freq,'unit should be \'Hz\', \'kHz\', \'MHz\','\
                  ' \'GHz\'')
                
        if( freq_in_Hz < self.min_freq or freq_in_Hz > self.max_freq ):
            print('Error in set_frequency: frequency should be between %d'\
                  'and %d' % (self.min_freq, self.max_freq))
                
        if (unit_phase == 'FRAC' or unit_phase == 'frac'):
            phase_in_frac = phase
            
        elif(unit_phase == 'RAD' or unit_phase == 'rad' ):
            phase_in_frac = phase/(2*PI)
            
        elif(unit_phase == 'DEG' or unit_phase == 'deg'):
            phase_in_frac = phase/(360)
            
        else:
            print('Error in set_phase: not suitable unit (%s).'\
                  % unit_phase, 'unit should be \'FRAC\', \'RAD\', \'DEG\'')
        FTW = self.frequency_to_FTW(freq_in_Hz, unit = 'Hz')
        POW = self.phase_to_POW(phase_in_frac, unit = 'FRAC')
        ASF = self.amplitude_to_ASF(amplitude)
        data = ( ASF << 48 ) | ( POW << 32 ) | ( FTW << 0 )
        self.write64(PROFILE0_ADDR + profile,data, ch1, ch2)
        
    def set_profile(self, profile1, profile2):
        inst_to_send = 0
        inst_to_send = ( ( DEST_DDS_PROFILE << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( profile1 & 0xff  ) \
                        | ( ( profile2 << 3 ) & 0xff ))
        inst_int_list = self.make_9_int_list(inst_to_send)
        
        if(TEST != 1):
            self.fpga.send_mod_BTF_int_list(config_int_list1)
            self.fpga.send_command('****')
        else:
            print('inst to send')
            for i in range(config_int_list1):
                print(bin(i << 1 + 1)[2:].zfill(10), end = '')
                
            print('')
    
    def set_parallel_frequency(self, frequency, parallel_en = 1, unit = 'MHz'):
        inst_to_send = 0
    
    def set_parallel_amplitude(self, amplitude, parallel_en = 1):
        inst_to_send = 0
    
    def set_parallel_phase(self, phase, parallel_en = 1, unit = 'FRAC'):
        inst_to_send = 0
    
    def io_update(self, ch1, ch2):
        self.fpga.send_command('DDS IO UPDATE')
        

if __name__ == "__main__":
    dds = AD9910(None)
    print(dds.make_header_string(0x11, direction = 'R'))