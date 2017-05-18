#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2017/1/12 Tino 4th
# 2017/1/17 Tino 5th

import math
import numpy as np
from sympy import solve, Symbol, exp
from scipy import constants as C

# CONSTANTS
KB_EV = C.k * C.physical_constants["joule-electron volt relationship"][0]


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
        self.total_pressure = total_pressure
        self.beta = beta
        self.temperature = temperature
        pass

    def get_sys_parameters(self):
        return self.system_a_length, self.system_b_length, self.active_site, self.beta, self.total_pressure, self.total_pressure

    def set_sys_parameters(self, system_a_length, system_b_length, active_site, beta, total_pressure, temperature):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure
        self.temperature = temperature
        
    sys_parameters = property(get_sys_parameters, 'sys_parameters property')

class Gas(DesorptionSystem):
    """
    輸入吸附氣體之參數 ,
    mass = 氣體質量, kg;
    rot_const = rotation constant, 1/m;  rotational constants (http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
    sigma =  symmetry factor
    hvs = vibration energy
    """

    def __init__(self, mass, rot_const_a, rot_const_b, rot_const_c, symmetry_factor, hvs):
        if mass > math.pow(10, -24) or mass < 1.6 * math.pow(10, -27):
            print("mass unit is kg?")
        if rot_const_a > 5000 or rot_const_a < 1:
            print("rot_const_a unit is 1/m?")
        if rot_const_b > 5000 or rot_const_b < 1:
            print("rot_const_b unit is 1/m?")
        if rot_const_c > 5000 or rot_const_c < 1:
            print("rot_const_c unit is 1/m?")
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.symmetry_factor = symmetry_factor
        for hv in hvs:
            if hvs > 10000 or hvs < 1:
                print("hv unit is meV?")
        self.hvs = hvs

    def get_gas_parameters(self):
        return self.mass, self.rot_const_a, self.rot_const_b, self.rot_const_c, self.symmetry_factor, self.hvs

    def set_gas_parameters(self, mass, rot_const_a, rot_const_b, rot_const_c, symmetry_factor, hvs):
        if mass > math.pow(10, -24) or mass < 1.6 * math.pow(10, -27):
            print("mass unit is kg?")
        if rot_const_a > 5000 or rot_const_a < 1:
            print("rot_const_a unit is 1/m?")
        if rot_const_b > 5000 or rot_const_b < 1:
            print("rot_const_b unit is 1/m?")
        if rot_const_c > 5000 or rot_const_c < 1:
            print("rot_const_c unit is 1/m?")
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.symmetry_factor = symmetry_factor
        for hv in hvs:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hvs = hvs


    gas_parameters = property(get_gas_parameters, 'gas_parameters property')

    def get_translation_partition_function(self):
        volume = C.k * self.temperature / self.total_pressure
        Lambda = np.sqrt((C.h ** 2) / (2 * np.pi * self.mass * C.k * self.temperature))
        qt = volume / (Lambda ** 3)
        return qt

    def get_rotation_partition_function_nonlinear(self):
        qr_nonlinear = 1 / self.symmetry_factor * (((C.k * self.temperature / (C.h * C.c)) ** 1.5) * np.sqrt(np.pi / (self.rot_const_a * self.rot_const_b * self.rot_const_c)))
        return qr_nonlinear
        
    def get_vibration_partition_function(self):
        partition_function = [1.0 / (1.0 - np.exp(-1 * hv * math.pow(10, -3) / (KB_EV * self.temperature))) for
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
    def __init__(self, hv_surface, hv_adsorbent, desorption_energy): #, adsorbent):
        for hv in hv_surface:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_surface = hv_surface
        for hv in hv_adsorbent:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_adsorbent = hv_adsorbent
        self.desorption_energy = 9.9
        self.E_T_list = []
        
    
    def get_adsorbent_parameters(self):
        return self.hv_surface, self.hv_adsorbent, self.desorption_energy, self.E_T_list
        
    def set_adsorbent_parameters(self, hv_surface, hv_adsorbent, desorption_energy, E_T_list):#, desorption_energy):
        for hv in hv_surface:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_surface = hv_surface
        for hv in hv_adsorbent:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_adsorbent = hv_adsorbent
        self.desorption_energy = desorption_energy
        self.E_T_list = E_T_list
    
    adsorbent_parameters = property(get_adsorbent_parameters, 'gas_parameters property')
    
    def get_rate_const_adsorption(self):
        rate_const_adsorption = self.total_pressure / (np.sqrt(2 * np.pi * self.mass * C.k * self.temperature) * self.active_site)
        return rate_const_adsorption
        
    def get_adsorbent_vibration_partition_function(self, hvs):
        partition_function = [1.0 / (1.0 - np.exp(-1 * hv * math.pow(10, -3) / (KB_EV * self.temperature))) for hv in hvs]
        qvs = np.prod(partition_function)
        return qvs
        
    def get_rate_partition_function_term(self):
        qa = self.get_gas_molecular_partition_function()
        q_star = self.get_adsorbent_vibration_partition_function(self.hv_surface)
        qa_star = self.get_adsorbent_vibration_partition_function(self.hv_adsorbent)
        partition_function_term = qa * q_star / qa_star
        return partition_function_term
        
    def get_v(self, temperature):
        self.temperature = temperature
        v = self.get_rate_partition_function_term() * self.get_rate_const_adsorption()
        return v
        
#==============================================================================
#       P.J.Barrie, Phys. Chem. Chem. Phys., 2008, 10, 1688-96            
#==============================================================================

    def get_theta_distribution(self, E):
        A = self.get_v(self.temperature)
        theta = np.exp(-1 * KB_EV * A * math.pow(self.temperature, 2) * np.exp(-1 * E / (KB_EV * self.temperature))/(self.beta * E * np.sqrt(1 + 2 * KB_EV * self.temperature / E)))
        return theta

    def get_f_energy_distribution(self, E):
        A = self.get_v(self.temperature)
        theta = np.exp(-1 * KB_EV * A * math.pow(self.temperature, 2) * np.exp(-1 * E / (KB_EV * self.temperature))/(self.beta * E * np.sqrt(1 + 2 * KB_EV * self.temperature / E)))
#        theta = float(math.exp(-1 * KB_EV * A * math.pow(self.temperature, 2) * math.exp(-1 * E / (KB_EV * self.temperature))/(self.beta * E * np.sqrt(1 + 2 * KB_EV * self.temperature))))
        f = A * np.exp(-1 * E / (KB_EV * self.temperature)) * theta
        return f
        
    def get_E_star(self):
        x = Symbol('x', positive=True) # x = E_star / RT - 0.368 from eqn(18)
        A = self.get_v(self.temperature)
        t = self.temperature
        [c] = solve(x * exp(x) - (A * t) / self.beta, x)
        E_star = (c + 0.368) * KB_EV * self.temperature 
        return E_star
        
    # 精細度待處理
    def get_E_t_list(self):
        self.temperature = 60
        E = 0
        E_list = []
        t_list = []
        while self.temperature < 1500:
            E_star = self.get_E_star()
            if E_star - E > 0.01:
                E_list.append(round(E_star, 4)) # 回傳小數四位
                t_list.append(self.temperature)
                E_star = E
            self.temperature += 40
        E_T_dict = dict(zip(E_list,t_list))
#        self.E_T_dict = E_T_dict
        self.E_T_list = [(k, E_T_dict[k]) for k in sorted(E_T_dict.keys())]
        return self.E_T_list
                        
    def get_T(self, E):
        for i in range(len(self.E_T_list) - 1):
            (x,y) = self.E_T_list[i]
            if x >= E:
                if i == 0:
                    (x_plus, y_plus) = self.E_T_list[i+1]
                    T = y - (y_plus - y) / (x_plus - x) * (x - E)
                    return round(T, 4)
                else:
                    (x_mi, y_mi) = self.E_T_list[i-1]
                    T =  y - (y - y_mi) / (x - x_mi) * (x - E)
                    return round(T, 4)
        i_max = len(self.E_T_list) - 1
        (x,y) = self.E_T_list[i_max]
        if x < E:
            (x_mi, y_mi) = self.E_T_list[i-1]
            T =  y - (y - y_mi) / (x - x_mi) * (x - E)
            return round(T, 4)

class Reactant(Adsorbent):
    """
    反應之吸附物
    hvs = 頻率能量, meV
    reaction_barrier = 反應能
    """
    def __init__(self, hv_IS, hv_TS, barrier): #, adsorbent):
        for hv in hv_IS:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_IS = hv_IS
        for hv in hv_TS:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_TS = hv_TS
        self.barrier = 0
        
    
    def get_reactant_parameters(self):
        return self.hv_surface, self.hv_IS, self.hv_TS, self.barrier
        
    def set_reactant_parameters(self, hv_IS, hv_TS, barrier):#, desorption_energy):
        for hv in hv_IS:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_IS = hv_IS
        for hv in hv_TS:
            if hv > 10000 or hv < 1:
                print("hv unit is meV?")
        self.hv_TS = hv_TS
        if barrier > 6:
            print("barrier unit is eV?")
        self.barrier = 0
    
    reactant_parameters = property(get_reactant_parameters, 'gas_parameters property')   

#==============================================================================
#       TS theory            
#==============================================================================            
    def get_rate_constant(self, t):
        self.temperature = t
        q_IS = self.get_adsorbent_vibration_partition_function(self.hv_IS)
        q_TS = self.get_adsorbent_vibration_partition_function(self.hv_TS)
        rate_constant = (C.k * self.temperature / C.h) * (q_TS/q_IS) * np.exp(- self.barrier / (KB_EV * self.temperature))
        return rate_constant
            
if __name__ == "__main__":
    pass
