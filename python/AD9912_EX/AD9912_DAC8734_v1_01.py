# -*- coding: utf-8 -*-
"""
Created on Fri May 18 23:33:57 2018

@author: 1109282

Version history
v1_01: 
    
"""

from Arty_S7_v1_01 import ArtyS7

    
class DAC8734():
    def __init__(self, fpga):
        self.fpga = fpga
    

    def voltage_register_update(self, dac_number, ch, voltage, bipolar=True, v_ref=7.5):
        if bipolar:
            input_code = int(65536/(4*v_ref)*voltage)
            if (input_code < -32768) or (input_code > 32767):
                raise ValueError('Error in voltage_out: voltage is out of range')
        
            code = (input_code + 65536) % 65536
        else:
            if voltage < 0:
                raise ValueError('Error in voltage_out: voltage cannot be negative with unipolar setting')
            elif voltage > 17.5:
                raise ValueError('Error in voltage_out: voltage cannot be larger than 17.5 V')
                
            code = int(65536/(4*v_ref)*voltage)
            if (code > 65535):
                raise ValueError('Error in voltage_out: voltage is out of range')

        #print('Code:', code)
        message = [1<<dac_number, 0x04+ch, code // 256, code % 256]
            
        self.fpga.send_mod_BTF_int_list(message)
        self.fpga.send_command('WRITE DAC REG')
    
    def load_dac(self):
        #dac.send_mod_BTF_int_list([0xff,0x00, 0x40, 0x3C])
        #dac.send_command('WRITE REG')
        self.fpga.send_command('LDAC')
    
    def update_ldac_period(self, clock_count):
        if clock_count > 255:
            raise ValueError('Error in update_ldac_period: clock_count should be less than 256')
        self.fpga.send_mod_BTF_int_list([clock_count])
        self.fpga.send_command('LDAC LENGTH')

    def set_ch123(self, ch, voltage, bipolar=False, v_ref=7.5):
        self.voltage_register_update(ch, 1, voltage, bipolar, v_ref)
        self.voltage_register_update(ch, 2, voltage, bipolar, v_ref)
        self.voltage_register_update(ch, 3, voltage, bipolar, v_ref)
        self.load_dac()





class AD9912():
    def __init__(self, fpga, min_freq=10, max_freq=400):
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.fpga = fpga

        

    def make_header_string(self, register_address, bytes_length, direction='W'):
        if direction == 'W':
            MSB = 0
        elif direction == 'R':
            MSB = 1
        else:
            print('Error in make_header: unknown direction (%s). ' % direction, \
                  'direction should be either \'W\' or \'R\'.' )
            raise ValueError()
            
        if type(register_address) == str:
            address = int(register_address, 16)
        elif type(register_address) == int:
            address = register_address
        else:
            print('Error in make_header: unknown register address type (%s). ' % type(register_address), \
                  'register_address should be either hexadecimal string or integer' )
            raise ValueError()
            
        if (bytes_length < 1) or (bytes_length > 8):
            print('Error in make_header: length should be between 1 and 8.' )
            raise ValueError()
        elif bytes_length < 4:
            W1W0 = bytes_length - 1
        else:
            W1W0 = 3
        
        print(MSB, W1W0, address)
        header_value = (MSB << 15) + (W1W0 << 13) + address
        return ('%04X' % header_value)
            
    
    def FTW_Hz(self, freq):
        # make_header_string('0x01AB', 8)
        FTW_header = "61AB"
        y = int((2**48)*(freq/(10**9)))
        z = hex(y)[2:]
        FTW_body = (12-len(z))*"0"+z
        return FTW_header + FTW_body
    
    
    def make_9int_list(self, hex_string, ch1, ch2):
        hex_string_length = len(hex_string)
        byte_length = (hex_string_length // 2)
        if hex_string_length % 2 != 0:
            print('Error in make_int_list: hex_string cannot be odd length')
            raise ValueError()
            
        int_list = [(ch1 << 5) + (ch2 << 4) + byte_length]
        for n in range(byte_length):
            int_list.append(int(hex_string[2*n:2*n+2], 16))
        for n in range(8-byte_length):
            int_list.append(0)
        return int_list



    def set_frequency(self, freq_in_MHz, ch1, ch2):
        if (freq_in_MHz < self.min_freq) or (freq_in_MHz > self.max_freq):
            print('Error in set_frequency: frequency should be between 10 and 100 MHz')
            raise ValueError(freq_in_MHz)
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.FTW_Hz(freq_in_MHz*1e6), ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(self.make_9int_list('000501', ch1, ch2)) # Update the buffered (mirrored) registers
        self.fpga.send_command('WRITE DDS REG')


    def set_current(self, current, ch1, ch2):
        # DAC full-scale current
        # 1020 mVp-p (264*I_DAC_REF) => 670 mVp-p w/ FDB_IN
        #  270 mVp-p  (72*I_DAC_REF) => 180 mVp-p w/ FDB_IN
        if (current < 0) or (current > 0x3ff):
            print('Error in set_current: current should be between 0 and 0x3ff')
            raise ValueError(current)
    
        self.fpga.send_mod_BTF_int_list(
            self.make_9int_list(self.make_header_string(0x040C, 2)+('%04x' % current), ch1, ch2)) 
        self.fpga.send_command('WRITE DDS REG')
    
    def ch2_trigger_output(self, on=True):
        # HSTL driver
        # HSTL driver cannot work below 5.7MHz
        if on:
            register_value = '10'
        else:
            register_value = '90'
            
        self.fpga.send_mod_BTF_int_list( \
            self.make_9int_list(self.make_header_string(0x0010, 1)+register_value, 0, 1)) # Only ch2 has HSTL driver connected
        self.fpga.send_command('WRITE DDS REG')
    
    def soft_reset(self, ch1, ch2):
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.make_header_string(0, 1)+'3C', ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.make_header_string(0, 1)+'18', ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')
        
    def set_phase(self, phase, ch1, ch2):
        #  Phase value: 0000 ~ 3FFF
        if (phase<0) or (phase > 0x3fff):
            print('Error in set_phase: phase should be between 0 and 16383.')
            raise ValueError(phase)
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.make_header_string(0x01AD, 2)+'2580', ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')
        self.fpga.send_mod_BTF_int_list(self.make_9int_list('000501', ch1, ch2)) # Update the buffered (mirrored) registers
        self.fpga.send_command('WRITE DDS REG')

    def power_down(self, ch1, ch2):
        # Digital powerdown
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.make_header_string(0x0010, 1)+'91', ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')

    def power_up(self, ch1, ch2):
        # Digital power-up. We don't turn on the ch2 HSTL trigger automatically
        self.fpga.send_mod_BTF_int_list(self.make_9int_list(self.make_header_string(0x0010, 1)+'90', ch1, ch2))
        self.fpga.send_command('WRITE DDS REG')
        

    
if __name__ == '__main__':
    if 'fpga' in vars(): # To close the previously opened device when re-running the script with "F5"
        fpga.close()
    fpga = ArtyS7('COM18') # IonTrap-laptop1 (white - 32bit)
    #fpga = ArtyS7('COM31') # IonTrap8-광학실험실 테이블위 dummy terminal
    fpga.print_idn()
    
    dna_string = fpga.read_DNA()
    print('FPGA DNA string:', dna_string)


    dac = DAC8734(fpga)
    dds = AD9912(fpga, 10, 200)

"""
    dac.set_ch123(0, 5)
    dds.set_frequency(10, 1, 1)
    fpga.close()
"""