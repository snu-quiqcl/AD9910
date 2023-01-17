onbreak {quit -f}
onerror {quit -f}

vsim -t 1ps -lib xil_defaultlib CLK62_5MHZGen_opt

do {wave.do}

view wave
view structure
view signals

do {CLK62_5MHZGen.udo}

run -all

quit -force
