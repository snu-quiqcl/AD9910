# -*- coding: utf-8 -*-
"""
Created on Sun May 20 19:26:57 2018

@author: IonTrap

# Revision history
v1_00: initial version
v2_00: Find min/max power, min/max freq.
"""

import csv
import bisect

class power_table():
    def __init__(self, filename):
        """ Generate a structured list of power vs. voltage at different frequency
        
        Master list (freq_list) is composed of the following structure:

        freq_list = [
            [f1, power_keys_list1, [(p1, v1), (p2, v2),...(pN, vN)]],
            [f2, power_keys_list2, [(p1, v1), (p2, v2),...(pN, vN)]],  # p1, v1 @ f2 frequency is different from p1, v1 @ f1.
            [f3, power_keys_list2, [(p1, v1), (p2, v2),...(pN, vN)]],  # The length of (px, vx) list for f1 is different from the length of other frequencies
            :
            [fM, power_keys_listM, [(p1, v1), (p2, v2),...(pN, vN)]]
        ] # where f1, f2, .., fM are frequencies, px are powers, vx are corresponding voltages for certain frequency
            
        freq_keys = [f1, f2, ..., fM] # Sorted list of frequency data. Mainly used for quick binary search.
        
        """
        with open(filename) as csvfile:
            freq_power_data = csv.reader(csvfile, delimiter=',')
            freq = None
            self.freq_list = []
            for row in freq_power_data:
                if freq != float(row[0]): 
                    # New frequency data starts
                    if freq != None: 
                        # Add all the power:voltage list to the master list(freq_list)
                        power_list.sort(key=lambda r: r[0])
                        # Check if the relation between power and voltage is monotonic
                        prev = (power_list[0][0], power_list[0][1]-1) 
                        for each in power_list:
                            if prev[1] > each[1]:
                                print('Error in data(%d): previous value (%s)is larger than current value(%s)' % (freq, str(prev), str(each)))
                            prev = each
                        power_keys = [r[0] for r in power_list] # For quick search, make a sorted key list in advance
                        self.freq_list.append((freq, power_keys, power_list))
                    # Start a new power:voltage list
                    freq = float(row[0])
                    power_list=[]
                    
                power_list.append((float(row[3]), float(row[1])))

            # Don't forget to add the last power:voltage list to the master list(freq_list)
            power_list.sort(key=lambda r: r[0])
            prev = (power_list[0][0], power_list[0][1]-1)
            for each in power_list:
                if prev[1] > each[1]:
                    print('Error in data(%d): previous value (%s)is larger than current value(%s)' % (freq, str(prev), str(each)))
                prev = each
            power_keys = [r[0] for r in power_list]
            self.freq_list.append((freq, power_keys, power_list))
            
        # For quick search, make a sorted key of the master list (freq_list) in advance    
        self.freq_list.sort(key=lambda r: r[0])
        self.freq_keys = [r[0] for r in self.freq_list]
        
        self.min_freq = self.freq_keys[0]
        self.max_freq = self.freq_keys[-1]
        self.common_min_power = self.freq_list[0][1][0] # This will be the maximum of all the minimum power
        self.common_max_power = self.freq_list[0][1][-1] # This will be the minimum of all the maximum power
        for each_freq in self.freq_list:
            power_keys_list = each_freq[1]
            if self.common_min_power < power_keys_list[0]:
                self.common_min_power = power_keys_list[0]
            if self.common_max_power > power_keys_list[-1]:
                self.common_max_power = power_keys_list[-1]

    
    def search_index(self, keys, value):
        index = bisect.bisect_left(keys, value)
        if index == len(keys):
            return (index-1, index-1)
        elif keys[index] == value or index == 0:
            return (index, index)
        else:
            return (index-1, index)
    
    def determine_voltage(self, power_list, low_index, high_index, power):
        if (low_index == high_index):
            return power_list[low_index][1]
        dist_from_low = (power-power_list[low_index][0])/(power_list[high_index][0]-power_list[low_index][0])
        voltage = dist_from_low*(power_list[high_index][1]-power_list[low_index][1])+power_list[low_index][1]
        #print(dist_from_low, voltage)
        return voltage
        
        
    def voltage_for_freq_power(self, freq_in_MHz, power_in_dBm):
        if (freq_in_MHz < 10) or (freq_in_MHz > 100):
            print('Error in voltage_for_freq_power: frequency should be between 10 MHz and 100 MHz')
            raise ValueError()
        if (power_in_dBm < self.common_min_power) or (power_in_dBm > self.common_max_power):
            print('Error in voltage_for_freq_power: power should be between %.1f dBm and %.1f dBm' % (self.common_min_power, self.common_max_power))
            raise ValueError()
        (low_freq, high_freq) = self.search_index(self.freq_keys, freq_in_MHz)
        if low_freq == high_freq:
            power_list = self.freq_list[low_freq]
            power_indices = self.search_index(power_list[1], power_in_dBm)
            return self.determine_voltage(power_list[2], power_indices[0], power_indices[1], power_in_dBm)
        else:
            low_list = self.freq_list[low_freq]
            high_list = self.freq_list[high_freq]
            
            low_power_indices = self.search_index(low_list[1], power_in_dBm)
            high_power_indices = self.search_index(high_list[1], power_in_dBm)
            
            #print(low_list[0], str(low_list[2][low_power_indices[0]]), str(low_list[2][low_power_indices[1]]))
            #print(high_list[0], str(high_list[2][high_power_indices[0]]), str(high_list[2][high_power_indices[1]]))
            
            low_voltage = self.determine_voltage(low_list[2], low_power_indices[0], low_power_indices[1], power_in_dBm)
            high_voltage = self.determine_voltage(high_list[2], high_power_indices[0], high_power_indices[1], power_in_dBm)
            dist_from_low = (freq_in_MHz-self.freq_list[low_freq][0])/(self.freq_list[high_freq][0]-self.freq_list[low_freq][0])
            return dist_from_low*(high_voltage -low_voltage)+low_voltage

if __name__ == '__main__':
    #pt = power_table('calibration_DDS2_DAC0_HSTL_FB_connected_DDS_full_current_ZX73-2500-S+_180522.csv')
    pt = power_table('calibration_DDS1_DAC1_DDS_full_current_ZX73-2500-S+_180522.csv')

    print(pt.voltage_for_freq_power(30, -10))
    

