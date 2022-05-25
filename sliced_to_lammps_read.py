#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:04:22 2018

@author: brettcornick
"""

def make_readable_data(chkpt_file, num_atoms, mass, atom_types):
    with open(chkpt_file, 'r') as r_d:
        pre_data = r_d.readlines()
    x_min = pre_data[5].split()[0]
    x_max = pre_data[5].split()[1]
    y_min = pre_data[6].split()[0]
    y_max = pre_data[6].split()[1]
    z_min = pre_data[7].split()[0]
    z_max = pre_data[7].split()[1]
    new_lammps = open('%s_relaxed_lmp_read' % chkpt_file, 'w')
    i = [n for n, l in enumerate(pre_data) if l.startswith('ITEM: ATOMS')][0]
    new_lammps.write('LAMMPS readable\n\n%s atoms\n%s atom types\n\n%s %s xlo xhi\n%s %s ylo yhi\n%s %s zlo zhi\n\nMasses\n\n1 %s\n2 %s\n3 %s\nAtoms\n\n' \
                     % (num_atoms, atom_types, x_min, x_max, y_min, y_max, z_min, z_max, mass, mass, mass))
    for line in range(i + 1, len(pre_data)):
        line_list = pre_data[line].split()
        del line_list[6:]
        del line_list[2]
        line = ' '.join(line_list)
        new_lammps.write(line + '\n')
    new_lammps.close()

file_name = '650.chkpt'    
num_atoms = 9936
mass = 63.546
atom_types = 3
make_readable_data(file_name, num_atoms, mass, atom_types)