#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 11:11:03 2017

@author: brettcornick

This script is designed to track the movement of a certain group of atoms from
one time step to another. It will then colorize this group and display it's original
position and its final position.
"""

import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
#import glob
from operator import itemgetter

def read_chkpt(chkpt_file):
    with open(chkpt_file, 'r') as chkpt:
        chkpt_data = chkpt.readlines()
        i = [n for n, l in enumerate(chkpt_data) if l.startswith('ITEM: ATOMS')][0]
        id_x_z_list = []
        for line in range(i + 1, len(chkpt_data)):
            atom_id = float(chkpt_data[line].split()[0])
            x_pos = float(chkpt_data[line].split()[3])
            z_pos = float(chkpt_data[line].split()[5])
            id_x_z_list.append([atom_id, x_pos, z_pos])
        id_x_z_array = np.array(id_x_z_list)
        return (id_x_z_array, id_x_z_list)   
    
def x_based_select(input_array):
    ordered_array = sorted(input_array, key=itemgetter(1))
    left = np.array_split(ordered_array, 3, axis=0)[0]
    middle = np.array_split(ordered_array, 3, axis=0)[1] #for wider or narrower chunk, split into more sections and concatenate
    right = np.array_split(ordered_array, 3, axis=0)[2]
    last = np.concatenate((middle, right), axis=0)
    first_ids =  left[:,0]
    last_ids = last[:,0]
    return (first_ids, last_ids) 

xz_array_0 = read_chkpt('0.chkpt')[0] #this should always be initial file
#xz_list_0 = read_chkpt('0.chkpt')[1]
first_atoms = x_based_select(xz_array_0)[0]
#last_atoms = x_based_select(xz_array_0)[1]
plt.figure(1, figsize=(2,20))
#xz_array = read_chkpt('10000000.chkpt')[0] #filename of step you would like to see
xz_list = read_chkpt('6000000.chkpt')[1]
for atom in xz_list:
    if atom[0] in first_atoms:
        plt.plot(atom[1], atom[2], 'cx')
    else:
        plt.plot(atom[1], atom[2], 'bx')
plt.show(1)


#def plot_particles(pos_array, time_step):
#    plt.figure(1)
#    plt.plot(pos_array[:,0], pos_array[:,1], 'k.')
#    plt.axis('off')
#    plt.savefig('figures/' + str(time_step) + '.png', bbox_inches='tight')
#    plt.close(1)
    
#file_list = glob.glob('*' + '.chkpt')
#templ = '.chkpt'
#for file in file_list:
#    xz_array = read_chkpt(file)
#    plot_particles(xz_array, int(file[:-len(templ)]))

  