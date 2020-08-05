vlib work
vlib activehdl

vlib activehdl/xil_defaultlib
vlib activehdl/xpm
vlib activehdl/fifo_generator_v13_2_0

vmap xil_defaultlib activehdl/xil_defaultlib
vmap xpm activehdl/xpm
vmap fifo_generator_v13_2_0 activehdl/fifo_generator_v13_2_0

vlog -work xil_defaultlib  -sv2k12 "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93 \
"E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work fifo_generator_v13_2_0  -v2k5 "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../ipstatic/simulation/fifo_generator_vlog_beh.v" \

vcom -work fifo_generator_v13_2_0 -93 \
"../../../ipstatic/hdl/fifo_generator_v13_2_rfs.vhd" \

vlog -work fifo_generator_v13_2_0  -v2k5 "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../ipstatic/hdl/fifo_generator_v13_2_rfs.v" \

vlog -work xil_defaultlib  -v2k5 "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+E:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../../v3_03.srcs/sources_1/ip/fifo_generator_bram_64x1024/sim/fifo_generator_bram_64x1024.v" \

vlog -work xil_defaultlib \
"glbl.v"

