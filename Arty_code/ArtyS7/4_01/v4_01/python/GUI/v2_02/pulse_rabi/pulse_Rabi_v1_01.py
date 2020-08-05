# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:06:07 2018

@author: 1109282

* Change log
v1_00: 

"""

import sys
import os

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
new_path_list.append(dirname + '\\..') # For ImportForSpyderAndQt5
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)

import ImportForSpyderAndQt5


from code_editor.code_editor_v2_00 import TextEditor
from SG384.SG384_v1_01 import SG384Control
from plot_window.plot_window_v2_00 import PlotWindow
from pulse_rabi.pulse_rabi_worker_thread_v1_00 import worker
from pulse_rabi.Rabi_PollingWorker_v1_00 import PollingWorker

from PyQt5 import uic
qt_designer_file = dirname + '\\pulse_RabiUI_v1_02.ui'
Ui_Form, QtBaseClass = uic.loadUiType(qt_designer_file)


import configparser, socket
from shutil import copyfile

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # Make sure that we are using QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PulseRabiWidget(QtWidgets.QWidget, Ui_Form):
    worker_run_signal = QtCore.pyqtSignal()
    polling_run_signal = QtCore.pyqtSignal()
    
    def __init__(self, parent=None, controller=None, hd_filename=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)


        self.controller = controller
        self.hd_filename = hd_filename
        
        self.editor = TextEditor(window_title = 'Repeat run source editor')
        self.config_editor = TextEditor(window_title = 'Repeat run config editor')
        
        self.editor = TextEditor(window_title = 'Rabi with pulse program editor')

        self.plot_window = PlotWindow('pulse Rabi plot window')

        self.worker_thread= QtCore.QThread()
        self.worker = worker(self)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker_run_signal.connect(self.worker.run)
        self.running = False
        
        self.polling_thread = QtCore.QThread()
        self.polling_worker = PollingWorker(self)
        self.polling_worker.moveToThread(self.polling_thread)
        self.polling_thread.start()
        self.polling_run_signal.connect(self.polling_worker.run)

        filename = os.path.abspath(__file__)
        dirname = os.path.dirname(filename)
        config_dir = dirname + '\\config'
        self.config_filename = '%s\\%s.ini' % (config_dir, socket.gethostname())
        self.config_file_label.setText(self.config_filename)
        if not os.path.exists(self.config_filename):
            copyfile('%s\\default.ini' % config_dir, self.config_filename)
        self.reload_config()
        
        self.RF_generator = SG384Control(connection_callback = self.connection_callback)
        self.RF_generator.IP_address.setText(self.IP_address)
        self.frame.setEnabled(False)


    def connection_callback(self, status):
        self.frame.setEnabled(status)
        if status:
            self.RF_generator_status.setText('Connected')
        else:
            self.RF_generator_status.setText('Disconnected')
            


    def closeEvent(self, event):
        if self.config_changed():
            buttonReply = QMessageBox.question(self, 'Configuration changed', \
                'Some of the configuration is changed. Do you want to save to the config file?', \
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if buttonReply == QMessageBox.Cancel:
                event.ignore()
                return
            elif buttonReply == QMessageBox.Yes:
                self.save_config()
        
        self.worker_thread.quit()
            
        if self.editor.isVisible():
            self.editor.quit()

        if self.config_editor.isVisible():
            self.config_editor.quit()
            
        if self.plot_window.isVisible():
            self.plot_window.close()
            
        if self.controller != None:
            self.controller.pR = None
            
        self.RF_generator.close()
        

    def open_RF_generator(self):
        self.RF_generator.show()

    def reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        sequencer_conf = self.config['sequencer']
        self.program_path_line_edit.setText(sequencer_conf['last_program'])

        power_sweep_conf = self.config['power sweep settings']
        self.start_spinbox.setValue(float(power_sweep_conf['start']))
        self.stop_spinbox.setValue(float(power_sweep_conf['stop']))
        self.step_spinbox.setValue(float(power_sweep_conf['step']))

        RF_generator_conf = self.config['RF generator']
        self.IP_address = RF_generator_conf['IP_address']

    def edit_config(self):
        self.config_editor.show()
        self.config_editor.open_document_by_external(self.config_filename)


    def config_changed(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)

        sequencer_conf = self.config['sequencer']
        if self.program_path_line_edit.text() != sequencer_conf['last_program']:
            return True

        power_sweep_conf = self.config['power sweep settings']
        if self.start_spinbox.value() != float(power_sweep_conf['start']):
            return True
        if self.stop_spinbox.value() != float(power_sweep_conf['stop']):
            return True
        if self.step_spinbox.value() != float(power_sweep_conf['step']):
            return True

        RF_generator_conf = self.config['RF generator']
        if self.RF_generator.IP_address.text() != RF_generator_conf['IP_address']:
            return True

        
        return False

    
    def save_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        self.config['sequencer']['last_program'] = self.program_path_line_edit.text()

        sequencer_conf = self.config['sequencer']
        sequencer_conf['last_program'] = self.program_path_line_edit.text()

        power_sweep_conf = self.config['power sweep settings']
        power_sweep_conf['start'] = str(self.start_spinbox.value())
        power_sweep_conf['stop'] = str(self.stop_spinbox.value())
        power_sweep_conf['step'] = str(self.step_spinbox.value())
        
        RF_generator_conf = self.config['RF generator']
        RF_generator_conf['IP_address'] = self.RF_generator.IP_address.text()

        with open(self.config_filename, 'w') as new_config_file:
            self.config.write(new_config_file)



    def choose_program(self, status):
        current_path = self.program_path_line_edit.text()
        if len(current_path) == 0:
            current_path = os.getcwd()
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose program for sequencer', \
            current_path, 'Python Files (*.py);;All Files (*)')

        if fname[0]:
            self.program_path_line_edit.setText(fname[0])


    def program_exists(self, program):
        if os.path.exists(program):
            return True
        else:
            QMessageBox.critical(self, 'Program file not found', \
                program + '\n\ndoes not exist. Please check the path for the ' + \
                'program before you continue.')
            return False
        


    def edit_program(self, status):
        self.editor.show()
        current_path = self.program_path_line_edit.text()
        if self.program_exists(current_path):
            self.editor.open_document_by_external(current_path)
        else:
            return


    def check_with_editor(self, current_path):
        """ Returns True if it is ok to run current_path
            Returns False if we should not run
        """
        if self.editor.isVisible():
            current_program_in_editor = self.editor.current_filename
            if current_program_in_editor != '':
                if current_program_in_editor != current_path:
                    buttonReply = QMessageBox.warning(self, 'Warning', \
                        ('Source editor: %s\n\nChosen program: %s\n\nare different. ' \
                        + 'Do you still want to continue?') % \
                        (current_program_in_editor, current_path), \
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if buttonReply == QMessageBox.No:
                        return False
                else:
                    if self.editor.text_edited:
                        buttonReply = QMessageBox.warning(self, 'Warning', \
                            'There is unsaved changes in the source editor.' \
                            + 'Do you want to save the changes before you continue?', \
                            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
                        if buttonReply == QMessageBox.Cancel:
                            return False
                        elif buttonReply == QMessageBox.Yes:
                            if not self.editor.save():
                                return False
        return True
    

    def export_data(self):
        data_exported = [self.xdata, self.ydata]
        ## Temporary
        self.header = self.gl['header']
        self.data = self.data
        try:
            header_exported = self.gl['header']
        except NameError:
            header_exported = '%% no header loaded %% \n'
        self.controller.update_global_data_header(data_exported, header_exported)
        #print('export_data:', data_exported, 'header', header_exported)
        
            
        
        
    def run(self):
        if self.running:
            self.running = False
            return
        
        if not self.RF_generator.output_on:
            buttonReply = QMessageBox.critical(self, 'RF generator is off', \
                'The output of the RF generator is off. Do you still want to continue?', \
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.No:
                return

        current_path = self.program_path_line_edit.text()
        if not self.program_exists(current_path):
            return
        if not self.check_with_editor(current_path):
            return
        
        if current_path[-3:] != '.py':
            return
        
        script_filename = os.path.basename(current_path)
        script_name = script_filename[:-3]
        gl = dict(globals())
        gl['__name__'] = script_name
        gl['__file__'] = current_path
        exec(open(current_path).read(), gl)

        program_hd = os.path.abspath(gl['hd'].__file__)
        if self.hd_filename != program_hd:
            QMessageBox.critical(self, 'Error in program execution', \
                'Hardware definition in controller (%s) is different' \
                + ' from what is used in program (%s).' % \
                (self.hd_filename, program_hd))
            return

        self.gl = gl
        s = self.gl['s']
        
        self.count_for_plot = self.gl['count_for_plot']

        self.sequencer = self.controller.sequencer
        s.program(show=False, target=self.sequencer)
        self.sequencer.auto_mode()

        self.plot_window.setWindowState(self.plot_window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.plot_window.raise_()
        self.plot_window.show()

        self.start = self.start_spinbox.value()
        self.stop = self.stop_spinbox.value()
        self.step = self.step_spinbox.value()
        
        self.align_count = self.Realign_count_spinbox.value()

#        dummy_xdata = np.arange(self.start, self.stop+self.step, self.step)
#        dummy_ydata = np.zeros_like(dummy_xdata)
#        
#        self.line_list = self.plot_window.canvas.axes.plot(dummy_xdata, dummy_ydata)
        self.xdata = []
        self.ydata = []
        self.run_count = 0
        self.current = self.start
        if (self.current <= self.stop):
            self.xdata.append(self.current)
            self.RF_generator.set_power_mW(self.current)
            self.current_power_label.setText(str(self.current))
            self.current += self.step
            self.run_count += 1
            self.worker_run_signal.emit()
            
        self.run_button.setText('Stop')
        self.running = True
            
            
    def worker_finished(self):
        self.ydata.append(self.count_for_plot(self.data, self.plot_window.status_bar))
        self.plot_window.canvas.axes.cla()
        self.plot_window.canvas.axes.plot(self.xdata, self.ydata)
        self.plot_window.canvas.draw()

        if self.running and (self.current <= self.stop):
            self.xdata.append(self.current)
            self.RF_generator.set_power_mW(self.current)
            self.current_power_label.setText(str(self.current))
            self.current += self.step
            self.run_count += 1
            if self.align_count != 0:
                if self.run_count % self.align_count == 0:
                    self.polling_run_signal.emit()
                else:
                    self.worker_run_signal.emit()
            else:
                self.worker_run_signal.emit()
            return
        else:
            self.stop_process()

    def polling_finished(self):
        if self.running:
            self.worker_run_signal.emit()
        else:
            self.stop_process()            
            
    def stop_process(self):
        if not self.controller.auto_mode:
            self.controller.sequencer.manual_mode()
        self.run_button.setText('Run')
        self.running = False
        



if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    pR = PulseRabiWidget()
    pR.show()
    app.exec_()
    #sys.exit(app.exec_())

