vlib modelsim_lib/work
vlib modelsim_lib/msim

vlib modelsim_lib/msim/xil_defaultlib
vlib modelsim_lib/msim/xpm

vmap xil_defaultlib modelsim_lib/msim/xil_defaultlib
vmap xpm modelsim_lib/msim/xpm

vlog -work xil_defaultlib -64 -incr -sv -L xil_defaultlib "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -64 -93 \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib -64 -incr "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../../AD9910V2_SERDES.srcs/sources_1/ip/CLK500MHZ_GEN/CLK500MHZ_GEN_clk_wiz.v" \
"../../../../AD9910V2_SERDES.srcs/sources_1/ip/CLK500MHZ_GEN/CLK500MHZ_GEN.v" \

vlog -work xil_defaultlib \
"glbl.v"

