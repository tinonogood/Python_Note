#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 17:29:51 2017

@author: tino
"""

import unittest
from util import *

import math
import numpy as np


class TestUtil(unittest.TestCase):
    
    def test_get_rate_const_adsorption(self):
        system_a_length = 1
        system_b_length = 2
        active_site = 3
        beta = 4
        total_pressure = 2 * math.pow(10, -10)
        temperature = 273
        
        
        
if __name__ == '__main__':
    unittest.main()