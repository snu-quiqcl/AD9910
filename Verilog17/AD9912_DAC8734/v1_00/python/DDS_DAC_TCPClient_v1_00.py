# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 00:10:48 2018

@author: 1109282

* Change log
v1_00: Initial working version

"""
# from http://wiki.python.org/moin/TcpCommunication
# About SCPI over TCP: page 12 from ftp://ftp.datx.com/Public/DataAcq/MeasurementInstruments/Manuals/SCPI_Measurement.pdf

from __future__ import unicode_literals
import os, sys
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
new_path_list.append(dirname + '\\ui_resources') # For resources_rc.py
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)

import ImportForSpyderAndQt5

from PyQt5 import uic
qt_designer_file = dirname + '\\DDS_DAC_UI_v1_00.ui'
Ui_QDialog, QtBaseClass = uic.loadUiType(qt_designer_file)
ICON_ON = ":/icons/Toggle_Switch_ON_64x34.png"
ICON_OFF = ":/icons/Toggle_Switch_OFF_64x34.png"


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

import math
import socket

class DDS_DAC(QtWidgets.QDialog, Ui_QDialog):
    
    def __init__(self, parent=None, connection_callback=None):
        QtWidgets.QDialog.__init__(self, parent)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        self.DDS1_old_Vpp_stepBy = self.DDS1_Vpp_spinbox.stepBy
        self.DDS1_Vpp_spinbox.stepBy = self.DDS1_new_Vpp_stepBy

        self.DDS1_old_mW_stepBy = self.DDS1_mW_spinbox.stepBy
        self.DDS1_mW_spinbox.stepBy = self.DDS1_new_mW_stepBy

        self.DDS1_old_dBm_stepBy = self.DDS1_dBm_spinbox.stepBy
        self.DDS1_dBm_spinbox.stepBy = self.DDS1_new_dBm_stepBy

        self.DDS1_old_freq_stepBy = self.DDS1_freq_spinbox.stepBy
        self.DDS1_freq_spinbox.stepBy = self.DDS1_new_freq_stepBy
        self.DDS1_prev_freq_unit_index = self.DDS1_freq_unit.currentIndex()
        
        self.connected = False
        self.connection_callback = connection_callback
        
        self.on_pixmap = QtGui.QPixmap(ICON_ON)
        self.on_icon = QtGui.QIcon(self.on_pixmap)

        self.off_pixmap = QtGui.QPixmap(ICON_OFF)
        self.off_icon = QtGui.QIcon(self.off_pixmap)

        self.DDS1_groupBox.setEnabled(False)
        
        


    def query(self, message):
        """ Send the message and read the reply.
        
        Args:
            query (unicode string): query
        
        Returns:
            unicode string: reply string
        """
        self.socket.send((message+'\n').encode('latin-1'))
        data = self.socket.recv(1024)
        data_decoded = data.decode('latin-1')
        if data_decoded[-1] != '\n':
            print(data_decoded)
            raise ValueError('Error in query: the returned message is not finished with \"\\n\"')
            
        return data_decoded[:-1] # Removing the trailing '\n'

    
    def write(self, message):
        """ Send the command.
        
        Args:
            message (unicode string): message to send
        
        Returns:
            None
        """
        self.socket.send((message + '\n').encode('latin-1'))


    def read(self):
        """ Reads data from the device.
        
        Args:
            None
        
        Returns:
            unicode string: received string
        """
        data = self.socket.recv(1024)
        data_decoded = data.decode('latin-1')
        if data_decoded[-1] != '\n':
            raise ValueError('Error in read: the returned message is not finished with \\n')
            
        return data_decoded[:-1] # Removing the trailing '\n'
        




    
    def closeEvent(self, event):

        if hasattr(self, 'socket') and self.socket.fileno() != -1:
            buttonReply = QMessageBox.warning(self, 'Connection to SG384 is still open', \
                'Do you want to close the connection to the device?', \
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
            if buttonReply == QMessageBox.Cancel:
                event.ignore()
                return
            elif buttonReply == QMessageBox.Yes:
                self.socket.close()
                if self.connection_callback != None:
                    self.connection_callback(False)

        # Clean-up
        self.DDS1_Vpp_spinbox.stepBy = self.DDS1_old_Vpp_stepBy
        self.DDS1_mW_spinbox.stepBy = self.DDS1_old_mW_stepBy
        self.DDS1_dBm_spinbox.stepBy = self.DDS1_old_dBm_stepBy
        self.DDS1_freq_spinbox.stepBy = self.DDS1_old_freq_stepBy

            

    def connect_to_DDS(self):
        if self.connected:
            self.socket.close() 
            self.IDN_label.setText('')
            
            self.connection_status.setText('Disconnected')
            self.connect_button.setText('Connect')
            self.DDS1_groupBox.setEnabled(False)
            self.connected = False
            if self.connection_callback != None:
                self.connection_callback(False)

            
        else:
            self.TCP_IP = self.IP_address.text()
            self.TCP_PORT = int(self.port.text())
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.TCP_IP, self.TCP_PORT))
            self.socket.settimeout(1) # unit in second?
            
            connection_status = self.read()
            if connection_status[:2] == 'A:':
                QMessageBox.critical(self, 'Connection to Dual DDS server failed', \
                    ('There is another active connection. Please disconnect another connection from %s first.' % str(connection_status[2:])), \
                    QMessageBox.Ok, QMessageBox.Ok)
                return
            elif connection_status[:2] == 'C:':
                #print('This connection became active')
                pass

            self.IDN_label.setText('connected to '+self.query('*IDN?')) # 'TCP Server for DAC8734 CH0 AOUT0'

            #print(self.query('Q:DDS1:RFOUT'))

            if self.query('Q:DDS1:RFOUT') == 'False':
                self.DDS1_output_button.setIcon(self.off_icon)
                self.DDS1_output_on = False
            else:
                self.DDS1_output_button.setIcon(self.on_icon)
                self.DDS1_output_on = True

            if self.query('Q:DDS2:TRIG') == 'False':
                self.DDS2_trigger_button.setIcon(self.off_icon)
                self.DDS2_trigger_on = False
            else:
                self.DDS2_trigger_button.setIcon(self.on_icon)
                self.DDS2_trigger_on = True


            self.DDS1_read_power()
            self.DDS1_read_freq()
            
            self.connection_status.setText('Connected')
            self.connect_button.setText('Disconnect')
            self.DDS1_groupBox.setEnabled(True)
            self.connected = True
            if self.connection_callback != None:
                self.connection_callback(True)
            
            
    def DDS1_read_power(self):
        dBm = float(self.query('Q:DDS1:POWER'))
        self.DDS1_dBm_spinbox.setValue(dBm)
        mW = 10**(dBm/10)
        Vamp = math.sqrt(mW/10)
        self.DDS1_mW_spinbox.setValue(mW)
        self.DDS1_Vpp_spinbox.setValue(2*Vamp)

        
    
    def DDS1_apply_power(self):
        dBm = self.DDS1_dBm_spinbox.value()
        self.write('DDS1:POWER %.2f' % dBm)
    
    def DDS1_read_freq(self):
        query = 'Q:DDS1:FREQ'
        freq_in_MHz = float(self.query(query))
        
        DDS1_freq_unit_index = self.DDS1_freq_unit.currentIndex()
        scale = 10**(3*DDS1_freq_unit_index)
        
        self.DDS1_freq_spinbox.setValue((freq_in_MHz*1e6)/scale)



    
    def DDS1_apply_freq(self):
        DDS1_freq_unit_index = self.DDS1_freq_unit.currentIndex()
        scale = 10**(3*DDS1_freq_unit_index)
        freq_in_MHz = self.DDS1_freq_spinbox.value() * scale /1e6
        self.write('DDS1:FREQ %f' % freq_in_MHz)

    def DDS1_output_on_off(self):
        if self.DDS1_output_on:
            self.write('DDS1:RFOUT False')
            self.DDS1_output_button.setIcon(self.off_icon)
            self.DDS1_output_on = False
        else:
            self.write('DDS1:RFOUT True')
            self.DDS1_output_button.setIcon(self.on_icon)
            self.DDS1_output_on = True


    def DDS2_trigger_on_off(self):
        if self.DDS2_trigger_on:
            self.write('DDS2:TRIG False')
            self.DDS2_trigger_button.setIcon(self.off_icon)
            self.DDS2_trigger_on = False
        else:
            self.write('DDS2:TRIG True')
            self.DDS2_trigger_button.setIcon(self.on_icon)
            self.DDS2_trigger_on = True




            
    
    def DDS1_new_freq_stepBy(self, steps):
        self.DDS1_old_freq_stepBy(steps)
        self.DDS1_freq_updated()

    def DDS1_freq_editing_finished(self):
        self.DDS1_freq_updated()

    def DDS1_freq_updated(self):
        #print('Freq', self.DDS1_freq_spinbox.value())
        if self.DDS1_auto_freq_apply_checkbox.isChecked():
            self.DDS1_apply_freq()

    
    def DDS1_freq_unit_changed(self, index):
        #print('freq_unit_changed', self.DDS1_freq_unit.currentIndex())
        DDS1_new_freq_unit_index = self.DDS1_freq_unit.currentIndex()
        scale = 10**(3*(DDS1_new_freq_unit_index - self.DDS1_prev_freq_unit_index))
        
        self.DDS1_freq_spinbox.setValue(self.DDS1_freq_spinbox.value()/scale)
        self.DDS1_freq_step_size.setText(str(float(self.DDS1_freq_step_size.text())/scale))
        
        self.DDS1_prev_freq_unit_index = DDS1_new_freq_unit_index
    
    def DDS1_freq_step_size_changed(self):
        self.DDS1_freq_spinbox.setSingleStep(float(self.DDS1_freq_step_size.text()))
    

    def DDS1_new_Vpp_stepBy(self, steps):
        self.DDS1_old_Vpp_stepBy(steps)
        self.DDS1_Vpp_updated()
        
    def DDS1_Vpp_editing_finished(self):
        self.DDS1_Vpp_updated()

    def DDS1_Vpp_updated(self):
        #print('Vpp', self.DDS1_Vpp_spinbox.value())
        
        Vamp=self.DDS1_Vpp_spinbox.value()/2
        mW=10*Vamp**2
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.DDS1_mW_spinbox.setValue(mW)
        self.DDS1_dBm_spinbox.setValue(dBm)
        
        if self.DDS1_auto_power_apply_checkbox.isChecked():
            self.DDS1_apply_power()

    def DDS1_Vpp_step_size_changed(self):
        self.DDS1_Vpp_spinbox.setSingleStep(float(self.DDS1_Vpp_step_size.text()))



    def DDS1_new_mW_stepBy(self, steps):
        self.DDS1_old_mW_stepBy(steps)
        self.DDS1_mW_updated()
        
    def DDS1_mW_editing_finished(self):
        self.DDS1_mW_updated()

    def DDS1_mW_updated(self):
        #print('mW', self.DDS1_mW_spinbox.value())

        mW = self.DDS1_mW_spinbox.value()
        Vamp = math.sqrt(mW/10)
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.DDS1_Vpp_spinbox.setValue(2*Vamp)
        self.DDS1_dBm_spinbox.setValue(dBm)
        
        if self.DDS1_auto_power_apply_checkbox.isChecked():
            self.DDS1_apply_power()

    def DDS1_mW_step_size_changed(self):
        self.DDS1_mW_spinbox.setSingleStep(float(self.DDS1_mW_step_size.text()))


    def DDS1_set_power_mW(self, mW):
        self.DDS1_mW_spinbox.setValue(mW)
        Vamp = math.sqrt(mW/10)
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.DDS1_Vpp_spinbox.setValue(2*Vamp)
        self.DDS1_dBm_spinbox.setValue(dBm)
        
        self.DDS1_apply_power()
        
        
    def DDS1_set_freq_Hz(self, Hz):
        DDS1_freq_unit_index = self.DDS1_freq_unit.currentIndex()
        scale = 10**(3*DDS1_freq_unit_index)
        
        self.DDS1_freq_spinbox.setValue(Hz/scale)
        self.DDS1_apply_freq()


    def DDS1_new_dBm_stepBy(self, steps):
        self.DDS1_old_dBm_stepBy(steps)
        self.DDS1_dBm_updated()
        
    def DDS1_dBm_editing_finished(self):
        self.DDS1_dBm_updated()

    def DDS1_dBm_updated(self):
        #print('dBm', self.DDS1_dBm_spinbox.value())

        dBm = self.DDS1_dBm_spinbox.value()
        mW = 10**(dBm/10)
        Vamp = math.sqrt(mW/10)
        self.DDS1_mW_spinbox.setValue(mW)
        self.DDS1_Vpp_spinbox.setValue(2*Vamp)
        
        if self.DDS1_auto_power_apply_checkbox.isChecked():
            self.DDS1_apply_power()

    def DDS1_dBm_step_size_changed(self):
        self.DDS1_dBm_spinbox.setSingleStep(float(self.DDS1_dBm_step_size.text()))

        
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    dds_dac = DDS_DAC()
    dds_dac.show()
    app.exec_()
    #sys.exit(app.exec_())

