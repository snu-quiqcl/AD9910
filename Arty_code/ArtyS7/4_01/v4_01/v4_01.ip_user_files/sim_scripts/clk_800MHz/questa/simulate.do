onbreak {quit -f}
onerror {quit -f}

vsim -t 1ps -lib xil_defaultlib clk_800MHz_opt

do {wave.do}

view wave
view structure
view signals

do {clk_800MHz.udo}

run -all

quit -force
