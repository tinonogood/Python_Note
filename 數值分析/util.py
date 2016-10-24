#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2016/10/1 Tino 1st
# 2016/10/14 Tino 2nd

import math

class Gas:
    """
    輸入吸附氣體之參數 ,
    mass = 氣體質量, kg;
    rot_const = rotation constant, 1/m;  rotational constants ( http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
    sigma =  symmetry factor

    """

    # def __init__(self, mass=2.99 * math.pow(10,-26), rot_const_a=921.21, rot_const_b=1391.9, rot_const_c=2724.1, sigma=2):
    def __init__(self, mass, rot_const_a, rot_const_b, rot_const_c, sigma):
        """default: Water, H2O"""
        # self.mass = 2.99 * math.pow(10, -26)
        # self.rot_const_a = 921.21
        # self.rot_const_b = 1391.9
        # self.rot_const_c = 2724.1
        # self.sigma = 2
        self.mass = mass
        self.rot_const_a = rot_const_a
        self.rot_const_b = rot_const_b
        self.rot_const_c = rot_const_c
        self.sigma = sigma

    @property
    def mass(self):
        return self.mass

    # def rot_const_a(self):
    #     return self.rot_const_a
    #
    # def rot_const_b(self):
    #     return self.rot_const_b
    #
    # def rot_const_c(self):
    #     return self.rot_const_c
    #
    # def sigma(self):
    #     return self.sigma

    @mass.setter
    def mass(self, mass):
        self.mass = mass


NH3 = Gas(2.82 * math.pow(10, -26), 610.85, 983.86, 983.91, 3)

print(NH3.mass)
