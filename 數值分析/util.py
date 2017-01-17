#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2017/1/12 Tino 4th
# 2017/1/17 Tino 5th

import math
import numpy as np
import matplotlib.pyplot as plt

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
    hvs = vibration energy
    """

    def __init__(self, mass, rot_const_a, rot_const_b, rot_const_c, symmetry_factor, hvs):
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.symmetry_factor = symmetry_factor
        self.hvs = hvs

    def get_gas_parameters(self):
        return self.mass, self.rot_const_a, self.rot_const_b, self.rot_const_c, self.symmetry_factor, self.hvs

    def set_gas_parameters(self, mass, rot_const_a, rot_const_b, rot_const_c, symmetry_factor, hvs):
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.symmetry_factor = symmetry_factor
        self.hvs = hvs


    gas_parameters = property(get_gas_parameters, 'gas_parameters property')

    def get_translation_partition_function(self):
#        volume = KB_J * temperature / pressure
        volume = KB_J * self.temperature / self.total_pressure
        Lambda = np.sqrt((H_J ** 2) / (2 * np.pi * self.mass * KB_J * self.temperature))
        qt = volume / (Lambda ** 3)
        return qt

    def get_rotation_partition_function_nonlinear(self):
        qr_nonlinear = 1 / self.symmetry_factor * (((KB_J * self.temperature / (H_J * C)) ** 1.5) * np.sqrt(np.pi / (self.rot_const_a * self.rot_const_b * self.rot_const_c)))
        return qr_nonlinear
        
    def get_vibration_partition_function(self):
        partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (KB_EV * self.temperature))) for
                              hv in self.hvs]
        qvs = np.prod(partition_function)
        return qvs
        

    def get_gas_molecular_partition_function(self):
        qt = self.get_translation_partition_function()
        qr = self.get_rotation_partition_function_nonlinear()
        qv = self.get_vibration_partition_function()
#        gas_molecular_partition_functions_at_T = [i * j * k for i, j, k in zip(qt, qr, qv)]
        gas_molecular_partition_functions_at_T = qt * qr * qv
        return gas_molecular_partition_functions_at_T
        
class Adsorbent(Gas):
    """
    吸附之氣體
    hvs = 頻率能量, meV
    desorption_energy = 脫付能
    """
    def __init__(self, hv_surface, hv_adsorbent): #, adsorbent):
        self.hv_surface = hv_surface
        self.hv_adsorbent = hv_adsorbent
#        self.desorption_energy = desorption_energy
        
    
    def get_adsorbent_parameters(self):
        return self.hv_surface, self.hv_adsorbent, self.desorption_energy
        
    def set_adsorbent_parameters(self, hv_surface, hv_adsorbent):#, desorption_energy):
        self.hv_surface = hv_surface
        self.hv_adsorbent = hv_adsorbent
#        self.desorption_energy = desorption_energy
    
    adsorbent_parameters = property(get_adsorbent_parameters, 'gas_parameters property')
    
    def get_rate_const_adsorption(self):
        rate_const_adsorption = self.total_pressure / (np.sqrt(2 * np.pi * self.mass * KB_J * self.temperature) * self.active_site)
        return rate_const_adsorption
        
    def get_adsorbent_vibration_partition_function(self, hvs):
        partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (KB_EV * self.temperature))) for
                              hv in self.hvs]
        qvs = np.prod(partition_function)
        return qvs
        
    def get_rate_partition_function_term(self):
        qa = self.get_gas_molecular_partition_function()
        q_star = self.get_adsorbent_vibration_partition_function(self.hv_surface)
        qa_star = self.get_adsorbent_vibration_partition_function(self.hv_adsorbent)
        partition_function_term = qa * q_star / qa_star
        return partition_function_term
        
    def get_v(self):
        v = self.get_rate_partition_function_term() * self.get_rate_const_adsorption()
        return v

    def get_energy_distribution(self, E):
        A = self.get_v()
        theta = math.exp(-1 * KB_EV * A * math.pow(self.temperature, 2) * math.exp(-1 * E / (KB_EV * self.temperature))/(self.beta * E * np.sqrt(1 + 2 * KB_EV * self.temperature)))
        f = A * math.exp(-1 * E / (KB_EV * self.temperature)) * theta
        return f
        
#==============================================================================
# PARAMETERS OF SYS

LATTICE_A = 9.49569 * math.pow(10, -10)
LATTICE_B = 9.49569 * math.pow(10, -10)
ACTIVE_SITE = 6 / (LATTICE_A * LATTICE_B)
BETA = 3
TOTAL_PRESSURE = 2 * math.pow(10, -10)
TEMPERATURE = 700
#==============================================================================
    
#==============================================================================
# PARAMETER OF NH3

GAS_MASS = 14.001
ROT_CONST_A = 610.85
ROT_CONST_B = 983.86
ROT_CONST_C = 983.91
SIGMA = 3
HVS_GAS = [435.460659, 431.205986, 415.541526, 203.517923, 201.833141, 120.027150]
#==============================================================================

##==============================================================================
## adsorbent 1xnh3
#
#HVS_SURFACE = [88.368339, 88.038457, 87.125882, 86.891439, 86.012095, 85.717264, 84.604000, 84.485125, 80.133617, 78.343028, 78.182778, 77.126894, 77.083545, 75.596970, 74.995153, 73.286149, 72.656771, 72.404724, 71.432893, 70.936344, 70.790529, 70.453227, 67.365325, 66.677105, 66.406831, 65.753694, 65.705142, 65.576043, 65.536429, 63.216185, 60.042358, 59.381490, 58.340878, 58.221463, 57.734002, 57.099516, 45.387040, 41.341623, 36.067831, 35.938650, 35.208225, 34.854890, 33.974190, 33.852179, 33.707111, 33.567680, 33.417010, 32.220465, 30.220988, 30.193443, 30.142710, 29.926241, 29.424193, 29.337073, 27.569408, 27.520570, 27.229696, 26.418508, 26.173327, 26.150120, 24.281846, 23.701113, 22.331511, 21.859667, 21.819634, 20.963830, 20.772723, 20.448961, 20.408148, 20.328676, 20.133545, 19.630061, 19.320961, 19.090038, 19.048791, 18.901550, 18.770183, 18.096004, 18.062549, 17.972906, 17.286228, 17.251330, 17.072143, 16.264899, 14.848576, 14.764126, 14.694975, 8.844488, 8.600608, 3.810817]
#HVS_ADSORBENT = [430.198631, 427.540569, 413.961910, 198.085064, 197.954985, 155.888486, 100.626456, 96.913905, 91.150507, 90.571449, 89.577129, 89.333135, 88.593270, 88.076295, 87.886616, 86.694058, 83.365306, 81.745121, 80.947879, 80.185729, 79.852830, 78.509102, 78.224377, 75.948489, 75.623308, 75.216938, 73.746860, 73.650604, 70.716749, 70.119930, 69.654502, 69.168927, 68.939090, 65.750349, 64.807776, 64.321902, 64.119328, 63.509015, 61.902849, 61.104554, 60.901952, 60.668654, 60.155707, 59.358441, 58.895983, 44.163961, 42.740979, 37.943257, 36.766113, 35.552710, 35.284977, 34.827630, 34.380060, 34.257256, 33.587371, 33.302352, 33.108034, 30.834472, 30.731268, 30.660547, 30.331024, 30.283868, 30.224699, 29.193081, 28.773556, 28.233508, 27.796885, 27.517773, 27.211584, 26.602082, 26.049863, 24.195551, 22.550748, 22.217728, 21.832439, 21.661550, 21.522873, 21.328779, 20.743273, 20.667872, 20.507662, 20.257865, 19.767438, 19.121150, 18.917779, 18.821477, 18.724233, 18.552834, 17.980644, 17.809680, 17.072836, 16.866863, 16.051825, 15.705389, 15.338813, 14.747400]
##==============================================================================

#==============================================================================
# adsorbent 2xnh3

HVS_SURFACE = [430.198631, 427.540569, 413.961910, 198.085064, 197.954985, 155.888486, 100.626456, 96.913905, 91.150507, 90.571449, 89.577129, 89.333135, 88.593270, 88.076295, 87.886616, 86.694058, 83.365306, 81.745121, 80.947879, 80.185729, 79.852830, 78.509102, 78.224377, 75.948489, 75.623308, 75.216938, 73.746860, 73.650604, 70.716749, 70.119930, 69.654502, 69.168927, 68.939090, 65.750349, 64.807776, 64.321902, 64.119328, 63.509015, 61.902849, 61.104554, 60.901952, 60.668654, 60.155707, 59.358441, 58.895983, 44.163961, 42.740979, 37.943257, 36.766113, 35.552710, 35.284977, 34.827630, 34.380060, 34.257256, 33.587371, 33.302352, 33.108034, 30.834472, 30.731268, 30.660547, 30.331024, 30.283868, 30.224699, 29.193081, 28.773556, 28.233508, 27.796885, 27.517773, 27.211584, 26.602082, 26.049863, 24.195551, 22.550748, 22.217728, 21.832439, 21.661550, 21.522873, 21.328779, 20.743273, 20.667872, 20.507662, 20.257865, 19.767438, 19.121150, 18.917779, 18.821477, 18.724233, 18.552834, 17.980644, 17.809680, 17.072836, 16.866863, 16.051825, 15.705389, 15.338813, 14.747400]
HVS_ADSORBENT = [424.125172, 423.849717, 420.595920, 419.403011, 410.808280, 405.796797, 200.394007, 199.456838, 199.033067, 198.587343, 157.676765, 155.343118, 107.766780, 102.077340, 100.129117, 99.457258, 89.161474, 88.785527, 87.924722, 87.561085, 86.573713, 86.383606, 85.801908, 85.655321, 81.868313, 79.400476, 79.191369, 78.312681, 77.940721, 77.281795, 77.080852, 74.568861, 74.157690, 73.548951, 72.704997, 72.368210, 70.624597, 69.999068, 69.224256, 67.960474, 67.319906, 65.274200, 65.197919, 64.764850, 64.505284, 64.288516, 61.433483, 60.961585, 60.692938, 60.199048, 59.864068, 59.473005, 58.830080, 58.539293, 44.672150, 43.767245, 39.090709, 38.339463, 36.558748, 36.146206, 36.026258, 35.695262, 35.472710, 35.007167, 34.594195, 33.993084, 33.264194, 30.937056, 30.909414, 30.723105, 30.570799, 30.219125, 30.022164, 29.945579, 29.074837, 28.866068, 28.836132, 28.575930, 28.134741, 27.892153, 27.633395, 26.837740, 24.615636, 24.092543, 23.078251, 22.608815, 22.301980, 22.102627, 21.934406, 21.521768, 21.330050, 21.174876, 20.590801, 20.347330, 19.927018, 19.692588, 19.582158, 19.292423, 19.203925, 18.711171, 18.404162, 18.315183, 18.035711, 17.909694, 17.207706, 16.780799, 16.550679, 16.327247]
#==============================================================================

adsorbent = Adsorbent(HVS_SURFACE, HVS_ADSORBENT)
adsorbent.set_sys_parameter(LATTICE_A, LATTICE_B, ACTIVE_SITE, BETA, TOTAL_PRESSURE, TEMPERATURE)
adsorbent.set_gas_parameters(GAS_MASS, ROT_CONST_A, ROT_CONST_B, ROT_CONST_C, SIGMA, HVS_GAS)
#adsorbent.set_adsorbent_parameters(HVS_SURFACE, HVS_ADSORBENT)


E = np.linspace(6.1, 6.8, 256, endpoint=True)
f = np.vectorize(adsorbent.get_energy_distribution)

plt.plot(E, f(E))
plt.show()        
    
if __name__ == "__main__":
    pass
