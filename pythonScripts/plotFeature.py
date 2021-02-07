import numpy as np
import matplotlib.pyplot as plt

class plotFeatures:
    def __init__(self, fileName, feature1 , feature2, title, xAxis, yAxis):
        column_list = ['voiceID','startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR',
                        'localJitter', 'localabsoluteJitter', 'rapJitter',
                             'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                             'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                             'meanIntensity', 'maxIntensity', 'minIntensity']

        data = np.genfromtxt(fileName,delimiter=',', dtype = float, names=column_list)
        data = np.array(np.asarray(data.tolist())).transpose()
        plt.plot(data[feature1][1:],data[feature2][1:],marker='.',color='b',)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show()
