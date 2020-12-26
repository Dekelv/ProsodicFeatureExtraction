import numpy as np
import matplotlib.pyplot as plt
column_list = ['voiceID','startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
                     'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                     'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                     'meanIntensity', 'maxIntensity', 'minIntensity']
data = np.genfromtxt('KNNCSVFiles/processed_results.csv',delimiter=',', dtype = float, names=column_list)
print(data["startTime"][1:])
print(data["meanPitch"][1:])
plt.plot(data["startTime"][1:],data["meanPitch"][1:])
plt.show()