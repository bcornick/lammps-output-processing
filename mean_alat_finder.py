#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 14:48:08 2017

@author: brettcornick
"""

import numpy as np

with open('log.lammps', 'r') as f:
    line_list = []
    read_data = f.readlines()
    line_index = 0
    for lines in read_data:
        if line_index >= 119 and line_index <= 399: #start reading data from line n1 + 1 and stop after n2 + 1
            lx = float(lines.split()[1])
            temperature = float(lines.split()[3])
            press = float(lines.split()[8])
            line_list.append([lx,  temperature, press])
        line_index += 1
    log_array = np.array(line_list)
    log_means = np.mean(log_array, axis=0)
    
print('Mean alat = %.8f Angstroms' % (log_means[0]))