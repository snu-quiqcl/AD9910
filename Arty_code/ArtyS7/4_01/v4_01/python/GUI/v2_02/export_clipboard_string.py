# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 16:18:27 2018

@author: iontrap
"""

import time
import clipboard

def send_clipboard():
    clipboard.copy("Matlab_turn")

    while clipboard.paste() != "Python_turn" :
        time.sleep(2.0)
   #print('.')
   