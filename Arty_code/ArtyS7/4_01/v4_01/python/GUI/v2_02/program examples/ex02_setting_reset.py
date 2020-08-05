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

###################################################################

# Hardware definition

Channel = 1             # 1 for 1S, 2 for 4G

if Channel == 1:
    PMT_reset = hd.PMT1_stopwatch_reset 
    PMT_start = hd.PMT1_stopwatch_start
    PMT_stopped_TLI = hd.PMT1_stopwatch_stopped_TLI
    PMT_result = hd.PMT1_stopwatch_result
    	
    PMT_counter_reset = hd.PMT1_counter_reset
    PMT_counter_enable = hd.PMT1_counter_enable
    PMT_counter_result = hd.PMT1_counter_result
    
elif Channel == 2:
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

s.set_output_port(hd.counter_control_port, [(hd.C1_AOM_on_out, 1), (hd.C2_AOM_on_out, 1),\
                                            (hd.C1_AOM_switch_out, 1), (hd.C2_AOM_switch_out, 1), ], 'Start counter')
    
s.stop()


#%%
import time
import statistics

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM26')
    sequencer.check_version(hd.HW_VERSION)

    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')

    time.sleep(1)
    
    sequencer.close()