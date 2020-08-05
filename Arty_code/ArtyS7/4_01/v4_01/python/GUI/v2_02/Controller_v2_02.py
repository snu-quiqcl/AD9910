# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 23:24:54 2018

@author: 1109282

* Change log
v1_00: Initial version
v1_01: Working version
v1_02: Changed to use uic.loadUiType() to directly load .ui file

"""

import ImportForSpyderAndQt5
import sys
import os
new_path = os.path.dirname(__file__) + '\\..\\..' # For ArtyS7_v1_01 and other hardware-related definitions
if not (new_path in sys.path):
    sys.path.append(new_path)

from shutil import copyfile

import socket
import configparser

from ArtyS7_v1_02 import ArtyS7
import HardwareDefinition_type_D as hd


from code_editor.code_editor_v2_00 import TextEditor
from worker_thread_v1_01 import worker
from PollingWorker_v1_00 import PollingWorker

from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg') # Make sure that we are using QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

data_exported = []
header_exported = []


from repeat_run.repeat_run_v1_01 import RepeatRunWidget
from pulse_rabi.pulse_Rabi_v1_01 import PulseRabiWidget

qt_designer_file = 'ControllerUI_v2_01.ui'
Ui_Form, QtBaseClass = uic.loadUiType(qt_designer_file)


class Controller(QtWidgets.QWidget, Ui_Form):
    worker_run_signal = QtCore.pyqtSignal()
    Polling_run_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.setupUi(self)
        
        self.editor = TextEditor(window_title = 'Controller program editor')
        self.config_editor = TextEditor(window_title = 'Config editor')
        
        self.sequencer = None
        self.auto_mode = False
        self.COM_port_open = False
        
        self.worker_thread= QtCore.QThread()
        self.worker = worker(self)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker_run_signal.connect(self.worker.run)
        
        self.polling_thread = QtCore.QThread()
        self.polling_worker = PollingWorker(self)
        self.polling_worker.moveToThread(self.polling_thread)
        self.polling_thread.start()
        self.Polling_run_signal.connect(self.polling_worker.run)
        
        self.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE = ArtyS7.MAX_OUTPUT_DATA_FIFO_TRANSMISSION_CHUNK_SIZE

        filename = os.path.abspath(__file__)
        dirname = os.path.dirname(filename)
        config_dir = dirname + '\\config'
        self.config_filename = '%s\\%s.ini' % (config_dir, socket.gethostname())
        self.config_file_label.setText(self.config_filename)
        if not os.path.exists(self.config_filename):
            copyfile('%s\\default.ini' % config_dir, self.config_filename)
        self.reload_config()
        
        self.check_box_mapping = {
            (32-hd.single_shot_out, self.single_shot_checkbox), \
            (32-hd.C1_AOM_on_out, self.C1_AOM_Cool), \
            (32-hd.C1_AOM_switch_out, self.C1_AOM_Detect), \
            (32-hd.C1_EOM_2_1GHz_out, self.C1_EOM_Initialize), \
            (32-hd.C1_EOM_7_37GHz_out, self.C1_EOM_Cooling), \
            (32-hd.C1_Microwave_SW_out, self.C1_Microwave), \
            (32-hd.C2_AOM_on_out, self.C2_AOM_Cool), \
            (32-hd.C2_AOM_switch_out, self.C2_AOM_Detect), \
            (32-hd.C2_EOM_2_1GHz_out, self.C2_EOM_Initialize), \
            (32-hd.C2_EOM_7_37GHz_out, self.C2_EOM_Cooling), \
            (32-hd.C2_Microwave_SW_out, self.C2_Microwave), \
            }
        
     
    def repeat_run(self):
        if (not hasattr(self, 'rr')) or (self.rr == None):
            self.rr = RepeatRunWidget(controller=self, hd_filename = os.path.abspath(hd.__file__))
        self.rr.setWindowState(self.rr.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.rr.raise_()
        self.rr.show()
        
        
    def pulse_rabi(self):
        if (not hasattr(self, 'pR')) or (self.pR == None):
            self.pR = PulseRabiWidget(controller=self, hd_filename = os.path.abspath(hd.__file__))
        self.pR.setWindowState(self.pR.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.pR.raise_()
        self.pR.show()
        

    def worker_finished(self):
        analyze = self.gl['analyze']		
        analyze(self.data)
        self.header = self.gl['header']
         
    def polling_finished(self):
        self.worker_run_signal.emit()
        
        
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
        self.polling_thread.quit()
        
        if self.COM_port_open:
            self.open_COM_port()
            
        if self.editor.isVisible():
            self.editor.quit()
            
        if hasattr(self, 'rr') and (self.rr != None):
            self.rr.close()

        if hasattr(self, 'pR') and (self.pR != None):
            self.pR.close()
            
            
            

    def reload_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        self.COM_port.setText(self.config['COM port']['port'])
        
        self.program_path_line_edit.setText(self.config['sequencer']['last_program'])
          
          
    def edit_config(self):
        self.config_editor.show()
        self.config_editor.open_document_by_external(self.config_filename)

    def config_changed(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        if (self.config['COM port']['port'] != self.COM_port.text()):
            return True
        if (self.config['sequencer']['last_program'] != self.program_path_line_edit.text()):
            return True
        
        return False

    
    def save_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_filename)
        
        self.config['COM port']['port'] = self.COM_port.text()
        self.config['sequencer']['last_program'] = self.program_path_line_edit.text()
        

        with open(self.config_filename, 'w') as new_config_file:
            self.config.write(new_config_file)
            
    def read_manual_output(self):
        bit_pattern_bytes = self.sequencer.read_bit_pattern(debug=False)
        bit_pattern = 32*[0]
        byte_count = 0
        for each_byte in bit_pattern_bytes:
            each_byte = ord(each_byte)
            for n in range(7):
                bit_pattern[8*byte_count+7-n] = (each_byte % 2)
                each_byte = each_byte // 2
            bit_pattern[8*byte_count] = each_byte
            byte_count += 1

        for (pin, check_box) in self.check_box_mapping:
            if bit_pattern[pin-1] == 0:
                check_box.setChecked(False)
            else:
                check_box.setChecked(True)
                

    def send_pulse(self):
        pattern_bit = 32-hd.single_shot_out
        self.sequencer.update_bit_pattern([(pattern_bit, 0),])
        self.sequencer.update_bit_pattern([(pattern_bit, 1),])
        self.sequencer.update_bit_pattern([(pattern_bit, 0),])
        self.single_shot_checkbox.setChecked(False)
        

    def single_shot(self, status):
        pattern_bit = 32-hd.single_shot_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)

        
    def C1_AOM_cooling(self, status):
        pattern_bit = 32-hd.C1_AOM_on_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
            
    
    def C1_AOM_detect(self, status):
        pattern_bit = 32-hd.C1_AOM_switch_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
    
    def C1_EOM_cooling(self, status):
        pattern_bit = 32-hd.C1_EOM_7_37GHz_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
    
    def C1_EOM_initialize(self, status):
        pattern_bit = 32-hd.C1_EOM_2_1GHz_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
    
    def C1_microwave(self, status):
        pattern_bit = 32-hd.C1_Microwave_SW_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
    
    def C1_phase(self):
        pass
    
    def C2_AOM_cooling(self, status):
        pattern_bit = 32-hd.C2_AOM_on_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)
    
    def C2_AOM_detect(self, status):
        pattern_bit = 32-hd.C2_AOM_switch_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)

    
    def C2_EOM_cooling(self, status):
        pattern_bit = 32-hd.C2_EOM_7_37GHz_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)

    
    def C2_EOM_initialize(self, status):
        pattern_bit = 32-hd.C2_EOM_2_1GHz_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)

    
    def C2_phase(self):
        pass

    
    def C2_microwave(self, status):
        pattern_bit = 32-hd.C2_Microwave_SW_out
        if status:
            self.sequencer.update_bit_pattern([(pattern_bit, 1),])
            #print('pattern bit %d on' % pattern_bit)
        else:
            self.sequencer.update_bit_pattern([(pattern_bit, 0),])
            #print('pattern bit %d off' % pattern_bit)

    
    def open_COM_port(self):
        if self.COM_port_open:
            self.sequencer.close()
            self.COM_port_open = False
            self.COM_status = 'Closed'
            self.COM_button.setText('Open')
            self.COM_port.setEnabled(True)
            
            self.control_mode_group.setEnabled(False)
            self.manual_control_group.setEnabled(False)
            self.sequencer_group.setEnabled(False)
            self.application_group.setEnabled(False)
            
        else:
            try:
                self.sequencer = ArtyS7(self.COM_port.text())
            except Exception as e:
                QMessageBox.critical(self, 'Error in opening COM port', str(e))
                return

            try:
                self.sequencer.check_version(hd.HW_VERSION)
            except RuntimeError as e:
                QMessageBox.critical(self, 'Hardware version mismatch', str(e))
                return

            self.COM_port_open = True
            self.COM_status = 'Opened'
            self.COM_button.setText('Close')
            self.COM_port.setEnabled(False)
            
            self.control_mode_group.setEnabled(True)
            
            # Read the current control mode of the sequencer
            control_mode = self.sequencer.control_mode_status()
            if control_mode == 'auto':
                self.set_to_auto_mode()
            else:
                self.set_to_manual_mode()
                """
                self.auto_mode = False
                self.manual_control_group.setEnabled(True)
                self.chamber1_group.setEnabled(True)
                self.chamber2_group.setEnabled(True)
                """
            self.read_manual_output()
            self.sequencer_group.setEnabled(True)
            self.application_group.setEnabled(True)
            

    def set_to_auto_mode(self):
        if (self.sequencer != None) and (self.sequencer.com.isOpen()):
            self.sequencer.auto_mode()
        self.mode_status.setText('Auto')
        self.mode_button.setText('Manual')
        self.manual_control_group.setEnabled(False)
        self.auto_mode = True
        
    def set_to_manual_mode(self):
        if (self.sequencer != None) and (self.sequencer.com.isOpen()):
            self.sequencer.manual_mode()
        self.mode_status.setText('Manual')
        self.mode_button.setText('Auto')
        self.manual_control_group.setEnabled(True)
        self.chamber1_group.setEnabled(True)
        self.chamber2_group.setEnabled(True)
        self.auto_mode = False
        
        

    def change_mode(self):
        if self.auto_mode:
            self.set_to_manual_mode()
            """
            if (self.sequencer != None) and (self.sequencer.com.isOpen()):
                self.sequencer.manual_mode()
            self.mode_status.setText('Manual')
            self.mode_button.setText('Auto')
            self.manual_control_group.setEnabled(True)
            self.chamber1_group.setEnabled(True)
            self.chamber2_group.setEnabled(True)
            self.auto_mode = False
            """
        else:
            self.set_to_auto_mode()
            """
            if (self.sequencer != None) and (self.sequencer.com.isOpen()):
                self.sequencer.auto_mode()
            self.mode_status.setText('Auto')
            self.mode_button.setText('Manual')
            self.manual_control_group.setEnabled(False)
            self.auto_mode = True
            """
            


    
    def set_program_path(self, status):
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


    def run_program_analyze(self):
        current_path = self.program_path_line_edit.text()
        if not self.program_exists(current_path):
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
                        (controller_hd, program_hd))
                    return

                #self.s = gl['s']
                self.gl = gl
                self.worker_run_signal.emit()
                
                        


    def export_data(self):
        global data_exported, header_exported
        data_exported = self.data
        try:
            header_exported = self.header
        except NameError:
            header_exported = '### no header loaded ### \n'
        return

    def update_global_data_header(self, data, header):
        global data_exported, header_exported
        data_exported = data
        header_exported = header
        return
        
                
    def print_thread_message(self, msg):
        print('Error in thread: ' + msg)




if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    mw = Controller()
    mw.show()
    app.exec_()
    #sys.exit(app.exec_())
