import numpy as np
import matplotlib.pyplot as plt

class plotFeatures:
    def __init__(self, fileName, feature1 , feature2):
        column_list = ['voiceID','startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
                             'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                             'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                             'meanIntensity', 'maxIntensity', 'minIntensity']

        data = np.genfromtxt(fileName,delimiter=',', dtype = float, names=column_list)
        print(data[1][50])
        plt.plot(data[feature1][1:],data[column_list[feature2]][1:])
        plt.show(data)