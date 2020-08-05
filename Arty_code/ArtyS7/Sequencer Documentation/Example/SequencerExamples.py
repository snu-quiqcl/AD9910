# Import required modules for sequencer programming
from SequencerProgram_v1_07 import SequencerProgram, reg
import SequencerUtility_v1_01 as su
from ArtyS7_v1_02 import ArtyS7
import HardwareDefinition_type_EX as hd


# Example 1: Arithmetic Operations
s = SequencerProgram()

s.load_immediate(reg[0], 0)
s.add(reg[0], reg[0], 1, 'reg[0] <= reg[0] + 1')
s.add(reg[1], reg[0], reg[0], 'reg[1] <= reg[0] + reg[0]')
s.subtract(reg[2], reg[1], reg[0], 'reg[2] <= reg[1] - reg[0]')
s.subtract(reg[2], reg[2], 2, 'reg[2] <= reg[2] - 2')
s.write_to_fifo(reg[0], reg[1], reg[2], 10, 'Arithmetic Example')
s.stop()


##--------------------------------------------------------------------
# # Example 2: Branch/Jump Operations
# s = SequencerProgram()

# s.load_immediate(reg[0], 0)
# s.load_immediate(reg[1], 1)

# s.add_value = \
# \
# s.add(reg[0], reg[0], reg[1], 'reg[0] += reg[1]')
# s.add(reg[1], reg[1], 1, 'reg[1]++')
# s.branch_if_less_than('add_value', reg[1], 11)

# s.write_to_fifo(reg[0], reg[0], reg[1], 10, 'Branch/Jump Example')
# s.stop()


##--------------------------------------------------------------------
# # Example 3: Memory Access(Load, Store)
# s = SequencerProgram()

# s.load_immediate(reg[0], 0)
# s.load_immediate(reg[1], 0)

# s.repeat_store = \
# \
# s.add(reg[0], reg[0], 2)
# s.store_word_to_memory(reg[1], reg[0])
# s.add(reg[1], reg[1], 1)
# s.branch_if_less_than('repeat_store', reg[1], 3)

# s.load_immediate(reg[0], 0)
# s.load_word_from_memory(reg[1], reg[0])
# s.add(reg[0], reg[0], 1)
# s.load_word_from_memory(reg[2], reg[0])
# s.add(reg[0], reg[0], 1)
# s.load_word_from_memory(reg[3], reg[0])

# s.write_to_fifo(reg[1], reg[2], reg[3], 10, 'Store/Load Example')
# s.stop()


##--------------------------------------------------------------------
# # Example 4: External Output Port
# s = SequencerProgram()

# s.set_output_port(hd.external_control_port, [(hd.LED1_out, 1), (hd.LED2_out, 0)])

# s.load_immediate(reg[0], 0)
# s.repeat_wait1 = \
# \
# s.wait_n_clocks(30000, 'Wait 30000 cycles unconditionally')
# s.add(reg[0], reg[0], 1)
# s.branch_if_less_than('repeat_wait1', reg[0], 10000)

# s.set_output_port(hd.external_control_port, [(hd.LED1_out, 0), (hd.LED2_out, 1)])

# s.load_immediate(reg[0], 0)
# s.repeat_wait2 = \
# \
# s.wait_n_clocks(30000, 'Wait 30000 cycles unconditionally')
# s.add(reg[0], reg[0], 1)
# s.branch_if_less_than('repeat_wait2', reg[0], 10000)

# s.set_output_port(hd.external_control_port, [(hd.LED2_out, 0)])
# s.write_to_fifo(reg[0], reg[0], reg[0], 10, 'End')
# s.stop()


##--------------------------------------------------------------------
# # Example 5: Counter
# s = SequencerProgram()

# s.trigger_out([hd.push_button1_counter_reset, hd.push_button2_counter_reset], 'Reset counter')
# s.set_output_port(hd.counter_control_port, [(hd.push_button1_counter_enable, 1), (hd.push_button2_counter_enable, 1), ], 'Start counter')

# s.load_immediate(reg[0], 0)
# s.repeat_wait = \
# \
# s.wait_n_clocks(50000, 'Wait 50000 cycles unconditionally')
# s.add(reg[0], reg[0], 1)
# s.branch_if_less_than('repeat_wait', reg[0], 10000)

# s.set_output_port(hd.counter_control_port, [(hd.push_button1_counter_enable, 0), (hd.push_button2_counter_enable, 0), ], 'Stop counter')

# s.read_counter(reg[10], hd.push_button1_counter_result)
# s.read_counter(reg[11], hd.push_button2_counter_result)
# s.write_to_fifo(reg[0], reg[10], reg[11], 10, 'Counts within 5s')

# s.stop()


##--------------------------------------------------------------------
# # Example 6: Stopwatch
# s = SequencerProgram()

# s.trigger_out([hd.push_button1_stopwatch_reset , hd.push_button2_stopwatch_reset, ], 'Reset stopwatches')
# s.nop() # Between reset and start of the stopwatches , add at least one clock
# s.trigger_out([hd.push_button1_stopwatch_start, hd.push_button2_stopwatch_start, ], 'Start stopwatches')

# s.load_immediate(reg[0], 0)
# s.repeat_wait = \
# s.wait_n_clocks(50000, 'Wait 50000 cycles unconditionally')
# s.add(reg[0], reg[0], 1)
# s.branch_if_less_than('repeat_wait', reg[0], 10000)

# s.read_counter(reg[0], hd.push_button1_stopwatch_result, 'push_button1 stopwatch result')
# s.read_counter(reg[1], hd.push_button2_stopwatch_result, 'push_button2 stopwatch result')
# s.read_counter(reg[2], hd.Trigger_level, 'Status of stopwatches')

# s.write_to_fifo(reg[0], reg[1], reg[2], 10, 'Stopwatch Example')

# s.stop()


##--------------------------------------------------------------------
# # Example 7: Timing Issue of Wait
# s = SequencerProgram()

# s.load_immediate(reg[10], 3)

# s.trigger_out([hd.push_button1_stopwatch_reset], 'Reset stopwatch')
# s.nop() # Between reset and start, add at least one clock
# s.trigger_out([hd.push_button1_stopwatch_start], 'Start stopwatch')

# s.read_counter(reg[0], hd.push_button1_stopwatch_result, '1 clock after start')
# s.read_counter(reg[1], hd.push_button1_stopwatch_result, '2 clock after start')
# s.nop()     # 3 clock after start
# s.read_counter(reg[2], hd.push_button1_stopwatch_result, '4 clock after start')
# s.wait_n_clocks(1, 'Wait 1 cycle')
# s.read_counter(reg[3], hd.push_button1_stopwatch_result)
# s.wait_n_clocks(reg[10], 'Wait 3 cycle')
# s.read_counter(reg[4], hd.push_button1_stopwatch_result)
# s.wait_n_clocks(5000, 'Wait 5000 cycle')
# s.read_counter(reg[5], hd.push_button1_stopwatch_result)

# s.write_to_fifo(reg[0], reg[1], reg[2], 10, 'Timing Issue of Wait')
# s.write_to_fifo(reg[3], reg[4], reg[5], 10, 'Timing Issue of Wait')

# s.stop()


##--------------------------------------------------------------------
# # Example 8: Masked Operations
# mask = 1 << hd.push_button1_stopwatch_stopped_TLI
# push_buttons_stopped = (1 << hd.push_button1_stopwatch_stopped_TLI) + (1 << hd.push_button2_stopwatch_stopped_TLI)

# s = SequencerProgram()

# s.trigger_out([hd.push_button1_stopwatch_reset , hd.push_button2_stopwatch_reset, ], 'Reset stopwatches')
# s.nop() # Between reset and start of the stopwatches , add at least one clock
# s.trigger_out([hd.push_button1_stopwatch_start, hd.push_button2_stopwatch_start, ], 'Start stopwatches')
# s.set_output_port(hd.external_control_port, [(hd.LED1_out, 1)])

# s.load_immediate(reg[0], 0)
# s.repeat_wait = \
# s.wait_n_clocks_or_masked_trigger(50000, [(hd.push_button1_stopwatch_stopped_TLI, 1)])
# s.read_counter(reg[1], hd.Trigger_level, 'Status of stopwatches')
# s.branch_if_equal_with_mask('turn_off_LED', reg[1], push_buttons_stopped, mask)
# s.add(reg[0], reg[0], 1)
# s.branch_if_less_than('repeat_wait', reg[0], 10000)

# s.turn_off_LED = \
# s.set_output_port(hd.external_control_port, [(hd.LED1_out, 0)])

# s.write_to_fifo(reg[0], reg[1], reg[1], 10, 'Masked Operations')

# s.stop()


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
