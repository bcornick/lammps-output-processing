#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 13:25:58 2018

@author: brettcornick
"""

import math

theta = 18.9246444161
beta = 0.293579853
shear = 0.897672302381
v_p = 0.1

theta_radians = math.radians(theta)
v_n = v_p/beta
mobility = v_n/(beta*shear*1000)
mobility_const = 2*mobility*math.sin(theta_radians/2)/(math.cos(theta_radians/2)*math.cos(theta_radians/2))

print('Mobility = ' + str(mobility) + '*10^-6')
print('Mobility Constant = ' + str(mobility_const) + '*10^-6')