#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  17 11:11:03 2017

@author: brettcornick

This script reads an input LAMMPS file and creates a circle of variable radius within middle of the crystal. It changes the atom type
of the atoms inside the circle and then is able to create new LAMMPS files in which the circle is rotated.
"""

import numpy as np
import os, math, glob, re

def read_crystal(reference_file):
    """this fuction reads a custom LAMMPS file and returns the id, x, and y of each atom as an array and as a list. 
    It also returns the raw read data as 'position_data'"""
    with open(reference_file, 'r') as bulk_ref:
        position_data = bulk_ref.readlines()
        i = [n for n, l in enumerate(position_data) if l.startswith('ITEM: ATOMS')][0]
        id_x_y_list = []
        for line in range(i + 1, len(position_data)):
            atom_id = int(position_data[line].split()[0])
            x_pos = float(position_data[line].split()[3])
            y_pos = float(position_data[line].split()[4])
            mass = float(position_data[line].split()[2])
            id_x_y_list.append([atom_id, x_pos, y_pos])
        id_x_y_array = np.array(id_x_y_list)
        return (id_x_y_array, id_x_y_list, position_data, mass)   
    
def R_based_select(input_array, input_list, radius):
    """this function takes the list and array from the read_crystal function and a user entered radius and finds the atoms 
    inside of that radius. it returns lists of the ids of the atoms in the circle and of the ids of the atoms outside of the circle"""
    box_dim = (input_array.max(axis=0)[1]-input_array.min(axis=0)[1], input_array.max(axis=0)[2]-input_array.min(axis=0)[2])
    inside_ids = []
    outside_ids = []
    for atom in input_list:
        if (atom[1]-box_dim[0]/2)**2 + (atom[2]-box_dim[1]/2)**2 <= radius**2:
            inside_ids.append(atom[0])
        else:
            outside_ids.append(atom[0])
    return (inside_ids, outside_ids, box_dim) 

def write_in_circle(read_file):
    """this function makes a new LAMMPS script in which the atoms inside of the circle have been assigned a different type (type 2), 
    from the atoms outside of the circle"""
    new_lammps = open('bulk_circle_%iR.l' % R, 'w')
    i = [n for n, l in enumerate(read_file) if l.startswith('ITEM: ATOMS')][0]
    for line in range(0, i + 1):
        new_lammps.write(read_file[line])
    for line in range(i + 1, len(read_file)):
        if int(read_file[line].split()[0]) in circle_ids:
            new_line_list = read_file[line].split()
            new_line_list[1] = '2'
            new_line = ' '.join(new_line_list)
            new_lammps.write(new_line + '\n')
        else:
            new_lammps.write(read_file[line])
    new_lammps.close()

def rotate_circle(circled_lammps, theta, box_dim):
    """"this function reads a LAMMPS script in which the circle has already been selected and defined and then rotates that circle
    of atoms using the rotation matrix by an angle theta (degrees)"""
    rad_theta = math.radians(theta)
    a = math.cos(rad_theta)
    b = -math.sin(rad_theta)
    c = math.sin(rad_theta)
    d = math.cos(rad_theta)
    rot_mat = np.array([(a,b),(c,d)])
    with open(circled_lammps, 'r') as pre_rot:
        data = pre_rot.readlines()
    new_lammps = open('bulk_rotate_%ideg.l' % theta, 'w')
    i = [n for n, l in enumerate(data) if l.startswith('ITEM: ATOMS')][0]
    for line in range(0, i + 1):
        new_lammps.write(data[line])
    for line in range(i + 1, len(data)):
        if int(data[line].split()[0]) in circle_ids:
            new_line_list = data[line].split()
            x_y_list = []
            x_y_list.append(float(new_line_list[3])-float(box_dim[0]/2))
            x_y_list.append(float(new_line_list[4])-float(box_dim[1]/2))
            new_line_array = np.asarray(x_y_list)
            new_line_array = np.vstack(new_line_array)
            after_rot_array = np.dot(rot_mat, new_line_array)
            new_line_list[3] = str(after_rot_array[0][0]+box_dim[0]/2)
            new_line_list[4] = str(after_rot_array[1][0]+box_dim[1]/2)
            new_line = ' '.join(new_line_list)
            new_lammps.write(new_line + '\n')
        else:
            new_lammps.write(data[line])
    new_lammps.close()
    
def make_readable_data(rotated_circle, num_atoms, mass):
    with open(rotated_circle, 'r') as r_d:
        pre_data = r_d.readlines()
    x_min = pre_data[5].split()[0]
    x_max = pre_data[5].split()[1]
    y_min = pre_data[6].split()[0]
    y_max = pre_data[6].split()[1]
    z_min = pre_data[7].split()[0]
    z_max = pre_data[7].split()[1]
    new_lammps = open('rot_lmp_read.l', 'w')
    i = [n for n, l in enumerate(pre_data) if l.startswith('ITEM: ATOMS')][0]
    new_lammps.write('LAMMPS readable\n\n%s atoms\n2 atom types\n\n%s %s xlo xhi\n%s %s ylo yhi\n%s %s zlo zhi\n\nMasses\n\n1 %s\n2 %s\nAtoms\n\n' \
                     % (num_atoms, x_min, x_max, y_min, y_max, z_min, z_max, mass, mass))
    for line in range(i + 1, len(pre_data)):
        line_list = pre_data[line].split()
        del line_list[2]
        line = ' '.join(line_list)
        new_lammps.write(line + '\n')
    new_lammps.close()

numbers = re.compile(r'(\d+)')
def numericalSort(value):
    """this function is required to sort the files numerically (ie. 9 !> 10)"""
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts
    
#def track_orientation():
    
    
ref_file = 'reference_bulk.l'
R = 100 #angstroms
rotation_angle = 30 #degrees 
sim_temp = '1000K' #temperature in K as string

cwd = os.getcwd()
(xy_array, xy_list, original_read, mass) = read_crystal(str(cwd) + '/' + ref_file)

(circle_ids, other_ids, box_dim) = R_based_select(xy_array, xy_list, R)

write_in_circle(original_read)

rotate_circle(str(cwd + '/bulk_circle_%iR.l' % R), rotation_angle, box_dim)

num_atoms = str(int(xy_array.max(axis=0)[0]))
make_readable_data('bulk_rotate_%sdeg.l' % rotation_angle, num_atoms, mass)

file_list = sorted(glob.glob(str(cwd) + '/' + sim_temp + '/out/' + '*' + '.chkpt'), key=numericalSort)