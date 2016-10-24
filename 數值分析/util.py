#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2016/10/24 Tino 3rd

import math


class Gas:
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

    def get_sys_parameter(self):
        return self.system_a_length, self.system_b_length, self.active_site, self.beta, self.total_pressure

    def set_sys_parameter(self):
        self.system_a_length = system_a_length
        self.system_b_length = system_b_length
        self.active_site = active_site
        self.beta = beta
        self.total_pressure = total_pressure


class Adsorbent:
    """
    
    """