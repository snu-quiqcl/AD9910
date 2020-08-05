# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 14:13:26 2018

@author: IonTrap
"""
def make_bit_pattern_from_15_to_0(list_of_bit_position_and_value):
    mask_pattern = 16*[0]
    bit_pattern = 16*[0]
    for each_bit in list_of_bit_position_and_value:
        index = 15-each_bit[0]
        if mask_pattern[index] != 0:
            err_msg = ('Error in make_bit_pattern_from_15_to_0: same ' \
                       + 'location (%d) is specified multiple times.') % index
            raise KeyError(err_msg)
        mask_pattern[index] = 1
        bit_pattern[index] = each_bit[1]
    mask_pattern_value = bit_list_to_int(mask_pattern)
    bit_pattern_value = bit_list_to_int(bit_pattern)
    return (bit_pattern_value, mask_pattern_value)


def make_bit_pattern_from_position_list_from_15_to_0(list_of_bit_position):
    mask_pattern = 16*[0]
    for each_bit in list_of_bit_position:
        index = 15-each_bit
        if mask_pattern[index] != 0:
            err_msg = ('Error in make_bit_pattern_from_position_list_from_15_to_0: same ' \
                       + 'location (%d) is specified multiple times.') % index
            raise KeyError(err_msg)
        mask_pattern[index] = 1
    mask_pattern_value = bit_list_to_int(mask_pattern)
    return mask_pattern_value


#def make_bit_pattern_from_position_list_from_15_to_0(list_of_bit_position):
#    total = 0
#    for each_bit in list_of_bit_position:
#        total += 1 << each_bit
#    return total


def make_bit_pattern_from_1_to_16(list_of_bit_position_and_value):
    mask_pattern = 16*[0]
    bit_pattern = 16*[0]
    for each_bit in list_of_bit_position_and_value:
        mask_pattern[each_bit[0]-1] = 1
        bit_pattern[each_bit[0]-1] = each_bit[1]
    mask_pattern_value = bit_list_to_int(mask_pattern)
    bit_pattern_value = bit_list_to_int(bit_pattern)
    return (bit_pattern_value, mask_pattern_value)

        
 
def bit_list_to_int(bit_list):
    value = 0
    for bit in bit_list:
        value = (value << 1) | bit
    return value

def bit_string(value):
    return bit_string_n_l(value, 4, 4)

def bit_string_n_l(value, n, l):
    divider = 1<<l;
    bit_string_list = []
    for m in range(n):
        bit_string_list.append(format(value%divider, ('0%db' % l)))
        value = value // divider
    bit_string_list.reverse()
    bit_string = ''
    for m in bit_string_list:
        bit_string += m + ' '
    return bit_string

def show_16bits(value):
    four_bits_list = []
    for n in range(4):
        four_MSBs = value % 16
        value = value // 16
        four_bits_list.append(four_MSBs)
    if value > 0:
        print('Larger than 16 bits:', value)
    bit_string = ''
    for n in range(4):
        bit_string = format(four_bits_list[n], ' 05b') + bit_string
    return bit_string

        
    
    print(format(value//256, '08b'), format(value%256, '08b'))

