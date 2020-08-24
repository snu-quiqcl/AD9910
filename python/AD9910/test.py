#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:43:56 2020

@author: parkjeonghyun
"""
from unit_set import *
import os

with open(os.getcwd() + '/test_output.txt', 'w') as f:
    f.write('hello world')

print(os.getcwd() + '/test_os.txt')
print(1*MHz) 
print(180*DEG)
