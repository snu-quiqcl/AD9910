# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Time stamping of pulse picker trigger out and PMT w.r.t. pulse picker single shot

* Definitions
- PT_time: arrival time of pulse trigger out
- PMT_time: arrival time of PMT

* The following conditions should be satisfied:
- Both signals should arrive
- PMT_time > PT_time

* Collecting statistics of (PMT-PT_time)


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

# Hardware definition

Channel = 1             # 1 for 1S, 2 for 4G

if Channel == 1:
    AOM_out = hd.C1_AOM_200MHz_out
    PMT_reset = hd.PMT1_stopwatch_reset 
    PMT_start = hd.PMT1_stopwatch_start
    PMT_stopped_TLI = hd.PMT1_stopwatch_stopped_TLI
    PMT_result = hd.PMT1_stopwatch_result
    
elif Channel == 2:
    AOM_out = hd.C2_AOM_200MHz_out
    PMT_reset = hd.PMT2_stopwatch_reset 
    PMT_start = hd.PMT2_stopwatch_start
    PMT_stopped_TLI = hd.PMT2_stopwatch_stopped_TLI
    PMT_result = hd.PMT2_stopwatch_result  
    
debug_mode = 0          # 0 for normal operation. 1 for drawing detailed plots


# Post process parameters
max_index = 42                  # predefined max_index
Back_scattering_cut = 3         # 3*1.25 = 3.75 ns cut
scattering_threshold = 64       # 64*1.25 = 80 ns (~ 10 tau)


#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0] # global run number
sw_flags_R = reg[1]     # stopwatch status flags
pulse_trigger_timing_R = reg[2]   # Arrival time of pulse trigger from pulse picker since single shot output
PMT1_timing_R = reg[3] # Arrival time of PMT1 signal since single shot output
time_diff_R = reg[4]   # time difference between PMT1 and pulse_trigger

pulse_missing_R = reg[8]

trigger_precut_R = reg[13]

run_counter_second_loop_R = reg[5]      # second loop run number

# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_count =10000               # Number of repeat
max_second_loop = 200              # Number of second loop
Doppler_cooling_time = 250-3          # Doppler cooling time: 1000 * 10ns
time_bet_cooling_and_pulse = 45-3       # Clock counts to wait before pulse: 50 * 10ns
pre_waiting_time_for_start = 18         # Waiting time before initiate stopwatches
waiting_time_for_trigger = 12             # Clock counts to wait for stopwatches : 23 * 10ns
max_time_diff_to_record = 100      # If the time difference between PMT and pulse trigger is less than zero or >= max_time_diff_to_record, it won't be counted.

trigger_precut = 12               # if trigger comes before precut(tick), ignore that. 

pointer_for_PMT_record = 250
pointer_for_Pulse_Trigger_record = 500
# Counter time resolution is 1.25ns.


## Create a header for data export on a file.

header = \
"************************************************************************* \n"+\
("** The first loop number = %d, The second loop number = %d \n" %(max_run_count, max_second_loop)) +\
("** Total loop number = %d \n" %(max_run_count * max_second_loop)) + \
("** Doppler cooling time = %d ns, " %(Doppler_cooling_time*10)) +  \
("** Wait time before send pulse output = %d ns \n" %(time_bet_cooling_and_pulse*10)) + \
("** Wait time before initiate stopwatches = %d ns" %(pre_waiting_time_for_start*10)) +\
("** Stopwatch waiting time = %d ns, Maximum recorded time = %d ns \n" %(waiting_time_for_trigger*10, max_time_diff_to_record*1.25)) + \
("** Pulse triggers arrived before %1.2f ns are ignored due to data distortion \n" %(trigger_precut*1.25)) + \
"************************************************************************* \n"




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
s.memory_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_initialization', reg[10], max_time_diff_to_record)

s.load_immediate(reg[10],pointer_for_PMT_record)

s.memory_2_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_2_initialization', reg[10], max_time_diff_to_record+pointer_for_PMT_record)


s.load_immediate(reg[10],pointer_for_Pulse_Trigger_record)

s.memory_3_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_3_initialization', reg[10], max_time_diff_to_record+pointer_for_Pulse_Trigger_record)


#Reset run_number
s.load_immediate(run_counter_second_loop_R, 0, 'reg[5] will be used for second loop run number')

s.second_loop = \
\
s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')


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
s.trigger_out([PMT_reset, hd.pulse_trigger_stopwatch_reset, ], 'Reset stopwatches')
s.nop() # Between reset and start of the stopwatches, add at least one clock
s.trigger_out([PMT_start , hd.pulse_trigger_stopwatch_start, ], 'Start pulse trigger stopwatch')


#%%
s.wait_n_clocks(waiting_time_for_trigger-3, 'Waiting time is compensated for single shot input')
#s.wait_n_clocks_or_masked_trigger(waiting_time_for_trigger-3, [(hd.pulse_trigger_stopwatch_stopped_TLI, 1)], \
#                                  'Wait for an arrival of pulse trigger')

# Leave the Doppler cooling on
s.set_output_port(hd.external_control_port, [(AOM_out , 1),])

# Collect the result of stopwatch measurements
s.read_counter(sw_flags_R,              hd.Trigger_level, 'Read status of stopwatches')
s.read_counter(pulse_trigger_timing_R, hd.pulse_trigger_stopwatch_result, 'Read pulse trigger stopwatch result')
s.read_counter(PMT1_timing_R,           PMT_result, 'Read PMT1 stopwatch result')


# The following types of check can be removed, but here they are included for
# debugging purpose

# Check if pulse_trigger has arrived
s.branch_if_equal_with_mask('check_PMT1_triggered', sw_flags_R, \
    1 << hd.pulse_trigger_stopwatch_stopped_TLI , 1 << hd.pulse_trigger_stopwatch_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 10, 'pulse trigger did not arrive')
s.add(pulse_missing_R, pulse_missing_R, 1, 'pulse_missing_R++')
s.jump('decide_repeat')


# Check if PMT1 trigger is detected
s.check_PMT1_triggered = \
\
s.branch_if_equal_with_mask('check_if_pulse_trigger_arrived_before_PMT1', sw_flags_R, \
    1 << PMT_stopped_TLI, 1 << PMT_stopped_TLI)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 20, 'PMT1 trigger did not arrive')
s.jump('decide_repeat')


# Check if pulse trigger arrived before PMT1
s.check_if_pulse_trigger_arrived_before_PMT1 = \
\
s.branch_if_less_than('check_if_pulse_trigger_arrived_after_precut', pulse_trigger_timing_R, PMT1_timing_R)
#s.write_to_fifo(sw_flags_R, pulse_trigger_timing_R, PMT1_timing_R, 30, 'pulse trigger arrived after PMT1')
s.jump('decide_repeat')

# check if pulse trigger arrived after trigger_precut. (this case makes the second pulse)
s.check_if_pulse_trigger_arrived_after_precut = \
\
s.branch_if_less_than('calculate_time_difference', trigger_precut_R, pulse_trigger_timing_R)
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

#s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')

#s.write_to_fifo(run_counter_R, sw_flags_R, time_diff_R, 0, 'Store time difference')
#s.write_to_fifo(run_counter_R, pulse_trigger_timing_R, PMT1_timing_R, 1, 'Store time difference')

s.store_PMT_timing =\
\
s.add(reg[11], PMT1_timing_R, pointer_for_PMT_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])

# Store pulse trigger arrival time distribution
s.add(reg[11], pulse_trigger_timing_R, pointer_for_Pulse_Trigger_record)
s.load_word_from_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.store_word_to_memory(reg[11], reg[10])

# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')
s.branch_if_less_than('repeat', run_counter_R, max_run_count)

s.write_to_fifo(pulse_missing_R,run_counter_R,run_counter_second_loop_R, 10)

s.add(run_counter_second_loop_R, run_counter_second_loop_R, 1, 'second loop number ++')
s.branch_if_less_than('second_loop', run_counter_second_loop_R, max_second_loop)


# Leave the Doppler cooling on
s.set_output_port(hd.external_control_port, [(AOM_out , 1),])


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

s.load_immediate(reg[10], pointer_for_PMT_record, 'reg[10] is used as address pointer and counter')
s.transfer_statistics_2 = \
\
s.load_word_from_memory(reg[11], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[12], reg[10])
s.add(reg[10], reg[10], 1)
s.load_word_from_memory(reg[13], reg[10])
s.add(reg[10], reg[10], 1)
s.write_to_fifo(reg[11], reg[12], reg[13], 200)
s.branch_if_less_than('transfer_statistics_2', reg[10], max_time_diff_to_record+pointer_for_PMT_record)

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

    arrival_time = []
    PMT_arrival_time = []
    pulse_arrival_time = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
        elif each[3] == 200:
            PMT_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        else:
            print('Unknown signature:', each)
    
    print('pulse trigger did not arrive %d times \n' %pulse_trigger_not_arrive_count)

    max_count = max(arrival_time)    
    max_index = arrival_time.index(max_count)
    
    photon_count = sum(arrival_time[max_index+Back_scattering_cut:max_index+scattering_threshold])
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
        
        axs.bar(x*1.25, PMT_arrival_time)
        axs.set_title('Photon arrival time distribution w.r.t. stopwatch start')
        axs.set_xlabel('Photon arrival time distribution w.r.t. stopwatch start (ns)')
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

    arrival_time = []
    PMT_arrival_time = []
    pulse_arrival_time = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
        elif each[3] == 200:
            PMT_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        else:
            print('Unknown signature:', each)
    
    
    #print('pulse trigger did not arrive %d times \n' %pulse_trigger_not_arrive_count)
          
          
    # np.sum(arrival_time) => 18079 out of 60000 trials
    
    #threshold = 76  # peak data number = 72, 5 tick after the peak
    #cutoff = 60
    
    threshold = 86  # peak data number = 83, 5 tick after the peak
    cutoff = 60
#    # Random data generation
#    data = []
#    for n in range(int(100*random.random())):
#        data.append([n+1, 0, 0, 10])
#    for n in range(20):
#        data.append([int(100*random.random()), int(100*random.random()), int(100*random.random()), 100])
#    # End of random data generation        


    print('Successed trial =',sum(arrival_time))
    print('Overall trial =',max_run_count*max_second_loop)
    print('Success rate =',sum(arrival_time)/max_run_count/max_second_loop)
    
    # print(arrival_time)
    
    datestr = datetime.datetime.now().strftime("%Y-%m-%d")
    timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    #filename = 'O:\\Users\\thkim\\Arty_S7\\Sequencer\\v4_00\\python\\' + timestr +  '.csv'
    filename = 'O:\\Users\\JKKim\\data\\' +datestr +'\\'  + timestr +  '_' + n + '.csv'
    directory = os.path.dirname(filename)

    if not os.path.exists(directory):
        os.makedirs(directory)
        
    total_count = sum(arrival_time[threshold:(threshold+cutoff)])
    status_bar.setText(str(total_count))
    
    with open(filename, 'w') as f:
        f.write(header)
        for x in range(len(arrival_time)):
            f.write('%f, %d, %d, %d\n' %(x*1.25, arrival_time[x], PMT_arrival_time[x], pulse_arrival_time[x]))
    n += 1
    
    return total_count

def update_plot(data, axs, status_bar):
            
    pulse_trigger_not_arrive_count = 0

    arrival_time = []
    PMT_arrival_time = []
    pulse_arrival_time = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
        elif each[3] == 200:
            PMT_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        else:
            print('Unknown signature:', each)
    

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
#        for each in data:
#            print(each)
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    if data_count > 0:
        data =sequencer.read_fifo_data(data_count)
#        for each in data:
#            print(each)
            
    pulse_trigger_not_arrive_count = 0
            
    arrival_time = []
    PMT_arrival_time = []
    pulse_arrival_time = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
        elif each[3] == 200:
            PMT_arrival_time += each[0:3]
        elif each[3] == 300:
            pulse_arrival_time += each[0:3]
        elif each[3] == 10:
            pulse_trigger_not_arrive_count += each[0]
        else:
            print('Unknown signature:', each)
            
    # np.sum(arrival_time) => 18079 out of 60000 trials
    

    max_count = max(arrival_time)    
#    max_index = arrival_time.index(max_count)
    
    photon_count = sum(arrival_time[max_index+Back_scattering_cut:max_index+scattering_threshold])
    print('successful photon scattering = ', photon_count)
    print('total trial = ', max_run_count*max_second_loop)
    print('success rate = ', photon_count/max_run_count/max_second_loop)
    
    print(arrival_time)
    
    
    
    import matplotlib.pyplot as plt
    import numpy as np
#    
#    x = np.arange(len(arrival_time))
#    fig, axs = plt.subplots(1, 1, tight_layout=True)
#    axs.bar(x*1.25, arrival_time)
#    axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output')
#    axs.set_xlabel('PMT arrival time w.r.t. pulse picker trigger output (ns)')
#    axs.set_ylabel('Number of event')
#    
    
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
        
        axs.bar(x*1.25, PMT_arrival_time)
        axs.set_title('Photon arrival time distribution w.r.t. stopwatch start')
        axs.set_xlabel('Photon arrival time distribution w.r.t. stopwatch start (ns)')
        axs.set_ylabel('Number of event')
        axs.set_yscale('log', nonposy='clip')
    
        fig, axs = plt.subplots(1, 1, tight_layout=True)
        axs.cla()
        
        axs.bar(x*1.25, pulse_arrival_time)
        axs.set_title('Pulse picker trigger output time distribution w.r.t. stopwatch start')
        axs.set_xlabel('Pulse picker trigger output time distribution w.r.t. stopwatch start (ns)')
        axs.set_ylabel('Number of event')
        axs.set_yscale('log', nonposy='clip')

"""
data=[[0, 306, 364, 100],
 [84, 28, 15, 100],
 [6, 7, 2, 100],
 [2, 2, 9, 100],
 [585, 118, 62, 100],
 [17, 18, 7, 100],
 [8, 12, 8, 100],
 [13, 171, 518, 100],
 [61, 45, 16, 100],
 [4, 3, 2, 100],
 [9, 6, 14, 100],
 [468, 197, 48, 100],
 [25, 19, 5, 100],
 [6, 6, 2, 100],
 [8, 54, 558, 100],
 [99, 32, 38, 100],
 [13, 12, 12, 100],
 [38, 8, 91, 100],
 [3380, 2404, 440, 100],
 [213, 114, 42, 100],
 [37, 17, 22, 100],
 [9, 41, 1431, 100],
 [277, 121, 44, 100],
 [29, 27, 9, 100],
 [12, 3, 8, 100],
 [213, 343, 36, 100],
 [27, 15, 8, 100],
 [11, 7, 0, 100],
 [3, 10, 264, 100],
 [140, 35, 13, 100],
 [8, 3, 6, 100],
 [10, 5, 4, 100],
 [89, 350, 43, 100],
 [30, 20, 4, 100],
 [2, 2, 4, 100],
 [1, 8, 269, 100],
 [286, 39, 16, 100],
 [12, 4, 9, 100],
 [5, 3, 3, 100],
 [15, 433, 67, 100],
 [44, 11, 7, 100],
 [4, 2, 1, 100],
 [1, 7, 183, 100],
 [310, 41, 30, 100],
 [15, 4, 2, 100],
 [1, 3, 0, 100],
 [11, 328, 126, 100],
 [40, 14, 11, 100],
 [3, 1, 4, 100],
 [1, 5, 82, 100],
 [374, 52, 32, 100],
 [14, 4, 3, 100],
 [1, 2, 0, 100],
 [5, 267, 217, 100]]

arrival_time = []
for each in data:
    arrival_time += each[0:3]
# np.sum(arrival_time) => 18079 out of 60000 trials

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(len(arrival_time))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.bar(x*1.25, arrival_time)
axs.set_title('Photon arrival time distribution w.r.t. pulse picker trigger output')
axs.set_xlabel('PMT arrival time w.r.t. pulse picker trigger output (ns)')
axs.set_ylabel('Number of event')

"""
