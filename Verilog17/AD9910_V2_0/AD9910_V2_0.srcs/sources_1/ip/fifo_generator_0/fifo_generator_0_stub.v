// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Fri Jan  5 22:01:53 2018
// Host        : IonTrap7 running 64-bit Service Pack 1  (build 7601)
// Command     : write_verilog -force -mode synth_stub
//               O:/Users/thkim/Arty_S7/BasicProtocol/v1_01/v1_01.srcs/sources_1/ip/fifo_generator_0/fifo_generator_0_stub.v
// Design      : fifo_generator_0
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
(* x_core_info = "fifo_generator_v13_2_0,Vivado 2017.3" *)
module fifo_generator_0(clk, rst, din, wr_en, rd_en, dout, full, overflow, empty, 
  underflow)
/* synthesis syn_black_box black_box_pad_pin="clk,rst,din[7:0],wr_en,rd_en,dout[7:0],full,overflow,empty,underflow" */;
  input clk;
  input rst;
  input [7:0]din;
  input wr_en;
  input rd_en;
  output [7:0]dout;
  output full;
  output overflow;
  output empty;
  output underflow;
endmodule
