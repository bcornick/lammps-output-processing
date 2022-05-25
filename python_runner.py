#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 12:59:33 2017

@author: Brett


This script is designed to calculate average lattice parameter over a range of 
different temperature in order to calculate thermal expansion
"""
import shutil as sh
import re, random, os
import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt

"""First part below creates a new directory with potential and input script for each
temperature step. At each temperature multiple different runs from different random
seeds are performed. number of replications is determined by the variable num_rand_replicates"""

Tmin = 50
Tmax = 2750
Tstep = 100
num_rand_replicates = 2 #indicate number of replications from different seeds desired
mean_all_alats = []
mean_all_pressures = []
for temp in range(Tmin, Tmax + Tstep, Tstep):
    count = 1
    mean_alat = 0
    mean_pressure = 0
    for replicate in range(num_rand_replicates):
        path1 = '/Users/brettcornick/LAMMPS/simulations/npt'
        os.chdir(path1)
        new_dir_name = 'T_' + str(temp) + '/' + str(replicate + 1)
        sh.copytree('template_dir', new_dir_name)
        with open(new_dir_name+'/big_hybrid_tmp.in', 'r') as current_read:
            with (open(new_dir_name+'/big_hybrid.in','w')) as current_write:
                data = current_read.read()
                data_with_temp = re.sub('TEMPER', str(max(temp, 1)), data)
                data_with_rand = re.sub('RANDOM', str(random.randint(1, 10000)), data_with_temp)
                current_write.write(data_with_rand)
        
        """This next part runs each input file for each different temperature and outputs the results 
        (output variables defined by template script) into the out folder"""
        path2 = path1 + '/' + new_dir_name
        os.chdir(path2)
        p1 = sp.Popen(['/Users/brettcornick/bin/lmp_serial', '-i', path2 + '/big_hybrid.in'])
        p1.wait()
        """This next part reads the necessary lines of the LAMMPS logfile and turns them into an array"""
        with open(path2+'/log.lammps', 'r') as f:
            line_list = []
            read_data = f.readlines()
            line_index = 0
            for lines in read_data:
                if line_index >= 119 and line_index <= 199: #start reading data from line n1 + 1 and stop after n2 + 1
                    step = float(lines.split()[0])
                    lx = float(lines.split()[1])
                    atoms = float(lines.split()[2])
                    temperature = float(lines.split()[3])
                    pot_eng = float(lines.split()[4])
                    lx = float(lines.split()[5])
                    ly = float(lines.split()[6])
                    lz = float(lines.split()[7])
                    press = float(lines.split()[8])
                    pxx = float(lines.split()[9])
                    pyy = float(lines.split()[10])
                    pzz = float(lines.split()[11])
                    line_list.append([step, lx, atoms, temperature, pot_eng, lx, ly, lz, press, pxx, pyy, pzz])
                line_index += 1
        log_array = np.array(line_list)
        log_means = np.mean(log_array, axis=0)
        mean_alat = ((log_means[1]/3) + mean_alat) / count#the divide by 3 here comes from the xdim spec in the template LAMMPS file
        mean_pressure = ((log_means[8]) + mean_pressure) / count
        count += 1
    mean_all_alats.append(mean_alat)
    mean_all_pressures.append(mean_pressure)
       
plt.figure(1)
plt.subplot(211)
plt.plot(range(Tmin, Tmax + Tstep, Tstep), mean_all_alats, 'b.')
plt.subplot(212)
plt.plot(range(Tmin, Tmax + Tstep, Tstep), mean_all_pressures, 'r.')