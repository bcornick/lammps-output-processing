#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:47:08 2017

@author: brettcornick
"""

"""This script is designed to find how the position of a grain boundary changes
when shear stress is applied"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from operator import itemgetter
import glob

def read_chkpt(input_file):
    """this function takes a chkpt file and returns an array. each row is an atom. 
    first column is z position of the atom, second is c_eng of the atom"""
    with open(input_file, 'r') as infile:
        read_data = infile.readlines()
        line_index = [line_number for line_number, line in enumerate(read_data) if line.startswith('ITEM: ATOMS')][0] #makes a 1 element list and calls that element
        z_eng_list = []
        for in_index in range(line_index + 1, len(read_data)):
            z_pos = float(read_data[in_index].split()[5])
            c_eng = float(read_data[in_index].split()[11])
            z_eng_list.append([z_pos, c_eng])
        z_eng_array = np.array(sorted(z_eng_list, key=itemgetter(0)))
        return z_eng_array

def find_smooth(zs_and_engs):
    """this function takes an array of z and eng and smooths the line of z vs energy by finding rolling mean."""
    smooth_mean = pd.rolling_mean(zs_and_engs, 1000)
    middle = np.concatenate((np.array_split(smooth_mean, 5, axis=0)[1], np.array_split(smooth_mean, 5, axis=0)[2],np.array_split(smooth_mean, 5, axis=0)[3]), axis=0)
    return middle
    
def find_max(middle_smooth):
    """this function finds the z position of the max of the smoothed average line to find the z location of the grain boundary."""
    max_index = np.argmax(middle_smooth, axis=0)[1]
    max_position = middle_smooth[max_index]
    return max_position[0]

file_list = glob.glob('*'+'.chkpt')
#file_list = glob.glob('/Users/brettcornick/LAMMPS/simulations/coupling/Cu_highT/pbatch_run/out/*.chkpt') #change to directory with output files
z_list = []
count = 0
count_list = []
time_list = []
templ = '.chkpt'
for file in file_list:
    array_from_file = read_chkpt(file)
    smoothed_array = find_smooth(array_from_file)
    z_of_max = find_max(smoothed_array)
    z_list.append(z_of_max)
    count_list.append(count)
    count += 1
    time = int(file[:len(file)-len(templ)])
    time_list.append(time)

plt.figure(1)
plt.subplot(211)
plt.plot(array_from_file[:,0],array_from_file[:,1], 'b.')
plt.plot(smoothed_array[:,0],smoothed_array[:,1], 'r-')
plt.subplot(212)
plt.plot(time_list, z_list, 'g.')
plt.show(1)                    
