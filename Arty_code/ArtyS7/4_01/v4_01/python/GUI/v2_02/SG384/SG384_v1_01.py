# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 00:10:48 2018

@author: 1109282

* Change log
v1_00: Initial working version
v1_01: Optimized assuming that SG384Control panel will be called by another program

"""
# from http://wiki.python.org/moin/TcpCommunication
# About SCPI over TCP: page 12 from ftp://ftp.datx.com/Public/DataAcq/MeasurementInstruments/Manuals/SCPI_Measurement.pdf

from __future__ import unicode_literals
import os, sys
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

new_path_list = []
new_path_list.append(dirname + '\\..') # For ImportForSpyderAndQt5
new_path_list.append(dirname + '\\..\\ui_resources') # For resources_rc.py
# More paths can be added here...
for each_path in new_path_list:
    if not (each_path in sys.path):
        sys.path.append(each_path)

import ImportForSpyderAndQt5

from PyQt5 import uic
qt_designer_file = dirname + '\\SG384UI_v1_00.ui'
Ui_QDialog, QtBaseClass = uic.loadUiType(qt_designer_file)
ICON_RED_LED = ":/icons/led-red-on.png"
ICON_GREEN_LED = ":/icons/green-led-on.png"

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

import math
import socket

class SG384Control(QtWidgets.QDialog, Ui_QDialog):
    
    def __init__(self, parent=None, connection_callback=None):
        QtWidgets.QDialog.__init__(self, parent)
        #self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        
        self.old_Vpp_stepBy = self.Vpp_spinbox.stepBy
        self.Vpp_spinbox.stepBy = self.new_Vpp_stepBy

        self.old_mW_stepBy = self.mW_spinbox.stepBy
        self.mW_spinbox.stepBy = self.new_mW_stepBy

        self.old_dBm_stepBy = self.dBm_spinbox.stepBy
        self.dBm_spinbox.stepBy = self.new_dBm_stepBy

        self.old_freq_stepBy = self.freq_spinbox.stepBy
        self.freq_spinbox.stepBy = self.new_freq_stepBy
        self.prev_freq_unit_index = self.freq_unit.currentIndex()
        
        self.connected = False
        self.connection_callback = connection_callback
        
        self.red_icon = QtGui.QPixmap(ICON_RED_LED)
        self.green_icon = QtGui.QPixmap(ICON_GREEN_LED)
        self.frame.setEnabled(False)


    def query(self, message):
        self.socket.send((message + '\n').encode('latin-1'))
        data = self.socket.recv(1024)
        return data.decode('latin-1')[:-1] # Removing the trailing '\n'

    
    def write(self, message):
        self.socket.send((message + '\n').encode('latin-1'))

    
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

            

    def connect(self):
        if self.connected:
            self.socket.close() 
            self.IDN_label.setText('')
            
            self.connection_status.setText('Disconnected')
            self.connect_button.setText('Connect')
            self.frame.setEnabled(False)
            self.connected = False
            if self.connection_callback != None:
                self.connection_callback(False)

            
        else:
            self.TCP_IP = self.IP_address.text()
            self.TCP_PORT = int(self.port.text())
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.TCP_IP, self.TCP_PORT))
            self.socket.settimeout(1) # unit in second?

            self.IDN_label.setText(self.query('*IDN?'))

            if self.query('ENBR?')[0] == '0':
                #self.output_status.setText('Off')
                self.output_status.setPixmap(self.red_icon)
                self.output_button.setText('Turn on')
                self.output_on = False
            else:
                #self.output_status.setText('On')
                self.output_status.setPixmap(self.green_icon)
                self.output_button.setText('Turn off')
                self.output_on = True
                
            self.read_power()
            self.read_freq()
            
            self.connection_status.setText('Connected')
            self.connect_button.setText('Disconnect')
            self.frame.setEnabled(True)
            self.connected = True
            if self.connection_callback != None:
                self.connection_callback(True)
            
            
    def read_power(self):
        dBm = float(self.query('AMPR?'))
        self.dBm_spinbox.setValue(dBm)
        mW = 10**(dBm/10)
        Vamp = math.sqrt(mW/10)
        self.mW_spinbox.setValue(mW)
        self.Vpp_spinbox.setValue(2*Vamp)

        
    
    def apply_power(self):
        dBm = self.dBm_spinbox.value()
        self.write('AMPR %.2f' % dBm)
    
    def read_freq(self):
        unit = self.freq_unit.currentText()
        query = 'FREQ? %s' % unit
        #print(query)
        freq = float(self.query(query))
        self.freq_spinbox.setValue(freq)

    
    def apply_freq(self):
        unit = self.freq_unit.currentText()
        query = 'FREQ %f %s' % (self.freq_spinbox.value(), unit) 
        #print(query)
        self.write(query)
        

    def output_on_off(self):
        if self.output_on:
            self.write('ENBR 0')
            #self.output_status.setText('Off')
            #self.output_status.setPixmap(QtGui.QPixmap(ICON_RED_LED))
            self.output_status.setPixmap(self.red_icon)
            self.output_button.setText('Turn on')
            self.output_on = False
        else:
            self.write('ENBR 1')
            #self.output_status.setPixmap(QtGui.QPixmap(ICON_GREEN_LED))
            self.output_status.setPixmap(self.green_icon)
            self.output_button.setText('Turn off')
            self.output_on = True
            
    
    def new_freq_stepBy(self, steps):
        self.old_freq_stepBy(steps)
        self.freq_updated()

    def freq_editing_finished(self):
        self.freq_updated()

    def freq_updated(self):
        #print('Freq', self.freq_spinbox.value())
        if self.auto_freq_apply_checkbox.isChecked():
            self.apply_freq()

    
    def freq_unit_changed(self, index):
        #print('freq_unit_changed', self.freq_unit.currentIndex())
        new_freq_unit_index = self.freq_unit.currentIndex()
        scale = 10**(3*(new_freq_unit_index - self.prev_freq_unit_index))
        
        self.freq_spinbox.setValue(self.freq_spinbox.value()/scale)
        self.freq_step_size.setText(str(float(self.freq_step_size.text())/scale))
        
        self.prev_freq_unit_index = new_freq_unit_index
    
    def freq_step_size_changed(self):
        self.freq_spinbox.setSingleStep(float(self.freq_step_size.text()))
    

    def new_Vpp_stepBy(self, steps):
        self.old_Vpp_stepBy(steps)
        self.Vpp_updated()
        
    def Vpp_editing_finished(self):
        self.Vpp_updated()

    def Vpp_updated(self):
        #print('Vpp', self.Vpp_spinbox.value())
        
        Vamp=self.Vpp_spinbox.value()/2
        mW=10*Vamp**2
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.mW_spinbox.setValue(mW)
        self.dBm_spinbox.setValue(dBm)
        
        if self.auto_power_apply_checkbox.isChecked():
            self.apply_power()

    def Vpp_step_size_changed(self):
        self.Vpp_spinbox.setSingleStep(float(self.Vpp_step_size.text()))



    def new_mW_stepBy(self, steps):
        self.old_mW_stepBy(steps)
        self.mW_updated()
        
    def mW_editing_finished(self):
        self.mW_updated()

    def mW_updated(self):
        #print('mW', self.mW_spinbox.value())

        mW = self.mW_spinbox.value()
        Vamp = math.sqrt(mW/10)
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.Vpp_spinbox.setValue(2*Vamp)
        self.dBm_spinbox.setValue(dBm)
        
        if self.auto_power_apply_checkbox.isChecked():
            self.apply_power()

    def mW_step_size_changed(self):
        self.mW_spinbox.setSingleStep(float(self.mW_step_size.text()))


    def set_power_mW(self, mW):
        self.mW_spinbox.setValue(mW)
        Vamp = math.sqrt(mW/10)
        if mW > 0:
            dBm = 10*math.log10(mW)
        else:
            dBm = -1000
        self.Vpp_spinbox.setValue(2*Vamp)
        self.dBm_spinbox.setValue(dBm)
        
        self.apply_power()
        
        
    def set_freq_Hz(self, Hz):
        freq_unit_index = self.freq_unit.currentIndex()
        scale = 10**(3*freq_unit_index)
        
        self.freq_spinbox.setValue(Hz/scale)
        self.apply_freq()


    def new_dBm_stepBy(self, steps):
        self.old_dBm_stepBy(steps)
        self.dBm_updated()
        
    def dBm_editing_finished(self):
        self.dBm_updated()

    def dBm_updated(self):
        #print('dBm', self.dBm_spinbox.value())

        dBm = self.dBm_spinbox.value()
        mW = 10**(dBm/10)
        Vamp = math.sqrt(mW/10)
        self.mW_spinbox.setValue(mW)
        self.Vpp_spinbox.setValue(2*Vamp)
        
        if self.auto_power_apply_checkbox.isChecked():
            self.apply_power()

    def dBm_step_size_changed(self):
        self.dBm_spinbox.setSingleStep(float(self.dBm_step_size.text()))

        
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    sg384 = SG384Control()
    sg384.show()
    app.exec_()
    #sys.exit(app.exec_())

