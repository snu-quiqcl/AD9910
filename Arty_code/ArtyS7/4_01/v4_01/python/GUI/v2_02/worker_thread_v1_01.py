# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 09:02:17 2018

@author: 1109282
"""

from PyQt5 import QtCore

class worker(QtCore.QObject):
    worker_finished_signal = QtCore.pyqtSignal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.worker_finished_signal.connect(self.controller.worker_finished)

    
    def run(self):
        #try:
        controller = self.controller
        s = controller.gl['s']
        #anal_func = controller.gl['analysis']

        s.program(show=False, target=controller.sequencer)
        controller.sequencer.auto_mode()
        controller.sequencer.send_command('START SEQUENCER')
                
        controller.data = []
        while(controller.sequencer.sequencer_running_status() == 'running'):
            data_count = controller.sequencer.fifo_data_length()
            if data_count > controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            controller.data += controller.sequencer.read_fifo_data(data_count)
            controller.status_display.setText('%d data is read' % len(controller.data))
            
        data_count = controller.sequencer.fifo_data_length()
        while (data_count > 0):
            if data_count > controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE:
                data_count = controller.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
            controller.data += controller.sequencer.read_fifo_data(data_count)
            controller.status_display.setText('%d data is read' % len(controller.data))
            data_count = controller.sequencer.fifo_data_length()
            
        controller.status_display.setText('Total: %d data is read' % len(controller.data))
        if not controller.auto_mode:
            controller.sequencer.manual_mode()
            
        """
        axes_list = []
        for each_win in controller.plot_windows_list:
            each_win.show()
            axes_list.append(each_win.canvas.axes)

        anal_func(controller.data, axes_list)

        for each_win in controller.plot_windows_list:
            each_win.canvas.draw()
        """
        
        self.worker_finished_signal.emit()
        


        #except Exception as e:
        #    self.print_error(e)
        
        
        
    def print_error(self, msg):
        self.controller.print_thread_message('from worker thread(%s): %s' % (self.thread(), msg))
        