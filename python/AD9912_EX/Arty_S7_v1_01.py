# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 23:23:46 2017

@author: 1109282

v1_01: Added read_DNA(), print_idn() methods

"""

import serial

class escapeSequenceDetected(Exception):
    def __init__(self, escape_char):
        self.escape_char = escape_char
    def __str__(self):
        return ('\\x10%c is detected' % self.escape_char)

class ArtyS7:
    CMD_RX_BUFFER_BYTES = 0xf
    BTF_RX_BUFFER_BYTES = 0x100
    TERMINATOR_STRING = '\r\n'
    PATTERN_BYTES = 4
    
    def __init__(self, serialPort):
        self.com = serial.Serial(serialPort, baudrate=57600, timeout=1, \
                parity='N', bytesize=8, stopbits=2, xonxoff=False, \
                rtscts=False, dsrdtr=False, writeTimeout = 0 )
        
    def close(self):
        self.com.close()


    def send_command(self, cmd):
        string_length = len(cmd)
        if (string_length > ArtyS7.CMD_RX_BUFFER_BYTES):
            print('send_command: CMD cannot be longer than %d. Current length is %d.' % \
                  (ArtyS7.CMD_RX_BUFFER_BYTES, string_length))
        else:
            string_to_send = ('!%x' % string_length)
            for each_char in cmd:
                if each_char == '\x10':
                    string_to_send += '\x10\x10'
                else:
                    string_to_send += each_char
            string_to_send += '\r\n'
            string_to_send = string_to_send.encode('latin-1')
            self.com.write(string_to_send)

    def send_mod_BTF_string(self, modified_BTF):
        string_length = len(modified_BTF)
        if (string_length > ArtyS7.BTF_RX_BUFFER_BYTES):
            print('send_mod_BTF_string: Modified BTF cannot be longer than %d. Current length is %d.' \
                  % (ArtyS7.BTF_RX_BUFFER_BYTES, string_length))
        else:
            byte_count_string = '%x' % string_length
            num_digits = len(byte_count_string)
            data_to_send = ('#%x%s' % (num_digits, byte_count_string))
            for each_char in modified_BTF:
                if each_char == '\x10':
                    data_to_send += '\x10\x10'
                else:
                    data_to_send += each_char
            data_to_send += '\r\n'
            data_to_send = data_to_send.encode('latin-1')
            #print(data_to_send)
            self.com.write(data_to_send)

    def send_mod_BTF_int_list(self, modified_BTF):
        dataLength = len(modified_BTF)
        if (dataLength> ArtyS7.BTF_RX_BUFFER_BYTES):
            print('send_mod_BTF_int_list: Modified BTF cannot be longer than %d. Current length is %d.' \
                  % (ArtyS7.BTF_RX_BUFFER_BYTES, dataLength))
        else:
            byte_count_string = '%x' % dataLength
            num_digits = len(byte_count_string)
            data_to_send = ('#%x%s' % (num_digits, byte_count_string))
            for each_byte in modified_BTF:
                if each_byte == 0x10:
                    data_to_send += '\x10\x10'
                else:
                    data_to_send += chr(each_byte)
            data_to_send += '\r\n'
            data_to_send = data_to_send.encode('latin-1')
            #print(data_to_send)
            self.com.write(data_to_send)



    def read_next(self):
        first_char = self.com.read(1).decode('latin-1') # bytes larger than 127 cannot be translated into 'utf-8', but 'latin-1' can handle up to 255
        if first_char == '\x10':
            second_char = self.com.read(1).decode('latin-1')
            if second_char == '\x10': # '\x10\x10' is detected
                return '\x10'
            else:
                raise escapeSequenceDetected(second_char)
        else:
            return first_char
            
    
    def flush_input(self):
        length = self.com.inWaiting()
        print(self.com.read(length))
        print('flush_input: %d bytes are waiting.', length)

    
    def read_next_message(self, escape_debug=False):
        try:
            next_char = self.read_next()
            
            if next_char == '!':
                length_of_following_data = int(self.read_next(), 16)
                data = ''
                for n in range(length_of_following_data):
                    data += self.read_next()
                    
                for n in range(len(ArtyS7.TERMINATOR_STRING)):
                    next_char = self.read_next()
                    if ArtyS7.TERMINATOR_STRING[n] != next_char:
                        print('read_next_message: Termination string does not match. Expected: %s, reply: %s' \
                              % (ArtyS7.TERMINATOR_STRING[n], next_char))
                
                return ('!', data)
            
            elif next_char == '#':
                num_digits = int(self.read_next(), 16)
                byte_count = 0
                for n in range(num_digits):
                    byte_count = byte_count*16 + int(self.read_next(), 16)
                data = ''
                for n in range(byte_count):
                    data += self.read_next()
                    
                for n in range(len(ArtyS7.TERMINATOR_STRING)):
                    next_char = self.read_next()
                    if ArtyS7.TERMINATOR_STRING[n] != next_char:
                        print('read_next_message: Termination string does not match. Expected: %s, reply: %s' \
                              % (ArtyS7.TERMINATOR_STRING[n], next_char))
                
                return ('#', data)
    
            elif next_char == '':
                print('read_next_message: No more messages')
                return ('0', '')
                
            else:
                print('read_next_message: Unknown signature character: %s' % next_char)
                return ('E', next_char)
        except escapeSequenceDetected as e:
            if e.escape_char == 'C':
                if escape_debug:
                    print('read_next_message: Escape reset ("\\x10C") is returned')
            elif e.escape_char == 'R':
                if escape_debug:
                    print('read_next_message: Escape read ("\\x10R") is returned')
                data = []
                for n in range(5):
                    data.append(ord(self.read_next()))
                for n in range(len(ArtyS7.TERMINATOR_STRING)):
                    next_char = self.read_next()
                    if ArtyS7.TERMINATOR_STRING[n] != next_char:
                        print('read_next_message: Termination string of "\\x10R" does not match. Expected: %s, reply: %s' \
                              % (ArtyS7.TERMINATOR_STRING[n], next_char))
                e.escape_R_data = data
            elif e.escape_char == 'W':
                if escape_debug:
                    print('read_next_message: Escape waveform ("\\x10W") is returned')
                
            raise e


    def escape_read(self):
        self.com.write(b'\x10R') # Read bits
        try:
            self.read_next_message()
        except escapeSequenceDetected as e:
            if e.escape_char != 'R':
                raise e
            else:
                raw_data = e.escape_R_data
                data = []
                for n in range(4):
                    data.append(format(raw_data[n], '08b'))
                status_bits = format(raw_data[4], '08b')
                return ('\x10R', status_bits, data)

    def check_waveform_capture(self):
        self.com.write(b'\x10R') # Read bits
        try:
            self.read_next_message()
        except escapeSequenceDetected as e:
            if e.escape_char != 'R':
                raise e
            else:
                waveform_capture_info = (e.escape_R_data)[4]
                if (waveform_capture_info & (1<<2)) == 0:
                    status_string = 'No capture_waveform_data module is implemented!'
                else:
                    status_string = ''
                    if (waveform_capture_info & (1<<1)) > 0:
                        status_string += 'Trigger is armed. '
                    if (waveform_capture_info & (1<<0)) > 0:
                        status_string += 'Captured waveform data exists. '
                    if (waveform_capture_info & 3) == 0:
                        status_string += 'No waveform data exists. '
        print(status_string)


    def escape_reset(self):
        self.com.write(b'\x10C') # Reset
        try:
            self.read_next_message()
        except escapeSequenceDetected as e:
            if e.escape_char != 'C':
                raise e
            print('escape_reset: Escape reset ("\\x10C") is returned')
            

    def intensity(self, value):
        if value > 255:
            print('Current value is %d. Value should be lessn than 256.' % value)
            return
        self.send_mod_BTF_int_list([value]) # com.write(b'#11\x04\r\n') # toggle led0_g
        self.send_command('ADJ INTENSITY')

    
    def read_intensity(self):
        self.send_command('READ INTENSITY')
        message = self.read_next_message()
        if message[0] != '!':
            print('read_intensity: Reply is not CMD type:', message)
            return False
        print('read_intensity: Current intensity is ', ord(message[1]))


    def bit_list_to_int(self, bit_list):
        value = 0
        for bit in bit_list:
            value = (value << 1) | bit
        return value

    
    def update_bit_pattern(self, list_of_bit_position_and_value):
        mask_pattern = (ArtyS7.PATTERN_BYTES*8)*[0]
        bit_pattern = (ArtyS7.PATTERN_BYTES*8)*[0]
        for each_bit in list_of_bit_position_and_value:
            mask_pattern[each_bit[0]-1] = 1
            bit_pattern[each_bit[0]-1] = each_bit[1]
        #print(mask_pattern, bit_pattern)
        mask_pattern_value = self.bit_list_to_int(mask_pattern)
        bit_pattern_value = self.bit_list_to_int(bit_pattern)
        #print('%x, %x' % (mask_pattern_value, bit_pattern_value))
        mask_pattern_list = []
        bit_pattern_list = []
        for n in range(ArtyS7.PATTERN_BYTES):
            mask_pattern_list.append(mask_pattern_value % 256)
            mask_pattern_value = mask_pattern_value // 256
            bit_pattern_list.append(bit_pattern_value % 256)
            bit_pattern_value = bit_pattern_value // 256
        mask_pattern_list.reverse()
        bit_pattern_list.reverse()
        #print(list(map(lambda x: format(x, '08b'), mask_pattern_list)), \
        #      list(map(lambda x: format(x, '08b'), bit_pattern_list)))
        self.send_mod_BTF_int_list(mask_pattern_list + bit_pattern_list)
        self.send_command('UPDATE BITS')


    def read_bit_pattern(self):
        self.send_command('READ BITS')
        message = self.read_next_message()
        if message[0] != '!':
            print('read_bit_pattern: Reply is not CMD type:', message)
            return False
        bit_pattern_string = ''
        for eachByte in message[1]:
            bit_pattern_string += (format(ord(eachByte), '08b') + ' ')
        print(bit_pattern_string)

    def read_captured_waveform(self, print_output=False):
        message = self.read_next_message()
        if message[0] != '#':
            print('read_captured_waveform: Reply is not modified BTF type:', message)
            return False
        binary_data = message[1]
        if print_output:
            for n in range(len(binary_data)>>1):
                print(format(ord(binary_data[2*n]), '08b'), format(ord(binary_data[2*n+1]), '08b'))
            print('read_captured_waveform: Total bytes read:', len(binary_data))
        return len(binary_data)

    def read_DNA(self):
        self.send_command('DNA_PORT')
        DNA_PORT = self.read_next_message()
        dna = DNA_PORT[1]
        
        # 4 MSBs show if reading from DNA_PORT is finished. If 4 MSBs == 4'h1, DNA_PORT reading is done 
        if ord(dna[0]) // 16 != 1:
            raise ValueError('Device DNA is not ready yet!')
            
        dna_val = ord(dna[0]) % 16 # Strips the 4 MSBs
        for n in dna[1:]:
            dna_val = dna_val * 256 + ord(n)
            
        return ('%015X' % dna_val) # Returns strings representing 57 bits of device DNA 
    
    def print_idn(self):
        self.send_command('*IDN?') # com.write(b'!5*IDN?\r\n')
        print(self.read_next_message())
        #self.fpga.check_waveform_capture() # Check the status of trigger

        
                
#%%        
if __name__ == '__main__':
    if 'dev' in vars(): # To close the previously opened device when re-running the script with "F5"
        dev.close()
    dev = ArtyS7('COM18')
    dev.send_command('*IDN?') # com.write(b'!5*IDN?\r\n')
    print(dev.read_next_message())
    dev.check_waveform_capture() # Check the status of trigger

    dna_string = dev.read_DNA()
    print('FPGA DNA string:', dna_string)
    #dev.close()

"""
#%%
###############################################################################
# Resets all the FSM
#dev.com.write(b'\x10C')
#dev.com.read(30)
dev.escape_reset()




#%%
###############################################################################
# Reads all the bits connected to monitoring_32bits similar to the following line at the end of main module. These bits are useful for debugging purpose.
# assign monitoring_32bits = patterns;
#dev.com.write(b'\x10R')
#dev.com.read(30)
dev.escape_read()    





#%%
###############################################################################
# Change the intensity of LED0 & LED1

dev.intensity(1)
dev.read_intensity()





#%%
###############################################################################
# Change the bit output. Destination of each bit output is generally specified
# at the end of main module similar to the following line
# assign {led, red1, green1, blue1, red0, green0, blue0} = patterns[1:10];

dev.update_bit_pattern([(1,1), (3,0), (4,0), (5,1), (7, 1), (10, 1)])
dev.update_bit_pattern([(1,0), (3,1)])
dev.update_bit_pattern([(32,1)])

dev.update_bit_pattern([(15,0)])
        
dev.read_bit_pattern()





#%%
###############################################################################
# The following commands flushes the serial input buffer
dev.flush_input()




#%%
###############################################################################
# This function is to fill BTF buffer with some arbitrary data
def send_dummy_BTF(length, start):
    data_list = []
    for n in range(length):
        data_list.append((n+start)%256)
    #print(data_list)
    dev.send_mod_BTF_int_list(data_list)

send_dummy_BTF(256, 0)    

# 'CAPTURE BTF' command captures the current status of BTF buffer, and it can be read by 'READ BTF'. This command is useful for debugging BTF buffer.

dev.send_command('CAPTURE BTF')

# 'BTF READ COUNT' command sets how many bytes 'READ BTF' command will read
# dev.send_mod_BTF_string('\x01\x00') means read all 256 bytes in BTF_capture
dev.send_mod_BTF_string('\x01\x00')
dev.send_command('BTF READ COUNT')

# 'READ BTF' will read BTF_capture[1:('BTF READ COUNT')*8]
dev.send_command('READ BTF')
dev.read_next_message()

# The following are testing non-escape character situation
dev.com.write(b'!6\x10\x10TEST\x10\x10\r\n') # dev.send_command('\x10TEST\x10')
dev.read_next_message()

# Once the wrong format is transmitted, ('!', 'Wrong format') message can be
# returned multiple times because the remaing part of the string will be
# also recognized as additional wrong format
dev.com.write(b'!6\x10\x10TEST\x10\r\n') # Wrong format
dev.read_next_message()





#%%
###############################################################################
# The following codes are used to test the waveform capturing and reading
# To capture waveform, use the following command

after_trigger_count = 1024-4
after_trigger_count // 256
after_trigger_count % 256
dev.send_mod_BTF_int_list([int('11000000', 2), int('00111111', 2), 
                           int('10101001', 2), int('10010000', 2), 
                           after_trigger_count // 256, after_trigger_count % 256])
dev.com.write(b'\x10T')


dev.check_waveform_capture() # Check the status of trigger
dev.send_command('WAVEFORM') # Trigger from main FSM. This is sample implementation
dev.check_waveform_capture() # Check the status of trigger
dev.com.write(b'\x10W') # If any captured waveform data exists, read those waveform data
dev.read_next_message() # This will raise b'\x10W' detection
dev.com.inWaiting() # returns the bytes waiting in the first-level buffer (max ~4,000)
dev.read_captured_waveform(True) # Read one block of actual waveform
dev.com.inWaiting()

dev.flush_input()


dev.check_waveform_capture() # Check the status of trigger
dev.com.write(b'\x10A') # similar to dev.send_command('WAVEFORM'), but the trigger is armed through escape character, therefore it will work even if the main FSM is running in infinite loop
dev.check_waveform_capture() # Check the status of trigger
dev.com.write(b'\x10W') # Read waveform data
dev.read_next_message() # This will raise b'\x10W' detection
dev.read_captured_waveform(True) # Read one block of actual waveform

dev.com.inWaiting()
dev.flush_input()



def test_trigger_pattern_and_delay(mask1, mask2, pattern1, pattern2, firstCount):
    after_trigger_count = 1024-firstCount
    dev.send_mod_BTF_int_list([int(mask1, 2), int(mask2, 2), 
                           int(pattern1, 2), int(pattern2, 2), 
                           after_trigger_count // 256, after_trigger_count % 256])
    dev.com.write(b'\x10T')

    dev.send_command('WAVEFORM')
    dev.com.write(b'\x10W') # Read waveform data
    try:
        dev.read_next_message() # This will raise b'\x10W' detection
    except Exception:
        pass
    dev.read_captured_waveform(True) # Read one block of actual waveform
    
dev.flush_input()
test_trigger_pattern_and_delay('11000000', '00111111',
                               '10101001', '10010000', 60)

    


#%%
###############################################################################
# The following is to test how many bytes can be buffered in serial port.
# When the following code was tested on Windows7, about 8,000 bytes were buffered.
import time
def test_trigger_and_read_multiple_captured_waveform(number):
    for n in range(number):
        dev.send_command('WAVEFORM')
        dev.com.write(b'\x10W') # Read waveform data
        print('Reading %d-th waveform...' % n)
        time.sleep(1)

    count = 0
    while(dev.com.inWaiting() > 0):
        try:
            count += dev.read_captured_waveform()
        except escapeSequenceDetected as e:
            if e.escape_char == 'W':
                print('Block of size %d was read' % count)
                count = 0
    print('Block of size %d was read' % count)

dev.flush_input()
test_trigger_and_read_multiple_captured_waveform(3) # works well
test_trigger_and_read_multiple_captured_waveform(4) # Reading 4 waveforms without reading any data from serial port causes some problem.



#%%
###############################################################################
# When the return strings cannot be easily decoded, just try the following:
dev.com.read(30)


dev.close()
"""

