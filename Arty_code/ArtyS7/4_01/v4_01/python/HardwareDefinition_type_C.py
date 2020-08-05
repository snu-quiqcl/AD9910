# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 07:59:12 2018

@author: 1109282

According to the given mapping, we will add alias for each pin
"""

from HardwareDefinition_v4_01 import *

# Input port pin mapping
# For input pin, there will be only one driver
input_mapping = {'jb_2': 'PMT1', 'jb_0': 'PMT2', 'ja_2': 'pulse_trigger'}

# Output port pin mapping
# For output pin, there might be more than one device controlled by the output pin
output_mapping = {'C1_AOM_on' : 'jb_1', \
                  'C1_AOM_switch' : 'jb_3', \
                  'C1_EOM_2_1GHz' : 'ja_7', \                  
                  'C1_EOM_7_37GHz' : 'ja_0', \
                  'C1_Microwave_SW': 'jb_5', \
                  'single_shot': 'jb_7', \
                  \
                  'C2_AOM_200MHz' : 'ja_3', \
                  'C2_EOM_7_37GHz' : 'ja_1', \
                  'C2_EOM_2_1GHz'  : 'ja_4', \
                  'C2_AOM_210MHz'  : 'ja_5', \
                  'C2_Microwave_SW': 'ja_6', \
                  }


# Output port configuration
C1_phase_shifter_port = 2
C2_phase_shifter_port = 3




var_dict = globals()
var_list = list(var_dict.keys())

for each_var in var_list:
    for (pin_name, mapping_name) in input_mapping.items():
        pin_name += '_'
        mapping_name += '_'
        index_found = each_var.find(pin_name)
        if index_found == -1:
            continue
        if index_found != 0:
            print('There is a variable (%s) whose name contains %s in the middle' \
                  % (each_var, pin_name))
            continue
        new_var_name = mapping_name + each_var[len(pin_name):]
        var_dict[new_var_name] = var_dict[each_var]

    for (mapping_name, pin_name) in output_mapping.items():
        pin_name += '_'
        mapping_name += '_'
        index_found = each_var.find(pin_name)
        if index_found == -1:
            continue
        if index_found != 0:
            print('There is a variable (%s) whose name contains %s in the middle' \
                  % (each_var, pin_name))
            continue
        new_var_name = mapping_name + each_var[len(pin_name):]
        var_dict[new_var_name] = var_dict[each_var]
    
    
    