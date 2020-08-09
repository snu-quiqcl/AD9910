# -*- coding: utf-8 -*-
"""
Created on Fri May 18 12:13:34 2018

@author: 1109282
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io
from ds1054z import DS1054Z # To install the package, open "Anaconda Prompt", type "pip install ds1054z[savescreen,discovery]"

def show_screen(scope):
    global image_fig, image_axis
    print('Getting screen image...')
    png_image = Image.open(io.BytesIO(scope.display_data)) # This property will be updated every time you access it.
    if not 'image_axis' in globals():
        image_fig = plt.figure(10)
        image_axis = image_fig.add_subplot(1,1,1)
    else:
        image_axis.cla()
    image_axis.imshow(png_image)
    if image_fig.canvas.manager.window.isHidden():
        image_fig.canvas.manager.window.show()
    image_fig.canvas.manager.window.activateWindow()
    #image_fig.canvas.manager.window.showMaximized()

def plot_data(x_data, y_data_list):
    global plot_data_fig, plot_data_axis
    if not 'plot_data_axis' in globals():
        plot_data_fig = plt.figure(11)
        plot_data_axis = plot_data_fig.add_subplot(1,1,1)
    else:
        plot_data_axis.cla()
    for each_data in y_data_list:
        plot_data_axis.plot(x_data*1e9, each_data)
    plot_data_axis.set(xlabel='Time (ns)', ylabel='Voltage (V)')
    plot_data_axis.grid()
    if plot_data_fig.canvas.manager.window.isHidden():
        plot_data_fig.canvas.manager.window.show()
    plot_data_fig.canvas.manager.window.activateWindow()
    
def show_chan1(scope):
    chan1_data = scope.get_waveform_samples('CHAN1')
    x_data = np.linspace(0, 12*scope.timebase_scale, len(chan1_data))
    plot_data(x_data, chan1_data)


if __name__ == '__main__':
    if 'scope' in globals():
        scope.open()
    else:
        scope = DS1054Z('10.1.1.87')
    #print(scope.query('*IDN?'))
    print(scope.idn)
    
    chan1_data = scope.get_waveform_samples('CHAN1')
    x_data = np.linspace(0, 12*scope.timebase_scale, len(chan1_data))
    chan2_data = scope.get_waveform_samples('CHAN2')
    chan3_data = scope.get_waveform_samples('CHAN3')
    plot_data(x_data, [chan1_data, chan2_data, chan3_data])
    
    scope.display_channel(2, enable=True)
    scope.display_channel(3, enable=True)
    
    #scope.ask(':DISPlay:DATA?') # This does not work for unknown reason

"""    
    show_chan1(scope)
    show_screen(scope)
    scope.set_channel_scale('CHAN1', 0.5, use_closest_match=True)
    scope.get_channel_measurement('CHAN1', 'frequency', type='CURRent')
    scope.close()
"""
