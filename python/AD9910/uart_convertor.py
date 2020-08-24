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
    while True:
        line = rf.readline()
        if not line:
            rf.close()
            wf.close()
            return
        if line[0] == '1' or line[0] == '0':
            num = ( len(line) >> 3 )
            for i in range(num):
                wf.write('1')
                wf.write(line[ i * 8 : ( i + 1 ) * 8])
                wf.write('0')
            wf.write('\n')
            
if __name__ == '__main__':
    convertor()