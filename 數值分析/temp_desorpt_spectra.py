#!/usr/bin/env/python
# -*- coding: UTF-8 -*-

# 2016/10/1 Tino 1st

from scipy import interpolate
import numpy as np
import math
from scipy import integrate


# CONSTANTS
M_NH3 = (14.001 + 3 * 1.000) * 0.001 / (6 * math.pow(10, 23))  # MASS_OF_NH3, kg
KB_J = 1.38064852 * math.pow(10, -23)  # K_BOLTZMANN_J, J/K
KB_EV = 8.6173324 * math.pow(10, -5)  # K_BOLTZMANN_EV. eV/K
LATTICE_A = 9.49569 * math.pow(10, -10)  # m
LATTICE_B = 12.8097 * math.pow(10, -10)  # m
C_OF_ACTIVE_SITE = 6 / (LATTICE_A * LATTICE_B)  # CONC_OF_ACTIVE_SITE, number of site/m2
H_J = 6.626070040 * math.pow(10, -34)  # H_PLANCK_J, J.sec
# Rotational constants ( http://www.colby.edu/chemistry/PChem/scripts/ABC.html)
ROT_CONST_A_NH3 = 610.85  # 1/m
ROT_CONST_B_NH3 = 983.86  # 1/m
ROT_CONST_C_NH3 = 983.91  # 1/m
ROT_CONST_A_H2O = 921.21  # 1/m
ROT_CONST_B_H2O = 1391.9  # 1/m
ROT_CONST_C_H2O = 2724.1  # 1/m
SIGMA_NH3 = 3  # SYM_FACTOR_NH3
SIGMA_H2O = 2  # SYM_FACTOR_H2O
C = 299792458  # speed of light m/s

# hvs_vib
hvs_surface = [88.368339, 88.038457, 87.125882, 86.891439, 86.012095, 85.717264, 84.604000, 84.485125, 80.133617, 78.343028, 78.182778, 77.126894, 77.083545, 75.596970, 74.995153, 73.286149, 72.656771, 72.404724, 71.432893, 70.936344, 70.790529, 70.453227, 67.365325, 66.677105, 66.406831, 65.753694, 65.705142, 65.576043, 65.536429, 63.216185, 60.042358, 59.381490, 58.340878, 58.221463, 57.734002, 57.099516, 45.387040, 41.341623, 36.067831, 35.938650, 35.208225, 34.854890, 33.974190, 33.852179, 33.707111, 33.567680, 33.417010, 32.220465, 30.220988, 30.193443, 30.142710, 29.926241, 29.424193, 29.337073, 27.569408, 27.520570, 27.229696, 26.418508, 26.173327, 26.150120, 24.281846, 23.701113, 22.331511, 21.859667, 21.819634, 20.963830, 20.772723, 20.448961, 20.408148, 20.328676, 20.133545, 19.630061, 19.320961, 19.090038, 19.048791, 18.901550, 18.770183, 18.096004, 18.062549, 17.972906, 17.286228, 17.251330, 17.072143, 16.264899, 14.848576, 14.764126, 14.694975, 8.844488, 8.600608, 3.810817]
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
hvs_nh3_gas = [435.460659, 431.205986, 415.541526, 203.517923, 201.833141, 120.027150]
hvs_1nh3 = [430.198631, 427.540569, 413.961910, 198.085064, 197.954985, 155.888486, 100.626456, 96.913905, 91.150507, 90.571449, 89.577129, 89.333135, 88.593270, 88.076295, 87.886616, 86.694058, 83.365306, 81.745121, 80.947879, 80.185729, 79.852830, 78.509102, 78.224377, 75.948489, 75.623308, 75.216938, 73.746860, 73.650604, 70.716749, 70.119930, 69.654502, 69.168927, 68.939090, 65.750349, 64.807776, 64.321902, 64.119328, 63.509015, 61.902849, 61.104554, 60.901952, 60.668654, 60.155707, 59.358441, 58.895983, 44.163961, 42.740979, 37.943257, 36.766113, 35.552710, 35.284977, 34.827630, 34.380060, 34.257256, 33.587371, 33.302352, 33.108034, 30.834472, 30.731268, 30.660547, 30.331024, 30.283868, 30.224699, 29.193081, 28.773556, 28.233508, 27.796885, 27.517773, 27.211584, 26.602082, 26.049863, 24.195551, 22.550748, 22.217728, 21.832439, 21.661550, 21.522873, 21.328779, 20.743273, 20.667872, 20.507662, 20.257865, 19.767438, 19.121150, 18.917779, 18.821477, 18.724233, 18.552834, 17.980644, 17.809680, 17.072836, 16.866863, 16.051825, 15.705389, 15.338813, 14.747400]
hvs_2nh3 = [424.125172, 423.849717, 420.595920, 419.403011, 410.808280, 405.796797, 200.394007, 199.456838, 199.033067, 198.587343, 157.676765, 155.343118, 107.766780, 102.077340, 100.129117, 99.457258, 89.161474, 88.785527, 87.924722, 87.561085, 86.573713, 86.383606, 85.801908, 85.655321, 81.868313, 79.400476, 79.191369, 78.312681, 77.940721, 77.281795, 77.080852, 74.568861, 74.157690, 73.548951, 72.704997, 72.368210, 70.624597, 69.999068, 69.224256, 67.960474, 67.319906, 65.274200, 65.197919, 64.764850, 64.505284, 64.288516, 61.433483, 60.961585, 60.692938, 60.199048, 59.864068, 59.473005, 58.830080, 58.539293, 44.672150, 43.767245, 39.090709, 38.339463, 36.558748, 36.146206, 36.026258, 35.695262, 35.472710, 35.007167, 34.594195, 33.993084, 33.264194, 30.937056, 30.909414, 30.723105, 30.570799, 30.219125, 30.022164, 29.945579, 29.074837, 28.866068, 28.836132, 28.575930, 28.134741, 27.892153, 27.633395, 26.837740, 24.615636, 24.092543, 23.078251, 22.608815, 22.301980, 22.102627, 21.934406, 21.521768, 21.330050, 21.174876, 20.590801, 20.347330, 19.927018, 19.692588, 19.582158, 19.292423, 19.203925, 18.711171, 18.404162, 18.315183, 18.035711, 17.909694, 17.207706, 16.780799, 16.550679, 16.327247]
hvs_3nh3 = [431.945641, 431.720410, 429.573144, 427.738331, 426.200762, 424.256943, 411.698185, 410.737511, 406.708417, 199.903388, 199.697292, 199.091961, 198.000023, 196.959930, 194.147980, 153.768967, 149.543130, 148.136182, 105.460435, 98.777335, 97.587559, 97.078918, 94.820326, 91.433966, 89.606141, 88.430589, 88.064178, 87.236970, 86.748031, 86.377619, 85.955183, 84.994139, 82.188524, 79.478418, 79.318996, 78.546190, 78.128916, 77.472750, 77.022601, 74.645981, 74.283931, 73.989109, 73.027070, 72.342573, 69.807794, 69.517106, 68.795268, 67.928083, 67.607465, 64.768611, 64.634633, 64.110019, 63.219582, 61.232240, 60.297210, 59.899599, 59.521632, 59.101234, 59.031000, 58.712717, 58.292185, 57.540361, 56.611263, 45.828275, 44.893989, 40.546186, 39.708552, 37.825992, 37.593690, 36.389396, 36.138395, 36.021527, 35.250088, 35.105642, 33.981288, 32.070714, 31.406423, 30.822510, 30.665804, 30.391265, 30.171136, 29.952202, 29.486314, 29.189925, 28.730505, 28.398837, 28.228877, 27.786885, 27.560522, 24.981284, 24.842628, 23.935793, 23.737744, 23.282072, 22.429283, 22.154002, 22.005428, 21.843666, 21.703135, 21.217822, 20.951794, 20.793121, 20.526373, 20.200131, 19.631758, 19.517599, 19.351901, 19.280363, 18.982125, 18.685935, 18.291913, 17.958897, 17.772454, 17.343421, 16.841268, 16.629067, 16.436494, 16.002124, 15.587709, 14.640104, 12.306777, 9.042349, 8.822680, 4.926397, 2.671439]
hvs_4nh3 = [443.218996, 430.502894, 430.005568, 429.694462, 423.668619, 423.452506, 423.064244, 421.659984, 416.263090, 410.875070, 410.762992, 408.358889, 201.039610, 200.015129, 199.576171, 199.367007, 196.819325, 196.619683, 193.360714, 192.708082, 150.077234, 149.547913, 147.994476, 146.024155, 98.912999, 98.223812, 97.550656, 96.771268, 95.567220, 94.631321, 91.771421, 89.740078, 89.545912, 88.947602, 87.699093, 87.463183, 87.045083, 86.750145, 86.398492, 85.972595, 82.847232, 79.598093, 79.531043, 79.171711, 78.901163, 78.228826, 77.813375, 75.284586, 74.801763, 74.546732, 73.528632, 72.672632, 69.814706, 68.902276, 68.665863, 67.896352, 67.477726, 65.352905, 63.184512, 62.706346, 61.978097, 61.138219, 59.407245, 59.224912, 59.154675, 58.775412, 58.345591, 58.142868, 57.945077, 57.761957, 57.307247, 57.152828, 46.077826, 45.355963, 41.287876, 40.921196, 37.912663, 37.647217, 37.460352, 36.752853, 36.308679, 35.696606, 35.294998, 34.278565, 32.936334, 31.709892, 31.519742, 30.837961, 30.625968, 30.439380, 30.272052, 29.927929, 29.631375, 29.534315, 29.367678, 28.902328, 28.660366, 28.446956, 28.071860, 26.083025, 25.126738, 24.579572, 24.228806, 24.063071, 23.613473, 22.793216, 22.724116, 22.278833, 21.645011, 21.462779, 21.240680, 20.624524, 20.424062, 20.288325, 19.850006, 19.651531, 19.520048, 19.419085, 19.157918, 18.875580, 18.487890, 18.201916, 18.082724, 17.896046, 17.300743, 16.713287, 16.511288, 16.376500, 15.299197, 14.527256, 13.568941, 12.821245, 9.190963, 8.842684, 8.386258, 4.951641, 2.882830]
hvs_5nh3 = [437.904160, 434.994695, 432.261686, 430.582267, 430.338213, 428.886294, 427.693623, 424.327237, 423.800130, 422.245070, 416.447874, 413.931159, 408.926752, 408.762898, 396.018763, 205.755928, 203.396063, 199.933276, 199.269291, 197.861443, 196.779580, 195.860982, 194.423485, 193.138126, 192.045871, 148.775068, 146.999881, 146.285251, 142.044078, 140.104865, 101.535794, 98.526095, 96.785373, 96.017672, 93.361335, 93.193241, 91.471347, 90.447682, 89.675694, 89.281324, 88.294838, 87.811740, 87.516572, 87.147855, 86.646772, 85.771967, 84.262018, 83.406074, 80.960419, 80.670421, 80.068125, 79.604090, 78.404350, 78.248630, 77.052076, 75.492391, 75.079276, 74.951805, 72.981652, 72.413942, 69.718640, 68.681349, 68.044342, 67.961792, 66.175785, 64.955007, 61.816420, 61.047973, 60.374934, 59.921171, 58.759718, 58.367088, 58.270119, 57.620908, 57.533098, 57.211828, 56.692715, 56.558401, 56.370518, 55.047034, 53.983123, 47.308310, 46.037447, 44.164202, 41.373451, 41.083493, 40.132225, 38.549880, 37.878612, 37.808830, 36.829497, 36.511383, 35.994456, 35.848434, 35.179856, 34.161729, 33.714903, 31.078596, 31.004425, 30.495364, 30.324133, 30.232721, 29.901395, 29.521388, 29.380959, 29.304287, 28.971229, 28.876760, 27.940451, 27.768778, 25.382052, 24.890033, 24.835875, 24.360015, 24.280651, 23.688137, 23.000639, 22.645432, 22.511348, 22.155251, 21.707958, 21.037556, 20.961247, 20.773897, 20.277454, 20.164532, 20.011565, 19.709291, 19.598126, 19.392528, 19.071874, 18.819868, 18.537166, 18.169248, 17.556829, 17.451671, 16.759828, 16.577790, 16.370595, 15.887763, 15.477651, 14.619638, 11.725703, 8.538634, 8.167696, 5.681876, 4.975406]
hvs_6nh3 = [433.837675, 433.118086, 432.912621, 428.396763, 428.108910, 427.721850, 423.613889, 423.060225, 421.460238, 418.501050, 417.332656, 416.334602, 411.506883, 410.384384, 384.121121, 352.850239, 311.531353, 296.760783, 206.549179, 205.425860, 201.828751, 201.163825, 200.633458, 198.795084, 196.419896, 196.078848, 193.904927, 193.593983, 186.014790, 184.663777, 159.331289, 156.031530, 152.615765, 152.272819, 143.849427, 143.121028, 107.844627, 106.775949, 106.298126, 103.465295, 95.575907, 93.745531, 92.446153, 91.575865, 91.012623, 90.613898, 88.906102, 88.386329, 88.277820, 88.189144, 87.899257, 86.721519, 85.351651, 84.894381, 84.565041, 83.991546, 83.430792, 79.867868, 79.722644, 79.326698, 79.128258, 78.435661, 78.030359, 75.549474, 75.320339, 75.270443, 72.666996, 72.379812, 69.441253, 68.529895, 68.227996, 67.790849, 66.095560, 64.799391, 62.351017, 62.126914, 60.112489, 59.816858, 59.405311, 59.134287, 58.531696, 58.375765, 57.715772, 57.297284, 57.136672, 56.969169, 55.636758, 55.449482, 55.216941, 54.896134, 53.036037, 48.961492, 46.894852, 45.824476, 43.678844, 42.605130, 42.147617, 41.617921, 40.674081, 39.851414, 39.688355, 39.218713, 38.302958, 37.552243, 37.463657, 37.171596, 36.703929, 36.179576, 35.892368, 35.048164, 34.553532, 33.736765, 33.356612, 32.636247, 32.127163, 31.445217, 31.202313, 30.677558, 29.904776, 29.755576, 29.392829, 28.813866, 28.450334, 27.798440, 27.627663, 26.781423, 26.335813, 25.816016, 25.360688, 24.816588, 24.464680, 23.406063, 23.122800, 22.991898, 22.479305, 21.844706, 21.522134, 21.285202, 20.642959, 20.450250, 20.344665, 20.168077, 19.971818, 19.915858, 19.637015, 19.518857, 18.994768, 18.651891, 18.456458, 18.197423, 17.759527, 17.318207, 17.132150, 16.785634, 16.090058, 15.318546, 14.843982, 14.599198, 10.741229, 8.845284, 7.778016, 6.095807]
hvs_7nh3 = [447.325394, 437.331228, 436.696371, 430.515122, 430.281898, 429.629591, 429.130031, 428.415587, 428.355989, 427.548215, 426.683353, 423.514282, 423.091429, 419.288841, 416.060955, 415.119703, 414.782531, 366.288934, 365.238968, 357.500084, 353.052430, 205.788584, 204.949444, 204.643885, 204.457920, 201.795328, 200.212455, 197.923957, 197.209099, 196.863551, 195.038854, 194.011634, 193.565788, 191.590935, 190.569937, 161.344804, 153.682554, 148.704193, 145.755436, 144.768818, 143.625757, 142.096132, 111.508992, 101.945201, 100.928732, 95.442720, 93.541041, 92.217305, 91.784793, 91.074342, 90.058827, 89.701880, 89.609171, 89.367054, 88.473240, 88.299203, 87.894789, 86.876467, 86.492977, 85.569967, 84.046711, 83.835167, 81.698204, 80.981501, 80.882773, 80.529063, 80.323961, 78.603179, 78.477039, 75.994025, 75.627186, 75.347597, 72.817838, 72.367129, 69.619584, 68.835656, 68.724370, 68.373028, 65.949628, 64.588386, 64.050030, 62.746594, 61.833099, 61.675041, 61.106918, 60.737433, 60.074359, 59.119857, 58.275304, 57.627178, 57.173067, 56.818975, 55.775320, 55.144312, 54.517524, 53.903609, 52.537024, 48.181619, 45.631369, 45.263450, 44.533997, 43.704885, 42.228318, 41.267804, 40.685331, 40.442139, 38.963205, 38.658988, 37.818474, 37.426719, 36.961723, 36.698769, 36.209697, 35.904043, 34.466190, 34.135336, 33.470073, 33.293084, 32.506665, 31.975710, 31.412411, 31.197806, 31.015020, 30.732525, 30.394416, 30.225096, 29.967104, 29.329587, 29.135783, 28.682577, 27.759767, 27.543499, 26.972113, 26.460092, 25.127411, 24.915820, 24.682285, 23.883041, 23.175193, 22.357900, 22.211619, 21.943634, 21.815370, 21.369832, 20.939098, 20.725320, 20.433550, 20.278908, 19.897118, 19.770439, 19.370325, 19.234605, 19.118673, 18.696385, 18.594242, 18.334643, 18.260042, 17.644487, 17.429533, 17.208642, 17.050598, 16.514567, 16.175939, 15.093278, 14.153149, 13.653147, 11.068193, 10.452755, 9.306683, 7.464912, 5.663137, 4.473397]
hvs_8nh3 = [458.298060, 437.233061, 436.820472, 435.312493, 433.340757, 431.553643, 430.725388, 430.439893, 427.871176, 423.379394, 416.390616, 416.165901, 415.476585, 414.138407, 403.584187, 398.725595, 397.723698, 394.978213, 382.431964, 377.535397, 376.629308, 367.860666, 367.276536, 356.458045, 207.655110, 207.281874, 205.249960, 204.370792, 202.751913, 201.734366, 201.596931, 200.803507, 199.641552, 197.690993, 196.585726, 196.371922, 195.440641, 193.309700, 191.807945, 189.257236, 160.414564, 158.919131, 154.234357, 152.069700, 149.862151, 147.380365, 142.795762, 140.723322, 114.462785, 109.971623, 109.753292, 104.720555, 102.204679, 96.136593, 94.168013, 93.718293, 92.281002, 91.352241, 88.565222, 88.374124, 87.842459, 87.729564, 87.356719, 86.746615, 85.031144, 84.441149, 82.692921, 82.540760, 80.838909, 79.716234, 79.380991, 78.767662, 78.496300, 77.806515, 77.329658, 75.131771, 74.733741, 74.548131, 74.429758, 71.761954, 71.492150, 71.214034, 68.485991, 68.295747, 67.474318, 67.306988, 65.657456, 63.519107, 62.770834, 60.888600, 60.678903, 60.560205, 60.131203, 59.935742, 59.459244, 59.080589, 58.926514, 58.241328, 57.914547, 57.559675, 56.695160, 56.071535, 55.816041, 55.701512, 54.525573, 52.959317, 52.286118, 48.367391, 47.582075, 46.407114, 45.310069, 44.473173, 43.251506, 42.192494, 41.579754, 40.968000, 40.052513, 39.563823, 39.053574, 38.280567, 37.552687, 37.368060, 36.773247, 36.429939, 35.651341, 35.507310, 34.908370, 34.247868, 34.061040, 32.961519, 32.742927, 31.964781, 31.354722, 31.170283, 30.613886, 30.476830, 30.230283, 30.099015, 29.231503, 28.641151, 28.078589, 27.758031, 27.350866, 27.122899, 26.536029, 25.923280, 25.404416, 24.901853, 24.326036, 24.023156, 22.569718, 22.292982, 21.981386, 21.785722, 21.642006, 21.202988, 20.927816, 20.739375, 20.511296, 20.285729, 20.180577, 20.009828, 19.855054, 19.671834, 19.532734, 19.165633, 18.849623, 18.437532, 18.376850, 18.255048, 17.672439, 17.357707, 16.701163, 16.440340, 16.361522, 15.723947, 15.111143, 13.963278, 12.652533, 11.131057, 10.140965, 8.078727, 6.643676, 4.821930]
hvs_9nh3 = [460.679672, 437.445632, 437.057725, 435.009319, 434.612774, 427.786993, 426.956202, 426.824517, 423.765152, 419.993927, 418.299852, 415.155829, 413.842486, 410.570233, 408.565193, 407.906698, 406.605201, 406.179053, 404.392131, 402.155760, 399.336107, 392.421903, 390.241794, 387.352408, 372.128691, 366.000232, 360.458956, 207.091624, 206.848420, 205.480774, 204.837966, 203.633507, 202.568151, 202.337375, 201.867537, 201.644359, 199.028863, 197.349166, 196.684762, 196.565928, 195.776238, 195.544732, 193.795618, 191.051230, 189.007713, 163.329876, 158.548736, 155.044258, 153.457375, 152.722193, 151.642615, 147.561018, 143.356396, 140.328936, 115.205130, 111.155289, 110.365494, 106.525348, 99.673621, 96.816056, 96.386692, 95.549511, 94.534159, 91.861114, 88.989949, 88.805230, 88.675688, 88.330196, 87.340058, 86.832152, 86.600754, 85.914361, 85.385826, 84.196957, 83.187296, 79.976965, 79.794338, 79.104530, 78.637222, 78.233061, 77.986815, 75.238542, 75.187919, 75.019047, 73.108032, 72.499400, 71.806123, 71.024293, 70.116021, 68.877222, 68.664617, 67.878639, 67.737316, 65.822829, 65.357315, 63.926111, 63.637085, 62.258881, 62.104206, 61.316356, 61.056157, 60.635105, 60.031006, 59.153617, 58.333856, 58.098460, 57.889867, 57.678757, 57.241749, 56.686721, 55.954088, 55.206497, 52.720004, 52.124510, 50.125126, 48.624321, 46.634348, 46.376326, 45.242246, 43.833800, 43.415469, 42.010871, 41.302918, 40.297620, 39.969832, 39.534849, 39.008202, 38.500502, 37.999113, 37.668816, 36.913794, 36.329706, 36.049116, 35.694092, 35.197111, 34.698631, 34.020857, 33.609776, 32.921083, 32.741705, 32.429582, 32.022520, 31.290466, 30.955046, 30.707939, 30.479457, 30.176718, 29.098569, 28.783683, 28.320135, 28.122351, 27.712225, 26.755229, 26.423902, 26.171725, 25.933332, 25.019055, 24.430172, 24.271852, 23.860202, 23.220127, 22.673937, 22.331949, 21.809171, 21.500883, 21.488114, 20.929236, 20.867542, 20.598427, 20.487780, 20.301577, 20.177316, 19.937167, 19.831104, 19.657343, 19.298681, 19.209644, 18.863291, 18.855737, 18.293367, 18.223944, 17.636951, 17.374119, 17.093863, 16.514689, 15.859263, 15.548123, 15.373062, 13.978543, 13.259106, 12.854525, 11.933698, 11.341845, 10.325224, 8.908910, 6.018015, 3.802713]
hvs_10nh3 = [436.682186, 434.955514, 434.821758, 434.676782, 434.301183, 433.722005, 433.457653, 430.756958, 426.812443, 425.179224, 422.859904, 421.621180, 418.337815, 417.439574, 416.342145, 414.895422, 411.810225, 404.299497, 402.917004, 397.097578, 396.658167, 392.019454, 388.477301, 387.318051, 384.851666, 384.343662, 381.004169, 377.872896, 372.580889, 370.780289, 211.501309, 211.312304, 205.905401, 205.031429, 204.489834, 203.151325, 202.262887, 201.636811, 200.603702, 199.997358, 199.620179, 198.581554, 198.282037, 196.445850, 195.870042, 195.444359, 192.963941, 192.388185, 191.099188, 190.087883, 160.265386, 159.872889, 154.685036, 153.673197, 150.840394, 149.823118, 149.527046, 149.111723, 147.832016, 146.802514, 112.945073, 111.629929, 110.733960, 110.152120, 107.229598, 105.709353, 96.505989, 96.267558, 96.219825, 95.858126, 89.507698, 88.576347, 88.064066, 87.557317, 87.434233, 86.885534, 86.716485, 84.929630, 84.474512, 83.887212, 82.545458, 79.185875, 79.140211, 78.611236, 78.328328, 77.324981, 77.141257, 74.640699, 74.451906, 74.431964, 74.229190, 73.918748, 71.122468, 70.928754, 68.334656, 68.249509, 68.029801, 67.155309, 67.082166, 66.765149, 65.759710, 64.107415, 63.229564, 63.136453, 62.801358, 62.088621, 61.900436, 61.106544, 60.487484, 60.080970, 59.962649, 59.809300, 58.976807, 58.821271, 58.460855, 57.975147, 57.551860, 57.315437, 57.057830, 56.770894, 56.177216, 55.145973, 53.754165, 53.221669, 47.613045, 47.103866, 46.240226, 44.702080, 42.760204, 42.288677, 41.958410, 41.277346, 40.560867, 40.252804, 39.718804, 38.541049, 38.286896, 37.990287, 37.611942, 37.283906, 36.799097, 36.559365, 35.944055, 35.306646, 34.782592, 34.583156, 33.927379, 33.296697, 33.191158, 32.395792, 31.883825, 31.751137, 31.463061, 30.806158, 30.429204, 30.127907, 29.885728, 28.958116, 28.595925, 28.299195, 27.807600, 27.655369, 27.111753, 26.878490, 25.782445, 25.346542, 25.020115, 24.596127, 24.217423, 24.165940, 23.015582, 22.777009, 22.339167, 22.084339, 21.853593, 21.537581, 20.975353, 20.667846, 20.582750, 20.516638, 20.192667, 20.103116, 19.997490, 19.765734, 19.508282, 19.414422, 19.302110, 19.238015, 18.756070, 18.343001, 18.080924, 17.920839, 17.576309, 17.466089, 17.034241, 16.773546, 16.485012, 15.746185, 15.251182, 14.989651, 14.544847, 14.173219, 13.702689, 11.022901, 10.360171, 8.434268, 6.083065, 3.529874]
hvs_11nh3 = [435.812085, 434.922597, 434.859922, 434.365611, 433.450592, 433.310530, 430.801293, 429.944615, 426.654468, 425.183071, 423.878564, 422.622118, 421.186666, 420.464654, 420.262443, 418.258868, 416.871425, 412.812426, 412.069530, 409.478601, 407.239450, 403.079613, 396.670825, 395.034431, 393.081645, 389.660753, 386.100003, 385.108848, 384.934439, 382.629132, 378.055835, 377.416098, 375.156594, 211.801386, 211.575538, 206.513271, 205.336706, 205.020673, 204.012391, 203.310406, 202.275961, 201.795593, 201.291630, 199.905901, 199.608432, 199.448479, 198.532710, 197.691429, 197.259417, 196.186628, 194.606992, 194.132571, 191.840369, 191.167937, 190.598767, 165.255066, 160.719052, 157.604847, 153.993703, 151.832135, 150.990682, 148.998140, 147.955596, 147.350270, 145.701300, 137.756616, 112.024628, 110.973968, 109.315363, 107.161300, 106.990323, 106.108535, 97.777409, 97.027607, 95.818614, 95.597189, 88.534181, 88.001076, 87.608494, 87.422804, 87.171441, 87.042108, 86.636495, 85.177255, 84.711079, 84.363813, 82.509318, 78.957318, 78.835371, 78.569163, 78.332024, 77.205295, 77.125592, 74.766111, 74.479540, 74.417787, 74.250355, 73.163220, 71.097722, 70.990244, 70.578440, 70.121201, 67.982427, 67.691183, 67.099555, 66.928301, 65.222449, 64.794979, 63.608607, 63.383573, 62.819371, 62.513312, 62.091406, 61.868690, 61.685480, 61.007235, 60.513401, 59.849361, 59.340987, 59.135692, 58.747867, 58.587959, 58.369924, 57.867245, 57.512177, 57.054103, 56.593298, 56.033247, 54.267988, 53.372325, 51.014209, 49.805171, 47.878473, 47.392699, 46.228396, 45.373922, 43.794377, 43.009783, 42.313891, 41.850617, 41.066991, 40.522003, 40.066469, 39.854873, 39.175030, 39.099058, 38.403223, 38.269242, 37.787598, 37.385972, 36.844563, 35.945571, 35.754917, 35.445143, 35.047148, 34.298945, 33.950141, 33.033139, 32.923866, 32.256021, 31.533122, 31.120551, 30.969516, 30.549369, 30.260676, 30.061664, 29.900576, 29.010033, 28.381438, 28.104477, 27.554739, 27.029441, 26.754475, 26.141148, 25.721959, 25.489020, 25.209074, 25.035104, 24.091071, 23.626431, 22.743601, 22.723080, 22.228558, 21.737579, 21.567948, 21.382376, 20.948571, 20.858796, 20.551675, 20.400695, 20.309650, 20.289785, 19.806609, 19.544296, 19.417692, 19.291825, 18.929643, 18.869386, 18.684901, 18.361858, 18.024969, 17.805700, 17.487463, 17.267078, 17.046637, 16.652655, 16.209552, 16.119645, 15.963654, 15.258409, 14.655550, 13.007898, 12.883268, 11.390289, 10.992229, 9.843484, 9.685476, 6.514110, 5.787344, 2.566014]
hvs_12nh3 = [435.391285, 435.126597, 435.071815, 434.242322, 433.264046, 433.235438, 433.134191, 432.500139, 427.354101, 425.981393, 424.333233, 424.112237, 422.302459, 421.987765, 420.827851, 420.094209, 419.678603, 418.494619, 418.104296, 417.104323, 411.627933, 410.681233, 410.016159, 409.138268, 408.411219, 402.511272, 394.687013, 394.102959, 389.633255, 387.071430, 386.006547, 385.561801, 383.541733, 378.242223, 375.401884, 374.948748, 212.328529, 211.624119, 206.638393, 205.357954, 205.062420, 203.861151, 203.111801, 202.604723, 201.793528, 201.279143, 200.822571, 200.151199, 199.955179, 199.478043, 198.548298, 198.053576, 197.311080, 197.085861, 196.368248, 194.209375, 193.922264, 192.091613, 191.521692, 190.596280, 165.438378, 165.158229, 156.326072, 155.623817, 152.270022, 151.732962, 149.560773, 147.764251, 146.849015, 145.242673, 136.421179, 134.680335, 112.077389, 109.678260, 109.246399, 106.679453, 105.385932, 105.156817, 98.377285, 98.190567, 96.446447, 96.288548, 89.838998, 89.349067, 88.201974, 87.842297, 87.380405, 87.190352, 86.623841, 84.932294, 84.757353, 84.578138, 82.523274, 78.941509, 78.839575, 78.518181, 78.309202, 77.261210, 77.081852, 75.676054, 74.621992, 74.549019, 74.477545, 74.300667, 72.108274, 70.738521, 70.592765, 69.300337, 67.890162, 67.484917, 67.087643, 66.976327, 65.353192, 64.942489, 64.097631, 63.371105, 63.046076, 62.725714, 62.545208, 62.078116, 61.943411, 61.751340, 61.282162, 60.694201, 60.202831, 60.085692, 59.786777, 59.249942, 59.038225, 58.670638, 58.182996, 57.747371, 57.356089, 56.703205, 55.682496, 54.982315, 51.578962, 49.682109, 48.966138, 47.592808, 47.001130, 46.457540, 45.900375, 45.565266, 43.588827, 43.271693, 42.587244, 41.924219, 41.211199, 40.926708, 40.350374, 40.035172, 39.705093, 39.248187, 38.800615, 38.331042, 37.957300, 37.664256, 36.831116, 36.153981, 35.516928, 35.379120, 34.574562, 34.346104, 33.918454, 33.084605, 32.864390, 32.410802, 32.116009, 31.182525, 30.957603, 30.704936, 30.488351, 30.341891, 29.869356, 29.545000, 28.522617, 28.363596, 27.956669, 27.823651, 27.355153, 26.651472, 26.470001, 25.668431, 25.389962, 25.141758, 24.641883, 24.218530, 23.878555, 23.317166, 22.337377, 22.273569, 21.934156, 21.779364, 21.662113, 21.339712, 21.109799, 20.870216, 20.665436, 20.515517, 20.458397, 20.238448, 20.044188, 19.900945, 19.739588, 19.209104, 19.087262, 18.882125, 18.785814, 18.588036, 18.393904, 18.213650, 17.576455, 16.971995, 16.943238, 16.710691, 16.442406, 15.740142, 14.718535, 14.367214, 13.976447, 13.164564, 12.996510, 11.389467, 10.776953, 10.426769, 9.016674, 6.815014, 5.761424]
hvs_13nh3 = [436.821809, 436.085054, 435.965845, 435.772803, 435.373569, 434.586831, 434.556268, 433.843547, 433.205975, 428.169631, 427.577942, 425.904392, 425.547174, 425.070370, 424.672849, 424.080141, 421.218703, 419.443190, 418.364323, 416.026107, 415.774668, 415.113001, 414.364718, 413.648082, 412.951760, 409.909810, 404.098441, 402.679568, 400.644960, 398.557797, 392.101126, 390.880635, 386.812571, 385.243941, 384.667421, 383.293366, 380.498937, 378.391587, 378.027138, 212.072590, 211.556794, 206.424857, 205.753063, 205.498681, 204.769106, 203.809923, 203.422427, 202.950369, 202.733325, 202.132837, 201.957643, 201.320329, 200.942722, 199.960981, 199.550106, 198.909197, 197.950189, 197.663024, 197.008410, 196.393188, 195.712463, 192.904759, 192.647427, 192.086115, 190.801336, 165.105327, 164.970680, 156.484284, 155.778557, 151.922957, 151.733702, 150.145195, 149.544202, 145.848241, 145.251970, 137.809647, 135.935386, 128.350800, 112.338019, 109.906301, 108.978643, 108.410909, 106.705497, 105.418475, 100.010451, 97.383157, 96.774489, 95.688728, 91.449023, 88.878730, 88.206640, 88.001427, 87.854124, 87.564702, 87.084026, 86.003628, 85.188576, 84.837099, 82.702138, 79.530105, 79.284222, 79.007731, 78.721307, 77.571209, 77.554899, 74.903022, 74.705304, 74.475938, 73.589195, 73.085777, 71.486933, 71.294162, 70.060909, 68.428381, 68.237904, 67.332638, 67.232585, 66.390509, 65.888027, 64.705926, 63.919141, 63.398138, 63.071547, 62.585130, 61.952797, 61.872627, 61.617194, 61.299658, 60.766428, 60.301014, 60.173840, 59.673811, 59.529267, 58.789209, 58.556480, 58.425428, 58.022087, 57.862104, 57.388980, 56.948250, 56.761028, 55.642298, 53.930791, 52.693345, 49.736555, 47.986670, 47.565308, 47.024768, 45.583549, 45.155070, 43.689951, 42.936745, 42.569401, 41.832162, 41.393963, 40.927841, 40.724078, 40.179796, 39.674243, 38.991100, 38.702202, 38.268049, 37.955062, 37.625456, 36.999497, 36.141383, 35.606291, 35.159670, 34.973143, 34.258406, 33.844634, 33.083773, 32.740731, 31.967721, 31.543018, 31.215515, 30.967103, 30.725388, 30.426698, 30.280574, 29.293153, 28.899264, 28.742962, 28.319419, 27.904861, 27.519035, 26.762012, 26.148691, 25.556601, 25.474131, 25.315565, 25.149578, 24.363827, 24.191971, 23.645744, 23.331665, 23.122615, 22.334650, 22.052363, 21.829543, 21.741555, 21.481497, 21.079486, 20.965396, 20.863942, 20.511030, 20.449237, 20.369069, 20.145336, 19.955034, 19.866402, 19.646292, 19.377930, 19.148911, 19.085533, 18.838148, 18.589064, 18.325130, 18.209142, 17.682805, 17.452640, 17.059870, 16.951852, 16.790355, 16.053017, 15.643446, 15.203903, 15.139166, 14.510608, 14.086240, 13.451616, 12.599198, 11.893684, 10.886321, 10.551650, 9.735856, 8.297658, 7.017232, 5.499615, 3.459499]


# Dersoption Energy(eV)
e_des_1nh3 = 2.559347
e_des_2nh3 = 2.100317
e_des_3nh3 = 2.109297
e_des_4nh3 = 2.030267
e_des_5nh3 = 1.556527
e_des_6nh3 = 1.464067
e_des_7nh3 = 1.557967
e_des_8nh3 = 1.109317
e_des_9nh3 = 0.841267
e_des_10nh3 = 0.836037
e_des_11nh3 = 0.496997
e_des_12nh3 = 0.442757
e_des_13nh3 = 0.352057


# #Dersoption Energy(eV)_ZPE
# e_des_1nh3_ZPE =
# e_des_2nh3_ZPE =
# e_des_3nh3_ZPE =
# e_des_4nh3_ZPE =
# e_des_5nh3_ZPE =
# e_des_6nh3_ZPE =
# e_des_7nh3_ZPE =
# e_des_8nh3_ZPE =
# e_des_9nh3_ZPE =
# e_des_10nh3_ZPE =
# e_des_11nh3_ZPE =
# e_des_12nh3_ZPE =
# e_des_13nh3_ZPE =


total_pressure = 2 * math.pow(10, -10)  # Pa, （m·kg·s-2）/m^2


def get_translation_partition_function(mass, temperature, pressure):
    t = temperature
    volume = KB_J * t / pressure
    λ = np.sqrt((H_J ** 2) / (2 * np.pi * mass * KB_J * t))
    qt = volume / (λ ** 3)
    return qt


def get_rotation_partition_function_nonlinear(symmetry_factor, temperature, rotational_constant_a, rotational_constant_b, rotational_constant_c):
    t = temperature
    qr_nonlinear = 1 / symmetry_factor * (((KB_J * t / (H_J * C)) ** 1.5) * np.sqrt(np.pi / (rotational_constant_a * rotational_constant_b * rotational_constant_c)))
    return qr_nonlinear


def get_vibration_partition_function(hvs, temperature):
    t = temperature
    partition_functions = []
    for hv in hvs:
        partition_function = [1.0 / (1.0 - math.exp(-1 * hv * math.pow(10, -3) / (KB_EV * t)))]
        partition_functions.append(partition_function)
    qv = np.prod(partition_functions)
    return qv


def get_vibration_partition_function_theta_nh3(theta, temperature):
    t = temperature
    coverage = [0, 1/6, 2/6, 3/6, 4/6, 5/6, 6/6, 7/6, 8/6, 9/6, 10/6, 11/6, 12/6, 13/6]
    qvs = [get_vibration_partition_function(hvs_surface, t), get_vibration_partition_function(hvs_1nh3, t), get_vibration_partition_function(hvs_2nh3, t), get_vibration_partition_function(hvs_3nh3, t), get_vibration_partition_function(hvs_4nh3, t), get_vibration_partition_function(hvs_5nh3, t), get_vibration_partition_function(hvs_6nh3, t), get_vibration_partition_function(hvs_7nh3, t), get_vibration_partition_function(hvs_8nh3, t), get_vibration_partition_function(hvs_9nh3, t), get_vibration_partition_function(hvs_10nh3, t), get_vibration_partition_function(hvs_11nh3, t), get_vibration_partition_function(hvs_12nh3, t), get_vibration_partition_function(hvs_13nh3, t)]
    f = interpolate.interp1d(coverage, qvs, kind='cubic')
    if theta < 0:
        qv = f(0)
    elif theta > 13/6:
        qv = f(13/6)
    else:
        qv = f(theta)
    return qv


def get_gas_molecular_partition_function_nh3(temperature):
    t = temperature
    qt = get_translation_partition_function(M_NH3, t, total_pressure)
    qr = get_rotation_partition_function_nonlinear(SIGMA_NH3, t, ROT_CONST_A_NH3, ROT_CONST_B_NH3, ROT_CONST_C_NH3)
    qv = get_vibration_partition_function(hvs_nh3_gas, t)
    gas_molecular_partition_function = qt * qr * qv
    return gas_molecular_partition_function


def get_rate_partition_function_term(temperature, theta):
    t = temperature
    qa = get_gas_molecular_partition_function_nh3(t)
    if theta < (1/6):
        q_star = get_vibration_partition_function_theta_nh3(0, t)
    else:
        q_star = get_vibration_partition_function_theta_nh3(theta - 1/6, t)
    qa_star = get_vibration_partition_function_theta_nh3(theta, t)
    partition_function_term = qa * q_star / qa_star
    return partition_function_term
print(get_rate_partition_function_term(240, 2))


def get_desportion_energy(theta):
    coverage = [1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6, 6 / 6, 7 / 6, 8 / 6, 9 / 6, 10 / 6, 11 / 6, 12 / 6, 13 / 6]
    e_dess = [e_des_1nh3, e_des_2nh3, e_des_3nh3, e_des_4nh3, e_des_5nh3, e_des_6nh3, e_des_7nh3, e_des_8nh3, e_des_9nh3, e_des_10nh3, e_des_11nh3, e_des_12nh3, e_des_13nh3]
    f = interpolate.interp1d(coverage, e_dess, kind='cubic')
    if theta < 1/6:
        desportion_energy = f(1/6)
    elif theta > 13/6:
        desportion_energy = f(13/6)
    else:
        desportion_energy = f(theta)
    return desportion_energy


def get_c_of_active_site_nh3(theta):
    if theta < 1/6:
        c_of_active_site = C_OF_ACTIVE_SITE
    elif 1/6 <= theta <= 1:
        c_of_active_site = C_OF_ACTIVE_SITE * (1 - (theta - 1 / 6))
    else:
        c_of_active_site = C_OF_ACTIVE_SITE * 3
    return c_of_active_site


def get_rate_const_adsorption_nh3(temperature, theta):
    t = temperature
    rate_const_adsorption = total_pressure / (np.sqrt(2 * np.pi * M_NH3 * KB_J * t) * get_c_of_active_site_nh3(theta))
    return rate_const_adsorption


def get_v(temperature, theta):
    v = get_rate_partition_function_term(temperature, theta) * get_rate_const_adsorption_nh3(temperature, theta)
    return v


def get_desorption_rate(temperature, theta):
    t = temperature
    kads = get_rate_const_adsorption_nh3(t, theta)
    q = get_rate_partition_function_term(t, theta)
    e_des = get_desportion_energy(theta)
    desorption_rate = kads * q * math.exp(-e_des / (KB_EV * t)) * theta
    return desorption_rate



# # detail
# def get_spectra(temperature, theta):
#     # beta = 3K/s, scan_step = 1/1500sec
#     t = temperature
#     while True:
#         print('%8f' % t + " " + '%8f' % theta + " * " + '%8f' % get_desorption_rate(t, theta))
#         dthetadt_1 = get_desorption_rate(t, theta)
#         theta = theta + get_desorption_rate(t, theta) * (1 / 1500)
#         t = t + 0.002
#         dthetadt_2 = get_desorption_rate(t, theta)
#         if -0.05 < (dthetadt_1 - dthetadt_2) / (1/1500) < 0.01:
#             t = t + 1
#             theta = theta + get_desorption_rate(t, theta) * (1 / 3)
#         if t > 800.0:
#             break

def get_spectra(temperature, theta):
    # beta = 3K/s, scan_step = 1/2400sec
    t = temperature
    while True:
        print('%8f' % t + " " + '%8f' % theta + " -- " + '%8f' % get_desorption_rate(t, theta))
        dthetadt_1 = get_desorption_rate(t, theta)
        theta = theta + get_desorption_rate(t, theta) * (1 / 2400)
        t = t + 0.00125
        dthetadt_2 = get_desorption_rate(t, theta)
        if -0.005 < (dthetadt_1 - dthetadt_2) / (1 / 2400) < 0.005:
            t = t + 1
            theta = theta + get_desorption_rate(t, theta) * (1 / 3)
        if t > 800.0:
            break

# # medium
# def get_spectra(temperature, theta):
#     # beta = 3K/s, scan_step = 1/60sec
#     t = temperature
#     while True:
#         # print(t, theta, get_desorption_rate(t, theta))
#         # print(round(t, 4), round(theta, 6), round(get_desorption_rate(t, theta), 6))
#         print('%6f' % t, '%6f' % theta, '%8f' % get_desorption_rate(t, theta))
#         theta = theta + get_desorption_rate(t, theta) * (1 / 60)
#         t = t + 0.05
#         if t > 700.0:
#             break


# # rough
# def get_spectra(temperature, theta):
#     # beta = 3K/s, scan_step = 1/3sec
#     t = temperature
#     # ts = []
#     # thetas = []
#     # desorption_rates = []
#     while True:
#         # desorption_rates.append(get_desorption_rate(t, theta))
#         # ts.append(t+1)
#         # thetas.append(theta + get_desorption_rate(t, theta) * (1/3))
#         # print(t, theta, get_desorption_rate(t, theta))
#         print('%6f' % t, '%6f' % theta, '%8f' % get_desorption_rate(t, theta))
#         theta = theta + get_desorption_rate(t, theta) * (1 / 3)
#         t = t + 1
#         if t > 700.0:
#             break

