import os

from pythonScripts import extract_features, MetricsComputation, standardizeData
from pythonScripts import KNNregression
from pythonScripts.plotFeature import plotFeatures
import time
from pythonScripts.cleanData import CleanData
from pythonScripts.readCSV import readTimestampCSV
from pythonScripts.disperseData import disperseData
dir = "Metrics"
experiments = os.listdir(dir)
cnt = 0

column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR',
               'localJitter', 'localabsoluteJitter', 'rapJitter',
               'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
               'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
               'meanIntensity', 'maxIntensity', 'minIntensity']

feature = 0
featureName = 'meanPitch'
for f in range(len(column_list)):
    if column_list[f] == featureName:
        feature = f
        break

timestamps = readTimestampCSV()

for exp in experiments:
    cnt+=1
    folder = dir + "/" + exp
    print("Start --> exp:" + str(cnt) + ";" + exp)
    start_time = time.time()

    experimentIdentifier = exp

   # x = extract_features.Extract(folder + "/Participant", folder + "/Participant_raw_features.csv", [firstParticipant, lastParticipant])
    x = standardizeData.standardizeData(folder + "/Participant_raw_features.csv", folder + "/Participant_zscore_features.csv")
    y = standardizeData.standardizeData(folder + "/Computer_raw_features.csv", folder + "/Computer_zscore_features.csv")
   # x = disperseData(folder + "/Participant_raw_features.csv", folder + "/Participant_raw_features_disp.csv") THIS IS STILL USING RAW INSTEAD OF ZSCORE
   # y = disperseData(folder + "/Computer_raw_features.csv", folder + "/Computer_raw_features_disp.csv") THIS IS STILL USING RAW INSTEAD OF ZSCORE
   # x = plotFeatures(folder + "/Participant_raw_features_disp.csv",1,feature, "(Participant Raw)Time vs. " + featureName, "Time(s)", featureName) THIS IS STILL USING RAW INSTEAD OF ZSCORE
   # y = plotFeatures(folder + "/Computer_raw_features_disp.csv",1,feature, "(Computer Raw)Time vs. " + featureName, "Time(s)", featureName) THIS IS STILL USING RAW INSTEAD OF ZSCORE
    x = KNNregression.KNNregression(folder + "/Participant_zscore_features.csv", folder + "/Participant_zscore_features_KNN.csv", 7)
    y = KNNregression.KNNregression(folder + "/Computer_zscore_features.csv", folder + "/Computer_zscore_features_KNN.csv", 7)
   # x = plotFeatures(folder + "/Participant_raw_features_KNN.csv",1,feature, "(Participant KNN)Time vs. " + featureName, "Time(s)", featureName) THIS IS STILL USING RAW INSTEAD OF ZSCORE
   # y = plotFeatures(folder + "/Computer_raw_features_KNN.csv",1,feature, "(Computer KNN)Time vs. " + featureName, "Time(s)", featureName) THIS IS STILL USING RAW INSTEAD OF ZSCORE
    x = MetricsComputation.getMetrics(exp, folder + "/Participant_zscore_features_KNN.csv", folder + "/Computer_zscore_features_KNN.csv", folder + "/")
    print("End(Time) --> exp:" + str(cnt) + ";" + exp + ", " + str(time.time() - start_time))

file1 = open("Metrics_Total_File.csv", "+a")
file1.write("Experiment ID,feature,Proximity,Convergence,convergence_pvalue\n")
for exp in experiments:
    f2 = open(dir + "/" + exp + "/" + "proximityConvergence.csv")
    for line in f2.readlines()[1:]:
        file1.write(line)

