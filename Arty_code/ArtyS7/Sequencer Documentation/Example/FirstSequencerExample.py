# Import required modules for sequencer programming
from SequencerProgram_v1_07 import SequencerProgram, reg
import SequencerUtility_v1_01 as su
from ArtyS7_v1_02 import ArtyS7
import HardwareDefinition_type_EX as hd

# Assembly Codes
s = SequencerProgram()

s.load_immediate(reg[0], 0)
s.write_to_fifo(reg[0], reg[0], reg[0], 10, 'First Sequencer Code')
s.stop()

if __name__ == '__main__':
    # Send Instructions and Start Sequencer
    if 'sequencer' in vars():
        sequencer.close()
    sequencer = ArtyS7('COM4')
    sequencer.check_version(hd.HW_VERSION)

    s.program(show=False, target=sequencer)

    sequencer.auto_mode()
    sequencer.start_sequencer()

    # Data Acquisition
    data = []
    
    while(sequencer.sequencer_running_status() == 'running'):
        data_count = sequencer.fifo_data_length()
        data += sequencer.read_fifo_data(data_count)

    data_count = sequencer.fifo_data_length()
    while (data_count > 0):
        data += sequencer.read_fifo_data(data_count)
        data_count = sequencer.fifo_data_length()

    for each in data:
        print(each)
