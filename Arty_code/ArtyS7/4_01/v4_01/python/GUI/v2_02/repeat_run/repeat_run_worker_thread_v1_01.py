# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 09:02:17 2018

@author: 1109282
"""

from PyQt5 import QtCore
import numpy as np
import random

class worker(QtCore.QObject):
    worker_finished_signal = QtCore.pyqtSignal()

    def __init__(self, run_controller):
        super().__init__()
        self.run_controller = run_controller
        self.worker_finished_signal.connect(self.run_controller.worker_finished)

    
    def run(self):

        
        update_plot = self.run_controller.gl['update_plot']                       
        controller = self.run_controller.controller
                
        controller.sequencer.send_command('START SEQUENCER')
            
        data = []
        while(controller.sequencer.sequencer_running_status() == 'running'):
            data_count = controller.sequencer.fifo_data_length()
            if data_count > controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += controller.sequencer.read_fifo_data(data_count)
            self.run_controller.status_display.setText('%d data is read' % len(data))
            
        data_count = controller.sequencer.fifo_data_length()
        while (data_count > 0):
            if data_count > controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += controller.sequencer.read_fifo_data(data_count)
            self.run_controller.status_display.setText('%d data is read' % len(data))
            data_count = controller.sequencer.fifo_data_length()
        
        self.run_controller.status_display.setText('Total: %d data is read' % len(data))
        
#        data = []
#        for n in range(int(100*random.random())):
#            data.append([n+1, 0, 0, 10])
#        for n in range(40):
#            data.append([int(100*random.random()), int(100*random.random()), int(100*random.random()), 100])

            #self.run_controller.plot_window.show()
        self.arrival_time = update_plot(data, self.run_controller.plot_window.canvas.axes, self.run_controller.plot_window.status_bar)
        if self.run_controller.plot_window.log_checkbox.isChecked():
            self.run_controller.plot_window.canvas.axes.set_yscale('log', nonposy='clip')
        self.run_controller.plot_window.canvas.draw()
        
        self.run_controller.data = data
#        print(self.arrival_time)
        
        if self.run_controller.CPlot:
            if self.run_controller.run_count == 1:
                self.run_controller.CPlot_arrival_time = self.arrival_time
                self.run_controller.CPlot_x = np.arange(len(self.arrival_time))     
            else:
                for i in range(len(self.arrival_time)):
                    self.run_controller.CPlot_arrival_time[i] += self.arrival_time[i]
            self.run_controller.CPlot_window.canvas.axes.cla()            
            self.run_controller.CPlot_window.canvas.axes.bar(self.run_controller.CPlot_x*1.25, self.run_controller.CPlot_arrival_time)
            
            self.run_controller.CPlot_window.canvas.axes.set_title('Cumulaive distribution')
            self.run_controller.CPlot_window.canvas.axes.set_xlabel('Arrival time of pulse picker trigger output w.r.t. stopwatch start (ns)')
            self.run_controller.CPlot_window.canvas.axes.set_ylabel('Number of event')
            
            self.run_controller.CPlot_window.canvas.draw()
            
            

            
        
        self.worker_finished_signal.emit()
        


        #except Exception as e:
        #    self.print_error(e)
        
        
        
    def print_error(self, msg):
        self.controller.print_thread_message('from worker thread(%s): %s' % (self.thread(), msg))
        