-makelib ies_lib/xil_defaultlib -sv \
  "C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
  "C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies_lib/xpm \
  "C:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../../AD9910_V2.srcs/sources_1/ip/CLK62_5MHZGen_1/CLK62_5MHZGen_clk_wiz.v" \
  "../../../../AD9910_V2.srcs/sources_1/ip/CLK62_5MHZGen_1/CLK62_5MHZGen.v" \
-endlib
-makelib ies_lib/xil_defaultlib \
  glbl.v
-endlib

