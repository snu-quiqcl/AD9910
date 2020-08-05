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
from ArtyS7_v1_02 import ArtyS7
import HardwareDefinition_type_D as hd

####################################################################
#
## Hardware definition
#
#Channel = 1             # 1 for 1S, 2 for 4G
#
#if Channel == 1:
#    PMT_reset = hd.PMT1_stopwatch_reset 
#    PMT_start = hd.PMT1_stopwatch_start
#    PMT_stopped_TLI = hd.PMT1_stopwatch_stopped_TLI
#    PMT_result = hd.PMT1_stopwatch_result
#    	
#    PMT_counter_reset = hd.PMT1_counter_reset
#    PMT_counter_enable = hd.PMT1_counter_enable
#    PMT_counter_result = hd.PMT1_counter_result
#    
#elif Channel == 2:
#    PMT_reset = hd.PMT2_stopwatch_reset 
#    PMT_start = hd.PMT2_stopwatch_start
#    PMT_stopped_TLI = hd.PMT2_stopwatch_stopped_TLI
#    PMT_result = hd.PMT2_stopwatch_result  
#    		
#    PMT_counter_reset = hd.PMT2_counter_reset
#    PMT_counter_enable = hd.PMT2_counter_enable
#    PMT_counter_result = hd.PMT2_counter_result
#    
#debug_mode = 0          # 0 for normal operation. 1 for drawing detailed plots
#


#%%################################################################
# Reserved registers in this program
###################################################################
run_counter = reg[0] # global run number
wait_counter = reg[1]
# Temporary storage
# reg[10]


# Timing values 
max_run_count = 30                # Number of repeat

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
s.trigger_out([hd.PMT1_counter_reset,hd.PMT2_counter_reset], 'Reset single counter')
s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 1),(hd.PMT2_counter_enable, 1) ], 'Start counter')

s.repeat_wait = \
\
s.wait_n_clocks(T_500us, 'Wait for 50000 * 10 ns unconditionally')
s.add(wait_counter, wait_counter, 1)
s.branch_if_less_than('repeat_wait', wait_counter, N_500us)

s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 0), (hd.PMT2_counter_enable, 0)], 'Stop counter')

s.read_counter(reg[10], hd.PMT1_counter_result)
s.read_counter(reg[11], hd.PMT2_counter_result)
s.add(reg[12], reg[10],reg[11])
s.write_to_fifo(reg[12], reg[10], reg[11], 10, 'Counts within 1 ms')


# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter, run_counter, 1, 'run_counter++')
s.branch_if_less_than('repeat_run', run_counter, max_run_count)
s.stop()


#%%
import time
import statistics

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26')
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
    pmt_log_sum = []
    pmt_log = []
    pmt_log2 = []
    for each in data:
        pmt_log_sum += [each[0]]
        pmt_log += [each[1]]
        pmt_log2 += [each[2]]
    
    mean = statistics.mean(pmt_log)
    stdev = statistics.stdev(pmt_log)
    mean2 = statistics.mean(pmt_log2)
    stdev2 = statistics.stdev(pmt_log2)
    print(pmt_log)
    print(pmt_log2)
    print(mean, stdev, mean2, stdev2)
    
    sequencer.close()
