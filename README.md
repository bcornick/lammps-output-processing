# lammps-output-processing
This repository is a collection of python scripts used for manipulating the outputs of LAMMPS molecular dynamics simulations for grain boundary analysis. This work was done as part of my Master's thesis in Computational Materials Science at UCLA, in collaboration with Lawrence Livermore National Laboratory. The larger aim of this project was to propose novel grain boundary structures in lattice materials and predict their behavior at extreme temperatures and stresses.

ASSETS
"sliced_to_lammps_read.py"
-convert slice of .chkpt file to LAMMPS readable file.

"chkpt_to_lammps_read.py"
-convert .chkpt file to LAMMPS input file

"sample.chkpt"
-example .chkpt file type. this file is a LAMMPS output.

"circle_find.py"
-This script reads an input LAMMPS file and creates a circle of variable radius within middle of the crystal. It changes the atom type
of the atoms inside the circle and then is able to create new LAMMPS files in which the circle is rotated.

find_shear.py
-plots shear stress vs. time using LAMMPS output files as input

gb_pos_find.py
-This script is designed to find how the position of a grain boundary changes
when shear stress is applied

mean_alat_finder.py
-find the mean lattice spacing of a crystal

mobility_calculator.py
-calculate grain boundary mobility

particle_track.py
-This script is designed to track the movement of a certain group of atoms from
one time step to another. It will then colorize this group and display it's original
position and its final position.

python_1Ddisplacement.py
-this script displaces a block of atoms in one dimension based on a collection of LAMMPS outputs

python_2Ddisplacement.py
-this script displaces a block of atoms in two dimensions based on a collection of LAMMPS outputs

python_runner.py
-This script is designed to calculate average lattice parameter over a range of 
different temperature in order to calculate thermal expansion
