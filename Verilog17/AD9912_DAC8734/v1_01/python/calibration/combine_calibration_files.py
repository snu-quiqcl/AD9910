# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:27:46 2018

@author: iontrap
"""

import csv

out_file = open('combined_cal.csv', 'w')

higher_voltage_file = open('calibration_DDS1_DAC1_DDS_full_current_ZX73-2500-S+_180521.csv', 'r')
lower_voltage_file = open('calibration_test.csv', 'r')

higher_voltage_data = list(csv.reader(higher_voltage_file, delimiter=','))
lower_voltage_data = list(csv.reader(lower_voltage_file, delimiter=','))

for index in range(len(higher_voltage_data)):
    each_line = higher_voltage_data[index]
    higher_voltage_data[index] = [float(each_line[0]), float(each_line[1]), float(each_line[2]), float(each_line[3])]

for index in range(len(lower_voltage_data)):
    each_line = lower_voltage_data[index]
    lower_voltage_data[index] = [float(each_line[0]), float(each_line[1]), float(each_line[2]), float(each_line[3])]
    
    
lower_index = 0
higher_index = 0
for each_freq in range(10, 101, 5):
    lower_data = lower_voltage_data[lower_index]
    while lower_data[0] == each_freq:
        if abs(lower_data[2] - each_freq) < 0.1:
            out_file.write('%f, %f , %f, %f\n' % (lower_data[0], lower_data[1], lower_data[2], lower_data[3]))
        lower_index += 1
        if lower_index == len(lower_voltage_data):
            break
        lower_data = lower_voltage_data[lower_index]
        
    higher_data = higher_voltage_data[higher_index]
    while higher_data[0] == each_freq:
        out_file.write('%f, %f , %f, %f\n' % (higher_data[0], higher_data[1], higher_data[2], higher_data[3]))
        higher_index += 1
        if higher_index == len(higher_voltage_data):
            break
        higher_data = higher_voltage_data[higher_index]
    

higher_voltage_file.close()
lower_voltage_file.close()
out_file.close()


