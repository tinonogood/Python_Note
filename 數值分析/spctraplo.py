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
HVS_GAS = [442.215649, 439.716700, 413.765200, 201.489356, 201.110381, 121.108217] # meV
#==============================================================================

#==============================================================================
# 1xnh3@RuO2 frequency (meV)
SURFACE = [87.451826, 80.106578, 79.975548, 77.307325, 75.540294, 74.284057, 73.507563, 70.909798, 69.364341, 66.736189, 65.459628, 59.846945, 59.762127, 58.402916, 56.389826, 50.908548, 47.039677, 43.783655, 42.120371, 38.468662, 36.719300, 35.521740, 34.658919, 33.950476, 31.236358, 29.144139, 28.116400, 27.156497, 26.432385, 25.117658, 18.864535, 17.967444, 17.666863, 17.296124, 8.732769, 6.099266]
ADSORBENT = [435.329134, 427.225735, 393.764737, 200.334825, 197.452612, 146.463008, 93.170142, 86.964056, 85.308324, 80.515343, 79.734141, 78.642741, 75.714881, 74.567728, 74.054587, 70.639176, 69.233592, 65.625511, 64.551719, 60.983900, 58.671394, 58.508002, 55.839249, 52.028901, 51.334941, 48.559752, 45.269616, 42.069942, 41.148117, 38.112503, 37.125374, 35.426930, 35.318497, 34.687400, 31.966553, 31.623575, 28.120155, 27.815018, 27.393464, 23.636484, 22.559864, 22.060609, 19.892524, 17.800949, 16.519593, 14.707077, 7.769280, 5.539398]

#==============================================================================

adsorbent = util.Adsorbent(SURFACE, ADSORBENT, 1.4623)
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
    for T in np.linspace(init_T, final_T, (final_T - init_T)/3 + 1, endpoint=True):
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
    plot_axis(100, 10, [init_T, final_T], 0.1, 0.02, [0,0.3])
    plt.show()
    

#==============================================================================
# 2to1_1xnh3@RuO2 frequency (meV)
one_nh3_ADSORBENT = [435.329134, 427.225735, 393.764737, 200.334825, 197.452612, 146.463008, 93.170142, 86.964056, 85.308324, 80.515343, 79.734141, 78.642741, 75.714881, 74.567728, 74.054587, 70.639176, 69.233592, 65.625511, 64.551719, 60.983900, 58.671394, 58.508002, 55.839249, 52.028901, 51.334941, 48.559752, 45.269616, 42.069942, 41.148117, 38.112503, 37.125374, 35.426930, 35.318497, 34.687400, 31.966553, 31.623575, 28.120155, 27.815018, 27.393464, 23.636484, 22.559864, 22.060609, 19.892524, 17.800949, 16.519593, 14.707077, 7.769280, 5.539398]
two_nh3_ADSORBENT = [431.960390, 430.160295, 429.133200, 428.386038, 414.069073, 408.124381, 209.590403, 204.287257, 200.770940, 200.676112, 146.591638, 136.878688, 89.010762, 84.367619, 82.403615, 82.217007, 80.755768, 79.775770, 77.449552, 76.494849, 72.723029, 70.929992, 69.100484, 68.476778, 66.627597, 63.893613, 62.048640, 61.758935, 56.997853, 53.504948, 53.303789, 51.219028, 47.355821, 46.427750, 45.069584, 42.834436, 42.578431, 41.402533, 40.392123, 39.208337, 38.361648, 36.796390, 36.058200, 33.688945, 33.407037, 31.939556, 31.504297, 27.823928, 27.517196, 25.847573, 23.920002, 22.754945, 21.326681, 20.631129, 19.285686, 16.542322, 15.377830, 13.548747, 8.864076, 6.811704]
one_over_one = [430.261462, 423.461759, 420.728744, 411.234202, 406.969028, 389.932302, 208.910728, 205.913021, 204.254089, 201.339644, 157.729026, 141.126163, 100.995957, 90.680370, 88.326264, 81.679925, 80.548951, 77.896540, 74.642817, 73.433380, 70.186208, 67.836017, 67.163859, 62.834858, 61.582670, 61.345909, 57.176771, 55.331660, 53.449043, 52.760421, 50.243820, 46.932347, 46.280561, 45.788876, 45.145490, 40.872852, 38.884738, 38.120144, 37.012330, 36.376139, 34.859078, 34.082528, 33.809868, 30.735909, 27.910674, 26.930452, 25.663632, 25.516415, 24.676988, 21.435896, 20.374634, 19.597943, 19.398040, 17.806246, 16.210188, 14.462278, 13.564712, 9.411448, 6.399291, 3.778888]
TS_two_one_over_one = [431.508063, 428.230746, 424.227159, 422.398178, 413.548617, 408.079814, 206.430620, 203.994245, 201.969431, 198.289225, 150.833102, 141.443991, 92.426497, 88.539729, 87.652288, 81.578912, 80.083901, 77.579146, 74.832042, 74.095204, 69.311758, 67.247960, 66.304572, 63.769508, 60.731376, 59.729874, 57.289399, 53.927452, 53.040714, 49.167444, 46.201347, 45.299452, 44.924003, 43.731837, 41.335927, 38.631204, 38.446768, 37.930912, 35.951265, 35.751263, 34.066407, 33.250938, 31.938148, 28.030904, 26.419255, 24.944056, 24.460265, 21.793249, 20.966108, 18.554686, 17.814053, 17.655456, 16.151337, 15.351500, 10.970940, 7.394059, 6.583119, 4.341430, 3.410195]
#==============================================================================


a1 = util.Adsorbent(one_nh3_ADSORBENT, two_nh3_ADSORBENT, 0.7633)
r1 = util.Reactant(two_nh3_ADSORBENT, TS_two_one_over_one, 0.329)
r2 = util.Reactant(one_over_one, TS_two_one_over_one, 0.085)
a2 = util.Adsorbent(one_nh3_ADSORBENT, one_over_one, 0.5193)

# try to improv
#==============================================================================
a1.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
a1.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
r1.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
r1.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
r2.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
r2.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
a2.set_sys_parameters(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
a2.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
#==============================================================================

theta_1st_0 = 1. # 1st layer population initial
theta_2nd_0 = 0.00000001  # 2nd layer population initial
gas_phase = 0.0  # gas  phase 
y0 = [theta_1st_0, theta_2nd_0]
#t = np.linspace(0, 50.0, 1000) # time grid
#T0 = 150
t = np.linspace(120, 210.0, 31)


# solve the mk model dy/dt = f(y, t) & y=theta
def f(y, t):
    theta_1st_i = y[0]
    theta_2nd_i = y[1]
    # the rate constant
#    k_diff = (C.k * (T0 + BETA * t) / C.h) * () * np.exp(- r1.barrier / (KB_EV * (T0 + BETA * t)))
#    k_diff_rev = (C.k * (T0 + BETA * t) / C.h) * np.exp(- r2.barrier / (KB_EV * (T0 + BETA * t)))
    k_diff = r1.get_rate_constant(t)
    k_diff_rev = r2.get_rate_constant(t)
    k_desorp_1st = a1.get_v(t) * np.exp(- 0.7633 / (KB_EV * t)) 
    k_desorp_2nd = a2.get_v(t) * np.exp(- 0.5193 / (KB_EV * t))
    # the model equations
    f0 = - k_diff * theta_1st_i + k_diff_rev * theta_2nd_i - k_desorp_1st * theta_1st_i
    f1 = k_diff * theta_1st_i - k_diff_rev * theta_2nd_i - k_desorp_2nd * theta_2nd_i
    return [f0, f1]

# slove the DEs
soln = odeint(f, y0, t)
theta_1st = soln[:, 0]
theta_2nd = soln[:, 1]
#print(theta_1st)
#print(theta_2nd)

plt.plot(t, theta_1st, color='b')
plt.plot(t, theta_2nd, color='b')
#plt.plot(t, 1-(theta_1st+theta_2nd), color='r')
plt.xlabel('Temperature ,K', fontsize=20)
plt.ylabel('rate', fontsize=20)
plot_axis(100, 10, [50, 250], 0.3, 0.1, [0,1.1])
print(t, 1-(theta_1st+theta_2nd))
   

print("--- %s seconds ---" % (time.time() - start_time))


        
if __name__ == "__main__":
    pass
