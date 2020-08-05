# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 22:06:07 2018

@author: 1109282
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


from PyQt5 import uic
qt_designer_file = dirname + '\\pulse_RabiUI_v1_00.ui'
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


class pulse_Rabi_widget(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        self.editor = TextEditor(window_title = 'Rabi with pulse program editor')

        """
        self.worker_thread= QtCore.QThread()
        self.worker = worker(self)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker_run_signal.connect(self.worker.run)
        
        self.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE = ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE
        """
        
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
        
        #self.worker_thread.quit()
            
        if self.editor.isVisible():
            self.editor.quit()


    def reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        sequencer_conf = self.config['sequencer']
        self.program_path_line_edit.setText(sequencer_conf['last_program'])

        power_sweep_conf = self.config['power sweep settings']
        self.start_spinbox.setValue(float(power_sweep_conf['start']))
        self.stop_spinbox.setValue(float(power_sweep_conf['stop']))
        self.step_spinbox.setValue(float(power_sweep_conf['step']))

        single_data_conf = self.config['single data point settings']
        self.repetition_spinbox.setValue(int(single_data_conf['repetition']))
        self.threshold_spinbox.setValue(int(single_data_conf['threshold']))


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

        single_data_conf = self.config['single data point settings']
        if self.repetition_spinbox.value() != int(single_data_conf['repetition']):
            return True
        if self.threshold_spinbox.value() != int(single_data_conf['threshold']):
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
        
        single_data_conf = self.config['single data point settings']
        single_data_conf['repetition'] = str(self.repetition_spinbox.value())
        single_data_conf['threshold'] = str(self.threshold_spinbox.value())


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

    """
    def run_program_analyze(self):
        current_path = self.program_path_line_edit.text()
        if self.program_exists(current_path):
            self.editor.open_document_by_external(current_path)
        else:
            return
        if self.check_with_editor(current_path):
            #print('Run')
            if current_path[-3:] == '.py':
                script_filename = os.path.basename(current_path)
                script_name = script_filename[:-3]
                gl = dict(globals())
                gl['__name__'] = script_name
                gl['__file__'] = current_path
                exec(open(current_path).read(), gl)
                controller_hd = os.path.abspath(hd.__file__)
                program_hd = os.path.abspath(gl['hd'].__file__)
                if controller_hd != program_hd:
                    QMessageBox.critical(self, 'Error in program execution', \
                        'Hardware definition in controller (%s) is different' \
                        + ' from what is used in program (%s).' % \
                        (controller_hd, controller_hd))
                    return

                #self.s = gl['s']
                self.gl = gl
                self.worker_run_signal.emit()
    """

    def export_data(self):
        global data_exported
        data_exported = self.data
        return
        
    def run(self):
        print('Run button is pressed')
    



if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    pR = pulse_Rabi_widget()
    pR.show()
    app.exec_()
    #sys.exit(app.exec_())

