# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:46:10 2018

@author: iontrap

* FIFO speed test

* write into FIFO in every T_interval

* readout FIFO as fast as possible


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

#%%################################################################
# Reserved registers in this program
###################################################################
run_counter_R = reg[0]
inner_loop_R = reg[1]

max_run = 1000
T_interval = 10000         # 100us
N_T = 10                    # 5ms


#%%###

s = SequencerProgram()

s.load_immediate(run_counter_R,0)

s.repeat = \
\
s.write_to_fifo(run_counter_R, run_counter_R, run_counter_R, 1)

s.load_immediate(inner_loop_R,0)
s.inner_repeat = \
\
s.wait_n_clocks(T_interval-2)
s.add(inner_loop_R,inner_loop_R,1)
s.branch_if_less_than('inner_repeat', inner_loop_R, N_T)

s.add(run_counter_R, run_counter_R, 1)

s.branch_if_less_than('repeat', run_counter_R, max_run)

s.stop

#%%
import time

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26') # COM port # : 4(labtop near MIRA), 18 (IonTrap2), 26 (new FPGA, IonTrap2)
    sequencer.check_version(hd.HW_VERSION)

    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')
    
    start_time = time.time()
    
    test_list = []
    while(sequencer.sequencer_running_status() == 'running'):
        data_count = sequencer.fifo_data_length()
        data =sequencer.read_fifo_data(data_count)
        if len(data)!= 0:
            end_time = time.time() -start_time            
            print(end_time, data[-1][0])
            test_list.append([end_time, data[-1][0]])
        #time.sleep(1)

    data_count = sequencer.fifo_data_length()
    if data_count > 0:
        data =sequencer.read_fifo_data(data_count)
        end_time = time.time() -start_time
        print(end_time, data[-1][0])
        test_list.append([end_time, data[-1][0]])
    
    sum = 0
#    for i in range(len(test_list)-1):
#        sum += test_list[i+1] - test_list[i]
        
    avg = test_list[-1][0] / len(test_list)
    print(avg)
    

    sequencer.close()


