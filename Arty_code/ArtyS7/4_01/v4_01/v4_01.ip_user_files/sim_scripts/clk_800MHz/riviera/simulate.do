onbreak {quit -force}
onerror {quit -force}

asim -t 1ps +access +r +m+clk_800MHz -L xil_defaultlib -L xpm -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.clk_800MHz xil_defaultlib.glbl

do {wave.do}

view wave
view structure

do {clk_800MHz.udo}

run -all

endsim

quit -force
