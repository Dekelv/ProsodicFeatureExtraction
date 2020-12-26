import os
import csv
import pandas as pd
import math
import numpy as np

dir = "originalCSVFiles"
csvFiles = os.listdir(dir)

k = 7
column_list = ['voiceID','startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter', 'localabsoluteJitter', 'rapJitter',
                     'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                     'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                     'meanIntensity', 'maxIntensity', 'minIntensity']


def lookForKNearest(df, index, avgTime, dfSize, variable):
    indices = []
    indexUp = index
    while(df.loc[indexUp][variable] == -1 or math.isnan(df.loc[indexUp][variable])):
        indexUp+= 1
        if (indexUp > dfSize):
            raise Exception("index up greater than dfSize")
    indexDown = index - 1

    if(index == 0):
        indexDown = 0

    while (df.loc[indexDown][variable] == -1 or math.isnan(df.loc[indexDown][variable])):
        indexDown -= 1
        if(indexDown < 0):
            raise Exception("index down lower than 0")

    onlyDown = False
    onlyUp = False
    while(len(indices) < k):
        diffup = abs(df.loc[indexUp]["avgTime"] - avgTime)
        diffDown = abs(df.loc[indexDown]["avgTime"] - avgTime)

        if((diffup < diffDown and not onlyDown) or (onlyUp and not onlyDown)):
            indices.append(indexUp)
            if(not indexUp>=dfSize - 1):
                indexUp += 1
                while (df.loc[indexUp][variable] == -1 or math.isnan(df.loc[indexUp][variable])):
                    indexUp += 1
                    if (indexUp >= dfSize - 1):
                        onlyDown = True
                        break
            else:
                onlyDown = True
        elif(not onlyUp):
            indices.append(indexDown)
            if (indexDown != 0):
                indexDown -= 1
                while (df.loc[indexDown][variable] == -1 or math.isnan(df.loc[indexDown][variable])):
                    indexDown -= 1
                    if (indexDown < 0):
                        onlyUp = True
                        break
            else:
                onlyUp = True
        else:
            raise Exception("cannot find another index to go to")
    return indices


for file in csvFiles:
    df = pd.read_csv(dir + "/" + file)
    columns = df.columns
    data = []
    for column in columns:
        data.append([])

    end_time = math.floor(df.to_dict()["endTime"][len(df.to_dict()["endTime"])-1])
    time = 0
    dfIndex = 0
    dfSize = len(df.to_dict().get("voiceID"))
    while time < end_time:
        time += 1
        data[0].append(str(time-1) + "-" + str(time))
        data[1].append(time-1)
        data[2].append(time)
        avgTime = ((time - 1) + time)/2
        data[3].append(avgTime)
        # calculates the data to be put in
        for variable in range(4, len(columns)):
            ## finds the knn nearest indices
            indices = lookForKNearest(df, dfIndex, avgTime, dfSize, variable)
            #print(indices)
            avgVal = 0
            for i in indices:
                avgVal += df.loc[i][columns[variable]]
            avgVal = avgVal/k
            data[variable].append(avgVal)

        if time > df.loc[dfIndex][1]:
            dfIndex += 1

    df = pd.DataFrame(np.column_stack(data),
                columns=column_list)  # add these lists to pandas in the right order
    # Write out the updated dataframe
    df.to_csv("KNNCSVFiles/" + file, index=False)

#print(data)
