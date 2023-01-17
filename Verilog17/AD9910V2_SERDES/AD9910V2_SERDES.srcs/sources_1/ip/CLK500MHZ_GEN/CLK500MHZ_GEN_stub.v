// Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
// Date        : Mon Jan  9 06:31:39 2023
// Host        : LAPTOP-ETOV1IS0 running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode synth_stub
//               c:/Jeonghyun/Lab/TaehyunKim/DDS/AD9910/JHPARK/JeonghyunPark/AD9910_CODE-AD9910V1_1/Verilog17/AD9910V2_SERDES/AD9910V2_SERDES.srcs/sources_1/ip/CLK500MHZ_GEN/CLK500MHZ_GEN_stub.v
// Design      : CLK500MHZ_GEN
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7s50csga324-1
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module CLK500MHZ_GEN(CLK500MHZ, reset, locked, CLK100MHZ)
/* synthesis syn_black_box black_box_pad_pin="CLK500MHZ,reset,locked,CLK100MHZ" */;
  output CLK500MHZ;
  input reset;
  output locked;
  input CLK100MHZ;
endmodule
