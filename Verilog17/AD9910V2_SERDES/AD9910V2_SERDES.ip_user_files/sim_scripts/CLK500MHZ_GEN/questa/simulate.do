onbreak {quit -f}
onerror {quit -f}

vsim -t 1ps -lib xil_defaultlib CLK500MHZ_GEN_opt

do {wave.do}

view wave
view structure
view signals

do {CLK500MHZ_GEN.udo}

run -all

quit -force
