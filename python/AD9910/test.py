#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:43:56 2020

@author: parkjeonghyun
"""
from unit_set import *
from AD9910 import AD9910
from Arty_S7_v1_01 import ArtyS7
from uart_convertor import convertor_chain

def exp1():
    dds = AD9910(ArtyS7('COM12'))
    dds.reset_driver()
    dds.auto_mode()
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 50*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 0)
    dds.delay_cycle(500)
    dds.set_profile_register(ch1 = 1, ch2 = 1, freq = 100*MHz, phase = 0 * RAD, 
                             amplitude = 1.0, profile = 1)
    dds.delay_cycle(500)
    dds.set_profile_pin(profile1 = 1, profile2 = 0)
    dds.delay_cycle(1000)
    while True:
        print('[1] auto start')
        print('[2] auto stop')
        print('[q] exit')
        s = input()
        if( s == '1' ):
            dds.auto_start()
        elif( s == '2'):
            dds.auto_stop()
        elif( s == 'q'):
            print('exit exp1')
            dds.fpga.close()
            return

def exp2():
    print('hi')
    
if __name__ == '__main__':
    while True:
        print('[1] exp1')
        print('[2] exp2')
        print('[c] convert')
        print('[q] exit')
        s = input()
        if( s == '1' ):
            exp1()
        elif( s == '2'):
            exp2()
        elif( s == 'c'):
            convertor_chain()
        elif( s == 'q'):
            print('exit')
            break
