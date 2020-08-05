# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* State initialize test

* This code is for stand-alone use. Do not run by GUI.

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

import numpy as np


###################################################################

# Hardware definition

# Hardware definition

Channel = 1             # 1 for 1S, 2 for 4G

if Channel == 1:
    EOM2_out = hd.C1_EOM_2_1GHz_out # added
    EOM7_out = hd.C1_EOM_7_37GHz_out # added
    
    #AOM_out = hd.C1_AOM_on_out
    
    AOM_switch = hd.C1_AOM_switch_out
    
    MW_switch = hd.C1_Microwave_SW_out
    
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
    AOM_switch = hd.C2_AOM_switch_out
    
    MW_switch = hd.C2_Microwave_SW_out
    
    PMT_reset = hd.PMT2_stopwatch_reset 
    PMT_start = hd.PMT2_stopwatch_start
    PMT_stopped_TLI = hd.PMT2_stopwatch_stopped_TLI
    PMT_result = hd.PMT2_stopwatch_result  
    
    PMT_counter_reset = hd.PMT2_counter_reset
    PMT_counter_enable = hd.PMT2_counter_enable
    PMT_counter_result = hd.PMT2_counter_result

debug_mode = 0          # 0 for normal operation. 1 for drawing detailed plots



#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0]              # global run number
run_counter_trial_R = reg[1]        # trial loop run number

Initialize_time_R = reg[2]

PMT1_result_R = reg[3]
PMT2_result_R = reg[4]
PMT_sum_R = reg[5]




# Registers for temporary storage
# reg[10], reg[11], reg[12], reg[13]


# Timing values 

Doppler_cooling_time =100-3          # Doppler cooling time: 1000 * 10ns
beam_off_time = 50
T_100us = 10000         
acquisition_time_in_100us = 30

# Rabi period for 1S : 139 us
Rabi_time_start = 100           #1 us
Rabi_time_step = 100            #1 us
Rabi_time_stop = 25000          # 350 us
number_of_trials = 300                         # number of trials for each exposure time


# Counter time resolution is 1.25ns.


## Create a header for data export on a file.

#header = \
#"############################################################################## \n"+\
#("## The first loop number = %d, The second loop number = %d \n" %(max_run_count, max_second_loop)) +\
#("## Total loop number = %d \n" %(max_run_count * max_second_loop)) + \
#("## Doppler cooling time = %d ns, " %(Doppler_cooling_time*10)) +  \
#("## Wait time before send pulse output = %d ns \n" %(time_bet_cooling_and_pulse*10)) + \
#("## Wait time before initiate stopwatches = %d ns \n" %(pre_waiting_time_for_start*10)) +\
#("## Stopwatch waiting time = %d ns, Maximum recorded time = %d ns \n" %(waiting_time_for_trigger*10, max_time_diff_to_record*1.25)) + \
#("## Pulse triggers arrived before %1.2f ns are ignored due to data distortion \n" %(trigger_precut*1.25)) + \
#"############################################################################## \n"




#%%    

def Code_program(Rabi_time):

    s=SequencerProgram()
    
    
    # Doppler cool the 171Yb ion
    s.set_output_port(hd.external_control_port, [(AOM_out , 1), (EOM7_out, 1), (EOM2_out, 0), \
        (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')
    
    
#    # Doppler cool the 174Yb ion
#    s.set_output_port(hd.external_control_port, [(AOM_out , 1), \
#        (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')
#    
    
    
    s.load_immediate(Initialize_time_R, Initialize_time, 'set to the start value')
    
    
    #Reset run_number
    s.load_immediate(run_counter_R, 0, 'reg[0] will be used for run number')
    
    # Repeating part
    # Turn on Doppler cooling and wait
    s.repeat = \
    \
    s.wait_n_clocks(Doppler_cooling_time, 'wait for enough cooling')
    s.set_output_port(hd.external_control_port, [(AOM_out , 1), (AOM_switch, 1), (EOM7_out, 1), (EOM2_out, 0),], 'Cooling')
    
    
    s.set_output_port(hd.external_control_port, [(EOM7_out, 0), (EOM2_out, 1),], 'State initialize to 0 state')
    s.wait_n_clocks(Initialize_time_R, 'wait for state initialize')
    
    # Turn off Doppler cooling and wait for enough time until the previously excited electron will decay
    s.set_output_port(hd.external_control_port, [(AOM_out , 0), ], 'Turn off beam')
    s.wait_n_clocks(beam_off_time, 'wait for enough time for previous decay')
    
    s.set_output_port(hd.external_control_port, [(MW_switch , 1), ], 'MW on')
    s.wait_n_clocks(Rabi_time, 'wait for Rabi oscillation')
    s.set_output_port(hd.external_control_port, [(MW_switch , 0), ], 'MW off')
#    
#    # Turn on detection beam & PMT counter on
    s.set_output_port(hd.external_control_port, [(AOM_out , 1), (AOM_switch, 0), (EOM2_out, 0),], 'Detection')
    s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 1), (hd.PMT2_counter_enable, 1)])
    s.trigger_out([hd.PMT1_counter_reset, hd.PMT2_counter_reset,], 'Reset counters')
    s.load_immediate(reg[10], 0)
    s.inner_loop = \
    \
    s.wait_n_clocks(T_100us-2, 'wait for state detection')
    s.add(reg[10],reg[10],1)
    s.branch_if_less_than('inner_loop', reg[10], acquisition_time_in_100us)
    
    # Turn off the counters
    s.set_output_port(hd.counter_control_port, [(hd.PMT1_counter_enable, 0), (hd.PMT2_counter_enable,0)], 'Turn off counters')
    s.set_output_port(hd.external_control_port, [(AOM_out , 1), (AOM_switch, 1), (EOM7_out, 1), (EOM2_out, 0),], 'Cooling')
    
    s.read_counter(PMT1_result_R, hd.PMT1_counter_result)
    s.read_counter(PMT2_result_R, hd.PMT2_counter_result)
    
    s.add(PMT_sum_R, PMT1_result_R, PMT2_result_R)
    
#    s.write_to_fifo(PMT_sum_R, PMT1_result_R, PMT2_result_R, 0)
    s.store_word_to_memory(run_counter_R, PMT_sum_R)
    
    s.add(run_counter_R, run_counter_R, 1)
    
    s.branch_if_less_than('repeat', run_counter_R, number_of_trials)
    
    
    s.set_output_port(hd.external_control_port, [(AOM_out , 1), (EOM7_out, 1), (EOM2_out, 0), \
        (hd.single_shot_out, 0) ], '369.5nm laser on and make sure pulse picker output is off')
    
    s.load_immediate(reg[10], 0)
    s.export_memory =\
    \
    s.load_word_from_memory(reg[11], reg[10])
    s.add(reg[10], reg[10], 1)
    s.load_word_from_memory(reg[12], reg[10])
    s.add(reg[10], reg[10], 1)
    s.load_word_from_memory(reg[13], reg[10])
    s.add(reg[10], reg[10], 1)
    s.write_to_fifo(reg[11], reg[12], reg[13], 100)
    s.branch_if_less_than('export_memory', reg[10], number_of_trials)
    
    s.stop()
    
    return s




    
#%%
import time
import statistics as stat
import matplotlib.pyplot as plt
from matplotlib import pylab
from scipy import optimize
import datetime

''' Setting constants for experiments '''

Expected_rabi_period = 130
Threshold = 3

''' --------------------------------- '''

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26') # COM port # : 4(labtop near MIRA), 18 (IonTrap2)
    sequencer.check_version(hd.HW_VERSION)
    
    raw_data = []
    values = []
    Initialize_time = 200
    Rabi_time = Rabi_time_start
    while(Rabi_time < Rabi_time_stop):
        s = Code_program(Rabi_time)
#        print('coding done')
        s.program(show=False, target=sequencer)

        sequencer.auto_mode()
        sequencer.send_command('START SEQUENCER')
    
        while(sequencer.sequencer_running_status() == 'running'):
            data_count = sequencer.fifo_data_length()
            data =sequencer.read_fifo_data(data_count)
#            for each in data:
#                print(each)

        data_count = sequencer.fifo_data_length()
        if data_count > 0:
            data =sequencer.read_fifo_data(data_count)
        
#        print('execution done')
        temp = []
        for each in data:
            temp += each[0:2]
        raw_data.append(temp)
        values.append([Rabi_time, stat.mean(temp), stat.stdev(temp)])
        
        Rabi_time += Rabi_time_step
        
    sequencer.close()
    
    print(stat.mean(temp), stat.stdev(temp))
    
    x = []
    y = []
    for each in values:
        x.append(each[0]*10)
        y.append(each[1])
        
    fig, axs = plt.subplots(1, 1, tight_layout=True)
    plt.plot(x, y)
    
    
    population = []
    for i in range(len(raw_data)):
        population.append(0)
        for each in raw_data[i]:
            if each> Threshold:
                population[i] += 1
    
    y_set = []
    for ll in range(len(raw_data)):
        y_set.append(population[ll] / len(raw_data[0]))
        

    p0=[2*np.pi/Expected_rabi_period, 0.9]


    def test_func(x, f, m):
        return ((np.sin(0.5*f*x)**2 * m))

    x_set = []
    for kk in range(len(raw_data)):
        x_set.append( x[kk] / 1000 )

    params, params_covariance = optimize.curve_fit(test_func, x_set, y_set, p0, maxfev=3000)
    rabi_period = 1/params[0] * (2*np.pi)

    fig, axs = plt.subplots(1, 1, tight_layout=True)



    xx = np.arange(1, len(raw_data), 1)
    
    plt.scatter(x_set, y_set, label='Data')
    plt.plot(xx, test_func(xx, params[0], params[1]), 'r', label='Fitted function')
    plt.text(50, 0.4, str('Rabi period: ' + '{:.2f}'.format(rabi_period)) + ' us', fontsize=12)
    plt.text(50, 0.3, str('Amplitude: ' + '{:.2f}'.format(params[1])), fontsize=12)

    plt.xlabel('Time (us)')
    plt.title("Rabi oscillation", fontsize=15)

    plt.legend(loc='best')
    
    
    #%% Saving figs
    if Channel == 1:
        CH_name = '1S'
    elif Channel == 2:
        CH_name = '4G'
    else:
        CH_nsme = ''
    SV_path = 'O:\\Users\\JKKim\\Data\\'
    nowT = datetime.datetime.now()
    nowDate = nowT.strftime('%Y%m%d%H%M%S')
    File_name = nowDate + '_' + CH_name + '_' + 'Rabi_oscillation'
    
    fig.savefig(SV_path + File_name + '.png')
    
    #%% Saving data
    with open(SV_path + File_name + '.csv', 'w') as ss:
        for kk in range(len(raw_data)):
            ss.write(str(raw_data[kk]) + '\n')
