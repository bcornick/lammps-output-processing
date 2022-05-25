#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:38:20 2017

@author: Brett
"""
import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
import os


"""This first section takes the initial LAMMPS input script, searches for a line
that contains 'displace_atoms' and is not a comment. It replaces that line
with a new line in LAMMPS format that increases the displacement by the step size.
For each new displacement step, a new LAMMPS input file is created with the
size of the displacement in the name"""

cwd = os.getcwd()

with open(cwd + '/gb4.in_final','r') as lammps_input:
    #change path and file name above to desired original input script
    read_data = lammps_input.readlines()
    y_start_displacement = 1.1
    y_displacement = y_start_displacement #starting displacement in x direction
    y_max_displacement = 1.3
    y_step = 0.01 #set to desired step size. be sure to change number of decimals in new file name and displacement below
    z_step = 0.01
    while y_displacement <= y_max_displacement: #set to max x displacement desired. note that displacement/step files will be created
        z_start_displacement = 1.3
        z_displacement = z_start_displacement#starting displacement in z direction
        z_max_displacement = 1.5
        while z_displacement <= z_max_displacement:
            new_file = open('new_lmp_file_%.3f_%.3f.in' % (y_displacement, z_displacement),'a') 
            #change path and name above to desired input folder/name , check decimals required
            for line in read_data:
                if 'displace_atoms' in line and '#' not in line:
                    new_file.write('displace_atoms upper move 0 %.3f %.3f units box \n' % (y_displacement, z_displacement))
                    #check decimals. be sure other parts of line above are consistent with original LAMMPS input
                else:
                    new_file.write(line)
            z_displacement = z_displacement + z_step
            new_file.close()
        y_displacement = y_displacement + y_step
        
    
    
"""This next section is inteded to individually run each of the different LAMMPS
input files created in the section above and to store their output of grain boundary
energy (Egb) to a new file called sepfile.dat (this name and output is defined in the 
LAMMPS script)"""

def frange(frange_start, frange_stop, frange_step): 
    #this function allows for the creation of a range using floats so that we can do a for loop over the displacement
    i = frange_start
    float_range = []
    while i <= frange_stop:
        float_range.append(i)
        i += frange_step
    return float_range

y_iterable_range = np.array(frange(y_start_displacement, y_displacement - y_step, y_step)) #change number of digits to match first section
z_iterable_range = np.array(frange(z_start_displacement, z_displacement - z_step, z_step))
percent_inc = float((1 / ((y_max_displacement - y_start_displacement) / y_step)) * 100)
print('Submitting to LAMMPS...')
time_index = 1
for y_step_file in y_iterable_range: #iterating across range of displacements
    for z_step_file in z_iterable_range:
        p1 = sp.Popen(['/g/g14/cornick1/bin/lmp_impi_borax', '-i', 'new_lmp_file_%.3f_%.3f.in' % (y_step_file, z_step_file)])
        p1.wait()
    print('Finished a step... %.1f percent complete.' % (time_index * percent_inc))
    time_index += 1
print('Submitted all LAMMPS.')
        #p1 runs the LAMMPS scripts using Popen. be sure that input file matches files made above
        #wait command is necessary to allow the process time to finish before moving on to the next
    


"""This next section minimizes the Egb data in sepfil.dat and returns the index 
of the minimum. Note that there may be indexing error if starting displacement
does not equal zero"""
#this is all done with similar structure to my read_file.py practice script
with open(cwd + '/sepfile.dat','r') as egb_outputs_file:
    read_egbs = egb_outputs_file.readlines()
    egb_list = []
    for egb in read_egbs:
        grain_bound_eng = float(egb.split()[2])
        egb_list.append(grain_bound_eng)
        
min_index = egb_list.index(min(egb_list))

"""This next section uses the index of the minimum found above to resubmit the
LAMMPS script that supplied the minimum. then it reads the output and it plots 
that grain boundary using matplotlib and supplies the data in an output file 
called rel.chkpt (file name and location defined in LAMMPS script)"""
if min_index < len(z_iterable_range): #be sure to check that indexes are returning correct file.
    y_file_index = y_start_displacement
else:
    y_file_index = (int((min_index)/len(z_iterable_range)) + 1) * y_step + y_start_displacement - y_step
z_file_index = (min_index) % len(z_iterable_range) * z_step + z_start_displacement


p2 = sp.Popen(['/g/g14/cornick1/bin/lmp_impi_borax', '-i', 'new_lmp_file_%.3f_%.3f.in' % (y_file_index, z_file_index)])
p2.wait()

#with open(cwd + '/out/rel.chkpt', 'r') as final_output:
#    line_list = []
#    read_data = final_output.readlines()
#    line_index = 0
#    for lines in read_data:
#        if line_index >= 9: #start reading data from line 10
#            identity = float(lines.split()[0])
#            atom_type = float(lines.split()[1])
#            mass = float(lines.split()[2])
#            x = float(lines.split()[3])
#            y = float(lines.split()[4])
#            z = float(lines.split()[5])
#            c_eng = float(lines.split()[6])
#            line_list.append([identity, atom_type, mass, x, y, z, c_eng])
#        line_index += 1
#file_array = np.array(line_list)
#x_coords = file_array[:,3]
#y_coords = file_array[:,4]
#z_coords = file_array[:,5]
#c_eng_val = file_array[:,6]
#plt.figure(1, figsize=(1,8)) #creates figure for two plots
#plt.subplot(211)
#plt.plot(y_coords, z_coords, 'b.') 
#plt.subplot(212)
#plt.plot(x_coords, c_eng_val, 'r.')
#plt.savefig('gb_plot.pdf') #saves figure to pdf file called 'gb_plot'
#plt.show(1)


"""this final portion deletes all of the additional input files (except the one 
that provided the min Egb) as well as the sepfile with all Egb values that were 
created and can be commented out if desired"""

files = os.listdir(cwd)
for file in files:
    if '_%.3f_%.3f.in' %(y_file_index, z_file_index) not in file: #adjust for number of decimals in step
        if file.startswith('new_'):# or file.startswith('sepfile'):
            os.remove(os.path.join(cwd, file))
print('Finished!')
