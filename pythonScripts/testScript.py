from pythonScripts import KNNregression
from pythonScripts import extract_features
from pythonScripts import MetricsComputation
import os

from pythonScripts.plotFeature import plotFeatures
import time
start_time = time.time()
file1 = ""
file2 = ""
folder = "testAudioFiles"

column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR',
               'localJitter', 'localabsoluteJitter', 'rapJitter',
               'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
               'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
               'meanIntensity', 'maxIntensity', 'minIntensity']

feature = 0
featureName = 'meanPitch'
for f in range(len(column_list)):
    if column_list[f] == 'meanPitch':
        feature = f
        break
# print(os.listdir("testAudioFiles"))
# x = extract_features.Extract(folder + "/Participant", folder + "/Participant_raw_features.csv")
# y = extract_features.Extract(folder + "/Computer", folder + "/Computer_raw_features.csv")
x = plotFeatures(folder + "/Participant_raw_features.csv",1,feature, "(Participant Raw)Time vs. " + featureName, "Time(s)", featureName)
y = plotFeatures(folder + "/Computer_raw_features.csv",1,feature, "(Computer Raw)Time vs. " + featureName, "Time(s)", featureName)
x = KNNregression.KNNregression(folder + "/Participant_raw_features.csv", folder + "/Participant_raw_features_KNN.csv", 7)
y = KNNregression.KNNregression(folder + "/Computer_raw_features.csv", folder + "/Computer_raw_features_KNN.csv", 7)
x = plotFeatures(folder + "/Participant_raw_features_KNN.csv",1,feature, "(Participant KNN)Time vs. " + featureName, "Time(s)", featureName)
y = plotFeatures(folder + "/Computer_raw_features_KNN.csv",1,feature, "(Computer KNN)Time vs. " + featureName, "Time(s)", featureName)
x = MetricsComputation.getMetrics(folder + "/Participant_raw_features_KNN.csv", folder + "/Computer_raw_features_KNN.csv", folder + "/")

print("--- %s seconds ---" % (time.time() - start_time))
