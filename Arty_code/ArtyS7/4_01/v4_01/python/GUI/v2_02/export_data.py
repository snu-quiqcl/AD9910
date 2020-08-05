# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:46:48 2018

@author: iontrap
"""

import datetime
import os

datestr = datetime.datetime.now().strftime("%Y-%m-%d")
timestr = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
namestr = '_4G_fake_signals_w_no_ion'
#filename = 'O:\\Users\\thkim\\Arty_S7\\Sequencer\\v4_00\\python\\' + timestr +  '.csv'
#filename = 'O:\\Users\\JKKim\\data\\' +datestr +'\\'  + timestr + namestr +  '.csv'
filename = 'O:\\Users\\JHJeong\\data\\' +datestr +'\\'  + timestr + namestr +  '.csv'
directory = os.path.dirname(filename)

if not os.path.exists(directory):
    os.makedirs(directory)
    

data = data_exported
header = header_exported
#
#arrival_time = []
#PMT_arrival_time = []
#pulse_arrival_time = []
#pulse_trigger_not_arrive_count = 0
#for each in data_exported:
#    if each[3] == 100:
#        arrival_time += each[0:3]
#    elif each[3] == 200:
#        PMT_arrival_time += each[0:3]
#    elif each[3] == 300:
#        pulse_arrival_time += each[0:3]
#    elif each[3] == 10:
#        pulse_trigger_not_arrive_count += 1
#    else:
#        print('Unknown signature:', each)
    
    
pulse_trigger_not_arrive_count = 0

PMT1_arrival_time = []
PMT2_arrival_time = []
pulse_arrival_time = []
coincidence_list = []
for each in data:
    if each[3] == 100:
        PMT1_arrival_time += each[0:3]
    elif each[3] == 200:
        PMT2_arrival_time += each[0:3]
    elif each[3] == 300:
        pulse_arrival_time += each[0:3]
    elif each[3] == 10:
        pulse_trigger_not_arrive_count += each[0]
    elif each[3] == 111:            
        coincidence_list.append(each)
    else:
        print('Unknown signature:', each)


with open(filename, 'w') as f:
    f.write(header)
    f.write('## %d times counted for not arrived pulse triggers \n' %pulse_trigger_not_arrive_count)
    for x in range(len(PMT1_arrival_time)):
        f.write('%f, %d, %d, %d\n' %(x*1.25, PMT1_arrival_time[x], PMT2_arrival_time[x], pulse_arrival_time[x]))
    f.write('## coincidence list \n')
    for each in coincidence_list:
        f.write('%d, %d, %d, %d\n' %(each[0], each[1], each[2], each[3]))

'''
with open(filename, 'w') as f:
    f.write(header_exported)
    f.write('## %d times counted for not arrived pulse triggers \n' %pulse_trigger_not_arrive_count)
    for x in range(len(C_arrival_time_PMT1)):
        f.write('%f, %d, %d, %d\n' %(x*1.25, C_arrival_time[x], C_arrival_time_PMT1[x], C_arrival_time_PMT2[x]))
    for x in range(len(C_arrival_time_PMT1)):
        f.write('%f, %d\n' %((x+len(C_arrival_time_PMT1))*1.25, C_arrival_time[(x+len(C_arrival_time_PMT1))]))
'''
                
    
    
        
print('File saved!')