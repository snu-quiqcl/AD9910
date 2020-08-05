# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Count the number of rising edge of the RF signal during fixed time

"""

import sys
import os
new_path = os.path.dirname(__file__) + '\\..'
if not (new_path in sys.path):
    sys.path.append(new_path)

from SequencerProgram_v1_07 import SequencerProgram, reg
import SequencerUtility_v1_01 as su
from ArtyS7_v1_01 import ArtyS7
import HardwareDefinition_type_A as hd

#%%################################################################
# Reserved registers in this program
###################################################################
run_counter = reg[0] # global run number
wait_counter = reg[1]
# Temporary storage
# reg[10]


# Timing values 
max_run_count = 10                 # Number of repeat

T_500us = 50000-3-2     # Clock counts for 500us (subtract 3 clocks for wait_command and subtract 2 clocks for repeat decision)
N_500us = 2     # 1000us


#%%    
s=SequencerProgram()

#Reset run_number
s.load_immediate(run_counter, 0, 'reg[0] will be used for run number')

# Start of the repeating part
s.repeat_run = \
\
s.load_immediate(wait_counter, 0)
s.trigger_out([hd.jb_4_counter_reset], 'Reset single counter')
s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 1), ], 'Start counter')

s.repeat_wait = \
\
s.wait_n_clocks(T_500us, 'Wait for 50000 * 10 ns unconditionally')
s.add(wait_counter, wait_counter, 1)
s.branch_if_less_than('repeat_wait', wait_counter, N_500us)

s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 0), ], 'Stop counter')

s.read_counter(reg[10], hd.PMT1_counter_result)
s.write_to_fifo(run_counter, reg[10], reg[10], 10, 'Counts within 1 ms')


# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter, run_counter, 1, 'run_counter++')
s.branch_if_less_than('repeat_run', run_counter, max_run_count)
s.stop()


#%%
import time

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM18')
    sequencer.check_version(hd.HW_VERSION)

    #sequencer.check_waveform_capture() # Check the status of trigger


    #s.program()
    #s.program(hex_file='O:\\Users\\thkim\\Arty_S7\\Sequencer\\v3_04\\v3_04.srcs\\sim_1\\new\\test_hex.mem')
    #s.program(machine_code=True)
    #s.program(target=sequencer, machine_code=True)
    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')

    time.sleep(1)
    
    data_count = sequencer.fifo_data_length()
    print('FIFO data length:', data_count)

    data =sequencer.read_fifo_data(data_count)
    """
    example_data = [[63488, 183, 199, 0], [213, 229, 246, 100]]
    for n in range(data_count//2):
        #print(n)
        if data[2*n] != example_data[0]:
            print('1st data (%s) is different from %s' % (data[2*n], example_data[0]))
        if data[2*n+1] != example_data[1]:
            print('2nd data (%s) is different from %s' % (data[2*n+1], example_data[1]))
    """
    for each in data:
        print(each)
    #assign monitoring_32bits = {output_ports[0], stopped, manual_control_on, {(14-INSTRUCTION_MEMORY_ADDR_WIDTH){1'b0}}, PC[INSTRUCTION_MEMORY_ADDR_WIDTH-1:0]};
    print(sequencer.escape_read() )
