import os

from pythonScripts import extract_features, MetricsComputation
from pythonScripts.KNNregression import KNNregression
from pythonScripts.extract_features import Extract
from pythonScripts.plotFeature import plotFeatures
import time

dir = "dataset"
experiments = os.listdir(dir)
cnt = 0
for exp in experiments:
    cnt+=1
    folder = dir + "/" + exp
    print("Start --> exp:" + str(cnt) + ";" + exp)
    start_time = time.time()
    x = extract_features.Extract(folder + "/Participant", folder + "/Participant_raw_features.csv")
    y = extract_features.Extract(folder + "/Computer", folder + "/Computer_raw_features.csv")
    # x = plotFeatures(folder + "/Participant_raw_features.csv",1,feature)
    # y = plotFeatures(folder + "/Computer_raw_features.csv",1,feature)
    x = KNNregression.KNNregression(folder + "/Participant_raw_features.csv", folder + "/Participant_raw_features_KNN.csv", 7)
    y = KNNregression.KNNregression(folder + "/Computer_raw_features.csv", folder + "/Computer_raw_features_KNN.csv", 7)
    # x = plotFeatures(folder + "/Participant_raw_features_KNN.csv",1,feature)
    # y = plotFeatures(folder + "/Computer_raw_features_KNN.csv",1,feature)
    x = MetricsComputation.getMetrics(folder + "/Participant_raw_features_KNN.csv", folder + "/Computer_raw_features_KNN.csv", folder + "/")
    print("End(Time) --> exp:" + str(cnt) + ";" + exp + ", " + str(time.time() - start_time))
