import matplotlib.pyplot as plt
import numpy as np


PMT1_arrival_time = []
PMT2_arrival_time = []
for each in PMT1_data:
    PMT1_arrival_time += each[0:3]
for each in PMT2_data:
    PMT2_arrival_time += each[0:3]

PMT1_x = [0]*90
PMT2_x = [0]*90
PMT1_trig = [0]*90
PMT2_trig = [0]*90

for i in range(len(PMT1_x)):
    for kk in range(len(PMT1_data)):
        if i == PMT1_data[kk][0] - PMT1_data[kk][1]:
            PMT1_x[i] += 1

for i in range(len(PMT1_x)):
    for kk in range(len(PMT1_data)):
        if i == PMT1_data[kk][1]:
            PMT1_trig[i] += 1

for i in range(len(PMT2_x)):
    for kk in range(len(PMT2_data)):
        if i == PMT2_data[kk][0] - PMT2_data[kk][1]:
            PMT2_x[i] += 1
            
for i in range(len(PMT2_x)):
    for kk in range(len(PMT2_data)):
        if i == PMT2_data[kk][1]:
            PMT2_trig[i] += 1
      

#%% 
import time
import statistics as stat
import matplotlib.pyplot as plt
from matplotlib import pylab
from scipy import optimize
import datetime

#%% Saving figs
SV_path = 'O:\\Users\\JHJeong\\Data\\'
nowT = datetime.datetime.now()
nowDate = nowT.strftime('%Y%m%d%H%M%S')
File_name = nowDate + '_'        

anomaly_list_PMT1_40 = []
anomaly_list_PMT1_61 = []
for each in PMT1_data:
    if (each[0]-each[1]) == 40:
        anomaly_list_PMT1_40.append(each)
    elif (each[0]-each[1]) == 61:
        anomaly_list_PMT1_61.append(each)
            
        
anomaly_list_PMT2_46 = []
anomaly_list_PMT2_61 = []
for each in PMT2_data:
    if (each[0]-each[1]) == 46:
        anomaly_list_PMT2_46.append(each)
    elif (each[0]-each[1]) == 61:
        anomaly_list_PMT2_61.append(each)

    plt.plot()      

x1 = np.arange(len(PMT1_x))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x1, PMT1_x)
axs.set_title('Photon arrival time of PMT1 w/o ion')
axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig.savefig(SV_path + File_name + 'PMT1_arrival_time' + '.png')

x2 = np.arange(len(PMT1_x))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x2, PMT2_x)
axs.set_title('Photon arrival time of PMT2 w/o ion')
axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig.savefig(SV_path + File_name + 'PMT2_arrival_time' + '.png')


x1 = np.arange(len(PMT1_x))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x1, PMT1_trig)
axs.set_title('Pulse trigger timing of PMT1 w/o ion')
axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig.savefig(SV_path + File_name + 'PMT1_pulse_trigger' + '.png')


x2 = np.arange(len(PMT1_x))
fig, axs = plt.subplots(1, 1, tight_layout=True)
axs.cla()

axs.bar(x2, PMT2_trig)
axs.set_title('Pulse trigger timing of PMT2 w/o ion')
axs.set_xlabel('Photon arrival time distribution w.r.t. pulse picker trigger output (ns)')
axs.set_ylabel('Number of event')
axs.set_yscale('log', nonposy='clip')

fig.savefig(SV_path + File_name + 'PMT2_pulse_trigger' + '.png')

#%% Saving data
with open(SV_path + File_name + 'backreflection' + '_19_clocks' + '.csv', 'w') as ss:
    ss.write('Trial time: 2500000' + '\n')
    
    ss.write('time:')
    for jj in range(len(x1)):
        ss.write(',' + str(x1[jj]))
    ss.write('\n')
    
    ss.write('PMT1:')
    for jj in range(len(x1)):
        ss.write(',' + str(PMT1_x[jj]))
    ss.write('\n')
    
    ss.write('PMT2:')
    for jj in range(len(x1)):
        ss.write(',' + str(PMT2_x[jj]))
    ss.write('\n')
    
    ss.write('1_trig:')
    for jj in range(len(x1)):
        ss.write(',' + str(PMT1_trig[jj]))
    ss.write('\n')
    
    ss.write('2_trig:')
    for jj in range(len(x1)):
        ss.write(',' + str(PMT2_trig[jj]))
    ss.write('\n')
    ss.write('\n')
    
    ss.write('[raw_data_PMT1]')
    ss.write('\n')
    
    for each in PMT1_data:
        ss.write('%d, %d, %d, %d\n' %(each[0], each[1], each[2], each[3]))
    
    ss.write('\n')
    ss.write('[raw_data_PMT2]')
    ss.write('\n')
    
    for each in PMT2_data:
        ss.write('%d, %d, %d, %d\n' %(each[0], each[1], each[2], each[3]))