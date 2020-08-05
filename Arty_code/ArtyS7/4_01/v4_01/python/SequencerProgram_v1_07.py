# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

<change log>
v1_03:
  * Add data memory (16bits x 1024) with memory reset
    - Added the following commands
    - load_word  reg3 <= mem[reg1]
    - store_word mem[reg1] <= reg3

  * Add trigger_out command
    - trigger_out some bits (imm1)

  * When the sequencer starts, PC, register file, data memory are resetted

  * Changed the name of the following commands
    - Change move command to 'read': method read_counter
    - Change load command to 'loadi': method load_immediate
    - Change store command to 'write' method write_to_fifo
    
  * Change the set command
    - Make multiple array for output pattern bits
    - set_output_port: r3(=reg3 address), bit pattern: imm1, mask: imm2

  * Modified the wait command
    - move the remaining count to the counter[15]

  * output FIFO is implemented
    - Implement command to read the data size in output FIFO
    - Implement command to read output FIFO

v1_04:
  * Changed the order of the return value from make_bit_pattern to match the
    order of set_output_port
    
v1_05:   
  * Allowed bit list argument for set_output_port method
  
  * Moved bit manipulation tools to SequencerUtility module
  
v1_06:
  * Added addi, subi, blti, beqi, waiti
  
  * Re-assigned op-code
  
  * Changed address of branch and jump from imm1 to imm2
  
  * waiti uses imm3 as comparison operand
  
v1_07:
  * Changed wait and trigger_out command to allow bit list argument similar to set_output_port
  * Bit location index is changed from [1:16] to [15:0] to make it easy to match hardware
  
"""

import math
import SequencerUtility_v1_01 as su

reg=tuple(('reg%d' % n) for n in range(32))
line_number_discrepancy_detected = False
each_line = []

class SequencerProgram():
    opcode = {'nop': 0x00,
              'add': 0x02,
              'addi': 0x03,
              'sub': 0x04,
              'subi': 0x05,
              
              'loadi': 0x06,
              'read': 0x07,
              'set': 0x08,
              'write': 0x09,
              
              'blt': 0x0a,
              'blti': 0x0b,
              'beq': 0x0c,
              'beqi': 0x0d,
              
              'jump': 0x0e,
              'stop': 0x0f,
              
              'load_word': 0x11,
              'store_word': 0x12,
              'trigger_out': 0x13,

              'wait': 0x14,
              'waiti': 0x15,

              }

    
    def __init__(self):
        self.program_list = []
        self.label_dict = {}
        self.inv_label_dict = {}
        self.initial_keys = []

        self.initial_keys = set(vars(self).keys())

    def _add_to_list(self, new_line):
        new_line[0] = len(self.program_list)
        self.program_list.append(new_line)
        #new_line[0] = self.program_list.index(new_line) # The problem with this is that "a=[0,1]; b=[0,1]; a==b" returns True
        return new_line

    def _get_raw_address(self, address):
        global each_line, line_number_discrepancy_detected
        if type(address) == int:
            if line_number_discrepancy_detected:
                print('\n!!Warning!!\nLine number discrepancy was detected in the previous check.')
                print('The current line %s uses the line number address which might be outdated.' % each_line)
                answer = input('Do you still want to use the current line number address (y/n)?')
                if answer == 'y':
                    line_number_discrepancy_detected = False
                else:
                    raise ValueError('Line number address needs to be updated')
            raw_address = address
        elif type(address) == list:
            raw_address = address[0]
        elif type(address) == str:
            line = getattr(self, address)
            raw_address = line[0]
        else:
            print('Unknown address type:', type(address))
        return raw_address
        
    def _addr_string(self, address):
        raw_address = self._get_raw_address(address)
        if raw_address in self.inv_label_dict:
            return ('addr[%d]<%s>' % (raw_address, self.inv_label_dict[raw_address]))
        else:
            return ('addr[%d]' % raw_address)

        
    def add(self, result_reg, operand1_reg, operand2, comment=None):
        """ Command to add two registers or one register and an immediate value
        and store the result into a specified register. 
        There is no restriction for registers meaning that you can
        specify the same register for all three parameters in which case the
        specified register will be simply doubled. For example,
        
        s.add(reg[3], reg[3], reg[3]): The value in reg[3] will be doubled.
        s.add(reg[2], reg[5], reg[7]): reg[2] <= reg[5] + reg[7]
        s.add(reg[4], reg[5], 1): reg[4] <= reg[5] + 1
        
        Args:
            result_reg (string): Target register to store result of additon.
                It should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.

            operand1_reg (string): register holding one of the value for addition.
                Use the same notation with result_reg such as reg[7]

            operand2 (string or int): register holding the other value or integer for addition.
                Use the same notation with result_reg such as reg[7] or integer
        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
            
        if type(operand2) == str:
            new_line = [0, 'add', reg.index(operand1_reg), reg.index(operand2), \
                    reg.index(result_reg), 0, 0, comment]
        elif type(operand2) == int:
            if (operand2 < 0) or (operand2 >= 1<<16):
                raise KeyError('Error in add: operand2(%d) cannot be larger than 65535 or negative' % operand2)
            new_line = [0, 'addi', reg.index(operand1_reg), 0, \
                    reg.index(result_reg), operand2, 0, comment]
        else:
            raise KeyError('Error in add: unknown type (%s) for operand2' % type(operand2))
            
        return self._add_to_list(new_line)
    
    def subtract(self, result, from_operand, delta, comment=None):
        """ Command to subtract one register value or an immediate value 
        from another register value
        and store the result into a specified register. 
        There is no restriction for registers meaning that you can
        specify the same register for all three parameters in which case the
        specified register will be simply doubled. For example,
        
        s.subtract(reg[3], reg[3], reg[3]): The value in reg[3] will be reset to zero.
        s.subtract(reg[2], reg[5], reg[7]): reg[2] <= reg[5] - reg[7]
        s.subtract(reg[2], reg[5], 1): reg[2] <= reg[5] - 1
        
        Args:
            result_reg (string): Target register to store result of additon.
                It should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.

            operand1_reg (string): register hold the target value for subtraction.
                Use the same notation with result_reg such as reg[7]

            delta (string): register holding a delta value or an integer for subtraction.
                Use the same notation with result_reg such as reg[7]
        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()

        if type(delta) == str:
            new_line = [0, 'sub', reg.index(from_operand), reg.index(delta), \
                    reg.index(result), 0, 0, comment]
        elif type(delta) == int:
            if (delta< 0) or (delta >= 1<<16):
                raise KeyError('Error in subtract: delta(%d) cannot be larger than 65535 or negative' % delta)
            new_line = [0, 'subi', reg.index(from_operand), 0, \
                    reg.index(result), delta, 0, comment]
        else:
            raise KeyError('Error in subtract: unknown type (%s) for delta' % type(delta))

        return self._add_to_list(new_line)
    
    def load_immediate(self, dest_reg, value, comment=None):
        """ Command to load immediate value to the destination register. For example,
        
        s.loadi(reg[3], 100): value 100 will be loaded into reg[3].
        
        Args:
            dest_reg (string): destination register to store the value.
                It should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.

            value (integer): immediate value to store into the destination register.
        
        Returns:
            list: This list contains the machine code for this line.
        """
        new_line = [0, 'loadi', 0, 0, reg.index(dest_reg), value, 0, comment]
        return self._add_to_list(new_line)

    def read_counter(self, dest_reg, counter_index, comment=None):
        """ Read 16-bit value at the input of the counters into a register.
        There are total 16 counter inputs, and counter_index specifies which
        counter will be read into the destination register.
        counter[14] and counter[15] are special inputs.
        counter[14] contains the remaining counts from the WAIT command when
        the WAIT command was interrupted by the specified trigger pattern.
        If counter[14] is 0, it means that WAIT command waited for 
        the full clock counts specified in the register.
        The input of the trigger_level also shows up at counter[15].
        counter[15] might be useful for debugging or detect trigger pattern programmatically.
        
        s.read(reg[3], 5): reg[3] <= counter[5].
        
        Args:
            dest_reg (string): destination register to store the value.
                It should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.

            counter_index (integer): index for counter. It should be between
                0 and 15.
        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        if counter_index > 15:
            print(('Error in line# %d: the given counter index (%d)' + \
                   'in move command is out of range (0~15)') \
                % (len(self.program_list), counter_index))
        new_line = [0, 'read', 0, 0, reg.index(dest_reg), counter_index, 0, comment]
        return self._add_to_list(new_line)

    def set_output_port(self, port_number, *args):
        """ Change the output bit pattern in the specified output port.
        This command changes the specified bits only, and the other bits will
        remain unchanged.
        
        set_output_port method supports the following two types of arguments.
        
        1. set_output_port(port_number, bit_pattern, bit_mask, optional_comment)
          - Both bit_pattern and bit_mask should be specified in integer
        2. set_output_port(port_number, [list of (bit_position, 0_or_1)], optional_comment)
          - List of (bit_position, 0_or_1) specifies which bit will be changed to what state
        
        'port_number' specify the output port number. For example,
        
        1. s.set_output_port(2, int('1000010001000000', 2), int('1000010001000100', 2))
        2. s.set_output_port(2, 0x8440, 0x8444)
        3. s.set_output_port(2, [(15, 1), (10, 1), (6, 1), (2, 0)])
        
        * Above three formats are equivalent.
        * Bit location is counted from right to left and LSB location is 0 and MSB location is 15
        * it will change only 15th, 10th, 6th, 2nd bits as specified by bit mask 1000 0100 0100 0100
        * bit data 1000 0100 0100 0000
        * The output at port[2] will be changed
        
        
        Args:
            port_number (integer): output port address from 0 to 3

            bit_pattern_list (list): List of bits to change
                This is a list composed of (bit_location, bit_value) pair
                
            or 
            
            [
            bit_pattern (integer): 16-bit integer. Even if some of the bit are 1,
                if that bit is not specified in the mask bit, it will be ignored
                
            bit_mask (integer): 16-bit integer.
            ]
        
        Returns:
            list: This list contains the machine code for this line.
        """
        comment = None
        if isinstance(args[0], (list, tuple)):
            for each_item in args[0]:
                if (not isinstance(each_item, (list, tuple))) or (len(each_item) != 2) \
                or (type(each_item[0]) != int) or (type(each_item[1]) != int):
                    err_msg = 'Error in set_output_port: Wrong format for bit list argument: %s in %s'\
                        % (each_item, str(args[0]))
                    raise SyntaxError(err_msg)
            if len(args) != 1:
                if len(args) > 2 or (type(args[1]) != str):
                    err_msg = ('Error in set_output_port: bit list type argument ' + \
                               'can be followed only by string comment, but ' + \
                               '"%s" is given.') % str(args[1:])
                    raise SyntaxError(err_msg)
                comment = args[1]
            (bit_pattern, bit_mask) = su.make_bit_pattern_from_15_to_0(args[0])
            
        elif isinstance(args[0], int) and isinstance(args[1], int):
            if len(args) != 2:
                if len(args) > 3 or ((type(args[2]) != str) and (args[2] != None)):
                    err_msg = ('Error in set_output_port: (bit pattern) and (bit mask) ' + \
                               'arguments combination can be followed ' + \
                               'only by string comment, but "%s" is given.') % str(args[2:])
                    raise SyntaxError(err_msg)
                comment = args[2]
            (bit_pattern, bit_mask) = args[0:2]
        else:
            err_msg = 'Error in set_output_port: unknown argument types "%s".' % str(args)
            raise SyntaxError(err_msg)
            
        new_line = [0, 'set', 0, 0, port_number, bit_pattern, bit_mask, comment]
        return self._add_to_list(new_line)



    def write_to_fifo(self, reg1, reg2, reg3, event_label, comment=None):
        """ Writes the intended information to the FIFO. Each FIFO line will be
        filled with (reg1, reg2, reg3, event_label) which is 64-bit long.
        For example, if reg[3] = 0x1234, reg[5] = 0x5678, reg[6] = 0x9abc,
        
        s.write(reg[3], reg[5], reg[6], 0x0001) will add "1234 5678 9abc 0001" to the FIFO.
        
        Args:
            reg1, reg2, reg3 (string): registers to write to FIFO.
                It should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.
                
            reg1 (integer): output port address from 0 to 3

            event_label (integer): any arbitrary 16-bit integer. You can use this
                value to distinguish data stored for different reason.
        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'write', reg.index(reg1), reg.index(reg2), \
                    reg.index(reg3), event_label, 0, comment]
        return self._add_to_list(new_line)

    def branch_if_less_than(self, addr, reg1, reference, comment=None):
        """ Jump to address if reg1 is less than reference.
        reference can be either register or immediate value
        For example, if reg[3] = 5, reg[5] = 10,
        
          s.branch_if_less_than(20, reg[3], reg[5])
          or 
          s.branch_if_less_than(20, reg[3], 10)
          
        
        The above command will make the program jump to line number 20.
        Because it is not easy to know the line number during programming,
        you can just store the target line in an attribute of SequencerProgram class object
        and use that as target. For example,
        
          s.doppler_cooling = s.s.set_output_port(2, 0x8440, 0x4444)
                :
                :
          s.branch_if_less_than(s.doppler_cooling, reg[3], reg[5])
          s.jump('PMT_count')
                :
                :
          s.PMT_count = s.read(reg[3], 5)
                :
                    
        If the target line is not yet defined or even if it is already defined,
        you can simply use the line name string such as 'PMT_count" 
        as shown in the above example.
        
        Args:
            addr (integer or string or class attribute): address to jump if the condition is true.
                If it is integer, it means the line number. Line number can be changed
                at any point, so it is not recommended.
                If the target address is already defined before, you can just
                specify the class attribute containing that line.
                This allows you to use the auto completion of the python editor,
                so it will be convenient.
                If the target line is not already defined, or if you simply don't 
                want to worry whether it is already defined or not, 
                then you can just use string type address.
                
                
            reg1 (string): the first register containing a value to compare.

            reference (string or int): the second register containing a value or immediate value to compare.

        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()

        if type(reference) == str:
            new_line = [0, 'blt', reg.index(reg1), reg.index(reference), 0, 0, addr, comment]
        elif type(reference) == int:
            if (reference < 0) or (reference >= 1<<16):
                raise KeyError('Error in blt: reference (%d) cannot be larger than 65535 or negative' % reference)
                
            new_line = [0, 'blti', reg.index(reg1), reference // 256, reference % 256, 0, addr, comment]
        else:
            raise KeyError('Error in blt: unknown type (%s) for reference' % type(reference))
        return self._add_to_list(new_line)

    def branch_if_equal_with_mask(self, addr, reg1, reference, mask=0xffff, comment=None):
        """ Jump to address if reg1 is equal to reference for the masked bits
        reference can be either register or immediate value
        For example, if reg[3] = 0x8421, reg[5] = 0x8400,
        
          s.branch_if_equal_with_mask(20, reg[3], reg[5], 0x8400)
          
          or
          
          s.branch_if_equal_with_mask(20, reg[3], 0x8400, 0x8400)

        The above command will make the program jump to line number 20, but
        
          s.branch_if_equal_with_mask(20, reg[3], reg[5], 0x8420)
          
          or
          
          s.branch_if_equal_with_mask(20, reg[3], 0x8400, 0x8420)
        
        the above command won't make the program jump to line number 20, because
        the masked bit are not the same.
        
        Because it is not easy to know the line number during programming,
        you can just store the target line in an attribute of SequencerProgram class object
        and use that as target. For example,
        
          s.doppler_cooling = s.s.set_output_port(2, 0x8440, 0x4444)
                :
                :
          s.branch_if_equal_with_mask(s.doppler_cooling, reg[3], reg[5], 0xffff)
          s.jump('PMT_count')
                :
                :
          s.PMT_count = s.read(reg[3], 5)
                :
                    
        If the target line is not yet defined or even if it is already defined,
        you can simply use the line name string such as 'PMT_count" 
        as shown in the above example.
        
        Args:
            addr (integer or string or class attribute): address to jump if the condition is true.
                If it is integer, it means the line number. Line number can be changed
                at any point, so it is not recommended.
                If the target address is already defined before, you can just
                specify the class attribute containing that line.
                This allows you to use the auto completion of the python editor,
                so it will be convenient.
                If the target line is not already defined, or if you simply don't 
                want to worry whether it is already defined or not, 
                then you can just use string type address.
                
                
            reg1 (string): the first register containing a value to compare.

            reference (string or int): the second register containing a value or immediate value to compare.
            
            mask (integer): 16-bit integer. If you want reg1 and reference to be exact,
                use 0xffff.
        
        Returns:
            list: This list contains the machine code for this line.
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()

        if type(reference) == str:
            new_line = [0, 'beq', reg.index(reg1), reg.index(reference), 0, mask, addr, comment]
        elif type(reference) == int:
            if (reference < 0) or (reference >= 1<<16):
                raise KeyError('Error in beq: reference (%d) cannot be larger than 65535 or negative' % reference)
            new_line = [0, 'beqi', reg.index(reg1), reference // 256, reference % 256, mask, addr, comment]
        else:
            raise KeyError('Error in beq: unknown type (%s) for reference' % type(reference))

        return self._add_to_list(new_line)

    def branch_if_equal(self, addr, reg1, reference, comment=None):
        """ Jump to address if reg1 is equal to the reference
        reference can be either register or immediate value
        For example, if reg[3] = 0x8421, reg[5] = 0x8400,
        
          s.branch_if_equal(20, reg[3], reg[5])
          or
          s.branch_if_equal(20, reg[3], 0x8400)

        The above command will make the program jump to line number 20
        
        Because it is not easy to know the line number during programming,
        you can just store the target line in an attribute of SequencerProgram class object
        and use that as target. For example,
        
          s.doppler_cooling = s.s.set_output_port(2, 0x8440, 0x4444)
                :
                :
          s.branch_if_equal(s.doppler_cooling, reg[3], reg[5])
          s.jump('PMT_count')
                :
                :
          s.PMT_count = s.read(reg[3], 5)
                :
                    
        If the target line is not yet defined or even if it is already defined,
        you can simply use the line name string such as 'PMT_count" 
        as shown in the above example.
        
        Args:
            addr (integer or string or class attribute): address to jump if the condition is true.
                If it is integer, it means the line number. Line number can be changed
                at any point, so it is not recommended.
                If the target address is already defined before, you can just
                specify the class attribute containing that line.
                This allows you to use the auto completion of the python editor,
                so it will be convenient.
                If the target line is not already defined, or if you simply don't 
                want to worry whether it is already defined or not, 
                then you can just use string type address.
                
                
            reg1 (string): the first register containing a value to compare.

            reference (string or int): the second register containing a value or immediate value to compare.
            
        Returns:
            list: This list contains the machine code for this line.
        """
        return self.branch_if_equal_with_mask(addr, reg1, reference, mask=0xffff, comment=comment)


    def jump(self, addr, comment=None):
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'jump', 0, 0, 0, 0, addr, comment]
        return self._add_to_list(new_line)


    def wait_n_clocks_or_masked_trigger(self, clock_count, *args):
        """ Wait for n clocks specified either by clock_count argument.
        clock_count can be either register or an immediate value.
        wait_n_clocks_or_masked_trigger method supports the following two types of arguments.
        For example, if reg[3] contains 20 (clock counts), the following command
        will wait for 20+2 clocks unless it is interrupted by trigger
        
        s.wait_n_clocks_or_masked_trigger(reg[3], 0x1008, 0x1248)
        
        or
        
        s.wait_n_clocks_or_masked_trigger(reg[3], [(12, 1), (9, 0), (6, 0), (3, 1)])
        
        or
        
        s.wait_n_clocks_or_masked_trigger(20, [(12, 1), (9, 0), (6, 0), (3, 1)])
        
        If bit_mask is 0, it will wait for n clocks unconditionally.
        If bit_mask is not 0, the wait can be interrupted by the pattern trigger.
        When the wait is interrupted, the remaining clock count will be available through counter[15].
        If the timer expires without the pattern trigger, counter[15] will be reset.
        
        Args:
            clock_count (string or int): register containing clock count or immediate value.
                In case of register, it should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.
                In case of immeidate value, it should be between 0 and 65535.

            bit_pattern (integer): bit pattern to match with the trigger_level

            bit_mask (integer): bit mask to use for bit matching
        
        Returns:
            list: This list contains the machine code for this line.
        """
        comment = None
        if isinstance(args[0], (list, tuple)):
            for each_item in args[0]:
                if (not isinstance(each_item, (list, tuple))) or (len(each_item) != 2) \
                or (type(each_item[0]) != int) or (type(each_item[1]) != int):
                    err_msg = 'Error in wait_n_clocks_or_masked_trigger: Wrong format for bit list argument: %s in %s'\
                        % (each_item, str(args[0]))
                    raise SyntaxError(err_msg)
            if len(args) != 1:
                if len(args) > 2 or (type(args[1]) != str):
                    err_msg = ('Error in wait_n_clocks_or_masked_trigger: bit list type argument ' + \
                               'can be followed only by string comment, but ' + \
                               '"%s" is given.') % str(args[1:])
                    raise SyntaxError(err_msg)
                comment = args[1]
            (bit_pattern, bit_mask) = su.make_bit_pattern_from_15_to_0(args[0])
            
        elif isinstance(args[0], int) and isinstance(args[1], int):
            if len(args) != 2:
                if len(args) > 3 or ((type(args[2]) != str) and (args[2] != None)):
                    err_msg = ('Error in wait_n_clocks_or_masked_trigger: (bit pattern) and (bit mask) ' + \
                               'arguments combination can be followed ' + \
                               'only by string comment, but "%s" is given.') % str(args[2:])
                    raise SyntaxError(err_msg)
                comment = args[2]
            (bit_pattern, bit_mask) = args[0:2]
        else:
            err_msg = 'Error in wait_n_clocks_or_masked_trigger: unknown argument types "%s".' % str(args)
            raise SyntaxError(err_msg)

        if type(clock_count) == str:
            new_line = [0, 'wait', reg.index(clock_count), 0, 0, bit_pattern, bit_mask, comment]
        elif type(clock_count) == int:
            if (clock_count < 0) or (clock_count >= 1<<16):
                raise KeyError('Error in wait: clock_count(%d) cannot be larger than 65535 or negative' % clock_count)
            new_line = [0, 'waiti', 0, clock_count//256, clock_count%256, bit_pattern, bit_mask, comment]
        else:
            raise KeyError('Error in wait: unknown type (%s) for clock_count' % type(clock_count))

        return self._add_to_list(new_line)

    def wait_n_clocks(self, clock_count, comment=None):
        """ Wait for n clocks specified either by clock_count argument.
        clock_count can be either register or an immediate value.
        For example, if reg[3] contains 20 (clock counts), the following command
        will wait for 20+2 clocks
        
        s.wait_n_clocks_or_masked_trigger(reg[3])
        
        or
        
        s.wait_n_clocks_or_masked_trigger(20)
        
        Args:
            clock_count (string or int): register containing clock count or immediate value.
                In case of register, it should be one of the string between 'reg0' and 'reg31'. 
                This is not easy way to type and not easy to recognize, 
                so a convenient dictionary reg[] is provided.
                If you type reg[3], it will automatically convert to 'reg3'.
                In case of immeidate value, it should be between 0 and 65535.

        Returns:
            list: This list contains the machine code for this line.
        """
        return self.wait_n_clocks_or_masked_trigger(clock_count, 0, 0, comment)

    def stop(self, comment=None):
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'stop', 0, 0, 0, 0, 0, comment]
        return self._add_to_list(new_line)


    def nop(self, comment=None):
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'nop', 0, 0, 0, 0, 0, comment]
        return self._add_to_list(new_line)


    def load_word_from_memory(self, target_reg, memory_address_reg, comment=None):
        """
        - load_word  target_reg <= mem[memory_address_reg]
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'load_word', reg.index(memory_address_reg), 0, reg.index(target_reg), 0, 0, comment]
        return self._add_to_list(new_line)


    def store_word_to_memory(self, memory_address_reg, source_reg, comment=None):
        """
        - store_word mem[memory_address_reg] <= source_reg
        """
        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'store_word', reg.index(memory_address_reg), 0, reg.index(source_reg), 0, 0, comment]
        return self._add_to_list(new_line)
        

    def trigger_out(self, *args):
        """
        - trigger_out bit_pattern
        """
        comment = None
        if isinstance(args[0], (list, tuple)):
            for each_item in args[0]:
                if (type(each_item) != int):
                    err_msg = 'Error in trigger_out: Wrong format for bit list argument: %s in %s'\
                        % (each_item, str(args[0]))
                    raise SyntaxError(err_msg)
            if len(args) != 1:
                if len(args) > 2 or (type(args[1]) != str):
                    err_msg = ('Error in trigger_out: bit list type argument ' + \
                               'can be followed only by string comment, but ' + \
                               '"%s" is given.') % str(args[1:])
                    raise SyntaxError(err_msg)
                comment = args[1]
            bit_pattern = su.make_bit_pattern_from_position_list_from_15_to_0(args[0])
        elif isinstance(args[0], int):
            if len(args) != 1:
                if len(args) > 2 or ((type(args[1]) != str) and (args[1] != None)):
                    err_msg = ('Error in trigger_out: bit list type argument ' + \
                               'can be followed only by string comment, but ' + \
                               '"%s" is given.') % str(args[1:])
                    raise SyntaxError(err_msg)
                comment = args[1]
            bit_pattern = args[0]
            
            
        else:
            err_msg = 'Error in wait_n_clocks_or_masked_trigger: unknown argument types "%s".' % str(args)
            raise SyntaxError(err_msg)




        if (comment != None) and (type(comment) != str):
            print('Comment should be string type')
            raise KeyError()
        new_line = [0, 'trigger_out', 0, 0, 0, bit_pattern, 0, comment]
        return self._add_to_list(new_line)
        

    def _check_program_consecutiveness(self):
        global line_number_discrepancy_detected
        for line_number in range(len(self.program_list)):
            if line_number != self.program_list[line_number][0]:
                line_number_discrepancy_detected = True
                print('Line number of %s is not consecutive. It is supposed to be %d.' \
                      % (self.program_list[line_number], line_number))
                raise ValueError('Line number is not consecutive')


    def _update_labels(self):
        self._check_program_consecutiveness()
        label_list = set(vars(self).keys()) - self.initial_keys
        #print(label_list)
        for each_label in label_list:
            line = getattr(self, each_label)
            self.label_dict[each_label] = line[0]
            
        self.inv_label_dict = {v: k for k, v in self.label_dict.items()}
        #print(self.label_dict)
        #print(self.inv_label_dict)



    


    def program(self, show=True, show_comment=True, target=None, machine_code=False, hex_file=None):
        """ Shows the program with human-readable outputs.
        If target parameter is given, it will call the target device's 
        load_prog(addr, prog) method which loads each line of the program
        into the instruction memory.
        If machine_code parameter is set to True, it will show the machine code
        on the screen, which is useful for debugging.
        
        Args:
            show (Bool): decides whether the human-readable output will be shown
            
            target (FPGA device): specify which device to program.
                Target device should have load_prog(addr, prog) method which 
                loads each line of the program into the instruction memory.
                
            machine_code (Bool): specify whether machine_code should be printed.
                If set to True, it will show the machine code
                on the screen, which is useful for debugging.
        
        Returns:
            None
        """
        global each_line
        tabsize=10
        self._update_labels()
        header = '%%0%dd: ' % math.ceil(math.log(len(self.program_list), 10))
        
        if (hex_file != None):
            hex_output = open(hex_file, 'w')
        
        if show:
            print('\n')
        for each_line in self.program_list:
            output = ''
            if each_line[0] in self.inv_label_dict:
                output += ('\n<%s>\n' % self.inv_label_dict[each_line[0]])
            if each_line[1] == 'add':
                output += ((header+'reg[%d] <= reg[%d] + reg[%d] %s') % \
                      (each_line[0], each_line[4], each_line[2], each_line[3], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'addi':
                output += ((header+'reg[%d] <= reg[%d] + %d %s') % \
                      (each_line[0], each_line[4], each_line[2], each_line[5], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]
                
            elif each_line[1] == 'sub':
                output += ((header+'reg[%d] <= reg[%d] - reg[%d] %s') % \
                      (each_line[0], each_line[4], each_line[2], each_line[3], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]
                
            elif each_line[1] == 'subi':
                output += ((header+'reg[%d] <= reg[%d] - %d %s') % \
                      (each_line[0], each_line[4], each_line[2], each_line[5], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'loadi':
                output += ((header+'loadi reg[%d] <= %d %s') % \
                      (each_line[0], each_line[4], each_line[5], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'read':
                output += ((header+'read reg[%d] <= counter[%d] %s') % \
                      (each_line[0], each_line[4], each_line[5], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'set':
                output += ((header+'Update the selected bits at port[%d]. bit pattern:%s, bit mask: %s %s') % \
                      (each_line[0], each_line[4], su.bit_string(each_line[5]), su.bit_string(each_line[6]), \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'write':
                output += ((header+'write {reg[%d], reg[%d], reg[%d], %d} into output FIFO %s') % \
                      (each_line[0], each_line[2], each_line[3], each_line[4], each_line[5], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'blt':
                output += ((header+'Branch to %s if reg[%d] < reg[%d] %s') % \
                      (each_line[0], self._addr_string(each_line[6]), each_line[2], each_line[3], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:6] + [self._get_raw_address(each_line[6])]

            elif each_line[1] == 'blti':
                output += ((header+'Branch to %s if reg[%d] < %d %s') % \
                      (each_line[0], self._addr_string(each_line[6]), each_line[2], 256*each_line[3]+each_line[4], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:6] + [self._get_raw_address(each_line[6])]

            elif each_line[1] == 'beq':
                if each_line[5] == 0xffff:
                    output += ((header+'Branch to %s if reg[%d] == reg[%d] %s') % \
                        (each_line[0], self._addr_string(each_line[6]), \
                        each_line[2], each_line[3], \
                        ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                else:
                    output += ((header+'Branch to %s if reg[%d] == reg[%d] for masked bits(%s) %s') % \
                        (each_line[0], self._addr_string(each_line[6]), \
                        each_line[2], each_line[3], su.bit_string(each_line[5]), \
                        ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                       
                prog = [self.opcode[each_line[1]]]+each_line[2:6] + [self._get_raw_address(each_line[6])]

            elif each_line[1] == 'beqi':
                if each_line[5] == 0xffff:
                    output += ((header+'Branch to %s if reg[%d] == %d %s') % \
                         (each_line[0], self._addr_string(each_line[6]), \
                         each_line[2], 256*each_line[3]+each_line[4], \
                         ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                else:
                    output += ((header+'Branch to %s if reg[%d] == %d for masked bits(%s) %s') % \
                         (each_line[0], self._addr_string(each_line[6]), \
                         each_line[2], 256*each_line[3]+each_line[4], su.bit_string(each_line[5]), \
                         ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)

                prog = [self.opcode[each_line[1]]]+each_line[2:6] + [self._get_raw_address(each_line[6])]

            elif each_line[1] == 'jump':
                output += ((header+'jump to %s %s') % \
                          (each_line[0], self._addr_string(each_line[6]), \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:6] + [self._get_raw_address(each_line[6])]
                    
            elif each_line[1] == 'wait':
                if each_line[6] == 0:
                    output += ((header+'Wait for (reg[%d]) clocks %s') % \
                      (each_line[0], each_line[2], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                else:
                    output += ((header+'Wait for (reg[%d]) clocks or break if trigger_input == %s for masked bits(%s) %s') % \
                         (each_line[0], each_line[2], su.bit_string(each_line[5]), su.bit_string(each_line[6]), \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]
                
            elif each_line[1] == 'waiti':
                if each_line[6] == 0:
                    output += ((header+'Wait for %d clocks %s') % \
                      (each_line[0], 256*each_line[3]+each_line[4], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                else:
                    output += ((header+'Wait for %d clocks or break if trigger_input == %s for masked bits(%s) %s') % \
                         (each_line[0], 256*each_line[3]+each_line[4], su.bit_string(each_line[5]), su.bit_string(each_line[6]), \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]
                
                
            elif each_line[1] == 'stop':
                output += ((header+'Stop %s') % (each_line[0], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'nop':
                output += ((header+'No operation %s') % (each_line[0], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'load_word':
                output += ((header+'load_word reg[%d] <= memory[reg[%d]] %s') % \
                      (each_line[0], each_line[4], each_line[2], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'store_word':
                output += ((header+'store_word memory[reg[%d]] <= reg[%d] %s') % \
                      (each_line[0], each_line[2], each_line[4], \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]

            elif each_line[1] == 'trigger_out':
                output += ((header+'trigger_out for bits(%s) %s') % \
                      (each_line[0], su.bit_string(each_line[5]), \
                      ('\t# %s' % each_line[7]) if (show_comment and each_line[7] != None) else '')).expandtabs(tabsize)
                prog = [self.opcode[each_line[1]]]+each_line[2:]
                    
            else:
                output += ('Unknown command:' + each_line[1])

            if show:
                print(output)
            prog = prog[:4] + [prog[4]//256, prog[4]%256, prog[5]//256, prog[5]%256]
            if machine_code:
                print(each_line[0], prog)
            if target != None:
                target.load_prog(each_line[0], prog)
            if (hex_file != None):
                for each_byte in prog:
                    hex_output.write('%02x' % each_byte)
                hex_output.write('\n')
        if (hex_file != None):
            hex_output.close()


    
if __name__ == '__main__':
    s=SequencerProgram()
    
    s.initialize = s.add(reg[1], reg[2], reg[3])
    s.add(reg[3], 'reg3', 'reg4')
    s.subtract(reg[5], reg[2], reg[3])
    s.test_if_it_works = s.jump('doppler_cooling')
    s.load_immediate(reg[1], 30)
    s.doppler_cooling = s.jump(0)    
    s.where_am_I = s.branch_if_less_than(s.test_if_it_works, reg[1], reg[2])
    s.jump(3)
    s.nop()
    
    
    s.branch_if_equal_with_mask(2, 'reg1', 'reg2', 0)
    s.nop()
    mask,bit = su.make_bit_pattern_from_15_to_0(
            [(15,1), (13,0), (12,0), (11,1), (9, 1), (6, 1)])
    s.test_label = s.set_output_port(0, bit, mask)
    s.stop()
    
    s.program()
    #s.program(arty)
    #s.program(machine_code=True)

                
        