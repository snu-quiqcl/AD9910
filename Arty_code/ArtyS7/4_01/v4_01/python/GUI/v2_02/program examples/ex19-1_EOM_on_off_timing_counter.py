# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Time stamping of PMT w.r.t. cooling beam switching on/off

* Definitions
- PMT_time: arrival time of PMT (start with cooling beam on/off)

* The following conditions should be satisfied:
- PMT is triggered

* Collecting statistics of PMT


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

#import export_clipboard_string as cp

###################################################################

# Hardware definition

Channel = 1             # 1 for 1S, 2 for 4G

if Channel == 1:
    EOM2_out = hd.C1_EOM_2_1GHz_out # added
    EOM7_out = hd.C1_EOM_7_37GHz_out # added
    
    AOM_out = hd.C1_AOM_on_out
    PMT_reset = hd.PMT1_stopwatch_reset 
    PMT_start = hd.PMT1_stopwatch_start
    PMT_stopped_TLI = hd.PMT1_stopwatch_stopped_TLI
    PMT_result = hd.PMT1_stopwatch_result
    
    PMT_counter_reset = hd.PMT1_counter_reset
    PMT_counter_enable = hd.PMT1_counter_enable
    PMT_counter_result = hd.PMT1_counter_result
    
    
elif Channel == 2:    
    EOM2_out = hd.C2_EOM_2_1GHz_out # added
    EOM7_out = hd.C2_EOM_7_37GHz_out # added
    
    AOM_out = hd.C2_AOM_on_out
    PMT_reset = hd.PMT2_stopwatch_reset 
    PMT_start = hd.PMT2_stopwatch_start
    PMT_stopped_TLI = hd.PMT2_stopwatch_stopped_TLI
    PMT_result = hd.PMT2_stopwatch_result  
    
    PMT_counter_reset = hd.PMT2_counter_reset
    PMT_counter_enable = hd.PMT2_counter_enable
    PMT_counter_result = hd.PMT2_counter_result

#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0] # global run number
sw_flags_R = reg[1]     # stopwatch status flags
PMT1_timing_R = reg[2] # Arrival time of PMT1 signal since single shot output
counter_result_R = reg[3]
counter_number_R = reg[4]

run_counter_second_loop_R = reg[5]      # second loop run number

# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 
max_run_count = 50000               # Number of repeat
max_second_loop = 10              # Number of second loop
Doppler_cooling_time = 30-3          # Doppler cooling time: 100 * 10ns
#Doppler_cooling_time = 30-3          # Doppler cooling time: 100 * 10ns

T_30ns = 3                 # tick for 1us (10ns * 100)
T_100ns = 10                 # tick for 1us (10ns * 100)
T_1us = 100                 # tick for 1us (10ns * 100)
Max_acquistion_time = 300   # 100 us

Buffer_time = 500

memory_pointer = 500            


# Counter time resolution is 1.25ns.



#%%    

s=SequencerProgram()


# Doppler cool the 174Yb ion
s.set_output_port(hd.external_control_port, [(AOM_out, 1), (EOM7_out, 1), (EOM2_out, 0),\
    (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')

    
# Initialize the memory
s.load_immediate(reg[11], 0) # Reset value for the momery initialization
s.load_immediate(reg[10], 0)
s.memory_initialization = \
\
s.store_word_to_memory(reg[10], reg[11])
s.add(reg[10], reg[10], 1)
s.branch_if_less_than('memory_initialization', reg[10], Max_acquistion_time)
#
#s.load_immediate(reg[10], memory_pointer)
#s.memory_initialization_2 = \
#\
#s.store_word_to_memory(reg[10], reg[11])
#s.add(reg[10], reg[10], 1)
#s.branch_if_less_than('memory_initialization_2', reg[10], Max_acquistion_time+memory_pointer)


#Reset run_number
s.load_immediate(run_counter_second_loop_R, 0, 'reg[5] will be used for second loop run number')

s.second_loop = \
\
s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')


# Repeating part
# Turn on Doppler cooling and wait
s.repeat = \
\
s.set_output_port(hd.external_control_port, [(AOM_out, 1), (EOM7_out, 1), (EOM2_out, 1)],)

s.wait_n_clocks(Doppler_cooling_time, 'wait for enough cooling')


## beam off timing measurement

# Turn on EOM_2G and wait for enough time until it goes dark
s.set_output_port(hd.external_control_port, [(EOM2_out, 0),])

#s.wait_n_clocks(10, 'Wait for 100ns')
#
#s.set_output_port(hd.external_control_port, [(EOM2_out, 0),])

# reset counter
s.load_immediate(counter_number_R, 0)

s.trigger_out([PMT_counter_reset], 'Reset single counter')
s.set_output_port(hd.counter_control_port, [(PMT_counter_enable, 1), ], 'Start counter')
s.wait_n_clocks(T_100ns, 'wait for 100ns')

s.acquisition_process = \
\
s.read_counter(counter_result_R, PMT_counter_result)
s.trigger_out([PMT_counter_reset], 'Reset single counter')

s.load_word_from_memory(reg[10], counter_number_R)
s.add(reg[10], reg[10], counter_result_R)
s.store_word_to_memory(counter_number_R, reg[10])

s.add(counter_number_R, counter_number_R, 1)
s.wait_n_clocks(T_100ns-6, 'wait for 100ns')
s.branch_if_less_than('acquisition_process', counter_number_R, Max_acquistion_time)

# Decide whether we will repeat running
s.decide_repeat = \
\
s.add(run_counter_R, run_counter_R, 1, 'run_counter_R++')
s.branch_if_less_than('repeat', run_counter_R, max_run_count)

s.write_to_fifo(run_counter_R,run_counter_second_loop_R,run_counter_second_loop_R,0)

s.add(run_counter_second_loop_R, run_counter_second_loop_R, 1, 'second loop number ++')
s.branch_if_less_than('second_loop', run_counter_second_loop_R, max_second_loop)


s.set_output_port(hd.external_control_port, [(AOM_out, 1), (EOM7_out, 1), (EOM2_out, 0)],)


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
s.branch_if_less_than('transfer_statistics', reg[10], Max_acquistion_time)

#s.load_immediate(reg[10], memory_pointer, 'reg[10] is used as address pointer and counter')
#s.transfer_statistics_2 = \
#\
#s.load_word_from_memory(reg[11], reg[10])
#s.add(reg[10], reg[10], 1)
#s.load_word_from_memory(reg[12], reg[10])
#s.add(reg[10], reg[10], 1)
#s.load_word_from_memory(reg[13], reg[10])
#s.add(reg[10], reg[10], 1)
#s.write_to_fifo(reg[11], reg[12], reg[13], 200)
#s.branch_if_less_than('transfer_statistics_2', reg[10], max_time_to_record+memory_pointer)


#s.load_immediate(counter_number_R, 0)
#s.trigger_out([PMT_counter_reset], 'Reset single counter')


s.stop()


n = 0
def count_for_plot(data, status_bar):
    global n
    
    arrival_time = []
    arrival_time_2 = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
    # np.sum(arrival_time) => 18079 out of 60000 trials
    
    #threshold = 76  # peak data number = 72, 5 tick after the peak
    #cutoff = 60
    
    threshold = 86  # peak data number = 82, 5 tick after the peak
    cutoff = 60
#    # Random data generation
#    data = []
#    for n in range(int(100*random.random())):
#        data.append([n+1, 0, 0, 10])
#    for n in range(20):
#        data.append([int(100*random.random()), int(100*random.random()), int(100*random.random()), 100])
#    # End of random data generation        


    #print('Successed trial =',sum(arrival_time))
    #print('Overall trial =',max_run_count*max_second_loop)
    #print('Success rate =',sum(arrival_time)/max_run_count/max_second_loop)
    
    #print(arrival_time)
    #print(arrival_time_2)
       
    total_count = sum(arrival_time[threshold:(threshold+cutoff)])
    status_bar.setText(str(total_count))
    filename = 'O:\\Users\\thkim\\Arty_S7\\Sequencer\\v4_00\\python\\GUI\\v2_00\\pulse_rabi\\program examples\\%d.txt' % n
    with open(filename, 'w') as f:
        f.write(str(arrival_time))
    n += 1
    if n%5 == 0:
        cp.send_clipboard()
    
    return total_count


import matplotlib.pyplot as plt
import numpy as np

def analyze(data):
    pulse_trigger_not_arrive_count = 0

    arrival_time_1 = []
    arrival_time_2 = []
    for each in data:
        if each[3] == 100:
            arrival_time_1 += each[0:3]
        elif each[3] == 200:
            arrival_time_2 += each[0:3]
        elif each[3] == 0:
            pass
        else:
            print('Unknown signature:', each)

    x = np.arange(len(arrival_time_1))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x, arrival_time_1)
    axs.set_tit2le('Photon arrival time distribution w.r.t. 2G EOM on')
    axs.set_xlabel('PMT arrival time w.r.t. 2G EOM on (0.1us)')
    axs.set_ylabel('Number of event')
#    
#    fig, axs = plt.subplots(1, 1, tight_layout=True)
#    axs.cla()
#    
#    axs.bar(x*1.25, arrival_time_2)
#    axs.set_title('Photon arrival time distribution w.r.t. 2G EOM off')
#    axs.set_xlabel('PMT arrival time w.r.t. 2G EOM off (ns)')
#    axs.set_ylabel('Number of event')    





    
#%%
import time

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26') # COM port # : 4(labtop near MIRA), 18 (IonTrap2), 26 (new FPGA, IonTrap2)
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
        #for each in data:
        #    print(each)
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    if data_count > 0:
        data =sequencer.read_fifo_data(data_count)
        #for each in data:
        #    print(each)
            
    arrival_time = []
    arrival_time_2 = []
    for each in data:
        if each[3] == 100:
            arrival_time += each[0:3]
        elif each[3] == 200:
            arrival_time_2 += each[0:3]
        else:
            print(each)
    # np.sum(arrival_time) => 18079 out of 60000 trials
    
    print('Successed trial =',sum(arrival_time))
    print('Overall trial =',max_run_count*max_second_loop)
    print('Success rate =',sum(arrival_time)/max_run_count/max_second_loop)
    
    
    print(arrival_time)
    print(arrival_time_2)
            
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(len(arrival_time))
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x*1.25, arrival_time)
    axs.set_title('Photon arrival time distribution w.r.t. 2G EOM on')
    axs.set_xlabel('PMT arrival time w.r.t. 2G EOM on (0.1us)')
    axs.set_ylabel('Number of event')
    
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    axs.cla()
    
    axs.bar(x*1.25, arrival_time_2)
    axs.set_title('Photon arrival time distribution w.r.t. 2G EOM off')
    axs.set_xlabel('PMT arrival time w.r.t. 2G EOM off (0.1us)')
    axs.set_ylabel('Number of event')    


    sequencer.close()

