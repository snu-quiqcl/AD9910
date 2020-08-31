#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:51:42 2020

@author: parkjeonghyun
"""
import os

VERILOG_HEADER = 'logic Uart_RXD;\n\
logic Uart_TXD;\n\
logic CLK100MHZ;\n\
logic BTN0;\n\
logic BTN1;\n\
logic BTN2;\n\
logic ja_7; //powerdown\n\
wire ja_6; //sdio\n\
logic ja_5; //csb\n\
logic ja_4; //reset\n\
logic ja_3; // sclk\n\
logic ja_2; // powerdown2\n\
wire ja_1; //sdio2\n\
logic ja_0; // csb2\n\
logic jb_0;\n\
logic jb_1;\n\
logic jb_2;\n\
logic jb_3;\n\
logic jb_4;\n\
logic jb_5;\n\
logic jb_6;\n\
logic jb_7;\n\
logic [5:2] led;\n\
logic led0_r;\n\
logic led0_g;\n\
logic led0_b;\n\
logic led1_r;\n\
logic led1_g;\n\
logic led1_b;\n\
logic d5, d4, d3, d2, d1, d0;\n\
wire jc_0;\n\
wire jc_1;\n\
wire jc_2;\n\
wire jc_3;\n\
wire jc_4;\n\
wire jc_5;\n\
wire jc_6;\n\
wire jc_7;\n\
wire jd_0;\n\
wire jd_1;\n\
wire jd_2;\n\
wire jd_3;\n\
wire jd_4;\n\
wire jd_5;\n\
wire jd_6;\n\
wire jd_7;\n\
\n\
logic io_val;\n\
\n\
assign ja_1 = (~main0.AD9910_driver_0.slave_en_wire)? 1\'bz:io_val;\n\
assign ja_6 = (~main0.AD9910_driver_0.slave_en_wire)? 1\'bz:io_val;\n\
\n\
main main0(\n\
    .Uart_RXD(Uart_RXD),\n\
    .Uart_TXD(Uart_TXD),\n\
    .CLK100MHZ(CLK100MHZ),\n\
    .BTN0(BTN0),\n\
    .BTN1(BTN1),\n\
    .BTN2(BTN2),\n\
    .ja_7(ja_7), //powerdown\n\
    .ja_6(ja_6),\n\
    .ja_5(ja_5), //csb\n\
    .ja_4(ja_4), //reset\n\
    .ja_3(ja_3), // sclk\n\
    .ja_2(ja_2), // powerdown2\n\
    .ja_1(ja_1),\n\
    .ja_0(ja_0), // csb2\n\
    .jb_0(jb_0),\n\
    .jb_1(jb_1),\n\
    .jb_2(jb_2),\n\
    .jb_3(jb_3),\n\
    .jb_4(jb_4),\n\
    .jb_5(jb_5),\n\
    .jb_6(jb_6),\n\
    .jb_7(jb_7),\n\
    .jc_0(jc_0),\n\
    .jc_1(jc_1),\n\
    .jc_2(jc_2),\n\
    .jc_3(jc_3),\n\
    .jc_4(jc_4),\n\
    .jc_5(jc_5),\n\
    .jc_6(jc_6),\n\
    .jc_7(jc_7),\n\
    .jd_0(jd_0),\n\
    .jd_1(jd_1),\n\
    .jd_2(jd_2),\n\
    .jd_3(jd_3),\n\
    .jd_4(jd_4),\n\
    .jd_5(jd_5),\n\
    .jd_6(jd_6),\n\
    .jd_7(jd_7),\n\
    .led(led),\n\
    .led0_r(led0_r),\n\
    .led0_g(led0_g),\n\
    .led0_b(led0_b),\n\
    .led1_r(led1_r),\n\
    .led1_g(led1_g),\n\
    .led1_b(led1_b),\n\
    .d5(d5), \n\
    .d4(d4), \n\
    .d3(d3), \n\
    .d2(d2), \n\
    .d1(d1), \n\
    .d0(d0) // For debugging purpose    \n\
    );\n\
   \n\
always begin\n\
    #5\n\
    CLK100MHZ = ~CLK100MHZ;\n\
end\n\
\n\
parameter MAX_LENGTH = 256;\n\
\n\
logic [MAX_LENGTH-1:0] TEMP;\n\
logic [9:0] TEMP_S;\n\
integer i;\n\
initial begin\n\
    //TEMP = (2**256-1) & 256\'b 00001010 00001101 11001100 11001100 11001100 00001100 00000000 00000000 11111111 00111111 00001110 00111001 01100001 00110001 00100011;\n\
    //TEMP = (2**256-1) & 256\'b 1000010100 1000011010 1110011000 1110011000 1110011000 1000011000 1000000000 1000000000 1111111110 1001111110 1000011100 1001110010 1011000010 1001100010 1001000110;\n\
    \n\
    Uart_RXD = 1;\n\
    CLK100MHZ = 0;\n\
    BTN0 = 0;\n\
    BTN1 = 0;\n\
    BTN2 = 0;\n\
    io_val = 1;\n\
'

    
def convertor():
    rf = open(os.getcwd() + '/test_output.txt', 'r')
    wf = open(os.getcwd() + '/test_uart_output.txt', 'w')
    print('converting start')
    while True:
        line = rf.readline()
        if not line:
            rf.close()
            wf.close()
            print('converting end')
            return
        if line[0] == '1' or line[0] == '0':
            num = ( len(line) >> 3 )
            for i in range(num):
                wf.write('1')
                wf.write(line[ i * 8 : ( i + 1 ) * 8])
                wf.write('0')
            wf.write('\n')

def create_sim_file():
    rf = open(os.getcwd() + '/test_uart_output.txt', 'r')
    
    print('verilog converting start')
    
    module_name = input('module name >> ')
    wf = open(os.getcwd() + '/' + module_name + '.sv', 'w')
    wf.write('`timescale 1ns / 1ps\n')
    wf.write('\n')
    wf.write('\n')
    wf.write('module ')
    wf.write(module_name)
    wf.write(';\n')
    wf.write(VERILOG_HEADER)
    wf.write('\n')
    wf.write('\n')
    
    while True:
        line = rf.readline()
        if not line:
            wf.write('end\n')
            wf.write('\n')
            wf.write('endmodule\n')
            rf.close()
            wf.close()
            print('verilog converting end')
            return
        wf.write('    #1000\n')
        wf.write('    TEMP =((2**256 - 1) - (2**' + str(len(line)-1) + '- 1)) + 256\'b')
        wf.write(line[:-1])
        wf.write(';\n')
        wf.write('    for( i = 0; i <= MAX_LENGTH - 1 ; i++ ) begin\n')
        wf.write('        #17361\n')
        wf.write('        Uart_RXD = TEMP[i];\n')
        wf.write('    end\n')

def convertor_chain():
    convertor()
    create_sim_file()
    
if __name__ == '__main__':
    convertor()
    create_sim_file()