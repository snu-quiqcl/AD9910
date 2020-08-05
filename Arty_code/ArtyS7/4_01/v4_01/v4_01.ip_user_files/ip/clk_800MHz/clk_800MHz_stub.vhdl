-- Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
-- --------------------------------------------------------------------------------
-- Tool Version: Vivado v.2017.3 (win64) Build 2018833 Wed Oct  4 19:58:22 MDT 2017
-- Date        : Wed Jan 31 22:30:17 2018
-- Host        : IonTrap7 running 64-bit Service Pack 1  (build 7601)
-- Command     : write_vhdl -force -mode synth_stub
--               o:/Users/thkim/Arty_S7/Sequencer/v3_05/v3_05.srcs/sources_1/ip/clk_800MHz/clk_800MHz_stub.vhdl
-- Design      : clk_800MHz
-- Purpose     : Stub declaration of top-level module interface
-- Device      : xc7s50csga324-1
-- --------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity clk_800MHz is
  Port ( 
    clk_800MHz_out1 : out STD_LOGIC;
    clk_800MHz_out2 : out STD_LOGIC;
    clk_800MHz_out3 : out STD_LOGIC;
    clk_800MHz_out4 : out STD_LOGIC;
    clk_800MHz_out5 : out STD_LOGIC;
    clk_800MHz_out6 : out STD_LOGIC;
    clk_800MHz_out7 : out STD_LOGIC;
    reset : in STD_LOGIC;
    locked : out STD_LOGIC;
    clk_in1 : in STD_LOGIC
  );

end clk_800MHz;

architecture stub of clk_800MHz is
attribute syn_black_box : boolean;
attribute black_box_pad_pin : string;
attribute syn_black_box of stub : architecture is true;
attribute black_box_pad_pin of stub : architecture is "clk_800MHz_out1,clk_800MHz_out2,clk_800MHz_out3,clk_800MHz_out4,clk_800MHz_out5,clk_800MHz_out6,clk_800MHz_out7,reset,locked,clk_in1";
begin
end;
