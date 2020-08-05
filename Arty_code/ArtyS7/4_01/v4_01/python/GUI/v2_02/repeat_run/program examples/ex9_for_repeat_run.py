# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Time stamping of pulse picker trigger out and PMT1 w.r.t. pulse picker single shot

* Definitions
- PT_time: arrival time of pulse trigger out
- PMT1_time: arrival time of PMT1

* The following conditions should be satisfied:
- Both signals should arrive
- PMT1_time > PT_time

* Collecting statistics of (PMT1-PT_time)


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
run_level1_counter_R = reg[0] # global run level1 counter
run_level2_counter_R = reg[5] # global run level2 counter
sw_flags_R = reg[1]     # stopwatch status flags
pulse_trigger_timing_R = reg[2]   # Arrival time of pulse trigger from pulse picker since single shot output
PMT1_timing_R = reg[3] # Arrival time of PMT1 signal since single shot output
time_diff_R = reg[4]   # time difference between PMT1 and pulse_trigger

# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_level1_count = 10               # Number of repeat1
max_run_level2_count = 60000               # Number of repeat2
Doppler_cooling_time = 100-3          # Doppler cooling time: 100 * 10ns
time_bet_cooling_and_pulse = 10-3       # Clock counts to wait before pulse: 10 * 10ns
waiting_time_for_stopwatch = 100-3       # Clock counts to wait for both stopwatches: 10 * 10ns
max_time_diff_to_record = 162      # If the time difference between PMT and pulse trigger is less than zero or >= max_time_diff_to_record, it won't be counted.

# Counter time resolution is 1.25ns.



#%%    

s=SequencerProgram()


# Doppler cool the 174Yb ion
s.set_output_port(hd.external_control_port, [(hd.C1_AOM_200MHz_out, 1), \
    (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')

    
# Initialize the memory
s.load_immediate(reg[11], 0) # Reset value for the momery initialization
s.load_immediate(reg[10], 0)
s.memory_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_initialization', reg[10], max_time_diff_to_record)


#Reset run_number
s.load_immediate(run_level1_counter_R, 0, 'reg[0] will be used for run number')
# Repeating part1
s.level1_repeat = \
\
s.load_immediate(run_level2_counter_R, 0, 'reg[5] will be used for run number')


# Repeating part
# Turn on Doppler cooling and wait
s.level2_repeat = \
\
s.set_output_port(hd.external_control_port, [(hd.C1_AOM_200MHz_out, 1),])
s.wait_n_clocks(Doppler_cooling_time, 'wait for enough cooling')

# Turn off Doppler cooling and wait for enough time until the previously excited electron will decay
s.set_output_port(hd.external_control_port, [(hd.C1_AOM_200MHz_out, 0),])
s.wait_n_clocks(time_bet_cooling_and_pulse, 'wait for enough time for previous decay')

# Should I add ion loss check?

# Start stopwatches
s.trigger_out([hd.PMT1_stopwatch_reset , hd.pulse_trigger_stopwatch_reset, ], 'Reset stopwatches')
s.nop() # Between reset and start of the stopwatches, add at least one clock
s.trigger_out([hd.PMT1_stopwatch_start, hd.pulse_trigger_stopwatch_start, ], 'Start stopwatches')

# Send a 20ns-long pulse to the pulse picker single shot input
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 1)])
s.nop()
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 0)])



#%%
s.wait_n_clocks(waiting_time_for_stopwatch-3, 'Waiting time is compensated for single shot input')


# Collect the result of stopwatch measurements
s.read_counter(sw_flags_R,              hd.Trigger_level, 'Read status of stopwatches')
s.read_counter(pulse_trigger_timing_R, hd.pulse_trigger_stopwatch_result, 'Read pulse trigger stopwatch result')
s.read_counter(PMT1_timing_R,           hd.PMT1_stopwatch_result, 'Read PMT1 stopwatch result')


# The following types of check can be removed, but here they are included for
# debugging purpose

# Check if pulse_trigger has arrived
s.branch_if_equal_with_mask('check_PMT1_triggered', sw_flags_R, \
    1 << hd.pulse_trigger_stopwatch_stopped_TLI , 1 << hd.pulse_trigger_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 10, 'pulse trigger did not arrive')
s.jump('decide_repeat')


# Check if PMT1 trigger is detected
s.check_PMT1_triggered = \
\
s.branch_if_equal_with_mask('check_if_pulse_trigger_arrived_before_PMT1', sw_flags_R, \
    1 << hd.PMT1_stopwatch_stopped_TLI, 1 << hd.PMT1_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 20, 'PMT1 trigger did not arrive')
s.jump('decide_repeat')


# Check if pulse trigger arrived before PMT1
s.check_if_pulse_trigger_arrived_before_PMT1 = \
\
s.branch_if_less_than('calculate_time_difference', pulse_trigger_timing_R, PMT1_timing_R)
s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 30, 'pulse trigger arrived after PMT1')
s.jump('decide_repeat')


# Calculate time difference and decide whether it lies between the desired range
s.calculate_time_difference = \
\
s.subtract(time_diff_R, PMT1_timing_R, pulse_trigger_timing_R)
s.branch_if_less_than('store_time_difference', time_diff_R, max_time_diff_to_record)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 40, 'Time difference is larger than criteria')
s.jump('decide_repeat')


s.store_time_difference = \
\
s.load_word_from_memory(reg[10], time_diff_R)
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(time_diff_R, reg[10])
#s.write_to_fifo(run_counter_R, sw_flags_R, time_diff_R, 0, 'Store time difference')
#s.write_to_fifo(run_counter_R, pulse_trigger_timing_R, PMT1_timing_R, 1, 'Store time difference')


# Decide whether we will repeat run level2
s.decide_repeat = \
\
s.add(run_level2_counter_R, run_level2_counter_R, 1, 'run_level2_counter_R++')
s.branch_if_less_than('level2_repeat', run_level2_counter_R, max_run_level2_count)
# End of run level2 repetition

s.add(run_level1_counter_R, run_level1_counter_R, 1, 'run_level1_counter_R++')
s.branch_if_less_than('level1_repeat', run_level1_counter_R, max_run_level1_count)


# Leave the Doppler cooling on
s.set_output_port(hd.external_control_port, [(hd.C1_AOM_200MHz_out, 1),])


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


import random
def update_plot(data, axs, status_bar):
    """
    # Generating random distribution for example
    data = []
    for n in range(int(100*random.random())):
        data.append([n+1, 0, 0, 30])
    for n in range(40):
        data.append([int(100*random.random()), int(100*random.random()), int(100*random.random()), 100])
    # End of generating random distribution for example
    """   
            
    pulse_trigger_arrived_after_PMT1 = 0
    arrival_time = []
    error_case = []
    for each in data:
        if each[3] == 30:
            pulse_trigger_arrived_after_PMT1 += 1
            error_case.append(each)

        elif each[3] == 100:
            arrival_time += each[0:3]
        else:
            print('Unknown signature:', each)
            error_case.append(each)

    axs.cla() # Delete the previously plotted data
    x = np.arange(len(arrival_time))
     
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Arrival time distribution of pulse picker trigger output w.r.t. stopwatch start')
    axs.set_xlabel('Arrival time of pulse picker trigger output w.r.t. stopwatch start (ns)')
    axs.set_ylabel('Number of event')

    status_message = 'Successed trial = %d\n' % sum(arrival_time)
    status_message += 'Overall trial = %d\n' % (max_run_level1_count *max_run_level2_count)
    status_message += 'Success rate = %f' % (sum(arrival_time)/(max_run_level1_count *max_run_level2_count))
    status_bar.setText(status_message)
    
    #print(error_case)
    
#%%
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
    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')

    while(sequencer.sequencer_running_status() == 'running'):
        data_count = sequencer.fifo_data_length()
        data =sequencer.read_fifo_data(data_count)
        for each in data:
            print(each)
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    if data_count > 0:
        data =sequencer.read_fifo_data(data_count)
        for each in data:
            print(each)
            
    arrival_time = []
    for each in data:
        arrival_time += each[0:3]
    # np.sum(arrival_time) => 18079 out of 60000 trials
    
    print('Successed trial =',sum(arrival_time))
    print('Overall trial =',max_run_level1_count *max_run_level2_count)
    print('Success rate =',sum(arrival_time)/ (max_run_level1_count *max_run_level2_count))
    
    
    print(arrival_time)
    
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(len(arrival_time))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output')
    axs.set_xlabel('PMT arrival time w.r.t. pulse picker trigger output (ns)')
    axs.set_ylabel('Number of event')

