// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Wed Jan 31 22:30:17 2018
// Host        : IonTrap7 running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode synth_stub
//               o:/Users/thkim/Arty_S7/Sequencer/v3_05/v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz_stub.v
// Design      : clk_800MHz
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module clk_800MHz(clk_800MHz_out1, clk_800MHz_out2, 
  clk_800MHz_out3, clk_800MHz_out4, clk_800MHz_out5, clk_800MHz_out6, clk_800MHz_out7, reset, 
  locked, clk_in1)
/* synthesis syn_black_box black_box_pad_pin="clk_800MHz_out1,clk_800MHz_out2,clk_800MHz_out3,clk_800MHz_out4,clk_800MHz_out5,clk_800MHz_out6,clk_800MHz_out7,reset,locked,clk_in1" */;
  output clk_800MHz_out1;
  output clk_800MHz_out2;
  output clk_800MHz_out3;
  output clk_800MHz_out4;
  output clk_800MHz_out5;
  output clk_800MHz_out6;
  output clk_800MHz_out7;
  input reset;
  output locked;
  input clk_in1;
endmodule
