import csv
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import dateutil.parser
import dateutil
import datetime

import glob

data_list = [
             'calibration_divider_20-2.csv',
             'calibration_divider_15-3.csv'
             # 'calibration_divider_18.csv'
            ]

freq_list = []
power_list = []
for each_data_filename in data_list:
    with open(each_data_filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    #print ("Total data:", len(data))
    
    # Transpose the data
    temp = list(map(list, zip(*data)))
    
    freq_list.append(list(map(float, temp[0])))
    power_list.append(list(map(float, temp[3])))


plt.rcParams.update({'figure.autolayout': True})


##################################################################
# Example for multiple plots (heterogeneous-type data)
##################################################################
fig = plt.figure(1)
data_count = len(data_list)

axes_list = []
for data_number in range(data_count):
    axes = fig.add_subplot(data_count, 1, data_number+1)
    axes_list.append(axes)

    # Subplot for center frequency
    axes.cla() # In case the previous plot still remains in the given axes. Especially when the figure with the same fig_number is used
    axes.plot(freq_list[data_number], power_list[data_number])
    axes.set(xlabel='Frequency (MHz)', ylabel='Power (dBm)',
           title=data_list[data_number])
    axes.grid()
    if 'freq_ylim' in globals():
        axes.set_ylim(freq_ylim)
    labels = axes.get_xticklabels()
    plt.setp(labels, rotation=45, horizontalalignment='right')

##################################################################

#fig.canvas.manager.window.showMaximized()




