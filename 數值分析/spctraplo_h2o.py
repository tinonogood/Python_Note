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
from matplotlib.ticker import MultipleLocator
from scipy import constants as C
from scipy.integrate import odeint


H_eV = C.h * C.physical_constants["joule-electron volt relationship"][0]  # H_PLANCK_eV, eV.sec
KB_EV = C.k * C.physical_constants["joule-electron volt relationship"][0]  # K_BOLTZMANN_EV. eV/K

#==============================================================================
# PARAMETERS OF SYS

LATTICE_A = 6.214 * math.pow(10, -10) # m
LATTICE_B = 6.3625 * math.pow(10, -10) # m
ACTIVE_SITE = 2 / (LATTICE_A * LATTICE_B) 
BETA = 8 # K/sec
TOTAL_PRESSURE = 2 * math.pow(10, -10) # atm
TEMPERATURE = 500 # K
#==============================================================================
    
#==============================================================================
# PARAMETER OF H2O

GAS_MASS = 18.00 / (6 * math.pow(10, 23) * 1000) # kg /atom
ROT_CONST_A = 921.21 # 1/m
ROT_CONST_B = 1391.9 # 1/m
ROT_CONST_C = 2724.1 # 1/m
SIGMA = 2
HVS_GAS = [475.536814, 440.226355, 195.183757] # meV
#==============================================================================

#==============================================================================
# 1xh2o@RuO2 frequency (meV)
SURFACE = [455.791118, 437.673094, 406.518391, 353.720848, 202.458167, 132.718034, 129.316596, 110.417176, 105.727556, 98.972498, 87.759257, 83.806765, 79.684028, 78.730699, 77.750323, 76.520569, 74.072214, 71.293954, 70.079807, 68.374942, 67.338243, 64.433568, 63.573644, 63.132790, 58.570732, 57.795491, 56.417384, 55.081672, 53.068364, 48.808827, 48.643408, 44.479379, 44.168074, 43.253037, 42.268033, 39.006981, 38.548198, 35.938332, 33.315367, 31.419334, 30.462824, 29.078611, 27.608362, 27.282557, 26.142434, 24.343011, 22.679998, 22.108185, 21.363139, 17.673306, 17.438105, 15.975060, 8.962585, 6.156649]
ADSORBENT = [462.838623, 437.274472, 419.399265, 380.427820, 345.519074, 333.546344, 205.664339, 200.503152, 147.329413, 138.501300, 136.048144, 118.196733, 110.030323, 103.142250, 86.799463, 82.553807, 82.127941, 79.448467, 76.468837, 76.088168, 75.910615, 73.676461, 71.962872, 70.315971, 69.259844, 65.957307, 64.955788, 64.006513, 62.533722, 61.491612, 60.305435, 57.955834, 56.208768, 52.952737, 52.489161, 49.788815, 46.801586, 45.627972, 45.335517, 44.731363, 42.253815, 41.409345, 39.212749, 37.861885, 36.708333, 36.134104, 31.914182, 30.231775, 29.033810, 28.254211, 26.849478, 26.177759, 24.364067, 23.352589, 22.121441, 21.434693, 20.170855, 17.579106, 16.248021, 14.940966, 10.876287, 8.761324, 6.298514]

#==============================================================================

DesorpE = 0.4758

adsorbent = util.Adsorbent(SURFACE, ADSORBENT, DesorpE)
adsorbent.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
adsorbent.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)

d1 = adsorbent.get_E_t_list()

def plot_axis(x_major, x_minor, xlim, y_major, y_minor, ylim):
    majorLocator_x = MultipleLocator(x_major)
    minorLocator_x = MultipleLocator(x_minor)
    majorLocator_y = MultipleLocator(y_major)
    minorLocator_y = MultipleLocator(y_minor)    
    ax = plt.gca()
    ax.xaxis.set_major_locator(majorLocator_x)
    ax.xaxis.set_minor_locator(minorLocator_x)
    ax.set_xlim(xlim)
    ax.yaxis.set_major_locator(majorLocator_y)
    ax.yaxis.set_minor_locator(minorLocator_y)
    ax.set_ylim(ylim)
    for label in ax.xaxis.get_majorticklabels():
        label.set_fontsize(20)
    for label in ax.yaxis.get_majorticklabels():
        label.set_fontsize(20)

def normal_E_distri(desorp_E, sigma):
    E = np.linspace(desorp_E - 3 * sigma, desorp_E + 3 * sigma, 64, endpoint=True)
    N0 = 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (E - desorp_E)**2 / (2 * sigma**2))
    return E, N0
        
def E_distri(desorp_E, sigma): 
    E_checks = []
    N0_of_E_cals = []
    for E_check in np.linspace(desorp_E - 3 * sigma, desorp_E + 3 * sigma, 64, endpoint=True):
        T = adsorbent.get_T(E_check)
        adsorbent.temperature = T
        fs = []
        N0s_of_E_guess = []
        for E in np.linspace(E_check - 2 * KB_EV * T, E_check + 4 * KB_EV * T, 256, endpoint=True):
            f = adsorbent.get_f_energy_distribution(E)
            fs.append(f)
            N0s_of_E_guess.append(1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (E - desorp_E)**2 / (2 * sigma**2)))
        rd_sec = [i * j * (6 * KB_EV * T / 255) for i, j in zip(fs, N0s_of_E_guess)]
        rd = sum(rd_sec)
        N0_of_E_cal = rd / (BETA * (E_check / T))
        E_checks.append(E_check)
        N0_of_E_cals.append(N0_of_E_cal)
    return E_checks, N0_of_E_cals
        
def plot_E_distri(desorp_E, sigma): #red: normal distribution, blue: calculated
    print("sigma", sigma)
    (E, N0) = normal_E_distri(desorp_E, sigma)
    (E_checks, N0_of_E_cals) = E_distri(desorp_E, sigma)
    plt.plot(E, N0, color='r')
    plt.plot(E_checks, N0_of_E_cals)
    plot_axis(0.3, 0.1, [desorp_E - 4 * sigma, desorp_E + 4 * sigma], 1, 0.5, [0,1/(2.5 * sigma)])
    plt.show()
    return

def get_rmse(desorp_E, sigma):
    (E, N0) = normal_E_distri(desorp_E, sigma)
    (E_checks, N0_of_E_cals) = E_distri(desorp_E, sigma)
    err_square = [(i - j) ** 2 for i, j in zip(N0, N0_of_E_cals)]
    rmse = np.sqrt(sum(err_square)/64)
    return rmse
    
def sigma_rmse(desorp_E, init_sigma, final_sigma):
    sigmas = []
    rmses = []
    for sigma in np.linspace(init_sigma, final_sigma, int((final_sigma - init_sigma)/0.005 + 1), endpoint=True):
        sigmas.append(sigma)
        rmses.append(get_rmse(desorp_E, sigma))
    return sigmas, rmses
    
def plot_sigma_rmse(desorp_E, init_sigma, final_sigma):
    (sigma, rmse) = sigma_rmse(desorp_E, init_sigma, final_sigma)
    plot_axis((final_sigma - init_sigma)/5, (final_sigma - init_sigma)/10, [init_sigma, final_sigma], 1, 0.5, [0,2])
    plt.plot(sigma, rmse)
    plt.show()
    return
    
def get_proper_sigma(desorp_E, init_sigma, final_sigma):
    (sigmas, rmses) = sigma_rmse(desorp_E, init_sigma, final_sigma)
    curvatue_pre = 0
    for i in range(int((final_sigma - init_sigma)/0.005 + 1)):
#        x = np.array([sigmas[i], sigmas[i+1], sigmas[i+2], sigmas[i+3], sigmas[i+4]])
#        y = np.array([rmses[i], rmses[i+1], rmses[i+2], rmses[i+3], rmses[i+4]])
        x = np.array(sigmas)
        y = np.array(rmses)
        curve = np.polyfit(x, y, 5)
        y_dev = 5 * curve[0] * (sigmas[i] ** 4) + 4 * curve[1] * (sigmas[i] ** 3) + 3 * curve[2] * (sigmas[i] ** 2) + 2 * curve[3] * (sigmas[i] ** 1) + curve[4]
#        y_dev = 3 * curve[0] * (sigmas[i+2] ** 2) + 2 * curve[1] * (sigmas[i+2]) + curve[2]
        y_sec_dev = 20 * curve[0] * (sigmas[i] ** 3) + 12 * curve[1] * (sigmas[i] ** 2) + 6 * curve[2] * (sigmas[i] ** 1) + 2 * curve[3] 
#        y_sec_dev = 6 * curve[0] * (sigmas[i]) + 2 * curve[1]
        curvature = (y_sec_dev / np.power(1 + y_dev * y_dev, 3/2))
        if curvature < curvatue_pre:
            return sigmas[i-1]
        curvatue_pre = curvature
        
def disrp_TPD_data(desorp_E, init_T, final_T):
    sigma = get_proper_sigma(desorp_E, 0.03, 0.12)
    Ts = []
    rds = []
    for T in np.linspace(init_T, final_T, int((final_T - init_T)/3 + 1), endpoint=True):
        adsorbent.temperature = T
        E = adsorbent.get_E_star()
        N0 = 1/(sigma * np.sqrt(2 * np.pi)) * math.exp(-(E - desorp_E)**2 / (2 * sigma ** 2))
        rd = N0 * BETA * adsorbent.get_E_star() / T
        Ts.append(T)
        rds.append(rd)
    return Ts,rds
        
def plot_disrp_TPD(desorp_E, init_T, final_T):
    (Ts,rds) = disrp_TPD_data(desorp_E, init_T, final_T)
    plt.plot(Ts, rds)
    plot_axis(100, 10, [init_T, final_T], 0.1, 0.02, [0,0.1])
    plt.show()
    
#plot_disrp_TPD(DesorpE, 100 , 700)    
print(disrp_TPD_data(0.4758, 81, 381))

#    
#
##==============================================================================
## 2to1_1xnh3@RuO2 frequency (meV)
#one_nh3_ADSORBENT = [456.880565, 334.137440, 196.234894, 123.790603, 87.560382, 85.792435, 80.972677, 79.627873, 78.848991, 76.466637, 75.616584, 74.174262, 71.137194, 68.809740, 66.355949, 64.535744, 61.541220, 61.103742, 59.352419, 58.000482, 55.724779, 50.174117, 49.636665, 47.064896, 43.811751, 43.378082, 40.371879, 40.282785, 39.162899, 36.330909, 36.029404, 34.494009, 33.998444, 28.367278, 27.731475, 27.362270, 24.406388, 24.006098, 22.846637, 21.684477, 19.684382, 17.884116, 16.900007, 8.865033, 6.269974]
#two_nh3_ADSORBENT = [455.791118, 437.673094, 406.518391, 353.720848, 202.458167, 132.718034, 129.316596, 110.417176, 105.727556, 98.972498, 87.759257, 83.806765, 79.684028, 78.730699, 77.750323, 76.520569, 74.072214, 71.293954, 70.079807, 68.374942, 67.338243, 64.433568, 63.573644, 63.132790, 58.570732, 57.795491, 56.417384, 55.081672, 53.068364, 48.808827, 48.643408, 44.479379, 44.168074, 43.253037, 42.268033, 39.006981, 38.548198, 35.938332, 33.315367, 31.419334, 30.462824, 29.078611, 27.608362, 27.282557, 26.142434, 24.343011, 22.679998, 22.108185, 21.363139, 17.673306, 17.438105, 15.975060, 8.962585, 6.156649]
#one_over_one = [464.000419, 436.119585, 373.215652, 329.801828, 199.111619, 149.164559, 139.515281, 119.181599, 102.037040, 87.432002, 80.492300, 78.651569, 78.360742, 76.674627, 75.842272, 74.661124, 71.700671, 70.944751, 68.409538, 65.931427, 64.674028, 64.569292, 62.730466, 61.523136, 60.881744, 56.469928, 52.130516, 50.564355, 50.423893, 49.131868, 45.373776, 43.651074, 43.281694, 41.029238, 38.656532, 37.358483, 36.051169, 34.907899, 34.742890, 31.312666, 28.399370, 27.403800, 26.712642, 25.691564, 23.312081, 22.896481, 20.136837, 18.748826, 16.509681, 15.977567, 14.740473, 11.646889, 9.127809, 1.355649]
#TS_two_one_over_one = [465.631005, 441.836313, 437.886970, 389.851005, 199.583711, 120.520470, 108.420743, 98.003866, 89.456273, 87.799626, 81.800452, 80.572722, 78.545095, 78.082815, 77.958707, 74.556669, 73.289763, 69.854332, 67.480174, 66.835758, 63.875444, 63.563492, 61.872990, 59.580503, 57.060299, 56.020442, 51.138358, 49.105310, 47.223915, 45.290040, 44.660684, 43.020891, 40.831524, 38.454580, 37.344204, 35.581141, 35.302690, 34.055150, 33.740825, 30.642405, 27.871478, 27.560207, 26.218996, 25.451416, 23.649690, 20.290027, 19.837353, 17.932397, 17.129328, 12.233839, 9.780265, 6.620777, 5.230981]
##==============================================================================
#
###==============================================================================
### 2to1_1xnh3@RuO2 frequency (meV)
##one_nh3_ADSORBENT = [429.368941, 423.051695, 404.362478, 204.748221, 203.158308, 151.299805, 90.738006, 88.160513, 85.158983, 84.156261, 83.280042, 81.144880, 79.630317, 77.897430, 72.395107, 70.549398, 67.944035, 67.707895, 65.351565, 64.374373, 64.193986, 63.239739, 61.071018, 60.628457, 58.943888, 58.156973, 57.223757, 54.709008, 53.493446, 52.831642, 48.456687, 47.101755, 46.834532, 43.838785, 42.644135, 40.731688, 40.202173, 38.402156, 37.938231, 36.996661, 35.104647, 34.922085, 34.522268, 33.735834, 31.616255, 30.688896, 28.616233, 28.015585, 27.310186, 25.785377, 25.572355, 23.866189, 23.434342, 22.201330, 21.567864, 19.879773, 18.508609, 18.397817, 16.484656, 16.069680, 15.581425, 13.159342, 7.582662, 5.389274, 4.608332, 2.632964]
##two_nh3_ADSORBENT = [429.291494, 427.816384, 426.981887, 423.398537, 412.552573, 403.094597, 205.684320, 204.554723, 202.920684, 198.665841, 147.315748, 145.142703, 89.468711, 88.172499, 86.713124, 84.241799, 83.903469, 83.137720, 82.421655, 81.153815, 78.895439, 78.270790, 75.206332, 74.648850, 73.154166, 69.478701, 68.464942, 67.488184, 66.800234, 66.146387, 63.676219, 62.521544, 61.557594, 60.229905, 56.648046, 55.500780, 55.008409, 54.626045, 49.932728, 49.567770, 45.715937, 43.799295, 43.466350, 42.913877, 42.748133, 42.237561, 40.581568, 39.731710, 38.211020, 37.512763, 36.881931, 35.852139, 35.697463, 35.231574, 33.779379, 33.091465, 29.984015, 28.693642, 28.425567, 27.650142, 26.559301, 26.417113, 23.782648, 23.230340, 22.955146, 22.143194, 22.014823, 20.964036, 19.757497, 19.190496, 18.663609, 17.756373, 16.683390, 16.180146, 15.202208, 10.554146, 7.928159, 6.112400]
##one_over_one = [429.744174, 424.374887, 421.659790, 412.892437, 411.389469, 380.336985, 208.394752, 206.448016, 203.900837, 202.302280, 159.913830, 141.674962, 102.102229, 91.845925, 88.660901, 85.430129, 84.200344, 81.472451, 79.647712, 77.047263, 75.464004, 73.795867, 72.302617, 71.304573, 68.980852, 67.553130, 66.514080, 65.436828, 64.660755, 63.114707, 60.242825, 60.090120, 57.685263, 56.177320, 54.334929, 54.176153, 53.587678, 52.123489, 49.860297, 49.392241, 46.637304, 45.456067, 44.608034, 41.902363, 41.534222, 39.975066, 38.363489, 37.809789, 37.340157, 36.511950, 35.847481, 35.018343, 34.453330, 33.896068, 32.824597, 31.044703, 30.612834, 30.184494, 28.481089, 26.924725, 26.474315, 25.859281, 25.358878, 24.385051, 22.087408, 20.154645, 19.782358, 19.595317, 19.336111, 18.164005, 17.068955, 16.420131, 15.813034, 14.916618, 14.393971, 9.957209, 8.169838, 4.593077]
##TS_two_one_over_one = [430.279471, 425.280865, 424.955933, 414.017373, 411.574689, 382.548886, 208.135683, 205.514589, 202.902355, 201.374010, 158.241473, 142.876815, 101.955507, 93.491723, 89.008642, 85.885723, 84.285204, 81.412186, 79.601532, 77.572416, 74.885680, 73.665592, 71.916738, 69.732709, 68.934237, 67.252685, 66.188157, 65.566813, 64.244823, 62.376203, 60.162486, 60.078258, 56.413568, 55.707568, 54.724378, 53.947638, 51.350309, 50.017996, 49.419999, 46.659818, 45.637352, 45.381176, 44.908047, 42.790553, 42.277013, 39.930133, 38.065413, 37.647639, 36.755329, 36.240597, 35.498033, 34.484975, 33.514505, 33.082736, 31.829929, 30.152531, 29.847069, 29.562774, 28.103474, 27.414732, 25.196665, 25.096331, 23.912057, 21.199906, 20.208322, 19.655355, 19.147554, 18.543720, 17.298080, 16.547087, 15.921743, 15.354637, 14.301688, 13.505006, 8.466336, 7.615109, 4.592687]
###==============================================================================
#
#
#
#a1 = util.Adsorbent(one_nh3_ADSORBENT, two_nh3_ADSORBENT, 1.453)
#r1 = util.Reactant(two_nh3_ADSORBENT, TS_two_one_over_one, 11.093)
#r2 = util.Reactant(one_over_one, TS_two_one_over_one, 10.213)
#a2 = util.Adsorbent(one_nh3_ADSORBENT, one_over_one, 0.581)
#
## try to improv
##==============================================================================
#a1.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
#a1.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
#r1.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
#r1.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
#r2.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
#r2.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
#a2.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
#a2.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
##==============================================================================
#
#theta_1st_0 = 1. # 1st layer population initial
#theta_2nd_0 = 0.00000001  # 2nd layer population initial
#gas_phase = 0.0  # gas  phase 
#y0 = [theta_1st_0, theta_2nd_0]
#t = np.linspace(375, 440, 31)
#
## solve the mk model dy/dt = f(y, t) & y=theta
#def f(y, t):
#    theta_1st_i = y[0]
#    theta_2nd_i = y[1]
#    # the rate constant
##    k_diff = (C.k * (T0 + BETA * t) / C.h) * () * np.exp(- r1.barrier / (KB_EV * (T0 + BETA * t)))
##    k_diff_rev = (C.k * (T0 + BETA * t) / C.h) * np.exp(- r2.barrier / (KB_EV * (T0 + BETA * t)))
#    k_diff = r1.get_rate_constant(t)
#    k_diff_rev = r2.get_rate_constant(t)
#    k_desorp_1st = a1.get_v(t) * np.exp(- a1.desorption_energy / (KB_EV * t)) 
#    k_desorp_2nd = a2.get_v(t) * np.exp(- a2.desorption_energy / (KB_EV * t))
#    # the model equations
##    print(k_diff/k_diff_rev, k_desorp_1st, k_desorp_2nd, theta_1st_i, 1-(theta_1st_i+theta_2nd_i))
##    print(theta_1st_i, theta_2nd_i, 1-(theta_1st_i+theta_2nd_i))
#    f0 = - k_diff * theta_1st_i + k_diff_rev * theta_2nd_i - k_desorp_1st * theta_1st_i
#    f1 = k_diff * theta_1st_i - k_diff_rev * theta_2nd_i - k_desorp_2nd * theta_2nd_i
#    return [f0, f1]
#
## slove the DEs
#soln = odeint(f, y0, t)
#theta_1st = soln[:, 0]
#theta_2nd = soln[:, 1]
##print(theta_1st)
##print(theta_2nd)
#
#plt.plot(t, theta_1st, '--', color='k')
#plt.plot(t, theta_2nd, '--', color='k')
#plt.plot(t, 1-(theta_1st+theta_2nd), '--', color='k')
#plt.xlabel('Temperature ,K', fontsize=20)
#plt.ylabel('percent', fontsize=20)
#plot_axis(25, 5, [375, 440], 0.5, 0.1, [0,1.1])
#
#r1 = util.Reactant(two_nh3_ADSORBENT, TS_two_one_over_one, 1.093)
#r2 = util.Reactant(one_over_one, TS_two_one_over_one, 0.213)
#soln = odeint(f, y0, t)
#theta_1st = soln[:, 0]
#theta_2nd = soln[:, 1]
#plt.plot(t, theta_1st, color='g')
#plt.plot(t, theta_2nd, color='b')
#plt.plot(t, 1-(theta_1st+theta_2nd), color='r')
##print(t, 1-(theta_1st+theta_2nd))


   

print("--- %s seconds ---" % (time.time() - start_time))


        
if __name__ == "__main__":
    pass
