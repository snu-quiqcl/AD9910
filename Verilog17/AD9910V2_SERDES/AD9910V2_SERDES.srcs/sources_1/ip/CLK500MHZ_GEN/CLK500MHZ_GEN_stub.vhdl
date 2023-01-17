-- Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
-- Date        : Mon Jan  9 06:31:39 2023
-- Host        : LAPTOP-ETOV1IS0 running 64-bit major release  (build 9200)
-- Command     : write_vhdl -force -mode synth_stub
--               c:/Jeonghyun/Lab/TaehyunKim/DDS/AD9910/JHPARK/JeonghyunPark/AD9910_CODE-AD9910V1_1/Verilog17/AD9910V2_SERDES/AD9910V2_SERDES.srcs/sources_1/ip/CLK500MHZ_GEN/CLK500MHZ_GEN_stub.vhdl
-- Design      : CLK500MHZ_GEN
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7s50csga324-1
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity CLK500MHZ_GEN is
  Port ( 
    CLK500MHZ : out STD_LOGIC;
    reset : in STD_LOGIC;
    locked : out STD_LOGIC;
    CLK100MHZ : in STD_LOGIC
  );

end CLK500MHZ_GEN;

architecture stub of CLK500MHZ_GEN is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "CLK500MHZ,reset,locked,CLK100MHZ";
begin
end;
