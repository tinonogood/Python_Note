#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

#2016/10/1 tino 1st

import numpy as np
import math

# CONSTANTS
MASS_OF_NH3_KILOGRAM_PER_MOLE = (14.001 + 3 * 1.000) * 0.001  # kg/mole
MASS_OF_NH3 = MASS_OF_NH3_KILOGRAM_PER_MOLE / (6 * math.pow(10, 23))  # kg
K_BOLTZMANN_J = 1.38064852 * math.pow(10, -23)  # J/K
K_BOLTZMANN_EV = 8.6173324 * math.pow(10, -5)  # eV/K
LATTICE_A = 9.49569  # Angstum
LATTICE_B = 12.8097  # Angstum
CONC_OF_ACTIVE_SITE = 6 / ( LATTICE_A * LATTICE_B * math.pow(10, -20))  # number of site/m2
BETA_HEATING_RATE = 3  # K/s
H_PLANK_J = 6.626070040 * math.pow(10, -34)  # J.sec
# Rotational constants ( http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
ROT_CONST_A_NH3 = 610.85  # 1/m
ROT_CONST_B_NH3 = 983.86  # 1/m
ROT_CONST_C_NH3 = 983.91  # 1/m
ROT_CONST_A_H2O = 921.21  # 1/m
ROT_CONST_B_H2O = 1391.9  # 1/m
ROT_CONST_C_H2O = 2724.1  # 1/m
SYM_FACTOR_NH3 = 3
SYM_FACTOR_H2O = 2


# variables
time = 0.00
# temperture = 100 + BETA_HEATING_RATE * time
total_pressure = 2 * math.pow(10, -10)  # Pa, （m·kg·s-2）/m^2

# hvs_vib
hvs_surface = []
hvs_h2o_gas = []
hvs_1h2o = []
hvs_2h2o = []
hvs_3h2o = []
hvs_4h2o = []
hvs_5h2o = []
hvs_6h2o = []
hvs_7h2o = []
hvs_8h2o = []
hvs_9h2o = []
hvs_10h2o = []
hvs_11h2o = []
hvs_12h2o = []
hvs_13h2o = []
hvs_nh3_gas = []
hvs_1nh3 = []
hvs_2nh3 = []
hvs_3nh3 = []
hvs_4nh3 = []
hvs_5nh3 = []
hvs_6nh3 = []
hvs_7nh3 = []
hvs_8nh3 = [438.775021, 437.949482, 436.762264, 434.440552, 434.224810, 433.305892, 432.869853, 430.898249, 429.174646, 424.632318, 417.025527, 416.210198, 415.160595, 414.916849, 405.276550, 400.388275, 398.213399, 397.295026, 384.416548, 378.127641, 375.614944, 370.993282, 368.501827, 359.582767, 207.444471, 207.409741, 205.280089, 204.153621, 202.911506, 201.748168, 201.510384, 200.866881, 199.302470, 197.883944, 197.787287, 196.461653, 195.927557, 194.143759, 192.558326, 189.494023, 159.954281, 158.666879, 154.332279, 153.377912, 151.521138, 148.318138, 143.690381, 141.229537, 114.491228, 110.644835, 110.088544, 107.387422, 103.711298, 96.390154, 95.985387, 93.789589, 92.729083, 91.896251, 88.807374, 88.359045, 87.512865, 87.344311, 87.180092, 86.600460, 84.700966, 84.300609, 83.905633, 82.422198, 82.029553, 80.033003, 79.798866, 78.969876, 78.900595, 78.619604, 78.352295, 78.014023, 77.415660, 77.377770, 77.140524, 76.977920, 76.645670, 76.227718, 75.652339, 74.704802, 74.294421, 74.065609, 71.562409, 71.302271, 69.842583, 68.764089, 68.492020, 68.117597, 68.072134, 67.842909, 67.610342, 67.351216, 66.918122, 66.794661, 66.631435, 65.973567, 65.425946, 64.547911, 63.011055, 62.663099, 60.946491, 60.650289, 60.319028, 59.415086, 58.883405, 58.637473, 58.357056, 58.108167, 57.879420, 56.677974, 56.642106, 56.122617, 55.894296, 55.644248, 55.224567, 54.953502, 54.435730, 54.044792, 52.591050, 51.567588, 49.972169, 46.763875, 46.504837, 45.687287, 44.154833, 43.054171, 42.002636, 41.606439, 41.061790, 40.575010, 40.231998, 39.796632, 39.299857, 39.129521, 37.518787, 37.334380, 36.517399, 36.401780, 35.418618, 35.205894, 34.773066, 34.328836, 33.959777, 33.728519, 33.154625, 32.737278, 32.343393, 31.587695, 31.459209, 31.183585, 30.790076, 30.610472, 30.491323, 30.020316, 29.291148, 28.887931, 28.136621, 27.694186, 27.602131, 27.464970, 26.745447, 26.491955, 26.382949, 26.200079, 25.930871, 25.744195, 25.510992, 25.233108, 24.873796, 24.364129, 23.374246, 22.947384, 22.461385, 21.875663, 21.621070, 21.361996, 20.751192, 20.558949, 20.253127, 19.975773, 19.662552, 19.334944, 18.967115, 18.914271, 18.544925, 18.416279, 17.916372, 17.721331, 17.414130, 16.978171, 16.891663, 16.613361, 16.422280, 15.901451, 15.481372, 15.062699, 14.532694, 13.677767, 13.312180, 12.997102, 12.724327, 12.351176]
hvs_9nh3 = [438.400838, 437.426952, 436.856151, 435.098928, 434.373205, 433.244433, 428.414876, 428.221452, 425.105739, 420.150207, 418.816556, 416.738576, 412.883411, 412.794755, 409.636380, 409.039463, 408.229541, 407.333891, 404.043903, 401.283305, 399.204731, 393.991062, 390.195490, 390.013912, 373.477915, 368.199742, 360.407510, 207.228709, 206.575907, 205.761269, 204.841750, 203.862327, 202.828187, 202.601596, 202.046069, 201.522844, 199.048709, 197.629544, 197.564413, 196.050050, 195.477893, 194.987669, 193.807827, 191.652566, 189.805910, 164.155072, 159.662717, 155.726691, 153.994060, 152.561196, 151.923061, 149.766683, 142.706032, 140.400969, 115.363068, 112.621640, 111.759628, 108.022015, 100.247531, 98.139500, 96.967850, 96.577080, 96.493026, 93.010138, 89.215705, 88.576768, 88.224616, 88.014908, 87.687588, 86.926529, 85.856365, 85.139596, 84.748287, 84.234442, 82.806485, 80.732511, 80.647112, 79.734675, 79.633487, 79.335645, 79.098958, 78.653635, 78.320708, 78.090900, 77.711991, 77.390292, 77.316945, 75.514478, 74.855865, 74.605941, 74.456907, 73.811593, 72.071250, 71.565081, 69.372469, 69.295918, 68.938602, 68.515948, 68.306077, 68.200187, 68.073837, 67.937463, 67.615593, 67.109368, 66.991016, 65.757083, 65.085513, 64.642536, 63.116049, 62.903790, 61.247710, 60.981324, 60.929437, 60.562556, 59.900084, 59.645866, 59.200859, 58.756529, 58.291131, 57.626015, 57.351353, 57.010207, 56.529574, 56.317068, 56.051189, 55.707981, 55.164793, 54.672073, 54.268747, 52.788343, 51.112852, 50.724546, 48.895853, 46.403126, 45.543278, 45.147815, 44.244057, 43.460902, 43.192606, 41.886487, 41.165628, 40.895522, 40.502111, 40.102448, 39.389302, 39.026663, 38.574104, 37.715438, 36.990913, 36.601210, 36.372928, 35.601405, 35.128943, 34.943617, 33.848167, 33.576442, 33.259202, 33.049040, 32.817600, 32.138129, 31.827532, 30.977901, 30.778342, 30.661845, 30.254351, 30.054492, 29.799698, 29.393301, 28.801856, 28.478613, 28.302145, 27.843784, 27.750947, 27.404376, 26.934111, 26.501411, 26.289625, 25.854916, 25.709295, 25.469574, 25.279792, 25.111201, 24.491124, 24.001908, 23.536599, 22.566786, 21.939120, 21.547191, 21.440833, 20.884407, 20.705424, 20.495739, 20.279331, 19.684001, 19.529093, 19.412187, 18.957337, 18.786555, 18.574201, 18.197783, 18.044199, 17.968685, 17.856068, 17.660940, 17.327263, 17.055762, 16.643211, 16.266531, 15.940985, 15.808013, 15.278258, 14.948776, 14.841765, 13.975914, 13.344724, 12.808389, 11.826654, 11.543892]
hvs_10nh3 = []
hvs_11nh3 = []
hvs_12nh3 = []
hvs_13nh3 = []

#hvs_molecular


# method()
def get_translation_partition_function(mass):
    translation_partition_functions_at_T = []
    for temperture in np.linspace(50, 500, 20):
        translation_partition_function = (2 * np.pi * mass * K_BOLTZMANN_J * temperture / (H_PLANK_J ** 2)) ** 1.5
        translation_partition_functions_at_T.append(translation_partition_function)
    return translation_partition_functions_at_T


def get_rotation_partition_function_nonlinear(symmetry_factor, rotational_constant_A, rotational_constant_B, rotational_constant_C):
    rotation_partition_functions_nonlinear_at_T = []
    for temperture in np.linspace(50, 500, 20):
        rotation_partition_function_nonlinear = 1 / symmetry_factor * ((K_BOLTZMANN_J * temperture / H_PLANK_J) ** 1.5) * \
                                                np.sqrt(np.pi / (rotational_constant_A * rotational_constant_B * rotational_constant_C))
        rotation_partition_functions_nonlinear_at_T.append(rotation_partition_function_nonlinear)
    return rotation_partition_functions_nonlinear_at_T


def get_vibration_partition_function(hvs):
    vibration_partition_functions_at_T = []
    for temperture in np.linspace(50, 500, 20):
        partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (K_BOLTZMANN_EV * temperture))) for
                              hv in hvs]
        vibration_partition_functions_at_T.append(np.prod(partition_function))
        # print(np.prod(partition_function))
    return vibration_partition_functions_at_T


def get_gas_molecular_partition_function(gas_molecular):
    qt = get_translation_partition_function(MASS_OF_NH3)
    qr = get_rotation_partition_function_nonlinear(SYM_FACTOR_NH3, ROT_CONST_A_NH3, ROT_CONST_B_NH3, ROT_CONST_C_NH3)
    qv = get_vibration_partition_function(hvs_nh3_gas)
    gas_molecular_partition_functions_at_T = [i * j * k for i, j, k in zip(qt, qr, qv)]
    # gas_molecular_partition_functions_at_T = [j * k for j, k in zip(qr, qv)]
    return gas_molecular_partition_functions_at_T
    print(gas_molecular)

def get_rate_const_adsorption():
    for temperture in np.linspace(50, 500, 20):
        rate_const_adsorptions = []
        rate_const_adsorption = total_pressure / (
        np.sqrt(2 * np.pi * MASS_OF_NH3 * K_BOLTZMANN_J * temperture) * CONC_OF_ACTIVE_SITE)

# def get_pre_exponential_factor():
#     pre_exponential_factors = []
#     Edes = 0.8412 #eV
#     for temperture in np.linspace(50, 500, 20):
#         rate_const_adsorptions = []
#         rate_const_adsorptions.append(rate_const_adsorption)
#     print(rate_const_adsorptions)


#Temp,Coverage_NH3 vs pre-exponetial factor
print(get_translation_partition_function(MASS_OF_NH3))
print(get_rotation_partition_function_nonlinear(SYM_FACTOR_NH3, ROT_CONST_A_NH3, ROT_CONST_B_NH3, ROT_CONST_C_NH3))
print(get_vibration_partition_function(hvs_nh3_gas))

print(get_vibration_partition_function(hvs_8nh3))
print(get_vibration_partition_function(hvs_9nh3))
print(get_pre_exponential_factor())
