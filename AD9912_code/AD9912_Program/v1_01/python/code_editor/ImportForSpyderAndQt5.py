# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 09:57:10 2017

@author: IonTrap
"""

"""
The following code is monkeypatch to fix "No error message of Qt inside 
IPython while GUI event loop is enabled by %gui qt5".
"""
from PyQt5 import QtCore
import sys
from traceback import format_exception
def new_except_hook(etype, evalue, tb):
    print(''.join(format_exception(etype, evalue, tb)))
def patch_excepthook():
    sys.excepthook = new_except_hook
TIMER = QtCore.QTimer()
TIMER.setSingleShot(True)
TIMER.timeout.connect(patch_excepthook)
TIMER.start()
"""
End of monkeypatch. IPython replaces sys.excepthook every time you execute 
a line of code, so the excepthook should be replaced only during execution.
This block should be removed once this issue is fixed.
"""

