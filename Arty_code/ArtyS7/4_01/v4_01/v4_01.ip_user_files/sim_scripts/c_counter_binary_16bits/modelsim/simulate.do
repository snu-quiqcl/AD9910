onbreak {quit -f}
onerror {quit -f}

vsim -voptargs="+acc" -t 1ps -L xil_defaultlib -L xpm -L xbip_utils_v3_0_8 -L c_reg_fd_v12_0_4 -L xbip_dsp48_wrapper_v3_0_4 -L xbip_pipe_v3_0_4 -L xbip_dsp48_addsub_v3_0_4 -L xbip_addsub_v3_0_4 -L c_addsub_v12_0_11 -L c_gate_bit_v12_0_4 -L xbip_counter_v3_0_4 -L c_counter_binary_v12_0_11 -L unisims_ver -L unimacro_ver -L secureip -lib xil_defaultlib xil_defaultlib.c_counter_binary_16bits xil_defaultlib.glbl

do {wave.do}

view wave
view structure
view signals

do {c_counter_binary_16bits.udo}

run -all

quit -force
