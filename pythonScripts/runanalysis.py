import os

from pythonScripts import extract_features, MetricsComputation
from pythonScripts import KNNregression
from pythonScripts.plotFeature import plotFeatures
import time
from readCSV import readTimestampCSV

dir = "dataset"
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

    # Determine first timestamp by using the csv file.
    participantTimestamps = timestamps.getFolderInfo(exp)
    # Extract computer first. Then use the timestamps to determine the last timestamp.
    y = extract_features.Extract(folder + "/Computer", folder + "/Computer_raw_features.csv")

    # Determine latest non_silence in computer and then add 20 seconds. Calculate relative timestamp for participant and append to array
    # First non silent segment is first question. Last non silent segment is last question.
    firstNonsilence = y.non_silences[0][0]
    lastNonsilence = y.non_silences[len(y.non_silences)-1][1] + 20
    experimentLength = (lastNonsilence - firstNonsilence)
    # Calculate difference and add it to participantTimestamp[1]. You now have the first and last timestamp in experiment.
    firstParticipant = participantTimestamps[1]
    lastParticipant = participantTimestamps[1] + experimentLength

    # Then calculate participant timestamps by adding the participant delay.
    firstParticipant = firstParticipant + participantTimestamps[2]
    lastParticipant = lastParticipant + participantTimestamps[2]

    x = extract_features.Extract(folder + "/Participant", folder + "/Participant_raw_features.csv", [firstParticipant, lastParticipant])

    x = plotFeatures(folder + "/Participant_raw_features.csv",1,feature, "(Participant Raw)Time vs. " + featureName, "Time(s)", featureName)
    y = plotFeatures(folder + "/Computer_raw_features.csv",1,feature, "(Computer Raw)Time vs. " + featureName, "Time(s)", featureName)
    x = KNNregression.KNNregression(folder + "/Participant_raw_features.csv", folder + "/Participant_raw_features_KNN.csv", 7)
    y = KNNregression.KNNregression(folder + "/Computer_raw_features.csv", folder + "/Computer_raw_features_KNN.csv", 7)
    x = plotFeatures(folder + "/Participant_raw_features_KNN.csv",1,feature, "(Participant KNN)Time vs. " + featureName, "Time(s)", featureName)
    y = plotFeatures(folder + "/Computer_raw_features_KNN.csv",1,feature, "(Computer KNN)Time vs. " + featureName, "Time(s)", featureName)
    x = MetricsComputation.getMetrics(folder + "/Participant_raw_features_KNN.csv", folder + "/Computer_raw_features_KNN.csv", folder + "/")
    print("End(Time) --> exp:" + str(cnt) + ";" + exp + ", " + str(time.time() - start_time))
