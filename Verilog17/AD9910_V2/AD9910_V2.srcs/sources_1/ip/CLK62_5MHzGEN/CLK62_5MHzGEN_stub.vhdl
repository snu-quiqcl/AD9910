-- Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
-- Date        : Mon Jan  9 04:18:22 2023
-- Host        : LAPTOP-ETOV1IS0 running 64-bit major release  (build 9200)
-- Command     : write_vhdl -force -mode synth_stub
--               c:/Jeonghyun/Lab/TaehyunKim/DDS/AD9910/JHPARK/JeonghyunPark/AD9910_CODE-AD9910V1_1/Verilog17/AD9910_V2/AD9910_V2.srcs/sources_1/ip/CLK62_5MHzGEN/CLK62_5MHzGEN_stub.vhdl
-- Design      : CLK62_5MHzGEN
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7s50csga324-1
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity CLK62_5MHzGEN is
  Port ( 
    CLK62_5MHz : out STD_LOGIC;
    reset : in STD_LOGIC;
    locked : out STD_LOGIC;
    CLK100MHz : in STD_LOGIC
  );

end CLK62_5MHzGEN;

architecture stub of CLK62_5MHzGEN is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "CLK62_5MHz,reset,locked,CLK100MHz";
begin
end;
