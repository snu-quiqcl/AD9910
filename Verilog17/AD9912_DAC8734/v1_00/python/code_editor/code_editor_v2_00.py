# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 17:16:46 2018

Change log
v1_00: Initial version
v1_01: Check if the file is changed by another program whenever the mouse comes
    over the window and convert tab to spaces
    Text highlighting for python
v1_02: Whenever the return key is pressed, it checks the leading whitespaces of 
    the previous lines and copy them. If the previous line is ended with ':',
    then it will add indentation. Status bar will show the current cursor position.
"""

import sys
import os

import ImportForSpyderAndQt5

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

from . import syntax_highlighter

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QInputDialog

from PyQt5 import uic
qt_designer_file = dirname + '\\code_editorUI_v1_02.ui'

Ui_QMainWindow, QtBaseClass = uic.loadUiType(qt_designer_file)

class TextEditor(QtWidgets.QMainWindow, Ui_QMainWindow):
    def __init__(self, window_title = 'Source editor', parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.highlight = syntax_highlighter.PythonHighlighter(self.plainTextEdit.document())
        
        self.window_title = window_title
        self.setWindowTitle(self.window_title)

        self.current_filename = ''
        self.text_edited = False
        self.modified_time = 0
        self.tab_size = 4

        self.old_keyPressEvent = self.plainTextEdit.keyPressEvent
        self.plainTextEdit.keyPressEvent = self.new_keyPressEvent
        self.statusbar.showMessage('Line: 1, Col: 1')
        
        
    def cursor_position_changed(self):
        cursor = self.plainTextEdit.textCursor()
        block = cursor.block()
        #print(block.blockNumber(), cursor.positionInBlock())
        self.statusbar.showMessage('Line: %d, Col: %d' % \
            (block.blockNumber()+1, cursor.positionInBlock()+1))
        
    def change_tab_size(self):
        new_tab_size, ok = QInputDialog.getInt(self, 'Change tab size', 
            'Tab size:', value = self.tab_size, min = 1, max = 16)
        if ok:
            self.tab_size = new_tab_size
        
    def enterEvent(self, event):
        if self.current_filename != '':
            if self.modified_time < os.path.getmtime(self.current_filename):
                if self.text_edited:
                    additional_comment = 'If you reload it, the current changes will be lost.\n'
                else:
                    additional_comment = ''
                
                buttonReply = QMessageBox.question(self, 'Reload', \
                    self.current_filename + '\n\n' \
                    + 'This file has been modified by another program.\n' \
                    + additional_comment + "Do you want to reload it?", \
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if buttonReply == QMessageBox.Yes:
                    with open(self.current_filename, 'r') as f:
                        data = f.read()
                        self.plainTextEdit.setPlainText(data)
                    self.setWindowTitle(self.window_title + ' - ' + self.current_filename)
                    self.text_edited = False
                    
                self.modified_time = os.path.getmtime(self.current_filename)
                


        
    def new_keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            #cursor = self.plainTextEdit.textCursor()
            #cursor.insertText(4*' ')
            #self.plainTextEdit.setTextCursor(cursor)
            self.plainTextEdit.insertPlainText(self.tab_size * ' ')
            event.accept()
        elif event.key() == QtCore.Qt.Key_Return:
            self.old_keyPressEvent(event)
            cursor = self.plainTextEdit.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Up)
            """
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            # I didn't use LineUnderCursor because when the line is wrapped, 
            # it is split as shown visual. So to get the entire line, 
            # I need to get block. However getting block generally include 
            # paragraph separator at the beginning unless it is the first block.
            upper_block = cursor.selectedText()
            if upper_block[0] == '\u2029': # Unicode paragraph separator
                upper_block = upper_block[1:]
            """
            upper_block = cursor.block().text()
            whitespace_count = 0
            for n in range(len(upper_block)):
                if upper_block[n] == ' ':
                    whitespace_count += 1
                else:
                    break
            if (len(upper_block) > 0) and (upper_block[-1] == ':'):
                whitespace_count += self.tab_size
            self.plainTextEdit.insertPlainText(whitespace_count * ' ')
            #print('current_line:', ord(upper_block[0]), upper_block, len(upper_block))
            #print('white spaces:', whitespace_count)
        else:
            return self.old_keyPressEvent(event)
        
    
    def new_document(self):
        self.close_document()
        
    def open_document_by_external(self, filename):
        if self.text_edited:
            if not self.close_document():
                return

        with open(filename, 'r') as f:
            data = f.read()
            self.plainTextEdit.setPlainText(data)

        self.current_filename = filename
        self.text_edited = False
        self.modified_time = os.path.getmtime(self.current_filename)
        self.setWindowTitle(self.window_title + ' - ' + self.current_filename)

    def open_document(self):
        if self.text_edited:
            if not self.close_document():
                return

        if self.current_filename == '':
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', filter = 'python sources (*.py);;All Files (*)')
        else:
            fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', directory =self.current_filename, filter = 'python sources (*.py);;All Files (*)')

        
        
        if fname[0]:
            with open(fname[0], 'r') as f:
                data = f.read()
                self.plainTextEdit.setPlainText(data)

            self.current_filename = fname[0]
            self.text_edited = False
            self.modified_time = os.path.getmtime(self.current_filename)
            self.setWindowTitle(self.window_title + ' - ' + self.current_filename)

    
    def save(self):
        if self.current_filename == '':
            return self.saveAs()
        else:
            with open(self.current_filename, 'w') as f:
                    f.write(self.plainTextEdit.toPlainText())
            self.setWindowTitle(self.window_title + ' - ' + self.current_filename)
            self.plainTextEdit.document().setModified(False)
            self.text_edited = False
            self.modified_time = os.path.getmtime(self.current_filename)
            return True


    def text_changed(self):
        modified = self.plainTextEdit.document().isModified()
        if modified and (not self.text_edited):
            self.text_edited = True
            self.setWindowTitle(self.window_title + ' - ' + self.current_filename+'*')

        if (not modified) and self.text_edited:
            self.text_edited = False
            self.setWindowTitle(self.window_title + ' - ' + self.current_filename)
        
    
    def saveAs(self):
        if self.current_filename == '':
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file as', filter = 'python sources (*.py);;All Files (*)')
        else:
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file as',directory =self.current_filename, filter = 'python sources (*.py);;All Files (*)')
        
        if fname[0]:
            with open(fname[0], 'w') as f:
                    f.write(self.plainTextEdit.toPlainText())
            self.current_filename = fname[0]
            self.setWindowTitle(self.window_title + ' - ' + self.current_filename)
            self.plainTextEdit.document().setModified(False)
            self.text_edited = False
            self.modified_time = os.path.getmtime(self.current_filename)
            return True
        else:
            return False
        
    
    def close_document(self):
        if self.text_edited:
            buttonReply = QMessageBox.question(self, 'The code is modified', \
                "Do you want to save the changes?", 
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                if self.save():
                    self.plainTextEdit.setPlainText('')
                    self.text_edited = False
                    self.current_filename = ''
                    self.setWindowTitle(self.window_title)
                    return True
                else:
                    return False
            elif buttonReply == QMessageBox.No:
                self.plainTextEdit.setPlainText('')
                self.text_edited = False
                self.current_filename = ''
                self.setWindowTitle(self.window_title)
                return True
            else:
                return False
        else:
            self.plainTextEdit.setPlainText('')
            self.text_edited = False
            self.current_filename = ''
            self.setWindowTitle(self.window_title)
            return True
            
                
    def closeEvent(self, event):
        if self.text_edited:
            if not self.close_document():
                event.ignore()
                return
        QtWidgets.QMainWindow.closeEvent(self, event)

    
    def quit(self):
        QtWidgets.QMainWindow.close(self)


    def undo(self):
        self.plainTextEdit.document().undo()

        
    def redo(self):
        self.plainTextEdit.document().redo()

        
    def change_font(self):
        font, ok = QtWidgets.QFontDialog.getFont(self.plainTextEdit.font(), self)
        if ok:
            self.plainTextEdit.setFont(font)
   
    def word_wrapping(self, status):
        if status:
            self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        else:
            self.plainTextEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
            
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    
    te = TextEditor()
    te.show()
    app.exec_()
    #sys.exit(app.exec_())

