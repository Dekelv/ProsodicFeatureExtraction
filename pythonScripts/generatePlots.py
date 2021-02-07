import os
import numpy as np
from pythonScripts import extract_features, MetricsComputation, standardizeData
from pythonScripts import KNNregression
from pythonScripts.plotFeature import plotFeatures
import time
from pythonScripts.cleanData import CleanData
from pythonScripts.readCSV import readTimestampCSV
from pythonScripts.disperseData import disperseData
from pythonScripts.plotsMaker import plotsMaker
dir = "Metrics/Nash5- Human/"
experiments = os.listdir(dir)
cnt = 0

column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR',
               'localJitter', 'localabsoluteJitter', 'rapJitter',
               'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
               'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
               'meanIntensity', 'maxIntensity', 'minIntensity']

featureName = 'meanPitch'
for f in range(len(column_list)):
    if column_list[f] == featureName:
        feature = f
        break

plotMaker = plotsMaker()
plotMaker.readDataFromFile(dir + "Computer_raw_features_disp.csv",column_list)
plotMaker.readDataFromFile(dir + "Participant_raw_features_disp.csv",column_list)
# plotMaker.readDataFromFile(dir + "Computer_raw_features_KNN2.csv", column_list)

# plotMaker.readDataFromFile(dir + "Computer_raw_features_KNN4.csv", column_list)
plotMaker.readDataFromFile(dir + "Computer_raw_features_KNN7.csv", column_list)
plotMaker.readDataFromFile(dir + "Participant_raw_features_KNN7.csv", column_list)

data = np.genfromtxt(dir + "Participant_raw_features.csv", delimiter=',', dtype=float, names=column_list)
data = np.array(np.asarray(data.tolist())).transpose()
shift = data[1][1]
# plotMaker.plot(3, 1, feature, color="purple", marker="_", shift=shift)
# data = np.genfromtxt(dir + "Computer_raw_features.csv", delimiter=',', dtype=float, names=column_list)
# data = np.array(np.asarray(data.tolist())).transpose()
# shift = data[1][1]
# print(shift)
#plotMaker.plot(1, 3, feature, color="b", marker="_", shift=0)
plotMaker.scatter(0, 3, feature, color="salmon", marker=(4, 0, 45), shift=0)
plotMaker.scatter(1, 1, feature, color="skyblue", marker=(4, 0, 45), shift=0)
plotMaker.plot(2, 1, feature, color="r", marker="_", shift=0)
plotMaker.plot(3, 1, feature, color="b", marker="_", shift=0)


plotMaker.setLabels("Time(s)", yLabel="Mean Pitch(Hz)", title="kNN(k=7) vs. original feature values")
plotMaker.setLegend(["kNN(k=7) (Participant)","kNN(k=7) (Human-Teacher)","Utterance Feature Data (Participant)", "Utterance Feature Data (Human-Teacher)"])
plotMaker.show()