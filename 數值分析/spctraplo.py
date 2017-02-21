#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 17:57:40 2017

@author: tino
"""        
import time
start_time = time.time()


import math
import util
import numpy as np
import matplotlib.pyplot as plt
dict_E_T_Threads = [] 


#==============================================================================
# PARAMETERS OF SYS

LATTICE_A = 9.49569 * math.pow(10, -10) # m
LATTICE_B = 9.49569 * math.pow(10, -10) # m
ACTIVE_SITE = 6 / (LATTICE_A * LATTICE_B) 
BETA = 3 # K/sec
TOTAL_PRESSURE = 2 * math.pow(10, -10) # atm
TEMPERATURE = 500 # K
#==============================================================================
    
#==============================================================================
# PARAMETER OF NH3

GAS_MASS = 17.001 / (6 * math.pow(10, 23) * 1000) # kg /atom
ROT_CONST_A = 610.85 # 1/m
ROT_CONST_B = 983.86 # 1/m
ROT_CONST_C = 983.91 # 1/m
SIGMA = 3
HVS_GAS = [435.460659, 431.205986, 415.541526, 203.517923, 201.833141, 120.027150] # meV
#==============================================================================

#==============================================================================
# 1xnh3@RuO2 frequency (cm-1)

SURFACE = [702.5384, 667.3163, 666.8468, 637.0404, 632.6593, 619.8975, 619.8880, 594.6102, 565.8163, 549.3752, 535.0747, 533.3084, 531.2641, 526.4177, 525.8286, 510.1579, 494.7568, 494.3726, 491.6280, 489.0763, 480.0920, 468.2642, 435.4031, 434.9185, 366.7504, 319.1306, 318.9866, 313.6116, 280.4454, 277.8176, 277.7921, 256.1764, 253.9295, 251.0983, 250.5850, 238.4942, 234.3757, 228.4755, 227.8496, 213.4265, 213.0562, 208.7910, 197.7978, 195.4322, 155.2341, 150.9349, 150.7593, 150.6323, 142.9187, 138.6253, 138.3549, 119.8644, 119.2399, 113.8064, 109.3032, 108.8512, 104.3528, 86.9122, 73.1832, 22.8849]
ADSORBENT = [3497.8656, 3470.6895, 3357.7690, 1612.5701, 1600.9326, 1183.3037, 719.5083, 693.4747, 692.7758, 668.3197, 652.8541, 633.7733, 617.3873, 612.5937, 611.8252, 589.7271, 579.3086, 568.4171, 548.1430, 544.2284, 541.5081, 531.2811, 525.1468, 521.1906, 516.3771, 511.2057, 505.1219, 497.6588, 484.5486, 479.2293, 474.5780, 450.5895, 435.0337, 381.6198, 345.6290, 341.5104, 309.1609, 293.0269, 287.1928, 285.3356, 285.0449, 280.7592, 277.3797, 260.9612, 259.1692, 254.9810, 251.2341, 248.6749, 246.2514, 233.4536, 227.0563, 223.6744, 221.7741, 208.7098, 207.1964, 202.0659, 201.4852, 198.8288, 187.8602, 184.9007, 177.7483, 169.9000, 164.6706, 159.0970, 146.6093, 138.8189, 133.0448, 130.0533, 120.7778, 95.2894, 91.4410, 59.2641]

#==============================================================================


H_eV = 4.135667662 * math.pow(10, -15)  # H_PLANCK_eV, eV.sec
C = 299792458  # speed of light m/s
HVS_SURFACE = [H_eV * C * (i * 100) * 1000 for i in SURFACE] # convert to meV
HVS_ADSORBENT = [H_eV * C * (i * 100)* 1000 for i in ADSORBENT]

adsorbent = util.Adsorbent(HVS_SURFACE, HVS_ADSORBENT)
adsorbent.set_sys_parameter(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
adsorbent.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)


#t = []
#E = []
#for adsorbent.temperature in np.linspace(0.02, 1, 40, endpoint=True):
#    t.append(adsorbent.temperature)
#    E.append(adsorbent.get_E_star())
#print(E)
#plt.plot(t, E)

#print(adsorbent.get_translation_partition_function())
#print(adsorbent.get_rotation_partition_function_nonlinear())
#print(adsorbent.get_vibration_partition_function())
#print(adsorbent.get_E_t_dict())
#print(adsorbent.get_T('1.8314'))

#print(HVS_ADSORBENT)
#print(HVS_SURFACE)

#bins = np.linspace(1.3, 2, 100, endpoint=True)
#mu, sigma = 1.56, 0.1
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2)),linewidth=2, color='r')
##plt.show()
#
#print(bins) 

   
d1 = adsorbent.get_E_t_list()
print(adsorbent.get_T(8))

    

print("--- %s seconds ---" % (time.time() - start_time))


        
if __name__ == "__main__":
    pass
