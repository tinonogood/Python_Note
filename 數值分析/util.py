#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2016/10/24 Tino 3rd
# 2017/1/12 Tino 4th

import math
import numpy as np

# CONSTANTS
KB_J = 1.38064852 * math.pow(10, -23)  # K_BOLTZMANN_J, J/K
KB_EV = 8.6173324 * math.pow(10, -5)  # K_BOLTZMANN_EV. eV/K
H_J = 6.626070040 * math.pow(10, -34)  # H_PLANCK_J, J.sec
C = 299792458  # speed of light m/s

class DesorptionSystem:
    """"
    脫附環境
    system_a_length, system_b_length = surface邊長
    active_site = 吸附點數量
    beta = heating rate
    total_pressure = 反應器壓力
    temperature = 溫度
    """

    def __init__(self, system_a_length, system_b_length, active_site, beta, total_pressure, temperature):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure
        self.temperature = temperature
        pass

    def get_sys_parameter(self):
        return self.system_a_length, self.system_b_length, self.active_site, self.beta, self.total_pressure

    def set_sys_parameter(self, system_a_length, system_b_length, active_site, beta, total_pressure, temperature):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure
        self.temperature = temperature

class Gas(DesorptionSystem):
    """
    輸入吸附氣體之參數 ,
    mass = 氣體質量, kg;
    rot_const = rotation constant, 1/m;  rotational constants (http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
    sigma =  symmetry factor
    """

    def __init__(self, mass, rot_const_a, rot_const_b, rot_const_c, sigma):
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.sigma = sigma

    def get_gas_parameters(self):
        return self.mass, self.rot_const_a, self.rot_const_b, self.rot_const_c, self.sigma

    def set_gas_parameters(self, mass, rot_const_a, rot_const_b, rot_const_c, sigma):
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.sigma = sigma

    gas_parameters = property(get_gas_parameters, 'gas_parameters property')

    def get_translation_partition_function(self):
#        volume = KB_J * temperature / pressure
        volume = KB_J * self.temperature / self.total_pressure
        Lambda = np.sqrt((H_J ** 2) / (2 * np.pi * self.mass * KB_J * self.temperature))
        qt = volume / (Lambda ** 3)
        return qt

    def get_rotation_partition_function_nonlinear(self):
        qr_nonlinear = 1 / self.symmetry_factor * (((KB_J * self.temperature / (H_J * C)) ** 1.5) * np.sqrt(np.pi / (self.rotational_constant_A * self.rotational_constant_B * self.rotational_constant_C)))
        return qr_nonlinear
        
    def get_vibration_partition_function(self, hvs):
        qvs_at_T = []  # qv = partition_function
        for t in np.linspace(50, 500, 20):  # t= temperature
            partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (KB_EV * t))) for
                                  hv in hvs]
            qvs_at_T.append(np.prod(partition_function))
        return qvs_at_T

    def get_gas_molecular_partition_function(self, gas_molecular):
        qt = self.get_translation_partition_function(self.mass)
        qr = self.get_rotation_partition_function_nonlinear(self.sigma, self.rot_const_a, self.rot_const_b, self.rot_const_c)
        qv = self.get_vibration_partition_function(hvs_nh3_gas)
        gas_molecular_partition_functions_at_T = [i * j * k for i, j, k in zip(qt, qr, qv)]
        return gas_molecular_partition_functions_at_T
        
class Adsorbent(Gas):
    """
    吸附之氣體
    hvs = 頻率能量, meV
    
    """
    def __init__(self, hvs_gas, hv_surface, hv_adsorbent):
        self.hvs_gas = hvs_gas
        self.hv_surface = hv_surface
        self.hv_adsorbent = hv_adsorbent
    
    def get_adsorbent_parameters(self):
        return self.hvs_gas, self.hv_surface, self.hv_adsorbent
        
    def set_adsorbent_parameters(self, hvs_gas, hv_surface, hv_adsorbent):
        self.hvs_gas = hvs_gas
        self.hv_surface = hv_surface
        self.hv_adsorbent = hv_adsorbent
    
    adsorbent_parameters = property(get_adsorbent_parameters, 'gas_parameters property')


#==============================================================================
# PARAMETER OF NH3

GAS_MASS = 14.001
ROT_CONST_A = 610.85
ROT_CONST_B = 983.86
ROT_CONST_C = 983.91
SIGMA = 3
#==============================================================================
        
gas = Gas(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA)

#==============================================================================
# PARAMETERS OF SYS

LATTICE_A = 9.49569 * math.pow(10, -10)
LATTICE_B = 9.49569 * math.pow(10, -10)
ACTIVE_SITE = 6 / (LATTICE_A * LATTICE_B)
BETA = 3
TOTAL_PRESSURE = 2 * math.pow(10, -10)
TEMPERATURE = 273
#==============================================================================


gas.set_sys_parameter(LATTICE_A , LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
print(gas.get_translation_partition_function())

#==============================================================================
# adsorbent
HVS_GAS = [435.460659, 431.205986, 415.541526, 203.517923, 201.833141, 120.027150]
HVS_SURFACE = [88.368339, 88.038457, 87.125882, 86.891439, 86.012095, 85.717264, 84.604000, 84.485125, 80.133617, 78.343028, 78.182778, 77.126894, 77.083545, 75.596970, 74.995153, 73.286149, 72.656771, 72.404724, 71.432893, 70.936344, 70.790529, 70.453227, 67.365325, 66.677105, 66.406831, 65.753694, 65.705142, 65.576043, 65.536429, 63.216185, 60.042358, 59.381490, 58.340878, 58.221463, 57.734002, 57.099516, 45.387040, 41.341623, 36.067831, 35.938650, 35.208225, 34.854890, 33.974190, 33.852179, 33.707111, 33.567680, 33.417010, 32.220465, 30.220988, 30.193443, 30.142710, 29.926241, 29.424193, 29.337073, 27.569408, 27.520570, 27.229696, 26.418508, 26.173327, 26.150120, 24.281846, 23.701113, 22.331511, 21.859667, 21.819634, 20.963830, 20.772723, 20.448961, 20.408148, 20.328676, 20.133545, 19.630061, 19.320961, 19.090038, 19.048791, 18.901550, 18.770183, 18.096004, 18.062549, 17.972906, 17.286228, 17.251330, 17.072143, 16.264899, 14.848576, 14.764126, 14.694975, 8.844488, 8.600608, 3.810817]
HVS_ADSORBENT = [430.198631, 427.540569, 413.961910, 198.085064, 197.954985, 155.888486, 100.626456, 96.913905, 91.150507, 90.571449, 89.577129, 89.333135, 88.593270, 88.076295, 87.886616, 86.694058, 83.365306, 81.745121, 80.947879, 80.185729, 79.852830, 78.509102, 78.224377, 75.948489, 75.623308, 75.216938, 73.746860, 73.650604, 70.716749, 70.119930, 69.654502, 69.168927, 68.939090, 65.750349, 64.807776, 64.321902, 64.119328, 63.509015, 61.902849, 61.104554, 60.901952, 60.668654, 60.155707, 59.358441, 58.895983, 44.163961, 42.740979, 37.943257, 36.766113, 35.552710, 35.284977, 34.827630, 34.380060, 34.257256, 33.587371, 33.302352, 33.108034, 30.834472, 30.731268, 30.660547, 30.331024, 30.283868, 30.224699, 29.193081, 28.773556, 28.233508, 27.796885, 27.517773, 27.211584, 26.602082, 26.049863, 24.195551, 22.550748, 22.217728, 21.832439, 21.661550, 21.522873, 21.328779, 20.743273, 20.667872, 20.507662, 20.257865, 19.767438, 19.121150, 18.917779, 18.821477, 18.724233, 18.552834, 17.980644, 17.809680, 17.072836, 16.866863, 16.051825, 15.705389, 15.338813, 14.747400]
#==============================================================================

        
    
    
if __name__ == "__main__":
    pass
