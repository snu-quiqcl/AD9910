# This file is automatically generated.
# It contains project source information necessary for synthesis and implementation.

# XDC: imports/Arty_S7/Arty-S7-50-Master.xdc

# IP: ip/fifo_generator_1/fifo_generator_1.xci
set_property DONT_TOUCH TRUE [get_cells -hier -filter {REF_NAME==fifo_generator_1 || ORIG_REF_NAME==fifo_generator_1} -quiet] -quiet

# XDC: ip/fifo_generator_1/fifo_generator_1.xdc
set_property DONT_TOUCH TRUE [get_cells [split [join [get_cells -hier -filter {REF_NAME==fifo_generator_1 || ORIG_REF_NAME==fifo_generator_1} -quiet] {/U0 } ]/U0 ] -quiet] -quiet
