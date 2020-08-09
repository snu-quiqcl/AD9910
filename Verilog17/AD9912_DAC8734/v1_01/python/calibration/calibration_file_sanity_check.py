# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:27:46 2018

@author: iontrap
"""

import csv

out_file = open('new_calibration.csv', 'w')

calibration_file = open('calibration_DDS2_DAC0_HSTL_FB_connected_DDS_full_current_ZX73-2500-S+_DNA_028A5804965885C_raw.csv', 'r')
#calibration_file = open('new_calibration_2.csv', 'r')

calibration_data = list(csv.reader(calibration_file, delimiter=','))

for index in range(len(calibration_data)):
    each_line = calibration_data[index]
    calibration_data[index] = [float(each_line[0]), float(each_line[1]), float(each_line[2]), float(each_line[3])]

index = 0
stop_requested = False
for each_freq in range(10, 101, 5):
    if stop_requested:
        break
    current_data = calibration_data[index]
    prev_dBm = current_data[3]
    while current_data[0] == each_freq:
        answer = 'n'
        if abs(current_data[2] - each_freq) < 0.2:
            if current_data[3] < prev_dBm:
                print('\nError: dBm is not in ascending order.')
                for n in range(-2, 0):
                    print(calibration_data[index+n])
                print(calibration_data[index], '<<<<<<<<<<<<<<<<<<< will be skipped')
                for n in range(1, 3):
                    print(calibration_data[index+n])
                    
                #print(current_data[3], prev_dBm)
                answer = input('Do you want to skip[Y/n/stop]?')
                if answer == 'stop':
                    stop_requested = True
                    break
            if not (len(answer) == 0 or (answer in 'Yy')):
                out_file.write('%f, %f , %f, %f\n' % (current_data[0], current_data[1], current_data[2], current_data[3]))
                prev_dBm = current_data[3]
        index += 1
        if index == len(calibration_data):
            break
        current_data = calibration_data[index]
        
    

calibration_file.close()
out_file.close()


