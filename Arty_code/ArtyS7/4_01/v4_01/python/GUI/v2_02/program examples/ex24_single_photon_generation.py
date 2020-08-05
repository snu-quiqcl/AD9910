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
from ArtyS7_v1_02 import ArtyS7
import HardwareDefinition_type_D as hd
import export_clipboard_string as cp

###################################################################

# Hardware definition

Channel = 2             # 1 for 1S, 2 for 4G

if Channel == 1:
    AOM_out = hd.C1_AOM_switch_out
    #AOM_out = hd.C1_AOM_on_out
elif Channel == 2:
    AOM_out = hd.C2_AOM_on_out
    
debug_mode = 1          # 0 for normal operation. 1 for drawing detailed plots


# Post process parameters
max_index = 43                  # predefined max_index
Back_scattering_cut = 3         # 3*1.25 = 3.75 ns cut
scattering_threshold = 64       # 64*1.25 = 80 ns (~ 10 tau)


#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0] # global run number
run_counter_second_loop_R = reg[1]      # second loop run number
sw_flags_R = reg[2]     # stopwatch status flags
pulse_trigger_timing_R = reg[3]   # Arrival time of pulse trigger from pulse picker since single shot output
PMT1_timing_R = reg[4] # Arrival time of PMT1 signal since single shot output
PMT2_timing_R = reg[5]
time_diff1_R = reg[6]   # time difference between PMT1 and pulse_trigger
time_diff2_R = reg[7]

pulse_missing_R = reg[8]

trigger_precut_R = reg[13]



# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_count = 10000               # Number of repeat
max_second_loop = 5 # 500             # Number of second loop
Doppler_cooling_time = 100-3          # Doppler cooling time: 1000 * 10ns
time_bet_cooling_and_pulse = 100-3       # Clock counts to wait before pulse: 50 * 10ns
pre_waiting_time_for_start = 19         # Waiting time before initiate stopwatches
waiting_time_for_trigger = 23             # Clock counts to wait for stopwatches : 23 * 10ns
max_time_diff_to_record = 105      # If the time difference between PMT and pulse trigger is less than zero or >= max_time_diff_to_record, it won't be counted.

trigger_precut = 5               # if trigger comes before precut(tick), ignore that. 

pointer_for_PMT1_record = 0
pointer_for_PMT2_record = 250
pointer_for_Pulse_Trigger_record = 500
# Counter time resolution is 1.25ns.


## Create a header for data export on a file.

header = \
"############################################################################## \n"+\
("## The first loop number = %d, The second loop number = %d \n" %(max_run_count, max_second_loop)) +\
("## Total loop number = %d \n" %(max_run_count * max_second_loop)) + \
("## Doppler cooling time = %d ns, " %(Doppler_cooling_time*10)) +  \
("## Wait time before send pulse output = %d ns \n" %(time_bet_cooling_and_pulse*10)) + \
("## Wait time before initiate stopwatches = %d ns \n" %(pre_waiting_time_for_start*10)) +\
("## Stopwatch waiting time = %d ns, Maximum recorded time = %d ns \n" %(waiting_time_for_trigger*10, max_time_diff_to_record*1.25)) + \
("## Pulse triggers arrived before %1.2f ns are ignored due to data distortion \n" %(trigger_precut*1.25)) + \
"############################################################################## \n"




#%%    

s=SequencerProgram()


# Doppler cool the 174Yb ion
s.set_output_port(hd.external_control_port, [(AOM_out , 1), \
    (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')


s.load_immediate(trigger_precut_R, trigger_precut)
s.load_immediate(reg[9], 0)
    
# Initialize the memory
s.load_immediate(reg[11], 0) # Reset value for the momery initialization
s.load_immediate(reg[10], 0)
#s.memory_initialization = \
#\
#s.store_word_to_memory(reg[10], reg[11])
#s.add(reg[10], reg[10], 1)
#s.branch_if_less_than('memory_initialization', reg[10], max_time_diff_to_record)

s.load_immediate(reg[10],pointer_for_PMT1_record)

s.memory_2_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_2_initialization', reg[10], max_time_diff_to_record+pointer_for_PMT1_record)


s.load_immediate(reg[10],pointer_for_PMT2_record)

s.memory_3_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_3_initialization', reg[10], max_time_diff_to_record+pointer_for_PMT2_record)


s.load_immediate(reg[10],pointer_for_Pulse_Trigger_record)

s.memory_4_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_4_initialization', reg[10], max_time_diff_to_record+pointer_for_Pulse_Trigger_record)


#Reset run_number
s.load_immediate(run_counter_second_loop_R, 0, 'reg[5] will be used for second loop run number')

s.second_loop = \
\
s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')

s.load_immediate(pulse_missing_R, 0, 'reset pulse missing count')

# Repeating part
# Turn on Doppler cooling and wait
s.repeat = \
\
s.set_output_port(hd.external_control_port, [(AOM_out , 1),])
s.wait_n_clocks(Doppler_cooling_time, 'wait for enough cooling')

# Turn off Doppler cooling and wait for enough time until the previously excited electron will decay
s.set_output_port(hd.external_control_port, [(AOM_out , 0),])
s.wait_n_clocks(time_bet_cooling_and_pulse, 'wait for enough time for previous decay')

# Should I add ion loss check?

# Send a 20ns-long pulse to the pulse picker single shot input
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 1)])
s.nop()
s.set_output_port(hd.external_control_port, [(hd.single_shot_out, 0)])

s.wait_n_clocks(pre_waiting_time_for_start-3, 'wait while before start stopwatches')

# Start stopwatches
s.trigger_out([hd.PMT1_stopwatch_reset, hd.PMT2_stopwatch_reset, hd.pulse_trigger_stopwatch_reset, ], 'Reset stopwatches')
s.nop() # Between reset and start of the stopwatches, add at least one clock
s.trigger_out([hd.PMT1_stopwatch_start, hd.PMT2_stopwatch_start, hd.pulse_trigger_stopwatch_start, ], 'Start pulse trigger stopwatch')


#%%
s.wait_n_clocks(waiting_time_for_trigger-3, 'Waiting time is compensated for single shot input')
#s.wait_n_clocks_or_masked_trigger(waiting_time_for_trigger-3, [(hd.pulse_trigger_stopwatch_stopped_TLI, 1)], \
#                                  'Wait for an arrival of pulse trigger')

# Leave the Doppler cooling on
s.set_output_port(hd.external_control_port, [(AOM_out , 1),])

# Collect the result of stopwatch measurements
s.read_counter(sw_flags_R,              hd.Trigger_level, 'Read status of stopwatches')
s.read_counter(pulse_trigger_timing_R, hd.pulse_trigger_stopwatch_result, 'Read pulse trigger stopwatch result')
s.read_counter(PMT1_timing_R,           hd.PMT1_stopwatch_result, 'Read PMT1 stopwatch result')
s.read_counter(PMT2_timing_R,           hd.PMT2_stopwatch_result, 'Read PMT2 stopwatch result')


# The following types of check can be removed, but here they are included for
# debugging purpose

# Check if pulse_trigger has arrived
s.branch_if_equal_with_mask('check_if_pulse_trigger_arrived_after_precut', sw_flags_R, \
    1 << hd.pulse_trigger_stopwatch_stopped_TLI , 1 << hd.pulse_trigger_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 10, 'pulse trigger did not arrive')
s.add(pulse_missing_R, pulse_missing_R, 1, 'pulse_missing_R++')
s.jump('decide_repeat')

# check if pulse trigger arrived after trigger_precut. (this case makes the second pulse)
s.check_if_pulse_trigger_arrived_after_precut = \
\
s.branch_if_less_than('check_PMT1_triggered', trigger_precut_R, pulse_trigger_timing_R)
s.jump('decide_repeat')



# Check if PMT1 trigger is detected
s.check_PMT1_triggered = \
\
s.branch_if_equal_with_mask('calculate_time_difference_PMT1', sw_flags_R, \
    1 << hd.PMT1_stopwatch_stopped_TLI, 1 << hd.PMT1_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 20, 'PMT1 trigger did not arrive')
s.jump('check_PMT2_triggered')


# Check if pulse trigger arrived before PMT1
#s.check_if_pulse_trigger_arrived_before_PMT1 = \
#\
#s.branch_if_less_than('calculate_time_difference_PMT1', pulse_trigger_timing_R, PMT1_timing_R)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 30, 'pulse trigger arrived after PMT1')
#s.jump('check_PMT2_triggered')



# Calculate time difference and decide whether it lies between the desired range
s.calculate_time_difference_PMT1 = \
\
s.subtract(time_diff1_R, PMT1_timing_R, pulse_trigger_timing_R)
#s.branch_if_less_than('store_time_difference_PMT1', time_diff1_R, max_time_diff_to_record)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 40, 'Time difference is larger than criteria')
#s.jump('check_PMT2_triggered')



s.store_time_difference_PMT1 = \
\
s.add(reg[11], time_diff1_R, pointer_for_PMT1_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])
s.write_to_fifo(PMT1_timing_R, pulse_trigger_timing_R, run_counter_R, 900)


s.load_immediate(reg[9], 1)

# Store pulse trigger arrival time distribution
s.add(reg[11], pulse_trigger_timing_R, pointer_for_Pulse_Trigger_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])



#s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')

#s.write_to_fifo(run_counter_R, sw_flags_R, time_diff_R, 0, 'Store time difference')
#s.write_to_fifo(run_counter_R, pulse_trigger_timing_R, PMT1_timing_R, 1, 'Store time difference')

# Check if PMT2 trigger is detected
s.check_PMT2_triggered = \
\
s.branch_if_equal_with_mask('calculate_time_difference_PMT2', sw_flags_R, \
    1 << hd.PMT2_stopwatch_stopped_TLI, 1 << hd.PMT2_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT2_timing_R, 20, 'PMT2 trigger did not arrive')
s.jump('decide_repeat')


# Check if pulse trigger arrived before PMT2
#s.check_if_pulse_trigger_arrived_before_PMT2 = \
#\
#s.branch_if_less_than('calculate_time_difference_PMT2', pulse_trigger_timing_R, PMT2_timing_R)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT2_timing_R, 30, 'pulse trigger arrived after PMT2')
#s.jump('decide_repeat')
#


# Calculate time difference and decide whether it lies between the desired range
s.calculate_time_difference_PMT2 = \
\
s.subtract(time_diff2_R, PMT2_timing_R, pulse_trigger_timing_R)
#s.branch_if_less_than('store_time_difference_PMT2', time_diff2_R, max_time_diff_to_record)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT2_timing_R, 40, 'Time difference is larger than criteria')
#s.jump('decide_repeat')



s.store_time_difference_PMT2 = \
\
s.add(reg[11], time_diff2_R, pointer_for_PMT2_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])
s.write_to_fifo(PMT2_timing_R, pulse_trigger_timing_R, run_counter_R, 901)


s.check_if_pulse_trigger_saved =\
\
s.branch_if_equal('check_both_PMT_triggered', reg[9], 1)

# Store pulse trigger arrival time distribution
s.add(reg[11], pulse_trigger_timing_R, pointer_for_Pulse_Trigger_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])


s.check_both_PMT_triggered = \
\
s.branch_if_equal_with_mask('record_coincidence_detection', sw_flags_R, \
    (1 << hd.PMT1_stopwatch_stopped_TLI) + (1 << hd.PMT2_stopwatch_stopped_TLI), (1 << hd.PMT1_stopwatch_stopped_TLI) + (1 << hd.PMT2_stopwatch_stopped_TLI))
s.jump('decide_repeat')

s.record_coincidence_detection = \
\
s.write_to_fifo(time_diff1_R, time_diff2_R, pulse_trigger_timing_R, 111, 'Coincidence measurement')

# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')
s.load_immediate(reg[9], 0)
s.branch_if_less_than('repeat', run_counter_R, max_run_count)


s.write_to_fifo(pulse_missing_R,run_counter_R,run_counter_second_loop_R, 10)

s.add(run_counter_second_loop_R, run_counter_second_loop_R, 1, 'second loop number ++')
s.branch_if_less_than('second_loop', run_counter_second_loop_R, max_second_loop)


# Leave the Doppler cooling on
s.set_output_port(hd.external_control_port, [(AOM_out , 1),])


# Transfer the statistics
# We will read three values stored in the consecutive address and write them into FIFO
#s.load_immediate(reg[10], 0, 'reg[10] is used as address pointer and counter')
s.load_immediate(reg[10], pointer_for_PMT1_record, 'reg[10] is used as address pointer and counter')
s.transfer_statistics = \
\
s.load_word_from_memory(reg[11], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[12], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[13], reg[10])
s.add(reg[10], reg[10], 1)
s.write_to_fifo(reg[11], reg[12], reg[13], 100)
s.branch_if_less_than('transfer_statistics', reg[10], max_time_diff_to_record+pointer_for_PMT1_record)

s.load_immediate(reg[10], pointer_for_PMT2_record, 'reg[10] is used as address pointer and counter')
s.transfer_statistics_2 = \
\
s.load_word_from_memory(reg[11], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[12], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[13], reg[10])
s.add(reg[10], reg[10], 1)
s.write_to_fifo(reg[11], reg[12], reg[13], 200)
s.branch_if_less_than('transfer_statistics_2', reg[10], max_time_diff_to_record+pointer_for_PMT2_record)

s.load_immediate(reg[10], pointer_for_Pulse_Trigger_record, 'reg[10] is used as address pointer and counter')
s.transfer_statistics_3 = \
\
s.load_word_from_memory(reg[11], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[12], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[13], reg[10])
s.add(reg[10], reg[10], 1)
s.write_to_fifo(reg[11], reg[12], reg[13], 300)
s.branch_if_less_than('transfer_statistics_3', reg[10], max_time_diff_to_record+pointer_for_Pulse_Trigger_record)

s.stop()




import matplotlib.pyplot as plt
import numpy as np

def analyze(data):
    pulse_trigger_not_arrive_count = 0

    PMT1_arrival_time = []
    PMT2_arrival_time = []
    pulse_arrival_time = []
    coincidence_list = []
    for each in data:
        if each[3] == 100:
            PMT1_arrival_time += each[0:3]
        elif each[3] == 200:
            PMT2_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
#            pulse_trigger_not_arrive_count += 1
        elif each[3] == 111:            
            coincidence_list.append(each)
        else:
            print('Unknown signature:', each)
    
    arrival_time = PMT1_arrival_time        
    for i in range(len(PMT1_arrival_time)):
        arrival_time[i] += PMT2_arrival_time[i]
        
    
    print('pulse trigger did not arrive %d times \n' %pulse_trigger_not_arrive_count)

    max_count = max(arrival_time)    
    max_index = arrival_time.index(max_count)
    
    #photon_count = sum(arrival_time[max_index+Back_scattering_cut:max_index+scattering_threshold])
    photon_count = sum(arrival_time[max_index:max_index+scattering_threshold])
    print('successful photon scattering = ', photon_count)
    print('total trial = ', max_run_count*max_second_loop)
    print('success rate = ', photon_count/max_run_count/max_second_loop)
    
          

    x = np.arange(len(arrival_time))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output ')
    axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
    axs.set_ylabel('Number of event')
    axs.set_yscale('log', nonposy='clip')
    
    if debug_mode:

        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.cla()
        
        axs.bar(x*1.25, PMT1_arrival_time)
        axs.set_title('PMT1 trigger time distribution w.r.t. stopwatch start')
        axs.set_xlabel('PMT1 trigger time distribution w.r.t. stopwatch start (ns)')
        axs.set_ylabel('Number of event')
        axs.set_yscale('log', nonposy='clip')
        
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.cla()
        
        axs.bar(x*1.25, PMT2_arrival_time)
        axs.set_title('PMT2 trigger time distribution w.r.t. stopwatch start')
        axs.set_xlabel('PMT2 trigger time distribution w.r.t. stopwatch start (ns)')
        axs.set_ylabel('Number of event')
        axs.set_yscale('log', nonposy='clip')
    
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.cla()
        
        axs.bar(x*1.25, pulse_arrival_time)
        axs.set_title('Pulse picker trigger output time distribution w.r.t. stopwatch start')
        axs.set_xlabel('Pulse picker trigger output time distribution w.r.t. stopwatch start (ns)')
        axs.set_ylabel('Number of event')
        axs.set_yscale('log', nonposy='clip')
#    
#    cp.send_clipboard()


import datetime
n = 0

def count_for_plot(data, status_bar):
    global n, header
    
    pulse_trigger_not_arrive_count = 0

    PMT1_arrival_time = []
    PMT2_arrival_time = []
    pulse_arrival_time = []
    coincidence_list = []
    for each in data:
        if each[3] == 100:
            PMT1_arrival_time += each[0:3]
        elif each[3] == 200:
            PMT2_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        elif each[3] == 111:            
            coincidence_list.append(each)
        else:
            print('Unknown signature:', each)
    
    arrival_time = PMT1_arrival_time       
    for i in range(len(PMT1_arrival_time)):
        arrival_time[i] += PMT2_arrival_time[i]
    
    #print('pulse trigger did not arrive %d times \n' %pulse_trigger_not_arrive_count)
          
          
    # np.sum(arrival_time) => 18079 out of 60000 trials
    
    max_count = max(arrival_time)
#    max_index = arrival_time.index(max_count)
    
    threshold = max_index + Back_scattering_cut
    cutoff = scattering_threshold
        
#    threshold = 86  # peak data number = 83, 5 tick after the peak
#    cutoff = 60


    print('Successed trial =',sum(arrival_time))
    print('Overall trial =',max_run_count*max_second_loop)
    print('Success rate =',sum(arrival_time)/max_run_count/max_second_loop)
    
    # print(arrival_time)
    
    datestr = datetime.datetime.now().strftime("%Y-%m-%d")
    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    namestr = 'Ex16_SinglePhoton'
    #filename = 'O:\\Users\\thkim\\Arty_S7\\Sequencer\\v4_00\\python\\' + timestr +  '.csv'
    filename = 'O:\\Users\\JKKim\\data\\' +datestr +'\\'  + timestr + '_' + namestr + '_' + str(n) + '.csv'
    directory = os.path.dirname(filename)

    if not os.path.exists(directory):
        os.makedirs(directory)
        
    total_count = sum(arrival_time[threshold:(threshold+cutoff)])
    status_bar.setText(str(total_count))
    
    partial_count = sum(arrival_time[48:56])
    status_bar.setText(str(partial_count))
    
    
    with open(filename, 'w') as f:
        f.write(header)
        f.write('time, arrival_time, PMT1_arrival_time, PMT2_arrival_time, pulse_arrival_time')
        for x in range(len(arrival_time)):
            f.write('%f, %d, %d,%d, %d\n' %(x*1.25, arrival_time[x], PMT1_arrival_time[x], PMT2_arrival_time[x], pulse_arrival_time[x]))
    n += 1
    
#    return total_count
    return partial_count

def update_plot(data, axs, status_bar):
    pulse_trigger_not_arrive_count = 0

    PMT1_arrival_time = []
    PMT2_arrival_time = []
    pulse_arrival_time = []
    coincidence_list = []
    for each in data:
        if each[3] == 100:
            PMT1_arrival_time += each[0:3]
        elif each[3] == 200:
            PMT2_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        elif each[3] == 111:            
            coincidence_list.append(each)
        else:
            print('Unknown signature:', each)
    
    arrival_time = []        
    for i in range(len(PMT1_arrival_time)):
        arrival_time[i] = PMT1_arrival_time[i] + PMT2_arrival_time[i]

    axs.cla() # Delete the previously plotted data
    x = np.arange(len(arrival_time))
     
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Arrival time distribution of pulse picker trigger output w.r.t. stopwatch start')
    axs.set_xlabel('Arrival time of pulse picker trigger output w.r.t. stopwatch start (ns)')
    axs.set_ylabel('Number of event')

    status_message = 'Successed trial = %d\n' % sum(arrival_time)
    status_message += 'Overall trial = %d\n' % (max_run_count *max_second_loop)
    status_message += 'Success rate = %f' % (sum(arrival_time)/(max_run_count *max_second_loop))
    status_bar.setText(status_message)
    
    return arrival_time
    
    #print(error_case)

    







    
#%%
import time

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26') # COM port # : 4(labtop near MIRA), 26 (IonTrap2)
    sequencer.check_version(hd.HW_VERSION)

    #s.program()
    #s.program(hex_file='O:\\Users\\thkim\\Arty_S7\\Sequencer\\v3_04\\v3_04.srcs\\sim_1\\new\\test_hex.mem')
    #s.program(machine_code=True)
    #s.program(target=sequencer, machine_code=True)
    
    start = time.time()
    
    s.program(show=False, target=sequencer)
    PMT1_data = []
    PMT2_data = []
        
    
    
    time_run = 0
    
    while (time_run < 100):
        data = []
    
        sequencer.auto_mode()
    
        sequencer.send_command('START SEQUENCER')
    
        while(sequencer.sequencer_running_status() == 'running'):
            data_count = sequencer.fifo_data_length()
            if data_count > sequencer.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = sequencer.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += sequencer.read_fifo_data(data_count)
            print('%d data is read' % len(data))
            
        data_count = sequencer.fifo_data_length()
        while (data_count > 0):
            if data_count > sequencer.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = sequencer.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += sequencer.read_fifo_data(data_count)
            print('%d data is read' % len(data))
            data_count = sequencer.fifo_data_length()
        
    
        PMT1 = []
        PMT2 = []
        for each in data:
            if each[3] == 900:
                PMT1.append(each)
            elif each[3] == 901:
                PMT2.append(each)
            
        PMT1_data = PMT1_data + PMT1
        PMT2_data = PMT2_data + PMT2
        time_run += 1
        print('')
        print('run time: ', time_run)
        print('')
        
        
    sequencer.close()
        
