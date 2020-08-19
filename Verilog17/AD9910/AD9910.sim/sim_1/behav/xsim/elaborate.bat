@echo off
REM ****************************************************************************
REM Vivado (TM) v2017.3 (64-bit)
REM
REM Filename    : elaborate.bat
REM Simulator   : Xilinx Vivado Simulator
REM Description : Script for elaborating the compiled design
REM
REM Generated by Vivado on Wed Aug 19 16:30:38 +0900 2020
REM SW Build 2018833 on Wed Oct  4 19:58:22 MDT 2017
REM
REM Copyright 1986-2017 Xilinx, Inc. All Rights Reserved.
REM
REM usage: elaborate.bat
REM
REM ****************************************************************************
call xelab  -wto c410dce74b084c639dc5e6e81cac80b5 --incr --debug typical --relax --mt 2 -L fifo_generator_v13_2_0 -L xil_defaultlib -L unisims_ver -L unimacro_ver -L secureip -L xpm --snapshot new_testbench_fifo_generator_behav xil_defaultlib.new_testbench_fifo_generator xil_defaultlib.glbl -log elaborate.log
if "%errorlevel%"=="0" goto SUCCESS
if "%errorlevel%"=="1" goto END
:END
exit 1
:SUCCESS
exit 0