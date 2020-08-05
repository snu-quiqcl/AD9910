# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 10:32:44 2018

@author: 1109282

* Count the number of rising edge of the RF signal during fixed time

"""

import os
import sys
import numpy as np
import math
import csv


os.getcwd()
filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)
#user_directory = 'Q:\\Users\\JHJeong\\data\\PMT\\'
user_directory = 'C:\\Users\\WaterBear29\\desktop\\'

from PyQt5 import uic
qt_designer_file = dirname + '\\PMT_count.ui'
Ui_Form, QtBaseClass = uic.loadUiType(qt_designer_file)

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap, QIcon, QColor, QCursor, QPainter, QPen
from PyQt5.QtWidgets import QMessageBox, QLabel, QApplication, QWidget, QInputDialog, QFileDialog
from PyQt5.QtCore import QCoreApplication, Qt

import ex13_counter.py

class PMT_Stepper(QtWidgets.QWidget, Ui_Form):

    def __init__(self, instance_name, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.instance_name = instance_name
        self.save_path = user_directory
        
        self.Data_x = []
        self.Data_y = []
        self.Data_value = 0
        
        self.Reposition()
        
        
    def Reposition(self):
        self.xy_min = int(self.TextBox_xy_min.text())
        self.xy_MAX = int(self.TextBox_xy_MAX.text())
        
        # z values
        self.z_min = int(self.TextBox_z_min.text())
        self.z_MAX = int(self.TextBox_z_MAX.text())
        
        # Position
        self.x_point = int(self.TextBox_X.text())
        self.y_point = int(self.TextBox_Y.text())
        self.z_point = int(self.TextBox_Z.text())
        
        # Step
        self.x_step = int(self.TextBox_X_step.text())
        self.y_step = int(self.TextBox_Y_step.text())
        self.z_step = int(self.TextBox_Z_step.text())
        
        self.xy_min_real = self.xy_min * self.x_step
        self.xy_MAX_real = self.xy_MAX * self.x_step
        self.z_min_real = self.z_min * self.z_step
        self.z_MAX_real = self.z_MAX * self.z_step
        
        # Set textbox
        self.xy_min_real_TXT.setText(str(self.xy_min_real))
        self.xy_MAX_real_TXT.setText(str(self.xy_MAX_real))
        
        self.z_min_real_TXT.setText(str(self.z_min_real))
        self.z_MAX_real_TXT.setText(str(self.z_MAX_real))
        

    def MM_Edit(self):
        self.Reposition()

    def x_Change(self):
        
        val_in = self.sender().value()
        if (val_in != 0):
            if (val_in < 0):
                Min_flag = 1
            else:
                Min_flag = -1
            # Changing the value       
         
            new_val = self.x_point + self.x_step * Min_flag
            self.TextBox_X.setText(str(int(new_val)))
            self.ScrollBar_X.setValue(0)
            
            self.Reposition()
        else: 
            pass
    
    def y_Change(self):
        val_in = self.sender().value()
        if (val_in != 0):
            if (val_in < 0):
                Min_flag = 1
            else:
                Min_flag = -1
            # Changing the value            
            new_val = self.y_point + self.y_step * Min_flag
            self.TextBox_Y.setText(str(int(new_val)))
    
            self.ScrollBar_Y.setValue(0)
            
            self.Reposition()
        else: 
            pass
    
    def z_Change(self):
        val_in = self.sender().value()
        if (val_in != 0):
            if (val_in < 0):
                Min_flag = 1
            else:
                Min_flag = -1
            # Changing the value            
            new_val = self.z_point + self.z_step * Min_flag
            self.TextBox_Z.setText(str(int(new_val)))
    
            self.ScrollBar_Z.setValue(0)
            
            self.Reposition()
        else: 
            pass

    def SettoMin(self):
        X_val = self.xy_min * self.x_step
        Y_val = self.xy_min * self.y_step
        Z_val = self.z_min * self.z_step
        
        
        self.TextBox_X.setText(str(X_val))
        self.TextBox_Y.setText(str(Y_val))
        self.TextBox_Z.setText(str(Z_val))
        
        self.Reposition()
    
    def SettoMax(self):
        X_val = self.xy_MAX * self.x_step
        Y_val = self.xy_MAX * self.y_step
        Z_val = self.z_MAX * self.z_step
        
        
        self.TextBox_X.setText(str(X_val))
        self.TextBox_Y.setText(str(Y_val))
        self.TextBox_Z.setText(str(Z_val))
        
        self.Reposition()
    
    def SaveData(self):
        pass
    
    def ReadValue(self):
        pass
    
    def NextStep(self):
        self.ReadValue()
        
        # X = Y = Max
        if (self.y_point >= self.xy_MAX * self.y_step):
            if (self.x_point >= self.xy_MAX * self.x_step):
                self.Data_x.append(self.Data_value)
                self.Data_y.append(self.Data_x)
                
                self.Data_x = []
                
                #Saving
                with open (self.save_path + 'z_' + str(self.z_point) + '.csv', 'w', newline='') as ll:
                    writer = csv.writer(ll)
                    
                    for i in range(len(self.Data_y)):
                        writer.writerow(self.Data_y[i])
                
                if (self.z_point >= self.z_MAX * self.z_step):
                    self.Acq_value.setText('Scan Finished!')
                    
                else:
                    self.TextBox_X.setText(str(self.xy_min * self.x_step))
                    self.TextBox_Y.setText(str(self.xy_min * self.y_step))
                    self.TextBox_Z.setText(str(self.z_point + self.z_step))
                    
                    self.Data_y = []
                        
                
            else:
                self.Data_x.append(self.Data_value)
                self.TextBox_X.setText(str(self.x_point + self.x_step))
        

        # Y != MAX      
        else:
            if (self.x_point >= self.xy_MAX * self.x_step):
                self.Data_x.append(self.Data_value)
                self.Data_y.append(self.Data_x)
                
                self.Data_x = []
                
                
                self.TextBox_X.setText(str(self.xy_min * self.x_step))
                self.TextBox_Y.setText(str(self.y_point + self.y_step))
                
            else:
                self.Data_x.append(self.Data_value)
                self.TextBox_X.setText(str(self.x_point + self.x_step))
                    
        # z = MAX    
        self.Reposition()
    
        
    def main(self):
        pass
        



if __name__ == '__main__':

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    PMT_ST = PMT_Stepper(instance_name = 'PMT_auto_stepper')
    PMT_ST.show()
    


    app.exec_()
