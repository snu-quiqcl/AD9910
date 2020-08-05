vlib work
vlib riviera

vlib riviera/xil_defaultlib
vlib riviera/xpm

vmap xil_defaultlib riviera/xil_defaultlib
vmap xpm riviera/xpm

vlog -work xil_defaultlib  -sv2k12 "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93 \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib  -v2k5 "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz_clk_wiz.v" \
"../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz.v" \

vlog -work xil_defaultlib \
"glbl.v"

