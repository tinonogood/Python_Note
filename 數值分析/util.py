#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2016/10/24 Tino 3rd

import math
import numpy as np

class DesorptionSystem:
    """"
    脫附環境
    system_a_length, system_b_length = surface邊長
    active_site = 吸附點數量
    beta = heating rate
     total_pressure = 反應器壓力
    """

    def __init__(self, system_a_length, system_b_length, active_site, beta, total_pressure):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure
        pass

    def get_sys_parameter(self):
        return self.system_a_length, self.system_b_length, self.active_site, self.beta, self.total_pressure

    def set_sys_parameter(self):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure

class Gas(DesorptionSystem):
    """
    輸入吸附氣體之參數 ,
    mass = 氣體質量, kg;
    rot_const = rotation constant, 1/m;  rotational constants ( http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
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

# -----------------------------------------------------------------------------------------------------------------------
    def get_translation_partition_function(self, mass, temperature, pressure):
        volume = KB_J * temperature / pressure
        Lambda = np.sqrt((H_J ** 2) / (2 * np.pi * mass * KB_J * temperature))
        qt = volume / (Lambda ** 3)
        return qt

    def get_rotation_partition_function_nonlinear(self, symmetry_factor, rotational_constant_A, rotational_constant_B,
                                                  rotational_constant_C):
        qrs_nonlinear_at_T = []  # qr = translation_rotation_functions
        t = 273  # t= temperature
        qr_nonlinear = 1 / symmetry_factor * (((KB_J * t / (H_J * 3 * math.pow(10, 8))) ** 1.5) * np.sqrt(
            np.pi / (rotational_constant_A * rotational_constant_B * rotational_constant_C))
        qrs_nonlinear_at_T.append(qr_nonlinear)
        return qrs_nonlinear_at_T

    def get_vibration_partition_function(self, hvs):
        qvs_at_T = []  # qv = partition_function
        for t in np.linspace(50, 500, 20):  # t= temperature
            partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (KB_EV * t))) for
                                  hv in hvs]
            qvs_at_T.append(np.prod(partition_function))
        return qvs_at_T

    def get_gas_molecular_partition_function(self, gas_molecular):
        # qt = get_translation_partition_function(M_NH3)
        qr = get_rotation_partition_function_nonlinear(SIGMA_NH3, ROT_CONST_A_NH3, ROT_CONST_B_NH3, ROT_CONST_C_NH3)
        qv = get_vibration_partition_function(hvs_nh3_gas)
        gas_molecular_partition_functions_at_T = [i * j * k for i, j, k in zip(qt, qr, qv)]
        return gas_molecular_partition_functions_at_T
#-----------------------------------------------------------------------------------------------------------------------


class Adsorbent(Gas, DesorptionSystem):
    """
    吸附之氣體
    """

if __name__ == "__main__":
    pass