#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 15:51:42 2020

@author: parkjeonghyun
"""
import os

    
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
    wf = open(os.getcwd() + '/test_verilog_sim.txt', 'w')
    print('verilog converting start')
    while True:
        line = rf.readline()
        if not line:
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