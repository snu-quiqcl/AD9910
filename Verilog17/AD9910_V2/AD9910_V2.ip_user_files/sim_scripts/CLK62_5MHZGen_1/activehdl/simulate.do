onbreak {quit -force}
onerror {quit -force}

asim -t 1ps +access +r +m+CLK62_5MHZGen -L xil_defaultlib -L xpm -L unisims_ver -L unimacro_ver -L secureip -O5 xil_defaultlib.CLK62_5MHZGen xil_defaultlib.glbl

do {wave.do}

view wave
view structure

do {CLK62_5MHZGen.udo}

run -all

endsim

quit -force
