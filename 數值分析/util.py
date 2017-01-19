#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2017/1/12 Tino 4th
# 2017/1/17 Tino 5th

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
                              hv in hvs]
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
                
    
if __name__ == "__main__":
    pass
