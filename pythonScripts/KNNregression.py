import os
import csv
import pandas as pd
import math
import numpy as np



class KNNregression:
    k = 7
    column_list = ['voiceID', 'startTime', 'endTime', 'avgTime', 'meanF0Hz', 'stdevF0Hz', 'HNR', 'localJitter',
                   'localabsoluteJitter', 'rapJitter',
                   'ppq5Jitter', 'ddpJitter', 'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer',
                   'apq11Shimmer', 'ddaShimmer', 'meanPitch', 'maxPitch', 'minPitch',
                   'meanIntensity', 'maxIntensity', 'minIntensity']

    def __init__(self, filename, outputfileName, k):
        self.k = k

        df = pd.read_csv(filename)
        columns = df.columns
        data = []
        for column in columns:
            data.append([])

        end_time = math.floor(df.to_dict()["endTime"][len(df.to_dict()["endTime"]) - 1])
        print("end_time: " + str(end_time))
        time = 0
        dfIndex = 0
        dfsize = len(df.to_dict().get("voiceID"))
        while time < end_time:
            time += 1
            data[0].append(str(time - 1) + "-" + str(time))
            data[1].append(time - 1)
            data[2].append(time)
            avgTime = ((time - 1) + time) / 2
            data[3].append(avgTime)
            # calculates the data to be put in
            for variable in range(4, len(columns)):
                ## finds the knn nearest indices
                indices = self.lookForKNN(df, dfIndex, avgTime, dfsize, variable)
                # print(indices)
                avgVal = 0
                for i in indices:
                    avgVal += df.loc[i][columns[variable]]
                avgVal = avgVal / self.k
                data[variable].append(avgVal)

            if time > df.loc[dfIndex][2]:
                dfIndex += 1

            dfnew = pd.DataFrame(np.column_stack(data),
                              columns=self.column_list)  # add these lists to pandas in the right order
            # Write out the updated dataframe
            dfnew.to_csv(outputfileName, index=False)

    def lookForKNN(self, df, index, avgTime, dfSize, variable):
        indices = []
        indexUp = index
        while(math.isnan(float(df.loc[indexUp][variable])) or float(df.loc[indexUp][variable]) == -1):
            indexUp+= 1
            if (indexUp >= dfSize):
                indexUp = -1
                break

        indexDown = index - 1

        if(index == 0):
            indexDown = 0

        while (float(df.loc[indexDown][variable]) == -1 or math.isnan(float(df.loc[indexDown][variable]))):
            indexDown -= 1
            if(indexDown < 0):
                indexDown = -1
                break

        onlyDown = False
        onlyUp = False
        while(len(indices) < self.k):
            if(indexUp != -1):
                diffup = abs(float(df.loc[indexUp]["avgTime"]) - avgTime)
            else:
                diffup = float('inf')
            if(indexDown != -1):
                diffDown = abs(float(df.loc[indexDown]["avgTime"]) - avgTime)
            else:
                diffDown = float('inf')
            if(indexUp == -1 and indexDown == -1):
                raise Exception("Out of bounds")

            if((diffup < diffDown and not onlyDown) or (onlyUp and not onlyDown)):
                indices.append(indexUp)
                if(not indexUp>=dfSize - 1):
                    indexUp += 1
                    while (float(df.loc[indexUp][variable]) == -1 or math.isnan(float(df.loc[indexUp][variable]))):
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




#print(data)
