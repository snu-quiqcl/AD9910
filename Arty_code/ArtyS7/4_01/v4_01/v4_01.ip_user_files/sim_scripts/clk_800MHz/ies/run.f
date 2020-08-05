-makelib ies_lib/xil_defaultlib -sv \
  "E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_cdc/hdl/xpm_cdc.sv" \
  "E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_memory/hdl/xpm_memory.sv" \
-endlib
-makelib ies_lib/xpm \
  "E:/Xilinx/Vivado/2017.3/data/ip/xpm/xpm_VCOMP.vhd" \
-endlib
-makelib ies_lib/xil_defaultlib \
  "../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz_clk_wiz.v" \
  "../../../../v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz.v" \
-endlib
-makelib ies_lib/xil_defaultlib \
  glbl.v
-endlib

