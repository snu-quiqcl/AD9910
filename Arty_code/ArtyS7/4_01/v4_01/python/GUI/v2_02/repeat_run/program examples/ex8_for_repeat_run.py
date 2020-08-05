# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Time stamping of pulse picker trigger out w.r.t. pulse picker single shot

* Definitions
 - PT_time: arrival time of pulse trigger out
 
* The following conditions should be satisfied:
  - Pulse trigger signals should arrive after the stopwatch is started
  
* Collecting distribution of PT_time


"""
import sys
import os
#new_path = os.path.dirname(__file__) + '\\..'
#if not (new_path in sys.path):
#    sys.path.append(new_path)

from SequencerProgram_v1_07 import SequencerProgram, reg
import SequencerUtility_v1_01 as su
from ArtyS7_v1_01 import ArtyS7
import HardwareDefinition_type_A as hd

#%%

#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0] # global run number
sw_flags_R = reg[1]     # stopwatch status flags
pulse_trigger_timing_R = reg[2]   # Arrival time of pulse trigger from pulse picker since single shot output

# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_count = 1000                # Number of repeat
# There is significant delay between single shot and the pulse picker trigger, so I should give enough clocks for max_time_diff_to_record
# It is better to choose max_time_diff_to_record as multiples of 3, because statistics will be transferred in block of 3 items
max_time_diff_to_record = 202       # Maximum stopwatch value to record. If the stopwatch output is less than zero or >= max_time_diff_to_record, it won't be counted.

waiting_time_for_stopwatch = 150-3       # Clock counts to wait for stopwatch expiration: 10 * 10ns

# Counter time resolution is 1.25ns.


#%%    

s=SequencerProgram()


# Initialize the memory
s.load_immediate(reg[11], 0) # Reset value for the momery initialization
s.load_immediate(reg[10], 0)
s.memory_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_initialization', reg[10], max_time_diff_to_record)


#Reset run_number
s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')


################################################################
# Repeating part
################################################################
# Start stopwatches
s.repeat = \
\
s.trigger_out([hd.pulse_trigger_stopwatch_reset, ], 'Reset stopwatch')
s.nop() # Between reset and start of the stopwatches, add at least one clock
s.trigger_out([hd.pulse_trigger_stopwatch_start, ], 'Start stopwatch')

# Send a 20ns-long pulse to the pulse picker single shot input
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 1)])
s.nop()
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 0)])



"""
#%%
# For the test, the single_shot_out (jb_7) is already connected to ja_2 (pulse_trigger) input with coax cable

# Remove this block in real experiment
"""

#%%

s.wait_n_clocks(waiting_time_for_stopwatch-3, 'Waiting time is compensated for single shot input')


# Collect the result of stopwatch measurements
s.read_counter(sw_flags_R,              hd.Trigger_level, 'Read status of stopwatches')
s.read_counter(pulse_trigger_timing_R, hd.pulse_trigger_stopwatch_result, 'Read pulse trigger stopwatch result')


# The following types of check can be removed, but here they are included for
# debugging purpose

# Check if pulse_trigger has arrived
s.branch_if_equal_with_mask('store_time_difference', sw_flags_R, \
    1 << hd.pulse_trigger_stopwatch_stopped_TLI , 1 << hd.pulse_trigger_stopwatch_stopped_TLI)
s.write_to_fifo(run_counter_R, sw_flags_R, pulse_trigger_timing_R, 10, 'pulse trigger did not arrive')
s.jump('decide_repeat')


s.store_time_difference = \
\
s.load_word_from_memory(reg[10], pulse_trigger_timing_R)
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(pulse_trigger_timing_R, reg[10])
#s.write_to_fifo(run_counter_R, sw_flags_R, pulse_trigger_timing_R, 0, 'Store time difference')



# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')



# If I don't wait long enough, the output FIFO will be filled up too quickly, 
# and not all the output data can be sent to PC. In this case, I should reduce the number of run
# or add extreme delay between each run to slow down the writing.
s.wait_n_clocks(50000)
s.wait_n_clocks(50000)
s.wait_n_clocks(50000)
s.wait_n_clocks(50000)



s.branch_if_less_than('repeat', run_counter_R, max_run_count)



# Transfer the statistics
# We will read three values stored in the consecutive address and write them into FIFO
s.load_immediate(reg[10], 0, 'reg[10] is used as address pointer and counter')
s.transfer_statistics = \
\
s.load_word_from_memory(reg[11], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[12], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[13], reg[10])
s.add(reg[10], reg[10], 1)
s.write_to_fifo(reg[11], reg[12], reg[13], 100)
s.branch_if_less_than('transfer_statistics', reg[10], max_time_diff_to_record)

s.stop()


import matplotlib.pyplot as plt
import numpy as np

import random
#example_global_variable = 0 # This is a global variable whose value will be maintained between calls
def update_plot(data, axs, statusBar):
    """
    # If we want to hand over some previous result to the next call, global variables can be used by declaring 
    global example_global_variable
    example_global_variable += 1
    print(example_global_variable)
    """

    """
    data = [
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 47, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 50, 0, 100],
        [422, 885, 1014, 100],
        [864, 972, 848, 100],
        [1093, 923, 876, 100],
        [912, 962, 132, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        [0, 0, 0, 100],
        ]
    """        
    
    # Generating random distribution for example
    data = [[0, 0, 0, 10], [0, 0, 0, 10]]
    for n in range(20):
        data.append([int(100*random.random()), int(100*random.random()), int(100*random.random()), 100])


        
    pulse_trigger_not_arrive_count = 0
    arrival_time = []
    for each in data:
        if each[3] == 10:
            pulse_trigger_not_arrive_count += 1
        elif each[3] == 100:
            arrival_time += each[0:3]
        else:
            print('Unknown signature:', each)

    x = np.arange(len(arrival_time))
    #fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
     
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Arrival time distribution of pulse picker trigger output w.r.t. stopwatch start')
    axs.set_xlabel('Arrival time of pulse picker trigger output w.r.t. stopwatch start (ns)')
    axs.set_ylabel('Number of event')
    
    statusBar.setText('Number of events when the pulse trigger did not arrive: %d' % pulse_trigger_not_arrive_count)





#%%
import time

if __name__ == '__main__':
    #s.program()
    #s.program(hex_file='O:\\Users\\thkim\\Arty_S7\\Sequencer\\v3_04\\v3_04.srcs\\sim_1\\new\\test_hex.mem')
    #s.program(machine_code=True)
    #s.program(target=sequencer, machine_code=True)
    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')

    data = []
    while(sequencer.sequencer_running_status() == 'running'):
        data_count = sequencer.fifo_data_length()
        if data_count > ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
            data_count = ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
        data += sequencer.read_fifo_data(data_count)
        #for each in data:
        #    print(each)
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    while (data_count > 0):
        data += sequencer.read_fifo_data(data_count)
        if data_count > ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
            data_count = ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
        #data =sequencer.read_fifo_data(data_count)
        #for each in data:
        #    print(each)
        data_count = sequencer.fifo_data_length()


    for each in data:
    #for each in data[:2*max_run_count]:
    #for each in data[2*max_run_count:]:
        print(each)

""" 
data = [
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 47, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 50, 0, 100],
[422, 885, 1014, 100],
[864, 972, 848, 100],
[1093, 923, 876, 100],
[912, 962, 132, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
[0, 0, 0, 100],
]



"""
