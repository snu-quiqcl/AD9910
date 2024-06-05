# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 05:08:40 2020

@author: JeonghyunPark
"""

import time
from Arty_S7_v1_01 import ArtyS7
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
                        


class AD9910:
    def __init__(
            self, 
            fpga : ArtyS7 = None, 
            min_freq : float = 10 * MHz, 
            max_freq : float = 400 * MHz, 
            sys_clk : float = 1000 * MHz, 
        ) -> None:                        
        #default min_freq, max_freq should be checked.
        """
        Parameters
        ----------
        fpga            : ArtyS7
        max_freq        : maximum output frequency of DDS
        min_freq        : minimum output frequency of DDS
        sys_clk         : REF_CLK of DDS
        
                                  
        Returns
        -------
        None
        
        in this version we assum not using PLL in DDS. after this version 
        parameter about PLL will be added.
        
        AD9910 has CFR (ConFiguration Register) which specifies machine 
        property(e.g. output sin or cos, profile mode or ram mode etc). In
        this init function, set CFR register value as a default value
        
        Disabled Features
        
        dest_val        : Destination address declared in Verilog code
                          this dest_val is used when multiple IP modules
                          are declared, and we have to designate these modules.
                          But in almost case you donnot have to specify this
                          dest_val value
        auto_en         : Verilog code of AD9910 code has auto function.
                          In auto mode, you make command with timestamp, which 
                          is exact time when command is executed. However, 
                          in almost cases this auto function will be disabled,
                          and make direct command at that time.
        
        
        """
        self.fpga = fpga
        self.fpga.send_command('OVERRIDE EN')
        self.dest_val = 1
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
        
    def make_8_int_list(self, data : int) -> list[int]:
        """
        
        Parameters
        ----------
        data : int
            int data to make 8 int lists

        Returns
        -------
        int_list : list(int)
            list of int which will be sent to FPGA
            
        This function returns list of int which will be sent to FPGA

        """
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
        
    def set_config(
            self, 
            cs : int = 0, 
            length : int = 8, 
            end_spi : int = 0, 
            slave_en : int = 0, 
            lsb_first : int = 0, 
            cspol : int = 0, 
            cpol : int = 0, 
            cpha : int = 0, 
            clk_div : int = 16
        ) -> None:
        """
        Parameters
        ----------
        cs : int
            Number of chip selected to send data
        length : int
            Length of data which will be sent
        end_spi : int 
            Indicate whether SPI communication ends after this command
        slave_en : int 
            Indicate whether FPGA read from other devices.
            (i.e. AD9910 : master -> FPGA : slave)
        lsb_first : int
            Specify order of data. For instance, at lsb first data 0b00001111 
            data will be sent as 0 0 0 0 1 1 1 1, and msb first data will be 
            sent as 1 1 1 1 0 0 0 0.
        cspol : int 
            Chip select polarity. when cspol is 0, chip select be LOW
            when data is sent. When cspol is 1, chip select become HIGH when 
            data is sent.
        cpol : int
            Clock polarity. when clock polarity is 0, positive edge makes data 
            transmission to module. On the other hand, when clock polarity is 1
            negative edge makes data transmission.
        cpha : int
            Clock phase. When cpha is 0, data(SDIO) changes when data 
            transmission ends. On the other hand, when cpha is 1, data 
            changes when data transmission occurs.
        clk_div : int
            Division of clock which will be used as a SCLK. For instance, when 
            FPGA clock is 100MHz, and clk_div is 16, SCLK is 100/16 = 6.25MHz

        Returns
        -------
        config_int_list : list(int)
            SPI configuration data list from FPGA
            
        This function returns SPI configuration int list according to input
        parameters.
        """
        config = ( ( DEST_SPI_CONFIG  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | ( lsb_first << 31 ) \
                        | ( slave_en << 30 ) \
                        | ( end_spi << 29 ) \
                        | ( 0 << 24 ) \
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
    
    def make_write_list(
            self, 
            data : int
        )->list[int]:
        """
        Parameters
        ----------
        data : int
            data will be sent to FPGA. 

        Returns
        -------
        data_int_list : list(int)
            data will be sent to FPGA. 
        """
        data_to_send = ( ( DEST_SPI_DATA  << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 )
                        | ( data & 0xffffffff ) )
        data_int_list = self.make_8_int_list(data_to_send)
        return data_int_list
    
    def write(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            register_addr : int, 
            register_data_list : int, 
            last_length : int
        ) -> None:
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 16.
        """
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        
        addr_int_list = self.make_write_list(register_addr << 24)
        
        
        self.fpga.send_mod_BTF_int_list(config_int_list1)
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(addr_int_list)
        self.fpga.send_command('WRITE DDS REG')
    
        for i in range(len(register_data_list) - 1):
            if ( i == 0 ):
                config_int_list2 = self.set_config( cs =((ch2 << 1)|(ch1 << 0)), 
                                                   length = 32)
                self.fpga.send_mod_BTF_int_list(config_int_list2)
                self.fpga.send_command('WRITE DDS REG')
                
            data_int_list = self.make_write_list(register_data_list[i])
            
            self.fpga.send_mod_BTF_int_list(data_int_list)
            self.fpga.send_command('WRITE DDS REG')
    
        config_int_list3 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = last_length,
                                           end_spi = 1 )
        
        last_int_list = self.make_write_list(register_data_list[-1] << ( 32 - last_length ) )
        
        self.fpga.send_mod_BTF_int_list(config_int_list3)
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(last_int_list)
        self.fpga.send_command('WRITE DDS REG')
        
        
    def write32(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            register_addr : int, 
            register_data_list : int
        ) -> None:
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1 )
        data_int_list = self.make_write_list(register_data)
        
        self.fpga.send_mod_BTF_int_list(config_int_list1)
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(addr_int_list)
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(config_int_list2)
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(data_int_list)
        self.fpga.send_command('WRITE DDS REG')
    
    def write64(
            self,
            ch1 : bool, 
            ch2 : bool, 
            register_addr : int, 
            register_data_list : int
        ) -> None:
        """
        register_addr   : address of register in DDS. this is int type.
        register_data   : data to be input. this is int type and length in
                        binary should be equal to 32.
        """
        config_int_list1 = self.set_config(cs = ((ch2 << 1) | (ch1 << 0)), 
                                           length = 8)
        addr_int_list = self.make_write_list(register_addr << 24)
        config_int_list2 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32 )
        data_int_list1 = self.make_write_list(register_data >> 32)
        config_int_list3 = self.set_config( cs = ((ch2 << 1)|(ch1 << 0)), 
                                           length = 32, end_spi = 1 )
        data_int_list2 = self.make_write_list(register_data)
        
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
            
    def frequency_to_FTW(self, freq : int) -> int:
        """
        makes frequency to FTW of DDS. Not need to consider sys_clk.
        Note that FTW is 32 bits in AD9910
        """
        FTW = int((2**32)*(freq*(10**0)/(self.sys_clk))) & 0xffffffff
        
        return FTW
    
    def phase_to_POW(self, phase : float) -> int:
        """
        notice that defulat unit is radian
        """
        POW = int( phase * (2**16) / (2*PI) ) & 0xffff
        
        return POW
    
    def amplitude_to_ASF(self, amplitude_frac : float) -> int:
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
                
        ASF = int( amplitude_frac * ( 0x3fff ) ) & 0x3fff
        
        return ASF
        
    def set_frequency(self, ch1, ch2, freq) -> None:
        """
        freq            : frequency user want to set
        unit            : unit of frequency. default is MHz
        """
        freq_in_Hz = freq  
        
        self.write32(ch1, ch2, FTW_ADDR, self.frequency_to_FTW(freq_in_Hz) )
        
    def set_phase(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            phase : float
        ) -> None:
        """
        phase           : phase user want to set
        unit            : unit of phase. defualt is fraction of 2 pi
        """
        self.write(ch1, ch2, POW_ADDR, [self.phase_to_POW(phase)], 
                   last_length = 16 )
        
    def set_amplitude(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            amplitude_frac : float
        ) -> None:
        if(amplitude_frac > 1 or amplitude_frac < 0):
            print('Error in amplitude_to_ASF: ampltiude range error (%s).'\
                  % amplitude_frac, 'ampltiude should be in 0 to 1')
                
        print('set amplitude')
        self.write32(ch1, ch2, ASF_ADDR, ( self.amplitude_to_ASF(amplitude_frac) << 2 ) )
        
    def initialize(self, ch1 : bool, ch2 : bool) -> None:
        delayed_cycle = 0
        self.set_CFR1(ch1,ch2)
        self.set_CFR2(ch1,ch2)
        self.set_CFR3(ch1,ch2)
        self.delay_cycle(-delayed_cycle)
        
    def set_CFR1(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            ram_en : bool = 0, 
            ram_playback : bool = 0, 
            manual_OSK : bool = 0, 
            inverse_sinc_filter : bool = 0, 
            internal_porfile : bool = 0, 
            sine : bool = 1,
            load_LRR : bool = 0, 
            autoclear_DRG : bool = 0, 
            autoclear_phase : bool = 0, 
            clear_DRG : bool = 0, 
            clear_phase : bool = 0, 
            load_ARR : bool = 0, 
            OSK_en : bool = 0,
            auto_OSK : bool = 0, 
            digital_power_down : bool = 0, 
            DAC_power_down : bool = 0, 
            REFCLK_powerdown : bool = 0, 
            aux_DAC_powerdown : bool = 0, 
            external_power_down_ctrl : bool = 0, 
            SDIO_in_only : bool = 0, 
            LSB_first : bool = 0
        ) -> None:
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
        
    def set_CFR2(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            amp_en_single_tone : bool = 1, 
            internal_IO_update : bool = 0, 
            SYNC_CLK_en : bool = 0, 
            DRG_dest : bool = 0, 
            DRG_en : bool = 0, 
            DRG_no_dwell_high : bool = 0, 
            DRG_no_dwell_low : bool = 0, 
            read_eff_FTW : bool = 1, 
            IO_update_rate : bool = 0, 
            PDCLK_en : bool = 0, 
            PDCLK_inv : bool = 0, 
            Tx_inv : bool = 0, 
            matched_latency_en : bool = 0, 
            data_ass_hold : bool = 0, 
            sync_val_dis : bool = 1, 
            parallel_port : bool = 0, 
            FM_gain : int = 0
        ) -> None:
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
            self.fm_gain = FM_gain
        if( ch2 == 1 ):
            self.cfr2[1] = CFR2_setting
            self.fm_gain = FM_gain
        self.write32(ch1, ch2, CFR2_ADDR, CFR2_setting)
        
    def set_CFR3(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            DRV0 : bool = 0, 
            PLL_VCO : int = 0, 
            I_CP : int = 0, 
            REFCLK_div_bypass : bool = 1, 
            REFCLK_input_div_reset : bool = 1, 
            PFD_reset : bool = 0, 
            PLL_en : bool = 0,
            N : int = 0
        ) -> None:
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
    
    def set_profile_register(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            freq : int, 
            phase : float, 
            amplitude : float, 
            profile : int = 0 
        ) -> None:
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
        
    def set_profile_pin(
            self, 
            profile1 : int, 
            profile2 : int
        ) -> None:
        data_to_send = 0
        data_to_send = ( ( DEST_DDS_PROFILE << (CHANNEL_LENGTH + 32) ) \
                        | ( self.dest_val << 32 ) \
                        | ( profile1 & 0b111  ) \
                        | ( ( profile2 << 3 ) & 0b111000 ) )
        data_int_list = self.make_8_int_list(data_to_send)
        
        self.fpga.send_mod_BTF_int_list(data_int_list)
        self.fpga.send_command('SET DDS PIN')
        
    def bits_to_represent(self, num : int) -> int:
        val = num
        count = 0
        while(val > 0):
            count = count + 1
            val = val >> 1
            
        return count
    
    def set_fm_gain(self, fm_gain : int) -> None:
        self.fm_gain = fm_gain & 0xf
        self.cfr1[0] = self.cfr1[0] - ( self.cfr1[0] & 0xf )
        self.cfr1[0] = self.cfr1[0] + fm_gain & 0xf
        self.write32(1, 0, CFR1_ADDR, self.cfr1[0])
    
    def minimum_fm_gain(self, frequency : int) -> int:
        return max(min(self.bits_to_represent(
            self.frequency_to_FTW(frequency)) - 16, 15),0)
    
    def io_update(self, ch1, ch2) -> None:
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
    
        self.fpga.send_mod_BTF_int_list(data_int_list1)
        self.fpga.send_command('DDS IO UPDATE')
        self.fpga.send_mod_BTF_int_list(data_int_list2)
        self.fpga.send_command('DDS IO UPDATE')
        
        
    def reset_driver(self) -> None:
        self.fpga.send_command('RESET DRIVER')
        
    def ram_write(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            data_list : list[int]
        ) -> None:
        self.write(ch1, ch2, RAM_ADDR, data_list, 32)
    
    def ram_write_frequency(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            data_list : list[int]
        ) -> None:
        frequency_list = []
        for data_each in data_list:
            frequency_list.append(self.frequency_to_FTW(data_each))
        self.ram_write(ch1, ch2, frequency_list)
    
    def ram_write_amplitude(
            self, 
            ch1 : bool,  
            ch2 : bool, 
            data_list : list[float]
        ) -> None:
        amplitude_list = []
        for data_each in data_list:
            amplitude_list.append(self.amplitude_to_ASF(data_each) << 18)
        self.ram_write(ch1, ch2, amplitude_list)
        
    def ram_write_phase(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            data_list : list[float]
        ) -> None:
        phase_list = []
        for data_each in data_list:
            phase_list.append(self.phase_to_POW(data_each) << 16)
        self.ram_write(ch1, ch2, phase_list)
    
    def ram_write_polar(
            self, 
            ch1 : bool, 
            ch2 : bool, 
            data_list : list[int]
        ) -> None:
        polar_list = []
        for data_each in data_list:
            polar_list.append( ( self.phase_to_POW(data_each[0]) << 16 )\
                              | ( self.amplitude_to_ASF(data_each[1]) << 2 ) )
        self.ram_write(ch1, ch2, polar_list)
    
    def set_ram_profile_register(
            self,
            ch1 : bool, 
            ch2 : bool, 
            addr_step_rate : int, 
            end_addr : int, 
            start_addr : int, 
            no_dwell_high : bool, 
            zero_crossing : bool, 
            ram_mode_ctrl : bool, 
            profile : int
        ) -> None:
        data_to_send = ( ( ( addr_step_rate & 0xffff ) << 40 ) \
                        | ( ( end_addr & 0x3ff ) << 30 ) \
                        | ( ( start_addr & 0x3ff ) << 14 ) \
                        | ( ( no_dwell_high & 0x1 ) << 5 ) \
                        | ( ( zero_crossing & 0x1 ) << 3 ) \
                        | ( ( ram_mode_ctrl & 0x7 ) << 0 ) )
        self.write64(ch1, ch2, PROFILE0_ADDR + profile, data_to_send)
        
        
    def reset_DDS(self) -> None:
        self.fpga.send_command('DDS RESET')
        time.sleep(1)
    
    def powerdown(self,ch1 : bool,ch2 : bool) -> None:
        if ch1 == True: self.fpga.send_command('DDS PWR DOWN1')
        if ch2 == True: self.fpga.send_command('DDS PWR DOWN2')
    
    def poweron(self,ch1 : bool,ch2 : bool) -> None:
        if ch1 == True: self.fpga.send_command('DDS PWR ON1')
        if ch2 == True: self.fpga.send_command('DDS PWR ON2')
        
    def set_internal(self) -> None:
        self.fpga.send_command('INTERNAL')
    
    def set_external(self) -> None:
        self.fpga.send_command('EXTERNAL')
        