# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Example for stopping an infinite loop in the sequencer
- Press Ctrl+C
sequencer.flush_input() # Flush the input buffer of the serial port
sequencer.escape_reset() # Reset most of the parts
sequencer.sequencer_running_status() # This will give us "running" status
sequencer.stop_sequencer()
sequencer.sequencer_running_status() # This will give us "stopped" status
sequencer.flush_input() # Flush the input buffer of the serial port
sequencer.flush_Output_FIFO(debug=True) # To flush any remaining data in the Output FIFO

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

#%%    

s=SequencerProgram()

# Repeating part
s.repeat = \
\
s.nop()
s.write_to_fifo(reg[0], reg[0], reg[0], 0)
s.jump('repeat')

s.stop()


    
#%%

if __name__ == '__main__':
    if 'sequencer' in vars(): # To close the previously opened device when re-running the script with "F5"
        sequencer.close()
    sequencer = ArtyS7('COM18') # COM port # : 4(labtop near MIRA), 18 (IonTrap2)
    sequencer.check_version(hd.HW_VERSION)

    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.send_command('START SEQUENCER')

    while(sequencer.sequencer_running_status() == 'running'): # For infinite loop, the python program will be stuck in this loop. Press Ctrl+C
        data_count = sequencer.fifo_data_length()
        data =sequencer.read_fifo_data(data_count)
        for each in data:
            print(each)
        #time.sleep(1)

            
