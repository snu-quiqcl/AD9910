# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 09:02:17 2018

@author: 1109282
"""

from PyQt5 import QtCore
import time
import clipboard

"""
The folling should be added in the controller part

# Define polling worker run signal
    polling_worker_run_signal = QtCore.pyqtSignal()



# Declare polling worker
        self.polling_thread = QtCore.QThread()
        self.polling_worker = PollingWorker(self)
        self.polling_worker.moveToThread(self.polling_thread)
        self.polling_thread.start()
        self.polling_worker_run_signal.connect(self.polling_worker.run)




# Start polling worker

    self.polling_worker_run_signal.emit()




# Add method which will be called once the polling is done
    def polling_finished(self):
        ...
        
"""

class PollingWorker(QtCore.QObject):
    polling_finished_signal = QtCore.pyqtSignal()

    def __init__(self, pulse_rabi_controller):
        super().__init__()
        self.pulse_rabi_controller = pulse_rabi_controller
        self.polling_finished_signal.connect(self.pulse_rabi_controller.polling_finished)

    
    def run(self):
        clipboard.copy("Matlab_turn")
        print('signal sent to Matlab')
        while clipboard.paste() != "Python_turn" :
            time.sleep(1.0)
            if not self.pulse_rabi_controller.running:
                print('stopped immediately')
                break
        print('Align done!')
        self.polling_finished_signal.emit()
        


        #except Exception as e:
        #    self.print_error(e)
        
        
        
    def print_error(self, msg):
        self.controller.print_thread_message('from polling_thread(%s): %s' % (self.thread(), msg))


        