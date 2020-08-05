# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 09:02:17 2018

@author: 1109282
"""

from PyQt5 import QtCore

class worker(QtCore.QObject):
    worker_finished_signal = QtCore.pyqtSignal()

    def __init__(self, pulse_rabi_controller):
        super().__init__()
        self.pulse_rabi_controller = pulse_rabi_controller
        self.worker_finished_signal.connect(self.pulse_rabi_controller.worker_finished)

    
    def run(self):
        pulse_rabi_controller = self.pulse_rabi_controller
        
        MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE = pulse_rabi_controller.controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
        sequencer = pulse_rabi_controller.sequencer
            
        sequencer.send_command('START SEQUENCER')
                
        data = []
        while(sequencer.sequencer_running_status() == 'running'):
            data_count = sequencer.fifo_data_length()
            if data_count > MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += sequencer.read_fifo_data(data_count)
            pulse_rabi_controller.status_display.setText('%d data is read' % len(data))
            
        data_count = sequencer.fifo_data_length()
        while (data_count > 0):
            if data_count > MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            data += sequencer.read_fifo_data(data_count)
            pulse_rabi_controller.status_display.setText('%d data is read' % len(data))
            data_count = sequencer.fifo_data_length()
        
        pulse_rabi_controller.status_display.setText('Total: %d data is read' % len(data))

        pulse_rabi_controller.data = data
        #self.run_controller.plot_window.show()
        #update_plot(data, self.run_controller.plot_window.canvas.axes, self.run_controller.plot_window.status_bar)
        #if self.run_controller.plot_window.log_checkbox.isChecked():
        #    self.run_controller.plot_window.canvas.axes.set_yscale('log', nonposy='clip')
        #self.run_controller.plot_window.canvas.draw()

        self.worker_finished_signal.emit()
            
            
        
        


        #except Exception as e:
        #    self.print_error(e)
        
        
        
    def print_error(self, msg):
        self.controller.print_thread_message('from worker thread(%s): %s' % (self.thread(), msg))
        