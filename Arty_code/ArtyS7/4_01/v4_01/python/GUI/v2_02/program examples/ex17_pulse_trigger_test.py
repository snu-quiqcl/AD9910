# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Time stamping of pulse picker trigger out and PMT w.r.t. pulse picker single shot

* Definitions
- PT_time: arrival time of pulse trigger out
- PMT1_time: arrival time of PMT1
- PMT2_time: arrival time of PMT2

* The following conditions should be satisfied:
- PT signal should arrive
- one of PMT signal should arrive
- PMT1_time > PT_time or PMT2_time > PT_time

* Collecting statistics of (PMT1-PT_time), (PMT2-PT_time)


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
import export_clipboard_string as cp

###################################################################

debug_mode = 0          # 0 for normal operation. 1 for drawing detailed plots

#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0] # global run number
run_counter_second_loop_R = reg[1]      # second loop run number
sw_flags_R = reg[2]     # stopwatch status flags
pulse_trigger_timing_R = reg[3]   # Arrival time of pulse trigger from pulse picker since single shot output

pulse_missing_count = reg[4]


# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_count =50000              # Number of repeat
max_second_loop = 1             # Number of second loop
Waiting_time = 10          # Doppler cooling time: 1000 * 10ns
pre_waiting_time_for_start = 10         # Waiting time before initiate stopwatches
waiting_time_for_trigger = 15             # Clock counts to wait for stopwatches : 23 * 10ns
max_time_diff_to_record = 140      # If the time difference between PMT and pulse trigger is less than zero or >= max_time_diff_to_record, it won't be counted.

# Counter time resolution is 1.25ns.


## Create a header for data export on a file.

header = \
"************************************************************************* \n"+\
("** The first loop number = %d, The second loop number = %d \n" %(max_run_count, max_second_loop)) +\
("** Total loop number = %d \n" %(max_run_count * max_second_loop)) + \
("** Waiting time = %d ns, " %(Waiting_time*10)) +  \
("** Wait time before initiate stopwatches = %d ns" %(pre_waiting_time_for_start*10)) +\
("** Stopwatch waiting time = %d ns, Maximum recorded time = %d ns \n" %(waiting_time_for_trigger*10, max_time_diff_to_record*1.25)) + \
"************************************************************************* \n"


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

# Initialize counts
s.load_immediate(pulse_missing_count, 0, 'Missing count')

#Reset run_number
s.load_immediate(run_counter_second_loop_R, 0, 'reg[1] will be used for second loop run number')

s.second_loop = \
\
s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')


# Repeating part
# Turn on Doppler cooling and wait
s.repeat = \
\
s.wait_n_clocks(Waiting_time, 'wait for enough cooling')

# Send a 20ns-long pulse to the pulse picker single shot input
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 1)])
s.nop()
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 0)])

s.wait_n_clocks(pre_waiting_time_for_start-3, 'wait while before start stopwatches')

# Start stopwatches
s.trigger_out([hd.pulse_trigger_stopwatch_reset, ], 'Reset stopwatches')
s.nop() # Between reset and start of the stopwatches, add at least one clock
s.trigger_out([hd.pulse_trigger_stopwatch_start, ], 'Start pulse trigger stopwatch')


#%%
s.wait_n_clocks(waiting_time_for_trigger-3, 'Waiting time is compensated for single shot input')
#s.wait_n_clocks_or_masked_trigger(waiting_time_for_trigger-3, [(hd.pulse_trigger_stopwatch_stopped_TLI, 1)], \
#                                  'Wait for an arrival of pulse trigger')

# Collect the result of stopwatch measurements
s.read_counter(sw_flags_R,              hd.Trigger_level, 'Read status of stopwatches')
s.read_counter(pulse_trigger_timing_R, hd.pulse_trigger_stopwatch_result, 'Read pulse trigger stopwatch result')

# The following types of check can be removed, but here they are included for
# debugging purpose

# Check if pulse_trigger has arrived
s.branch_if_equal_with_mask('record', sw_flags_R, \
    1 << hd.pulse_trigger_stopwatch_stopped_TLI , 1 << hd.pulse_trigger_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 10, 'pulse trigger did not arrive')
s.add(pulse_missing_count, pulse_missing_count, 1, 'pulse_missing_count++')
s.jump('decide_repeat')

s.record = \
\
s.load_word_from_memory(reg[10], pulse_trigger_timing_R)
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(pulse_trigger_timing_R, reg[10])


# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')
s.branch_if_less_than('repeat', run_counter_R, max_run_count)

s.write_to_fifo(pulse_missing_count,run_counter_R,run_counter_second_loop_R,0)

s.add(run_counter_second_loop_R, run_counter_second_loop_R, 1, 'second loop number ++')
s.branch_if_less_than('second_loop', run_counter_second_loop_R, max_second_loop)

#
#s.write_to_fifo(pulse_missing_count,run_counter_R,run_counter_second_loop_R,0)

# Transfer the statistics
# We will read three values stored in the consecutive address and write them into FIFO
#s.load_immediate(reg[10], 0, 'reg[10] is used as address pointer and counter')
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

def analyze(data):
    
    arrival_time = []
    pulse_missing = 0
    for each in data:
        if each[3] == 0:
            pulse_missing += each[0]        
        elif each[3] == 100:
            arrival_time += each[0:3]
        else:
            print('Unknown signature:', each)        
    
    print('pulse trigger did not arrive %d times \n' %pulse_missing)
          
#    print(pulse_missing)

    x = np.arange(len(arrival_time))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output ')
    axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
    axs.set_ylabel('Number of event')
    axs.set_yscale('log', nonposy='clip')
    


import datetime
n = 0






    
##%%
import time

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM18') # COM port # : 4(labtop near MIRA), 18 (IonTrap2)
    sequencer.check_version(hd.HW_VERSION)

    #s.program()
    #s.program(hex_file='O:\\Users\\thkim\\Arty_S7\\Sequencer\\v3_04\\v3_04.srcs\\sim_1\\new\\test_hex.mem')
    #s.program(machine_code=True)
    #s.program(target=sequencer, machine_code=True)
    
    start = time.time()
    
    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')
    

    while(sequencer.sequencer_running_status() == 'running'):
        data_count = sequencer.fifo_data_length()
        data =sequencer.read_fifo_data(data_count)
#        for each in data:
#            print(each)
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    if data_count > 0:
        data =sequencer.read_fifo_data(data_count)
#        for each in data:
#            print(each)
        
        
    end = time.time()
    print('elapsed time = ', end - start)
            

    arrival_time = []
    pulse_missing = 0
    for each in data:
        if each[3] == 0:
            pulse_missing += each[0]
        elif each[3] == 100:
            arrival_time += each[0:3]
        else:
            print('Unknown signature:', each)        
    
    print(pulse_missing)
    

          
    import matplotlib.pyplot as plt
    import numpy as np


    x = np.arange(len(arrival_time))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output ')
    axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
    axs.set_ylabel('Number of event')
    axs.set_yscale('log', nonposy='clip')
    
    
    sequencer.close()
