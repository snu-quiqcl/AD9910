vlib work
vlib riviera

vlib riviera/xil_defaultlib
vlib riviera/xpm

vmap xil_defaultlib riviera/xil_defaultlib
vmap xpm riviera/xpm

vlog -work xil_defaultlib  -sv2k12 "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \

vcom -work xpm -93 \
"C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \

vlog -work xil_defaultlib  -v2k5 "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" "+incdir+../../../ipstatic" "+incdir+C:/Xilinx/Vivado/2017.3/data/xilinx_vip/include" \
"../../../../AD9910_V2.srcs/sources_1/ip/CLK62_5MHZGen_1/CLK62_5MHZGen_clk_wiz.v" \
"../../../../AD9910_V2.srcs/sources_1/ip/CLK62_5MHZGen_1/CLK62_5MHZGen.v" \

vlog -work xil_defaultlib \
"glbl.v"

