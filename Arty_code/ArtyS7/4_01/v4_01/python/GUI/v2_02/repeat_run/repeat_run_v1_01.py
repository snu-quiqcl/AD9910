# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:06:07 2018

@author: 1109282
"""

import datetime
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


from PyQt5 import uic
qt_designer_file = dirname + '\\repeat_runUI_v1_01.ui'
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

from repeat_run.repeat_run_worker_thread_v1_01 import worker
from repeat_run.repeat_run_PollingWorker_v1_00 import PollingWorker
from plot_window.plot_window_v2_00 import PlotWindow

class RepeatRunWidget(QtWidgets.QWidget, Ui_Form):
    worker_run_signal = QtCore.pyqtSignal()
    polling_run_signal = QtCore.pyqtSignal()
    
    def __init__(self, controller=None, hd_filename=None, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        self.controller = controller
        self.hd_filename = hd_filename
        
        self.editor = TextEditor(window_title = 'Repeat run source editor')
        self.config_editor = TextEditor(window_title = 'Repeat run config editor')

        self.plot_window = PlotWindow('Repeat run plot window')
                    

        self.worker_thread= QtCore.QThread()
        self.worker = worker(self)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker_run_signal.connect(self.worker.run)
        self.keep_worker_run = False
        
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
            
        if self.CPlot_window.isVisible():
            self.CPlot_window.close()
            
        self.controller.rr = None
        

    def reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        sequencer_conf = self.config['sequencer']
        self.program_path_line_edit.setText(sequencer_conf['last_program'])

        repetitions_conf = self.config['Repetitions']
        self.repetition_spinbox.setValue(int(repetitions_conf['repetition']))


    def edit_config(self):
        self.config_editor.show()
        self.config_editor.open_document_by_external(self.config_filename)


    def config_changed(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)

        sequencer_conf = self.config['sequencer']
        if self.program_path_line_edit.text() != sequencer_conf['last_program']:
            return True

        repetitions_conf = self.config['Repetitions']
        if self.repetition_spinbox.value() != int(repetitions_conf['repetition']):
            return True
        
        return False

    
    def save_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        self.config['sequencer']['last_program'] = self.program_path_line_edit.text()

        sequencer_conf = self.config['sequencer']
        sequencer_conf['last_program'] = self.program_path_line_edit.text()

        repetitions_conf = self.config['Repetitions']
        repetitions_conf['repetition'] = str(self.repetition_spinbox.value())

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

    def repeat(self):
        current_path = self.program_path_line_edit.text()
        if not self.program_exists(current_path):
            return
        if self.check_with_editor(current_path):
            if current_path[-3:] == '.py':
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

                #self.s = gl['s']
                self.gl = gl
                self.keep_worker_run = True
                self.plot_window.setWindowState(self.plot_window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
                self.plot_window.raise_()
                self.plot_window.show()
                
                s = gl['s']
                
                controller = self.controller
                s.program(show=False, target=controller.sequencer)
                controller.sequencer.auto_mode()
                                
                self.repeat_group.setEnabled(False)
                self.CPlot_group.setEnabled(False)
                self.repeat_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                
                self.indefinite = self.indefinite_checkbox.isChecked()
                if not self.indefinite:
                    self.run_max = self.repetition_spinbox.value()
                
                self.FLAG_realign = self.realign_checkbox.isChecked()
                self.realign_count = self.realign_count_spinbox.value()
                
                self.CPlot = self.CPlot_checkbox.isChecked()
                
                self.auto_save = self.auto_save_checkbox.isChecked()
                self.save_data_as_file = self.gl['save_data_as_file']
                if self.CPlot:                    
                    self.CPlot_window = PlotWindow('Repeat run cumulative plot window')
                    self.CPlot_window.setWindowState(self.CPlot_window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
                    self.CPlot_window.raise_()
                    self.CPlot_window.show()
                
                
                self.data = []
                self.run_count = 0
                if self.keep_worker_run:
                    self.run_count += 1
                    if self.indefinite:
                        self.current_run_label.setText('Running indefinitely...')
                    else:
                         if self.run_count <= self.run_max:
                             self.current_run_label.setText(str(self.run_count))
                         else:
                             return
                    if self.FLAG_realign & (self.run_count % self.realign_count == 0):
                        self.polling_run_signal.emit()
                    else:
                        self.worker_run_signal.emit()
                         
                    
                
    def stop_repetition(self):
        self.keep_worker_run = False
                
    def worker_finished(self):
        try:
            self.header = self.gl['header']
        except KeyError:
            self.header = "##### no header loaded #####"
            
        if self.auto_save:
            self.save_data_as_file(self.data, self.header, self.run_count)
            
        if self.keep_worker_run:
            self.run_count += 1
            if self.indefinite:
                self.current_run_label.setText('Running indefinitely...')
            else:
                 if self.run_count <= self.run_max:
                     self.current_run_label.setText(str(self.run_count))
                 else:
                     self.stop_process()
                     return
            if self.FLAG_realign & (self.run_count % self.realign_count == 0):
                self.polling_run_signal.emit()
            else:                
                self.worker_run_signal.emit()
        else: 
            self.stop_process()
            
    
    def polling_finished(self):
        if self.keep_worker_run:
            self.worker_run_signal.emit()
        else:
            self.stop_process()
                
    def stop_process(self):
        self.repeat_group.setEnabled(True)
        self.CPlot_group.setEnabled(True)
        self.repeat_button.setEnabled(True)
        self.stop_button.setEnabled(False)               
            
        self.current_run_label.setText('Stopped...')    
        if not self.controller.auto_mode:
            self.controller.sequencer.manual_mode()
                
            
        
    def export_data(self):
        global data_exported, CPlot_arrival_time_exported
        data_exported = self.data
        
        if self.CPlot:            
            CPlot_arrival_time_exported = self.CPlot_arrival_time
        return
    




if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    rr = RepeatRunWidget()
    rr.show()
    app.exec_()
    #sys.exit(app.exec_())

