vlib modelsim_lib/work
vlib modelsim_lib/msim

vlib modelsim_lib/msim/xil_defaultlib
vlib modelsim_lib/msim/xpm

vmap xil_defaultlib modelsim_lib/msim/xil_defaultlib
vmap xpm modelsim_lib/msim/xpm

vlog -work xil_defaultlib -64 -incr -sv -L xil_defaultlib "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -64 -93 \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib -64 -incr "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz_clk_wiz.v" \
"../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz.v" \

vlog -work xil_defaultlib \
"glbl.v"

