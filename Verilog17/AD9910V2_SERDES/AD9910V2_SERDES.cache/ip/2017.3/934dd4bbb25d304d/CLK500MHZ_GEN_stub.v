// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Mon Jan  9 06:20:15 2023
// Host        : LAPTOP-ETOV1IS0 running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode synth_stub -rename_top decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix -prefix
//               decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix_ CLK500MHZ_GEN_stub.v
// Design      : CLK500MHZ_GEN
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module decalper_eb_ot_sdeen_pot_pi_dehcac_xnilix(CLK500MHz, reset, locked, CLK100MHZ)
/* synthesis syn_black_box black_box_pad_pin="CLK500MHz,reset,locked,CLK100MHZ" */;
  output CLK500MHz;
  input reset;
  output locked;
  input CLK100MHZ;
endmodule
