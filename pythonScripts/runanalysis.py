import os
from pythonScripts import extract_features, MetricsComputation, standardizeData
from pythonScripts import KNNregression
import time
from pythonScripts.readCSV import readTimestampCSV
import argparse

parser=argparse.ArgumentParser()

parser.add_argument('--runDirectory', '-dir', help='give a directory that contains experiment sub directories, each subdirectory should contain File1 and File2', default= "")
parser.add_argument('--File1', '-f1',help='name of first file', default= "")
parser.add_argument('--File2', '-f2', help='name of second file', default= "")
parser.add_argument('--k', help='k value for the kNN regression', default= 7)

args=parser.parse_args()

column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR',
               'localJitter', 'localabsoluteJitter', 'rapJitter',
               'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
               'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
               'meanIntensity', 'maxIntensity', 'minIntensity']

def runFiles(folder, file1, file2, k):
    x = standardizeData.standardizeData(folder + "/" + file1 + "_raw_features.csv", folder + "/" + file1 + "_zscore_features.csv")
    y = standardizeData.standardizeData(folder + "/" + file2 + "_raw_features.csv", folder + "/" + file2 + "_zscore_features.csv")
    x = KNNregression.KNNregression(folder + "/" + file1 + "_raw_features.csv", folder + "/" + file1 + "_raw_features_knn(" + str(k) + ").csv", k)
    y = KNNregression.KNNregression(folder + "/" + file2 + "_raw_features.csv", folder + "/" + file2 + "_raw_features_knn(" + str(k) + ").csv", k)
    x = KNNregression.KNNregression(folder + "/" + file1 + "_zscore_features.csv", folder + "/" + file1 + "_zscore_features_knn(" + str(k) + ").csv", k)
    y = KNNregression.KNNregression(folder + "/" + file2 + "_zscore_features.csv", folder + "/" + file2 + "_zscore_features_knn(" + str(k) + ").csv", k)
    x = MetricsComputation.getMetrics(exp, folder + "/Participant_zscore_features_KNN" + str(k) + ".csv", folder + "/Computer_zscore_features_KNN" + str(k) + ".csv", folder + "/Participant_raw_features_KNN" + str(k) + ".csv", folder + "/Computer_raw_features_KNN" + str(k) + ".csv", folder + "/results(K=" + str(k) + ").csv")

def extractFeatures(folder, file1):
    x = extract_features.Extract(folder + "/" + file1, folder + "/" + file1 + "_raw_features.csv")

# timestamps = readTimestampCSV()

folder = args.runDirectory

if(folder == ""):
    if(args.File1 != ""):
        extractFeatures(folder, args.File1)

    if(args.File2 != ""):
        extractFeatures(folder, args.File2)

    if(args.File1 != "" and args.File1 != ""):
        runFiles(folder, args.File1, args.File2, args.k)
else:
    cnt = 0
    experiments = os.listdir(folder)
    for exp in experiments:
        print("Start --> exp:" + str(cnt) + ";" + exp)
        start_time = time.time()
        dir = folder + "/" + exp
        if (args.File1 != ""):
            extractFeatures(dir, args.File1)

        if (args.File2 != ""):
            extractFeatures(dir, args.File2)

        if (args.File1 != "" and args.File1 != ""):
            runFiles(dir, args.File1, args.File2, args.k)
        print("End(Time) --> exp:" + str(cnt) + ";" + exp + ", " + str(time.time() - start_time))

