// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Mon Jan  9 04:18:22 2023
// Host        : LAPTOP-ETOV1IS0 running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode synth_stub
//               c:/Jeonghyun/Lab/TaehyunKim/DDS/AD9910/JHPARK/JeonghyunPark/AD9910_CODE-AD9910V1_1/Verilog17/AD9910_V2/AD9910_V2.srcs/sources_1/ip/CLK62_5MHzGEN/CLK62_5MHzGEN_stub.v
// Design      : CLK62_5MHzGEN
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module CLK62_5MHzGEN(CLK62_5MHz, reset, locked, CLK100MHz)
/* synthesis syn_black_box black_box_pad_pin="CLK62_5MHz,reset,locked,CLK100MHz" */;
  output CLK62_5MHz;
  input reset;
  output locked;
  input CLK100MHz;
endmodule
