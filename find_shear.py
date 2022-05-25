#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 16:52:25 2018

@author: brettcornick
"""

import numpy as np
from operator import itemgetter

def read_shear(shear_input):
    """reads shear input file in order to make plot of shear stress vs time"""
    with open(shear_input, 'r') as shear_file:
        shear_data = shear_file.readlines()
        line_index = [n for n, l in enumerate(shear_data) if not l.startswith('#')][0]
        shear_list = []
        for i in range(line_index, len(shear_data)):
            t_step = float(shear_data[i].split()[0])
            #sxz = float(shear_data[i].split()[1]) #shear_coup
            #natoms = float(shear_data[i].split()[2]) #shear_coup
            #shear_list.append([t_step, sxz, natoms]) #shear_coup
            stress = float(shear_data[i].split()[1]) #shear-tf
            sxx2 = float(shear_data[i].split()[2]) #shear-tf
            syy2 = float(shear_data[i].split()[3]) #shear-tf
            szz2 = float(shear_data[i].split()[4]) #shear-tf
            sxy2 = float(shear_data[i].split()[5]) #shear-tf
            sxz2 = float(shear_data[i].split()[6]) #shear-tf
            syz2 = float(shear_data[i].split()[7]) #shear-tf
            shear_list.append([t_step, stress, sxx2, syy2, szz2, sxy2, sxz2, syz2]) #shear-tf
        shear_array = np.array(sorted(shear_list, key=itemgetter(0)))
        return shear_array

x = read_shear('/Shear_0K.txt')
shear_max = min(list(x[:,7])) #6 is xz, 7 is yz, 4 is zz
print(shear_max)